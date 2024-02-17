# assert numeric
########################
assert type(3) is int
assert type(3.0) is float

# numeric types
x = 3
assert type(x) is int or type(x) is float
x = 3.0
assert type(x) is int or type(x) is float

# instance
x = 3
assert isinstance(x, int) or isinstance(x, float)

# numpy
import numpy as np

x = np.float64(3)
assert type(x) is np.float64 or type(x) is np.float32


# checking instance
def check_numeric(num):
    assert isinstance(num, (int, float, complex)), "Input must be numeric"
    if isinstance(num, int):
        print("Input is an integer")
    elif isinstance(num, float):
        print("Input is a float")
    elif isinstance(num, complex):
        print("Input is a complex number")


check_numeric(3)
check_numeric(3.0)
check_numeric(3 + 0j)


# checking via protocols
def check_addition_support(obj):
    assert hasattr(obj, "__add__"), "Type does not support addition"
    print("Type supports addition")


check_addition_support(3)
check_addition_support(3.0)
check_addition_support(3 + 0j)
