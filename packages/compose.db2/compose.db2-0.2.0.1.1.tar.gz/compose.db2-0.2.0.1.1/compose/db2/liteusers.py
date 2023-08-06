from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.sqlUtils import Db2connection, DBStmtException
from compose.db2.utils.db2rc import db2_cmd_execution
from compose.db2.users import UserManager
from time import sleep
from cdb import log
from json import load, loads
import ibm_db
from compose.db2.utils.sqlUtils import Db2SQL

logger = log.get_logger(__name__)

def readUntilSynced():
	timeout = 0
	holder = None
	while(True):
		try:
			masterFD = open("/data/blumeta0/db2_config/users.json", "r+")
			jsonData = load(masterFD)
			if holder == None:
				holder = jsonData
				jsonData = None

				masterFD.close()
				sleep(0.5)
			else:
				if jsonData["rev"] == holder["rev"]:
					masterFD.close()
					return jsonData
				else:
					holder = jsonData
					jsonData = None

					masterFD.close()
					sleep(0.5)

		except Exception as e:
			if not masterFD.closed:
				masterFD.close()
			timeout += 1
			if timeout == 5:
				raise(e)
			continue


class LiteUserManager(UserManager, DB2Commands):
	def __init__(self, conf=None, forceSync=False):
		UserManager.__init__(self, conf, forceSync, True)
		DB2Commands.__init__(self, conf)
		self.logger.info("Reading from master json: {}".format(self.conf['db2_user_file']))
		masterJson = readUntilSynced()
		if masterJson["rev"] >= self.json_data["rev"]:
			self.logger.info("Using master json data")
			self.json_data = masterJson


	def create_lite_user_schema(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)
		schema_name = user_data['username']
		sql = "CREATE SCHEMA {}".format(schema_name)

		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Setting up Schema for user: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		sql = "TRANSFER OWNERSHIP OF SCHEMA {0} TO USER {1} PRESERVE PRIVILEGES".format(
			schema_name, user_data['username'])
		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Granting schema privilege to user: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		ibm_db.close(conn)

	def create_lite_user_tablespace(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)
		size = "200M"
		tablespace = "{}space1".format(user_data['username'])

		sql="CREATE TABLESPACE {0} MAXSIZE {1}".format(tablespace, size)
		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Creating tablespace for user: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		sql = "TRANSFER OWNERSHIP OF TABLESPACE {0} TO USER {1} PRESERVE PRIVILEGES".format(
			tablespace, user_data['username']
		)
		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Transferring ownership of table to user: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		ibm_db.close(conn)

	def grant_lite_user_privilege(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)
		tablespace = "{}space1".format(user_data['username'])

		sql = "GRANT CREATETAB ON DATABASE TO user {0}".format(user_data['username'])
		stmt = ibm_db.prepare(conn,sql)
		self.logger.info("Granting database privilege to: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		sql = "GRANT USE OF TABLESPACE {0} TO user {1}".format(tablespace, user_data['username'])
		stmt = ibm_db.prepare(conn,sql)
		self.logger.info("Grant use of tablespace to user: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		ibm_db.close(conn)

	# TODO: figure out if this is even needed for v2
	# currently not functioning as the role is not existing?
	def grant_role(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)

		# may have to change bluedemouser to just bluuser
		sql = "GRANT ROLE \"BLUDEMOUSER\" TO user {0}".format(user_data['username'])
		stmt = ibm_db.prepare(conn,sql)
		self.logger.info("Grant bludemouser role to: {}".format(user_data['username']))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
			self.logger.error("Rolling back")
			ibm_db.rollback(conn)
			ibm_db.close(conn)
			raise DBStmtException(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		ibm_db.close(conn)

	def remove_lite_user_table(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)
		tablespace = "{}space1".format(user_data['username'])

		sql = "DROP TABLESPACE {}".format(tablespace)
		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Removing table {}".format(tablespace))

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		sql = "DROP TABLE ERRORSCHEMA.ERRORTABLE"
		stmt = ibm_db.prepare(conn, sql)
		self.logger.info("Dropping errorschema table")

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)

		ibm_db.close(conn)

	@log.log_execution(logger)
	def remove_error_schema(self, data):
		conn = Db2connection(conf=self.conf).getDatabaseConnection()
		user_data = loads(data)
		schema = user_data['username']

		sql = "DROP SCHEMA ERRORSCHEMA RESTRICT"
		stmt = ibm_db.prepare(conn,sql)
		self.logger.info("Dropping errorschema schema")

		try:
			ibm_db.execute(stmt)
		except Exception as e:
			self.logger.error(e)
			self.logger.error(ibm_db.stmt_errormsg())
		else:
			ibm_db.commit(conn)
		ibm_db.close(conn)

		cmd = "runuser -l {0} -c \"{1};{2}\"".format(
			self.dbuser,
			self.connect_db_remote(),
			self.delete_lite_schema.format(schema)
		)
		logger.info(cmd.replace(self.dbuser, "xxxxxxx").replace(self.using, "xxxxxxx"))
		try:
			db2_cmd_execution(cmd)
		except Exception as e:
			raise(e)
		finally:
			self.db2_terminate()

	@log.log_execution(logger)
	def force_lite_user_apps(self, user):
		self.logger.info(user)
		username = loads(user)['username']

		app_ids = self.get_user_applications(username)
		logger.info(app_ids)

		if len(app_ids) == 0:
			return

		app_handles = ""
		for app_id in app_ids:
			app_handles += str(app_id['AGENT_ID']) + ", "
		app_handles = app_handles[:-2]

		logger.info("forcing apps: {}".format(app_handles))

		self.force_application(app_handles)


	@log.log_execution(logger)
	def db2_terminate(self):
		cmd = "runuser -l {0} -c \"{1}\"".format(self.dbuser,
													 self.terminate)
		logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(
			self.using, "xxxxxx"
		))
		db2_cmd_execution(cmd)

	def get_user_applications(self, username):
		try:
			sql = Db2SQL(self.conf)
			query = sql.db2_get_user_connections.format(username.upper())
			logger.info(query)
			application_ids = sql.run_desired_select_sql(ip=self.conf['fqdn'],
														query=query,
														fetch='assoc')
			return application_ids
		except Exception as e:
			logger.error(e)
			raise (e)

	def force_application(self, app_handles):
		cmd = "runuser -l {0} -c \"{1};{2}\"".format(self.dbuser,
														self.attach_to_dbnode(),
														self.force_apps.format(app_handles))
		logger.info(cmd.replace(self.dbuser, "xxxxxx").replace(self.using, "xxxxxx"))
		try:
			db2_cmd_execution(cmd)
		except Exception as e:
			raise (e)
		finally:
			self.db2_terminate()