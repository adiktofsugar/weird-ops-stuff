#!/bin/bash

filename=$1
if [ "$filename" = "" ];then
	echo "Enter a filename"
	exit 1
fi
if [ ! -e $filename ];then
	echo "$filename does not exist"
	exit 1;
fi

sed -i '.bak' -e 's/^\([	 ]*\)\([^:]*\):[ ]*/\1"\2": /g' $filename
rm $filename.bak
