#!/bin/bash

curl 'http://192.168.1.1/cgi-bin/setobject?/' --data-raw 'setobject_reboot=i1.3.6.1.4.1.283.1000.2.1.6.3.1.0%3D1' -s > /dev/null && echo "Success!"
