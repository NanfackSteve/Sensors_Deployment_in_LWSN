#!/usr/bin/bash

for i in `seq 30 4000 100`
do
    ts=$( /usr/bin/time -f "%e" ./sensors_deploy.exe 50000 $i 1 0.4 0.5 < fich1.txt )
    echo "$i $ts" > ts.dat
done

#/usr/bin/time -f "%e" ./sensors_deploy.exe 50000 25000 1 0.4 0.5 < fich1.txt