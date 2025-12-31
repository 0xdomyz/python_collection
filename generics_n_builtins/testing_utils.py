"""
Testing helpers shared across simple pytest examples.
"""

from typing import Callable

import pytest


def assert_raises(expected_exception: Exception, fn: Callable, *args, **kwargs):
    """Assert that a callable raises the expected exception.

    Example:
        >>> assert_raises(ZeroDivisionError, lambda: 1/0)
    """
    with pytest.raises(expected_exception):
        fn(*args, **kwargs)
