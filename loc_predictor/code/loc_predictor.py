#! /usr/bin/python
import pickle
import sys
import numpy as np
data_path = '../ProcessedData/'

def get_read_buffer(path):
        name = file(path).read()
        return name

def get_users(path_city):
	return get_read_buffer(path_city + 'users.json').split('\n')

def get_business(path_city):
	return get_read_buffer(path_city + 'businesses.json').split('\n')

#calculate for city
def predict_profitable_location():
	with open(data_path + city1+'_profittable_businesses.json', 'w') as profitable_b:
		for i in range(business1_count):
			business_id = business1[i]
			user_ratings = ip_matrix.item(i)
			count = 0
			for j in range(first_pivote[0], first_pivote[1]):
				#print ip_matrix.item(i, j)
				if 5*ip_matrix.item(i, j)/10 > 2:
					count += 1
			if count > users2_count/2:
				profitable_b.write(business_id+'\n')

	with open(data_path + city2+'_profittable_businesses.json', 'w') as profitable_b:
		for i in range(business1_count, business1_count + business2_count -1):
			business_id = business2[business1_count - i]
			user_ratings = ip_matrix.item(i)
			count = 0
			for j in range(second_pivote[0], second_pivote[1]):
				print ip_matrix.item(i, j)
				if 5*ip_matrix.item(i, j)/10 > 2:
					count += 1
			if count > users1_count/2:
				profitable_b.write(business_id+'\n')


Usage = "python loc_predictor.py <city1> <city2> <matrix_file>"

command_arguments = len(sys.argv)

if command_arguments < 3:
	print Usage
	city1 = 'dummy'
	city2 = 'dummy'
	matrix_file = '../ProcessedData/dummy/dummy_matrix'
else:
	city1 = sys.argv[1]
	city2 = sys.argv[2]
	matrix_file = '../ProcessedData/'+sys.argv[3]

path_city1 = data_path + city1 + '/'
path_city2 = data_path + city2 + '/'

business1 = get_business(path_city1)
business2 = get_business(path_city2)
business1_count = len(business1)
business2_count = len(business2)

users1 = get_users(path_city1)
users2 = get_users(path_city2)
users1_count = len(users1)
users2_count = len(users2)

with open(data_path + matrix_file,'rb') as f:
        ip_matrix = np.matrix(pickle.load(f))

print ip_matrix

first_pivote = (users1_count, users1_count + users2_count -1)
second_pivote = (0, users1_count - 1)

predict_profitable_location()
