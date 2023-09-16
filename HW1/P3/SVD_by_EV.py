import numpy as np
from scipy.linalg import eig


# Input matrix A
A = np.array([
    [3, 2, 2],
    [2, 3, -2],
])

# Get the Left singular vectors U
## Compute W = A.A^T
W = A.dot(A.T)

## Call eig function to get eigenvalues, eigenvector of W
eigvalsW, eigvecsW = eig(W, left=True, right=False)

## Sort eigvalsW, eigvecsW desceading order
eigvalsW_copy = eigvalsW.copy()
eigvecsW_copy = eigvecsW.copy()
sorted_indices = np.argsort(-eigvalsW)
print("sorted_indices: ", sorted_indices)
eigvalsW = np.array([eigvalsW_copy[sorted_indices[i]] for i in range(len(sorted_indices))])
eigvecsW = np.array([eigvecsW_copy[sorted_indices[i]] for i in range(len(sorted_indices))])

## Assign U by eigvecsW, and square root eigvalsW to get singular values of A, the convert it into diangonal matrix
U = eigvecsW
sigvals = np.sqrt(eigvalsW)
S = np.zeros(A.shape)
np.fill_diagonal(S, sigvals)

# Get the Right singular vectors V
## Compute W = A^T.T
Z = (A.T).dot(A)
## Call eig function to get engienvalues, eigenvector of Z
eigvalsZ, eigvecsZ = eig(Z)

## Assign V by eigvecsZ
V = eigvecsZ

## Sort eigvalsZ, eigvecsZ desceading order
eigvalsZ_copy = eigvalsZ.copy()
eigvecsZ_copy = eigvecsZ.copy()
sorted_indices = np.argsort(-eigvalsZ)
print("sorted_indices: ", sorted_indices)
eigvalsZ = np.array([eigvalsZ_copy[sorted_indices[i]] for i in range(len(sorted_indices))])
eigvecsZ = np.array([eigvecsZ_copy[sorted_indices[i]] for i in range(len(sorted_indices))])


# Show result
print("The input matrix: \n{}".format(A))
print("The U (left singular vectors) matrix: \n{}".format(U))
print("The S (singular values) matrix: \n{}".format(S))
print("The V (right singular vectors) matrix: \n{}".format(V))

# Reconstruct A = USV^T
B = (U.dot(S)).dot(V.T)
print("Reconstruct matrix B from U, S, V: \n{}".format(B))