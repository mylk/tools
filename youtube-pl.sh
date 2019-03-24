#!/bin/bash
for i in "$@"; do
    URL=$(youtube-dl -q -g $i | awk 'NR%2==0')
    mplayer -novideo $URL
done;

