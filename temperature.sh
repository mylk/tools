#!/bin/bash

# get your local meteo station url from http://meteo.gr/Gmap.cfm
STATION_URL="http://penteli.meteo.gr/stations/faliro/"

TEMPERATURE=`wget "$STATION_URL" -O - -o /dev/null | grep --text "3366FF" | head -1 | awk -F ">" '{print($5)}' | awk -F "<" '{print($1)}' | iconv -f WINDOWS-1253 -t UTF8`

echo $TEMPERATURE;
