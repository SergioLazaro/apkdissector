#!/bin/bash

if [ -z $1 ];then
    echo "Invalid parameter"
elif [ ! -d $1 ];then
    echo "Parameter should be a directory"
else
    for elem in `ls $1`;do
        echo "main.py -v 5.1.1 -i $1 -o /home/sid/android/malware/analysis"
        #python main.py -v "5.1.1" -i "$1" -o "/home/sid/android/malware/analysis"
    done
fi