#!/bin/bash

##############################
##      Izz Noland          ##
##  Updated: 10/10/2017     ##
##############################

# dump the auditlog table from the datanet prod DB
# single transaction takes point in time and does not lock the DB

today=`date +%Y%m%d`
yesterday=`date -d "yesterday 18:00" '+%Y%m%d'`

rm -rf /opt/datanet/DN_auditLog_bak-$yesterday.sql
mysqldump -h rxapp01 -u svcrepback --single-transaction datanet-3 AuditLog > /opt/datanet/DN_auditLog_bak-$today.sql
