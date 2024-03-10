"""
Examples
-----------
ipython::

    from main import *

    %timeit df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)
    %prun -l 4 df.apply(lambda x: integrate_f(x["a"], x["b"], x["N"]), axis=1)

    %timeit df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)
    %prun -l 4 df.apply(lambda x: integrate_f_typed(x["a"], x["b"], x["N"]), axis=1)

    %timeit apply_integrate_f(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())
    %prun -l 4 apply_integrate_f(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())

    %timeit apply_integrate_f_wrap(df["a"].to_numpy(), df["b"].to_numpy(), df["N"].to_numpy())

"""

import numpy as np
import pandas as pd
from example1 import integrate_f_typed
from example2 import apply_integrate_f
from example3 import apply_integrate_f_wrap

df = pd.DataFrame(
    {
        "a": np.random.randn(1000),
        "b": np.random.randn(1000),
        "N": np.random.randint(100, 1000, (1000)),
        "x": "x",
    }
)


def f(x):
    return x * (x - 1)


def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
