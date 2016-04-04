#!/bin/bash

PWD=`pwd`
echo $PWD
echo $1
if [ -z $1 ];then
    echo "Invalid parameter"
elif [ ! -d $1 ];then
    echo "Parameter should be a directory"
else
    for elem in `ls $1`;do
        if [ -f $elem ]; then
            python /home/sid/android/apkdissector/dissector/main.py -v 5.1.1 -i "$PWD/$1" -o /tmp/asd
        fi
    done
fi