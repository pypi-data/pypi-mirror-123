
from debroni_client.client import DebroniClient
from cdb import log
from compose.db2 import db2
from compose.db2.utils.db2rc import *
from compose.db2 import configuration
from compose.db2.utils.hadr import Db2HADR
import yaml
import time
import os
from os import path

logger = log.get_logger(__name__)


class Debroni:
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        self.debroni_client = DebroniClient(self.conf['fqdn'],
                                            self.conf['debroni_port'],
                                            ca_file=self.conf['tls_crt_file'],
                                            crt_file=self.conf['tls_crt_file'],
                                            key_file=self.conf['tls_key_file'])

    def close(self):
        self.debroni_client.close()

    def get_version(self):
        try:
            return self.debroni_client.get_version()
        except Exception as e:
            raise(e)

    def get_member_debroni_info(self):
        try:
            return self.debroni_client.get_member_debroni_info()
        except Exception as e:
            raise(e)

    # pause debroni orchestration
    def pause_debroni(self):
        try:
            self.debroni_client.pause_debroni()
        except Exception as e:
            raise(e)

    # unpause debroni orchestration
    def unpause_debroni(self):
        try:
            self.debroni_client.unpause_debroni()
        except Exception as e:
            raise(e)

    # get debroni info
    def debroni_info(self):
        try:
            info = self.debroni_client.get_member_debroni_info()
            return str(info).replace('\n', ', ')
        except Exception as e:
            raise(e)

    def get_member_database_details(self):
        try:
            info = self.debroni_client.get_member_database_details()
            return str(info).replace('\n', ', ')
        except Exception as e:
            raise(e)

    def get_bootstrap_msg(self):
        try:
            return self.debroni_client.get_bootstrap_msg()
        except Exception as e:
            raise(e)

    # directed takeover on local node
    def init_takeover(self, method="force_peer"):
        try:
            self.debroni_client.takeover(method)
        except Exception as e:
            raise(e)

    # flip_sync exchanges the standby sync and async nodes
    def flip_sync(self, direction):
        try:
            status = self.debroni_client.get_member_debroni_info()
            if status.is_controller:
                return self.debroni_client.flip_sync(direction)

            if not status.is_election_participant:
                raise RuntimeError(
                    "Current node is not an election participant; can't reliably determine which node is the controller")
            try:
                controller_client = DebroniClient(status.last_known_controller,
                                                  self.conf['debroni_port'],
                                                  ca_file=self.conf['tls_crt_file'],
                                                  crt_file=self.conf['tls_crt_file'],
                                                  key_file=self.conf['tls_key_file'])

                return controller_client.flip_sync(direction)
            except Exception as e:
                raise(e)
        except Exception as e:
            raise(e)

    # rotate_primary is an indirect takeover.
    # Will determine the standby node before issuing takeover
    def rotate_primary(self):
        try:
            status = self.debroni_client.get_member_debroni_info()
            if status.is_controller:
                return self.debroni_client.rotate_primary()

            if not status.is_election_participant:
                raise RuntimeError(
                    "Current node is not an election participant;"
                    "can't reliably determine which node is the controller")

            try:
                controller_client = DebroniClient(status.last_known_controller,
                                                  self.conf['debroni_port'],
                                                  ca_file=self.conf['tls_crt_file'],
                                                  crt_file=self.conf['tls_crt_file'],
                                                  key_file=self.conf['tls_key_file'])

                return controller_client.rotate_primary()
            except Exception as e:
                raise(e)
        except Exception as e:
            raise(e)

    # quick_rotate_primary is an indirect takeover.
    # Will determine the standby node before issuing takeover
    # expected to only be used in healthy scenarios such as eviction
    def quick_rotate_primary(self):
        try:
            status = self.debroni_client.get_member_debroni_info()
            if status.is_controller:
                return self.debroni_client.quick_rotate_primary()

            if not status.is_election_participant:
                raise RuntimeError(
                    "Current node is not an election participant;"
                    "can't reliably determine which node is the controller")

            try:
                controller_client = DebroniClient(status.last_known_controller,
                                                  self.conf['debroni_port'],
                                                  ca_file=self.conf['tls_crt_file'],
                                                  crt_file=self.conf['tls_crt_file'],
                                                  key_file=self.conf['tls_key_file'])

                return controller_client.quick_rotate_primary()
            except Exception as e:
                raise(e)
        except Exception as e:
            raise(e)

    # is_leader returns true if current node is primary node
    def is_leader(self):
        try:
            return self.debroni_client.is_leader()
        except Exception as e:
            raise(e)

    # is_sync returns true if current node is standby sync node
    def is_sync(self):
        try:
            return self.debroni_client.is_sync()
        except Exception as e:
            raise(e)

    # is_async returns true if current node is async node
    def is_async(self):
        try:
            return self.debroni_client.is_async()
        except Exception as e:
            raise(e)

    def is_singlenode(self):
        try:
            if len(self.conf['extended_peers']) == 1:
                return True
            else:
                return False
        except Exception as e:
            raise(e)

    # is_controller checks whether the current member is the controller node
    def is_controller(self):
        try:
            return self.debroni_client.is_controller()
        except Exception as e:
            raise(e)

    def assert_db_updated(self):
        try:
            result = self.debroni_client.run_process(
                "detect_db2_vrmf_change.sh")
            if result.rc != 0:
                raise RuntimeError("Db2 is not up to date: Return code {}\n{}".format(
                    result.rc, result.stderr))
        except Exception as e:
            logger.error(e)
            raise(e)

    def update_instance(self):
        filename = "/tmp/db_updated.txt"

        if path.exists(filename): # remove the file if it existed before this update
            os.remove(filename)

        try:
            result = self.debroni_client.run_process(
                "detect_db2_vrmf_change.sh")
            if result.rc == 0:
                # Already up to date: no-op
                pass

            elif result.rc == 1:
                open(filename, 'w').close() # create a marker file to denote we updated
                if path.exists(filename):
                    print("file created")

                result = self.debroni_client.run_process("update_instance.sh")
                if result.rc != 0:
                    logger.error("Couldn't update db2: Return code {}\n{}".format(
                        result.rc, result.stderr))
                    raise RuntimeError("Couldn't update db2")

            elif result.rc == 2:
                open(filename, 'w').close() # create a marker file to denote we updated
                if path.exists(filename):
                    print("file created")

                result = self.debroni_client.run_process("upgrade_instance.sh")
                if result.rc != 0:
                    logger.error("Couldn't upgrade db2: Return code {}\n{}".format(
                        result.rc, result.stderr))
                    raise RuntimeError("Couldn't upgrade db2")

            else:
                logger.error("Unexpected return code from VRMF check: {}\n{}\n{}".format(
                    result.rc, result.stdout, result.stderr))
                raise RuntimeError(
                    "Encountered unexpected result during update check")

        except Exception as e:
            logger.error(e)
            raise(e)

    def update_db(self):
        filename = "/tmp/db_updated.txt"
        try:
            if path.exists(filename):
                result = self.debroni_client.run_process("update_db.sh")
                os.remove(filename)  # remove marker file after update

                if result.rc != 0:
                    raise RuntimeError("Couldn't update db2")
        except Exception as e:
            logger.error(e)
            raise (e)

    def set_dr_member(self, host, svc_port):
        try:
            return self.debroni_client.set_dr_member(host, svc_port)
        except Exception as e:
            logger.error(e)
            raise(e)

    def validate_dr_connected(self):
        connected = False
        while not connected:
            try:
                connected = self.debroni_client.is_dr_connected()
            except Exception as e:
                logger.info(e)
                logger.info("Waiting 30 seconds to check DR connected again")
                time.sleep(30)
                continue

    @log.log_execution(logger)
    def validate_hadr(self, check='ha'):
        db = db2.Db2(self.conf)
        designated_role = Db2HADR(self.conf).set_designated_role()
        if (designated_role.lower() != "standard" and len(self.conf['extended_peers']) != 1):
            while True:
                try:
                    info = yaml.load(str(
                        self.get_member_debroni_info()),
                        Loader=yaml.FullLoader)
                    logger.info("Able to validate info and state is {}".format(
                        info['init_state']))
                    while info["init_state"] != "COMPLETED":
                        logger.info(
                            "looping to check if debroni completed init")
                        info = yaml.load(str(
                            self.get_member_debroni_info()),
                            Loader=yaml.FullLoader)
                        if info["init_state"] not in ("COMPLETED",
                                                      "MAINTENANCE"):
                            logger.info("Debroni didn't complete hasetup,"
                                        "its init state is {}"
                                        .format(info['init_state']))
                            time.sleep(30)
                            continue
                        else:
                            logger.info("Debrioni completed hasetup, or "
                                        "its init state is {}"
                                        .format(info['init_state']))
                            while True:
                                try:
                                    if check == "ha":
                                        logger.info("validating hadr status")
                                        db.db2_ha_status()
                                    elif check == "primary":
                                        logger.info("validating primary role")
                                        db.db2_check_ifpri_isup()
                                except ValueError as e:
                                    logger.error("failed to validate "
                                                 "{0} check {1}".format(check, e))
                                    time.sleep(5)
                                    continue
                                break
                            else:
                                logger.info(
                                    "successfully validated {}".format(check))
                        break
                    else:
                        logger.info(
                            "Debroni moved to init COMPLETED state, validating checks")
                        while True:
                            try:
                                if check == "ha":
                                    logger.info("validating hadr status")
                                    db.db2_ha_status()
                                elif check == "primary":
                                    logger.info("validating primary role")
                                    db.db2_check_ifpri_isup()
                            except ValueError as e:
                                logger.error("failed to validate "
                                             "{0} check {1}".format(check, e))
                                time.sleep(5)
                                continue
                            break
                        else:
                            logger.info(
                                "successfully validated {}".format(check))
                except Exception as e:
                    logger.error("Unable to validate info and state, looping")
                    logger.error("debroni isn't ready yet {}".format(e))
                    time.sleep(10)
                    continue
                break
            else:
                logger.info("successfully checked debroni")
        else:
            logger.info(
                "Checking database status for {} deployment".format(designated_role))
            retry = 30
            while retry > 0:
                try:
                    self.get_version()
                    db.db2_status()
                    return
                except Exception as e:
                    logger.info(str(e))
                    retry = retry - 1
                    time.sleep(10)
                    continue
            raise RuntimeError("Db2 uptime not received in 300 seconds")


    def get_db_cfgs(self):
        try:
            return self.debroni_client.get_db_cfgs()
        except Exception as e:
            raise(e)

            
    def update_db2_keystore(self):
        try: 
            result = self.debroni_client.run_process("keystore_update_driver.sh")
            if result.rc != 0:
                raise RuntimeError("Couldn't update db2 keystore")
        except Exception as e:
            logger.error(e)
            raise (e)

            
