import numpy as np
from scipy import sparse
import queue

def is_balanced(A):
    """
    Checks if a connected undirected signed graph is balanced. 
    Input: 
    A: The adjacency matrix of the graph, encoding positive (resp. negative) edges as 1 (resp. -1).
    """

    N = A.shape[0]
    if N < 3:
        return True

    first = np.argmax(np.sum(np.abs(A), axis=0)) # Start by the highest-degree vertex.
    switch = A[first, :]

    # neg (resp. pos) are indicator vectors for the two sides of the balanced partition.
    # We iniialise these vectors so they are active where negative (resp. positive) neighbours of the current vertex are.
    # If and only if the graph is balanced, these vectors are orthogonal upon termination.
    s = switch<=-1
    neg = np.zeros(N)
    negi = sparse.find(s)[1]
    neg[negi]=1

    s = switch>=1
    pos = np.zeros(N)
    posi = sparse.find(s)[1]
    pos[posi]=1

    oldpos = np.copy(pos)
    oldneg = np.copy(neg)
    posi = sparse.find(pos)[1]
    negi = sparse.find(neg)[1]
    
    finished = False    
    while not finished:
        # Here we take a BFS approach to test the consistency between the indicator vectors and the edge signs.
        # Positive neighbours of vertices in the positive side should be on the positive side, and so on.
        # Even though there is redundancy in some computations, the use of sparse matrices and vectors makes it efficient.
        posi = sparse.find(pos)[1]
        rows,cols=sparse.find(A[posi, :]>=1)[:2]
        pos = np.where(np.sum(sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=A.shape), axis=0) + pos, 1, 0)
        rows,cols=sparse.find(A[posi, :]<=-1)[:2]
        neg = np.where(np.sum(sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=A.shape), axis=0) + neg, 1, 0)

        negi = sparse.find(neg)[1]
        rows,cols=sparse.find(A[negi, :]>=1)[:2]
        neg = np.where(np.sum(sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=A.shape), axis=0) + neg, 1, 0)
        rows,cols=sparse.find(A[negi, :]<=-1)[:2]
        pos = np.where(np.sum(sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=A.shape), axis=0) + pos, 1, 0)

        # np.where returns a tuple. We only need the first item.
        pos = pos[0]
        neg = neg[0]

        # If and only if we find an inconsistent vertex, these vectors will not be orthogonal.
        balanced = pos.T.dot(neg) == 0
        switch = pos-neg
        finished = switch.T.dot(switch)==A.shape[0]
        if not balanced:
            break
        
    return balanced



def is_balanced_baseline(A):
    """
    Checks if a connected undirected signed graph is balanced. 
    Input: 
    A: The adjacency matrix of the graph, encoding positive (resp. negative) edges as 1 (resp. -1).
    """

    N = A.shape[0]
    if N < 3:
        return True

    visited = []
    partition = np.zeros(N)
    
    pending = queue.Queue()
    first = np.argmax(np.sum(np.abs(A), axis=0)) # Start by the highest-degree vertex.
    indicator = A[first, :]
    partition += indicator

    done = False
    # If we make it out of this loop, the graph is balanced. We break it if we find a discrepancy.
    while not done:
        
        for i in np.where(indicator)[0]:
            pending.put(i)

        i = pending.get()
        if i in visited:
            continue            
        visited.append(i)
        
        indicator = A[i,:] * partition[i]
        
        if -1 in (indicator * partition):
            return False
        else:
            partition = partition + indicator
            partition[partition <= -1] = -1
            partition[partition >= 1] = 1

        done = len(visited) == N

    return True



def find_connected_components(A):
    Ab = np.abs(A)
    A = Ab.copy()
    all_indices = np.arange(A.shape[0])
    remaining_indices = np.arange(A.shape[0])
    removed_indices = []
    components = []

    while (A.shape[0] > 0):
        # Start with the neighbours of the max-degree vertex
        maxdeg = np.argmax(np.sum(A, axis=0))
        component = np.hstack([[maxdeg],np.nonzero(A[maxdeg,:])[0]])
        # BFS
        prelen = 0
        while len(component) > prelen:
            prelen = len(component)
            B = np.sum(A[component,:], axis=0)
            component = np.unique(np.hstack([component, np.nonzero(B)[0]]))
        components.append(remaining_indices[component])
        remaining_indices = np.delete(remaining_indices, component)
        A=Ab[remaining_indices,:][:,remaining_indices]
    return components


