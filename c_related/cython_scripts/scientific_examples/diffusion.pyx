# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: language_level=3
# cython: nonecheck=False
# cython: initializedcheck=False

import cython


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef void diffusion_step(double[:] u, double[:] u_new, double alpha):
    """Single explicit diffusion step on a 1D line.

    Parameters
    ----------
    u : double[:]
        Current state (length n).
    u_new : double[:]
        Output buffer of length n. Will be fully written.
    alpha : float
        Stability factor (dt * k / dx^2).
    """
    cdef Py_ssize_t i, n = u.shape[0]
    for i in range(1, n - 1):
        u_new[i] = u[i] + alpha * (u[i - 1] - 2.0 * u[i] + u[i + 1])
    u_new[0] = u[0]
    u_new[n - 1] = u[n - 1]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double max_abs_diff(double[:] a, double[:] b):
    """Return max(|a - b|). Assumes same length."""
    cdef Py_ssize_t i, n = a.shape[0]
    cdef double best = 0.0
    cdef double diff
    for i in range(n):
        diff = a[i] - b[i]
        if diff < 0:
            diff = -diff
        if diff > best:
            best = diff
    return best


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef void diffusion_steps(double[:] u, double alpha, Py_ssize_t steps, double[:] scratch):
    """Run multiple diffusion steps in-place using a scratch buffer."""
    cdef Py_ssize_t s
    for s in range(steps):
        diffusion_step(u, scratch, alpha)
        diffusion_step(scratch, u, alpha)
