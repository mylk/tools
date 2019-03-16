#!/bin/bash
for i in "$@"; do
    youtube-dl -q -o - $i | mplayer -novideo -really-quiet - 2>/dev/null 
done;

