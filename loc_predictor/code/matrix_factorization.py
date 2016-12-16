import numpy 
import pandas as pd
import pickle
import math
import numpy as np
import random
import sys

def matrix_factorization(training_data, matrix1, matrix2, latent_features, steps, alpha, beta):
    matrix2 = matrix2.T
    for step in xrange(steps):
        for i in xrange(len(training_data)):
            for j in xrange(len(training_data[i])):
                if training_data.item(i,j) > 0:
                    eij = training_data.item(i,j) - numpy.dot(matrix1[i,:], matrix2[:,j])
                    for k in xrange(latent_features):
                        matrix1[i][k] = matrix1[i][k] + alpha * (2 * eij * matrix2[k][j] - beta * matrix1[i][k])
                        matrix2[k][j] = matrix2[k][j] + alpha * (2 * eij * matrix1[i][k] - beta * matrix2[k][j])
        e = 0
        for i in xrange(len(training_data)):
            for j in xrange(len(training_data[i])):
                if training_data.item(i,j) > 0:
                    e = e + pow(training_data.item(i,j) - numpy.dot(matrix1[i,:],matrix2[:,j]), 2)
                    for k in xrange(latent_features):
                        e = e + (beta/2) * (pow(matrix1[i][k],2) + pow(matrix2[k][j],2))
        if e < 0.001:
            break
    pred_matrix = numpy.dot(matrix1, matrix2)
    return np.round(pred_matrix)

def matrix_factorization_test(input_matrix, pred_matrix, test_indices, nonzero): 
    same_count = 0
    diff_by_one_count = 0
    for i in test_indices:
		diff = math.fabs(input_matrix.item(nonzero[0].item(i), nonzero[1].item(i)) - pred_matrix.item(nonzero[0].item(i), nonzero[1].item(i)))
		if(diff == 0):
			same_count += 1
		if(diff == 1):
			diff_by_one_count += 1
    print "Same Values: ", same_count
    print "Values differ by 1: ", diff_by_one_count
    print "No of nonzero values: ", len(test_indices)
    return (same_count+diff_by_one_count) * 100/len(test_indices)


Usage = "python matrix-factorization.py <input_matrix_file_name> <output_file_name>"
command_arguments = len(sys.argv)

if command_arguments < 2:
    input_matrix_file = '../ProcessedData/dummy/dummy_matrix'
    output_matrix_file = '../ProcessedData'
else:
    input_matrix_file = sys.argv[1]
    output_matrix_file = sys.argv[2]
    
with open(input_matrix_file,'rb') as f:
        input_matrix = np.matrix(pickle.load(f))

latent_features = 18
steps = 50000
alpha = 0.0002
beta = 0.5

training_matrix = np.matrix(input_matrix)
nonzero = np.nonzero(input_matrix)
test_indices = []

for i in range((nonzero[0].shape[1] * 30)/100):
        index = random.randrange(0, nonzero[0].shape[1])
        test_indices.append(index)
        training_matrix[nonzero[0].item(index), nonzero[1].item(index)] = 0

n = training_matrix.shape[0] #number of rows
m = training_matrix.shape[1] #number of columns

matrix1 = numpy.random.rand(n, latent_features) #Initial matrix 1
matrix2 = numpy.random.rand(m, latent_features) #Initia matrix 2

if command_arguments == 3:
    pred_matrix = matrix_factorization(training_matrix, matrix1, matrix2, latent_features, steps, alpha, beta)
    with open(output_matrix_file, 'w') as op_matr:
        pred_matrix.dump(op_matr)
    matrix_factorization_test(input_matrix, pred_matrix, test_indices, nonzero)
