#!/bin/bash
frequency=$1
modulation=fm
samplerate=170k
gain=50

rtl_fm -f $frequency -M $modulation -s $samplerate -g $gain - | play -r $samplerate -t raw -e s -b 16 -c 1 - -q &