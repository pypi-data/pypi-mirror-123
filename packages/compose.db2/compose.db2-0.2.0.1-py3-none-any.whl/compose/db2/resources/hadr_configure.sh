#!/bin/bash

sudo [ -d /root/bootstrap ] || sudo mkdir /root/bootstrap

log_file=/root/bootstrap/bootstrap.sh.hadrsetup.log.$(date +%Y%m%d_%H%M%S)
echo "Running /conf/db2oc/bootstrap.sh --hadrsetup logged to $log_file"

/conf/db2oc/bootstrap.sh --hadrsetup 2>&1 | sudo tee $log_file
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "HADR configure setup failed, check logs in /tmp"
    exit 1
fi