import shlex
import subprocess
import json
import re
import itertools
from cdb import log
from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.db2rc import SQLError, db2_cmd_execution
from compose.db2.utils.setup_utils import cleanup_dir, check_size
from compose.db2.utils.util_funcs import run_cmd
from compose.db2.utils.hadr import Db2HADR
from compose.db2 import configuration

logger = log.get_logger(__name__)


class Db2Restore(DB2Commands):
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        DB2Commands.__init__(self, conf=conf)

    @log.log_execution(logger)
    def list_available_backups_in_cos(self, restore_data):
        r = json.loads(restore_data)
        if r['isCopy']:
            cos = {'cos_endpoint': r['cos']['cos_endpoint'],
                   'cos_region': r['cos']['cos_region'],
                   'cos_access_key': r['cos']['cos_access_key'],
                   'cos_bucket': r['cos']['cos_bucket'],
                   'cos_secret_access_key': r['cos']['cos_secret_access_key']}
            filter = "{0}/{1}".format(self.bdir, "BLUDB.0")
            output, rc = run_cmd(self.s3action('ls', filter, **cos))
            if rc == 0:
                data = output.decode("utf-8").split("\n")
                stamps = [i.split(".")[-2] for i in data if i]
                return [k for k, _ in itertools.groupby(sorted(stamps,
                                                               reverse=True))]
        else:
            return self.backup_list()

    # function to get the closest backup for a PIT
    @log.log_execution(logger)
    def get_closest_bkp_forcopy(self, restore_data):
        r = json.loads(restore_data)
        if r['isCopy'] and (r['rfopt'] == "pit"):
            logger.info(
                "rfopt {} is passed for Copy, checking the "
                "closest backup".format(r['rfopt']))
            # backup time is 20200526073632
            # pit stamp to be passed is 2020-05-26T07:36:09Z
            backup_list = self.list_available_backups_in_cos(restore_data)
            if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', r['ts']):
                logger.info(
                    "ts {} passed for pit matches format".format(r['ts']))
                converted_ts = r['ts'].replace(
                    "-", '').replace(":", '').replace("T", '').replace("Z", '')
                logger.info("converted ts is {}".format(converted_ts))
                closest_bkp = max(
                    [i for i in backup_list if converted_ts >= i])
            if closest_bkp:
                logger.info("identified closest backup {0} for {1}".format(
                    closest_bkp, converted_ts))
                return closest_bkp

    @ log.log_execution(logger)
    def validate_backup_for_restore(self, restore_data):
        r = json.loads(restore_data)
        disk_info = check_size()
        backups = self.list_available_backups_in_cos(restore_data)
        if r['rfopt'] in ("eob", "eol"):
            if r['ts'] in backups:
                logger.info(
                    "found backup that is associated to request "
                    "ts {}".format(r['ts']))
                if not r['isCopy']:
                    logger.info(
                        "Validating disk capacity for restoring "
                        "backup {}".format(r['ts']))
                    backup_sz = self.backup_size(r['ts'])
                    if disk_info[2] > backup_sz:
                        logger.info(
                            "free disk space on /mnt is {0} than backup "
                            "sz {1}".format(disk_info[2], backup_sz))
                    else:
                        raise ValueError("There is not enough free space {0} "
                                         "on /mnt disk to restore backup {1} "
                                         "which is of size "
                                         "{2}".format(disk_info[2],
                                                      r['ts'],
                                                      backup_sz))
                else:
                    logger.info(
                        "We are running copy, so skipping backup sz validation")
            else:
                logger.error(
                    "failed to find a ts for backup, ts got in the request "
                    "is {}".format(r['ts']))
                logger.error("available backups are {}".format(str(backups)))
                raise ValueError(
                    "didn't find backup that is associated to "
                    "request {}".format(r['ts']))

        elif r['rfopt'] == "pit":
            if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', r['ts']):
                logger.info("PIT restore is requested for {}".format(r['ts']))
                if not r['isCopy']:
                    latest_bkp = max(backups)
                    backup_sz = self.backup_size(latest_bkp)
                    logger.info(
                        "Validating disk capacity for restoring "
                        "backup {}".format(latest_bkp))
                    if disk_info[2] > backup_sz:
                        logger.info(
                            "free disk space on /mnt is {0} than backup "
                            "sz {1}".format(disk_info[2], backup_sz))
                    else:
                        raise ValueError("There is not enough free space {0} "
                                         "on /mnt disk to restore backup {1} "
                                         "which is of size "
                                         "{2}".format(disk_info[2],
                                                      latest_bkp,
                                                      backup_sz))
                else:
                    logger.info(
                        "We are running pit and copy, skipping backup sz check")
            else:
                logger.error(
                    "{} timestamp for pit is not valid".format(r['ts']))
                raise ValueError(
                    "{} timestamp for pit is not valid".format(r['ts']))

    @ log.log_execution(logger)
    def clean_logtarget(self):
        cleanup_dir(self.opath)

    @ log.log_execution(logger)
    def stop_hadr(self):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standby"):
            cmd = "runuser -l {0} -c \"{1}; {2} {3}\"".format(self.dbuser,
                                                              self.attach_to_dbnode(),
                                                              self.stophadr,
                                                              self.creds
                                                              )
            logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
                self.using, "xxxxxx"))
            db2_cmd_execution(cmd)

    @ log.log_execution(logger)
    def db2_archive_log(self):
        if self.conf['type'] == "dv":
            cmd = "runuser -l {0} -c \"{1}; {2}\"".format(self.dbuser,
                                                          self.attach_to_dbnode(),
                                                          self.runarchive)
        else:
            cmd = "runuser -l {0} -c \"{1}; {2} {3}\"".format(self.dbuser,
                                                              self.attach_to_dbnode(),
                                                              self.runarchive,
                                                              self.creds)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def start_hadrs(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.start_hadr_s)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def start_hadrp(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.start_hadr_p_f)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def db2_terminate(self):
        cmd = "runuser -l {0} -c \"{1}\"".format(self.dbuser,
                                                 self.terminate)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def db2_uncatalog(self):
        cmd = "runuser -l {0} -c \"{1}\"".format(self.dbuser,
                                                 self.uncatalog)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def db2_force_apps(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.forceconns)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            for i in range(5):
                logger.info(
                    "attempting to force connections for iteration:{}".format(i))
                db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def list_active_database(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.activedbs
                                                     )
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_deactivate_db(self):
        cmd = "runuser -l {0} -c \"{1}; {2} {3}\"".format(self.dbuser,
                                                          self.attach_to_dbnode(),
                                                          self.deactivatedb,
                                                          self.creds
                                                          )

        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def quiesce_db2_instance(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.quiesceinstance)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def quiesce_db2_admincmd(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(
            self.dbuser,
            self.attach_to_dbnode(),
            self.run_admin_cmd("quiesce db immediate"))
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_quiesce_db(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(
            self.dbuser,
            self.connect_db_remote(),
            self.quiescedb)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_unquiesce_db(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(
            self.dbuser,
            self.connect_db_remote(),
            self.unquiescedb)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_drop_db_remote(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.dropdb)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def restore_db(self, restore_data):
        r = json.loads(restore_data)
        if (r['rfopt'] == "pit") and not r['isCopy']:
            logger.info("restore to PIT is requested")
            restore_cmd = self.db2_recover_cmd(**r)
        elif (r['rfopt'] in ("eob", "eol")) or (r['isCopy']):
            logger.info("restore to {0} and isCopy:{1}".format(
                r['rfopt'], r['isCopy']))
            restore_cmd = self.db2_restore_cmd(**r)
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     restore_cmd)
        if (r['isCopy']) and (r['rfopt'] == "pit"):
            bkp_for_pit = self.get_closest_bkp_forcopy(restore_data)
            logger.info("We are in Copy for PIT so replacing "
                        "{} with {}".format(r['ts'], bkp_for_pit))
            cmd = cmd.replace(r['ts'], bkp_for_pit)
        if r['isCopy']:
            logger.info(cmd.replace(self.dbuser, "xxxxxx").
                        replace(self.using, "xxxxxx").
                        replace(self.auth1, "xxxxxx").
                        replace(self.auth2, "xxxxxx").
                        replace(r['cos']['cos_access_key'], "xxxxxx").
                        replace(r['cos']['cos_secret_access_key'], "xxxxxx"))
        else:
            logger.info(cmd.replace(self.dbuser, "xxxxxx").
                        replace(self.using, "xxxxxx").
                        replace(self.auth1, "xxxxxx").
                        replace(self.auth2, "xxxxxx"))
        try:
            for retry in range(3):
                logger.info(
                    "performing iteration {} for restore".format(retry))
                try:
                    result = subprocess.run(shlex.split(cmd),
                                            universal_newlines=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            check=True,
                                            shell=False)
                    if result.returncode == 0:
                        logger.info("Restore ran successfully with {}".format(
                            result.stdout.replace('\n', '')))
                        break
                except subprocess.CalledProcessError as Ex:
                    msg = Ex.output
                    logger.error("restore cmd ran into {}".format(msg))
                    sqlcode = SQLError(str(msg)).sqlwarnerr()
                    if sqlcode == "SQL1035N":
                        logger.info("retrying restore here "
                                    "because of {}".format(sqlcode))
                        self.db2_force_apps()
                        self.db2_deactivate_db()
                        self.stop_hadr()
                    elif sqlcode == "SQL4970N":
                        logger.info("Rollforward ran into {} and "
                                    "requires to do rf and "
                                    "stop".format(sqlcode))
                        self.rfstop_exception()
                        break
                    else:
                        logger.info(
                            "Restore Failed with {} retrying here".format(sqlcode))
                        raise Exception(
                            "Restore Failed with {} retrying here".format(sqlcode))
                        break  # break since we don't know if we can continue
            else:
                logger.error("maxed out attempts to retry, still "
                             "failing "
                             "with{}".format(result.stdout.replace('\n', '')))
                raise ("Restore Failed with {}".format(
                    result.stdout.replace('\n', '')))
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def rollforward_db(self, restore_data):
        rf_cmd = ""
        r = json.loads(restore_data)
        if r['rfopt'] in ("eob", "eol"):
            logger.info("We are in rollforward for {}".format(r['rfopt']))
            rf_cmd = self.db2_rollforward_db_cmd(rfopt=r['rfopt'])
            rf_cmd = "runuser -l {0} -c \"{1}; {2}\"".format(self.dbuser,
                                                             self.attach_to_dbnode(),
                                                             rf_cmd)
        elif (((r['rfopt'] == "pit") and (r['isCopy'])) or
              ((r['rfopt'] == "eol") and (r['isCopy']))):
            logger.info("We are in Copy and PIT so replacing the ts with "
                        "{}".format(r['ts'].replace("T", '').replace("Z", '')))
            rf_cmd = self.db2_recover_cmd(**r)
            rf_cmd = "runuser -l {0} -c \"{1}; {2}\"".format(self.dbuser,
                                                             self.attach_to_dbnode(),
                                                             rf_cmd)
        logger.info(rf_cmd.replace(
            self.dbuser, "xxxxxx").replace(self.using, "xxxxxx"))
        if rf_cmd:
            try:
                result = subprocess.run(shlex.split(rf_cmd),
                                        universal_newlines=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        check=True,
                                        shell=False)
                if result.returncode == 0:
                    logger.info("Rollforward ran successfully with {}".format(
                        result.stdout.replace('\n', '')))
            except subprocess.CalledProcessError as Ex:
                self.rfquery_status()
                msg = Ex.output
                warn_code = SQLError(str(msg)).sqlwarnerr()
                if warn_code in SQLError(str(msg)).sqlignore_error_codes.keys():
                    logger.info(msg)
                    pass
                elif warn_code == "SQL4970N":
                    logger.info("Rollforward ran into {} and "
                                "requires to do rf and "
                                "stop".format(warn_code))
                    self.rfstop_exception()
                elif warn_code == "SQL1265N":
                    logger.info("Rollforward ran into {} and "
                                "requires to rf to eob and "
                                " stop".format(warn_code))
                    self.rf_eob_stop()
                elif warn_code == "SQL1275N":
                    logger.info("Rollforward ran into {} and "
                                "requires to do rf eob and "
                                "complete".format(warn_code))
                    self.rf_eob_complete()
                elif warn_code == "SQL1274N":
                    logger.info("Rollforward ran into {} and "
                                "requires to do rf eol and "
                                "complete".format(warn_code))
                    self.rf_eol_complete()
                    logger.info("Rollforward ran successfully with {}".format(
                        msg.replace('\n', '')))
                else:
                    logger.info("Rollforward Failed with{}".format(warn_code))
                    raise(Ex)
            except Exception as e:
                logger.error("Rollforward failed to run")
                raise(e)
            finally:
                self.db2_terminate()

    @ log.log_execution(logger)
    def rfstop_exception(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.rfstop)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def rfquery_status(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.rfquery)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def rf_eob_complete(self):
        rf_cmd = self.db2_rollforward_db_cmd('eob')
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     rf_cmd)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def rf_eob_stop(self):
        rf_cmd = self.db2_rollforward_db_cmd('eob', action='STOP')
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     rf_cmd)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxxx"))
        try:
            result = subprocess.run(shlex.split(cmd),
                                    universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    check=True,
                                    shell=False)
            if result.returncode == 0:
                logger.info("Rf_eob_stop ran successfully with {}".format(
                    result.stdout.replace('\n', '')))
        except subprocess.CalledProcessError as Ex:
            msg = Ex.output
            warn_code = SQLError(str(msg)).sqlwarnerr()
            if warn_code == "SQL4970N":
                logger.info("Rf_eob_stop ran into {} and "
                            "requires to do rf and "
                            "stop".format(warn_code))
                self.rfstop_exception()
        except Exception as e:
            logger.error("Rf_eob_stop failed to run")
            raise(e)
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def rf_eol_complete(self):
        rf_cmd = self.db2_rollforward_db_cmd('eol')
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     rf_cmd)
        logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(
            self.using, "xxxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @ log.log_execution(logger)
    def restore_history_file(self, restore_data):
        r = json.loads(restore_data)
        hfile = self.db2_restore_hist_file(**r)
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     hfile)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()
