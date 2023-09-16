import numpy as np
from scipy.linalg import eig


# Input matrix W
W = np.array([
    [20, 14, 0, 0],
    [14, 10, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

# Perform egienvalue decomposition
eigenvalues, eigenvectors = eig(W)

print("Eigenvalues: \n{}".format(eigenvalues))
print("Eigenvectors: \n{}".format(eigenvectors))