#!/bin/sh

format_file(){
    paste $1 $2 > tmp.txt
    sed 's/\t/ /g' tmp.txt > formated.txt
    cut -d ' ' -f 1,2,4 formated.txt > parallel_vs_sequential.dat

    rm tmp.txt formated.txt
}

format_file $1 $2
