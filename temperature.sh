#!/bin/bash

# get your local meteo station url from http://meteo.gr/Gmap.cfm
STATION_URL="http://penteli.meteo.gr/stations/faliro/"

TEMPERATURE=`wget "$STATION_URL" -O - -o /dev/null | grep -m1 "lright" | awk -F ">" '{print($3)}' | awk -F "<" '{print($1)}'`

echo $TEMPERATURE;
