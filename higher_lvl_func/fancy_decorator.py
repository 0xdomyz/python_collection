from dataclasses import dataclass
import functools

def repeat(num_times):
    def decorate(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return new_func
    return decorate

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


@dataclass
class PlayingCard:
    rank: str
    suit: str


@repeat(num_times=4)
def greet(name):
    print(f"Hello {name}")

@repeat(5)
def greet2(name):
    print(f"Hello {name}")

@count_calls
def say_whee():
    print("Whee!")

if __name__ == "__main__":
    card = PlayingCard("ace", "black")
    greet("aaa")
    greet2("bbb")
    say_whee()
    say_whee()
    say_whee()
    print(say_whee.num_calls)