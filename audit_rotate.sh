#!/bin/bash

today=`date '+%Y%m%d'`

machineName=`echo ${HOSTNAME} | cut -d. -f1`
curfileextension="_audit.log.gz.enc"
newfileextension="_audit.log."$today".gz.enc"

curfilename=$machineName$curfileextension
newfilename=$machineName$newfileextension

cd /opt/mysql/logs/

mv $curfilename $newfilename

mysql -e "set global audit_log_flush=1;"

scp $newfilename paxbkup01:/opt/datanet/99_mysql-audit-logs/

