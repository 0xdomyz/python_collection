import numpy as np

# example matrix
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
A

# sum over rows
A.sum(axis=1)

# ratio over sum of rows
A / A.sum(axis=1).reshape(-1, 1)

# standardize over rows
A - A.mean(axis=1).reshape(-1, 1)

# normalize over rows
(A - A.mean(axis=1).reshape(-1, 1)) / A.std(axis=1).reshape(-1, 1)

# cumulative sum over rows
A.cumsum(axis=1)

# reversed
A[:, ::-1]

# cumulative sum over rows reversed
A[:, ::-1].cumsum(axis=1)[:, ::-1]

# if cell < 3, return 0, else 1
np.where(A < 3, 0, 1)

# if cell < 5, return 0, else if cell < 7, return 1, else 2
np.where(A < 5, 0, np.where(A < 7, 1, 2))

# normalize whole matrix
A_normalized = (A - A.mean()) / A.std()

# standard normal inverse
from scipy.stats import norm

norm.ppf(0.975)
norm.ppf(0.11)
A_row_pct = A / A.sum(axis=1).reshape(-1, 1)
norm.ppf(A_row_pct)

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
A = np.array(np.random.randint(0, 10, size=(5, 5)))
A
A.T
np.all(A == A.T)
