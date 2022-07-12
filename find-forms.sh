#!/bin/bash

while true; do
    RANDOM_ID=`dd status=noxfer if=/dev/random bs=1 count=300 2>/dev/null | tr -dc 'a-z0-9A-Z-' | cut -b1-48`
    URL="https://docs.google.com/forms/d/e/1FAIpQLS$RANDOM_ID/viewform"
    
    echo "Testing $URL"
    RESPONSE_CODE=`curl --head -s -o /dev/null -w "%{http_code}\n" "$URL"`
    echo $RESPONSE_CODE
    if [ $RESPONSE_CODE = "404" ]; then
        echo "$URL" >> /tmp/form-failures
    elif [ $RESPONSE_CODE = "200" ]; then
        echo "$URL" >> /tmp/form-successes
    fi

    SLEEP_TIME=$(($RANDOM % 10))
    if [ $SLEEP_TIME -eq 0 ]; then SLEEP_TIME=1; fi
    echo "Sleeping for $SLEEP_TIME."
    echo "==========================================================================================================="
    sleep $SLEEP_TIME
done

