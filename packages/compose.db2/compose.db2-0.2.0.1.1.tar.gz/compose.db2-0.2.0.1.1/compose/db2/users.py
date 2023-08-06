import hashlib
import os
import time
from base64 import encodebytes, decodebytes
from json import JSONDecodeError, load, loads, dumps
from compose.db2 import configuration
from compose.db2.utils.sqlUtils import Db2connection, DBStmtException
from cdb import log
from compose.db2.utils.cloudUtils import S3Resource
from datetime import datetime
import string
import random
import ibm_db
from itertools import islice
import re

# For now rely on FormationLock to provide protection against server file, recipes are also gated to only run on leader
class UserManager:
    def __init__(self, conf=None, forceSync=False, lite=False):
        self.logger = log.get_logger(__name__)
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        if lite:
        	self.user_file = self.conf['db2_local_user_file']
        else:
        	self.user_file = self.conf['db2_user_file']
        self.fd = None
        self.dbtype = conf['type']
        self.restricted_users = ("db2inst1","rfmon","ucmon")
        if self.dbtype == "dv":
            self.restricted_users += ("cacheadmin","hive")
        self.dv_roles = ["DV_ADMIN", "DV_ENGINEER", "DV_STEWARD", "DV_WORKER"]

        if 'cosdisabled' not in self.conf or not self.conf['cosdisabled']: self.init_user_file(forceSync)

        #open file if we did not have to create one in the prior step with blank template
        if self.fd is None:
            self.logger.info("Loading json data from: {}".format(self.user_file))
            self.fd = open(self.user_file, "r+")
            self.json_data = load(self.fd)

    def __del__(self):
        self.logger.info("Closing file")
        self.fd.truncate()
        self.fd.close()
        #os.chmod(self.user_file, 0o740)

    def init_user_file(self,forceSync):
        cos = S3Resource(self.conf)
        size_of_file = 0
        cos_file = cos.s3bucket.objects.filter(Prefix='{}/users.json'.format(cos.bdir))
        num_user_files = sum(1 for _ in cos_file)
        if num_user_files > 0:
            for f in cos_file:
                mod_time = f.last_modified
                size_of_file = f.size
        sync_from_cos = False

        # Check if file exists
        try:
            st = os.stat(self.user_file)
            #if cos file exists and local mtime is less than server mtime, needs sync
            if num_user_files > 0 and \
                size_of_file > 0 and \
                (forceSync == True or st.st_mtime < mod_time.timestamp()):
                sync_from_cos = True
        except FileNotFoundError:
            self.logger.error("No user file found in dir: {}".format(self.user_file))
            #file doesn't exist, sync from COS
            if num_user_files > 0:
                sync_from_cos = True
            else:
                # compose-db2 init/config should initialize the user file if it doesn't exist,
                # if not there and not in COS we need to throw an error
                raise UserFileNotInitializedException

        if sync_from_cos:
            self.logger.info("Syncing user details from COS")
            cos.s3bucket.download_file("{}/users.json".format(cos.bdir),self.user_file)
            os.chown(self.user_file, 1500, 1500)
            os.chmod(self.user_file, 0o740)

            st = os.stat(self.user_file)
            if os.geteuid() == 0 and st.st_uid != 1500:
                os.chown(self.user_file, 1500, 1500)

            #update mtime
            server_mod_epoch_time = mod_time.timestamp()
            self.sync_mtime(server_mod_epoch_time)

    def sync_mtime(self, server_timestamp):
        st = os.stat(self.user_file)
        self.logger.info("Syncing mtime from local {} to server {}".format(int(st.st_mtime), int(server_timestamp)))
        os.utime(self.user_file, (int(st.st_atime), int(server_timestamp)))

    def create_user(self, data):
        ibmid_user = False
        user_data = loads(data)
        user_data['locked'] = False
        user_data['locked_count'] = 0
        user_data['locked_time'] = 0
        username = user_data['username']
        if 'policyname' not in user_data or user_data['policyname'] == "${policyname}":
            user_data['policyname'] = "default"

        # ibmid users do not require a password re user plugin, however backfilling the password with random as a failsafe
        if 'ibmid' in user_data and user_data['ibmid'] != "${ibmid}" and user_data['ibmid'] != "":
            ibmid_user = True
            if not re.match("^IBMid-.*", user_data['ibmid']) and not re.match("^iam-ServiceId-.*", user_data['ibmid']):
                raise IBMIDInvalidException
            user_data['password'] = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
            # IBM Service ID must be unique
            if user_data['ibmid'] in self.json_data['iamusers']:
                raise IAMUserAlreadyExistsException
        # Not an ibm user, requires at least either password or hash to exist in user data
        # Would have been catched as well on validate password line, but provide better explanation
        else:
            if ('hash' not in user_data or user_data['hash'] == "${hash}") and \
            ('password' not in user_data or user_data['password'] == "${password}"):
                raise NoPasswordAndHashException

        # ensure optional params are populated
        if 'email' not in user_data or user_data['email'] == "${email}": user_data['email'] = ""
        if 'group' not in user_data or user_data['group'] == "${group}": user_data['group'] = "bluusers"
        if 'ibmid' not in user_data or user_data['ibmid'] == "${ibmid}": user_data['ibmid'] = ""
        # Ensure to popluate the missing hash/password to empty string
        if 'hash' not in user_data or user_data['hash'] == "${hash}": user_data['hash'] = ""
        if 'password' not in user_data or user_data['password'] == "${password}": user_data['password'] = ""
        
        if self.dbtype == 'dv':
            if 'role' not in user_data or user_data['role'] == "${role}": user_data['role'] = "DV_WORKER"

        if user_data['group'] != "bluusers" and user_data['group'] != "bluadmin":
            raise InvalidUserGroupException
        
        if self.dbtype == 'dv':
            if user_data['role'] not in self.dv_roles:
                raise InvalidUserRoleException

        self.logger.info("Creating User: {}".format(username))

        if username in self.json_data['users']:
            self.logger.error("User already exists")
            raise UserAlreadyExistsException

        if len(user_data['hash']) == 0 and not validate_password(user_data['password']):
            self.logger.error("Invalid password format provided")
            raise ValidationError

        if len(user_data['hash']) != 0:
            user_data['password'] = user_data['hash']
        else:
            user_data['password'] = create_oldap_pw(user_data['password'])

        #Insert User into Db2 Table
        if 'db2disabled' not in self.conf or not self.conf['db2disabled']:
            conn = Db2connection(conf=self.conf).getDatabaseConnection()
            if(self.dbtype == 'dv'):
                sql = "INSERT INTO DB2INST1.USER_TABLE (USERNAME,GROUP,EMAIL,LOCKED,IBMID,POLICYNAME,ROLE) \
                VALUES (?,?,?,?,?,?,?)"
            else:
                sql = "INSERT INTO DB2INST1.USER_TABLE (USERNAME,GROUP,EMAIL,LOCKED,IBMID,POLICYNAME) \
                    VALUES (?,?,?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, user_data['group'])
            ibm_db.bind_param(stmt, 3, user_data['email'])
            ibm_db.bind_param(stmt, 4, user_data['locked'])
            ibm_db.bind_param(stmt, 5, user_data['ibmid'])
            ibm_db.bind_param(stmt, 6, user_data['policyname'])
            
            if(self.dbtype == 'dv'): 
                ibm_db.bind_param(stmt, 7, user_data['role'])
                grantSql = "GRANT ROLE " + user_data['role'] + " TO USER " + username
                grantStmt = ibm_db.prepare(conn, grantSql)
            try:
                if(self.dbtype == 'dv'):
                    ibm_db.execute(grantStmt)
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

        if ibmid_user:
            key = user_data['ibmid']
            if "liteuser" in user_data.keys() and user_data["liteuser"]:
                key += ":{}".format(user_data['username'])
                del user_data["liteuser"]
            self.json_data['iamusers'][key] = username
        # remove ibmid from payload since we now store it in iamusers dict
        if 'ibmid' in user_data:
            del user_data['ibmid']
        # Hash will be either an empty string or equal to password, remove from payload
        del user_data['hash']

        self.json_data['users'][username] = user_data
        self.write_user_file()

    def delete_user(self, data):
        user_data = loads(data)
        #check system locking
        username = user_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException
        self.logger.info("Deleting user: {}".format(username))
        if username in self.json_data['users']:
            #Delete User into Db2 Table
            if 'db2disabled' not in self.conf or not self.conf['db2disabled']:
                conn = Db2connection(conf=self.conf).getDatabaseConnection()
                sql = "DELETE FROM DB2INST1.USER_TABLE WHERE USERNAME=?"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, username)
                if(self.dbtype == 'dv'):
                    revokeSql = "REVOKE ROLE " + self.json_data['users'][username]['role']+ " FROM USER " + username
                    revokeStmt = ibm_db.prepare(conn, revokeSql)
                try:
                    if(self.dbtype == 'dv'):
                        ibm_db.execute(revokeStmt)
                    ibm_db.execute(stmt)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error(ibm_db.stmt_errormsg())
                    self.logger.error("Rolling back")
                    ibm_db.rollback(conn)
                    ibm_db.close(conn)
                    raise DBStmtException(ibm_db.stmt_errormsg())
                else:
                    self.logger.info("Committing transaction")
                    ibm_db.commit(conn)
                ibm_db.close(conn)

            # search the iamusers array and delete the entries where the value matches the username
            for iamkey, un in self.json_data['iamusers'].items():
                if username == un:
                    print("Deleting IAM key {}".format(iamkey))
                    del self.json_data['iamusers'][iamkey]
                    break
            self.json_data['users'].pop(username)
            self.write_user_file()
        else:
            raise NoUserExistsException

    def change_password(self, data):
        user_data = loads(data)
        username = user_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException
        self.logger.info("Modifying user: {}".format(username))
        if username not in self.json_data['users']:
            self.logger.error("Cannot change password on non-existing user: {}".format(username))
            raise NoUserExistsException

        if len(user_data['hash']) != 0 and user_data['hash'] != "${hash}":
            password = user_data['hash']
        else:
            password = create_oldap_pw(user_data['password'])

        self.json_data['users'][username]['password'] = password
        self.write_user_file()

    def change_password_bluuser(self, data):
        user_data = loads(data)
        username = user_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException
        self.logger.info("Changing bluuser password for user: {}".format(username))
        if username not in self.json_data['users']:
            self.logger.error("Cannot change password on non-existing user: {}".format(username))
            raise NoUserExistsException

        if self.json_data['users'][username]['group'] != "bluusers":
            self.logger.error("This endpoint can only be utilized by bluusers")
            raise UserIneligibleException

        curr_salt = extract_salt(self.json_data['users'][username]['password'])
        if self.json_data['users'][username]['password'][:6] == '{SSHA}':
            self.logger.info("Old hash")
            generated_hash = create_oldap_pw(user_data['oldpassword'], curr_salt, False) 
        else:
            self.logger.info("Standard hash")
            generated_hash = create_oldap_pw(user_data['oldpassword'], curr_salt)
        if generated_hash == self.json_data['users'][username]['password']:
            if len(user_data['newhash']) != 0 and user_data['newhash'] != "${newhash}":
                new_password = user_data['newhash']
            else:
                new_password = create_oldap_pw(user_data['newpassword'])
            self.json_data['users'][username]['password'] = new_password
            self.write_user_file()
        else:
            raise PasswordInvalidException

    def lock_user(self, data):
        user_data = loads(data)
        username = user_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException
        if username not in self.json_data['users']:
            self.logger.error("Cannot lock a non-existing user: {}".format(username))
            raise NoUserExistsException

        self.logger.info("Locking user: {}".format(username))
        self.json_data['users'][username]['locked'] = True
        self.write_user_file()

        #Set lock status in Db2
        if 'db2disabled' not in self.conf or not self.conf['db2disabled']:
            conn = Db2connection(conf=self.conf).getDatabaseConnection()
            sql = "UPDATE DB2INST1.USER_TABLE SET LOCKED=TRUE WHERE USERNAME=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, username)
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
                self.logger.info("Committing transaction")
                ibm_db.commit(conn)
            ibm_db.close(conn)


    def unlock_user(self, data):
        user_data = loads(data)
        username = user_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException
        if username not in self.json_data['users']:
            self.logger.error("Cannot unlock a non-existing user: {}".format(username))
            raise NoUserExistsException

        self.logger.info("Unlocking user: {}".format(username))
        self.json_data['users'][username]['locked'] = False
        self.json_data['users'][username]['locked_count'] = 0
        self.json_data['users'][username]['locked_time'] = 0
        self.write_user_file()

        #Set unlock status in Db2
        if 'db2disabled' not in self.conf or not self.conf['db2disabled']:
            conn = Db2connection(conf=self.conf).getDatabaseConnection()
            sql = "UPDATE DB2INST1.USER_TABLE SET LOCKED=FALSE WHERE USERNAME=?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, username)
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
                self.logger.info("Committing transaction")
                ibm_db.commit(conn)
            ibm_db.close(conn)

    def modify_user(self, data):
        mod_data = loads(data)
        self.logger.info("Modification parameters: {}".format(mod_data))
        username = mod_data['username']
        if username in self.restricted_users:
            raise NoUserExistsException

        if username not in self.json_data['users']:
            self.logger.error("Cannot modify a non-existing user: {}".format(username))
            raise NoUserExistsException

        self.logger.info("Modifying user: {}".format(username))

        db_update_data = {}
        if 'group' in mod_data and mod_data['group'] != "${group}":
            self.json_data['users'][username]['group'] = mod_data['group']
            db_update_data['group'] = mod_data['group']
        if 'email' in mod_data and mod_data['email'] != "${email}":
            self.json_data['users'][username]["email"] = mod_data['email']
            db_update_data['email'] = mod_data['email']

        #Shouldn't need a dv if statement since db2 doesn't use roles right?
        if 'role' in mod_data and mod_data['role'] != "${role}":
            oldRole = self.json_data['users'][username]['role']
            self.json_data['users'][username]['role'] = mod_data['role']
            db_update_data['role'] = mod_data['role']
        
        #Update row in Db2 table
        if 'db2disabled' not in self.conf or not self.conf['db2disabled']:
            conn = Db2connection(conf=self.conf).getDatabaseConnection()
            if(self.dbtype == 'dv' and not (oldRole == db_update_data)):
                grantSql = "GRANT ROLE " + db_update_data['role'] + " TO USER " + username
                revokeSql = "REVOKE ROLE " + oldRole + " FROM USER " + username
                self.logger.info("MOD TEMPLATE: {}".format(grantSql))
                self.logger.info("MOD TEMPLATE: {}".format(revokeSql))
                grantStmt = ibm_db.prepare(conn, grantSql)
                revokeStmt = ibm_db.prepare(conn, revokeSql)
            
            sql = "UPDATE DB2INST1.USER_TABLE SET {} WHERE USERNAME=?".format(",".join("{}=?".format(k) for k in db_update_data))
            self.logger.info("MOD TEMPLATE: {}".format(sql))
            stmt = ibm_db.prepare(conn, sql)
            for k, v in enumerate(db_update_data):
                ibm_db.bind_param(stmt, k+1, db_update_data[v])
            ibm_db.bind_param(stmt, len(db_update_data)+1, username)

            try:
                if(self.dbtype == 'dv' and not (oldRole == db_update_data)):
                    ibm_db.execute(grantStmt)
                    ibm_db.execute(revokeStmt)               
                ibm_db.execute(stmt)
            except Exception as e:
                self.logger.error(e)
                self.logger.error(ibm_db.stmt_errormsg())
                self.logger.error("Rolling back")
                ibm_db.rollback(conn)
                ibm_db.close(conn)
                raise DBStmtException(ibm_db.stmt_errormsg())
            else:
                self.logger.info("Committing transaction")
                ibm_db.commit(conn)
            ibm_db.close(conn)

        self.write_user_file()



    def list_users(self):
        user_dict = self.json_data['users'].copy()
        user_list = []

        for user in user_dict:
            del user_dict[user]['password']
            user_list.append(user)

        return user_list

    def get_user(self, data):
        user_data = loads(data)
        username = user_data['username']

        if username not in self.json_data['users']:
            self.logger.error("Cannot get a non-existing user: {}".format(username))
            raise NoUserExistsException

        user = self.json_data['users'][username].copy()
        del user['password']
        del user['locked_count']
        del user['locked_time']
        return user

    # this recipe is specific to db2inst1 and sets password to what
    # was passed to the rotate recipe
    def rotate_db2inst1(self, data):
        user_data = loads(data)
        hashed_pw = create_oldap_pw(user_data['password'])
        self.json_data['users']['db2inst1']['password'] = hashed_pw
        self.write_user_file()

    def write_user_file(self):
        self.json_data['rev'] = int(round(time.time() * 1000))
        try:
            self.logger.info("Writing file to: {}".format(self.user_file))
            self.fd.seek(0)
            self.fd.write(dumps(self.json_data, indent=4, separators=(',', ': ')))
            self.fd.flush()
            os.fsync(self.fd)
            self.fd.truncate()


            if 'cosdisabled' not in self.conf or not self.conf['cosdisabled']:
                #upload to COS
                cos = S3Resource(self.conf)
                cos_target = "{}/users.json".format(cos.bdir)
                self.logger.info("Uploading userfile details to COS dir: {} from local file {}".format(cos_target, self.user_file))
                cos.s3bucket.upload_file(self.user_file, cos_target)
                self.logger.info("Completed upload")

                #verify file exists
                cos_file = cos.s3bucket.objects.filter(Prefix='{}/users.json'.format(cos.bdir))
                num_user_files = sum(1 for _ in cos_file)
                if num_user_files > 0:
                    for f in cos_file: mod_time = f.last_modified
                    server_mod_epoch_time = mod_time.timestamp()
                    self.sync_mtime(server_mod_epoch_time)
                else:
                    self.logger.error("Unable to locate user file after upload")
                    raise UserFileUploadException
        except Exception as e:
            self.logger.error(e)
            raise (e)

    def construct_user_table(self):
        conn = Db2connection(conf=self.conf).getDatabaseConnection()
        #truncate user table
        sql = "TRUNCATE DB2INST1.USER_TABLE IMMEDIATE"
        self.logger.info("truncating DB2INST1.USER_TABLE")
        try:
            stmt = ibm_db.exec_immediate(conn,sql)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(ibm_db.stmt_errormsg())
            ibm_db.close(conn)
            raise DBStmtException(ibm_db.stmt_errormsg())

        #remove the system users as we do not populate these into user table
        trunc_users = self.json_data['users'].copy()
        del trunc_users['db2inst1']
        del trunc_users['rfmon']
        del trunc_users['ucmon']

        user_count = len(trunc_users)
        if user_count == 0:
            # no users to build, return success
            self.logger.info("No users to reconstruct")
            return

        iam_users = self.json_data['iamusers'].copy()
        for ibm_id, username in iam_users.items():
            if username in trunc_users:
                trunc_users[username]['ibmid'] = ibm_id

        self.logger.info("User List: {}".format(trunc_users.keys()))

        user_batches = chunk_users(trunc_users)

        try:
            for batch in user_batches:
                insert_batch_users(conn, batch)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(ibm_db.stmt_errormsg())
            self.logger.error("Rolling back")
            ibm_db.rollback(conn)
            ibm_db.close(conn)
            raise DBStmtException(ibm_db.stmt_errormsg())
        else:
            self.logger.info("Committing transactions")
            ibm_db.commit(conn)
        ibm_db.close(conn)

