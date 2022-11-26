#!/bin/bash

killall Xvfb
Xvfb :99 -screen 0 "1920x1080x16" &
DISPLAY=:99; liferea &

