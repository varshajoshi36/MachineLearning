#!/bin/bash

if [ $# -lt "3" ]
then
	echo "Usage: $0 <path-to-yelp-business-data-json-file> \"<name-of-the-city>\" <path-to-output-file>"
	exit 1
fi

grep "\"city\": \"$2\"" $1 | cut -f2 -d " " | tr -d '"' | tr -d ',' | sort -u > "$3"
exit 0
