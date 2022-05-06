#!/usr/bin/bash

TIMEFORMAT=%R

for i in `seq 30 100 4000`
do
    ts=$( time ./sensors_deploy.exe 10000 $i 1 0.4 0.5 < fich1.txt )
    echo -e "$ts" > ts.dat
    echo "$i" >> i.dat
    
done

#/usr/bin/time -f "%e" ./sensors_deploy.exe 50000 25000 1 0.4 0.5 < fich1.txt