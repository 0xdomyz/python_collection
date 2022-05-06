"""
`link <https://martinheinz.dev/blog/50>`_
"""
from functools import singledispatch

@singledispatch
def func(input):
    print("generic")

@func.register
def _(input: list):
    print("list")

@func.register
def _(input: str):
    print("str")

if __name__ == "__main__":
    func("ab")
    func(['a', 'b'])
    pass
