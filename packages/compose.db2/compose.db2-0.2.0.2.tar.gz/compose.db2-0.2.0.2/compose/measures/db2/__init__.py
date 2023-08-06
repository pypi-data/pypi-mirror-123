from importlib import import_module
import os
import socket
import sys
import time
import datetime
from compose.db2.debroni import Debroni
from compose.db2.utils.sqlUtils import Db2Utils, Db2SQL, DBConnException
from compose.db2.utils.db2utils import DB2Commands
from compose.db2.utils.db2rc import SQLError, runCmdException, db2_cmd_execution
from compose.db2 import formation, configuration
import cdb.service
import base64
import json

# can use debroni_client for this or
from cdb.metrics import ERROR
import kubernetes

MLIB_MODULE = 'db2'


class Db2Node:
    def __init__(self):
        try:
            os.symlink("/mnt", "/data")
        except FileExistsError:
            pass
        self.api_client = kubernetes.client.ApiClient(configuration=kubernetes.config.load_incluster_config())
        self.fmtn_id = os.getenv("ID")
        self.account = os.getenv("ACCOUNT")
        self.role = os.getenv("ROLE")
        self.conf = {
            'peers': get_hostnames(self.api_client, self.fmtn_id, self.account, self.role),
            'fqdn': socket.getfqdn(),
            'debroni_port': '21815',
            'tls_crt_file': '/conf/cert/tls.crt',
            'tls_key_file': '/conf/cert/tls.key',
            'db2_sysadmin_user': 'db2inst1',
            'db2_ssl_svr_keydb': '/mnt/blumeta0/db2/keystore/keystore.p12',
            'db2_ssl_svr_stash': '/mnt/blumeta0/db2/keystore/keystore.sth',
            'compose_password': get_compose_password(self.api_client, self.fmtn_id, self.account, self.role),
            'crd_group': 'crd.compose.com',
            'account': self.account,
            'id': self.fmtn_id,
            'db_name': 'BLUDB',
            'db2_tcp_svcename': '50000',
            'db2_ssl_svcename': '55000',
            'repo_type': 's3',
            'configuration': configuration.Configuration()

        }
        self.fqdn = self.conf['fqdn']
        self.node_stats = {}
        self.sql = Db2SQL(self.conf)
        self.is_primary = self.is_current_primary()
        self.dbtype = "db2"
        
        # Basic function mappings initialization
        self.functions_mapping = {
                'one': {'frequency_min': 1, 'functions': [], 'last_update': datetime.datetime.now()},
                'thirty': {'frequency_min': 30, 'functions': ['get_iam_status'], 'last_update': datetime.datetime.now()},
                'sixty': {'frequency_min': 60, 'functions': [], 'last_update': datetime.datetime.now()}
            }

        # All db2 pods are 'm'(master) pods, which run all common metric functions. If self.role == 'm', then add all common 
        # metric function mappings 
        # Other pods (such as 'w'(worker) pods) use basic function mapping initialization for service specific metric functions to be added later. 
        # Service specific metric functions are to be defined in service specific metrics code. 
        if self.role == 'm':
            self.functions_mapping['one']['functions'].extend(['get_db_availability', 'get_db_connections', 'get_db_commits', 'get_db_stmts', 'get_db_activities',
                                                        'get_db_logs', 'get_ha_status', 'get_debroni_status', 'get_buildback_status', 'get_lite_capacity'])
            self.functions_mapping['thirty']['functions'].extend(['get_disk_usage_in_bytes'])
            self.functions_mapping['sixty']['functions'].extend(['get_backup_status', 'get_standby_replay_log_time', 'get_hadr_log_wait_time'])  

        for key in self.functions_mapping.keys():
            for f in self.functions_mapping[key]['functions']:
                getattr(self, f)()

    def failed_metrics_total(self):
        errors = 0
        for metric_key in self.node_stats.keys():
            if self.node_stats[metric_key] == -1:
                errors += 1
        self.node_stats['failed_metrics_total'] = errors

    def is_db_available(self):
        pass

    def is_current_primary(self):
        if self.role == 'm':
            try:
                debroni = Debroni(self.conf)
                return debroni.is_leader()
            except Exception as e:
                print('is_primary exception: ', e)
                return 0
        else:
            return 0

    def get_db_metrics(self, conn):
        pass

    def calculate_disk_free(self, st):
        pass

    def calculate_disk_total(self):
        pass

    def calculate_disk_used(self, st):
        pass

    def get_major_version(self):
        # should be able to get version of the db2 cli should keep up to date
        pass

    # Check availability of the db
    # SELECT DB_STATUS FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_availability(self):
        self.node_stats['db_availability_check'] = -1
        try:
            if self.is_primary:
                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['db_availability_check'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_availability,
                                                         fetch='assoc')
                if status is not None:
                    self.node_stats['db_availability_check'] = self.get_status_number(
                        status[0]['DB_STATUS'])
            else:
                self.node_stats['db_availability_check'] = 0
        except Exception as e:
            print(e)

    # Change the values of db availability to numbers
    def get_status_number(self, status):
        if status == 'ACTIVE':
            return 0
        elif status == 'QUIESCE_PEND':
            return 1
        elif status == 'QUIESCED':
            return 2
        elif status == 'ROLLFWD':
            return 3
        elif status == 'ACTIVE_STANDBY':
            return 4
        elif status == 'STANDBY':
            return 5
        else:
            return -1

    # Calculate the count of open, active and idle connections of the database
    # SELECT APPLS_CUR_CONS, APPLS_IN_DB2 FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_connections(self):
        self.node_stats['total_conn'] = -1
        self.node_stats['active_conn'] = -1
        self.node_stats['idle_conn'] = -1

        try:
            if self.is_primary:

                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['total_conn'] = 0
                    self.node_stats['active_conn'] = 0
                    self.node_stats['idle_conn'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_connections,
                                                         fetch='assoc')

                if status is not None:
                    self.node_stats['total_conn'] = status[0]['APPLS_CUR_CONS']
                    self.node_stats['active_conn'] = status[0]['APPLS_IN_DB2']
                    self.node_stats['idle_conn'] = status[0]['APPLS_CUR_CONS'] - \
                        status[0]['APPLS_IN_DB2']
            else:
                self.node_stats['total_conn'] = 0
                self.node_stats['active_conn'] = 0
                self.node_stats['idle_conn'] = 0
        except Exception as e:
            print(e)

    # Calculate number of commits, commit time in total and rollback count
    # SELECT TOTAL_APP_COMMITS, INT_COMMITS, TOTAL_COMMIT_TIME, TOTAL_APP_ROLLBACKS, INT_ROLLBACKS FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_commits(self):
        self.node_stats['db_num_commits'] = -1
        self.node_stats['db_commits_time'] = -1
        self.node_stats['db_rollbacks'] = -1

        try:
            if self.is_primary:

                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['db_num_commits'] = 0
                    self.node_stats['db_commits_time'] = 0
                    self.node_stats['db_rollbacks'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_commits,
                                                         fetch='assoc')

                if status is not None:
                    self.node_stats['db_num_commits'] = status[0]['TOTAL_APP_COMMITS'] + \
                        status[0]['INT_COMMITS']
                    self.node_stats['db_commits_time'] = status[0]['TOTAL_COMMIT_TIME']
                    self.node_stats['db_rollbacks'] = status[0]['TOTAL_APP_ROLLBACKS'] + \
                        status[0]['INT_ROLLBACKS']
            else:
                self.node_stats['db_num_commits'] = 0
                self.node_stats['db_commits_time'] = 0
                self.node_stats['db_rollbacks'] = 0
        except Exception as e:
            print(e)

    # Get the status of the backups (hours since last one, total count of completed and failed, last backup duration)
    def get_backup_status(self):
        self.node_stats['since_last_backup_hours'] = -1
        self.node_stats['last_backup_status'] = -1
        self.node_stats['backups_total'] = -1
        self.node_stats['backups_completed_total'] = -1
        self.node_stats['backups_failed_total'] = -1
        self.node_stats['last_backup_duration_minutes'] = -1
        completed = 0
        failed = 0
        try:
            backups = self.get_backups()
            keys = list(backups.keys())

            if len(keys) == 0:
                self.node_stats['backups_total'] = 0
                self.node_stats['backups_completed_total'] = 0
                self.node_stats['backups_failed_total'] = 0
                return

            last_bkp = keys[0]
            last_successful_bkp = keys[0]
            bkp_time = []
            last_successful_bkp_time = []
            for key in keys:
                bkp_time.append(backups[key]['timestamp'])
                if 'FAILED_BACKUP' not in key:
                    last_successful_bkp_time.append(backups[key]['timestamp'])
            for key in keys:
                if len(bkp_time) != 0:
                    if backups[key]['timestamp'] == sorted(bkp_time, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))[-1]:
                        last_bkp = key
                if len(last_successful_bkp) != 0:
                    if backups[key]['timestamp'] == sorted(last_successful_bkp_time, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))[-1]:
                        last_successful_bkp = key

                if 'FAILED_BACKUP' in key:
                    failed += 1
                else:
                    completed += 1

            if 'FAILED_BACKUP' in last_bkp:
                self.node_stats['last_backup_status'] = 1
            else:
                self.node_stats['last_backup_status'] = 0

            if last_successful_bkp != '0':
                diff = datetime.datetime.now(
                ) - datetime.datetime.strptime(backups[last_successful_bkp]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                days, seconds = diff.days, diff.seconds
                minutes = days * 1440 + seconds // 60 - backups[last_successful_bkp]['duration'] / 60
                self.node_stats['since_last_backup_hours'] = minutes / 60
                self.node_stats['last_backup_duration_minutes'] = (
                    backups[last_successful_bkp]['duration'] / 60)

            self.node_stats['backups_total'] = completed + failed
            self.node_stats['backups_completed_total'] = completed
            self.node_stats['backups_failed_total'] = failed

        except Exception as e:
            print('get_backup_status: ', e)

    def get_disk_usage_in_bytes(self):
        directories = {
            'disk_usage_databases': '/mnt/bludata0/db2/databases',
            'disk_usage_audit': '/mnt/blumeta0/db2/audit',
            'disk_usage_log': '/mnt/bludata0/db2/log',
            'disk_usage_remotestorage': '/mnt/bludata0/db2/RemoteStorage'
        }
        try:
            cmd = " ".join(["du -sb"] + list(directories.values()) + ["| cut -f1"])
            out = os.popen(cmd).readlines()
            for key, value in zip(directories.keys(), out):
                self.node_stat[key] = int(value)
        except Exception as e:
            print('get_disk_usage_in_bytes exception: ', e)

    def is_dr_node(self):
        fmtn = formation.Formation(self.conf['crd_group'],
                                   self.conf['account'],
                                   self.conf['id'])
        return fmtn.is_disaster_recovery_site() and fmtn.is_dr_configured()

    # Get the id's of the buildback recipes that were run or are running on this formation.
    # This excludes formations that are queued in "prepared" state and have not been started.
    def get_buildback_recipes(self):
        recipes = []
        kube_cli = client.CustomObjectsApi(self.kubeclient)
        # Get the list of buildback recipes run on this formation. Sort by age--oldest to newest
        recipes_json = kube_cli.list_namespaced_custom_object(
            self.conf['crd_group'],
            "v1",
            self.conf['account'],
            "recipes",
            pretty="true",
            label_selector="formation_id={},template=buildback".format(self.conf['id']))
        recipes_list = recipes_json.get('items', [])
        recipes_list = [
            recipe for recipe in recipes_list if recipe['status']['start_timestamp'] is not None]
        recipes_list = sorted(
            recipes_list, key=lambda recipe: recipe['status']['start_timestamp'])

        return recipes_list

    # Get the status of the last buildback recipe run.
    # Identify if the buildback is running or ended succesfully.
    def get_buildback_status(self):
        self.node_stats['buildback_running'] = -1
        self.node_stats['last_buildback_status'] = -1

        # Check the state of the most recent buildback on the DR node only
        try:
            if self.is_dr_node() or self.is_primary:
                recipes = self.get_buildback_recipes()
                if recipes:
                    # check if there is an active buildback
                    n = len(recipes)
                    last_bb = recipes[-1] if n > 0 else None
                    prev_bb = None

                    for i in range(n - 1, 0, -1):
                        if recipes[i]['status']['state'] == "running":
                            last_bb = recipes[i]
                            break
                    # found a bb actively running
                    if last_bb is not None:
                        if last_bb['status']['state'] == "running":  # bb running
                            self.node_stats['buildback_running'] = 1
                        else:  # no bb running
                            self.node_stats['buildback_running'] = 0

                    # get the last bb recipe that ran
                    if n > 1:      # if multiple bb's were run find the most recent
                        i = n - 2
                        prev_bb = recipes[i]
                        while recipes[i]['status']['state'] == "running" or \
                                recipes[i]['status']['state'] == "new":
                            prev_bb = recipes[i]
                            i -= 1
                    else:          # if only one bb was run
                        if last_bb['status']['state'] != "running":
                            prev_bb = last_bb

                    # check status of previous bb
                    if prev_bb is not None and prev_bb['status']['state'] == "completed":
                        self.node_stats['last_buildback_status'] = 0
                    else:
                        self.node_stats['last_buildback_status'] = 1

        except Exception as e:
            print('get_buildback_status: ', e)

    # Calculate number of rows deleted, inserted, update, select and uid (update, insert, delete) statements
    # SELECT ROWS_DELETED, INT_ROWS_DELETED, ROWS_INSERTED, INT_ROWS_INSERTED, ROWS_UPDATED, INT_ROWS_UPDATED, SELECT_SQL_STMTS, UID_SQL_STMTS
    # FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_stmts(self):
        self.node_stats['rows_deleted'] = -1
        self.node_stats['rows_inserted'] = -1
        self.node_stats['rows_updated'] = -1
        self.node_stats['select_stmts'] = -1
        self.node_stats['uid_stmts'] = -1

        try:
            if self.is_primary:

                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['rows_deleted'] = 0
                    self.node_stats['rows_inserted'] = 0
                    self.node_stats['rows_updated'] = 0
                    self.node_stats['select_stmts'] = 0
                    self.node_stats['uid_stmts'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_stmts,
                                                         fetch='assoc')

                if status is not None:
                    self.node_stats['rows_deleted'] = status[0]['ROWS_DELETED'] + \
                        status[0]['INT_ROWS_DELETED']
                    self.node_stats['rows_inserted'] = status[0]['ROWS_INSERTED'] + \
                        status[0]['INT_ROWS_INSERTED']
                    self.node_stats['rows_updated'] = status[0]['ROWS_UPDATED'] + \
                        status[0]['INT_ROWS_UPDATED']
                    self.node_stats['select_stmts'] = status[0]['SELECT_SQL_STMTS']
                    self.node_stats['uid_stmts'] = status[0]['UID_SQL_STMTS']
            else:
                self.node_stats['rows_deleted'] = 0
                self.node_stats['rows_inserted'] = 0
                self.node_stats['rows_updated'] = 0
                self.node_stats['select_stmts'] = 0
                self.node_stats['uid_stmts'] = 0
        except Exception as e:
            print('get_db_stmts: ', e)

    # Calculate number of activities completed, aborted and rejected
    # SELECT ACT_COMPLETED_TOTAL, ACT_ABORTED_TOTAL, ACT_REJECTED_TOTAL FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_activities(self):
        self.node_stats['db_act_completed'] = -1
        self.node_stats['db_act_aborted'] = -1
        self.node_stats['db_act_rejected'] = -1

        try:
            if self.is_primary:

                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['db_act_completed'] = 0
                    self.node_stats['db_act_aborted'] = 0
                    self.node_stats['db_act_rejected'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_activities,
                                                         fetch='assoc')

                if status is not None:
                    self.node_stats['db_act_completed'] = status[0]['ACT_COMPLETED_TOTAL']
                    self.node_stats['db_act_aborted'] = status[0]['ACT_ABORTED_TOTAL']
                    self.node_stats['db_act_rejected'] = status[0]['ACT_REJECTED_TOTAL']
            else:
                self.node_stats['db_act_completed'] = 0
                self.node_stats['db_act_aborted'] = 0
                self.node_stats['db_act_rejected'] = 0
        except Exception as e:
            print('get_db_activities: ', e)

    # Calculate how long was the disk wait because of a log being saved
    # SELECT LOG_DISK_WAITS_TOTAL FROM TABLE(MON_GET_DATABASE(NULL))
    def get_db_logs(self):
        self.node_stats['log_disk_wait'] = -1

        try:
            if self.is_primary:

                if (cdb.service.stat('db2') != "run"):
                    self.node_stats['log_disk_wait'] = 0
                    return
                status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                         query=self.sql.db_logs,
                                                         fetch='assoc')

                if status is not None:
                    self.node_stats['log_disk_wait'] = status[0]['LOG_DISK_WAITS_TOTAL']
            else:
                self.node_stats['log_disk_wait'] = 0
        except Exception as e:
            print('get_db_logs: ', e)

    # Calculate IAM status
    def get_iam_status(self):
        fail_count = 0
        self.node_stats['iam_status'] = -1

        while fail_count < 5:
            cmd = 'curl --write-out %{http_code} --silent --output /dev/null https://iam.cloud.ibm.com/healthz'
            try:
                response = int(os.popen(cmd).read())
                if response != 200:
                    fail_count = fail_count + 1
                else:
                    break
            except:
                fail_count = fail_count + 1

        if fail_count < 5:
            self.node_stats['iam_status'] = 0
        else:
            self.node_stats['iam_status'] = 1

    def get_hadr_state(self, status):
        if status == "REMOTE_CATCHUP":
            return 0
        elif status == "PEER":
            return 1
        elif status is None:
            return -1
        else:
            return 2

    # Calculate if is leader, if hadr is connected, time since last recovery, hard log gap, number of hearbeat missed and expected, hadr state
    # SELECT HADR_ROLE, STANDBY_ID, HADR_CONNECT_STATUS, HADR_STATE, PRIMARY_MEMBER_HOST, STANDBY_MEMBER_HOST from table(MON_GET_HADR(NULL))
    def get_ha_status(self):
        self.node_stats['is_leader'] = -1
        self.node_stats['is_hadr_connected'] = -1
        self.node_stats['time_since_last_recv'] = -1
        self.node_stats['hadr_log_gap'] = -1
        self.node_stats['heartbeat_missed'] = -1
        self.node_stats['heartbeat_expected'] = -1
        self.node_stats['hadr_state'] = -1
        self.node_stats['is_dr_connected'] = -1
        self.node_stats['time_since_last_dr_recv'] = -1
        self.node_stats['dr_log_gap'] = -1
        self.node_stats['dr_heartbeat_missed'] = -1
        self.node_stats['dr_heartbeat_expected'] = -1
        self.node_stats['dr_state'] = -1
        try:
            if (cdb.service.stat('db2') != "run") or (self.dbtype == "dv" and not self.is_primary):
                self.node_stats['is_leader'] = 0
                self.node_stats['is_hadr_connected'] = 0
                self.node_stats['time_since_last_recv'] = 0
                self.node_stats['hadr_log_gap'] = 0
                self.node_stats['heartbeat_missed'] = 0
                self.node_stats['heartbeat_expected'] = 0
                self.node_stats['hadr_state'] = 0
                self.node_stats['is_dr_connected'] = 0
                self.node_stats['time_since_last_dr_recv'] = 0
                self.node_stats['dr_log_gap'] = 0
                self.node_stats['dr_heartbeat_missed'] = 0
                self.node_stats['dr_heartbeat_expected'] = 0
                self.node_stats['dr_state'] = 0
                return
            status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                     query=self.sql.ha_status,
                                                     fetch='assoc', conntimeout=5)
            if status is not None and len(status) > 0:
                hadr_role = status[0].get('HADR_ROLE', '')
                if hadr_role == "PRIMARY":
                    self.node_stats['is_leader'] = 1
                else:
                    self.node_stats['is_leader'] = 0

                for s in status:
                    if s.get('STANDBY_MEMBER_HOST', '') == None and 'private' in s.get('PRIMARY_MEMBER_HOST', ''):
                        dr_connect_status = s.get('HADR_CONNECT_STATUS', '')
                        if dr_connect_status == "CONNECTED":
                            self.node_stats['is_dr_connected'] = 0
                        else:
                            self.node_stats['is_dr_connected'] = 1

                        hadr_state = s.get('HADR_STATE', '')
                        state = self.get_hadr_state(hadr_state)
                        self.node_stats['dr_state'] = state
                        self.node_stats['time_since_last_dr_recv'] = int(
                            s.get('TIME_SINCE_LAST_RECV', -1))
                        self.node_stats['dr_log_gap'] = int(
                            s.get('HADR_LOG_GAP', -1))
                        self.node_stats['dr_heartbeat_missed'] = int(
                            s.get('HEARTBEAT_MISSED', -1))
                        self.node_stats['dr_heartbeat_expected'] = int(
                            s.get('HEARTBEAT_EXPECTED', -1))
                    else:
                        hadr_connect_status = s.get('HADR_CONNECT_STATUS', '')
                        if hadr_connect_status == "CONNECTED" and self.node_stats['is_hadr_connected'] != 1:
                            self.node_stats['is_hadr_connected'] = 0
                        else:
                            self.node_stats['is_hadr_connected'] = 1

                        if int(s.get('HADR_LOG_GAP', -1)) >= self.node_stats['hadr_log_gap']:
                            hadr_state = s.get('HADR_STATE', '')
                            state = self.get_hadr_state(hadr_state)
                            self.node_stats['hadr_state'] = state
                            self.node_stats['time_since_last_recv'] = int(
                                s.get('TIME_SINCE_LAST_RECV', -1))
                            self.node_stats['hadr_log_gap'] = int(
                                s.get('HADR_LOG_GAP', -1))
                            self.node_stats['heartbeat_missed'] = int(
                                s.get('HEARTBEAT_MISSED', -1))
                            self.node_stats['heartbeat_expected'] = int(
                                s.get('HEARTBEAT_EXPECTED', -1))
        except DBConnException as e:
            if 'SQL30082N' in e.message:
                print("Refreshing compose credentails")
                self.refresh_credentials()
        except Exception as e:
            print('get_ha_status: ', e)

    def get_standby_replay_log_time(self):
        self.node_stats['standby_replay_log_time'] = -1
        self.node_stats['dr_replay_log_time'] = -1
        try:
            status = self.sql.run_desired_select_sql(ip=self.fqdn,
                                                     query=self.sql.ha_status,
                                                     fetch='assoc')
            if status is not None:
                for s in status:
                    if s.get('STANDBY_MEMBER_HOST', '') == None and 'private' in s.get('PRIMARY_MEMBER_HOST', ''):
                        standby_replay_log_time = s.get(
                            'STANDBY_REPLAY_LOG_TIME', -1)
                        primary_log_time = s.get('PRIMARY_LOG_TIME', -1)
                        time_diff = (primary_log_time -
                                     standby_replay_log_time).total_seconds()
                        if time_diff > 0:
                            time_diff_min = time_diff / 60
                        else:
                            time_diff_min = time_diff
                        self.node_stats['dr_replay_log_time'] = time_diff_min
                    else:
                        standby_replay_log_time = s.get(
                            'STANDBY_REPLAY_LOG_TIME', -1)
                        primary_log_time = s.get('PRIMARY_LOG_TIME', -1)
                        time_diff = (primary_log_time -
                                     standby_replay_log_time).total_seconds()
                        if time_diff > 0:
                            time_diff_min = time_diff / 60
                        else:
                            time_diff_min = time_diff
                        if (time_diff_min >= self.node_stats['standby_replay_log_time']):
                            self.node_stats['standby_replay_log_time'] = time_diff_min
        except DBConnException as e:
            if 'SQL30082N' in e.message:
                print("Refreshing compose credentails")
                self.refresh_credentials()
        except Exception as e:
            print(e)


