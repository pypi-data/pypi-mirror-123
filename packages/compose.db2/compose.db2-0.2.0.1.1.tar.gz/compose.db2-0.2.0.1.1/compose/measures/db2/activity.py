from cdb.metrics import measures
from compose.measures.db2 import _collector
import os

@measures.measure('failed_metrics_total')
def failed_metrics_total():
    return _collector.node_stat('failed_metrics_total')

@measures.measure('active_conn')
def active_conn_count():
    return _collector.node_stat('active_conn')

@measures.measure('idle_conn')
def idle_conns_count():
    return _collector.node_stat('idle_conn')

@measures.measure('db_availability_check')
def db_availabilty_check():
    return _collector.node_stat('db_availability_check')

@measures.measure('is_leader', defaultValue=0)
def is_leader_check():
    return _collector.node_stat('is_leader')

@measures.measure('is_standby_leader', defaultValue="")
def is_standby_leader_check():
    return _collector.node_stat('is_standby_leader')

@measures.measure('total_conn')
def total_conn_count():
    return _collector.node_stat('total_conn')

@measures.measure('iam_status', defaultValue=1)
def iam_status():
    return _collector.node_stat('iam_status')

@measures.measure('db_num_commits')
def db_num_commits():
    return _collector.node_stat('db_num_commits')

@measures.measure('db_commits_time')
def db_commits_time():
    return _collector.node_stat('db_commits_time')

@measures.measure('db_rollbacks')
def db_rollbacks():
    return _collector.node_stat('db_rollbacks')

@measures.measure('last_backup_status')
def last_backup_status():
    return _collector.node_stat('last_backup_status')

@measures.measure('since_last_backup_hours')
def since_last_backup_hours():
    return _collector.node_stat('since_last_backup_hours')

@measures.measure('last_backup_duration_minutes')
def last_backup_duration_minutes():
    return _collector.node_stat('last_backup_duration_minutes')

@measures.measure('backups_total')
def backups_total():
    return _collector.node_stat('backups_total')

@measures.measure('backups_completed_total')
def backups_completed_total():
    return _collector.node_stat('backups_completed_total')

@measures.measure('backups_failed_total')
def backups_failed_total():
    return _collector.node_stat('backups_failed_total')

@measures.measure('rows_deleted')
def rows_deleted():
    return _collector.node_stat('rows_deleted')

@measures.measure('rows_inserted')
def rows_inserted():
    return _collector.node_stat('rows_inserted')

@measures.measure('rows_updated')
def rows_updated():
    return _collector.node_stat('rows_updated')

@measures.measure('select_stmts')
def select_stmts():
    return _collector.node_stat('select_stmts')

@measures.measure('uid_stmts')
def uid_stmts():
    return _collector.node_stat('uid_stmts')

@measures.measure('db_act_completed')
def db_act_completed():
    return _collector.node_stat('db_act_completed')

@measures.measure('db_act_aborted')
def db_act_aborted():
    return _collector.node_stat('db_act_aborted')

@measures.measure('db_act_rejected')
def db_act_rejected():
    return _collector.node_stat('db_act_rejected')

@measures.measure('log_disk_wait')
def log_disk_wait():
    return _collector.node_stat('log_disk_wait')

@measures.measure('is_hadr_connected', defaultValue=1)
def is_hadr_connected():
    return _collector.node_stat('is_hadr_connected')

@measures.measure('time_since_last_recv', defaultValue=0)
def time_since_last_recv():
    return _collector.node_stat('time_since_last_recv')

@measures.measure('hadr_log_gap', defaultValue=0)
def hadr_log_gap():
    return _collector.node_stat('hadr_log_gap')

@measures.measure('standby_replay_log_time', defaultValue=0)
def standby_replay_log_time():
    return _collector.node_stat('standby_replay_log_time')

@measures.measure('heartbeat_missed', defaultValue=0)
def hadr_heartbeat_missed():
    return _collector.node_stat('heartbeat_missed')

@measures.measure('heartbeat_expected', defaultValue=0)
def hadr_heartbeat_expected():
    return _collector.node_stat('heartbeat_expected')

@measures.measure('is_dr_connected', defaultValue=1)
def is_dr_connected():
    return _collector.node_stat('is_dr_connected')

@measures.measure('time_since_last_dr_recv', defaultValue=0)
def time_since_last_dr_recv():
    return _collector.node_stat('time_since_last_dr_recv')

@measures.measure('dr_log_gap', defaultValue=0)
def dr_log_gap():
    return _collector.node_stat('dr_log_gap')

@measures.measure('dr_replay_log_time', defaultValue=0)
def dr_replay_log_time():
    return _collector.node_stat('dr_replay_log_time')

@measures.measure('dr_heartbeat_missed', defaultValue=0)
def dr_heartbeat_missed():
    return _collector.node_stat('dr_heartbeat_missed')

@measures.measure('dr_heartbeat_expected', defaultValue=0)
def dr_heartbeat_expected():
    return _collector.node_stat('dr_heartbeat_expected')

@measures.measure('debroni_status')
def debroni_status():
    return _collector.node_stat('debroni_status')

# @measures.measure('debroni_state')
# def debroni_state():
#     return _collector.node_stat('debroni_state')

@measures.measure('hadr_state', defaultValue=-1)
def hadr_state():
    return _collector.node_stat('hadr_state')

@measures.measure('buildback_running', defaultValue=-1)
def buildback_running():
    return _collector.node_stat('buildback_running')

@measures.measure('last_buildback_status', defaultValue=-1)
def buildback_running():
    return _collector.node_stat('last_buildback_status')

@measures.measure('disk_usage_databases', defaultValue=-1)
def disk_usage_databases():
    return _collector.node_stat('disk_usage_databases')

@measures.measure('disk_usage_audit', defaultValue=-1)
def disk_usage_audit():
    return _collector.node_stat('disk_usage_audit')

@measures.measure('disk_usage_log', defaultValue=-1)
def disk_usage_log():
    return _collector.node_stat('disk_usage_log')

@measures.measure('disk_usage_remotestorage', defaultValue=-1)
def disk_usage_remotestorage():
    return _collector.node_stat('disk_usage_remotestorage')

if os.getenv('PLAN_ID') == "dashDBLiteFormation":
    @measures.measure('lite_capacity', defaultValue=-1)
    def lite_capacity():
        return _collector.node_stat('lite_capacity')

@measures.measure('hadr_log_wait_time', defaultValue=-1)
def hadr_log_wait_time():
    return _collector.node_stat('hadr_log_wait_time')

# Metrics currently not being collected. If they start to be, comment out the specific metric and use the same name during the collection

# @measures.measure('idle_in_transaction_conn')
# def idle_in_transaction_conn_count():
#     return _collector.node_stat('idle_in_transaction_conn')

# @measures.measure('fastpath_function_call_conn')
# def fastpath_function_call_conn_count():
#     return _collector.node_stat('fastpath_function_call_conn')

# @measures.measure('disabled_conn')
# def disabled_conn_count():
#     return _collector.node_stat('disabled_conn')

# @measures.measure('oldest_idle_xact_seconds')
# def oldest_idle_xact_seconds():
#     return _collector.node_stat('oldest_idle_xact_seconds')
