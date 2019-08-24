from Crypto.Random import random
import gmpy2 as gm
import numpy as np
def generateAPrime(scale):
    while True:
        x = random.getrandbits(scale)
        if gm.is_prime(x):
            return x

def generateNs(N, scale):
    M = np.zeros((N, N))
    M = M.tolist()
    for i in range(N):
        for j in range(i + 1):
            M[i][j] = generateAPrime(scale / 4)
            M[j][i] = M[i][j]
    ns = [1] * N
    for i in range(N):
        for j in range(N):
            ns[i] = ns[i] * M[i][j]
    return ns

