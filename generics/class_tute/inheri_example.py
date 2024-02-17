class Parent(object):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return Parent(self.value + other)


class Child(Parent):
    def __init__(self, value):
        super().__init__(value)

    def __repr__(self):
        return "Child({})".format(self.value)

    def __add__(self, other):
        return Child(self.value + other)


my_obj = Child(5)
print(my_obj + 10)
