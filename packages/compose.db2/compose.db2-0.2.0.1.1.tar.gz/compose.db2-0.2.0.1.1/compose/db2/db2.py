from compose.db2.users import create_oldap_pw
from compose.db2 import configuration, formation
from compose.db2.utils import util_funcs, setup_utils
import json
import os
import pwd
import re
import shlex
import subprocess
import jinja2
import datetime
from cdb.utils.file import executable_opener

from kubernetes import client as kubeclient
from kubernetes import config as kubeconfig

import cdb.service
from cdb import log
from cdb import backup_k8s
from compose.db2.debroni import Debroni
from compose.db2.utils.backup import Db2backup
from compose.db2.utils.restore import Db2Restore
from compose.db2.utils.sqlUtils import Db2Utils, Db2SQL
from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.db2rc import SQLError, runCmdException, db2_cmd_execution
from compose.db2.utils.hadr import Db2HADR

logger = log.get_logger(__name__)


class Db2:
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf

    def write_init_sql(self, sqlf, values=None):
        j2env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__, 'resources'))
        if values is None:
            values = dict(list(self.conf.items()))
        base = j2env.get_template(sqlf)
        with open('%s/%s' % (self.conf['conf_dir'], sqlf), 'w', opener=executable_opener) as f:
            f.write(base.render(**values))
        cmd = "chmod 775 %s/%s" % (self.conf['conf_dir'], sqlf)
        subprocess.check_call(shlex.split(cmd), shell=False)

    def db_summary(self):
        """
           Get a summary of the database for performance
           analysis with a 30 second duration
        """
        utils = Db2Utils()
        output = utils.get_summary('30')
        print(output)
        pass

    def write_db2u_config_var(self, values=None):
        """keeping jinja env in case we need to do var replacement later"""
        j2env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__, 'resources'))
        if values is None:
            values = dict(list(self.conf.items()))

        base = j2env.get_template('db2u-config-var.cfg')
        with open(self.conf['db2u_configmap_loc'], 'w', opener=executable_opener) as f:
            f.write(base.render(**values))
        cmd = 'chmod 755 %s' % self.conf['db2u_configmap_loc']
        subprocess.check_call(shlex.split(cmd), shell=False)

    def write_read_only_replica_configuration(self, r):
        pass

    def write_hadr_configuration(self, values=None):
        j2env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__, 'resources'))
        if values is None:
            values = dict(list(self.conf.items()))
            values['designated_role'] = Db2HADR(values).set_designated_role()
            values['db2_hadr_cfg'] = self.get_db2_hadr_setup_config(
                values['designated_role'])
            values['db2_backres_cmd'] = self.get_db2_backup_restore_cmd_init(values['designated_role'],
                                                                             self.db2_latest_bkp_for_bs())
        if values['designated_role'] == "PRIMARY":
            hasql = "prihasetup.sql"
        elif values['designated_role'] == "STANDBY":
            hasql = "sbyhasetup.sql"
        base = j2env.get_template('%s' % hasql)
        with open('%s/%s' % (self.conf['conf_dir'], hasql), 'w', opener=executable_opener) as f:
            f.write(base.render(**values))
        cmd = "chmod 740 %s/%s" % (self.conf['conf_dir'], hasql)
        subprocess.check_call(shlex.split(cmd), shell=False)

    def write_required_conf(self, fname, subdirectory=None, values=None):
        j2env = jinja2.Environment(
            loader=jinja2.PackageLoader(__package__, 'resources'))
        if values is None:
            values = dict(list(self.conf.items()))
            values['designated_role'] = Db2HADR(values).set_designated_role()
        base = j2env.get_template(fname)
        if subdirectory is not None:
            fname = '%s/%s' % (subdirectory, fname)
        with open('%s/%s' % (self.conf['conf_dir'], fname), 'w', opener=executable_opener) as f:
            f.write(base.render(**values))
        cmd = '/bin/chown -R ibm:ibm %s' % (
            os.path.join(self.conf['conf_dir'], fname))
        subprocess.check_call(shlex.split(cmd), shell=False)
        cmd = "chmod 740 %s/%s" % (self.conf['conf_dir'], fname)
        subprocess.check_call(shlex.split(cmd), shell=False)

    def write_db2u_conf(self, fname, mode=740, values=None):
        j2env = jinja2.Environment(loader=jinja2.PackageLoader(
            __package__, 'resources'), keep_trailing_newline=True)
        if values is None:
            values = dict(list(self.conf.items()))
            values['designated_role'] = Db2HADR(values).set_designated_role()
        base = j2env.get_template(fname)
        with open('%s/%s' % (self.conf['db2u_config_path'], fname), 'w', opener=executable_opener) as f:
            f.write(base.render(**values))
        cmd = '/bin/chown -R ibm:ibm %s' % (
            os.path.join(self.conf['db2u_config_path'], fname))
        subprocess.check_call(shlex.split(cmd), shell=False)
        cmd = "chmod %d %s/%s" % (mode, self.conf['db2u_config_path'], fname)
        subprocess.check_call(shlex.split(cmd), shell=False)

    def write_lite_users_file(self):
        user_file = "/mnt/blumeta0/db2_config/users.json"
        user_file_plugin = "/mnt/blumeta0/plugin/users.json"
        user_file_compose = "/mnt/blumeta0/compose/users.json"

        if not os.path.exists(user_file_compose):
            cmd = 'mkdir /mnt/blumeta0/compose'
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = 'cp %s %s' % (user_file, user_file_compose)
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = '/bin/chown -R ibm:ibm %s' % (user_file_compose)
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = 'chmod 740 %s' % (user_file_compose)
            subprocess.check_call(shlex.split(cmd), shell=False)

        if not os.path.exists(user_file_plugin):
            cmd = 'mkdir /mnt/blumeta0/plugin'
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = 'cp %s %s' % (user_file, user_file_plugin)
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = '/bin/chown -R ibm:ibm %s' % (user_file_plugin)
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = 'chmod 740 %s' % (user_file_plugin)
            subprocess.check_call(shlex.split(cmd), shell=False)

    def write_users_file(self, values=None, lite=False):
        user_file = "/mnt/blumeta0/db2_config/users.json"
        if os.path.exists(user_file):
            if lite:
                self.write_lite_users_file()

            pass
        else:
            j2env = jinja2.Environment(loader=jinja2.PackageLoader(
                __package__, 'resources'), keep_trailing_newline=True)
            if values is None:
                values = dict(list(self.conf.items()))
                values['designated_role'] = Db2HADR(
                    values).set_designated_role()
            values["db2inst1_hashed_password"] = create_oldap_pw(
                values["compose_password"])
            base = j2env.get_template("users.json")
            with open(user_file, 'w') as f:
                f.write(base.render(**values))
            cmd = '/bin/chown -R ibm:ibm %s' % (user_file)
            subprocess.check_call(shlex.split(cmd), shell=False)
            cmd = "chmod 740 %s" % (user_file)
            subprocess.check_call(shlex.split(cmd), shell=False)

            if lite:
                self.write_lite_users_file()

    def convert_to_read_only_replica(self, source_data):
        r = json.loads(source_data)
        self.write_read_only_replica_configuration(r['conninfo'])
        if 'cos' in r:
            self.run_restore(source_data)

    def run_catalog_on_client(self):
        self.setup_mgmt_side_ssl()
        self.db2_configure_mgmt_ssl()
        self.setup_dsdriver()
        cmds = DB2Commands(self.conf)
        run_cmds = []
        run_cmds.append(cmds.generate_catalog_node_commands(ssl=False))
        run_cmds.append(cmds.generate_catalog_db_commands(ssl=False))
        run_cmds.append(cmds.generate_catalog_node_commands())
        run_cmds.append(cmds.generate_catalog_db_commands())
        for cmd in run_cmds:
            cmd = "runuser -l {0} -c \"{1}\"".format(
                cmds.dbuser, cmd)
            try:
                subprocess.check_call(shlex.split(cmd), shell=False)
            except subprocess.CalledProcessError:
                try:
                    subprocess.check_output(shlex.split(cmd),
                                            stderr=subprocess.STDOUT,
                                            shell=False)
                except subprocess.CalledProcessError as e:
                    msg = e.output
                    if SQLError(str(msg)).sqlwarnerr() == "SQL1018N":
                        logger.info(msg)
                        pass
            except Exception as e:
                raise(e)
            finally:
                cmd = "runuser -l {0} -c \"{1}\"".format(
                    cmds.dbuser, cmds.terminate)
                db2_cmd_execution(cmd)

    def run_backup(self, backup_data):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            self.run_catalog_on_client()
            db_backup = Db2backup(self.conf)
            try:
                db_backup.take_db_backup(backup_data)
            except Exception as e:
                logger.error(e)
                raise e
        else:
            logger.info(
                "detected role is {} ignoring backup".format(designated_role))

    def validate_backup_run(self, backup_data):
        designated_role = Db2HADR(self.conf).set_designated_role()
        restore_info = {}
        if designated_role.lower() in ("primary", "standard"):
            db_backup = Db2backup(self.conf)
            try:
                restore_info = db_backup.get_restore_data_forbackupid(
                    backup_data)
                if 'restore_time' in restore_info:
                    logger.info("Successfully validated backup")
                else:
                    raise ValueError("restore_data is invalid {}".format(
                        json.dumps(restore_info)))
                return restore_info
            except Exception as e:
                logger.error(e)
                raise e
        else:
            logger.info(
                "detected role is {} ignoring backup validation".format(designated_role))

    def change_backup_config(self, cfg_data):
        self.run_catalog_on_client()
        db_backup = Db2backup(self.conf)
        try:
            db_backup.db2_cfg_backup(cfg_data)
        except Exception as e:
            logger.error(e)
            raise e

    @ log.log_execution(logger)
    def run_restore(self, restore_data):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            self.run_catalog_on_client()
            db_restore = Db2Restore(self.conf)
            try:
                db_restore.validate_backup_for_restore(restore_data)
                db_restore.clean_logtarget()
                db_restore.db2_force_apps()
                db_restore.db2_archive_log()
                db_restore.db2_quiesce_db()
                db_restore.db2_deactivate_db()
                db_restore.stop_hadr()
                db_restore.restore_db(restore_data)
                db_restore.rollforward_db(restore_data)
                db_restore.db2_unquiesce_db()
                # db_restore.clean_hadrprimary_bkp_files()
            except Exception as e:
                logger.error(e)
                raise e

    @ log.log_execution(logger)
    def backup_usersJson(self):
        pass

    @ log.log_execution(logger)
    def copy_usersJson(self, restore_data, success=(0,)):
        cmds = DB2Commands(self.conf)
        r = json.loads(restore_data)
        with open("/mnt/blumeta0/db2_config/users.json") as f:
            db2inst_pw = json.load(f)["users"]["db2inst1"]["password"]
        cos = {'cos_endpoint': r['cos']['cos_endpoint'],
               'cos_region': r['cos']['cos_region'],
               'cos_access_key': r['cos']['cos_access_key'],
               'cos_bucket': r['cos']['cos_bucket'],
               'cos_secret_access_key': r['cos']['cos_secret_access_key']}
        userfile = "{0}/{1}".format(cmds.bdir, "users.json")
        getcmd = cmds.s3action(
            'get', userfile, '/mnt/blumeta0/db2_config', **cos)
        listcmd = cmds.s3action(
            'ls', userfile, **cos)
        try:
            logger.info("running cmd "
                        "{}".format(listcmd.
                                    replace(self.conf['cos_access_key'],
                                            "xxxxxx").
                                    replace(self.conf['cos_secret_access_key'],
                                            "xxxxxx").
                                    replace(r['cos']['cos_access_key'],
                                            "xxxxxx").
                                    replace(r['cos']['cos_secret_access_key'],
                                            "xxxxxx")))
            output, brc = util_funcs.run_cmd(listcmd)
            if brc in success and output:
                logger.info("running cmd "
                            "{}".format(getcmd.
                                        replace(self.conf['cos_access_key'],
                                                "xxxxxx").
                                        replace(self.conf['cos_secret_access_key'],
                                                "xxxxxx").
                                        replace(r['cos']['cos_access_key'],
                                                "xxxxxx").
                                        replace(r['cos']['cos_secret_access_key'],
                                                "xxxxxx")))
                output, brc = util_funcs.run_cmd(getcmd)
                if brc in success:
                    logger.info("Downloaded users.json to target")
                    logger.info("resotring db2inst1 password")
                    read_user_file = open(
                        "/mnt/blumeta0/db2_config/users.json", "r")
                    user_json = json.load(read_user_file)
                    read_user_file.close()
                    user_json["users"]["db2inst1"]["password"] = db2inst_pw
                    write_user_file = open(
                        "/mnt/blumeta0/db2_config/users.json", "w")
                    json.dump(user_json, write_user_file)
                    write_user_file.close()
                    logger.info("restored successfully")
            else:
                logger.info(
                    "{} not found in COS skipping get".format(userfile))
        except Exception as e:
            raise(e)

    @ log.log_execution(logger)
    def run_copy(self, restore_data):
        # {'ts':"time to restore","rfopt":"eob|pit|eol","isCopy":true, "cos":{"cos_endpoint"}}
        r = json.loads(restore_data)
        try:
            if r['cos']:
                logger.info("cos arg is passed validating the cos information")
                for arg in r['cos'].items():
                    if not arg[1]:
                        raise ValueError(
                            "one of the args {0} value {1} is either empty or "
                            "not valid".format(arg[0], arg[1]))
        except KeyError:
            raise ValueError(
                "cos information is required for cos, args passed are {} not "
                "valid".format(restore_data))
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            self.run_catalog_on_client()
            db_restore = Db2Restore(self.conf)

            try:
                db_restore.validate_backup_for_restore(restore_data)
                db_restore.clean_logtarget()
                db_restore.db2_force_apps()
                db_restore.db2_archive_log()
                db_restore.db2_quiesce_db()
                db_restore.db2_deactivate_db()
                db_restore.stop_hadr()
                db_restore.restore_db(restore_data)
                db_restore.rollforward_db(restore_data)
                db_restore.db2_unquiesce_db()
                # db_restore.clean_hadrprimary_bkp_files()
            except Exception as e:
                logger.error(e)
                raise e

    @ log.log_execution(logger)
    def configure_hadr(self):
        db2cmds = DB2Commands(self.conf)
        cmd = "runuser -l {0} -c \"{1}; db2 \'{2}\'\"".format(db2cmds.dbuser,
                                                              db2cmds.attach_to_dbnode(),
                                                              self.conf['db2_hadr_cfg'])
        logger.info(cmd.replace(db2cmds.dbuser, "xxxxxx").
                    replace(db2cmds.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @ log.log_execution(logger)
    def run_buildback(self):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if self.conf['db2_setup_type'] == "ha" and designated_role.lower() == "standby":
            restore_info = {}
            time_to_restore = self.db2_latest_bkp_for_bs()
            restore_info.update(
                {"ts": int("{0}".format(time_to_restore)), "rfopt": "eob", "isCopy": False})
            restore_info = json.dumps(restore_info)
            db_restore = Db2Restore(self.conf)
            try:
                self.run_catalog_on_client()
                db_restore.db2_terminate()
                db_restore.clean_logtarget()
                db_restore.db2_force_apps()
                db_restore.db2_deactivate_db()
                db_restore.stop_hadr()
                # db_restore.db2_drop_db_remote()
                db_restore.restore_db(restore_info)
                self.configure_hadr()
                db_restore.start_hadrs()
            except Exception as e:
                logger.error(e)
                raise e
        else:
            logger.info("buildback is not required for plan {}".format(
                self.conf['db2_setup_type']))

    def create_folder(self, folder_path):
        os.makedirs('%s' % (folder_path))
        cmd = '/bin/chown -R ibm:ibm %s' % folder_path
        subprocess.check_call(shlex.split(cmd), shell=False)
        cmd = '/bin/chmod -R 0775 %s' % folder_path
        subprocess.check_call(shlex.split(cmd), shell=False)

    def create_db2_data_dirs(self):
        paths = ['/mmt/bludata0/db2',
                 '/mnt/bludata0/db2/RemoteStorage',
                 '/mnt/bludata0/db2/log',
                 '/mnt/bludata0/db2/overflow',
                 '/mnt/bludata0/db2/backup',
                 '/mnt/bludata0/db2/databases',
                 '/mnt/bludata0/db2/archive_log',
                 '/mnt/blutmp0/db2',
                 '/mnt/blutmp0/db2/temp_tablespace',
                 '/mnt/blumeta0/db2',
                 '/mnt/blumeta0/db2/ssl_keystore',
                 '/mnt/blumeta0/db2/copy',
                 '/mnt/blumeta0/db2/scripts/',
                 '/mnt/blumeta0/configmap',
                 '/mnt/blumeta0/configmap/db2u',
                 '/mnt/blumeta0/configmap/db2',
                 '/mnt/blumeta0/db2_config',
                 '/mnt/blumeta0/options',
                 '/mnt/blumeta0/db2/audit',
                 '/conf/db2oc/debroni']
        paths.append(self.conf['db2_ks_path'])
        paths.append(self.conf['mgmt_keystore_path'])
        for path in paths:
            try:
                self.create_folder(path)
            except FileExistsError:
                pass

    def create_symlinks(self):
        paths = {
            '/mnt/bludata0/db2/log': '/mnt/blumeta0/db2/log',
            '/mnt/bludata0/db2/RemoteStorage': '/mnt/blutmp0/db2/RemoteStorage',
            '/mnt/bludata0/db2/databases': '/mnt/blumeta0/db2/databases',
            '/mnt/bludata0/db2/backup': '/mnt/blumeta0/db2/backup',
            '/mnt': '/data'
        }

        for path in paths:
            try:
                os.symlink(path, paths[path])
            except FileExistsError:
                pass
            except Exception as e:
                logger.error("Symlink error: {}".format(repr(e)))
                raise e

    # generate db and hadr health report using MON_GET_HADR
    def check_db_health(self):
        pass

    def converge_settings(self):
        pass

    def gen_server_side_ks_bkp(self):
        db_backup = Db2backup(self.conf)
        cmds = db_backup.gen_mgmt_side_ks_bkp(self.conf['db2_keystore_loc'],
                                              self.conf['id'])
        return cmds

    def gen_server_side_ks_restore(self):
        db_backup = Db2backup(self.conf)
        cmds = db_backup.gen_mgmt_side_ks_bkp(self.conf['db2_keystore_loc'],
                                              self.conf['id'])
        return cmds

    def gen_mgmt_side_ks_bkp(self):
        db_backup = Db2backup(self.conf)
        cmds = db_backup.gen_mgmt_side_ks_bkp(self.conf['db2_keystore_loc'],
                                              self.conf['id'])
        return cmds

    def gen_mgmt_side_ks_restore(self):
        db_backup = Db2backup(self.conf)
        cmds = db_backup.gen_mgmt_side_ks_bkp(self.conf['db2_keystore_loc'],
                                              self.conf['id'])
        return cmds

    def db2_force_applications(self):
        try:
            restore_cmds = Db2Restore(self.conf)
            restore_cmds.db2_force_apps()
        except Exception as e:
            raise(e)

    def db2_backup_info(self):
        """ query backups from recipes"""
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            try:
                cos = DB2Commands(self.conf)
                """
                backup_data = self.get_backups_k8s_resources()
                sorted([logger.info(ts) for ts in backup_data.keys()
                        if not re.match(r"FAILED_BACKUP\d{1,3}", ts)], reverse=True)
                """
                [logger.info(ts) for ts in cos.backup_list()]
            except Exception as e:
                logger.error(e)
                raise(e)

    def db2_ha_status(self):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() == "primary":
            try:
                sql = Db2SQL(self.conf)
                status = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                                    query=sql.ha_status,
                                                    fetch='assoc')
                if status:
                    fmtn = formation.Formation(
                        self.conf['crd_group'], self.conf['account'], self.conf['id'])
                    logger.info("ha status is {}".format(status))
                    for idx in range(len(status)):
                        # separate check for DR node
                        if(status[idx]['STANDBY_ID'] == 3 and status[idx]['HADR_STATE'] == 'DISCONNECTED'):
                            logger.info("the DR node is currently disconnected. \
                                Please run a buildback to resync standby {} at {}".format(
                                        status[idx]['STANDBY_ID'], fmtn.get_disaster_recovery_site()))
                            continue

                        hadr_sync_mode = status[idx]['HADR_SYNCMODE']
                        if hadr_sync_mode == "SYNC" and (status[idx]['HADR_STATE'] != "PEER" or
                                                         status[idx]['HADR_CONNECT_STATUS'] != "CONNECTED"):
                            raise ValueError(
                                'Db2 {} node is not healthy'.format(hadr_sync_mode))
                        elif hadr_sync_mode == "SUPERASYNC" and (status[idx]['HADR_STATE'] != "REMOTE_CATCHUP" or
                                                                 status[idx]['HADR_CONNECT_STATUS'] != "CONNECTED"):
                            raise ValueError(
                                'Db2 {} node is not healthy'.format(hadr_sync_mode))
                        else:
                            if hadr_sync_mode == "SYNC" and (status[idx]['HADR_STATE'] == "PEER" or
                                                             status[idx]['HADR_CONNECT_STATUS'] == "CONNECTED"):
                                if status[idx]['PRIMARY_LOG_FILE'] != status[idx]['STANDBY_LOG_FILE'] != status[idx]['STANDBY_REPLAY_LOG_FILE']:
                                    raise ValueError('Db2 {} node logs files are not in sync PRIMARY_LOG_FILE:{},STANDBY_LOG_FILE:{},STANDBY_REPLAY_LOG_FILE:{}'.format(
                                        hadr_sync_mode, status[idx]['PRIMARY_LOG_FILE'], status[idx]['STANDBY_LOG_FILE'], status[idx]['STANDBY_REPLAY_LOG_FILE']))
                            elif hadr_sync_mode == "SUPERASYNC" and (status[idx]['HADR_STATE'] == "REMOTE_CATCHUP" or
                                                                     status[idx]['HADR_CONNECT_STATUS'] == "CONNECTED"):
                                if status[idx]['PRIMARY_LOG_FILE'] != status[idx]['STANDBY_LOG_FILE'] != status[idx]['STANDBY_REPLAY_LOG_FILE']:
                                    raise ValueError('Db2 {} node logs files are not in sync PRIMARY_LOG_FILE:{},STANDBY_LOG_FILE:{},STANDBY_REPLAY_LOG_FILE:{}'.format(
                                        hadr_sync_mode, status[idx]['PRIMARY_LOG_FILE'], status[idx]['STANDBY_LOG_FILE'], status[idx]['STANDBY_REPLAY_LOG_FILE']))

                else:
                    raise ValueError(
                        'Db2 returned invalid data from hadr query')
            except Exception as e:
                logger.error(e)
                raise (e)

    def db2_status(self):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            try:
                sql = Db2SQL(self.conf)
                status = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                                    query=sql.uptime,
                                                    fetch='assoc')
                if status:
                    logger.info("uptime check is {}".format(status))
                else:
                    raise ValueError(
                        'Db2 returned invalid data from uptime query')
            except Exception as e:
                logger.error(e)
                raise(e)

    @ log.log_execution(logger)
    def db2_check_ifpri_isup(self):
        try:
            sql = Db2SQL(self.conf)
            role = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                              query=sql.ha_role,
                                              fetch='assoc')
            if role:
                logger.info("role associated to {} is {}".format(
                    self.conf['fqdn'], role))
            else:
                raise ValueError(
                    'Could not validate role of {}'.format(self.conf['fqdn']))
        except Exception as e:
            logger.error(e)
            raise(e)

    def db2_adjust_scale_values(self, instance_memory=None):
        self.run_catalog_on_client()
        cmds = DB2Commands(self.conf)

        if instance_memory is None:
            mem_cmd = cmds.dbm_instance_mem_limit()
        else:
            mem_cmd = {'cfg': {"INSTANCE_MEMORY": instance_memory}}

        cmd = "runuser -l {0} -c \"{1};{2}\"".format(cmds.dbuser,
                                                     cmds.attach_to_dbnode(),
                                                     cmds.update_dbm_cfg(**mem_cmd))
        logger.info(cmd.replace(cmds.dbuser, "xxxxxx").
                    replace(cmds.using, "xxxxxx"))
        db2_cmd_execution(cmd, False, 3, 300, (0, 2))

    @ log.log_execution(logger)
    def db2_configure_mgmt_ssl(self):
        cmds = DB2Commands(self.conf)
        dbm_cfg = {"cfg": {"SSL_CLNT_KEYDB": format(self.conf['mgmt_keystore_loc']),
                           "SSL_CLNT_STASH": format(self.conf['mgmt_keystore_sth'])}}

        dbm_cfg = {"cfg": {"SSL_CLNT_KEYDB": "{}".format(self.conf['mgmt_keystore_loc']),
                           "SSL_CLNT_STASH": "{}".format(self.conf['mgmt_keystore_sth'])}}

        cmd = "runuser -l {0} -c \"{1}\"".format(self.conf['db2_sysadmin_user'],
                                                 cmds.update_dbm_cfg(
            **dbm_cfg))
        logger.info(cmd.replace(cmds.dbuser, "xxxxxx").
                    replace(cmds.using, "xxxxxx"))
        db2_cmd_execution(cmd)

    @ log.log_execution(logger)
    def setup_mgmt_side_ssl(self):
        if os.path.isfile(self.conf['db2_keystore_loc']) and not os.path.isfile(self.conf['mgmt_keystore_loc']):
            logger.info("{} doesn't exist copying over".format(
                self.conf['mgmt_keystore_loc']))
            setup_utils.cp_between_dir(
                self.conf['db2_keystore_loc'], self.conf['mgmt_keystore_loc'])
            os.chown(self.conf['mgmt_keystore_loc'],
                     pwd.getpwnam(self.conf['db2_sysadmin_user'])[2],
                     pwd.getpwnam(self.conf['db2_sysadmin_user'])[3])
        if os.path.isfile(self.conf['db2_keystore_sth']) and not os.path.isfile(self.conf['mgmt_keystore_sth']):
            logger.info("{} doesn't exist copying over".format(
                self.conf['mgmt_keystore_sth']))
            setup_utils.cp_between_dir(
                self.conf['db2_keystore_sth'], self.conf['mgmt_keystore_sth'])
            os.chown(self.conf['mgmt_keystore_sth'],
                     pwd.getpwnam(self.conf['db2_sysadmin_user'])[2],
                     pwd.getpwnam(self.conf['db2_sysadmin_user'])[3])

    @ log.log_execution(logger)
    def setup_dsdriver(self):
        cmds = DB2Commands(self.conf)
        if os.path.isfile(os.path.join(self.conf['conf_dir'], 'db2cli.sql')):
            logger.info("db2cli.sql found going to execute it")
            cmd = "runuser -l {0} -c \"db2 -tvf {1}\"".format(cmds.dbuser,
                                                              os.path.join(self.conf['conf_dir'], 'db2cli.sql'))
            logger.info(cmd.replace(cmds.dbuser, "xxxxxx").
                        replace(cmds.using, "xxxxxx"))
            db2_cmd_execution(cmd)

    def rotate_backups(self):
        """Triggers a backup rotation. It first fetches a list with all old k8s backup resources
        that should get deleted. Based on this list the COS bucket is getting cleaned up. Finally
        the k8s backup resources are deleted."""
        group = self.conf['crd_group']
        namespace = self.conf['account']
        formation_id = self.conf['id']
        retention_period_days = 14  # self.config['backup_retention_period']
        bup_k8s = backup_k8s.KubernetesBackups()
        try:
            old_backups = bup_k8s.get_backups_to_rotate(group,
                                                        namespace,
                                                        formation_id,
                                                        retention_period_days)
            logger.info("Found these old backups to rotate: '%s'",
                        [old_bup['metadata']['name'] for old_bup in old_backups])
            # Mark all old backups such that the dispatcher will ignore them
            for backup in old_backups:
                bup_k8s.mark_backup_for_deletion(
                    group, namespace, backup['metadata']['name'])

            logger.debug("Starting to delete old backups in k8s.")
            bup_k8s.delete_backups(group, namespace, old_backups)
        except Exception as ex:
            logger.exception("Could not rotate because of %s", str(ex))

    def get_backups_k8s_resources(self, include_incomplete=False):
        fmtn = formation.Formation(
            self.conf['crd_group'], self.conf['account'], self.conf['id'])
        return fmtn.get_backup_recipe_results(include_incomplete=include_incomplete)

    @ log.log_execution(logger)
    def get_lastknown_successful_backup(self):
        """ gets the last know good backup from the
        backup recipes ran"""
        fmtn = formation.Formation(
            self.conf['crd_group'], self.conf['account'], self.conf['id'])
        backups = fmtn.get_successful_backups()
        if len(backups) == 0:
            raise Exception("No successful backups found")
        return self.get_backups_k8s_resources(include_incomplete=True)[backups[0]]

    @ log.log_execution(logger)
    def backup_ifrequired(self, max_delta):
        """this is to set flag to buildback process to see if we need to take a new backup. max_delta is a datetime.timedelta"""
        fmtn = formation.Formation(
            self.conf['crd_group'], self.conf['account'], self.conf['id'])
        lastbackup = fmtn.get_successful_backups()[0]
        backup_time = datetime.datetime.strptime(
            self.get_backups_k8s_resources()[lastbackup]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')

        if datetime.datetime.now() - backup_time > max_delta:
            logger.info(
                "need a new backup, the backup {} is old ".format(lastbackup))
            self.run_backup(backup_data='')
        logger.info(
            "No need for a new backup, the backup {} is still new ".format(lastbackup))

    @ log.log_execution(logger)
    def run_a_select(self, query):
        designated_role = Db2HADR(self.conf).set_designated_role()
        if designated_role.lower() in ("primary", "standard"):
            r = json.loads(query)
            try:
                sql = Db2SQL(self.conf)
                query = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                                   query=r['sql'],
                                                   fetch='assoc')
                if query:
                    return query
            except Exception as e:
                raise(e)

    def get_db2_hadr_setup_config(self, designated_role):
        if designated_role in ("PRIMARY", "STANDBY"):
            cmds = DB2Commands(self.conf)
            cfg = cmds.generate_dbcfg_forhadr(designated_role)
            return cfg
        else:
            return "STANDARD"

    def get_db2_hadr_settings(self):
        # Need to use Debroni here to grab db cfgs because we run this on standby nodes.
        # We can't grab db cfgs via attach, and remote connection doesn't work because we can't
        # connect to standby databases.
        debroni = Debroni(self.conf)
        all_cfgs = debroni.get_db_cfgs()
        hadr_settings = {}
        hadr_cfgs = ['HADR_LOCAL_HOST', 'HADR_LOCAL_SVC', 'HADR_REMOTE_HOST', 'HADR_REMOTE_SVC',
                     'HADR_TARGET_LIST']
        for cfg in all_cfgs.params:
            if cfg.key in hadr_cfgs:
                hadr_settings[cfg.key] = cfg.value
        return hadr_settings

    def get_db2_backup_restore_cmd_init(self, designated_role, bkptime):
        if designated_role in ("PRIMARY", "STANDBY"):
            cmds = DB2Commands(self.conf)
            if designated_role == "PRIMARY":
                return cmds.backup_cmd
            elif designated_role == "STANDBY":
                return cmds.restore_cmd.replace("restoretime",
                                                str(bkptime))
        else:
            return "STANDARD"

    def db2_latest_bkp_for_bs(self):
        backup = Db2backup(self.conf)
        if (cdb.service.stat('db2') == "run"):
            return backup.db2_latest_bkp_for_bs()
        else:
            return 12345678910

    def run_lite_plan_setup_queries(self):
        cmds = DB2Commands(self.conf)
        setup_files = ['conn5.sp', 'fgac_grant_ddl.sql', 'fgac_ddl.sql']
        try:
            for file in setup_files:
                if os.path.isfile(os.path.join(self.conf['conf_dir'], file)):
                    logger.info(
                        "{0} found, going to execute it...".format(file))
                    db2_cmd_ops = "-tvf"
                    if file == "conn5.sp":
                        db2_cmd_ops = "-td@ -svf"

                    cmd = "runuser -l {0} -c \"{1}; db2 {2} {3}\"".format(cmds.dbuser, cmds.connect_db_remote(), db2_cmd_ops,
                                                                          os.path.join(self.conf['conf_dir'], file))
                    logger.info(cmd.replace(cmds.dbuser, "xxxxxx").
                                replace(cmds.using, "xxxxxx"))

                    db2_cmd_execution(cmd)

            cmd = "runuser -l {0} -c \"{1};{2}\"".format(
                cmds.dbuser, cmds.attach_to_dbnode(), cmds.forceconns)
            db2_cmd_execution(cmd)
        except Exception as e:
            raise(e)

    @ log.log_execution(logger)
    def mon_avg_hadr_log_wait_time(self):
        # the return should be an integer or decimal or hyphen(-)
        # or raise an exception if error
        cmds = DB2Commands(self.conf)
        if os.path.isfile(os.path.join('/tmp/compose/db2/resources/db2mon.db.logst.sql')):
            logger.info("db2mon.db.logst.sql found going to execute it")
            cmd = "runuser -l {0} -c \"{1}; db2 -tvf {2}\"".format(cmds.dbuser,
                                                                   cmds.connect_db_remote(),
                                                                   os.path.join('/tmp/compose/db2/resources/db2mon.db.logst.sql'))
            logger.info(cmd.replace(cmds.dbuser, "xxxxxx").
                        replace(cmds.using, "xxxxxx"))
            out = db2_cmd_execution(cmd, retries=0, return_msg=True)

            try:
                lines = out.splitlines()
                if len(lines) > 8:
                    line = lines[-8]  # interested in the 5th last line
                    logger.info("LINE OF INTEREST: {}".format(line))
                    items = line.split()
                    if len(items) == 5:
                        avg_hadr_log_wait_time = items[4]  # the 5th column
                        return avg_hadr_log_wait_time
                    else:
                        raise Exception(
                            "unexpected number of columns({})".format(len(items)))
                else:
                    raise Exception("expected more output from sql")

            except Exception as e:
                raise(e)
        else:
            logger.info("did not find {}".format(os.path.join(
                '/tmp/compose/db2/resources/db2mon.db.logst.sql')))
