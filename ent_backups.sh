#!/bin/bash

today=`date +%Y%m%d`
mkdir -p /opt/mysql/logs/$today

cd /opt/mysql/logs/

/usr/local/sbin/meb-4.1/bin/mysqlbackup --slave-info --compress --no-history-logging --backup-image=DN-$today.mbi --backup-dir=/opt/mysql/logs/$today backup-to-image

tar -pcvzf meb_DN_full-$today.tar.gz ./$today

scp meb_DN_full-$today.tar.gz paxbkup01:/opt/datanet/meb_DN_full-$today.tar.gz


rm -rf meb_DN_full-$today.tar.gz 
rm -rf $today/
