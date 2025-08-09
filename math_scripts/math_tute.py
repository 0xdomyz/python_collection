from math import floor, log10

import numpy as np
import pandas as pd

# data
######################
# create a dataframe of 10 rows and 3 columns with random numbers
df = pd.DataFrame(np.random.randn(10, 3), columns=list("ABC"))

# rounding
######################
round_to_n = lambda x, n: round(x, -int(floor(log10(x))) + (n - 1))
np.round(3.141592653589793, 2)

# mod, int division
######################

# Python
a = [10, 20, 30]
b = [3, 7, 10]

print([x % y for x, y in zip(a, b)])  # Output: [1, 6, 0]
print([x // y for x, y in zip(a, b)])  # Output: [3, 2, 3]

# NumPy
a_np = np.array([10, 20, 30])
b_np = np.array([3, 7, 10])

print(np.mod(a_np, b_np))  # Output: [1 6 0]
print(np.floor_divide(a_np, b_np))  # Output: [3 2 3]

# pandas
a_pd = pd.Series([10, 20, 30])
b_pd = pd.Series([3, 7, 10])

print(a_pd.mod(b_pd))  # Output: 0    1
#         1    6
#         2    0
#         dtype: int64
print(a_pd.floordiv(b_pd))  # Output: 0    3
#         1    2
#         2    3
#         dtype: int64

# np log functions
######################
np.log(2.718281828459045)
np.log10(1000)
np.log2(1024)
np.log1p(1.718281828459045)
np.log1p(df)

# modulo
######################
5 % 2
5 // 2
result, remainder = divmod(5, 2)

# trigonometry
######################
np.sin(0)
np.cos(0)
np.tan(0)
np.arcsin(0)
np.arccos(1)
np.arctan(0)
np.arctan2(0, 1)
np.hypot(3, 4)
np.degrees(np.pi / 2)
np.radians(90)

# hyperbolic functions
######################
np.sinh(0)
np.cosh(0)
np.tanh(0)
np.arcsinh(0)
np.arccosh(1)

# exponential and logarithmic functions
######################
np.exp(1)
np.exp2(10)
np.power(2, 10)
np.expm1(1)
np.log(2.718281828459045)
np.log2(1024)
np.log10(1000)
np.log1p(1.718281828459045)

# special functions
######################
np.erf(0)
np.erfc(0)
np.gamma(1)
np.lgamma(1)

# logarithmic functions
######################
np.logaddexp(0, 0)
np.logaddexp2(0, 0)

# logistic functions
######################
np.expit(0)

# plot logistic function
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 100)
y = 1 / (1 + np.exp(-x))
plt.plot(x, y)
plt.show()


# floating point manipulation
######################
np.nextafter(0, 1)
np.spacing(1)
