import numpy as np
from scipy.linalg import svd


A = np.array([
    [3, 2, 2],
    [2, 3, -2],
])

U, S, Vt = svd(A)
a = np.zeros(A.shape)
np.fill_diagonal(a, S)
S = a

print("Original matrix A: \n{}".format(A))
print("Left singular vectors: \n{}".format(U))
print("Singular values: \n{}".format(S))
print("Right singular vectors: \n{}".format(Vt))

B = (U.dot(S)).dot(Vt)
print("Reconstruct matrix: \n{}".format(B))