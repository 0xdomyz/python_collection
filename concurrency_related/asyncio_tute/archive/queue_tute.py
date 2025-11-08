import asyncio
import itertools as it
import os
import random
import time


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(caller=None) -> None:
    """Sleep for a random amount of time between 0 and 2 seconds.

    Example::

        asyncio.run(randsleep(caller="Producer 1"))
    """
    i = random.randint(0, 2)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    """Produce random data and put it into the queue.

    Example::

        async def main():
            q = asyncio.Queue()
            # have 2 producers
            await asyncio.gather(produce(1, q), produce(2, q))
            #print out q current size
            print(f"q size: {q.qsize()}")

        asyncio.run(main())
    """
    n = random.randint(0, 10)
    print(f"Producer {name} will produce {n} items.")
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    """Produce random data and put it into the queue.

    Example::

        async def main():
            q = asyncio.Queue()
            # put 2 items into the queue
            await q.put((1, time.perf_counter()))
            await q.put((2, time.perf_counter()))
            # 2 consumer as task
            consumers = [asyncio.create_task(consume(1, q)),
                            asyncio.create_task(consume(2, q))]
            # wait for the queue to be empty
            await q.join()
            # cancel the consumers
            for c in consumers:
                c.cancel()
            #print out q current size
            print(f"q size: {q.qsize()}")

        asyncio.run(main())
    """
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>" f" in {now-t:0.5f} seconds.")
        print(f"q size: {q.qsize()}")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    import argparse

    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=3)
    parser.add_argument("-c", "--ncon", type=int, default=4)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")
