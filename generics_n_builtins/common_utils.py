"""
General-purpose utility functions used across examples.
"""

import time
from contextlib import contextmanager
from itertools import islice
from typing import Iterable, Iterator, List, TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield lists of length `size` from an iterable.

    Example:
        >>> list(chunked([1,2,3,4,5], 2))
        [[1,2], [3,4], [5]]
    """
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk


def flatten(list_of_lists: Iterable[Iterable[T]]) -> List[T]:
    """Flatten one level of nesting.

    Example:
        >>> flatten([[1,2],[3]])
        [1,2,3]
    """
    return [item for sublist in list_of_lists for item in sublist]


@contextmanager
def timer(label: str):
    """Context manager to measure elapsed time.

    Example:
        >>> with timer("work"):
        ...     heavy_work()
    """
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.3f}s")
