import os
import datetime
from json import load
import socket
import time

from cdb import log
from compose.db2.utils import setup_utils, util_funcs
from compose.db2.utils.cloudUtils import S3Resource
from compose.db2.utils.hadr import Db2HADR
from compose.db2.utils.sqlUtils import Db2SQL
from compose.db2 import formation, bucket
from compose.db2 import configuration
from compose.db2.utils.setup_utils import check_size
logger = log.get_logger(__name__)


class DB2Commands(S3Resource):
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        S3Resource.__init__(self, conf=conf)
        self.chkUser = setup_utils.checkUserRunning()
        self.ipath = setup_utils.find_db2_install()
        self.instance_owner = util_funcs.run_cmd(os.path.join(self.ipath, "db2ilist"))[
            0].decode("utf-8").strip("\n")  # for now use this as user
        self.dbuser = self.conf['db2_sysadmin_user']
        self.opath = self.conf['db2_overflow_path']
        self.user_file = self.conf['db2_user_file']
        self.fmtn = formation.Formation(
            self.conf['crd_group'], self.conf['account'], self.conf['id'])
        self.fmtn_spec = self.fmtn.get_formation_resources()
        try:
            self.using = self.conf['compose_password']
        except AttributeError as e:
            raise(e)
        self.host = self.ip
        self.bkp_loc = self.repo
        self.creds = "USER {0} USING {1}".format(self.dbuser,
                                                 self.using)
        self.dbname = self.conf['db_name']
        self.backup_repo = self.conf['repo_type']
        self.backup_path = self.conf['repo_path']
        self.dropdb = "db2 drop db %s" % self.dbname
        self.stopdb2 = "db2stop force"
        self.startdb2 = "db2start"
        self.terminate = "db2 terminate"
        self.listdb = "db2 list db directory"
        self.activatedb = "db2 activate db %s" % self.dbname
        self.deactivatedb = "db2 deactivate db %s" % self.dbname
        self.stophadr = "db2 stop hadr on db %s" % self.dbname
        self.quiescedb = "db2 quiesce database immediate force connections"
        self.unquiescedb = "db2 UNQUIESCE DATABASE"
        self.activedbs = "db2 list active databases"
        self.quiesceinstance = ("db2 QUIESCE INSTANCE {0} RESTRICTED ACCESS"
                                " IMMEDIATE FORCE "
                                "CONNECTIONS".format(self.dbuser))
        self.forceconns = "db2 force applications all"
        self.disk_sz = check_size()
        if self.conf['type'] == "dv":
            self.runarchive = "db2 archive log for db %s %s ON DBPARTITIONNUM '(0)'" % (
                self.dbname, self.creds)
        else:
            self.runarchive = "db2 archive log for db %s" % self.dbname
        self.uncatalog = "db2 uncatalog db %s" % self.dbname
        self.dbcfg = "db2 get db cfg for %s" % self.dbname
        self.dbmcfg = "db2 get dbm cfg"
        self.storage = "db2 list storage access"
        self.db2pd = "db2pd -dbcfg -db %s" % self.dbname
        self.lsapps = "db2 list applications for database %s" % self.dbname
        self.dbcfg = "db2 get db cfg for %s" % self.dbname
        self.dbmcfg = "db2 get dbm cfg"
        self.storage = "db2 list storage access"
        self.catalogInfo = "db2 list db directory | awk '/Database 2/,EOF'"
        self.autocfg = ("db2 AUTOCONFIGURE USING MEM_PERCENT 90 "
                        "WORKLOAD_TYPE SIMPLE APPLY NONE "
                        )
        # self.newdbcfglim = {'cfg': {"CATALOGCACHE_SZ": self.conf['db2_catcache_sz']}}
        self.db2audit_cmd = "db2audit configure datapath {0} archivepath {1}".format(
            self.conf['db2_audit_dir'], self.conf['db2_audit_dir'])
        # self.cos_backup_list = self.backup_list()
        if self.creds:
            self.rfstop = "db2 rollforward db %s %s stop" % (self.dbname,
                                                             self.creds)
            self.rfcomplete = "db2 rollforward db %s %s complete" % (self.dbname,
                                                                     self.creds)
            self.rfquery = "db2 rollforward db %s %s query status" % (self.dbname,
                                                                      self.creds)
            self.start_hadr_p_f = "db2 start hadr on db %s %s as primary by force" % (self.dbname,
                                                                                      self.creds)
            self.start_hadr_p = "db2 start hadr on db %s %s as primary" % (self.dbname,
                                                                           self.creds)
            self.start_hadr_s = "db2 start hadr on db %s %s as standby" % (self.dbname,
                                                                           self.creds)
        else:
            self.rfstop = "db2 rollforward db %s stop" % self.dbname
            self.rfcomplete = "db2 rollforward db %s complete" % self.dbname
            self.rfquery = "db2 rollforward db %s query status" % self.dbname
            self.start_hadr_p_f = "db2 start hadr on db %s as primary by force" % self.dbname
            self.start_hadr_p = "db2 start hadr on db %s as primary" % self.dbname
            self.start_hadr_s = "db2 start hadr on db %s as standby" % self.dbname
        self.loadalias = "db2-s3-load"
        self.backupalias = "db2-ssbr"
        # hard code to limit to 8 characters
        self.nodename = self.conf['role']+"db2oc"
        self.s3archloc = (
            "REMOTE:%s::default::"
            "%s::%s/Arlog" % (self.vendor,
                              self.container,
                              self.bdir)
        )
        self.s3archopts = (
            "-remotecredential={0}::{1}".format(self.auth1,
                                                self.auth2)

        )
        self.catloadAliasS3 = (
            "CATALOG STORAGE ACCESS ALIAS {0} VENDOR {1} SERVER"
            " {2} USER {3} PASSWORD {4} CONTAINER {5} "
            "DBGROUP {6}".format(self.loadalias,
                                 self.vendor,
                                 self.ep,
                                 self.auth1,
                                 self.auth2,
                                 self.container,
                                 'bluadmin'
                                 )

        )
        self.catBARAliasS3 = (
            "CATALOG STORAGE ACCESS ALIAS {0} VENDOR {1} SERVER"
            " {2} USER {3} PASSWORD {4} CONTAINER {5} "
            "DBGROUP {6}".format(self.backupalias,
                                 self.vendor,
                                 self.ep,
                                 self.auth1,
                                 self.auth2,
                                 self.container,
                                 'SYSADM'
                                 )

        )

        self.cos_alias_dir = (
            "DB2REMOTE://{alias}//{bdir}/{subbdir}".format(
                alias=self.backupalias,
                bdir=self.bdir,
                subbdir=self.bbdir)
        )
        if self.get_cos_download_concurrency_set() == 1:
            if self.fmtn.get_disk_sz() <= 20:
                self.cos_alias_dir = self.cos_alias_dir
            elif int(self.disk_sz[2]/1024/1024/1024) >= 20 and int(self.disk_sz[2]/1024/1024/1024) <= 40:
                self.cos_alias_dir = ",".join(
                    self.cos_alias_dir*1 for i in range(2))
            elif int(self.disk_sz[2]/1024/1024/1024) > 40:
                self.cos_alias_dir = ",".join(
                    self.cos_alias_dir*1 for i in range(4))
            else:
                self.cos_alias_dir = self.cos_alias_dir

        self.backup_dir = self.cos_alias_dir
        if self.fmtn.get_disk_sz() <= 20:
            if (int(self.disk_sz[2]/1024/1024/1024) > 15 and int(self.disk_sz[2]/1024/1024/1024) <= 20):
                self.backup_dir = ",".join(
                    self.cos_alias_dir*1 for i in range(4))
            else:
                self.backup_dir = self.cos_alias_dir
        else:
            self.backup_dir = ",".join(
                self.cos_alias_dir*1 for i in range(4))

        self.backup_cmd = (
            "BACKUP DB {db} ONLINE TO "
            "{bdir}"
            " INCLUDE LOGS WITHOUT PROMPTING".format(db=self.dbname,
                                                     alias=self.backupalias,
                                                     bdir=self.backup_dir,
                                                     subbdir=self.bbdir)
        )
        self.restore_cmd = (
            "RESTORE DB {db} FROM "
            "{bdir}"
            " TAKEN AT {ts}".format(db=self.dbname,
                                    alias=self.backupalias,
                                    bdir=self.cos_alias_dir,
                                    subbdir=self.bbdir,
                                    ts="restoretime")
        )

        self.catnode = (
            "db2 catalog tcpip node {0} remote {1}"
            " server".format(self.nodename,
                             self.conf['fqdn'])

        )

        self.catdb = "db2 catalog db {0} as {1} at node {2}".format(self.dbname,
                                                                    self.dbname,
                                                                    self.nodename)
        self.delete_lite_schema = "db2 CALL SYSPROC.ADMIN_DROP_SCHEMA\(\\\'{}\\\', NULL, \\\'ERRORSCHEMA\\\', \\\'ERRORTABLE\\\'\)"
        self.force_apps = (
            "db2 FORCE APPLICATION \( {0} \)"
        )
        self.clusterIPs = self.conf['extended_peers']

    def dbm_instance_mem_limit(self):
        fmtn = formation.Formation(
            self.conf['crd_group'], self.conf['account'], self.conf['id'])
        desired_mem = fmtn.desired_mem_to_set()
        return {'cfg': {"INSTANCE_MEMORY": desired_mem}}

    # function to attach to node
    def attach_to_dbnode(self):
        node = self.nodename
        attach_cmd = ("db2 attach to %s "
                      "user %s using %s >/dev/null" % (node,
                                                       self.dbuser,
                                                       self.using)
                      )
        return attach_cmd

    # function to terminate remote conn
    def terminate_db2bp(self):
        terminate_cmd = ("{} >/dev/null".format(self.terminate))
        return terminate_cmd

    # function to generate catalog commands
    def generate_catalog_node_commands(self, ssl=True):
        if ssl:
            cmd = self.catnode + \
                " {} security ssl".format(self.conf['db2_ssl_svcename'])
            return cmd.replace(self.nodename, "s{}".format(self.nodename))
        else:
            return self.catnode + " {}".format(self.conf['db2_tcp_svcename'])

    # function to generate catalog db commands
    def generate_catalog_db_commands(self, ssl=True):
        if ssl:
            cmd = (
                "db2 catalog db {0} as s{1} at node s{2}".format(self.dbname,
                                                                 self.dbname,
                                                                 self.nodename)
            )
            return cmd
        else:
            return self.catdb

    # function to remote connect
    def connect_db_remote(self):
        remote_connect = ("db2 connect to %s "
                          "USER %s USING %s >/dev/null" % (self.dbname,
                                                           self.dbuser,
                                                           self.using)

                          )
        return remote_connect

    # create an admin command
    def run_admin_cmd(self, sql):
        # SYSPROC.ADMIN_CMD( 'AUTOCONFIGURE USING MEM_PERCENT 80 APPLY NONE' )"
        admin_cmd = '''CALL SYSPROC.ADMIN_CMD(\'{}\')'''.format(sql)
        return admin_cmd

    # function to uncatalog storage access alias
    def uncatalog_storage_access(self, alias, attach=False):
        cmd = "db2 uncatalog storage access alias {0}".format(alias)
        return cmd

    # function to construct update db cfg params.
    def update_db_cfg(self, **kwargs):
        precmd = "db2 UPDATE DB CFG USING FOR DB {0}".format(self.dbname)
        dbcfg = ""
        for key in kwargs.get('cfg').keys():
            update_db_cfg = (
                " {0} {1} ".format(key,
                                   kwargs.get('cfg').get(key))
            )

            dbcfg += update_db_cfg
        return "{0} {1} IMMEDIATE".format(precmd, dbcfg)

    # function to construct update db cfg params.
    def update_dbm_cfg(self, **kwargs):
        """
        >>> x = {"cfg":{"INSTANCE_MEMORY":12345}}
        >>> x.items()
            [('cfg', {'INSTANCE_MEMORY': 12345})]
        >>> x.get('cfg')
            {'INSTANCE_MEMORY': 12345}
        >>> x.get('cfg').get('INSTANCE_MEMORY')
        """
        precmd = "db2 UPDATE DBM CFG USING "
        dbmcfg = ""
        for key in kwargs.get('cfg').keys():
            update_dbm_cfg = (
                " {0} {1} ".format(key,
                                   kwargs.get('cfg').get(key))
            )

            dbmcfg += update_dbm_cfg
        return "{0} {1} IMMEDIATE".format(precmd, dbmcfg)

    # function to catalog alernative server command.
    def catalog_alternative_server(self, primaryip, attach=False):
        alternative_catalog_cmd = (
            "db2 UPDATE ALTERNATE SERVER FOR DATABASE %s "
            "USING HOSTNAME %s PORT 50001" % (self.dbname,
                                              primaryip)
        )
        return alternative_catalog_cmd

    def get_cos_download_concurrency_set(self):
        count = 4
        sql = Db2SQL(self.conf)
        data = sql.run_desired_select_sql(ip=self.conf['fqdn'],
                                          query=sql.db2_get_object_store_settings,
                                          fetch='assoc')
        if data:
            count = int(data[0].get(
                'REG_VAR_ON_DISK_VALUE').split("=")[-1])
        return count

    def set_parallelism(self):
        if self.fmtn_spec["cpu"] != 0:
            parallelism = self.fmtn_spec["cpu"]
        else:
            if 4 <= self.fmtn_spec["memory"] < 8:
                parallelism = 2
            elif 8 <= self.fmtn_spec["memory"] < 16:
                parallelism = 3
            elif 16 <= self.fmtn_spec["memory"] < 32:
                parallelism = 4
            elif 32 <= self.fmtn_spec["memory"] < 64:
                parallelism = 5
            else:
                parallelism = 1
        return parallelism

    def set_util_impact_priority(self):
        pass

    # function to construct backup command.

    def db2_backup_cmd(self, use_alias=False):

        if self.backup_repo == "s3":
            if not use_alias:
                db2_backup_dir = "{0}::{1}::{2}::{3}::{4}::{5}".format('s3',
                                                                       self.ep,
                                                                       self.auth1,
                                                                       self.auth2,
                                                                       self.container,
                                                                       self.bdir)
            else:
                db2_backup_dir = "DB2REMOTE://{alias}//{bdir}/".format(alias=self.backupalias,
                                                                       bdir=self.bdir)

        if self.backup_repo == "posix":
            db2_backup_dir = self.backup_path
        elif self.backup_repo == "posix":
            db2_backup_dir = self.backup_path

        if int(self.disk_sz[2]/1024/1024/1024) >= 10 and int(self.disk_sz[2]/1024/1024/1024) < 20:
            db2_backup_dir = ",".join(db2_backup_dir*1 for i in range(2))
        elif int(self.disk_sz[2]/1024/1024/1024) > 20:
            db2_backup_dir = ",".join(db2_backup_dir*1 for i in range(3))
        else:
            db2_backup_dir = db2_backup_dir

        if not use_alias:
            if self.dbuser and self.using:
                backup_db = (
                    "db2 backup database %s user %s using %s %s to %s "
                    "PARALLELISM %d INCLUDE LOGS WITHOUT PROMPTING" % (self.dbname,
                                                                       self.dbuser,
                                                                       self.using,
                                                                       'ONLINE',
                                                                       db2_backup_dir,
                                                                       self.set_parallelism())
                )
            else:
                backup_db = "db2 backup database %s %s to %s PARALLELISM %d INCLUDE LOGS WITHOUT PROMPTING" % (self.dbname,
                                                                                                               'ONLINE',
                                                                                                               db2_backup_dir,
                                                                                                               self.set_parallelism())
        else:
            backup_db = (
                "backup database %s %s to %s PARALLELISM %d INCLUDE LOGS WITHOUT PROMPTING" % (self.dbname,
                                                                                               'ONLINE',
                                                                                               db2_backup_dir,
                                                                                               self.set_parallelism())
            )
        return backup_db

    # function to construct restore command, and checks if its isFlex or not.

    def db2_restore_cmd(self, **kwargs):
        if ((self.backup_repo == "s3") and (not kwargs['isCopy'])):
            db2_backup_dir = "{0}::{1}::{2}::{3}::{4}::{5}".format('s3',
                                                                   self.ep,
                                                                   self.auth1,
                                                                   self.auth2,
                                                                   self.container,
                                                                   self.bdir)
        elif ((self.backup_repo == "s3") and (kwargs['isCopy'])):
            db2_backup_dir = "{0}::{1}::{2}::{3}::{4}::{5}".format('s3',
                                                                   kwargs['cos']['cos_endpoint'],
                                                                   kwargs['cos']['cos_access_key'],
                                                                   kwargs['cos']['cos_secret_access_key'],
                                                                   kwargs['cos']['cos_bucket'],
                                                                   self.bdir)

        if self.backup_repo == "posix":
            db2_backup_dir = self.backup_path
        if self.get_cos_download_concurrency_set() == 1:
            if self.fmtn.get_disk_sz() <= 20:
                db2_backup_dir = db2_backup_dir
            elif int(self.disk_sz[2]/1024/1024/1024) >= 20 and int(self.disk_sz[2]/1024/1024/1024) <= 40:
                db2_backup_dir = ",".join(db2_backup_dir*1 for i in range(2))
            elif int(self.disk_sz[2]/1024/1024/1024) > 40:
                db2_backup_dir = ",".join(db2_backup_dir*1 for i in range(4))
            else:
                db2_backup_dir = db2_backup_dir

        if self.creds:
            creds = self.creds
        else:
            creds = ""

        if creds:
            restore_db = (
                "db2 RESTORE DATABASE {0} {1} FROM {2} TAKEN AT {3} "
                "INTO {4} LOGTARGET {5} REPLACE EXISTING".format(self.dbname,
                                                                 creds,
                                                                 db2_backup_dir,
                                                                 kwargs['ts'],
                                                                 self.dbname,
                                                                 self.opath
                                                                 )
            )
        else:
            restore_db = (
                "db2 RESTORE DATABASE {0} FROM {1} TAKEN AT {2} "
                "INTO {3} LOGTARGET {4} REPLACE EXISTING".format(self.dbname,
                                                                 db2_backup_dir,
                                                                 kwargs['ts'],
                                                                 self.dbname,
                                                                 self.opath
                                                                 )
            )
        return restore_db

    # function to construct rollforward eob or eol

    def db2_rollforward_db_cmd(self, rfopt, action='COMPLETE', ts=None):
        """
            eob: requires native rollforward
            eol or pit : can be done via recover
        """
        if self.creds:
            creds = self.creds
        else:
            creds = ""
        if rfopt == "eob":
            if creds:
                if self.conf['type'] == "dv":
                    rf_db = (
                        "db2 \'ROLLFORWARD DATABASE %s %s TO END OF LOGS ON DBPARTITIONNUM(0) AND %s "
                        "OVERFLOW LOG PATH (\'%s\') \'" % (self.dbname,
                                                           creds,
                                                           action,
                                                           self.opath)
                    )
                else:
                    rf_db = (
                        "db2 \'ROLLFORWARD DATABASE %s %s TO END OF BACKUP AND %s "
                        "OVERFLOW LOG PATH (\'%s\') NORETRIEVE\'" % (self.dbname,
                                                                     creds,
                                                                     action,
                                                                     self.opath)
                    )

            else:
                if self.conf['type'] == "dv":
                    rf_db = (
                        "db2 \'ROLLFORWARD DATABASE %s TO END OF LOGS ON DBPARTITIONNUM(0) AND %s "
                        "OVERFLOW LOG PATH (\'%s\') \'" % (self.dbname,
                                                           action,
                                                           self.opath)
                    )
                else:
                    rf_db = (
                        "db2 \'ROLLFORWARD DATABASE %s TO END OF BACKUP AND %s "
                        "OVERFLOW LOG PATH (\'%s\') NORETRIEVE\'" % (self.dbname,
                                                                     action,
                                                                     self.opath)
                    )

        if rfopt == "eol":
            if creds:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s TO END OF LOGS %s "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      creds,
                                                      self.opath)
                )
            else:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s TO END OF LOGS  "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      self.opath)
                )
        if rfopt == "pit":
            if creds:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s %s TO %s USING UTC TIME "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      creds,
                                                      ts,
                                                      self.opath)
                )
            else:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s TO %s USING UTC TIME "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      ts,
                                                      self.opath)

                )
        return rf_db

    # function to recover db
    def db2_recover_cmd(self, **kwargs):
        rf_db = ""
        if self.creds:
            creds = self.creds
        else:
            creds = ""
        if kwargs['rfopt'] == "pit":
            if creds:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s TO %s USING UTC TIME %s\'" % (self.dbname,
                                                                             datetime.datetime.strptime(kwargs['ts'],
                                                                                                        '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d-%H.%M.%S'),
                                                                             creds
                                                                             )
                )
            else:
                rf_db = (
                    "db2 \'RECOVER DATABASE %s TO %s USING UTC TIME\'" % (self.dbname,
                                                                          datetime.datetime.strptime(kwargs['ts'],
                                                                                                     '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d-%H.%M.%S')
                                                                          )
                )
        if kwargs['isCopy'] and kwargs['rfopt'] == "eol":
            if creds:
                rf_db = (
                    "db2 \'ROLLFORWARD DATABASE %s %s TO END OF LOGS AND COMPLETE "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      creds,
                                                      self.opath)
                )
            else:
                rf_db = (
                    "db2 \'ROLLFORWARD DATABASE %s TO END OF LOGS AND COMPLETE "
                    "OVERFLOW LOG PATH (\'%s\')\'" % (self.dbname,
                                                      self.opath)
                )

        return rf_db

    # function to copy history file
    def db2_restore_hist_file(self, **kwargs):
        if ((self.backup_repo == "s3") and (kwargs['isCopy'])):
            db2_backup_dir = "{0}::{1}::{2}::{3}::{4}::{5}".format('s3',
                                                                   kwargs['cos']['cos_endpoint'],
                                                                   kwargs['cos']['cos_access_key'],
                                                                   kwargs['cos']['cos_secret_access_key'],
                                                                   kwargs['cos']['cos_bucket'],
                                                                   self.bdir)
        if self.backup_repo == "posix":
            db2_backup_dir = self.backup_path

        db2_backup_dir = ",".join(db2_backup_dir*1 for i in range(0, 3))

        if self.dbuser and self.using:
            creds = "user %s using %s" % (self.dbuser, self.using)
        else:
            creds = ""
        if creds:
            restore_hist_cmd = (
                "db2 RESTORE DB {0} {1} HISTORY FILE ONLINE FROM {2} "
                "TAKEN AT {3} WITHOUT PROMPTING".format(self.dbname,
                                                        creds,
                                                        db2_backup_dir,
                                                        kwargs['ts'])
            )
        else:
            restore_hist_cmd = (
                "db2 RESTORE DB {0} HISTORY FILE ONLINE FROM {1} "
                "TAKEN AT {2} WITHOUT PROMPTING".format(self.dbname,
                                                        db2_backup_dir,
                                                        kwargs['ts'])
            )
        return restore_hist_cmd

    # function to set cloud alias for self serve backup and restore.
    def setup_cloud_alias(self, alias, dbgroup='SYSADM'):
        cloud_bkp_alias = (
            "db2 CATALOG STORAGE ACCESS ALIAS %s VENDOR %s SERVER "
            "%s USER %s PASSWORD %s CONTAINER %s "
            "DBGROUP %s" % (alias,
                            self.vendor,
                            self.ep,
                            self.auth1,
                            self.auth2,
                            self.container,
                            dbgroup)
        )
        return cloud_bkp_alias

    # function to set archive log path
    def set_archive_tos3(self):
        """
        # SwiftArchiveLogLOC="REMOTE:${CLOUD_OBJSTORE_TYPE}::default::${SWIFT_OBJECT_CONTAINER}::\
        CSYS.${SWIFT_OBJECT_CONTAINER_DIR}/Arlog"
        """
        cmd = (
            "db2 update db cfg for {0} using {1} {2}".format(self.dbname,
                                                             'logarchmeth1',
                                                             self.s3archloc)
        )
        return cmd

    # function to set archive logs creds
    def set_logarchopt_toS3(self):
        cmd = (
            "db2 update db cfg for {0} using {1} {2}".format(self.dbname,
                                                             'logarchopt1',
                                                             self.s3archopts)
        )
        return cmd

    # function to uncatalog the objs
    def undo_objS_alias(self, name):
        cmd = "db2 uncatalog storage access alias %s" % name
        return cmd

    # function build build_synchronous_standby_list
    def build_hadr_config(self):
        hadr = Db2HADR(self.conf)
        fmtn = formation.Formation(self.conf['crd_group'],
                                   self.conf['account'],
                                   self.conf['id'])
        primary_host = hadr.build_primary_host()
        standby_list = hadr.build_hadr_standby_list()
        dr_configured = fmtn.is_dr_configured()
        disaster_recovery_site = fmtn.is_disaster_recovery_site()
        prs_initialization = False

        existing_config = {}
        # Generated only when doing a buildback for DR. In that situation, we prefer to reuse
        # existing configs, to ensure we have the correct values.
        pod_name = socket.gethostname()
        conf_backup_file = "/mnt/blumeta0/home/db2inst1/hadr_conf_{}.json".format(
            pod_name)
        if dr_configured and os.path.exists(conf_backup_file):
            existing_config = load(open(conf_backup_file, "r"))

        target_list = self.generate_target_list(fmtn)

        # If DR site we want to wait for primary file to be populated
        # wait 15 minutes for file, if not we will crash loop and try again
        if disaster_recovery_site:
            interval = 30
            while len(target_list) == 0 and interval >= 0:
                logger.info("Disaster Recovery site requires the Primary Site to publish ports, \
                        checking every 30 seconds for 15 minutes")
                target_list = self.generate_target_list(fmtn)
                interval -= 1
                time.sleep(30)

        hacfg = {}
        if existing_config:
            hadr_cfgs = ['HADR_LOCAL_HOST', 'HADR_LOCAL_SVC', 'HADR_REMOTE_HOST', 'HADR_REMOTE_SVC',
                         'HADR_TARGET_LIST']
            for c in hadr_cfgs:
                hacfg.update({c: existing_config[c]})
        else:
            if dr_configured:
                hacfg.update({'HADR_LOCAL_HOST': "{}|{}".format(self.conf['fqdn'],
                                                                fmtn.get_external_hostname())})
                hacfg.update({'HADR_LOCAL_SVC': "{}|{}".format(self.conf['db2_hadr_port'],
                                                               fmtn.get_external_hadr_port())})
            else:
                hacfg.update({'HADR_LOCAL_HOST': self.conf['fqdn']})
                hacfg.update({'HADR_LOCAL_SVC': self.conf['db2_hadr_port']})

            # dr site needs ports published from primary site to set remote host
            if disaster_recovery_site and len(target_list) == 0:
                raise Exception(
                    "Primary pods/ports are not published to COS, failing init")

            # this is a single node primary recovery site but has not been initialized, this means we don't have
            # the port from the disaster recovery site, because dr site can't be setup without the
            # backup and keystore generated on primary site, we will set dr host, and non-reachable port
            # until it can be reconfigured
            if dr_configured and not disaster_recovery_site and \
                    len(target_list) == 0 and len(self.conf['peers']) == 1:
                prs_initialization = True
                target_list.append("{}:{}".format(
                    self.conf['disaster_recovery_host'], "51987"))

            # when no primary host specified DR site will need to set m-0 or we will need to specify in file
            if self.conf['fqdn'] != primary_host and not disaster_recovery_site:
                hacfg.update({'HADR_REMOTE_HOST': primary_host})
            else:
                hacfg.update(
                    {'HADR_REMOTE_HOST': target_list[0].split(":")[0]})

            # TODO:this will not cover the case where DR Site is primary and we re-init
            hacfg.update({'HADR_REMOTE_SVC': target_list[0].split(":")[1]})
            targets = "|".join(["{}".format(member) for member in target_list])
            hacfg.update({'HADR_TARGET_LIST': '{}'.format(targets)})
        hacfg.update({'HADR_REMOTE_INST': self.conf['db2_instance_name']})
        hacfg.update({'HADR_TIMEOUT': 120})

        # During single node primary site initialization we assume the
        # former single node is a primary site node
        if prs_initialization:
            designated_role = "PRIMARY"
        else:
            designated_role = Db2HADR(self.conf).set_designated_role()

        # always set disaster recovery site to SUPERASYNC
        if disaster_recovery_site:
            hacfg.update({'HADR_SYNCMODE': 'SUPERASYNC'})
        elif designated_role == "PRIMARY":
            hacfg.update({'HADR_SYNCMODE': 'SYNC'})
        elif designated_role == "STANDBY" and \
            (self.conf['fqdn'] == standby_list[-1]) or \
                (designated_role == "STANDBY" and len(self.conf['extended_peers']) == 2):
            hacfg.update({'HADR_SYNCMODE': 'SYNC'})
        else:
            hacfg.update({'HADR_SYNCMODE': 'SYNC'})
        hacfg.update({'HADR_PEER_WINDOW': 150})
        if self.conf['db2_ssl_svr_label'] != "CA-signed":  # temporary disable code TODO
            hacfg.update({'HADR_SSL_LABEL': self.conf['db2_ssl_svr_label']})
        hacfg.update({'LOGINDEXBUILD': 'ON'})

        if os.path.exists(conf_backup_file):
            os.remove(conf_backup_file)

        return hacfg

    # generate_target_list will return the target list with dr node appended if it is able to retrieve it
    def generate_target_list(self, fmtn=None):
        db2_hadr_port = self.conf['db2_hadr_port']
        local_peers = ["{}:{}".format(host, db2_hadr_port) for host in self.conf['peers']
                       if host != self.conf['fqdn']]

        hadr_target_list = local_peers.copy()

        if fmtn is None:
            fmtn = formation.Formation(self.conf['crd_group'],
                                       self.conf['account'],
                                       self.conf['id'])

        if fmtn.is_dr_configured():
            cos = bucket.Bucket(self.conf)

            port_data = cos.get_external_port_data_from_cos()

            if port_data is None:
                logger.error(
                    "Unable to retrieve port data from COS, returning local target list")
            else:
                for idx, _ in enumerate(port_data['pods']):
                    hadr_target_list.append("{}:{}".format(
                        port_data['hostnames'][idx], port_data['ports'][idx]))

        return hadr_target_list

    def generate_dbcfg_forhadr(self, role, bb=False):
        c = self.build_hadr_config()
        cmd = "UPDATE DATABASE CONFIGURATION FOR {0} USING".format(self.dbname)
        cfgs = ["{0} {1} ".format(k, c[k]) for k in c.keys()]
        full_cmd = cmd
        for cfg in cfgs:
            full_cmd += " {0} ".format(cfg)
        if bb and (role == "primary"):
            return "CALL SYSPROC.ADMIN_CMD(' " + full_cmd + "')"
        else:
            return full_cmd

    def gen_db2remstmgr_cmds(self,
                             protocol='s3',
                             action='list',
                             bdir=None,
                             subdir=None,
                             bfile=None,
                             source=None,
                             target=None):
        if action == "list":
            if bdir:
                prefix = "CSYS.{0}".format(bdir.replace("CSYS.", ""))
            if bdir and subdir:
                prefix = "CSYS.{0}/{1}".format(
                    bdir.replace("CSYS.", ""), subdir)
            if bdir and bfile:
                prefix = "CSYS.{0}/{1}".format(
                    bdir.replace("CSYS.", ""), bfile)
            cmd = (
                "db2RemStgManager {0} {1} server={2} auth1={3} auth2={4} "
                "container={5} prefix={6}".format(protocol,
                                                  action,
                                                  self.ep,
                                                  self.auth1,
                                                  self.auth2,
                                                  self.container,
                                                  prefix)
            )

        elif action in ("get", "put"):
            if bdir:
                source = "CSYS.{0}".format(bdir.replace("CSYS.", ""))
            if bdir and subdir:
                source = "CSYS.{0}/{1}".format(
                    bdir.replace("CSYS.", ""), subdir)
            if bdir and subdir and bfile:
                source = "CSYS.{0}/{1}/{2}".format(
                    bdir.replace("CSYS.", ""), subdir, bfile)
            if bdir and bfile:
                source = "CSYS.{0}/{1}".format(
                    bdir.replace("CSYS.", ""), bfile)
            if source:
                source = source
            if target:
                target = target
            cmd = (
                "db2RemStgManager {0} {1} server={2} auth1={3} auth2={4} "
                "container={5} source={6} target={7}".format(protocol,
                                                             action,
                                                             self.ep,
                                                             self.auth1,
                                                             self.auth2,
                                                             self.container,
                                                             source,
                                                             target)
            )

        return cmd

    def upload_userfile_cos(self):
        cos_target = "{}/users.json".format(self.bdir)
        logger.info("Uploading userfile details to COS dir: {} from local file {}".format(
            cos_target, self.user_file))
        self.s3bucket.upload_file(self.user_file, cos_target)
        logger.info("Completed upload")
