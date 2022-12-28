"""
Concurrency encompasses both multiprocessing (ideal for CPU-bound tasks)
and threading (suited for IO-bound tasks).

Multiprocessing is a form of parallelism,
with parallelism being a specific type (subset) of concurrency.

concurrent.futures
threading
asyncio
multiprocessing
"""

import asyncio


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def main():
    await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
