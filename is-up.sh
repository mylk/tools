#!/bin/bash

NAME="VIES"
HOST="http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
EMAIL="my@support.com"

RESPONSE_HEADERS=`curl --head --silent -L "$HOST"`
IS_UP=`echo $RESPONSE_HEADERS | grep "HTTP/1.1 200 OK" | wc -l | awk '{print($1)}'`;

if [ $IS_UP -ne 1 ]
then
    if [ ! -f "/tmp/$NAME_is_down" ]
    then
        touch "/tmp/$NAME_is_down";
        echo "$RESPONSE_HEADERS" | mail -s "$NAME is down." "$EMAIL";
    fi;
else
    if [ -f "/tmp/$NAME_is_down" ]
    then
        rm "/tmp/$NAME_is_down";
        echo "$RESPONSE_HEADERS" | mail -s "$NAME is up." "$EMAIL";
    fi;
fi;

