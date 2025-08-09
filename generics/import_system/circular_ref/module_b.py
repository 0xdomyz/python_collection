import module_a


def function_b():
    module_a.function_a()
    return "Hello from B"


print("Module B loaded")

function_b()
