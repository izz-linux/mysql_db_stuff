#!/bin/bash

##############################
##      Izz Noland          ##
##  Updated: 10/10/2017     ##
##############################

# dump the idcadcopy database from DN Prod MySQL Instance
# single transaction takes point in time and does not lock the DB

today=`date +%Y%m%d`
yesterday=`date -d "yesterday 22:00" '+%Y%m%d'`

rm -rf /opt/datanet/IDCC_full_bak-$yesterday.sql
mysqldump -h rxapp01 -u svcrepback --single-transaction idcardcopy > /opt/datanet/IDCC_full_bak-$today.sql
