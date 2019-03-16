#!/bin/bash

ORIGINAL_IP=`curl "https://www.showmyip.gr" --connect-timeout 5 --max-time 5 --silent | grep "ip_address" | awk -F ">" '{print($2)}'`;

OPEN_HOSTS=`sudo nmap -sS -PN -p 8080,8081,3128 --open -oG - --host-timeout 5s $1 | grep -v "#" | grep open | sed -e "s/\ //g" | sed -e "s/\t//g"`;

echo -n "Open hosts: ";
echo $OPEN_HOSTS | wc -w;

echo "";
echo "Real proxies:";

for EXAMINED_HOST in $OPEN_HOSTS
do
    EXAMINED_HOST_IP=`echo $EXAMINED_HOST | awk -F ":" '{print($2)}' | awk -F "(" '{print($1)}'`

    OPEN_3128=`echo $EXAMINED_HOST | grep 3128/open | wc -l`;
    OPEN_8080=`echo $EXAMINED_HOST | grep 8080/open | wc -l`;
    OPEN_8081=`echo $EXAMINED_HOST | grep 8081/open | wc -l`;

    OPEN_PORTS=();

    if [ $OPEN_3128 -gt 0 ]
    then
        OPEN_PORTS+=("3128");
    fi;

    if [ $OPEN_8080 -gt 0 ]
    then
        OPEN_PORTS+=("8080");
    fi;

    if [ $OPEN_8081 -gt 0 ]
    then
        OPEN_PORTS+=("8081");
    fi;

    for OPEN_PORT in "${OPEN_PORTS[@]}"
    do
        #echo "Examining $EXAMINED_HOST_IP:$OPEN_PORT";

        EXAMINED_HOST_IP_OPEN=`curl -x "$EXAMINED_HOST_IP:$OPEN_PORT" "https://www.showmyip.gr" --connect-timeout 5 --max-time 5 --silent | grep "ip_address" | awk -F ">" '{print($2)}'`;

        if [ -n "$EXAMINED_HOST_IP_OPEN" ] && [ "$ORIGINAL_IP" != "$EXAMINED_HOST_IP_OPEN" ]
        then
            echo "$EXAMINED_HOST_IP_OPEN:$OPEN_PORT";
        fi;
    done;
done;

