import os
import shlex
import subprocess
import socket
import time
from datetime import datetime, timedelta
from json import dump, dumps, load, loads
from pkg_resources import parse_version
from grpc import RpcError

import cdb.service
from cdb import log
from cdb.execute import CommandSuccess, CommandFailure, CommandSkipped
from kubernetes import client as kubeclient
from kubernetes import config as kubeconfig

from compose.db2 import configuration, db2, users, liteusers, formation, bucket
from compose.db2.debroni import Debroni
from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.hadr import Db2HADR

logger = log.get_logger(__name__)
eviction_score_primary = 1000000
eviction_score_sync_standby = 100
eviction_score_async_standby = 0


def lite_check(debroni, conf):
    return (debroni.is_leader() or debroni.is_singlenode) and conf['plan_id'] == 'dashDBLiteFormation'


def start():
    cdb.service.start('db2')
    return CommandSuccess()


def stop():
    cdb.service.stop('db2')
    return CommandSuccess()


def stop_standby():
    conf = configuration.Configuration()
    debroni = Debroni(conf)
    if not debroni.is_leader():
        return stop()
    else:
        return CommandSkipped()


def configure():
    conf = configuration.Configuration()
    conf_dir = conf['conf_dir']
    os.makedirs(conf_dir, exist_ok=True)
    db = db2.Db2(conf)
    hadr = Db2HADR(conf)
    db.create_db2_data_dirs()
    db.create_symlinks()
    template_values = dict(list(conf.items()))
    db.write_users_file(values=template_values, lite=(
        conf['plan_id'] == 'dashDBLiteFormation'))
    fmtn = formation.Formation(template_values['crd_group'],
                               template_values['account'],
                               template_values['id'])
    template_values['db2_acr_host'] = fmtn.get_connection_host()
    template_values['db2_acr_port'] = fmtn.get_connection_port()
    template_values['designated_role'] = hadr.set_designated_role()
    template_values['db2_hadr_start_cmd'] = hadr.get_db2_hadr_start_cmd()
    template_values['db2_instance_mem'] = fmtn.desired_mem_to_set()
    db.write_init_sql('db2cli.sql', values=template_values)

    db.run_catalog_on_client()
    if template_values['designated_role'] != "STANDARD":
        # add backres and hadr_cfg to payload
        template_values['db2_hadr_cfg'] = db.get_db2_hadr_setup_config(
            template_values['designated_role'])
        template_values['db2_backres_cmd'] = db.get_db2_backup_restore_cmd_init(template_values['designated_role'],
                                                                                db.db2_latest_bkp_for_bs())
        db.write_hadr_configuration(values=template_values)
    db.write_db2u_conf('custom_registry.cfg', values=template_values)
    db.write_db2u_conf('custom_dbm.cfg', values=template_values)
    db.write_db2u_conf('custom_db.cfg', values=template_values)
    db.write_db2u_conf('etc_profile-NEBULA.cfg', values=template_values)
    db.write_required_conf('parameters.ini', values=template_values)
    db.write_required_conf('bootstrap.sh', values=template_values)
    db.write_required_conf(
        'initialize.sh', subdirectory="debroni", values=template_values)
    db.write_required_conf('hadr_configure.sh',
                           subdirectory="debroni", values=template_values)
    db.write_required_conf('detect_db2_vrmf_change.sh',
                           subdirectory="debroni", values=template_values)
    db.write_required_conf('update_instance.sh',
                           subdirectory="debroni", values=template_values)
    db.write_required_conf(
        'update_db.sh', subdirectory="debroni", values=template_values)
    db.write_required_conf('upgrade_instance.sh',
                           subdirectory="debroni", values=template_values)
    db.write_required_conf('update_db2_ks.sh',
                           subdirectory="debroni", values=template_values)
    db.write_required_conf('keystore_update_driver.sh',
                           subdirectory="debroni", values=template_values)
    db.write_db2u_config_var(values=template_values)
    cmd = '/bin/chown -R ibm:ibm /conf'
    subprocess.check_call(shlex.split(cmd), shell=False)
    cmd = '/usr/local/bin/debroni'
    cdb.service.configure('db2', [cmd])
    cmd = '/usr/local/bin/db2logstdout.sh'
    cdb.service.configure('db2diag', [cmd])
    cmd = '/usr/local/bin/usersync.sh'
    cdb.service.configure('usersync', [cmd])

    # sql files for lite
    if conf['plan_id'] == 'dashDBLiteFormation':
        db.write_init_sql('fgac_ddl.sql', values=template_values)
        db.write_init_sql('fgac_grant_ddl.sql', values=template_values)
        db.write_init_sql('conn5.sp', values=template_values)
        cmd = '/usr/local/bin/user-json-file-sync'
        cdb.service.configure('user-json-file-sync', [cmd])

    def checkVersion(currVersion, required):
        currV = currVersion.split('.')
        currV = currV[-1]
        if (parse_version(currV) >= parse_version(required)):
            cmd = '/usr/local/bin/reaper.sh'
            cdb.service.configure('reaper', [cmd])
    checkVersion(conf["version"], "005")

    return CommandSuccess()


