import numpy as np
import time

def handle(req):
    # Create a large random array
    start_time = time.time()
    arr = np.random.rand(20000000)
    
    # sorted_arr = np.sort(arr)
    end_time = time.time()
    
    # Calculate and print the time taken
    elapsed_time = end_time - start_time

    print(f"Time taken to execute the entire function is: {elapsed_time:.4f} seconds")
    return elapsed_time