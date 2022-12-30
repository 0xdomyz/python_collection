# declar
#####################
import asyncio


async def main():
    print("hello")
    await asyncio.sleep(1)
    print("world")


asyncio.run(main())

# run
#####################

# await a coro
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, "hello")
    await say_after(2, "world")

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())

# tasks
#####################
async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))

    task2 = asyncio.create_task(say_after(2, "world"))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())

# awaitables - coroutines
################################
import asyncio


async def nested():
    return 42


async def main():
    # Nothing happens if we just call "nested()".
    # A coroutine object is created but not awaited,
    # so it *won't run at all*.
    nested()

    # Let's do it differently now and await it:
    print(await nested())  # will print "42".


asyncio.run(main())

# awaitables - Tasks
#######################
import asyncio


async def nested():
    return 42


async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    print(await task)


asyncio.run(main())

# awaitables - Futures

# create task
#####################
background_tasks = set()


async def some_coro(param):
    # Do something with param.
    print(param)


async def main():
    for i in range(10):
        task = asyncio.create_task(some_coro(param=i))

        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)

        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)

        await task


asyncio.run(main())

# sleep
#####################
import asyncio
import datetime


async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


asyncio.run(display_date())


# gather
#####################
import asyncio


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f


async def main():
    # Schedule three calls *concurrently*:
    L = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )
    print(L)


asyncio.run(main())