# Reconfigured get_debroni_status to better align with actual levels of status vs 0/1

#   Debroni         Sysdig
#   No response     3 - Black
#   UNSPECIFIED(0)  2 - Red
#   INIT(1)         2 - Red
#   COMPLETED(2)    0 - Green
#   MAINTENANCE(3)  1 - Yellow
#   REBUILD(4)      2 - Red

    def get_debroni_status(self):

        debroni = Debroni(self.conf)
        self.node_stats['debroni_status'] = 3

        try:
            status = debroni.get_member_debroni_info()

            if status is None:
                self.node_stats['debroni_status'] = 3

            elif status.init_state == 0:
                self.node_stats['debroni_status'] = 2

            elif status.init_state == 1:
                self.node_stats['debroni_status'] = 2

            elif status.init_state == 2:
                self.node_stats['debroni_status'] = 0

            elif status.init_state == 3:
                self.node_stats['debroni_status'] = 1

            elif status.init_state == 4:
                self.node_stats['debroni_status'] = 2
            else:
                self.node_stats['debroni_status'] = 0

        except Exception as e:
            print('get_debroni_status: ', e)

    # def get_debroni_state(self):
    #     self.node_stats['debroni_state'] = -1
    #     try:
    #         v1 = client.CoreV1Api(self.kubeclient)
    #         configmap_name = os.getenv("POD_NAME") + "-debroni"
    #         namespace = os.getenv("ACCOUNT")
    #         map = v1.read_namespaced_config_map(configmap_name, namespace)
    #         date = map.data.get('alert_timestamp')
    #         if date is None:
    #             self.node_stats['debroni_state'] = 1
    #         else:
    #             timestamp = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f %Z")
    #             time_now = datetime.datetime.now()
    #             time_diff = abs(time_now - timestamp)
    #             if time_diff <= datetime.timedelta(minutes=1):
    #                 self.node_stats['debroni_state'] = 1
    #             else:
    #                 self.node_stats['debroni_state'] = 0
    #     except Exception as e:
    #         print(e)

    def _measurement(self, name, value):
        return {
            'name': name,
            'value': value,
            'timestamp': time.time(),
            'module': MLIB_MODULE
        }

    def node_stat(self, path, rename=None, as_value=False):
        try:
            val = self.node_stats[path]
        except Exception:
            val = ERROR

        if as_value:
            return val

        if rename:
            path = rename

        return self._measurement(path, val)

    def get_backups(self):
        available_backup_resources_dic = {}

        # get the list of backup resources created for current formation
        available_backup_resources_json = kubernetes.client.CustomObjectsApi(self.api_client).list_namespaced_custom_object(
            self.conf['crd_group'],
            "v1",
            self.conf['account'],
            "backups",
            pretty="true",
            label_selector="formation_id={}".format(self.conf['id']))

        failed_backups = 0
        available_backup_list = available_backup_resources_json.get(
            'items', [])
        for resource in available_backup_list:
            if resource['status'] in ('failed', 'completed'):
                # The backup resources status could be in failed status either
                # due to a recipe execution failure or because pgbackrest
                # failed to take a backup correctly. In this case we will end
                # up with a failed backup resource without a restore label
                # referencing a valid backup in COS
                try:
                    if resource['status'] == 'completed':
                        backup_label = str(int(json.loads(resource["spec"]["restore_data"])[
                            'restore_time']) + json.loads(resource["spec"]["restore_data"])['duration_time'])
                    else:
                        backup_label = "FAILED_BACKUP" + str(failed_backups)
                        failed_backups += 1
                except Exception:
                    backup_label = "FAILED_BACKUP" + str(failed_backups)
                    failed_backups += 1
                if resource["spec"]["restore_data"] == '':
                    backup_resource_name = {
                        "id": resource["metadata"]["name"], "timestamp": resource["metadata"]["creationTimestamp"], "duration": 0}
                else:
                    backup_resource_name = {
                        "id": resource["metadata"]["name"], "timestamp": resource["metadata"]["creationTimestamp"], "duration": json.loads(resource["spec"]["restore_data"])['duration_time']}
                available_backup_resources_dic[
                    backup_label] = backup_resource_name

        return available_backup_resources_dic

    def get_lite_capacity(self):
        self.node_stats['lite_capacity'] = -1
	    # get details of current formation
        formation_detail_json = kubernetes.client.CustomObjectsApi(self.api_client).get_namespaced_custom_object(
        self.conf['crd_group'],
        "v1",
        self.conf['account'],
        "formations",
        "{}".format(self.conf['id']))
        try:
            if formation_detail_json['spec']['resource_configs']['m']['env'].get('capacity') != None:
                capacity = formation_detail_json['spec']['resource_configs']['m']['env']['capacity']
                self.node_stats['lite_capacity'] = int(capacity)
        except Exception as e:
            print('get_lite_capacity: ', e)	
	
    def get_hadr_log_wait_time(self):
        self.node_stats['hadr_log_wait_time'] = -1
        try:
            cmds = DB2Commands(self.conf['configuration'])
            if os.path.isfile(os.path.join('/tmp/compose/db2/resources/db2mon.db.logst.sql')):
                cmd = "runuser -l {0} -c \"{1}; db2 -tvf {2}\"".format(cmds.dbuser, cmds.connect_db_remote(),
                                                                                   os.path.join('/tmp/compose/db2/resources/db2mon.db.logst.sql'))
                out = db2_cmd_execution(cmd, retries=0, return_msg=True)
                lines = out.splitlines()
                print (lines)
                if len(lines) > 8:
                    line = lines[-8]
                    items = line.split()
                    if len(items) == 5:
                        hadr_log_wait_time = items[4]
                        if hadr_log_wait_time == '-':
                            self.node_stats['hadr_log_wait_time'] = 0
                        else:
                            self.node_stats['hadr_log_wait_time'] = hadr_log_wait_time
        except Exception as e:
            print('get_hadr_log_wait_time: ', e)


    # update credentials in case of rotation action
    def refresh_credentials(self):
        self.conf['compose_password'] = get_compose_password(
            self.kubeclient, self.fmtn_id, self.account, self.role)
        self.sql = Db2SQL(self.conf)


