#! /usr/bin/python

import json
import pickle
import pandas as pd
import pprint
import sys
from time import gmtime, strftime

def get_read_buffer(path):
	name = file(path).read()
	return name

def get_read_json(path):
	json_list = pd.read_json(open(path))
	return json_list
	
def concatenate_list(list1, list2):
	return list1 + list2

def concatenate_dataframe(df1, df2):
	reviews = [df1, df2]
	return pd.concat(reviews)

def create_matrix(business_list, user_list, review_list):
	review_matrix = []
	for business in business_list:
		b_list = []
		b_list.append(business)
		business_df = review_list[review_list["business_id"].isin(b_list)]
		business_list = []
		for user in user_list:
			u_list =[]
			u_list.append(user)
			if business_df.empty:
				business_list.append(0)				#add 0 if no review
			else:
				user_df = business_df[business_df["user_id"].isin(u_list)]
				if user_df.empty:
					business_list.append(0)
				else:
					business_list.append(int(user_df.iloc[0].get("stars")))	
		review_matrix.append(business_list)
	return review_matrix

def write_matrix(review_matrix, matrix_path):
	with open(matrix_path, 'w') as output_file:
		pickle.dump(review_matrix, output_file)


#load values from sys.argv
Usage = "python matrix_generator.py single/double city1 city2 output_path output_file "
total = len(sys.argv)

if total < 5:
        print(Usage)
	single_double = 'single'
        city1 = 'dummy'
        city2 = 'dummy'
        path =  '../ProcessedData'
        matrix_path = '../ProcessedData/dummy/dummy'
else:
	single_double = sys.argv[1]				#sys.argv[1]			#'double'
	city1 = sys.argv[2]					#sys.argv[2]			#'urbana'
	city2 = sys.argv[3]					#sys.argv[3]			#'montreal'
	path = 	sys.argv[4]					#sys.argv[4]			#'../ProcessedData'
	matrix_path = sys.argv[5]				#sys.argv[5]			#'../ProcessedData/montreal_urbana_matrix'


#declare lists required
business_list = []
user_list =[]
review_list = []

#read data from files
city_user_file1 = get_read_buffer(path+'/'+city1+'/'+'users.json')
city_business_file1 = get_read_buffer(path+'/'+city1+'/'+'businesses.json')

user_list1 = city_user_file1.split('\n')
business_list1 = city_business_file1.split('\n')
review_list1 = get_read_json(path+'/'+city1+'/'+'reviews.json')

if single_double == "single":
	user_list = user_list1
	business_list = business_list1
	review_list =review_list1

if single_double == "double":
	city_user_file2 = get_read_buffer(path+'/'+city2+'/'+'users.json')
	city_business_file2 = get_read_buffer(path+'/'+city2+'/'+'businesses.json')
	
	review_list2 = get_read_json(path+'/'+city2+'/'+'reviews.json')
	business_list2 = city_business_file2.split('\n')
	user_list2 = city_user_file2.split('\n')
	
	user_list = concatenate_list(user_list1, user_list2)
        business_list = concatenate_list(business_list1, business_list2)
        review_list = concatenate_dataframe(review_list1, review_list2)

print "Reading done, creating matrix",strftime("%a, %d %b %Y %H:%M:%S +0000")

review_matrix = create_matrix(business_list, user_list, review_list)
write_matrix(review_matrix, matrix_path)

print "Matrix creation done",strftime("%a, %d %b %Y %H:%M:%S +0000")
