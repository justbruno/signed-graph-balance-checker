import numpy as np
import time
import utils
import balance as bal

is_balanced = bal.is_balanced_new

tries = 0
while tries < 10:
    A = utils.make_random_signed_graph(3000, density=0.1, negatives_ratio=0.1)
    nc = len(bal.find_connected_components(A))
    if nc > 1:
        print("Skip")
        continue # ignore cases with multiple connected components    

    start = time.time()
    print(is_balanced(A))
    end = time.time()
    print("Time: {}".format(end-start))
    
    start = time.time()
    print(bal.is_balanced_baseline(A))
    end = time.time()
    print("Baseline time: {}".format(end-start))
    print()
    
    tries += 1