def get_compose_password(api_client, id, account, role):
    name = "c-{}-{}".format(id, role)
    secret = kubernetes.client.CoreV1Api(api_client).read_namespaced_secret(name, account)
    return base64.b64decode(secret.data.get('compose_password')).decode('utf-8')


def get_hostnames(api_client, id, account, role):
    """Lists all A record hostnames associated with the target statefulset and role."""

    name = "c-{}-{}".format(id, role)
    statefulset = kubernetes.client.AppsV1Api(api_client).read_namespaced_stateful_set(name, account)
    replicas = int(statefulset.status.replicas)
    peers = []
    for replica in range(replicas):
        peer = "{name}-{replica}.{name}.{account}.svc.cluster.local".format(
            name=name,
            replica=replica,
            account=account
        )
        peers.append(peer)

    return peers


_collector = Db2Node()

# with mlib>=0.2.0 we need to explicitly import all sub-modules to collect their metrics
import_module('compose.measures.db2.activity')
import_module('compose.measures.db2.replication')

# This function is called every 60 seconds


def refresh():
    _collector.is_primary = _collector.is_current_primary()
    time_now = datetime.datetime.now()

    # Check how long has been since last update, compare with frequency of the metric and call the functions
    for key in _collector.functions_mapping.keys():
        diff = time_now - _collector.functions_mapping[key]['last_update']
        minutes = (diff.days * 24 * 60) + (diff.seconds / 60)
        if minutes >= _collector.functions_mapping[key]['frequency_min']:
            for f in _collector.functions_mapping[key]['functions']:
                getattr(_collector, f)()
            _collector.functions_mapping[key]['last_update'] = datetime.datetime.now(
            )

    _collector.failed_metrics_total()
