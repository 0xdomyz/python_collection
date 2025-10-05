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

# plot list of matrix as 3D points
#####################################

from typing import List


def plot_list_of_matrix_as_3d_points(mats: List[np.ndarray]):
    # get size
    mat = mats[0]
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

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for mat in mats:
        z = mat.flatten()
        ax.scatter(x, y, z, c="r", marker="o")


plot_list_of_matrix_as_3d_points(mats)
plt.show()


# plot a matrix as 3d surface using plt
###########################################
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_matrix_as_3d_surface(mat: np.ndarray):
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


plot_matrix_as_3d_surface(mat=np.random.randint(0, 10, size=(10, 10)))
plt.show()

plot_matrix_as_3d_surface(mat=np.random.randint(0, 10, size=(5, 5)))
plt.show()

plot_matrix_as_3d_surface(mat=np.random.randint(0, 10, size=(4, 4)))
plt.show()

# make a saddle shape matrix
mat = np.zeros((10, 10))
for i in range(10):
    for j in range(10):
        mat[i, j] = i * j

plot_matrix_as_3d_surface(mat=mat)
plt.show()

# make a matrix where the diagonal is larger than slowly decreasing values to the sides
mat = np.zeros((10, 10))
for i in range(10):
    for j in range(10):
        mat[i, j] = 10 - i - j

plot_matrix_as_3d_surface(mat=mat)
plt.show()

# another
mat = np.zeros((10, 10))
for i in range(10):
    for j in range(10):
        mat[i, j] = i + j

plot_matrix_as_3d_surface(mat=mat)
plt.show()

# another matrix
mat = np.zeros((10, 10))
for i in range(10):
    for j in range(10):
        mat[i, j] = 10 - abs(i - j)

plot_matrix_as_3d_surface(mat=mat)
plt.show()


# plot 2 3d surfaces using plt
#####################################
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

mat1 = mats[0]
mat2 = mats[1]

# x, y coordinates of the matrixes via size
nrows, ncols = mat1.shape
if nrows != ncols:
    raise ValueError("matrix must be square")
size = nrows
row_idx = np.arange(size)
col_idx = np.arange(size)
row_idx, col_idx = np.meshgrid(row_idx, col_idx)

# plot
fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

x = row_idx.flatten()
y = col_idx.flatten()

z = mat1.flatten()
surf = ax.plot_trisurf(x, y, z, linewidth=0.1, label="mat1", color="r", alpha=0.9)

z = mat2.flatten()
surf = ax.plot_trisurf(x, y, z, linewidth=0.1, label="mat2", color="b", alpha=0.4)
plt.show()


# plot mat differences
##############################
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

mat_diff = mat1 - mat2

# x, y coordinates of the matrixes via size
nrows, ncols = mat_diff.shape
if nrows != ncols:
    raise ValueError("matrix must be square")
size = nrows
row_idx = np.arange(size)
col_idx = np.arange(size)
row_idx, col_idx = np.meshgrid(row_idx, col_idx)

# plot
fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

x = row_idx.flatten()
y = col_idx.flatten()

z = mat_diff.flatten()
surf = ax.plot_trisurf(
    x, y, z, linewidth=0.1, label="mat_diff", alpha=0.9, cmap=cm.coolwarm
)

# add surface representing the zero line
# z = np.zeros_like(z)
# surf = ax.plot_trisurf(x, y, z, linewidth=0.1, label="zero", alpha=0.5, color="k")

# add points grid representing the zero line
# z = np.zeros_like(z)
# ax.scatter(x, y, z, c="k", marker="o", alpha=0.5)

# add lines representing the zero line
# z = np.zeros_like(z)
# ax.plot(x, y, z, c="k", alpha=0.5)

# add lines representing a large value line and a small value line
z = np.ones_like(z) * 10
ax.plot_trisurf(x, y, z, linewidth=0.1, label="large", alpha=0.5, color="k")
z = np.ones_like(z) * -10
ax.plot_trisurf(x, y, z, linewidth=0.1, label="small", alpha=0.5, color="k")

fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

# save 3d surface plot
###############################

fig, ax = plot_matrix_as_3d_surface(mat=np.random.randint(0, 10, size=(10, 10)))

# save 3d surface plot as png
fig.savefig("test.png")

