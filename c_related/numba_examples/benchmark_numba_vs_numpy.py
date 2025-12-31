"""Benchmark Numba vs NumPy for simple kernels.

Run:
    python benchmark_numba_vs_numpy.py
"""

import time

import numpy as np
from numba import njit, prange


def np_pairwise_l2(a: np.ndarray, b: np.ndarray) -> float:
    diff = a - b
    return float(np.dot(diff, diff))


@njit
def nb_pairwise_l2(a: np.ndarray, b: np.ndarray) -> float:
    acc = 0.0
    for i in range(a.shape[0]):
        diff = a[i] - b[i]
        acc += diff * diff
    return acc


def np_row_sums(m: np.ndarray) -> np.ndarray:
    return m.sum(axis=1)


@njit(parallel=True)
def nb_row_sums(m: np.ndarray) -> np.ndarray:
    out = np.empty(m.shape[0], dtype=np.float64)
    for i in prange(m.shape[0]):
        s = 0.0
        for j in range(m.shape[1]):
            s += m[i, j]
        out[i] = s
    return out


def bench(fn, *args, repeat: int = 3):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - start)
    return min(times)


def main():
    rng = np.random.default_rng(0)
    a = rng.standard_normal(1_000_000, dtype=np.float64)
    b = rng.standard_normal(1_000_000, dtype=np.float64)
    m = rng.standard_normal((50_000, 64), dtype=np.float64)

    # warmup to compile numba functions
    nb_pairwise_l2(a, b)
    nb_row_sums(m)

    res = []
    res.append(("pairwise_l2", "numpy", bench(np_pairwise_l2, a, b)))
    res.append(("pairwise_l2", "numba", bench(nb_pairwise_l2, a, b)))
    res.append(("row_sums", "numpy", bench(np_row_sums, m)))
    res.append(("row_sums", "numba", bench(nb_row_sums, m)))

    print("Benchmark results (best of 3, seconds):")
    for name, kind, t in res:
        print(f"{name:12s} {kind:6s}: {t:.4f}s")


if __name__ == "__main__":
    main()
