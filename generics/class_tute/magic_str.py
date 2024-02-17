# str gives bahavioural when apply str
class Fruit(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# repr change display
class Fruit2(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


if __name__ == "__main__":
    f = Fruit("apple")
    f
    str(f)

    f = Fruit2("apple")
    f
    str(f)
    f.__str__.__doc__
    type(f)
