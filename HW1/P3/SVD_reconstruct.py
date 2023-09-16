import numpy as np
from scipy.linalg import svd
# define a matrix
A = np.array([
    [1, 2], 
    [3, 8], 
    [5, 1]
])

# Perform SVD
U, s, VT = svd(A)

# create m x n Sigma matrix
Sigma = np.zeros((A.shape[0], A.shape[1]))
# populate Sigma with n x n diagonal matrix
Sigma[:A.shape[1], :A.shape[1]] = np.diag(s)
# reconstruct matrix
B = U.dot(Sigma.dot(VT))

print("Original matrix A: \n{}".format(A))
print("Reconstruct matrix B: \n{}".format(B))