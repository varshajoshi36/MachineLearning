import numpy 
import pandas as pd
import pickle
import math
import numpy as np
import random

mfactorization_matrix_file = '../ProcessedData/montreal_urbana_matrix'
mfactorization_processed_matrix_file = '../ProcessedData/processed_montreal_urbana_matrix30'


with open(mfactorization_matrix_file,'rb') as f:
    np_matrix_orig = np.matrix(pickle.load(f))

np_matrix = np.matrix(np_matrix_orig)
nonzero = np.nonzero(np_matrix_orig)
test_indices = []

for i in range((nonzero[0].shape[1] * 30)/100):
	index = random.randrange(0, nonzero[0].shape[1])
	test_indices.append(index)
	np_matrix[nonzero[0].item(index), nonzero[1].item(index)] = 0

n = np_matrix.shape[0] #number of rows
M = np_matrix.shape[1] #number of columns
K = 18		       #latent features

P = numpy.random.rand(n,K) #Initial matrix 1
Q = numpy.random.rand(M,K) #Initia matrix 2

def matrix_factorization(R, P, Q, K, steps, alpha, beta):
    print steps, alpha, beta
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R.item(i,j) > 0:
                    eij = numpy.linalg.norm(R.item(i, j) - numpy.dot(P[i,:],Q[:,j]))
                    for k in xrange(K):
			P[i][k] = P[i][k] + alpha * (Q[k][j] * numpy.dot(P[i,:],Q[:,j])/pow(eij, 3) - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (P[i][K] * numpy.dot(P[i,:],Q[:,j])/pow(eij, 3) - beta * P[i][k])
        eR = numpy.dot(P,Q)
        e = 0
        e = numpy.linalg.norm(R - numpy.dot(P, Q))
	for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R.item(i, j) > 0:
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    return P, Q.T


nP, nQ=matrix_factorization(np_matrix, P, Q, K, 5000, 0.0002, 0.02)
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
print K
print "Same Values: ", same_count
print "Values differ by 1: ", diff_by_one_count
print "No of nonzero values: ", len(test_indices)
print "per cent ", ((same_count)/len(test_indices))*100
