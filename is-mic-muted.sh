#!/bin/bash

if [ $(amixer get Capture | grep '\[off\]' | wc -l) -gt 0 ]
then
    echo "Muted"
else
    echo "Not muted"
fi

