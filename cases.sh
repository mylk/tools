#!/bin/bash
TODAY=`command date '+%Y-%m-%d'`
# prefixed with "command" to override aliases of date command (ex. defined in .bashrc)

curl 'https://covidapi.ismood.com/daily-info/?country_name=greece' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://covid19live.ismood.com/' -H 'Authorization: Basic ZmFkaWw6aXNjb3Y0NTZA' -H 'Origin: https://covid19live.ismood.com' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -s | jq ".[] | select(.date == \"$TODAY\")[\"date\", \"new_cases\"]"
