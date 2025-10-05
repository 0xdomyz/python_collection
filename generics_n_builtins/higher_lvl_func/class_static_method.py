class C:
    """Class method as alternative constructor.

    Examples
    ------------
    >>> C([1,2])
    [1, 2]
    >>> C.from_filename("asdfdas")
    ['a', 's', 'd', 'f', 'd', 'a', 's']
    >>> C.from_dict({"a":1, "b":2})
    [('a', 1), ('b', 2)]
    """

    def __init__(self, x: list) -> None:
        self.x = x

    def __repr__(self) -> str:
        return str(self.x)

    @classmethod
    def from_filename(cls, filename):
        return cls(list(filename))

    @classmethod
    def from_dict(cls, dict):
        return cls(list(dict.items()))


class E:
    """class method no need instance to use

    Examples
    -----------
    >>> e = E()
    >>> E.print()
    dont need instance
    >>> e.print()
    dont need instance
    """

    def __init__(self):
        self._x = None

    @classmethod
    def print(cls):
        print("dont need instance")


def print1():
    print(1)


class F:
    """static method do not have self

    Examples
    -------------
    >>> f = F()
    >>> f.print0("f")
    f
    >>> F.print0("F")
    F
    >>> f.do_print()
    0
    >>> f.print1()
    1
    """

    def __init__(self):
        self._x = None

    @staticmethod
    def print0(x):
        print(x)

    print1 = staticmethod(print1)

    def do_print(self):
        self.print0(0)


if __name__ == "__main__":
    pass
