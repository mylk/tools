#!/bin/bash

# dummy command to request su permissions
sudo echo;

# echoes start time
TIME_START=`date +%s`;
echo "Started at:" `date +%H:%M:%S --date="@$TIME_START"`;


# the actual port scan
# -T4 is the equivalent of --max-rtt-timeout 1250ms --initial-rtt-timeout 500ms --max-retries 6 and sets the maximum TCP scan delay to 10ms
# -T3 is the default
# http://nmap.org/book/man-performance.html
OPEN_HOSTS=`sudo nmap -sS -n -T4 -p 139 $1 $2 --open -oG - | grep open | grep -v Nmap | awk '{print($2)}'`;


# echoes end time
TIME_END=`date +%s`;
echo "Ended at:" `date +%H:%M:%S --date="@$TIME_END"`;


# calculates duration and suffix
DURATION=`echo "$TIME_END - $TIME_START" | bc`;
if [ $DURATION -gt 60 ]
then
	DURATION=`echo "scale=2; $DURATION / 60" | bc`
	SUFFIX="m"
else
	SUFFIX="s"
fi;
echo "Duration: $DURATION$SUFFIX";


# gets total scanned hosts
# @TODO check if octets have "-". if not, don't multiply and assign 1 as default to octet3
# @TODO add 2nd octet too
# @TODO check if $1 === -R and set $2 to host_count
OCTET3=`echo $1 | awk -F "." '{print($3)}' | bc`;
OCTET4=`echo $1 | awk -F "." '{print($4)}' | bc`;
# fixes 128-129=-1, but are two octets
HOST_COUNT=`echo "($OCTET3-1) * $OCTET4" | bc`;


# prints open hosts count
echo "";
echo "Open hosts: " `echo $OPEN_HOSTS | wc -w`;
echo "Total scanned: $HOST_COUNT";


# loops through open hosts and gets shared disks
for EXAMINED_HOST in $OPEN_HOSTS;
do
	echo "";
	echo "Resolving $EXAMINED_HOST";
	smbclient -L $EXAMINED_HOST -U administrator --no-pass | grep Disk;
done;

