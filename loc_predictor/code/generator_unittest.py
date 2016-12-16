#! /usr/bin
import unittest
import json
import pandas as pd
from matrix_generator import *
from pandas.util.testing import assert_frame_equal

class TestMFactorization(unittest.TestCase):

	def setUp(self):
        	pass

	def test_get_read_buffer(self):
		read_buffer = file('test_unittest.py').read()
		self.assertEqual(get_read_buffer('test_unittest.py'), read_buffer)
	
	def test_read_json(self):
		path = '../ProcessedData/dummy/reviews.json'
		read_json = pd.read_json(open(path))
		assert_frame_equal(get_read_json(path), read_json)

	def test_concatenate_list(self):
		l1 = [1,2]
		l2 = [3,4]
		self.assertEqual(concatenate_list(l1, l2), l1 + l2)

	def test_concatenate_dataframe(self):
		path = '../ProcessedData/dummy/reviews.json'
                read_json = pd.read_json(open(path))
		read_json2 = pd.read_json(open(path))
		assert_frame_equal(concatenate_dataframe(read_json, read_json2), pd.concat([read_json, read_json2]))

	def test_write_matrix(self):
		matrix = [[1,2],[3,4]]
		path = '../ProcessedData/dummy/dummy_mtrix.json'
		self.assertEqual(write_matrix(matrix, path), None)

	def test_create_matrix(self):
		path = '../ProcessedData/dummy/'
		review_list = get_read_json(path+'reviews.json')
		user_list = get_read_buffer(path+'users.json').split()
		business_list = get_read_buffer(path+'businesses.json').split()
		print 'review_list, user_list, business_list', business_list, user_list
		print  business_list
		self.assertEqual(create_matrix(business_list, user_list, review_list), [[3]])
		

if __name__ == '__main__':
	unittest.main()
