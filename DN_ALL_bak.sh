#!/bin/bash

##############################
##      Izz Noland          ##
##  Updated: 10/10/2017     ##
##############################

# dump all databases from the mysql instance on rxapp01 prod, excluding the auditlog table
# single transaction takes point in time and does not lock the DB

today=`date +%Y%m%d`
yesterday=`date -d "yesterday 22:00" '+%Y%m%d'`

rm -rf /opt/datanet/DN_full_bak-$yesterday.sql
mysqldump -h rxapp01 -u svcrepback --single-transaction --routines --triggers --ignore-table=datanet-3.auditlog --all-databases > /opt/datanet/DN_full_bak-$today.sql
