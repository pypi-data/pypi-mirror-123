import os
import socket
import re
from kubernetes import client as kubeclient
from kubernetes import config as kubeconfig
import bitmath
from json import loads


class Formation():
    def __init__(self, crd_group, account, id):
        self.crd_group = crd_group
        self.account = account
        self.id = id

    def get_formation(self):
        kube_cli = kubeclient.CustomObjectsApi(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        formation = kube_cli.get_namespaced_custom_object(
            self.crd_group, 'v1', self.account, 'formations', self.id)
        return formation

    def is_downscale(self, data):
        formation = self.get_formation()
        # this check happens prior to patch so will be pre-scale value still
        current_memory = bitmath.parse_string_unsafe(
            formation["spec"]["resource_configs"]["m"]["memory"]).bytes
        scale_request_memory = bitmath.parse_string_unsafe(
            data["memory"]).bytes
        return scale_request_memory < current_memory

    def get_service(self, name):
        kube_cli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        svc = kube_cli.read_namespaced_service(
            name=name, namespace=self.account).to_dict()
        return svc

    def get_pod_zone(self, pod_name):
        kube_cli = kubeclient.CoreV1Api(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        pod = kube_cli.read_namespaced_pod(pod_name, self.account)
        if 'failure-domain.beta.kubernetes.io/zone' in pod.metadata.labels:
            return pod.metadata.labels["failure-domain.beta.kubernetes.io/zone"]
        if 'topology.kubernetes.io/zone' in pod.metadata.labels:
            return pod.metadata.labels["topology.kubernetes.io/zone"]

    def get_disk_sz(self):
        formation = self.get_formation()
        return int(bitmath.parse_string_unsafe(formation["spec"]["resource_configs"]["m"]["disk"]).bytes//1024//1024//1024)

    def desired_mem_to_set(self, desired_memory=None, role="m"):
        # kube_cli = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(kubernetes.config.load_incluster_config()))
        # labels = kube_cli.read_namespaced_pod(c['hostname'], c['account']).metadata.labels
        # desired_memory = bitmath.parse_string_unsafe(labels.get("desiredMemory", {})).bytes

        # Get the memory value from formation, the pod desiredMemory value lags during scale operations
        formation = self.get_formation()
        reserved_memory = (512+256)*1024*1024

        if desired_memory is None:
            desired_memory = formation["spec"]["resource_configs"][role]["memory"]

        desired_memory = bitmath.parse_string_unsafe(desired_memory).bytes

        return int(((desired_memory-reserved_memory)/1024)/4)

    def get_backup_recipe_results(self, include_incomplete=False):
        available_backup_resources_dic = {}
        kube_cli = kubeclient.CustomObjectsApi(
            kubeclient.ApiClient(kubeconfig.load_incluster_config()))
        # get the list of backup resources created for current formation
        available_backup_resources_json = kube_cli.list_namespaced_custom_object(
            self.crd_group,
            "v1",
            self.account,
            "backups",
            pretty="true",
            label_selector="formation_id={}".format(self.id))

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
                    if resource['status'] == 'completed' or include_incomplete:
                        try:
                            backup_label = loads(resource["spec"]["restore_data"])[
                                'restore_time']
                        except:
                            backup_label = "FAILED_BACKUP" + \
                                str(failed_backups)
                            failed_backups += 1
                    else:
                        backup_label = "FAILED_BACKUP" + str(failed_backups)
                        failed_backups += 1
                except Exception:
                    backup_label = "FAILED_BACKUP" + str(failed_backups)
                    failed_backups += 1
                backup_resource_name = {
                    "id": resource["metadata"]["name"], "timestamp": resource["metadata"]["creationTimestamp"]}
                available_backup_resources_dic[
                    backup_label] = backup_resource_name

        return available_backup_resources_dic

    def get_successful_backups(self):
        """ this is to check what is the backup timestamp for the last know good backup from the
        backup recipes ran"""
        good_backups = []
        backup_data = self.get_backup_recipe_results(include_incomplete=True)
        failed_str = r"FAILED_BACKUP\d{1,3}"
        good_backups = sorted([key for key in backup_data.keys(
        ) if not re.match(failed_str, key)], reverse=True)
        return good_backups

    def get_formation_resources(self):
        """ this function to rather characterstics of a formation, 
        like cpu, memory and if its a MT one or not"""
        formation_spec = {}
        formation = self.get_formation()
        formation_mem = int(bitmath.parse_string_unsafe(
            formation["spec"]["resource_configs"]["m"]["memory"]).bytes/1024/1024/1024)
        formation_spec["memory"] = formation_mem
        formation_cpu = formation["spec"]["resource_configs"]["m"]["cpu"]
        formation_spec["cpu"] = int(formation_cpu)
        return formation_spec

    def get_connection_host(self):
        formation = self.get_formation()
        try:
            host = formation["status"]["connections"]["global-public"][0]["Hostname"]
            return host
        except KeyError or Exception:
            try:
                host = formation["status"]["connections"]["global-private"][0]["Hostname"]
                return host
            except KeyError or Exception:
                return "{}.{}.databases.appdomain.cloud".format(os.getenv("ID"),
                                                                os.getenv('CLUSTER_ID'))

    def get_connection_port(self):
        formation = self.get_formation()
        try:
            port = formation["status"]["connections"]["global-public"][0]["Port"]
            return int(port)
        except KeyError or Exception:
            try:
                port = formation["status"]["connections"]["global-private"][0]["Port"]
                return int(port)
            except:
                id = os.environ.get("ID").upper().replace("-", "_")
                ssl = "C_{}_P_SERVICE_PORT_SSL".format(id)
                return os.environ.get(ssl)

    def get_external_hostname(self):
        zone = self.get_pod_zone(os.getenv('POD_NAME'))
        if zone:
            return "{}-{}.private.db2.databases.appdomain.cloud".format(os.getenv('CLUSTER_ID'), zone)
        else:
            return "{}.private.db2.databases.appdomain.cloud".format(os.getenv('CLUSTER_ID'))

    def get_external_hadr_port(self):
        svc = self.get_service(
            "c-{}-h-{}".format(self.id, int(socket.gethostname()[-1])))
        for p in svc['spec']['ports']:
            if p['name'] == "hadr":
                return p['node_port']

    def get_replicas(self, role):
        formation = self.get_formation()
        return formation["spec"]["resource_configs"][role]["replicas"]

    def get_disaster_recovery_site(self):
        formation = self.get_formation()
        if 'databases.cloud.ibm.com/disaster-recovery-site' in formation["metadata"]["annotations"]:
            return formation["metadata"]["annotations"]["databases.cloud.ibm.com/disaster-recovery-crn"]
        return ""

    def is_disaster_recovery_site(self):
        formation = self.get_formation()
        if 'databases.cloud.ibm.com/disaster-recovery-site' in formation["metadata"]["annotations"]:
            return bool(formation["metadata"]["annotations"]["databases.cloud.ibm.com/disaster-recovery-site"])
        return False

    def is_primary_recovery_site(self):
        formation = self.get_formation()
        if 'databases.cloud.ibm.com/primary-recovery-site' in formation["metadata"]["annotations"]:
            return bool(formation["metadata"]["annotations"]["databases.cloud.ibm.com/primary-recovery-site"])
        return False

    def is_dr_configured(self):
        formation = self.get_formation()
        if ('databases.cloud.ibm.com/primary-recovery-site' in formation["metadata"]["annotations"] and
                bool(formation["metadata"]["annotations"]["databases.cloud.ibm.com/primary-recovery-site"])) or\
            ('databases.cloud.ibm.com/disaster-recovery-site' in formation["metadata"]["annotations"] and
                bool(formation["metadata"]["annotations"]["databases.cloud.ibm.com/disaster-recovery-site"])):
            return True
        return False
