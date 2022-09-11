#!/bin/bash

# example: port:445 country:gr

source secrets.sh

key="${SHODAN_API_KEY}"
params=`echo $* | tr ' ' '+'`

echo "Searching with parameters: ${params}"

curl -s -X GET "https://api.shodan.io/shodan/host/search?key=$key&query=${params}" | jq -r ".matches[].ip_str"