def validate_password(password):
    if len(password) < 8:
        return False
    return True

def create_oldap_pw(password, salt=None, default_hash=True):
    if salt is None:
        salt = os.urandom(20)
    if default_hash:
        digest = build_ssha(password, salt)[:20]
        return "{{SHA2}}{}".format(encodebytes(digest + salt).strip().decode("utf-8"))
    digest = build_ssha(password, salt, default_hash)
    return "{{SSHA}}{}".format(encodebytes(digest + salt).strip().decode("utf-8"))

def build_ssha(password, salt, default_hash=True):
    if default_hash:
        ssha = hashlib.sha256(password.encode())
    else:
        ssha = hashlib.sha1(password.encode())
    ssha.update(salt)
    return ssha.digest()

def extract_salt(ssha):
    encoded_ssha=ssha.encode()[6:]
    decoded_ssha=decodebytes(encoded_ssha)
    return decoded_ssha[20:]

def chunk_users(users, default_size=1000):
    it = iter(users)
    for i in range(0, len(users), default_size):
        yield {k:users[k] for k in islice(it, default_size)}

def insert_batch_users(conn, users):
    num_user_table_cols = 6
    user_count = len(users)
    placeholders = ",".join("({})".format(",".join("?" for _ in range(num_user_table_cols))) for _ in range(user_count))
    sql = "INSERT INTO DB2INST1.USER_TABLE (USERNAME,GROUP,EMAIL,LOCKED,IBMID,POLICYNAME) \
                VALUES {}".format(placeholders)
    stmt_idx = 1
    stmt = ibm_db.prepare(conn, sql)
    for user in users:
        print("Reconstructing user:{} group:{} email:{} locked:{} ibmid:{} policyname:{}".format(
                    users[user]['username'],
                    users[user]['group'],
                    users[user]['email'],
                    users[user]['locked'],
                    users[user]['ibmid'] if 'ibmid' in users[user] else "empty",
                    users[user]['policyname']))
        ibm_db.bind_param(stmt, stmt_idx, users[user]['username'])
        ibm_db.bind_param(stmt, stmt_idx+1, users[user]['group'])
        ibm_db.bind_param(stmt, stmt_idx+2, users[user]['email'])
        ibm_db.bind_param(stmt, stmt_idx+3, users[user]['locked'])
        ibm_db.bind_param(stmt, stmt_idx+4, users[user]['ibmid'] if 'ibmid' in users[user] else "")
        ibm_db.bind_param(stmt, stmt_idx+5, users[user]['policyname'])
        stmt_idx += num_user_table_cols
    ibm_db.execute(stmt)

