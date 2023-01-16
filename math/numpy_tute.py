import numpy as np

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

np.zeros(2)

np.ones(2)

# example code of np array squeeze method
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)
print(a.shape)

b = a.squeeze()
print(b)
print(b.shape)

# example of some common numpy array methods
import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)
print(a.shape)

print(a.T)
print(a.T.shape)

print(a.flatten())
print(a.flatten().shape)

b = np.array([[1, 2, 3], [4, 5, 6]])
print(a + b)
print(np.add(a, b))

print(a - b)
print(np.subtract(a, b))

print(a * b)
print(np.multiply(a, b))

print(a / b)
print(np.divide(a, b))


import numpy as np

# creating arrays
a = np.array([1, 2, 3])
b = np.zeros((3, 3))
c = np.ones((3, 3))
d = np.eye(3)

# set random seed
np.random.seed(0)

# generating random numbers
e = np.random.randn(3, 3)
f = np.random.rand(3, 3)
g = np.random.randint(1, 10, (3, 3))

# computing statistics
h = np.mean(a)
i = np.median(a)
j = np.std(a)
k = np.min(a)
l = np.max(a)
m = np.argmin(a)
n = np.argmax(a)

# sorting and unique values
o = np.sort(a)
p = np.unique(a)

# reshaping and flattening
q = d.flatten()
r = a.reshape(3, 1)
r.shape

# linear algebra
s = np.dot(b, c)
t = np.cross(b, c)
u = np.linalg.inv(e)
v = np.linalg.det(e)
w = np.linalg.solve(e, f)

# saving and loading arrays
np.savetxt("a.txt", e)
x = np.loadtxt("a.txt")

# apply func to np array
import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def func(x):
    return str(x) + "1"


b = np.apply_along_axis(func, 0, a)
print(b)

# apply func to each element in np array
import numpy as np

a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def func(x):
    return str(x) + "1"


b = np.vectorize(func)(a)

print(b)


# numpy datetime64 to datetime
################################
import datetime

import numpy as np

a = np.datetime64("2020-01-01")
b = a.astype(datetime.datetime)

b == a

# datetime 64 with T and decimal seconds
a = np.datetime64("2020-01-01T00:00:00.000000000")
# remove decimal seconds
b = np.datetime64(a, "s")
# convert to datetime
c = b.astype(datetime.datetime)
