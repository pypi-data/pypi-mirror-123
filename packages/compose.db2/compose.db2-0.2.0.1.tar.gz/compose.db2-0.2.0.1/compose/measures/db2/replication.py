from cdb.metrics import measures
from compose.measures.db2 import _collector

@measures.measure('is_ha_replica_alive', defaultValue=0)
def is_ha_replica_alive():
    return _collector.node_stat('is_ha_replica_alive')

@measures.measure('is_read_only_replica_alive', defaultValue="")
def is_read_only_replica_alive():
    return _collector.node_stat('is_read_only_replica_alive')

@measures.measure('failed_archive_count')
def failed_archive_count():
    return _collector.node_stat('failed_archive_count')

@measures.measure('successful_archive_count')
def successful_archive_count():
    return _collector.node_stat('successful_archive_count')

# Metrics currently not being collected. If they start to be, comment out the specific metric and use the same name during the collection

# @measures.measure('replication_lag_seconds')
# def replication_lag_seconds():
#     return _collector.node_stat('replication_lag_seconds')

# @measures.measure('last_commit_time')
# def last_commit_time():
#     return _collector.node_stat('last_commit_time')

# @measures.measure('replication_lag_bytes', specialHandle=True)
# def replication_lag_bytes():
#     return _collector.node_stat('replication_lag_bytes')
