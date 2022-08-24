import numpy as np
import time
import utils
import balance as bal

is_balanced = bal.is_balanced

tries = 0
for logsize in  np.arange(7, 15):
    tries = 0
    while tries < 10:
        size = int(2**logsize)
        print("Running experiment with graph of size {}".format(size))
        A = utils.make_random_signed_graph(size, density=0.1, negatives_ratio=0.)
        nc = len(bal.find_connected_components(A))
        if nc > 1:
            print("Skip")
            continue # ignore cases with multiple connected components    
        
        start = time.time()
        print(is_balanced(A))
        end = time.time()
        print("Time: {}".format(end-start))
        with open("res_ours.csv", "a") as out:
            out.write("{},{}\n".format(size, end-start))

        
        start = time.time()
        print(bal.is_balanced_baseline(A))
        end = time.time()
        print("Baseline time: {}".format(end-start))
        with open("res_baseline.csv", "a") as out:
            out.write("{},{}\n".format(size, end-start))
        print()
        
        tries += 1
        
        
