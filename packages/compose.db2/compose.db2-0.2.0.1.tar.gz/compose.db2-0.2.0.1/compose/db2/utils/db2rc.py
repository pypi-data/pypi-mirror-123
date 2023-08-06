import shlex
import time
import subprocess
import re
import os
import signal
import functools
from cdb import log
logger = log.get_logger(__name__)

errors = (subprocess.CalledProcessError,
          subprocess.SubprocessError,
          subprocess.TimeoutExpired)


def retry(retries=2):
    def dec(rfunc):
        @functools.wraps(rfunc)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return rfunc(*args, **kwargs)
                except errors as e:
                    print(e)
                    left = retries - i
                    if left > 0:
                        print("Waiting 10 seconds to retry")
                        time.sleep(10)
        return wrapper
    return dec


class SQLError(Exception):
    def __init__(self, data):
        self.data = data

    def sqlwarnerr(self):
        regex = r"SQL\d{1,10}\w[WN]"
        sql_code = re.findall(regex, self.data)
        if len(sql_code) > 0:
            return sql_code[0]
        else:
            return None

    sqlignore_error_codes = {
        'SQL20189W': "The buffer pool operation (CREATE/ALTER) will not take effect until the next database startup due to insufficient memory.",
        'SQL0601N': "The name of the object to be created is identical to the existing name name of type type.",
        'SQL0061W': "The binder is in progress.",
        'SQL1766W': "The command completed successfully. However, LOGINDEXBUILD was not enabled before HADR was started.",
        'SQL1490W': "Activate database is successful, however, the database has already activated on one or more nodes.",
        'SQL1373W': "Cannot unquiesce instance or database name, because it is not quiesced.",
        'SQL1371W': "The quiesce operation was not executed because the specified instance or database named name is already quiesced.",
        'DBI1302E': "Invalid parameter detected.",
        'SQL1026N': "The database manager is already active.",
        'SQL1063N': "DB2START processing was successful.",
        'SQL6036N': "START or STOP DATABASE MANAGER command is already in progress.",
        'SQL1777N': "HADR is already started.",
        'SQL1363W': "One or more of the parameters submitted for immediate modification were not changed dynamically",
        'SQL1776N': "The command cannot be issued on an HADR Standby database.",
        'SQL1013N': "The database alias name or database name could not be found",
        'SQL30061N': "The database alias or database name can't be found",
        'SQL30082N': "Security processing failed with reason 3",
        'SQL1024N': "A database connection does not exist",
        'SQL1769N': "Stop HADR cannot complete. Reason code = reason-code.",
        "SQL1096N": "The command is not valid for this node type.", 
        "SQL2431W": "The database backup succeeded.  On each database partition, only those log files that were active during the backup operation are included in the backup image."
    }

    sqlretry_error_codes = {
        "SQL1119N": "restore is incomplete or still in progress",
        'SQL1035N': "The operation failed because the specified database cannot be connected to in the mode requested.",
        'SQL1495W': "Deactivate database is successful, however, there is still a connection to the database"
    }

    def return_error_msg(self, data):
        return SQLError.sqlignore_error_codes.get(data)


def return_error_code(message):
    return message.split(" ", 1)[0]


def db2_cmd_execution(cmd,
                      use_shell=False,
                      retries=3,
                      timeout=300,
                      success_ret=(0,),
                      return_msg=False):

    result = subprocess.Popen(shlex.split(cmd),
                              stdout=subprocess.PIPE,
                              shell=use_shell
                              )

    full_msg = ""
    try:
        full_msg = result.communicate(timeout)[0].decode("utf-8")
        if return_msg:
            return str(full_msg)
        msg = full_msg.strip("\n")
        if result.returncode not in success_ret:
            logger.error(
                "failed to run cmd with rc={} "
                "checking for sqlcode".format(result.returncode))
            if SQLError(str(msg)).sqlwarnerr() in SQLError(str(msg)).sqlignore_error_codes.keys():
                logger.info(msg)
                logger.info("cmd ran got {}".format(
                    SQLError(str(msg)).sqlwarnerr()))
                pass
            elif SQLError(str(msg)).sqlwarnerr() in SQLError(str(msg)).sqlretry_error_codes.keys():
                logger.info(msg)
                logger.info("cmd ran got {} retrying again".format(
                    SQLError(str(msg)).sqlwarnerr()))
                for i in range(retries):
                    result = subprocess.Popen(shlex.split(cmd),
                                              stdout=subprocess.PIPE,
                                              shell=use_shell
                                              )
                    full_msg = result.communicate(
                        timeout)[0].decode("utf-8")
                    msg = full_msg.strip("\n")
                    if result.returncode not in success_ret:
                        logger.error("cmd failed with {}, "
                                     "going to retry in 10s".format(msg))
                        time.sleep(10)
                        continue
                    else:
                        logger.info(
                            "cmd completed successfully with {}".format(msg))
                        break
                else:
                    logger.error("maxed out attempts to retry, still "
                                 "failing "
                                 "with{}".format(msg))
                    raise runCmdException(msg)
            else:
                logger.error("failed to run cmd {}".format(msg))
                raise runCmdException(msg)
        else:
            logger.info("cmd ran successfully with {}".format(msg))
    except subprocess.TimeoutExpired:
        logger.error("Timedout Running cmd")
        os.killpg(os.getpgid(result.pid), signal.SIGINT)
        raise runCmdException("Timedout Running db2 cmd")
    except Exception as e:
        if return_msg:
            return str(full_msg)
        raise(e)
    result.terminate()
    if return_msg:
        return str(full_msg)


def db2_checkcall_cmd_execution(cmd, use_shell=False):
    try:
        subprocess.check_call(shlex.split(cmd),
                              shell=use_shell)
    except subprocess.CalledProcessError as e:
        logger.error("failed to run cmd with error {}".format(
            str(subprocess.check_output(shlex.split(cmd)).strip(), 'utf-8').split(' ')[2]))
        raise runCmdException(e.output)


class FileUploadError():
    message = "Unable to upload Backup to objStore."


class FileDownloadError():
    message = "Unable to download file from objStore"


class BackupCreationError():
    message = "Unable to create Backup."


class runCmdException(Exception):
    message = "Untable to run a command"
