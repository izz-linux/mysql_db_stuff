#!/bin/bash

cd /opt/datanet/99_mysql-audit-logs/
today=`date '+%Y%m%d'`
openssl enc -d -aes-256-cbc -pass pass:JustAnotherKey4AES -md sha256 -in PAXDNDB01_audit.log.$today.gz.enc -out PAXDNDB01_audit.log.$today.gz
gzip -d PAXDNDB01_audit.log.$today.gz
cat PAXDNDB01_audit.log.$today | python -m json.tool > PAXDNDB01.$today.json
#cat PAXDNDB01.$today.json | grep -A 12 host | grep -E "(user|command|query|ip)" | grep -B 1 -A 1 Query | grep -iE -B 2 "(update|delete|insert)" | cut -d: -f2 > PAXDNDB01.$today.write

cat PAXDNDB01.$today.json | grep -A 12 host | grep -E "(user|command|query|ip)" | grep -B 1 -A 1 Query | grep -iE -B 2 '(\")(update |delete |insert )' | cut -d: -f2 > PAXDNDB01.$today.write

yesterday=`date -d "Yesterday 22:00" '+%Y-%m-%d'`

if [ -s PAXDNDB01.$today.write ]
then
    mail -s "Write Queries attempted on $yesterday" -r MySQL-Alerts@rxbenefits.com soc@email.com < PAXDNDB01.$today.write
else
    echo "No attempted changes to Master!" | mail -s "Write Queries attempted on $yesterday" -r soc@rxbenefits.com noc@rxbenefits.com    
fi

rm -rf PAXDNDB01.$today.*
rm -rf PAXDNDB01_audit.log.$today
