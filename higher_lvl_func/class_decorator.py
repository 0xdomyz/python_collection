from dataclasses import dataclass

@dataclass
class PlayingCard:
    """
    Examples
    -----------
    card = PlayingCard("ace", "black")
    """

    rank: str
    suit: str

class C:
    """
    Examples
    ----------
    >>> c = C()
    >>> c.setx(4)
    >>> print(c.getx())
    4
    >>> c.delx()
    """
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        if value < 0:
            raise ValueError
        else:
            self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")

class D:
    """
    Examples
    ------------
    >>> d = D()
    >>> d.x = 4
    >>> d.x = -4
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 14, in x
    ValueError
    >>> print(d.x)
    4
    >>> del d.x
    """
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property.

        Returns:
            x: x
        """
        return self._x

    @x.setter
    def x(self, value):
        if value < 0:
            raise ValueError
        else:
            self._x = value

    @x.deleter
    def x(self):
        del self._x
        return "deleted"

class E:
    """
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
    """
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




