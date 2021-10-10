#!/bin/bash

until ping -c1 $1 > /dev/null 2>&1; do sleep 1; done
