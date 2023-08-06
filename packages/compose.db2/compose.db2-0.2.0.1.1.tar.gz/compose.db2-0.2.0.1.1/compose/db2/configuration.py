import os
import socket

import cdb.configuration

from cdb.properties import (
    ChoiceProperty,
    IntegerProperty,
    StringProperty,
    CertificateProperty,
    BooleanProperty,
    PropertyList
)


class Configuration(cdb.configuration.Configuration):

    servicename = StringProperty(
        "The name of this instance"
    )

    version = StringProperty(
        "The version of db2"
    )

    account = StringProperty(
        "The account that owns this instance",
        default=os.environ.get('NAME')
    )

    id = StringProperty(
        "The ID of this formation",
        default=os.environ.get('ID')
    )

    role = StringProperty(
        "role of the pod",
        default=os.environ.get("ROLE")
    )

    maxmemory = IntegerProperty(
        "The maximum memory usage, in bytes.",
        default=1073741824
    )

    db2_instance_name = StringProperty(
        "Instance name of db2",
        default="db2inst1"
    )

    db2_major_version = StringProperty(
        "Major Db2 Version",
        default=lambda c: ".".join(c['version'].split('.')[:2])
    )

    db2_sysadmin_user = StringProperty(
        "sysadm user",
        default="db2inst1"
    )

    compose_password = StringProperty(
        "Password for ibm DB super user",
        customer_configurable=False,
    )

    conf_dir = StringProperty(
        "The directory that hosts the configuration files.",
        default='/conf/db2oc/'
    )

    db2_data_dir = StringProperty(
        "Db2 Data Dir",
        default='/mnt/bludata0/db2/databases'
    )

    listen_address = StringProperty(
        "Addresses for Db2 to listen on",
        default=lambda c: socket.gethostbyname(c['hostname']),
        default_description="Addresses for db2 to listen on."
    )

    repo_type = ChoiceProperty(
        "Type of storage used for the backup repository. Supported values: posix, s3",
        choices=["s3", "posix"],
        default="s3"
    )

    repo_path = StringProperty(
        "Path where backups and archive are stored",
        default="/backup"
    )

    db_name = StringProperty(
        "db name ",
        default="bludb"
    )

    db2_hadr_port = IntegerProperty(
        "hadr port for db2",
        default=51987
    )

    hostname = StringProperty(
        "The hostname of the container."
    )

    fqdn = StringProperty(
        "The fqdn of the db pod",
        default=lambda c: socket.getfqdn(socket.gethostbyname(c['hostname']))
    )

    cos_endpoint = StringProperty(
        "URL for backup provider",
        default="s3-api.us-geo.objectstorage.service.networklayer.com"
    )

    cos_region = StringProperty(
        "Region for backup",
        default="us-standard"
    )

    cos_access_key = StringProperty(
        "Key for backup storage",
        default="cos_access_key_unconfigured"
    )

    cos_bucket = StringProperty(
        "s3 Bucket",
        default="ibm-backups-dev-b"
    )

    cos_secret_access_key = StringProperty(
        "Key for backup storage",
        default="cos_secret_access_key_unconfigured"
    )

    tls_crt = CertificateProperty(
        "tls_crt setup created during formation",
        default="tls_crt_not_setup"
    )

    tls_key = CertificateProperty(
        "tls_key for the tls_crt",
        default="tls_key_not_setup"
    )

    tls_crt_file = StringProperty(
        "tls_crt_file is the location of the tls certificate",
        default="/conf/cert/tls.crt"
    )

    tls_key_file = StringProperty(
        "tls_key_file is the location of the tls key",
        default="/conf/cert/tls.key"
    )

    full_backups_to_retain = IntegerProperty(
        "How many full backups to retain.  Set arbitrarily high to disable auto-backup expiry",
        default=14
    )

    backup_transaction_log_retention_period = IntegerProperty(
        "Number of days to keep transaction log files for.",
        default=14,
        customer_configurable=False
    )

    num_backups_valid_for_pitr = IntegerProperty(
        "Number of backups (diff or full) valid for PITR.",
        default=14,
        customer_configurable=False
    )

    debroni_conf = StringProperty(
        "The full path of the debroni.json file",
        default=lambda c: '{}/debroni.json'.format(c['conf_dir']),
        default_description="Path to deroni.json."
    )

    debroni_port = IntegerProperty(
        "Debroni API port.",
        customer_configurable=False,
        default=21815
    )

    db2_hadr_port = IntegerProperty(
        "HADR Port",
        customer_configurable=False,
        default=51987
    )

    listen_address = StringProperty(
        "Addresses for Debroni to listen on",
        default=lambda c: socket.gethostbyname(c['hostname']),
        default_description="Addresses for Debroni to listen on."
    )

    db2_diag_path = StringProperty(
        "diag logs locations",
        customer_configurable=False,
        default="/mnt/bludata0/db2/log/"
    )

    db2_diag_size = IntegerProperty(
        "diag size",
        customer_configurable=False,
        default=1000
    )

    db2_s3_staging_path = StringProperty(
        "staging path for COS",
        customer_configurable=False,
        default="/mnt/blutmp0/db2/RemoteStorage"
    )

    db2_s3_loadalias_name = StringProperty(
        "load alias for s3",
        default="db2-s3-load"
    )

    db2_sysadm_group = StringProperty(
        "db2 sysadm group",
        customer_configurable=False,
        default="db2iadm1"
    )

    db2_sysctrl_group = StringProperty(
        "sysctrl group",
        customer_configurable=False,
        # default="db2iadm1"
        default="bluadmin"
    )

    db2_sysmaint_group = StringProperty(
        "sysmaint group",
        customer_configurable=False,
        default="db2iadm1"
    )

    db2_sysmon_group = StringProperty(
        "sysmon group",
        customer_configurable=False,
        default="db2iadm1"
    )

    db2_ssl_svr_keydb = StringProperty(
        "keydb location",
        customer_configurable=False,
        default="/mnt/blumeta0/db2/keystore/keystore.p12"
    )

    db2_ssl_svr_stash = StringProperty(
        "key stash location",
        customer_configurable=False,
        default="/mnt/blumeta0/db2/keystore/keystore.sth"
    )

    db2_ssl_svr_label = StringProperty(
        "ssl lable location",
        customer_configurable=False,
        # default="CA-signed"
        default="db2oc-signed"
    )

    db2_optprofile = StringProperty(
        "Optimizer guideline XML",
        customer_configurable=True,
        default="YES"
    )

    db2_reduced_optimization = StringProperty(
        "Control over optimization search space",
        customer_configurable=True,
        default="JULIE"
    )

    db2_evaluncommited = StringProperty(
        "Predicate evaluation on uncommited data",
        customer_configurable=True,
        default="ON"
    )

    db2_extended_optimization = StringProperty(
        "Parallel access plan",
        customer_configurable=True,
        default="NO_HVCHECK_ALL"
    )

    db2_skipdeleted = StringProperty(
        "Uncommited deleted rows skipped during table scans",
        customer_configurable=True,
        default="ON"
    )

    db2_parallel_io = StringProperty(
        "Registry variable set correctly for more disk per container",
        customer_configurable=True,
        default="*"
    )

    db2_compopt = StringProperty(
        "Recent addition for performance",
        customer_configurable=True,
        default="NO_SCALAR203_ROW"
    )

    disaster_recovery_host = StringProperty(
        "Disaster Recovery Hostname",
        default=""
    )

    extended_peers = PropertyList(
        StringProperty,
        "Extended peer list to include DR",
        default=lambda c: get_extended_peers(
            c['peers'], c['disaster_recovery_host'])
    )

    db2_setup_type = StringProperty(
        "check if its single or multi pod",
        default=lambda c: setup_type(c['extended_peers'])
    )

    dft_db_path = StringProperty(
        "default db path where db exists",
        default="/mnt/bludata0/db2/databases"
    )

    db2_ssl_svcename = StringProperty(
        "ssl port name for service",
        default=lambda c: get_ssl_port()
    )

    db2_tcp_svcename = StringProperty(
        "non ssl port for db2",
        default="50000"
    )

    db2_keystore_loc = StringProperty(
        "keystore location for the service",
        default="/mnt/blumeta0/db2/keystore/keystore.p12"
    )

    db2_keystore_sth = StringProperty(
        "keystore location for the service",
        default="/mnt/blumeta0/db2/keystore/keystore.sth"
    )

    db2_ks_path = StringProperty(
        "keystore path for db2",
        default=lambda c: get_ks_path(c['db2_keystore_loc'])
    )

    mgmt_keystore_loc = StringProperty(
        "keystore location for mgmt ssl",
        default="/mnt/blumeta0/db2/mgmt_keystore/keystore.p12"
    )

    mgmt_keystore_sth = StringProperty(
        "keystore location for mgmt ssl",
        default="/mnt/blumeta0/db2/mgmt_keystore/keystore.sth"
    )

    mgmt_keystore_path = StringProperty(
        "keystore location for mgmt ssl",
        default=lambda c: get_mgmt_ks_path(c['mgmt_keystore_loc'])
    )

    db2u_config_path = StringProperty(
        "Directory for dbm, db, and reg config used by db2u",
        default="/mnt/blumeta0/db2_config"
    )

    db2u_configmap_loc = StringProperty(
        "Location of configmap file used by db2u build",
        default="/mnt/blumeta0/configmap/db2u/db2u-config-var"
    )

    db2_overflow_path = StringProperty(
        "Location of the overflow log paths when restore is happening",
        default="/mnt/bludata0/db2/overflow"
    )

    db2_user_file = StringProperty(
        "Location of db2 user file used by security plugin",
        default="/mnt/blumeta0/db2_config/users.json"
    )

    db2_local_user_file = StringProperty(
        "Location of local db2 user file used for syncing",
        default="/mnt/blumeta0/compose/users.json"
    )

    ucmon_service_id = StringProperty(
        "Service ID in use by console team",
        default="iam-ServiceId-b24da8fb-14b8-4b40-a2e6-0edce5714adb"
    )

    rfmon_service_id = StringProperty(
        "Service ID in use by monitoring team",
        default="iam-ServiceId-3f17ceca-3bbc-4fb1-a61e-5ec3b5f9a504"
    )

    db2_audit_dir = StringProperty(
        "db2 audit directory",
        default="/mnt/blumeta0/db2/audit"
    )

    db2_audit_cmd = StringProperty(
        "cmd to configure db2audit",
        default=lambda c: get_db2audit_cmd(c)
    )

    compatibility_vector = StringProperty(
        "Compatibility vector [ORA = Oracle Compatibility]",
        default="NULL"
    )

    plan_id = StringProperty(
        "plan id = standard | lite",
        default="standard"
    )


