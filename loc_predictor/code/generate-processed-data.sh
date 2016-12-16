#!/bin/bash

#Running this script should generate all the pre-requisite files needed for matrix generation
#and factorization.
#The script takes required inputs and provides list of businesses, their ratings,
#and the list of users who have provided the ratings for every city in their
#respective destination directores.

if [ $# -lt "6" ]
then
       echo "Usage: $0 <cities-file> <path-to-extract-script> <path-to-yelp-business-data-json-file> <path-to-data-dir> <parser-script> <path-to-yelp-review-file>"
       exit 1
fi

while read line
do
       echo $line
       mkdir -p "$4/$line"
       $2 $3 "$line" "$4/$line/businesses.json"
       python $5 "$4/$line/businesses.json" $6 "$4/$line/users.json" "$4/$line/reviews.json"
done < $1
exit 0