# save 3d surface plot as svg
fig.savefig("test.svg")

# save 3d surface plot as pdf
fig.savefig("test.pdf")

# save 3d surface plot as eps
fig.savefig("test.eps")

# save 3d surface plot as ps
fig.savefig("test.ps")

# save 3d surface plot as pgf
fig.savefig("test.pgf")

# save 3d surface plot as raw data
fig.savefig("test.raw")

# save 3d surface plot as rgba
fig.savefig("test.rgba")

# save 3d surface plot as svgz
fig.savefig("test.svgz")

# save 3d surface plot as tif
fig.savefig("test.tif")

# save 3d surface plot as tiff
fig.savefig("test.tiff")

# save 3d surface plot as jpeg
fig.savefig("test.jpeg")

# save 3d surface plot as png, but at another view angle

# default view
ax.view_init(azim=-60, elev=30)
fig.savefig("test.png")

azim_range = np.arange(-360, 360, 30)

for azim in azim_range:
    ax.view_init(azim=azim, elev=30)
    # show sign of azim in file name
    fig.savefig(f"test_azim_{azim:+}.png")

# slight to the left
ax.view_init(azim=-20, elev=30)
fig.savefig("test_left.png")

# slight to the right
ax.view_init(azim=-80, elev=30)

fig.savefig("test_right.png")


# use mystic to minimize MSE of a matrix in relation to list of matrixes
# with constraint
########################################
import itertools

import numpy as np
from mystic.monitors import VerboseMonitor
from mystic.solvers import diffev2

# list of 10 by 10 matrixes
size = 10
n_mats = 5
mats = [np.random.randint(0, 50, size=(size, size)) for i in range(n_mats)]


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
def penalty_0_or_large(x: np.ndarray):
    """penalty_0_or_large(x=np.array(range(100)))"""
    mat = np.array(x).reshape(size, size)
    # mat is monotonic
    mat_is_monotonic = np.all(np.diff(mat, axis=0) >= 0) and np.all(
        np.diff(mat, axis=1) >= 0
    )
    return 0 if mat_is_monotonic else 10000


def penalty_continuous(x: np.ndarray):
    """penalty_continuous(x=np.array(np.random.randint(0, 10, size=(100,))))"""
    size = int(np.sqrt(len(x)))
    mat = np.array(x).reshape(size, size)
    # count of instance where not monotonic
    count_not_monotonic = np.sum(np.diff(mat, axis=0) < 0) + np.sum(
        np.diff(mat, axis=1) < 0
    )
    return count_not_monotonic**2


# a 10 by 10 matrix that is monotonic and bounded by 0 to 10

# 10 by 10 zero matrix
mat = np.array([0 for i in range(size**2)]).reshape(size, size)


# combinations of range(10), and range(10)
for i, j in itertools.product(range(10), range(10)):
    mat[i][j] = (i + j) / 2


# monitor
mon = VerboseMonitor(10)

# minimize
result = diffev2(
    objective,
    x0=mat.flatten(),
    bounds=bounds,
    npop=10,
    gtol=500,
    # penalty=penalty_0_or_large,
    penalty=penalty_continuous,
    disp=False,
    full_output=True,
    itermon=mon,
)

# optimized matrix
result[0].reshape(size, size)
penalty_continuous(result[0])

# MSE of the optimized matrix
result[1]

# plot result
plot_matrix_as_3d_surface(mat=result[0].reshape(size, size))
plt.show()

# plot list of matrixes as points and result as surface

# get size
mat = mats[0]
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

fig = plt.figure()

z = result[0]
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)
surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=0.1)
fig.colorbar(surf, shrink=0.5, aspect=5)

for mat in mats:
    z = mat.flatten()
    ax.scatter(x, y, z, c="r", marker="o")

plt.show()

# for each matrix cell, plot histogram of matrixes' values, against result's value
# plots share x axis
result_mat = result[0].reshape(size, size)
mats

fig = plt.figure()

for i, j in itertools.product(range(size), range(size)):
    ax = fig.add_subplot(size, size, i * size + j + 1)
    ax.hist([mat[i][j] for mat in mats], bins=10)
    ax.set_xbound(min_in_mats, max_in_mats)
    ax.axvline(result_mat[i][j], color="r")

plt.show()
