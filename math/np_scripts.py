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
