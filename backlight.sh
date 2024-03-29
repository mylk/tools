#!/bin/bash
set -e

# have to set some permissions
# https://stackoverflow.com/a/39230095

FILE="/sys/class/backlight/intel_backlight/brightness"
CURRENT=$(cat "$FILE")

if [ "$1" = "-inc" ]
then
    NEW=$(( CURRENT + $2 ))
elif [ "$1" = "-dec" ]
then
    NEW=$(( CURRENT - $2 ))
fi

echo "$NEW" | tee "$FILE"
