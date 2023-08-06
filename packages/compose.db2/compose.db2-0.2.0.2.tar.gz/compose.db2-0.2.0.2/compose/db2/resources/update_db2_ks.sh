#!/bin/bash

# need this to get access to runCommand and certs variables and BaR keystore funcs
DIR=/db2u/db2oc-neb-hasetup
source "$DIR/common_bkp_res_kskp.sh"

# creating this here temporarily as the one in $DIR/common_bkp_res_kskp.sh has bug; fixing it now will result to creating
# a new db container image which will complicate the ssl cert update release.
{% raw %}
function backup_restore_ks_v2() {
   logger_info "executing backup_restore_ks function" >>${logFile}
   load_variables
   role=$1
   action=$2
   
   shopt -s nocasematch
   if [[ ${CLOUD_OBJSTORE_USERNAME} == "" ]] || [[ ${CLOUD_OBJSTORE_APIKEY} == "" ]] ||
      [[ ${CLOUD_OBJSTORE_CONTAINER} == "" ]] || [[ ${CLOUD_OBJSTORE_CONTAINER_DIR} == "" ]] ||
      [[ ${CLOUD_OBJSTORE_EP} == "" ]]; then
      logger_error "Object store information can't be null" >>${logFile}
      exit $FAIL
   else
      SwiftKeystoreLoc="${CLOUD_OBJSTORE_CONTAINER_DIR}/HADRPrimary/${DBNAME}keystore"
      if [[ $role == "PRIMARY" ]] && [[ $action == "backup" ]]; then
         cleanup_ks_kp_inobjs
         if [ -d $KEYPROTECT_LOCATION ] || [ -d $KEYSTORE_LOCATION ]; then
            zip_files
            [ -d $KEYPROTECT_LOCATION ] && backup_config "kp.zip.tar" || echo "ignore running kp.zip.tar"
            [ -d $KEYSTORE_LOCATION ] && backup_config "ks.zip.tar" || echo "ignore running ks.zip.tar"
         fi
         [ -d $SQLRSDIR_LOCATION ] && backup_config "sqlrsdir"
         backup_config "sqlrsbak" ||
            logger_error "$SQLRSDIR_LOCATION doesn't exist ignore backup" >>${logFile}

      elif [[ $role == "STANDBY" ]] && [[ $action == "restore" ]]; then
         list_ks_kp_inobjs
         # retry for 10 minutes and then dump out, need to wait for sqlrsdir/sqlrsbak/ks.zip.tar to be available for full restore
         while [[ ! "${ksfiles[@]}" =~ "sqlrsdir" || ! "${ksfiles[@]}" =~ "sqlrsbak" || ! "${ksfiles[@]}" =~ "ks.zip.tar" && $retry_count -lt 120 ]]; do
            sleep 5
            logger_info "Waiting for keystore to be available for restore" >>${logFile}
            list_ks_kp_inobjs
            ((retry_count++))
         done
         [ -e $TMP_STORAGE/ks.zip ] && rm -rf $TMP_STORAGE/ks.zip || echo "$TMP_STORAGE/ks.zip doesn't exist yet"
         [ -e $TMP_STORAGE/kp.zip ] && rm -rf $TMP_STORAGE/kp.zip || echo "$TMP_STORAGE/kp.zip doesn't exist yet"
         logger_info "found ${ksfiles[@]} going to restore"
         if ((${#ksfiles[@]} != 0)); then
            for ksfile in ${ksfiles[@]}; do
               restore_config "$ksfile"
            done
         fi
      fi
   fi
}
{% endraw %}

function run_cert_validation(){
   db2_cert_expiry_year=`echo | openssl s_client -connect localhost:55000 2>/dev/null | openssl x509 -noout -dates | awk '/notAfter/{print $4}'`
   local_cert_expiry_year=`sudo cat /secrets/db2certs/db2.crt| openssl x509 -noout -dates | awk '/notAfter/{print $4}'`
   if (( ${db2_cert_expiry_year} == ${local_cert_expiry_year} )); then
      return 0
   else
      return 1
   fi
}

# if the cert db2's currently serviing doesn't match what got synced from ca-digicert then update the ks
db2_cert_expiry_year=`echo | openssl s_client -connect localhost:55000 2>/dev/null | openssl x509 -noout -dates | awk '/notAfter/{print $4}'`
local_cert_expiry_year=`sudo cat /secrets/db2certs/db2.crt| openssl x509 -noout -dates | awk '/notAfter/{print $4}'`

if [[ "$db2_cert_expiry_year" -ne "$local_cert_expiry_year" ]]; then 
  # To enable online update of SSL_SVR_LABEL
  runCommand "db2set -immediate DB2_DYNAMIC_SSL_LABEL=ON"

  # Recreate keystore only on PRIMARY then make it available on STANDBY
  role=`db2 get db cfg for bludb | grep -i role | awk -F'=' '{print $2}'`
  if [[ "$role" =~ "PRIMARY" || "$role" =~ "STANDARD" ]]; then
    
    ## re-creating the  keystore with new certs  
    # delete the signed certificate if exists to create a new one without errors
    if [[ -n `gsk8capicmd_64 -cert -list -db ${db2_keystore_file} -stashed | grep ${p12Label}` ]]; then
       runCommand "gsk8capicmd_64 -cert -delete -db ${db2_keystore_file} -stashed -label ${p12Label}" || traceExit "Cert Delete Failed"
    else
       logger_info "Cert with label \"$p12Label\" not found." >>${logFile} || traceExit "Cert with label\"$p12Label\" not found. "
    fi

    # re-generate the p12 bundle using the new cert/key pair
    generateP12

    # keep a copy of old ks before delete; ks is deleted as the import cmd will fail if already exists
    cp -f $db2_keystore_file /tmp/ks-bkup-`date +%Y-%m-%d-%s`.p12
    cp -f $db2_keystore_loc/keystore.sth /tmp/ks-bkup-`date +%Y-%m-%d-%s`.sth
    rm -rf $db2_keystore_loc/keystore.*

    # recreate the db keystore cert file
    runCommand "gsk8capicmd_64 -keydb -create -db ${db2_keystore_file} -pw ${admin_passwd} -type pkcs12 -stash" || traceExit "Failed creating db keystore"

    # import signed certificate
    runCommand "gsk8capicmd_64 -cert -import -db ${p12File} -pw ${p12FilePassword} -target ${db2_keystore_file} -target_stashed" || traceExit "Import Failed"

    # Set default label to $p12Label signed certificate
    runCommand "gsk8capicmd_64 -cert -setdefault -db ${db2_keystore_file} -stashed -label ${p12Label}" || traceExit "Failed setting default label to $p12Label"

    # list certificates
    runCommand "gsk8capicmd_64 -cert -list -db ${db2_keystore_file} -stashed -label ${p12Label}" || traceExit "Failed listing cert"

    # validate certificate
    runCommand "gsk8capicmd_64 -cert -validate -db ${db2_keystore_file} -stashed -label ${p12Label}" 

    [ -e ${p12File} ] && sudo rm -rf ${p12File} || logger_info "${p12File} does not exist" >>${logFile}

    # recreate alias
    runCommand "create_aliases " || trackerExit "Failed running create_aliases on $role "

    # backup the ks from PRIMARY and restore it on STANDBY
    runCommand "backup_restore_ks_v2 "PRIMARY" "backup"" || traceExit "Failed backing up new keystore from  primary"

    logger_info "backup ks done on primary" >> ${logFile}
  elif [[ "$role" =~ "STANDBY" ]]; then
    # move the old keystore files so the new ones can be restored in the known dir path
    mv $db2_keystore_loc/keystore.p12 /tmp/ks-bkup-`date +%Y-%m-%d-%s`.p12 
    mv $db2_keystore_loc/keystore.sth /tmp/ks-bkup-`date +%Y-%m-%d-%s`.sth
    runCommand "backup_restore_ks_v2 "STANDBY" "restore"" || traceExit "Failed restoring keystore on standby"
    
    logger_info "restore ks done on standby" >> ${logFile}
  fi

  # update ssl labels in db2 cfg 
  db2 attach to db2inst1; db2 update dbm cfg using SSL_SVR_LABEL ${p12Label} immediate
  db2 connect to bludb > /dev/null; db2 update db cfg for bludb using HADR_SSL_LABEL ${p12Label} immediate> /dev/null

  logger_info "Updated db2 cert." >> ${logFile}
   
  # For HA, reset the HADR connection on pri then restart db2 on sby then reset hadr as well
   if [[ "$role" =~ "PRIMARY" || "$role" =~ "STANDBY" ]]; then
    runCommand "db2stop force"
    runCommand "db2start"
    if [[ "$role" =~ "PRIMARY" ]]; then
      runCommand "db2 start hadr on db bludb as primary by force"
      run_cert_validation
      rc=$?
      if (( $rc == 0 )); then
         logger_info "successfully rotated the cert on primary, new expiry is ${db2_cert_expiry_year}" >>${logFile}
      else
          logger_error "failed to rotate the cert on primary, new expiry is ${db2_cert_expiry_year}" >>${logFile}
          exit 1
      fi          
      
    elif [[ "$role" =~ "STANDBY" ]]; then
      runCommand "db2 activate db bludb"
      runCommand "db2 start hadr on db bludb as standby"
      run_cert_validation
      rc=$?
      if (( $rc == 0 )); then
         logger_info "successfully rotated the cert on standby, new expiry is ${db2_cert_expiry_year}" >>${logFile}
      else
         logger_error "failed to rotate the cert on standby, new expiry is ${db2_cert_expiry_year}" >>${logFile}
         exit 1
      fi      
    fi

    logger_info "HADR connection restart completed." >> ${logFile}
  fi

else
  logger_info "db2 cert has been updated already. Doing nothing..." >> ${logFile}
fi

exit 0
