import ibm_db
from compose.db2.utils.db2rc import SQLError
from cdb import log
from cdb import service
from compose.db2 import configuration
logger = log.get_logger(__name__)


class DBConnException(Exception):
    def __init__(self, message):
        self.message = message


class DBStmtException(Exception):
    def __init__(self, message):
        self.message = message


class Db2connection():
    def __init__(self, ip=None, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        if ip is None:
            self.ip = self.conf['fqdn']
        else:
            self.ip = ip
        self.username = self.conf['db2_sysadmin_user']
        self.SSLClientKeystoredb = self.conf['db2_ssl_svr_keydb']
        self.SSLClientKeystash = self.conf['db2_ssl_svr_stash']
        self.conntimeout = 60

        try:
            self.password = self.conf['compose_password']
        except AttributeError as e:
            raise(e)
        self.dbname = self.conf['db_name']

    def getInstanceAttachment(self, ip=None, ssl=False):
        """Get an instance attachment"""
        if ssl and (ip is None):
            return self.getDatabaseConnection(self.ip,
                                              False,
                                              ssl,
                                              parms="attach=true")
        elif ssl and (ip is not None):
            return self.getDatabaseConnection(ip,
                                              False,
                                              ssl,
                                              parms="attach=true")
        else:
            if ip is None:
                return self.getDatabaseConnection(self.ip,
                                                  parms="attach=true")
            else:
                return self.getDatabaseConnection(ip,
                                                  parms="attach=true")

    def getDbPersistentConn(self, ip=None, ssl=False):
        if ssl and (ip is None):
            return self.getDatabaseConnection(self.ip, True, ssl)
        elif ssl and (ip is not None):
            return self.getDatabaseConnection(ip, True, ssl)
        else:
            if ip is None:
                return self.getDatabaseConnection(self.ip, True)
            else:
                return self.getDatabaseConnection(ip, True)

    def getDatabaseConnection(self,
                              ip=None,
                              pconn=False,
                              ssl=False,
                              conntimeout=60,
                              parms=""):
        if ssl and (ip is None):
            dsn = "UID=" + self.username + ";PWD=" + self.password + ";DATABASE=" + self.dbname + \
                  ";HOSTNAME=" + str(self.ip) + ";PORT=" + \
                  self.conf['db2_ssl_svcename'] + ";PROTOCOL=TCPIP;SECURITY=ssl;" + \
                  "SSLClientKeystoredb=" + self.SSLClientKeystoredb + \
                  ";SSLClientKeystash=" + self.SSLClientKeystash + \
                  ";CONNECTTIMEOUT=" + str(conntimeout) + parms
        elif ssl and (ip is not None):
            dsn = "UID=" + self.username + ";PWD=" + self.password + ";DATABASE=" + self.dbname + \
                  ";HOSTNAME=" + str(ip) + ";PORT=" + \
                  self.conf['db2_ssl_svcename'] + \
                  ";PROTOCOL=TCPIP;SECURITY=ssl;" + \
                  "SSLClientKeystoredb=" + self.SSLClientKeystoredb + \
                  ";SSLClientKeystash=;" + self.SSLClientKeystash + \
                  ";CONNECTTIMEOUT=" + str(conntimeout) + parms
        else:
            if ip is None:
                dsn = "UID=" + self.username + ";PWD=" + self.password + ";DATABASE=" + self.dbname + \
                      ";HOSTNAME=" + str(self.ip) + ";PORT=" + self.conf['db2_tcp_svcename'] + \
                      ";PROTOCOL=TCPIP;" + \
                      "CONNECTTIMEOUT=" + str(conntimeout) + parms
            else:
                dsn = "UID=" + self.username + ";PWD=" + self.password + ";DATABASE=" + self.dbname + \
                      ";HOSTNAME=" + str(ip) + ";PORT=" + self.conf['db2_tcp_svcename'] + \
                      ";PROTOCOL=TCPIP;" + \
                      "CONNECTTIMEOUT=" + str(conntimeout) + parms
        try:
            if pconn:
                conn = ibm_db.pconnect(dsn, '', '')
            else:
                conn = ibm_db.connect(dsn, '', '')
            return conn
        except Exception:
            err = ibm_db.conn_errormsg()
            warn_error_code = SQLError(err).sqlwarnerr()
            if warn_error_code in ("SQL1776N",
                                   "SQL30081N",
                                   "SQL30061N",
                                   "SQL1117N",
                                   "SQL1336N"):
                logger.error(err)
                pass
            else:
                raise DBConnException(
                    "Error: Not able to connect to the database:{0} with err: {1}".format(self.dbname, err))


class Db2Utils():
    """ Class which holds general utility functions that act against the database that
        will (re)open and close database connections as needed
    """

    def get_summary(self, duration):
        """Get a summary of the database for performance analysis with a 30 second duration"""
        db2Conn = Db2connection()
        conn = db2Conn.getDatabaseConnection()
        if conn:
            try:
                inn = (duration,)
                stmt, _ = ibm_db.callproc(conn, 'monreport.dbsummary', inn)
                output = ""
                while ibm_db.fetch_row(stmt):
                    output += ibm_db.result(stmt, 0) + "\n"
                return output
            except:
                raise DBStmtException("Transaction couldn't be completed: {0}".format(
                    ibm_db.stmt_errormsg()))
            finally:
                ibm_db.close(conn)

    def do_sysproc_admincmd(self, sql=''):
        """This is a function to do execute a db2 procedure"""
        db2Conn = Db2connection()
        conn = db2Conn.getDatabaseConnection()
        if conn:
            try:
                stmt, _ = ibm_db.callproc(
                    conn, 'SYSPROC.ADMIN_CMD', (sql,))
                output = ""
                while ibm_db.fetch_row(stmt):
                    output += ibm_db.result(stmt, 0) + "\n"
                return output
            except:
                raise DBStmtException("Transaction couldn't be completed: {0}".format(
                    ibm_db.stmt_errormsg()))
            finally:
                ibm_db.close(conn)

    def drop_db(self, dbname):
        db2Conn = Db2connection()
        conn = db2Conn.getInstanceAttachment()
        if conn:
            try:
                ibm_db.dropdb(conn, dbname)
            except Exception:
                raise DBStmtException("Transaction couldn't be completed: {0}".format(
                    ibm_db.stmt_errormsg()))
            finally:
                ibm_db.close(conn)

    def create_db(self, dbname):
        db2Conn = Db2connection()
        conn = db2Conn.getInstanceAttachment()
        if conn:
            try:
                ibm_db.createdb(conn, dbname)
            except Exception:
                raise DBStmtException("Transaction couldn't be completed: {0}".format(
                    ibm_db.stmt_errormsg()))
            finally:
                ibm_db.close(conn)


class Db2SQL:
    """ Class meant to run SQL select statements which opens a connection during object
        instantiation
    """

    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        self.uptime = "SELECT * FROM SYSIBM.SYSDUMMY1 WITH UR"
        self.get_activity = (
            "MON_GET_ACTIVITY_DETAILS"
        )
        self.connections = (
            "MON_GET_ACTIVITY_DETAILS"
        )
        self.db_availability = (
            "SELECT DB_STATUS FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        # This will return both open (APPLS_CUR_CONS) and active (APPLS_IN_DB2) connections
        self.db_connections = (
            "SELECT APPLS_CUR_CONS, APPLS_IN_DB2 FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.db_commits = (
            "SELECT TOTAL_APP_COMMITS, INT_COMMITS, TOTAL_COMMIT_TIME, TOTAL_APP_ROLLBACKS, INT_ROLLBACKS FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.db_backups = (
            "SELECT LAST_BACKUP, TOTAL_BACKUP_TIME, TOTAL_BACKUPS FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.db_stmts = (
            "SELECT ROWS_DELETED, INT_ROWS_DELETED, ROWS_INSERTED, INT_ROWS_INSERTED, ROWS_UPDATED, INT_ROWS_UPDATED, "
            "SELECT_SQL_STMTS, UID_SQL_STMTS FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.db_activities = (
            "SELECT ACT_COMPLETED_TOTAL, ACT_ABORTED_TOTAL, ACT_REJECTED_TOTAL FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.db_logs = (
            "SELECT LOG_DISK_WAITS_TOTAL FROM TABLE(MON_GET_DATABASE(NULL)) WITH UR"
        )
        self.ha_status = (
            "SELECT HADR_ROLE, STANDBY_ID, HADR_CONNECT_STATUS, HADR_STATE, HADR_SYNCMODE,"
            "TIME_SINCE_LAST_RECV, HADR_LOG_GAP, HEARTBEAT_MISSED, HEARTBEAT_EXPECTED,"
            "PRIMARY_MEMBER_HOST, STANDBY_MEMBER_HOST, STANDBY_REPLAY_LOG_TIME, PRIMARY_LOG_TIME,PRIMARY_LOG_FILE, STANDBY_LOG_FILE,STANDBY_REPLAY_LOG_FILE from table(MON_GET_HADR(NULL)) WITH UR"
        )
        self.ha_primary = (
            "SELECT PRIMARY_MEMBER_HOST FROM TABLE(MON_GET_HADR(NULL)) WITH UR"
        )
        self.ha_standby = (
            "SELECT STANDBY_MEMBER_HOST FROM TABLE(MON_GET_HADR(NULL)) WITH UR"
        )

        self.ha_role = (
            "SELECT HADR_ROLE FROM TABLE(MON_GET_HADR(NULL)) WITH UR"
        )
        self.tables_count = (
            "SELECT COUNT(*) AS TABLES FROM SYSCAT.TABLES T WHERE T.TYPE='T'"
        )
        self.tables_sizes = (
            "SELECT SUBSTR(TABSCHEMA,1,18) TABSCHEMA,SUBSTR(TABNAME,1,30) "
            "TABNAME,(DATA_OBJECT_P_SIZE + INDEX_OBJECT_P_SIZE + "
            "LONG_OBJECT_P_SIZE + LOB_OBJECT_P_SIZE + XML_OBJECT_P_SIZE) "
            "AS TOTAL_SIZE_IN_KB,(DATA_OBJECT_P_SIZE + INDEX_OBJECT_P_SIZE + "
            "LONG_OBJECT_P_SIZE + LOB_OBJECT_P_SIZE + XML_OBJECT_P_SIZE)/1024 AS "
            "TOTAL_SIZE_IN_MB, (DATA_OBJECT_P_SIZE + INDEX_OBJECT_P_SIZE + "
            "LONG_OBJECT_P_SIZE + LOB_OBJECT_P_SIZE + XML_OBJECT_P_SIZE) / (1024*1024) "
            "AS TOTAL_SIZE_IN_GB FROM SYSIBMADM.ADMINTABINFO WHERE TABSCHEMA NOT LIKE 'SYS%' WITH UR"
        )
        self.db2_version = (
            "SELECT SERVICE_LEVEL FROM SYSIBMADM.ENV_INST_INFO WITH UR"
        )
        self.db2_instance_name = (
            "SELECT INST_NAME FROM SYSIBMADM.ENV_INST_INFO WITH UR"
        )
        # see if we can check backups via procedure
        if self.conf['repo_type'] == "s3":
            self.db2_latest_backup = (
                "SELECT distinct(START_TIME) FROM SYSIBMADM.DB_HISTORY where OPERATION='B'"
                " AND ( LOCATION='{0}' OR LOCATION='s3' ) "
                "ORDER BY START_TIME DESC WITH UR".format('DB2REMOTE')
            )
            self.db2_get_backup_times = (
                "SELECT DISTINCT START_TIME, END_TIME, SECONDS_BETWEEN(END_TIME, START_TIME) AS DURATION_SECS"
                " FROM SYSIBMADM.DB_HISTORY where OPERATION='B'"
                " AND ( LOCATION='{0}' OR LOCATION='s3' )"
                "ORDER BY START_TIME DESC WITH UR".format('DB2REMOTE')
            )
        else:
            self.db2_latest_backup = (
                "SELECT distinct(START_TIME) FROM SYSIBMADM.DB_HISTORY where OPERATION='B'"
                " AND LOCATION='{0}' ORDER BY START_TIME DESC WITH UR".format(
                    self.conf['repo_type'])
            )
            self.db2_get_backup_times = (
                "SELECT DISTINCT START_TIME, END_TIME, SECONDS_BETWEEN(END_TIME, START_TIME) AS DURATION_SECS"
                " FROM SYSIBMADM.DB_HISTORY where OPERATION='B'"
                " AND LOCATION='{0}' ORDER BY START_TIME DESC WITH UR".format(
                    self.conf['repo_type'])
            )

        self.db2_snapdb_bkp = (
            "SELECT LAST_BACKUP FROM SYSIBMADM.SNAPDB WITH UR"
        )
        self.dbmcfg = (
            "SELECT * FROM SYSIBMADM.DBMCFG"
        )

        self.dbcfg = (
            "SELECT * FROM SYSIBMADM.DBCFG"
        )

        self.diag = (
            "SELECT * FROM SYSIBMADM.PDLOGMSGS_LAST24HOURS"
            "WHERE MSGSEVERITY='C' ORDER BY TIMESTAMP DESC"
        )

        self.db2_get_user_connections = (
            "SELECT AGENT_ID FROM SYSIBMADM.APPLICATIONS WHERE AUTHID = \'{0}\'"
        )
        self.db2_get_object_store_settings = (
            "select REG_VAR_ON_DISK_VALUE from table(env_get_reg_variables(-1)) where reg_var_name='DB2_OBJECT_STORAGE_SETTINGS'"
        )

    def run_desired_select_sql(self, ip, query, fetch='both', conntimeout=60):

        if (service.stat('db2') != "run"):
            return None
        dbconn = Db2connection(ip=ip, conf=self.conf)
        conn = dbconn.getDatabaseConnection(ip, conntimeout=conntimeout)
        if conn:
            try:
                stmt = ibm_db.exec_immediate(conn, query)
                if ibm_db.fetch_row(stmt):
                    stmt = ibm_db.exec_immediate(conn, query)
                if fetch == "both":
                    # fetch_both returns a dict but contains values
                    output = ibm_db.fetch_both(stmt)
                    values = []
                    while output:
                        values.append(output)
                        output = ibm_db.fetch_both(stmt)
                    return values
                elif fetch == "double":
                    return ibm_db.fetch_tuple(stmt)
                elif fetch == "assoc":
                    # fetch_assoc returns a dict, so return a list of dicts
                    output = ibm_db.fetch_assoc(stmt)
                    values = []
                    while output:
                        values.append(output)
                        output = ibm_db.fetch_assoc(stmt)
                    return values
            except:
                raise DBStmtException("Transaction couldn't be completed: {0}".format(
                    ibm_db.stmt_errormsg()))
            finally:
                ibm_db.close(conn)