def get_db2_ssl_svr_keydb_loc(db_name):
    return "/mnt/blumeta0/db2/ssl_keystore/{0}_ssl.kdb".format(db_name)


def get_db2_ssl_svr_stash_loc(db_name):
    return "/mnt/blumeta0/db2/ssl_keystore/{0}_ssl.sth".format(db_name)


def setup_type(peers):
    if len(peers) > 1:
        setup_type = 'ha'
    else:
        setup_type = 'single'
    return setup_type


def get_ssl_port():
    id = os.environ.get("ID").upper().replace("-", "_")
    ssl = "C_{}_P_SERVICE_PORT_SSL".format(id)
    return os.environ.get(ssl)


def get_ks_path(db2_keystore_loc):
    return os.path.dirname(os.path.realpath(db2_keystore_loc))


def get_mgmt_ks_path(mgmt_keystore_loc):
    return os.path.dirname(os.path.realpath(mgmt_keystore_loc))


def get_db2audit_cmd(c):
    db2audit_cmd = "db2audit configure datapath {0} archivepath {1}".format(
        c['db2_audit_dir'], c['db2_audit_dir'])
    return db2audit_cmd


def get_extended_peers(peers, dr_peer):
    if dr_peer != "" and dr_peer != "disabled":
        peers.append(dr_peer)
    return peers
