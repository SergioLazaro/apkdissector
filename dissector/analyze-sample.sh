#!/bin/bash

PWD=`pwd`
if [ -z $1 ];then
    echo "Invalid parameter"
elif [ ! -d $1 ];then
    echo "Parameter should be a directory"
else
    for elem in `ls $1`;do
        if [ -f $elem ]; then
            python /home/sid/android/apkdissector/dissector/main.py -v 5.1.1 -i "$PWD/$1" -o /tmp/asd
        fi
        #python main.py -v "5.1.1" -i "$1" -o "/home/sid/android/malware/analysis"
    done
fi