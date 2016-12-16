#! /bin/bash

data_path='../ProcessedData/'
city1=''
city2=''
yelp_reviews_file='yelp_academic_dataset_review.json'
businesses.json='businesses.json'
matrix='matrix'
processed='processed'

python matrix_generator.py "double" $city1 $city2 $data_path $city1+'_'+$city2+'_'+$matrix
python matrix_factorization.py $city1+'_'+$city2+'_'+$matrix $processed+'_'+$city1+'_'+$city2+'_'+$matrix
python loc_predictor.py $city1 $city2 $processed+'_'+$city1+'_'+$city2+'_'+$matrix

