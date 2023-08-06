### ************************************************************************###
###  IBM Confidential                                                       ###
###  OCO Source Materials                                                   ###
###                                                                         ###
###  (c) Copyright IBM Corporation 2017.                                    ###
###  All rights reserved.                                                   ###
###                                                                         ###
###  The source code for this program is not published or otherwise         ###
###  divested of its trade secrets, irrespective of what has been           ###
###  deposited with the U.S. Copyright Office.                              ###
### ************************************************************************###
###                                                                         ###
### Used to update key value pairs in a dashTX database despite which node  ###
### is the primary                                                          ###
### ************************************************************************###
import ibm_db
import yaml, os, json, time, base64, ssl, subprocess, sys, time
import logging
import argparse

from pprint import pprint as pp
from sqlUtils import DBConnException, Db2connection

NO_CONNECT_RC=99

"""
CRED_FILE="/opt/ibm/db2-governor/db2.yml"
DR_CRED_FILE="/opt/ibm/dashdbtxn-dr-engine/config.yml"



class DBConnException(Exception):
    def __init__(self, message):
        self.message = message


# Get a database connection from either the standby or the primary
# Since floating is not always available we will use the internal ip addresses
def getDatabaseConnection():
    '''Get the information needed to connect to the database'''
    if os.path.isfile(CRED_FILE):
        cred_data = open(CRED_FILE).read()
        cred_values = yaml.load(cred_data)
        username = cred_values['db2']['authentication']['username']
        password = cred_values['db2']['authentication']['password']
        dbname = cred_values['db2']['db']
        conn = None
        for ip in [cred_values['db2']['ip'],cred_values['db2']['ip_other']]:
            dsn = "UID=" + username + ";PWD=" + password + ";DATABASE=" + dbname + ";HOSTNAME=" + str(ip) + ";PORT=50001;PROTOCOL=TCPIP;SECURITY=ssl"
            try:
                conn = ibm_db.connect(dsn, '', '')
                return conn
            except Exception as e:
                pass

    if os.path.isfile(DR_CRED_FILE):
        cred_data = open(DR_CRED_FILE).read()
        cred_values = yaml.load(cred_data)
        dbname = cred_values['database']['db']
        conn = None
        sites = {"primary", "secondary"}
        for site in sites:
            values = []
            username = cred_values[site]['dbcreds']['user']
            password = cred_values[site]['dbcreds']['pwd']

            if "host_ip" in cred_values[site]:
                values.append(cred_values[site]['host_ip'])
            if "host_ip_other" in cred_values[site]:
                values.append(cred_values[site]['host_ip_other'])
            for ip in values:
                dsn = "UID=" + username + ";PWD=" + password + ";DATABASE=" + dbname + ";HOSTNAME=" + str(ip) + ";PORT=50001;PROTOCOL=TCPIP;SECURITY=ssl"
                try:
                    conn = ibm_db.connect(dsn, '', '')
                    return conn
                except Exception as e:
                    pass
                    
    raise DBConnException("ERROR:Not able to connect to standby or primary database.")
"""

# If the MASTER_KV table exists in the bluadmin_mon schema then use it otherwise create it
def makeTable(conn, schema, table):
   create = 'CREATE TABLE ' + schema + '.' + table +'( key varchar(50) NOT NULL, value varchar(240), PRIMARY KEY(key))'
   try:
      result = ibm_db.exec_immediate(conn, create)
   except Exception as e:
      pass
      
# Add the key and value to the database and then commit an exit.
def setKeyValuePair(key, value):
    db2Conn = Db2connection()
    conn = db2Conn.getDatabaseConnection()
    makeTable(conn, "IBMPDQ", "DASHDB_KVP")
    setvalues = ("merge into IBMPDQ.DASHDB_KVP using (values('"+key+"', '"+value+"')) AS tmp(KEY,VALUE) on IBMPDQ.DASHDB_KVP.KEY=tmp.KEY "
                "when matched then update set value='"+value+"' "
                "when not matched then insert (KEY, VALUE) values ('"+key+"', '"+value+"')")

    result = ibm_db.exec_immediate(conn, setvalues)
    ibm_db.commit(conn)
          
# Get the value requested
def getValue(key):
    db2Conn = Db2connection()
    conn = db2Conn.getDatabaseConnection()
    getvalue = 'select VALUE from '+  'IBMPDQ' + '.' + 'DASHDB_KVP' + " where key='" +  key + "'"
    stmt = ibm_db.exec_immediate(conn, getvalue)
    if ibm_db.fetch_row(stmt) != False:
        return ibm_db.result(stmt, "VALUE") 



parser = argparse.ArgumentParser(description='Get/Set key value pairs in the dashdb database under IBMPDQ.DASHDB_KVP.')
parser.add_argument('-k', '--key', required=True, action='append', dest='key_option', help='Key to set a value to or retrieve')
parser.add_argument('-v', '--value', dest='value_option', action='append', help="Value to set the key to")
parser.add_argument('-c','--credfile', dest='cred_file',default='/opt/ibm/db2-governor/db2.yml', help='Specify a credential file for the database connection. TESTING ONLY')
parser.add_argument("--verbose", action="store_true", help='print exceptions')

args = parser.parse_args()

CRED_FILE=args.cred_file


if args.key_option is None:
    parser.print_help()
    exit(2)

if args.value_option is None:
   try:
      rc = 0
      for i in range(len(args.key_option)):
         value = getValue(args.key_option[i])
         if value == None:
             if args.verbose:
                 print("Key does not exist")
             rc = 1
             exit(1)
         else:
             print(value)
      exit (rc)
   except DBConnException as e:
      if args.verbose:
          print(e.message)
      exit(NO_CONNECT_RC)
   except Exception as e2:
      if args.verbose:
          print(e2)
      exit(3)
else:
   try:
       if len(args.value_option) != len(args.key_option):
          print("The number of values must equal the number of keys.")
          exit(6)
       for i in range(len(args.value_option)):
           setKeyValuePair(args.key_option[i],args.value_option[i])
       exit (0)
   except Exception as e:
      if args.verbose:
          print(e)
      exit(4)

