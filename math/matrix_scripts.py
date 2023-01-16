import numpy as np

# example matrix
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
A

# sum over rows
####################
A.sum(axis=1)

# condition
######################

# test if sum over row is not 0
A.sum(axis=1) != 0
# as 1, else 0
np.where(A.sum(axis=1) != 0, 1, 0)

# if cell < 3, return 0, else 1
np.where(A < 3, 0, 1)

# if cell < 5, return 0, else if cell < 7, return 1, else 2
np.where(A < 5, 0, np.where(A < 7, 1, 2))

# element wise sum of 2 arrays
###################################
A = np.array([1, 2, 3])
B = np.array([4, 5, 6])

lsts = [A, B]
np.sum(lsts, axis=0)

# matrix add 1 more row
###################################
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
A

zeros = np.zeros(A.shape[1])
zeros
np.vstack((A, zeros))

np.vstack((A, np.array([10, 11, 12])))

# fill na with 0
###################################
B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]])
B
np.nan_to_num(B)

# reshape
###################################

# ratio over sum of rows
A / A.sum(axis=1).reshape(-1, 1)

# standardize over rows
A - A.mean(axis=1).reshape(-1, 1)

# normalize over rows
(A - A.mean(axis=1).reshape(-1, 1)) / A.std(axis=1).reshape(-1, 1)

# cumulative sum over rows
################################
A.cumsum(axis=1)

# cumulative sum over rows reversed
A[:, ::-1].cumsum(axis=1)[:, ::-1]

# reversed
###################
A[:, ::-1]


# normalize whole matrix
#############################
A_normalized = (A - A.mean()) / A.std()

# standard normal inverse
#############################
from scipy.stats import norm

norm.ppf(0.975)
norm.ppf(0.11)
A_row_pct = A / A.sum(axis=1).reshape(-1, 1)
norm.ppf(A_row_pct)

# diagonals
####################

# upper diagonal
np.triu(A, k=1)

# lower diagonal
np.tril(A, k=-1)

# the diagonal
np.diag(A)

# upper diagonal including the diagonal
np.triu(A, k=0)

# lower diagonal including the diagonal
np.tril(A, k=0)

# fill lower triangular matrix with diagonal with 1, else 0
np.tril(np.ones(A.shape), k=0)

np.where(np.tril(np.ones(A.shape), k=0) == 1, A, 0)

# fill lower triangular matrix with diagonal with True, else False
np.tril(np.ones(A.shape, dtype=bool), k=0)


# upper triangular matrix with diagonal,
# with lower triangular without diagonal filled with 100
A
np.triu(A, k=0) + np.tril(np.ones(A.shape), k=-1) * 100

# test a condition only on upper triangular matrix incl diagonal
np.triu(A, k=0) > 5

# conditions and diagonals
#########################

# test if matrix is monotonic increasing over columns
A = np.array(np.random.randint(0, 10, size=(5, 5)))
A
np.diff(A, axis=0)
np.all(np.diff(A, axis=0) >= 0)

# test if matrix is monotonic increasing over columns
# but only for upper triangular matrix incl diagonal
A
np.triu(A, k=0)
np.diff(np.triu(A, k=0), axis=0)
np.triu(np.diff(np.triu(A, k=0), axis=0), k=1)
np.all(np.triu(np.diff(np.triu(A, k=0), axis=0), k=1) >= 0)

A = np.array(range(25)).reshape(5, 5)
A
np.triu(np.diff(np.triu(A, k=0), axis=0), k=1)
np.all(np.triu(np.diff(np.triu(A, k=0), axis=0), k=1) >= 0)

# test if matrix is monotonic decreasing over columns
# but only for lower triangular matrix incl diagonal
A = np.array(range(25)).reshape(5, 5) * -1
A
np.tril(np.diff(np.tril(A, k=0), axis=0), k=0)
np.all(np.tril(np.diff(np.tril(A, k=0), axis=0), k=0) <= 0)

np.all(np.tril(np.diff(A), k=0) <= 0)


# test if matrix is symmetric
#############################
A = np.array(np.random.randint(0, 10, size=(5, 5)))
A
A.T
np.all(A == A.T)

# sum of list of matrices
################
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
C = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

lst = [A, B, C]

np.sum(lst, axis=0)
np.sum(lst, axis=1)

# division
###############
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

A / 2
A / np.array([1, 2, 3])
A / np.array([1, 2, 3]).reshape(-1, 1)


# split matrix into smaller matrices
####################################
# 10 by 10
A = np.array(range(100)).reshape(10, 10)
A

# split into 2 matrices
np.split(A, 2, axis=1)

# split into 5 matrices
np.split(A, 5, axis=1)

# split into matries of size n
A = np.array(range(100)).reshape(10, 10)
split_size = 4
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

matrix_size = A.shape[0]
split_points = list(range(split_size, matrix_size, split_size))
split_points
if len(split_points) < matrix_size:
    split_points.append(split_points[-1] + split_size)
split_points

for i, j in zip([0] + split_points, split_points):
    for k, l in zip([0] + split_points, split_points):
        print(i, j, k, l)
        print(labels[i:j], labels[k:l])
        print(A[i:j, k:l])

# matrix algebra
####################
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# matrix multiplication
A @ B

# matrix multiplication
np.dot(A, B)

# matrix inverse
np.linalg.inv(A)

# matrix determinant
np.linalg.det(A)

# matrix trace
np.trace(A)

# matrix transpose
A.T

# matrix rank
np.linalg.matrix_rank(A)

# matrix eigenvalues
np.linalg.eigvals(A)
