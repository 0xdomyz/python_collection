from functools import partial
from pathlib import Path


def make_path(a: str, b: str, c: str, d: str) -> Path:
    """
    Examples
    -------------
    >>> make_path("A", "B", "C", "D")
    WindowsPath('A/B/C/D')
    >>> make_a_path("B", "C", "D")
    WindowsPath('A/B/C/D')
    >>> make_ab_path("C", "D")
    WindowsPath('A/B/C/D')
    >>> make_d_path("A", "B", "C")
    WindowsPath('A/B/C/D')
    """
    return Path(a) / Path(b) / Path(c) / Path(d)


make_a_path = partial(make_path, "A")
make_a_path.__doc__ = "Make paths under A."

make_ab_path = partial(make_path, "A", "B")
make_ab_path.__doc__ = "Make paths under A/B."

make_d_path = partial(make_path, d="D")
make_d_path.__doc__ = "Make paths enveloping D."


if __name__ == "__main__":
    pass
