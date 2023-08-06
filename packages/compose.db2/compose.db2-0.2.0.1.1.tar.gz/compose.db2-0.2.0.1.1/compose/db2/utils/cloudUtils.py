import itertools
from compose.db2 import configuration
import cdb.backups as cos
from cdb import log
logger = log.get_logger(__name__)


class S3Resource:
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        self.vendor = 's3'
        self.ep = self.conf['cos_endpoint']
        self.auth1 = self.conf['cos_access_key']
        self.auth2 = self.conf['cos_secret_access_key']
        self.container = self.conf['cos_bucket']
        # self.bdir = 'CSYS.{}'.format(self.conf['id']).upper()
        self.bdir = 'CSYS.db2cos'.upper()
        self.s3bucket = cos.s3_client_bucket(config=self.conf)
        self.ip = self.conf['fqdn']
        self.repo = self.conf['repo_type']
        self.bbdir = "HADRPrimary"
        self.authdir = "AuthDB"

    def get_items(self):
        return self.s3bucket.objects.all()

    def get_items_byfilter(self, prefix):
        return self.s3bucket.objects.filter(Prefix='{}/{}'.format(prefix,
                                                                  self.conf['db_name'].upper()))

    def backup_list(self):
        content = self.get_items_byfilter(self.bdir)
        stamps = []
        for obj in content:
            ts = obj.key.split("/")[1].split(".")[4]
            stamps.append(ts)
        return [k for k, _ in itertools.groupby(sorted(stamps, reverse=True))]
    
    def backup_size(self, backup_timestamp):
        content = self.get_items_byfilter(self.bdir)
        size = 0
        for obj in content:
            ts = obj.key.split("/")[1].split(".")[4]
            if ts == str(backup_timestamp):
                size += obj.size
        return size

    def bb_backuplist(self):
        content = self.get_items_byfilter(
            "{}/{}".format(self.bdir, self.bbdir))
        files = []
        for obj in content:
            files.append(obj.key)
        return files

    def put_file(self, source, target):
        with open(source, "rb") as f:
            self.s3bucket.put_object(key=target, Body=f)
        f.close()

    def delete_file(self, obj):
        try:
            logger.info("attempting to delete {}".format(obj))
            self.s3bucket.delete_objects(
                Delete={'Objects': [{'Key': '{}'.format(obj)}]})
        except Exception as e:
            logger.error(
                "failed to delete obj {} with exception {}".format(obj, e))

    def clean_hadrprimary_bkp_files(self):
        bsbkplist = self.bb_backuplist()
        [self.delete_file(_key) for _key in bsbkplist]

    @log.log_execution(logger)
    def s3action(self, *args, **kwargs):
        if args[0] == "ls":
            cmd = (
                "s3cmd --access_key=%(user)s --secret_key=%(key)s "
                "--host=%(host)s --host-bucket=\"%(bucket)s.%(host)s\" "
                "-r %(action)s "
                "s3://%(container)s/%(filter)s" % {'user': kwargs['cos_access_key'],
                                                   'key': kwargs['cos_secret_access_key'],
                                                   'host': kwargs['cos_endpoint'],
                                                   'bucket': '%(bucket)s',
                                                   'action': args[0],
                                                   'container': kwargs['cos_bucket'],
                                                   'filter': args[1]
                                                   }
            )
        elif args[0] in ("get", "cp", "mv"):
            cmd = (
                "s3cmd --access_key=%(user)s --secret_key=%(key)s "
                "--host=%(host)s --host-bucket=\"%(bucket)s.%(host)s\" "
                "-r %(action)s s3://%(container)s/%(source)s "
                "--skip-existing "
                "--force" % {'user': kwargs['cos_access_key'],
                             'key': kwargs['cos_secret_access_key'],
                             'host': kwargs['cos_endpoint'],
                             'bucket': '%(bucket)s',
                             'action': args[0],
                             'container': kwargs['cos_bucket'],
                             'source': args[1]
                             }
            )
            # gets to target wd
            if args[2]:
                cmd = cmd + " {}".format(args[2])

        elif args[0] == "put":
            cmd = (
                "s3cmd --access_key=%(user)s --secret_key=%(key)s "
                "--host=%(host)s --host-bucket=\"%(bucket)s.%(host)s\" "
                "-r %(action)s %(source)s "
                "s3://%(container)s/%(target)s" % {'user': kwargs['cos_access_key'],
                                                   'key': kwargs['cos_secret_access_key'],
                                                   'host': kwargs['cos_endpoint'],
                                                   'bucket': '%(bucket)s',
                                                   'action': args[0],
                                                   'source': args[1],
                                                   'container': kwargs['cos_bucket'],
                                                   'target': args[2]
                                                   }
            )
        logger.info("running s3action cmd {}".format(
            cmd.replace(kwargs['cos_access_key'], "xxxxxx").
            replace(kwargs['cos_secret_access_key'], "xxxxxx")))
        return cmd
