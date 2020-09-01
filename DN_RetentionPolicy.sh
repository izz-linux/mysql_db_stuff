#!/bin/bash


# initialize variables
daily=false
weekly=false
monthly=false
yearly=false


# This will run at 3a after the backups have completed from the night before
yesterday=`date -d "yesterday 22:00" '+%Y%m%d'`
filename="meb_DN_full-$yesterday.tar.gz"

while getopts "dwmy" opt;
do
    case "$opt" in
	d)  daily=true
	    ;;
	w)  weekly=true
	    ;;
	m)  monthly=true
	    ;;
	y)  yearly=true
	    ;;
    esac
done


#echo -e "\n\nDaily is $daily, Monthly is $monthly, Yearly is $yearly\n\n"
#echo -e "\n\n$filename\n\n"

if [ $daily ]
then
    /usr/bin/cp /opt/datanet/$filename /opt/datanet/0_daily/
    #find /opt/datanet/0_daily/ -mtime +7 -exec rm -rf {} \;
    cd /opt/datanet/0_daily/
    ls -tp | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {}
fi

if [ $weekly ]
then
    /usr/bin/cp /opt/datanet/$filename /opt/datanet/1_weekly/
    #find /opt/datanet/1_weekly/ -mtime +28 -exec rm -rf {} \;
    cd /opt/datanet/1_weekly
    ls -tp | grep -v '/$' | tail -n +5 | xargs -I {} rm -- {}
fi

if [ $monthly ]
then
    /usr/bin/cp /opt/datanet/$filename /opt/datanet/2_monthly/
    cd /opt/datanet/2_monthly
    ls -tp | grep -v '/$' | tail -n +19 | xargs -I {} rm -- {}
fi

if [ $yearly ]
then
    /usr/bin/cp /opt/datanet/$filename /opt/datanet/3_yearly/
    cd /opt/datanet/3_yearly
    ls -tp | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {}
fi

rm -rf /opt/datanet/$filename
