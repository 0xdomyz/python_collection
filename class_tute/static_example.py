class MyClass:
    counter = 0

    def __init__(self):
        MyClass.counter += 1

    @staticmethod
    def get_counter():
        return MyClass.counter
