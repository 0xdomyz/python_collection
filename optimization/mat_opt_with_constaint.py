# use mystic to minimize MSE of a matrix in relation to list of matrixes
########################################
import matplotlib.pyplot as plt
import numpy as np

# list of 5 by 5 matrixes
mats = [np.random.randint(0, 10, size=(5, 5)) for i in range(5)]
mats

# function to be minimized
def objective(x: np.ndarray):
    """
    Examples::

        objective(x = np.array(range(25)))
        objective(x = np.array(range(1,26)))
    """
    mat = np.array(x).reshape(5, 5)
    return np.mean([np.mean((mat - m) ** 2) for m in mats])


# bounds
bounds = [(0, 10) for i in range(25)]

# import optimization library
from mystic.solvers import diffev2

# minimize
result = diffev2(objective, bounds, npop=10, gtol=200, disp=False, full_output=True)

# optimized matrix
result[0].reshape(5, 5)

# MSE of the optimized matrix
result[1]

# check if result is same as average of matrixes
avg = np.mean(mats, axis=0)
assert np.allclose(result[0].reshape(5, 5), avg, rtol=0.001)


# plot some 3d points using plt
####################################
x = np.random.randint(0, 10, size=10)
y = np.random.randint(0, 10, size=10)
z = np.random.randint(0, 10, size=10)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.scatter(x, y, z, c="r", marker="o")
plt.show()


# plot a matrix as 3d points using plt
###########################################
size = 10
n_mats = 5
mats = [np.random.randint(0, 10, size=(size, size)) for i in range(n_mats)]
mat = mats[0]


def plot_matrix_as_3d_points(mat: np.ndarray):
    nrows, ncols = mat.shape
    if nrows != ncols:
        raise ValueError("matrix must be square")
    size = nrows

    # get row and column indices of the matrixes
    row_idx = np.arange(size)
    col_idx = np.arange(size)

    # get all combinations of row and column indices
    row_idx, col_idx = np.meshgrid(row_idx, col_idx)

    # plot
    x = row_idx.flatten()
    y = col_idx.flatten()
    z = mat.flatten()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(x, y, z, c="r", marker="o")


plot_matrix_as_3d_points(mat=mat)
plt.show()


# plot a matrix as 3d surface using plt
###########################################
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_matrix_as_3d_surface(mat: np.ndarray):
    """
    Examples
    --------------
    ::

        plot_matrix_as_3d_surface(mat=np.random.randint(0, 10, size=(10, 10)))
        plt.show()
    """
    nrows, ncols = mat.shape
    if nrows != ncols:
        raise ValueError("matrix must be square")
    size = nrows

    # get row and column indices of the matrixes
    row_idx = np.arange(size)
    col_idx = np.arange(size)

    # get all combinations of row and column indices
    row_idx, col_idx = np.meshgrid(row_idx, col_idx)

    # plot
    x = row_idx.flatten()
    y = col_idx.flatten()
    z = mat.flatten()

    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    return fig, ax


# use mystic to minimize MSE of a matrix in relation to list of matrixes
# with constraint
########################################

# list of 10 by 10 matrixes
size = 10
n_mats = 5
mats = [np.random.randint(0, 10, size=(size, size)) for i in range(n_mats)]

# function to be minimized
def objective(x: np.ndarray):
    """
    Examples::

        objective(x = np.array(range(100)))
        objective(x = np.array(range(1,101)))
    """
    mat = np.array(x).reshape(size, size)
    return np.mean([np.mean((mat - m) ** 2) for m in mats])


# bounds
max_in_mats = max([mat.max() for mat in mats])
min_in_mats = min([mat.min() for mat in mats])
bounds = [(min_in_mats, max_in_mats) for i in range(size**2)]

# penalty
def penalty(x: np.ndarray):
    """
    Examples::

        penalty(x = np.array(range(100)))
        penalty(x = np.array(range(1,101)))
    """
    mat = np.array(x).reshape(size, size)
    # mat is monotonic
    mat_is_monotonic = np.all(np.diff(mat, axis=0) >= 0) and np.all(
        np.diff(mat, axis=1) >= 0
    )

    return 0 if mat_is_monotonic else 10000


# a 10 by 10 matrix that is monotonic and bounded by 0 to 10

# 10 by 10 zero matrix
mat = np.array([0 for i in range(size**2)]).reshape(size, size)

import itertools

# combinations of range(10), and range(10)
for i, j in itertools.product(range(10), range(10)):
    mat[i][j] = (i + j) / 2

# libs
from mystic.monitors import VerboseMonitor

# monitor
mon = VerboseMonitor(10)

# minimize
result = diffev2(
    objective,
    x0=mat.flatten(),
    bounds=bounds,
    npop=10,
    gtol=500,
    penalty=penalty,
    disp=False,
    full_output=True,
    itermon=mon,
)

# optimized matrix
result[0].reshape(size, size)

# MSE of the optimized matrix
result[1]

# plot result
plot_matrix_as_3d_surface(mat=result[0].reshape(size, size))
plt.show()
