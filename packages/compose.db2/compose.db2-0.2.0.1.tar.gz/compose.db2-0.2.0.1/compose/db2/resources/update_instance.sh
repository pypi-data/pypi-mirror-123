#set -e
set -x
sudo sed -i '/\/bin\/sync/s/^/#/' /opt/ibm/db2/V11.5.0.0/instance/db2iupdt_local
sudo /bin/su -l db2inst1 -c "/db2u/scripts/db2u_update.sh -inst > /tmp/update_instance.log 2>&1"


echo "** Adding db2set DB2_REMSTG_ENABLE_LOGARCH=TRUE -immediate for Archive Logging for 11.5.6 Db2 **" >> /tmp/update_instance.log
sudo /bin/su -l db2inst1 -c "db2set DB2_REMSTG_ENABLE_LOGARCH=TRUE -immediate"
return_code=`sudo /bin/su -l db2inst1 -c "db2set | grep -q DB2_REMSTG_ENABLE_LOGARCH; echo $?"`

if [[ $return_code == 0 ]] 
then
        echo "** db2set DB2_REMSTG_ENABLE_LOGARCH=TRUE was successfully set **" >> /tmp/update_instance.log
else
        echo "** db2set DB2_REMSTG_ENABLE_LOGARCH=TRUE failed  **" >> /tmp/update_instance.log
fi
