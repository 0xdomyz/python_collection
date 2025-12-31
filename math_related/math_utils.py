"""
Reusable math utilities for quick calculations and teaching examples.
"""

from typing import Iterable, Tuple

import numpy as np


def set_random_seed(seed: int) -> None:
    """Set NumPy RNG seed for reproducibility."""
    np.random.seed(seed)


def softmax(x: Iterable[float]) -> np.ndarray:
    """Compute stable softmax for a 1D iterable."""
    arr = np.asarray(list(x), dtype=float)
    shifted = arr - np.max(arr)
    exp = np.exp(shifted)
    return exp / exp.sum()


def sigmoid(x: Iterable[float]) -> np.ndarray:
    """Elementwise sigmoid for a 1D iterable."""
    arr = np.asarray(list(x), dtype=float)
    return 1 / (1 + np.exp(-arr))


def zscore(x: Iterable[float]) -> np.ndarray:
    """Standardize values to zero mean, unit variance."""
    arr = np.asarray(list(x), dtype=float)
    mean = arr.mean()
    std = arr.std()
    return (arr - mean) / std


def normalize_minmax(x: Iterable[float]) -> np.ndarray:
    """Scale values to [0, 1]."""
    arr = np.asarray(list(x), dtype=float)
    min_val = arr.min()
    max_val = arr.max()
    return (arr - min_val) / (max_val - min_val)


def logsumexp(x: Iterable[float]) -> float:
    """Stable log-sum-exp for a 1D iterable."""
    arr = np.asarray(list(x), dtype=float)
    m = np.max(arr)
    return float(m + np.log(np.exp(arr - m).sum()))


def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute Euclidean distances between rows of a and b."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    diff = a[:, None, :] - b[None, :, :]
    return np.sqrt((diff**2).sum(axis=2))


def meshgrid_xy(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Convenience meshgrid with float dtype."""
    X, Y = np.meshgrid(np.asarray(x, float), np.asarray(y, float))
    return X, Y
