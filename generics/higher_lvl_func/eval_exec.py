_GLOBAL = "global"


def return_1():
    print(_GLOBAL)
    return 1


def return_2():
    print(_GLOBAL)
    return 2


def return_args(*args):
    return args


def return_kwargs(**kwargs):
    a = 9
    print("in func:\n")
    print(globals())
    print("locals:\n")
    print(locals())
    return kwargs


if __name__ == "__main__":
    function_name = "return_1"
    print(eval(f"{function_name}()"))

    function_name = "return_args"
    args = ["1", "2", "3"]
    print(eval(f"{function_name}(*args)"))

    function_name = "return_kwargs"
    kwargs = dict(a="1", b=2)
    print(eval(f"{function_name}(**kwargs)"))

    print("in main:\n")
    print(globals())
    print("locals:\n")
    print(locals())

    exec(f"print(return_args(*args))")
