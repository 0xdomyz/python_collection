from typing import overload


@overload
def my_function(x: int) -> int:
    ...


@overload
def my_function(x: str) -> str:
    ...


def my_function(x):
    if isinstance(x, int):
        print("int")
        return x + 1
    elif isinstance(x, str):
        print("str")
        return x.upper()


if __name__ == "__main__":
    # python3 higher_lvl_func/overload_deco.py
    my_function(1)
    my_function("a")
    my_function(1.0)
