import numpy as np
import itertools as it

def make_random_signed_graph(N, density=0.9, negatives_ratio=0.5):
    A = np.zeros((N,N))
    for e in it.combinations(range(N),2):
        if np.random.rand() < density:
            w = 1
            if np.random.rand() < negatives_ratio:
                w = -1
            A[e[0],e[1]] = A[e[1],e[0]] = weight=w
    return A


def compute_laplacian(A):
    N = A.shape[0]
    At = -A
    for i in range(N):        
        x1 = A[i,:].T                
        At[i,i] = x1.T.dot(x1)
    return At

def compute_signed_laplacian(A):
    N = A.shape[0]
    At = -A
    for i in range(N):        
        x1 = A[i,:].T                
        At[i,i] = np.sum(np.abs(x1))
    return At
