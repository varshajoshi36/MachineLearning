#!/usr/bin/python
import pandas as pd
import json
import sys, getopt
from pprint import pprint

Usage = "python parser.py <business-ids-file> <yelp-review-file> <user-ids-output-file> <required-features-output-file>"
total = len(sys.argv)

if total==4:
	business_input_file = sys.argv[1]
	review_input_file = sys.argv[2]
	users_output_file = sys.argv[3]
	reviews_output_file = sys.argv[4]

def get_required_features ( business_input_file, review_input_file, users_output_file, reviews_output_file ):
	#Read the business IDs and store them in a dataFrame
	b_ids = []
	business_file = file(business_input_file).read()
	b_ids = business_file.split('\n')
	business_df = pd.DataFrame(b_ids)

	pprint ("Done reading")
	#Features being used from the reviews
	good_columns = [
		"business_id",
		"user_id",
		"stars"
	]
	users = []
	review_data = []

	#Read all the reviews into a list
	with open(review_input_file) as data_file:
		for new_line in data_file:
			review_data.append(json.loads(new_line))

	#Extract the required columns from the reviews
	review_features = pd.DataFrame(review_data, columns=good_columns)
	with open(reviews_output_file, 'w') as json_buff_file:
		review_features[review_features["business_id"].isin(b_ids)].to_json(json_buff_file)

	#For every business id get the distinct users who have rated for it and write into a file
	users = review_features[review_features["business_id"].isin(b_ids)].get("user_id")
	users = list(set(users))
	with open(users_output_file, 'w') as buff_file:
		for item in users:
			buff_file.write(item.split(',')[0]+'\n')

	return len (users)
if total == 4:
	get_required_features(business_input_file, review_input_file, users_output_file, reviews_output_file)
