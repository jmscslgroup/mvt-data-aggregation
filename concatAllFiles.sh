#!/bin/bash

if [ "$#" -lt 3 ]; then
	echo "Wrong number of args. Should pass lots of files, first one is output, the rest are inputs."
	exit
fi

SINGLEFILE=${1}
# all files except the first
FILES=${@:2}

# output the first line of the first input file as the new col headers
head -n 1 ${2} > ${SINGLEFILE}

# iterate over all the input files
for f in ${FILES}; do 
	echo "Processing file ${f}..." 
	# remove the columsn line, usually the first one, it will have Systime in it
	cat ${f} | grep -v "Systime" >> ${SINGLEFILE}
done
