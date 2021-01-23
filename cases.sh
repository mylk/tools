#!/bin/bash

TODAY=`command date '+%d/%m/%Y'`
TODAY_MONTH_NO_ZERO_PADDING=`command date '+%d/%_m/%Y' | sed 's/\s//g'`
# prefixed with "command" to override aliases of date command (ex. defined in .bashrc)

echo "${TODAY}"

curl -s --compressed 'https://flo.uri.sh/visualisation/3334247/embed?auto=1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0' -H 'Referer: https://public.flourish.studio/visualisation/3334247/' -H 'DNT: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' | \
grep "_Flourish_data = " | \
awk -F "= " '{print($2)}' | \
sed 's/.$//' | \
jq -r ".[][] | select(.label == \"${TODAY}\" or .label == \"${TODAY_MONTH_NO_ZERO_PADDING}\")[\"value\"][]"
