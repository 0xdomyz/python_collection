import numpy as np
from numba_examples.numba_intro import add_vec, pairwise_l2, row_sums


def test_pairwise_l2_matches_numpy():
    rng = np.random.default_rng(0)
    a = rng.standard_normal(1000)
    b = rng.standard_normal(1000)
    expected = np.dot(a - b, a - b)
    assert np.isclose(pairwise_l2(a, b), expected)


def test_add_vec_matches_numpy():
    rng = np.random.default_rng(1)
    a = rng.standard_normal(10)
    b = rng.standard_normal(10)
    assert np.allclose(add_vec(a, b), a + b)


def test_row_sums_matches_numpy():
    rng = np.random.default_rng(2)
    m = rng.standard_normal((100, 8))
    expected = m.sum(axis=1)
    assert np.allclose(row_sums(m), expected)
