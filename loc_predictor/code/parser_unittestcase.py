import unittest
import numpy.testing
from parser import *
import numpy
import pandas as pd

class MyTest(unittest.TestCase):

    def test_get_required_features(self):
        business_input_file='../ProcessedData/dummy/businesses.json'
        review_input_file='../yelp_data/yelp_academic_dataset_review.json'
        users_output_file='../ProcessedData/dummy/users.json'
        reviews_output_file='../ProcessedData/dummy/reviews.json'
        self.assertEqual(get_required_features(business_input_file, review_input_file, users_output_file, reviews_output_file),13)
if __name__ == '__main__':
    unittest.main()

