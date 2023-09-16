# Find V matrix in SVD formula: A = USV^T

import numpy as np
from scipy.linalg import eig


# Input matrix
A = np.array([
    [3, 2, 2],
    [2, 3, -2],
])

# Compute A^T.A
W = A.T.dot(A)

# Perform egienvalue decomposition
eigenvalues, eigenvectors = eig(W)

# Square egienvalues to get singular values
singular_values = np.sqrt(eigenvalues)

print("The matrix W: \n{}".format(W))
print("Eigenvalues of A^T.A: \n{}".format(eigenvalues))

print("(Right singular vectors V) Eigenvectors: \n{}".format(eigenvectors))
print("Singular values S of A: \n{}".format(singular_values))

