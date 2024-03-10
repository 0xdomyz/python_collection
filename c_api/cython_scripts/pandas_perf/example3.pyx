cimport numpy as np

cimport cython

import numpy as np


cdef np.float64_t f_typed(np.float64_t x) except? -2:
    return x * (x - 1)

cpdef np.float64_t integrate_f_typed(np.float64_t a, np.float64_t b, np.int64_t N):
    cdef np.int64_t i
    cdef np.float64_t s = 0.0, dx
    dx = (b - a) / N
    for i in range(N):
        s += f_typed(a + i * dx)
    return s * dx

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[np.float64_t] apply_integrate_f_wrap(
    np.ndarray[np.float64_t] col_a,
    np.ndarray[np.float64_t] col_b,
    np.ndarray[np.int64_t] col_N
):
    cdef np.int64_t i, n = len(col_N)
    assert len(col_a) == len(col_b) == n
    cdef np.ndarray[np.float64_t] res = np.empty(n, dtype=np.float64)
    for i in range(n):
        res[i] = integrate_f_typed(col_a[i], col_b[i], col_N[i])
    return res
