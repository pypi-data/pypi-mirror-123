import datetime
import os
import pwd
import time
import logging
import yaml
import fnmatch
import tarfile
import shutil
import base64
import binascii
import pickle
from compose.db2.utils import util_funcs
from threading import Timer
from cdb import log

db2_inst_path = os.path.expanduser("~db2inst1")
sqlrsdir_path = db2_inst_path + "/sqllib/sqlrsdir"
PICKLE_CACHE_FILE = "/tmp/db2pd_pickle_file" + str(os.getuid())
PICKLE_LOCK_FILE = "/tmp/tmp_lock_file" + str(os.getuid())
logger = log.get_logger(__name__)


# def find_installed_db2
def find_db2_install():
    base_dir = "/opt/ibm/db2"
    return "{0}/{1}/instance".format(base_dir, os.listdir(base_dir)[-1])

# function to uncompress a file


def uncompress_tgz(tgzfile):
    tar = tarfile.open(tgzfile)
    tar.extractall()
    tar.close()


# function check is shell variable exists
def check_os_variable(variable):
    try:
        os.environ[variable]
        return True
    except KeyError:
        return False


# function to find a file in dir
def findfile(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


# function to spawn a shell script
def run_a_script(name):
    return os.spawnl(os.P_NOWAIT, name)

# function generate a timestamp


def gen_tstamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

# function to copy between directories


def cp_between_dir(src, dst, method='cp'):
    if method == "cp":
        shutil.copy2(src, dst)
    elif method == "mv":
        shutil.move(src, dst)

# function is_base64


def is_base64string(value):
    try:
        base64.decodestring(value)
        return True
    except binascii.Error:
        return False


# function to load a cfg file
def load_config(cfgfile):
    with open(os.path.join(cfgfile), "r") as c:
        data = c.read()
        if is_base64string(data):
            config = yaml.load(base64.decodestring(data))
        else:
            config = yaml.load(data)
    return config


# function to see what user we are running as
def checkUserRunning():
    user = pwd.getpwuid(os.getuid()).pw_name
    return user

# function to run db2 command


def run_db2_command(command, user):
    payload = 'su - {0} -c \" {1} \"'.format(user, command)
    return payload


# function to cleanup directory
def cleanup_dir(folder):
    file_path = []
    for filename in os.listdir(folder):
        file_path.append(os.path.join(folder, filename))
    try:
        if file_path:
            for _file in file_path:
                if os.path.isfile(_file) or os.path.islink(_file):
                    os.unlink(_file)
                elif os.path.isdir(_file):
                    shutil.rmtree(_file)
    except Exception as e:
        logger.error('Failed to delete %s. Reason: %s' % (file_path, e))
        pass

# function to check size


def check_size(path="/mnt"):
    return shutil.disk_usage(path)


class RawPickle(object):
    def __init__(self, date=datetime.datetime(2000, 1, 1), raw_text="", db_name=""):
        """constructor"""
        self.db_name = db_name
        self.date = date
        self.raw_text = raw_text
        self.PICKLE_CACHE_FILE = "/tmp/db2pd_pickle_file" + str(os.getuid())
        self.PICKLE_LOCK_FILE = "/tmp/tmp_lock_file" + str(os.getuid())

    def get_raw_text(self):
        """Returns the raw text from the object"""
        return self.raw_text

    def is_old(self, age=15):
        """Used to determine if this object is old based on seconds passed in"""
        return (datetime.datetime.now() - self.date).total_seconds() > age
