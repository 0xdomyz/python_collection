"""Numba basics: jit-compiled functions and vectorized ufuncs.

Run directly:
    python numba_intro.py
"""

import time

import numpy as np
from numba import njit, prange, vectorize


@njit
def pairwise_l2(a: np.ndarray, b: np.ndarray) -> float:
    """Compute squared L2 distance between two 1D arrays."""
    acc = 0.0
    for i in range(a.shape[0]):
        diff = a[i] - b[i]
        acc += diff * diff
    return acc


@vectorize(["float64(float64, float64)"], nopython=True)
def add_vec(x, y):
    return x + y


@njit(parallel=True)
def row_sums(mat: np.ndarray) -> np.ndarray:
    """Parallel row sums using prange."""
    out = np.empty(mat.shape[0], dtype=np.float64)
    for i in prange(mat.shape[0]):
        s = 0.0
        for j in range(mat.shape[1]):
            s += mat[i, j]
        out[i] = s
    return out


def main():
    rng = np.random.default_rng(0)
    a = rng.standard_normal(1_000, dtype=np.float64)
    b = rng.standard_normal(1_000, dtype=np.float64)
    m = rng.standard_normal((10_000, 256), dtype=np.float64)

    # warmup to trigger compilation
    pairwise_l2(a, b)
    add_vec(a, b)
    row_sums(m)

    # simple checks
    print("pairwise_l2", pairwise_l2(a, b))
    print("add_vec", add_vec(a[:5], b[:5]))
    print("row_sums", row_sums(m)[:3])

    # micro benchmark
    def bench(fn, *args):
        start = time.perf_counter()
        out = fn(*args)
        return out, time.perf_counter() - start

    _, t_pair = bench(pairwise_l2, a, b)
    _, t_add = bench(add_vec, a, b)
    _, t_rows = bench(row_sums, m)

    print("\nTimings (after compilation):")
    print(f"pairwise_l2: {t_pair*1e3:.2f} ms")
    print(f"add_vec:    {t_add*1e3:.2f} ms")
    print(f"row_sums:   {t_rows*1e3:.2f} ms")


if __name__ == "__main__":
    main()
