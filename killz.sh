#!/bin/bash

PROC=$1

ps aux | grep $PROC | grep -v 'grep' | awk '{print($2)}' | xargs kill -9;
