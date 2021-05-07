#!/bin/bash

# get the list of tickers, keep the lines starting with a character, keep all lines except from the first 2, keep the second column
results=`wget -q -O - "https://raw.githubusercontent.com/nmapx/revolut-stocks-list/master/LIST.md" | grep ^\| | tail -n+3 | awk '{print($2)}'`

# split the input by the delimiter
tickers=($(echo $1 | tr "," "\n"))

# check if each ticker exists
for ticker in "${tickers[@]}"
do
    exists=`echo "$results" | grep -iE "^$ticker$"`

    if [ ! -z "$exists" ]; then
        # echo and convert to upper case
        echo "${ticker^^} exists!"
    fi;
done

exit 0

