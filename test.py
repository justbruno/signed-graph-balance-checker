import numpy as np
import itertools as it
import balance as bal
import time
import utils

is_balanced = bal.is_balanced

def run_basic_test(A, balanced, name):
    print()
    print("="*50)
    print(name)    
    if is_balanced(A) == balanced:
        print("OK")
    else:
        print("Failed")
    print("-"*50)


def run_spectral_test(A, thr=1e-12):
    L = utils.compute_signed_laplacian(A)
    eigenvalues = np.linalg.eigh(L)[0]
    spectral_balance = np.min(np.abs(eigenvalues)) <= thr

    if is_balanced(A) == spectral_balance:
        return True
    else:
        return False
        np.save("failed_test_matrix_{}".format(time.time()), A)


    
print("Running tests:")
##################################################
A = np.array([[0,1,1], [1,0,1], [1,1,0]])
run_basic_test(A, True, "Triad all positive")

##################################################
A = np.array([[0,1,1], [1,0,-1], [1,-1,0]])
run_basic_test(A, False, "Triad one negative")

##################################################
A = np.array([[0,-1,-1], [-1,0,-1], [-1,-1,0]])
run_basic_test(A, False, "Triad all negative")

##################################################
A = np.array([[0,-1,-1], [-1,0,1], [-1,1,0]])
run_basic_test(A, True, "Triad one positive")
    
##################################################
# Spectral tests
tries = 0
print("Running spectral tests...")
results = []
while tries < 100:
    A = utils.make_random_signed_graph(100, density=0.75, negatives_ratio=0.5)
    nc = len(bal.find_connected_components(A))
    if nc > 1:
        print("Skip")
        continue # ignore cases with multiple connected components    
    results.append(run_spectral_test(A))
    tries += 1
print("All spectral tests OK: {}".format(np.all(results)))
print("Check output files for failed tests.")

