# Find U matrix in SVD formula: A = USV^T

import numpy as np
from scipy.linalg import eig


# Input matrix
A = np.array([
    [3, 2, 2],
    [2, 3, -2],
])

# Compute A.A^T
W = A.dot(A.T)

# Perform egienvalue decomposition
eigenvalues, eigenvectors = eig(W)

# Square egienvalues to get singular values
singular_values = np.sqrt(eigenvalues)

print("The matrix W: \n{}".format(W))
print("Eigenvalues of AA^T: \n{}".format(eigenvalues))

print("(Left singular vectors U) Eigenvectors: \n{}".format(eigenvectors))
print("Singular values S of A: \n{}".format(singular_values))

