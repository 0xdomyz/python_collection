from dataclasses import dataclass
import functools


def repeat(num_times):
    """
    Examples
    ------------
    >>> @repeat(num_times=2)
    ... def greet(name):
    ...     print(f"Hello {name}")
    ...
    >>> @repeat(3)
    ... def greet2(name):
    ...     print(f"Hello {name}")
    ...
    >>> greet("aaa")
    Hello aaa
    Hello aaa
    >>> greet2("bbb")
    Hello bbb
    Hello bbb
    Hello bbb
    """

    def decorate(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return new_func

    return decorate


def count_calls(func):
    """
    Examples
    ------------
    >>> @count_calls
    ... def say_whee():
    ...     print("Whee!")
    ...
    >>> say_whee()
    Call 1 of 'say_whee'
    Whee!
    >>> say_whee()
    Call 2 of 'say_whee'
    Whee!
    >>> say_whee()
    Call 3 of 'say_whee'
    Whee!
    """

    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)

    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


def debug_count_calls(func):
    """Print the function signature and return value and number of calls on use

    Examples
    ---------
    >>> @debug_count_calls
    ... def factorial(n):
    ...     if n == 0:
    ...         return 1
    ...     else:
    ...         return n*factorial(n-1)
    ...
    >>> factorial(3)
    Call 1 of  factorial(3)
    Call 2 of  factorial(2)
    Call 3 of  factorial(1)
    Call 4 of  factorial(0)
    Call 4 of  factorial -> 1
    Call 3 of  factorial -> 1
    Call 2 of  factorial -> 2
    Call 1 of  factorial -> 6
    6
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        new_func.counter += 1
        display = f"Call {new_func.counter} of  {func.__name__}"
        print(f"{display}({signature})")
        value = func(*args, **kwargs)
        print(f"{display} -> {value!r}")
        return value

    new_func.counter = 0

    return new_func


@functools.lru_cache(maxsize=4)
def fibonacci(num):
    """
    Examples
    ------------
    >>> fibonacci(5)
    Calculating fibonacci(5)
    Calculating fibonacci(4)
    Calculating fibonacci(3)
    Calculating fibonacci(2)
    Calculating fibonacci(1)
    Calculating fibonacci(0)
    5
    >>> fibonacci(4)
    3
    >>> fibonacci(3)
    2
    >>> fibonacci(2)
    1
    >>> fibonacci(1)
    Calculating fibonacci(1)
    1
    >>> fibonacci(0)
    Calculating fibonacci(0)
    0
    >>> fibonacci.cache_info()
    CacheInfo(hits=6, misses=8, maxsize=4, currsize=4)
    >>> fibonacci.cache_clear()
    """
    print(f"Calculating fibonacci({num})")
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)


@functools.lru_cache(maxsize=2)
def identity(x):
    """
    Examples
    -----------
    >>> identity(0)
    x=0
    0
    >>> identity(1)
    x=1
    1
    >>> identity(2)
    x=2
    2
    >>> identity(0)
    x=0
    0
    >>> identity(2)
    2
    """
    print(f"{x=}")
    return x


@dataclass
class PlayingCard:
    """
    Examples
    -----------
    card = PlayingCard("ace", "black")
    """

    rank: str
    suit: str


if __name__ == "__main__":
    1
