from compose.db2 import configuration, formation
from compose.db2.utils.cloudUtils import S3Resource
from cdb import log
import datetime
import time
import os
from json import dumps, loads, dump, load

class Bucket():
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf
        self.cos = S3Resource(self.conf)
        self.logger = log.get_logger(__name__)
    
    def file_exists(self, filename):
        cos_file = self.cos.s3bucket.objects.filter(Prefix='{}/{}'.format(self.cos.bdir,filename))
        num_user_files = sum(1 for _ in cos_file)
        if num_user_files > 0:
            return True
        else:
            return False

    # wait_for_file waits indefinitely for a file presence on COS unless timeout specified
    def wait_for_file(self, filename, timeout=0, interval=60):
        time_start_seconds = round(time.time())
        exists=False
        while not exists:
            time_current_seconds = round(time.time())
            current_duration = time_current_seconds - time_start_seconds
            self.logger.info("checking for existance of file: {} with a timeout of {} secs | current duration: {} secs".format(
                                                                            filename, timeout, current_duration))
            exists = self.file_exists(filename)
            if timeout > 0:
                if current_duration > timeout:
                    raise Exception("specified timeout of {} secs exceeded while waiting for file: {}".format(timeout, filename))
            time.sleep(interval)

    # publish_fmtn_hadr_ports_to_cos publishes local hadr service ports to cos
    def publish_fmtn_hadr_ports_to_cos(self, hostnames, ports, peers):
        fmtn = formation.Formation(self.conf['crd_group'], 
                                self.conf['account'],
                                self.conf['id'])
        cos_ports = {}

        cos_ports['hostnames'] = hostnames
        cos_ports['ports'] = ports
        cos_ports['pods'] = peers

        if fmtn.is_disaster_recovery_site():
            self.logger.info("Publishing disaster recovery hadr ports for disaster recovery site: {}".format(ports))
            fname = "disaster_recovery_site_hadr_ports.json"
        elif fmtn.is_primary_recovery_site():
            self.logger.info("Publishing disaster recovery hadr ports for primary site: {}".format(ports))
            fname = "primary_recovery_site_hadr_ports.json"            
        else:
            raise Exception("Unable to determine disaster recovery site")

        self.logger.info("Writing payload to cloud: {}".format(cos_ports))

        with open(fname, 'w') as fd:
            dump(cos_ports, fd)

        cos_target = "{}/{}".format(self.cos.bdir, fname)
        self.cos.s3bucket.upload_file(fname,cos_target)

    # get_external_port_data_from_cos returns the port information from COS for the opposite site
    # format:
    # {
    #   "ports":[0,1,2]
    #   "hostname":"host"
    # }
    def get_external_port_data_from_cos(self, fname=None):
        try:
            if fname is None:
                fmtn = formation.Formation(self.conf['crd_group'], 
                                        self.conf['account'],
                                        self.conf['id'])

                # get the reverse site's data
                if fmtn.is_disaster_recovery_site():
                    fname = "primary_recovery_site_hadr_ports.json"  
                elif fmtn.is_primary_recovery_site():
                    fname = "disaster_recovery_site_hadr_ports.json"       
                else:
                    raise Exception("Unable to determine disaster recovery site")

            self.cos.s3bucket.download_file("{}/{}".format(self.cos.bdir,fname), fname)
            
            with open(fname) as fd:
                data = load(fd)
            return data
        except Exception as e:
            self.logger.error(e)
            return None




    



