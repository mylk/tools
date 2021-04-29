#!/bin/bash

results=`wget -q -O - "https://raw.githubusercontent.com/nmapx/revolut-stocks-list/master/LIST.md" | awk '{print($2)}' | grep -iE "^$1$"`

if [ -z "$results" ]; then exit 1; fi

echo "Yeap!"
exit 0

