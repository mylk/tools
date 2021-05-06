#!/bin/bash

# get the data
OUTPUT=`wget -o /dev/null -O - "http://www.actus.gr/export_code/eortologio_xhtml.php?morfi=1&what_day=1" | iconv -f WINDOWS-1253 -t UTF8`

# find data length
LENGTH=`echo $OUTPUT | wc -m`

# cut from pure data start position till the end of data
OUTPUT=`echo $OUTPUT | cut -c482-$LENGTH`

# get only pure data
OUTPUT=`echo $OUTPUT | awk -F '<' '{print($1)}'`

#echo $output | sed "s/\,\s/\n/g" | sort
echo $OUTPUT