class NoUserExistsException(Exception):
    def __init__(self):
        msg = 'Unable to locate user provided'
        super().__init__(msg)

class UserAlreadyExistsException(Exception):
    def __init__(self):
        msg = 'User already exists'
        super().__init__(msg)

class IAMUserAlreadyExistsException(Exception):
    def __init__(self):
        msg = 'IAM User already paired with a username'
        super().__init__(msg)

class UserFileUploadException(Exception):
    def __init__(self):
        msg = 'User file not found after upload'
        super().__init__(msg)

class ValidationError(Exception):
    def __init__(self):
        msg = 'Password did not meet validation requirements'
        super().__init__(msg)

class UserIneligibleException(Exception):
    def __init__(self):
        msg = 'User is not eligible to run this command'
        super().__init__(msg)

class PasswordInvalidException(Exception):
    def __init__(self):
        msg = 'Password provided does not match the current password'
        super().__init__(msg)

class UserFileNotInitializedException(Exception):
    def __init__(self):
        msg = 'User file was not initialized and there are no copies on COS'
        super().__init__(msg)

class IBMIDInvalidException(Exception):
    def __init__(self):
        msg = 'Format for IBM ID should be IBMId-* or iam-ServiceId-*'
        super().__init__(msg)

class InvalidUserGroupException(Exception):
    def __init__(self):
        msg = 'Invalid user group provided, valid user groups include bluadmin and bluusers'
        super().__init__(msg)

class NoPasswordAndHashException(Exception):
    def __init__(self):
        msg = 'Not an ibmid user, and no password or hash provided'
        super().__init__(msg)

class InvalidUserRoleException(Exception):
    def __init__(self):
        msg = 'Invalid user role provided, valid user roles include DV_ADMIN, DV_ENGINEER, DV_STEWARD, and DV_WORKER'
        super().__init__(msg)