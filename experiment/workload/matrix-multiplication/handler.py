import numpy as np
import time as t

np.random.seed(1)

def handle(req):
    
    mainStartTime = t.time()

    """This function will multiply two 2000 * 2000 matrices """
    m = 200
    n = 1

    # Initialzing the two square matrices
    matrix_1 = np.random.rand(m, m)
    matrix_2 = np.random.rand(m, m)

    # multiply the two matrices using np.matmul
    startTime = t.time()
    for i in range(n):
        result = np.matmul(matrix_1, matrix_2)
    endTime = t.time()

    # saving the result to the text file
    np.savetxt('result_matrix.txt', result, fmt='%.4f', delimiter=' ', header = 'The result of matrix multiplication is:')

    mainEndTime = t.time()

    elaspedFunTime = "Time taken to execute the entire function is:" + str(mainEndTime-mainStartTime) + " seconds"

    return elaspedFunTime