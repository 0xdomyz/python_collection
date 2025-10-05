import asyncio


@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine"""
    # No need to build these yourself, but be aware of what they are
    s = yield from stuff()
    return s


async def py35_coro():
    """Native coroutine, modern syntax"""
    s = await stuff()
    return s


async def stuff():
    return 0x10, 0x20, 0x30


def gen():
    yield from [1, 2, 3]


def gen2():
    for i in [1, 2, 3]:
        yield i


if __name__ == "__main__":
    py34_coro()
    py35_coro()

    list(gen())
    list(gen2())

    # generator expressions
    from itertools import cycle

    def endless():
        """Yields 9, 8, 7, 6, 9, 8, 7, 6, ... forever"""
        yield from cycle((9, 8, 7, 6))

    e = endless()
    total = 0
    for i in e:
        if total < 30:
            print(i, end=" ")
            total += i
        else:
            print()
            # Pause execution. We can resume later.
            break

    # Resume
    next(e), next(e), next(e)

    # async generator expressions
    async def mygen(u: int = 10):
        """Yield powers of 2."""
        i = 0
        while i < u:
            yield 2**i
            i += 1
            await asyncio.sleep(0.1)

    # async comprehensions
    async def main():
        # This does *not* introduce concurrent execution
        # It is meant to show syntax only
        g = [i async for i in mygen()]
        f = [j async for j in mygen() if not (j // 3 % 5)]
        return g, f

    g, f = asyncio.run(main())
    g

    f
