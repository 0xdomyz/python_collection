a: int = 3
b: float = 3.14
c: str = "abc"
d: bool = False
e: list = ["a", "b", "c"]
f: tuple = (1, 2, 3)
g: dict = {"a": 1, "b": 2}

from typing import Dict, List, Tuple

e: List[str] = ["a", "b", "c"]
f: Tuple[int, int, int] = (1, 2, 3)
g: Dict[str, int] = {"a": 1, "b": 2}


def func(a: str, b: float, c: dict, d: tuple, e: list) -> dict:
    res = {"a": a, "b": b, "c": c, "d": d, "e": e}
    return res


func("aaa", 2.0, {"a": 1}, (1, 2), [1, 3])
print(func.__annotations__)
