# a custom error class
class CustomError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def _raise():
    """
    ::

        _raise()
    """
    raise CustomError("Custom Error")


# a function that raises an exception or succeeds controlled by the argument
def func(x):
    if x == "success":
        pass
    elif x == "custom error":
        raise CustomError("Custom Error")
    else:
        raise Exception("Exception")


# example to show python's try except finally syntax
def main():
    try:
        fh = open("xlines.txt")
        for line in fh.readlines():
            print(line, end="")
    except IOError as e:
        print("something bad happened ({})".format(e))
    finally:
        print("this would be printed always")


# multiple except blocks
def main2():
    try:
        raise Exception("something bad happened")
    except IOError as e:
        print("something bad happened ({})".format(e))
    except Exception as e:
        print("Other exception ({})".format(e))
    finally:
        print("this would be printed always")


# try except else
def try_except_else(x):
    try:
        func(x)
    except CustomError as e:
        print(e)
    except Exception as e:
        print(e)
    else:
        print("success")


try_except_else("success")
try_except_else("custom error")
try_except_else("")
