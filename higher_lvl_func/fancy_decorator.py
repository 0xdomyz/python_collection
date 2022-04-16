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

if __name__ == "__main__":
    card = PlayingCard("ace", "black")
    greet("aaa")
    greet2("bbb")