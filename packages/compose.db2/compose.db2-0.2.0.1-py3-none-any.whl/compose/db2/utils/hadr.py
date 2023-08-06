import os
import socket
import re
from compose.db2.utils.sqlUtils import Db2SQL
from compose.db2 import configuration, formation


class Db2HADR():
    def __init__(self, conf=None):
        if conf is None:
            conf = configuration.Configuration()
        self.conf = conf

    def build_hadr_standby_list(self):
        peers = self.conf['extended_peers']
        if len(peers) == 1:
            return "STANDARD"
        else:
            designated_primary_name = self.build_primary_host()
            standby_list = "'"
            for peer in peers:
                if peer.split(".")[0] != designated_primary_name.split(".")[0]:
                    standby_list += '"' + peer + '",'
            standby_list = standby_list[: -1]
            standby_list += "'"
            return standby_list

    def build_primary_host(self):
        peers = self.conf['extended_peers']
        id = os.environ.get("ID")
        if len(peers) == 1:
            for peer in peers:
                if peer.split(".")[0] in ("c-" + id + "-m-0"):
                    designated_pri = peer
        else:
            sqls = Db2SQL(self.conf)
            try:
                # get the result from a non DR peer, this will reduce the number of times we call sqls.run_desired_select_sql
                for peer in peers:
                    query = sqls.ha_primary
                    if not re.search('^.*private.db2.databases.appdomain.cloud$', peer):
                        result = sqls.run_desired_select_sql(peer, query)
                        break

                for peer in peers:
                    # cannot connect across clusters using local ports
                    if not re.search('^.*private.db2.databases.appdomain.cloud$', peer):
                        if result[0].get(0).split("|")[0] == peer:
                            designated_pri = peer
                            return designated_pri
                        else:
                            designated_pri = None
                            continue
                    else:
                        # unlike "result", the DR peer's name does not include "-zone" (i.e "lon04" for "London")
                        # therefore instead of checking if the result is equal the peer's name, we check if it contains the first part
                        if peer.split(".")[0] in result[0].get(0).split("|")[0]:
                            designated_pri = peer
                            return designated_pri
                        else:
                            designated_pri = None
                            continue
            except Exception:
                designated_pri = None
                pass

            if designated_pri is None:
                # no connection to db2 assume dr setup is first time or -0 node is primary
                if self.conf['disaster_recovery_host'] != "":
                    fmtn = formation.Formation(self.conf['crd_group'],
                                               self.conf['account'],
                                               self.conf['id'])
                    if fmtn.is_disaster_recovery_site():
                        designated_pri = self.conf['disaster_recovery_host']

            if designated_pri is None:
                for peer in peers:
                    if peer.split(".")[0] in ("c-" + id + "-m-0"):
                        designated_pri = peer
                        break
        return designated_pri

    def set_designated_role(self):
        hostname = socket.gethostname()
        peers = self.conf['extended_peers']
        if len(peers) == 1:
            designated_role = "STANDARD"
        else:
            designated_pri = self.build_primary_host().split(".")[0]
            for peer in peers:
                if hostname == designated_pri:
                    designated_role = "PRIMARY"
                    break
                else:
                    designated_role = "STANDBY"
        return designated_role

    def get_db2_hadr_start_cmd(self):
        designated_role = self.set_designated_role()
        if designated_role in ("PRIMARY", "STANDBY"):
            if designated_role == "PRIMARY":
                return "db2 start hadr on db %s as primary by force" % self.conf['db_name']
            elif designated_role == "STANDBY":
                return "db2 start hadr on db %s as standby" % self.conf['db_name']
        else:
            return "STANDARD"
