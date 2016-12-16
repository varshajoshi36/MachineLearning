import numpy 
import pandas as pd
import pickle
import math
import numpy as np
import random
import sys

Usage = "python matrix_factorization.py steps alpha beta"
total = len(sys.argv)
if total < 3:
        print(Usage)
        sys.exit("Incorrect Usage")

steps = int(sys.argv[1])
alpha = float(sys.argv[2])
beta = float(sys.argv[3])
K = int(sys.argv[4])


mfactorization_matrix_file = '../ProcessedData/montreal_urbana_matrix'
mfactorization_processed_matrix_file = '../ProcessedData/processed_montreal_urbana_matrix30'


'''with open(mfactorization_matrix_file,'rb') as f:
    np_matrix_orig = np.matrix(pickle.load(f))'''

np_matrix_orig = np.random.rand(100,50) * 5
np_matrix_orig = np.round(np_matrix_orig)
np_matrix_orig = np.matrix(np_matrix_orig)

for i in range(10000):
	x, y = random.randrange(0, 100), random.randrange(0, 50)
	np_matrix_orig[x, y] = 0

print np_matrix_orig

np_matrix = np.matrix(np_matrix_orig)
nonzero = np.nonzero(np_matrix_orig)
test_indices = []
print 'nonzero', nonzero[0].shape[1]

for i in range((nonzero[0].shape[1] * 30)/100):
	index = random.randrange(0, nonzero[0].shape[1])
	test_indices.append(index)
	np_matrix[nonzero[0].item(index), nonzero[1].item(index)] = 0

n = np_matrix.shape[0] #number of rows
M = np_matrix.shape[1] #number of columns
#K = np.linalg.matrix_rank(np_matrix)       #latent features
#K = 30
P = numpy.random.rand(n,K) #Initial matrix 1
Q = numpy.random.rand(M,K) #Initia matrix 2

#P = np.random.rand(n, K) * 5
#Q = np.random.rand(M, K) * 5

def vec_matrix_factorization(R, P, Q, K, steps, alpha, beta):
	print steps, alpha, beta
	Q = Q.T
	print 'P, Q', P.shape, Q.shape
	for step in xrange(steps):
		e = numpy.zeros((len(R), len(R[0])))
		eij = numpy.matrix(R - numpy.dot(P, Q))
		Q = Q + alpha * (2 * numpy.dot(P.T, eij) - beta * Q)
		P = P + alpha * (2 * numpy.dot(eij, Q.T) - beta * P)
		e = 0
		print 'P prime, Q prime', P.shape, Q.shape
        	for i in xrange(len(R)):
	            for j in xrange(len(R[i])):
        	        if R.item(i, j) > 0:
                	    e = e + pow(R.item(i, j) - numpy.dot(P[i,:],Q[:,j]), 2)
	                    for k in xrange(K):
				print 'fgdjfgdgfdj', P[i][k], Q[k][j]
        	                e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
	        if e < 0.001:
        	        print "Obtained error < 0.001, exiting.."
                	break
	return P, Q.T


def matrix_factorization(R, P, Q, K, steps, alpha, beta):
    print steps, alpha, beta
    Q = Q.T
    
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R.item(i,j) >= 0:
	                eij = R.item(i, j) - numpy.dot(P[i,:],Q[:,j])
        	        for k in xrange(K):
				P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        	Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R.item(i, j) > 0:
                    e = e + pow(R.item(i, j) - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
       	    	print "Obtained error < 0.001, exiting.."
		break
    return P, Q.T


nP, nQ = vec_matrix_factorization(np_matrix, P, Q, K, steps, alpha, beta)
nR = numpy.dot(nP, nQ.T)
#nI = nR.astype(int)
nI = np.round(nR)

with open(mfactorization_processed_matrix_file, 'w') as op_matr:
	nI.dump(op_matr)

print nI.shape
print np_matrix.shape

same_count = 0
diff_by_one_count = 0

for i in test_indices:
	diff = math.fabs(np_matrix_orig.item(nonzero[0].item(i), nonzero[1].item(i)) - nI.item(nonzero[0].item(i), nonzero[1].item(i)))
	if(diff == 0):
		same_count += 1
	if(diff == 1):
		diff_by_one_count += 1
print nI
print K
print "Same Values: ", same_count
print "Values differ by 1: ", diff_by_one_count
print "No of nonzero values: ", len(test_indices)
print "per cent ", ((same_count)/len(test_indices))*100
