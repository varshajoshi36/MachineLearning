import unittest
import numpy.testing
from matrix_factorization import *
import numpy as np

class MyTest(unittest.TestCase):
	def test_matrix_factorization(self):
		matrix_input = [[3,2],[0,5]]
		matrix_output = [[3.,2.],[0.,5.]]
		np_matrix = np.matrix(matrix_input)
		P = np.random.rand(2,2) 
		Q = np.random.rand(2,2)        
		numpy.testing.assert_array_almost_equal(matrix_factorization(np_matrix,P,Q,1,5000, 0.02, 0.5), matrix_output)

	def test_values_bifurcate(self):
		pred_matrix = np.matrix([[3,2],[2,5]])
		input_matrix = np.matrix([[3,2],[2,5]])
		nonzero = np.nonzero(input_matrix)
		indices = [0,1,2,3]
		self.assertEqual(matrix_factorization_test(input_matrix, pred_matrix, indices, nonzero), 100)
     
if __name__ == '__main__':
    unittest.main()
