import time
import functools


def hello(func):
    """make a func that print hello then execute a func

    Examples
    -------------
    >>> def name():
    ...     print("Alice")
    ...
    >>> hello(name)()
    Hello
    Alice
    >>> @hello
    ... def name2():
    ...     print("Alice")
    ...
    >>> name2()
    Hello
    Alice
    """

    def inner():
        print("Hello")
        func()

    return inner


def measure_time(func):
    """
    Exampls
    -----------
    >>> def myFunction(n):
    ...     time.sleep(n)
    ...     print("done")
    ...
    >>> measure_time(myFunction)(0.5)
    done
    Function took 0.5110921859741211 seconds to run
    """

    def wrapper(*arg, **kwargs):
        t = time.time()
        res = func(*arg, **kwargs)
        print("Function took " + str(time.time() - t) + " seconds to run")
        return res

    return wrapper


def do_twice(function):
    """
    Examples
    ------------
    >>> do_twice(lambda x: print(f"do twice {x}"))("input")
    do twice input
    do twice input
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        return function(*args, **kwargs)

    return wrapper


def timer(func):
    """Print the runtime of the decorated function

    Examples
    ------------
    >>> @timer
    ... def waste_some_time(num_times):
    ...     for _ in range(num_times):
    ...         sum([i**2 for i in range(10000)])
    ...
    >>> waste_some_time(2)
    Finished 'waste_some_time' in 0.0056 secs
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value when called

    Examples
    ---------
    >>> import math
    >>> factorial = debug(math.factorial)
    >>> def approximate_e(terms=18):
    ...     return sum(1 / factorial(n) for n in range(terms))
    ...
    >>> approximate_e(4)
    Calling factorial(0)
    -> 1
    Calling factorial(1)
    -> 1
    Calling factorial(2)
    -> 2
    Calling factorial(3)
    -> 6
    2.6666666666666665
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"-> {value!r}")
        return value

    return new_func


if __name__ == "__main__":
    pass
