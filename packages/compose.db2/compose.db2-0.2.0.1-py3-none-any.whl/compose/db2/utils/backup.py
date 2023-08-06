import json
import os
from compose.db2.utils.cloudUtils import S3Resource
from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.db2rc import db2_cmd_execution
from compose.db2.utils.sqlUtils import Db2SQL, Db2Utils
from compose.db2 import configuration
from compose.db2.utils.hadr import Db2HADR
from cdb import log
from kubernetes import client as kubeclient
from kubernetes import config as kubeconfig
from compose.db2.utils.setup_utils import check_size

logger = log.get_logger(__name__)


class Db2backup(DB2Commands):
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        DB2Commands.__init__(self, conf=self.conf)

    @log.log_execution(logger)
    def db2_cfg_backup(self, cfg):
        r = json.loads(cfg)
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.update_db_cfg(**r))
        logger.info(cmd.replace(self.dbuser, "xxxxxx").
                    replace(self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def db2_force_apps(self):
        cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
                                                     self.attach_to_dbnode(),
                                                     self.forceconns)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").
                    replace(self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_deactivate_db(self):
        cmd = "runuser -l {0} -c \"{1};{2} {3}\"".format(self.dbuser,
                                                         self.attach_to_dbnode(),
                                                         self.deactivatedb,
                                                         self.creds)

        logger.info(cmd.replace(self.dbuser, "xxxxxx").
                    replace(self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def db2_terminate(self):
        cmd = "runuser -l {0} -c \"{1}\"".format(self.dbuser,
                                                 self.terminate)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
            self.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @log.log_execution(logger)
    def db2_activate_db(self):
        cmd = "runuser -l {0} -c \"{1};{2} {3}\"".format(self.dbuser,
                                                         self.attach_to_dbnode(),
                                                         self.activatedb,
                                                         self.creds)
        logger.info(cmd.replace(self.dbuser, "xxxxxx").
                    replace(self.using, "xxxxxx"))
        try:
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def check_staging_space(self):
        disk_sz = check_size()
        if int(disk_sz[2]/1024/1024/1024) > 5:
            logger.info("More than 5 Gb disk spae is required to stage backup, disk free space is {} GB".format(
                int(disk_sz[2]/1024/1024/1024)))
        else:
            logger.info("Atleast 5 Gb disk spae is required to stage backup, disk free space is {} GB".format(
                int(disk_sz[2]/1024/1024/1024)))
            raise ValueError("Atleast 5 Gb disk spae is required to stage backup, disk free space is {} GB".format(
                int(disk_sz[2]/1024/1024/1024)))

    @log.log_execution(logger)
    def take_db_backup(self, backup_data=''):
        logger.info(
            "received args {}, verifying disk space for staging".format(backup_data))
        self.check_staging_space()
        if backup_data:
            r = json.loads(backup_data)
            if "backup_id" not in r:
                raise ValueError("Missing required `backup_id`")

        backup_cmd = self.db2_backup_cmd(use_alias=True)
        logger.info(
            "We are in Db2oC Backup Code Path, running  backupcmd {}".format(backup_cmd))
        sqlutils = Db2Utils()

        try:

            result = sqlutils.do_sysproc_admincmd(sql=backup_cmd)
            logger.info(
                "db2 backup result, timestamp of backup:{}".format(result))
            if backup_data:
                restore_data = self.get_last_backup_data()
                self.set_restore_data(backup_data, restore_data)
        except Exception as e:
            raise(e)
        finally:
            self.db2_terminate()

    @log.log_execution(logger)
    def get_last_backup_data(self):
        return json.dumps({"restore_time": "{0}".
                           format(self.db2_latest_bkp_for_bs())})

    @log.log_execution(logger)
    def set_restore_data(self, backup_data, restore_data):
        if not isinstance(restore_data, str):
            raise TypeError(
                "restoreData is expected to be of type `str`, got {}".format(
                    type(restore_data)))
        try:
            db2_table_count = self.get_db2_table_count()[0]['TABLES']
            logger.info(
                "Total number of tables on the db2 instance: {}".format(db2_table_count))
            backup_times = self.get_db2_backup_times()[0]
            duration_time = backup_times['DURATION_SECS']
            start_time = backup_times['START_TIME']
            logger.info(
                "Total duration time in seconds: {}".format(duration_time))
            backup_data_json = json.loads(backup_data)
            logger.info(backup_data_json)
            backup_id = backup_data_json['backup_id']
            restore_data = json.loads(restore_data)
            restore_time = restore_data['restore_time']

            if (str(start_time) == str(restore_time)):
                backup_size = self.backup_size(start_time)
                logger.info(
                    "Total backup size in bytes: {}".format(backup_size))

            restore_data['table_count'] = db2_table_count
            restore_data['duration_time'] = duration_time

            cli = kubeclient.CustomObjectsApi(
                kubeclient.ApiClient(kubeconfig.load_incluster_config()))
            cli.patch_namespaced_custom_object(
                self.conf['crd_group'],
                'v1',
                self.conf['account'],
                'backups',
                name=backup_id,
                body={'spec': {
                    'restore_data': json.dumps(restore_data),
                    'size_in_bytes': backup_size
                }})
        except Exception as e:
            logger.error(e)
            if self.conf['type'] == "dv":
                pass
            else:
                raise (e)

    @log.log_execution(logger)
    def get_restore_data_forbackupid(self, backup_data):
        logger.info("Validating restore data for backup ran")
        r = json.loads(backup_data)
        backup_id = r['backup_id']
        restore_data = {}
        try:
            cli = kubeclient.CustomObjectsApi(
                kubeclient.ApiClient(kubeconfig.load_incluster_config()))
            backup_results = cli.list_namespaced_custom_object(
                self.conf['crd_group'],
                'v1',
                self.conf['account'],
                'backups',
                pretty="true",
                label_selector="formation_id={}".format(self.conf['id']))

            restore_info = [item['spec']['restore_data']
                            for item in backup_results['items'] if item['metadata']['name'] == backup_id]
            if restore_info:
                restore_data = json.loads(restore_info[0])
                logger.info("There is backup {} associated to backup_id {}".format(
                    restore_data['restore_time'], backup_id))
            return restore_data
        except Exception as e:
            logger.error(
                "Validating backup failed with {} for backup_id {}".format(e, backup_id))

    def gen_server_side_ks_bkp(self, db2_keystore_loc, id):
        cmds = DB2Commands()
        ks_path = os.path.dirname(
            os.path.realpath(self.conf['db2_keystore_loc']))
        files_to_bkp = os.listdir(ks_path)
        subdir = 'CSYS.{}'.format(self.conf['id'].upper())
        bkp_list = []
        for fl in files_to_bkp:
            source = os.path.join(ks_path, fl)
            target = "{0}/HADRPrimary/{1}".format(subdir, fl)
            bkp_list.append(cmds.gen_db2remstmgr_cmds(action='put',
                                                      source=source,
                                                      target=target))
        return bkp_list

    def gen_server_side_ks_restore(self, db2_keystore_loc, id):
        cmds = DB2Commands()
        ks_path = os.path.dirname(
            os.path.realpath(self.conf['db2_keystore_loc']))
        files_to_bkp = os.listdir(ks_path)
        subdir = 'CSYS.{}'.format(self.conf['id'].upper())
        bkp_list = []
        for fl in files_to_bkp:
            target = os.path.join(ks_path, fl)
            source = "{0}/HADRPrimary/{1}".format(subdir, fl)
            bkp_list.append(cmds.gen_db2remstmgr_cmds(action='get',
                                                      source=source,
                                                      target=target))
        return bkp_list

    def gen_mgmt_side_ks_bkp(self, db2_keystore_loc, id):
        cmds = S3Resource(self.conf)
        ks_path = os.path.dirname(
            os.path.realpath(self.conf['db2_keystore_loc']))
        files_to_bkp = os.listdir(ks_path)
        subdir = 'CSYS.{}'.format(self.conf['id'].upper())
        bkp_list = []
        for fl in files_to_bkp:
            source = os.path.join(ks_path, fl)
            target = "{0}/HADRPrimary/{1}".format(subdir, fl)
            bkp_list.append(cmds.s3action(action='put',
                                          source=source,
                                          target=target))

        return bkp_list

    def gen_mgmt_side_ks_restore(self, db2_keystore_loc, id):
        cmds = S3Resource(self.conf)
        ks_path = os.path.dirname(
            os.path.realpath(self.conf['db2_keystore_loc']))
        files_to_bkp = os.listdir(ks_path)
        subdir = 'CSYS.{}'.format(self.conf['id'].upper())
        bkp_list = []
        for fl in files_to_bkp:
            target = os.path.join(ks_path, fl)
            source = "{0}/HADRPrimary/{1}".format(subdir, fl)
            bkp_list.append(cmds.s3action(action='put',
                                          source=source,
                                          target=target))
        return bkp_list

    def db2_latest_bkp_for_bs(self):
        hadr = Db2HADR(self.conf)
        tstamp = 12345678910
        sqls = Db2SQL(self.conf)
        query = sqls.db2_latest_backup
        try:
            real_tstamp = sqls.run_desired_select_sql(
                hadr.build_primary_host(), query)
            if real_tstamp:
                return real_tstamp[0].get(0)
            return tstamp
        except Exception:
            return tstamp

    def get_db2_table_count(self):
        try:
            sql = Db2SQL(self.conf)
            table_count = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                                     query=sql.tables_count,
                                                     fetch='assoc')
            return table_count
        except Exception as e:
            logger.error(e)
            raise (e)
        return None

    def get_db2_backup_times(self):
        try:
            sql = Db2SQL(self.conf)
            query = sql.db2_get_backup_times
            db_backups = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                                    query=query,
                                                    fetch='assoc')
            return db_backups
        except Exception as e:
            logger.error(e)
            raise (e)
        return None
