"""Run and benchmark 1D diffusion with and without Cython."""

import time
from pathlib import Path

import diffusion
import numpy as np


def diffusion_py(u: np.ndarray, alpha: float, steps: int) -> np.ndarray:
    """Pure Python/Numpy version for comparison."""
    u_curr = u.copy()
    u_next = np.empty_like(u_curr)
    for _ in range(steps):
        u_next[1:-1] = u_curr[1:-1] + alpha * (
            u_curr[:-2] - 2.0 * u_curr[1:-1] + u_curr[2:]
        )
        u_next[0] = u_curr[0]
        u_next[-1] = u_curr[-1]
        u_curr, u_next = u_next, u_curr
    return u_curr


def run_demo(n: int = 20000, steps: int = 200, alpha: float = 0.1):
    x = np.linspace(0, 1, n)
    u0 = np.sin(2 * np.pi * x).astype(np.float64)

    t0 = time.perf_counter()
    py_out = diffusion_py(u0, alpha, steps)
    py_time = time.perf_counter() - t0

    scratch = np.empty_like(u0)
    u_cy = u0.copy()
    t1 = time.perf_counter()
    diffusion.diffusion_steps(u_cy, alpha, steps, scratch)
    cy_time = time.perf_counter() - t1

    err = diffusion.max_abs_diff(py_out, u_cy)

    print(f"Python time: {py_time:.3f}s for n={n}, steps={steps}")
    print(f"Cython time: {cy_time:.3f}s (speedup x{py_time / cy_time:.1f})")
    print(f"Max abs diff: {err:.3e}")


if __name__ == "__main__":
    if not Path("diffusion.pyd").exists() and not Path("diffusion.so").exists():
        print("Extension not built. Run: python setup.py build_ext --inplace")
    run_demo()