def configure_backup():
    # configure logarchmeth1 to S3 or residered location
    # setup alias
    # TODO Write a function in sqlUtils making user of ibm_db and CALL ADMIN_CMD
    pass


def backup_info():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.db2_backup_info()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def kill_all_connections():
    """
    db2 force applications all
    """
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.db2_force_applications()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def kill_user_connections(user):
    """
    db2 force applications for user
    """
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = liteusers.LiteUserManager(conf)
            um.force_lite_user_apps(user)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def buildback():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        debroni = Debroni(conf)
        if debroni.is_sync() or debroni.is_async():
            db.run_buildback()
            return CommandSuccess()
        else:
            return CommandSkipped("Member is leader")
    except Exception as e:
        return CommandFailure(str(e))


def backup_forbb():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        debroni = Debroni(conf)
        if debroni.is_leader():
            db.backup_ifrequired(timedelta(days=2))
            return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def db_summary():
    """
    Gets a summary of how the database is performing over a 30 second interval
    """
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.db_summary()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def backup(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            db.run_backup(data)
            return CommandSuccess()
        else:
            return CommandSkipped("Member is not leader")
    except RpcError as e:
        return CommandSkipped(str(e))
    except Exception as e:
        return CommandFailure(str(e))


def validate_recent_backup(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        restore_data = db.validate_backup_run(data)
        if restore_data:
            return CommandSuccess("Backup Validation Success {}".format(dumps(restore_data)))
        else:
            return CommandFailure("backup validation Failed, restore_data returned null, validate backup taken or setup")
    except Exception as e:
        return CommandFailure(str(e))


def backup_hadr_config():
    conf = configuration.Configuration()
    fmtn = formation.Formation(conf['crd_group'],
                               conf['account'],
                               conf['id'])
    if fmtn.is_dr_configured():
        db = db2.Db2(conf)
        hadr_config = db.get_db2_hadr_settings()
        pod_name = socket.gethostname()
        outfile = "/mnt/blumeta0/home/db2inst1/hadr_conf_{}.json".format(
            pod_name)
        dump(hadr_config, open(outfile, "w"))
        return CommandSuccess()
    else:
        return CommandSkipped("Backing up HADR config is only used for buildback on DR systems")


def sleep(secs):
    try:
        time.sleep(int(secs))
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def restore(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        db = db2.Db2(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            db.run_restore(data)
            return CommandSuccess()
        else:
            return CommandSkipped("Member is not leader")
    except Exception as e:
        return CommandFailure(str(e))


def copy(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            db.run_copy(data)
            return CommandSuccess()
        else:
            return CommandSkipped("Member is not leader")
    except Exception as e:
        return CommandFailure(str(e))


def backup_config(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.change_backup_config(data)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def is_leader():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            return CommandSuccess()
        else:
            return CommandFailure("Member is not the leader")
    except Exception as e:
        return CommandFailure(str(e))


def takeover():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_sync():
            debroni.init_takeover()
            return CommandSuccess()
        return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def dr_takeover(data):
    j = loads(data)
    method = "graceful"
    if j["force"] == True or j["force"] == "True" or j["force"] == "true":
        method = "force"

    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_async():
            debroni.init_takeover(method)
            return CommandSuccess()
        return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def pause_debroni():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.pause_debroni()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def unpause_debroni():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.unpause_debroni()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def debroni_info():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        info = debroni.debroni_info()
        return CommandSuccess(info)
    except Exception as e:
        return CommandFailure(str(e))


def debroni_database_details():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        info = debroni.get_member_database_details()
        return CommandSuccess(info)
    except Exception as e:
        return CommandFailure(str(e))


def flip_sync(direction="toggle"):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.flip_sync(direction)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def rotate_primary():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.rotate_primary()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))

# this function dictates Pod Ready status, if this passes pod will be marked as ready


def rotate_backups():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.rotate_backups()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def status():
    try:
        conf = {
            'fqdn': socket.getfqdn(),
            'debroni_port': "21815",
            'tls_crt_file': "/conf/cert/tls.crt",
            'tls_key_file': "/conf/cert/tls.key"
        }
        debroni = Debroni(conf)
        # this will require debroni GRPC be up, if not exception will occur (pod not ready)
        if (cdb.service.stat('db2') == "run"):
            debroni.get_version()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def eviction_score():
    """
    Function that determines if it's safe to evict (aka delete) a node
    based on Db2's HADR role
    Output is a numeric value (score), with these definitions:
    0 - best score, node can be evicted
    > 0 - the higher the score the less favourable a node is for eviction
    """
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_async() or debroni.is_singlenode():
            return CommandSuccess(eviction_score_async_standby)
        if debroni.is_sync():
            return CommandSuccess(eviction_score_sync_standby)

        return CommandSuccess(eviction_score_primary)
    except Exception:
        return CommandSuccess(eviction_score_primary)


def pre_evict():
    """
    Function that does all things necessary (aka 'actions') to be able to safely evict a node
    """
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)

        # The basic strategy is to get the node into async standby if possible
        if debroni.is_leader():
            debroni.quick_rotate_primary()
        elif debroni.is_sync():
            debroni.flip_sync("toggle")
    except Exception as e:
        return CommandFailure("Encountered error in pre_evict: {}".format(str(e)))

    return CommandSuccess("Successfully ran all actions to enable node eviction")


def ha_status():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.db2_ha_status()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def scale():
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.db2_adjust_scale_values()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))

# db2 does not respect cgroups so we need to
# prescale down in situations where instance memory
# might outstrip the new node (ie. scale down)


def prescale(data):
    try:
        conf = configuration.Configuration()

        fmtn = formation.Formation(conf['crd_group'],
                                   conf['account'],
                                   conf['id'])

        scale_data = loads(data)
        if fmtn.is_downscale(scale_data):
            db = db2.Db2(conf)
            desired_memory = fmtn.desired_mem_to_set(
                desired_memory=scale_data["memory"])
            db.db2_adjust_scale_values(instance_memory=desired_memory)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def create_user(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.create_user(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def create_lite_user(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.create_user(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def create_lite_user_schema(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.create_lite_user_schema(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def create_lite_user_tablespace(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.create_lite_user_tablespace(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def grant_lite_user_privilege(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.grant_lite_user_privilege(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


# def grant_lite_user_role(data):
#     try:
#         conf = configuration.Configuration()
#         debroni = Debroni(conf)
#         if debroni.is_leader() or debroni.is_singlenode():
#             um = liteusers.LiteUserManager(conf)
#             um.grant_role(data)
#             return CommandSuccess()
#         else:
#             return CommandSkipped()
#     except Exception as e:
#         return CommandFailure(str(e))


def delete_user(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.delete_user(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def delete_lite_user(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.delete_user(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def remove_lite_user_table(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.remove_lite_user_table(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def remove_error_schema(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.remove_error_schema(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


# def remove_spatial_reference(data):
#     try:
#         conf = configuration.Configuration()
#         debroni = Debroni(conf)
#         if debroni.is_leader():
#             um = liteusers.LiteUserManager(conf)
#             um.remove_spatial_reference(data)
#             return CommandSuccess()
#         else:
#             return CommandSkipped()
#     except Exception as e:
#         return CommandFailure(str(e))


def change_password(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.change_password(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def create_lite_password(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.change_password(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def sync_users():
    try:
        conf = configuration.Configuration()
        _ = users.UserManager(conf=conf, forceSync=True)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def assert_db_updated():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.assert_db_updated()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def update_instance():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.update_instance()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def update_db():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.update_db()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def lock_operation(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            user_data = loads(data)
            um = users.UserManager(conf)
            if user_data["locked"] == "true":
                um.lock_user(data)
            elif user_data["locked"] == "false":
                um.unlock_user(data)
            else:
                return CommandFailure("locked parameter missing")
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def lite_lock_operation(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            user_data = loads(data)
            um = liteusers.LiteUserManager(conf)
            if user_data["locked"] == "true":
                um.lock_user(data)
            elif user_data["locked"] == "false":
                um.unlock_user(data)
            else:
                return CommandFailure("locked parameter missing")
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def modify_user(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.modify_user(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def upload_userfile_cos(data):
    try:
        conf = configuration.Configuration()
        hostname = socket.gethostname()
        pod_name = loads(data)["pod_name"]
        if hostname == pod_name:
            cmds = DB2Commands(conf)
            cmds.upload_userfile_cos()
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def change_password_bluuser(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.change_password_bluuser(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def change_password_liteuser(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            um = liteusers.LiteUserManager(conf)
            um.change_password_bluuser(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def increase_logging():
    options_path = '/mnt/blumeta0/options'
    filename = os.path.join(options_path, 'DEBRONI_DEBUG')
    try:
        if not os.path.exists(options_path):
            os.makedirs(options_path)

        with open(filename, 'a'):
            os.utime(filename, None)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def decrease_logging():
    try:
        options_path = '/mnt/blumeta0/options'
        filename = os.path.join(options_path, 'DEBRONI_DEBUG')
        os.remove(filename)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def debroni_init_restore():
    try:
        conf = configuration.Configuration()
        kubecli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        # targetted call to primary to reset the configmaps to pri - init 2xsby - buildback
        pri_pod_idx = int(conf['hostname'][-1])
        init_member_cfgmap = "c-{}-m-{}-debroni".format(
            conf['id'], pri_pod_idx)
        # update pri configmap
        kubecli.patch_namespaced_config_map(
            init_member_cfgmap, conf['account'], kubeclient.V1ConfigMap(data={"init": "init"}))

        sby_pod_idxs = [i for i in range(len(conf['peers']))]
        sby_pod_idxs.remove(pri_pod_idx)

        for idx in sby_pod_idxs:
            buildback_member_cfgmap = "c-{}-m-{}-debroni".format(
                conf['id'], idx)
            # update sby configmap
            kubecli.patch_namespaced_config_map(
                buildback_member_cfgmap, conf['account'], kubeclient.V1ConfigMap(data={"init": "buildback"}))
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def debroni_init_buildback():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        fmtn = formation.Formation(conf['crd_group'],
                                   conf['account'],
                                   conf['id'])
        if not (debroni.is_leader() or fmtn.is_disaster_recovery_site()):
            return CommandSkipped()
        kubecli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        pri_pod_idx = int(conf['hostname'][-1])
        sby_len = len(conf['extended_peers'])
        if fmtn.is_dr_configured():
            # Disregard DR connection peer at the end of the peers list
            sby_len -= 1
        sby_pod_idxs = [i for i in range(sby_len)]
        if not fmtn.is_disaster_recovery_site():
            sby_pod_idxs.remove(pri_pod_idx)

        for idx in sby_pod_idxs:
            buildback_member_cfgmap = "c-{}-m-{}-debroni".format(
                conf['id'], idx)
            # update sby configmap
            kubecli.patch_namespaced_config_map(
                buildback_member_cfgmap, conf['account'], kubeclient.V1ConfigMap(data={"init": "buildback"}))
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def debroni_init(data):
    try:
        conf = configuration.Configuration()
        init_data = loads(data)
        init_state = init_data["init"]
        if init_state is None:
            return CommandFailure("init parameter must be passed to execute command")
        kubecli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        hostname = socket.gethostname()
        kubecli.patch_namespaced_config_map(
            "{}-debroni".format(hostname), conf['account'], kubeclient.V1ConfigMap(data={"init": init_state}))
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def construct_user_table():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.construct_user_table()
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def cp_user_data(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        db.copy_usersJson(data)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def db2_validate_hadr():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.validate_hadr()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def db2_validate_primary():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.validate_hadr(check='primary')
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def db2_run_select(data):
    try:
        conf = configuration.Configuration()
        db = db2.Db2(conf)
        data = db.run_a_select(data)
        return CommandSuccess(str(data))
    except Exception as e:
        return CommandFailure(str(e))


def disable_network():
    try:
        conf = configuration.Configuration()
        kubecli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        pod_name = socket.gethostname()
        logger.info("Disabling networking on pod: {}".format(pod_name))
        kubecli.patch_namespaced_pod(pod_name, conf['account'], body={"metadata": {
                                     "labels": {"ha_mode": "offline"}}}, pretty=True)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def rotate_db2inst1(data):
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_leader() or debroni.is_singlenode():
            um = users.UserManager(conf)
            um.rotate_db2inst1(data)
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def verify_single_replica():
    try:
        conf = configuration.Configuration()
        fmtn = formation.Formation(conf['crd_group'],
                                   conf['account'],
                                   conf['id'])
        if fmtn.get_replicas("m") == 1:
            return CommandSuccess()
        else:
            return CommandFailure()
    except Exception as e:
        return CommandFailure(str(e))


def configure_lite_plan():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if lite_check(debroni, conf):
            db = db2.Db2(conf)
            db.run_lite_plan_setup_queries()

            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def verify_not_primary():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)

        if debroni.is_leader():
            return CommandFailure()

        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def wait_for_cos_file(data):
    try:
        conf = configuration.Configuration()
        cos = bucket.Bucket(conf=conf)
        args = loads(data)
        timeout = 0
        interval = 60
        if 'timeout' in args:
            timeout = int(args['timeout'])
        if 'interval' in args:
            interval = int(args['interval'])
        cos.wait_for_file(
            filename=args['filename'], timeout=timeout, interval=interval)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def publish_ports():
    try:
        conf = configuration.Configuration()
        formation_id = conf['id']
        fmtn = formation.Formation(conf['crd_group'],
                                   conf['account'],
                                   formation_id)
        ports = []
        replicas = conf['replicas']
        for m in range(replicas):
            svc = fmtn.get_service("c-{}-h-{}".format(formation_id, m))
            for p in svc['spec']['ports']:
                if p['name'] == "hadr":
                    ports.append(p['node_port'])
        cos = bucket.Bucket(conf=conf)
        hostnames = []
        peers = conf['peers']
        peers.sort()
        cluster_id = os.getenv('CLUSTER_ID')
        for peer in peers:
            zone = fmtn.get_pod_zone(peer.split('.')[0])
            if zone:
                hostnames.append(
                    "{}-{}.private.db2.databases.appdomain.cloud".format(cluster_id, zone))
            else:
                hostnames.append(
                    "{}.private.db2.databases.appdomain.cloud".format(cluster_id))

        if len(ports) > 1:
            primary_pod_idx = int(os.getenv("POD_NAME").split("-")[-1])

            # flip primary idx contents to 0 idx
            ports[0], ports[primary_pod_idx] = ports[primary_pod_idx], ports[0]
            hostnames[0], hostnames[primary_pod_idx] = hostnames[primary_pod_idx], hostnames[0]
            peers[0], peers[primary_pod_idx] = peers[primary_pod_idx], peers[0]

        cos.publish_fmtn_hadr_ports_to_cos(hostnames, ports, peers)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def remote_ports():
    try:
        conf = configuration.Configuration()
        cos = bucket.Bucket(conf=conf)
        data = cos.get_external_port_data_from_cos()
        logger.info(data)
    except Exception as e:
        return CommandFailure(str(e))


def configure_disaster_recovery():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        if debroni.is_controller():
            cos = bucket.Bucket(conf=conf)
            # primary site will attempt to get single external host/port for dr site
            # and set it into the primary site hadr_target_list via debroni
            data = cos.get_external_port_data_from_cos()
            if data and len(data["ports"]) > 0:
                logger.info("Configuring DR Member: {} on port: {}".format(
                    data["hostnames"][0], data["ports"][0]))
                debroni.set_dr_member(data["hostnames"][0], data["ports"][0])
            else:
                raise Exception("Unable to configure primary, ensure disaster recovery \
                    ports are published and bucket is accessible")
            return CommandSuccess()
        else:
            return CommandSkipped()
    except Exception as e:
        return CommandFailure(str(e))


def unconfigure_disaster_recovery():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        # unset dr from target list
        debroni.set_dr_member("", 0)
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def is_disaster_recovery_site():
    try:
        conf = configuration.Configuration()
        formation_id = conf['id']
        fmtn = formation.Formation(conf['crd_group'],
                                   conf['account'],
                                   formation_id)
        if fmtn.is_disaster_recovery_site():
            return CommandSuccess()
        else:
            return CommandFailure("Member is not the disaster recovery site")
    except Exception as e:
        return CommandFailure(str(e))

# db2_validate_dr will loop check for DR connected status


def validate_dr_connected():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.validate_dr_connected()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))


def update_db2_keystore():
    try:
        conf = configuration.Configuration()
        debroni = Debroni(conf)
        debroni.update_db2_keystore()
        return CommandSuccess()
    except Exception as e:
        return CommandFailure(str(e))
