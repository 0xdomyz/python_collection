# example of using lock
import asyncio


async def worker_1(lock):
    print("worker_1: waiting for the lock")
    async with lock:
        print("worker_1: has lock")
        await asyncio.sleep(0.1)


async def worker_2(lock):
    print("worker_2: waiting for the lock")
    async with lock:
        print("worker_2: has lock")
        await asyncio.sleep(0.1)


async def main():
    lock = asyncio.Lock()
    await asyncio.gather(worker_1(lock), worker_2(lock))


asyncio.run(main())

# example of using semaphore
import asyncio


async def worker_1(semaphore):
    print("worker_1: waiting for the semaphore")
    async with semaphore:
        print("worker_1: has semaphore")
        await asyncio.sleep(0.1)


async def worker_2(semaphore):
    print("worker_2: waiting for the semaphore")
    async with semaphore:
        print("worker_2: has semaphore")
        await asyncio.sleep(0.1)


async def main():
    semaphore = asyncio.Semaphore(1)
    await asyncio.gather(worker_1(semaphore), worker_2(semaphore))


asyncio.run(main())

# example of using event
import asyncio


async def worker_1(event):
    print("worker_1: waiting for the event")
    await event.wait()
    print("worker_1: event is set")


async def worker_2(event):
    print("worker_2: setting the event")
    event.set()


async def main():
    event = asyncio.Event()
    await asyncio.gather(worker_1(event), worker_2(event))


asyncio.run(main())

# example of using condition
import asyncio


async def worker_1(condition):
    print("worker_1: waiting for the condition")
    async with condition:
        await condition.wait()
        print("worker_1: condition met")


async def worker_2(condition):
    print("worker_2: notifying the condition")
    async with condition:
        condition.notify(1)


async def main():
    condition = asyncio.Condition()
    await asyncio.gather(worker_1(condition), worker_2(condition))


asyncio.run(main())

# example of using barrier
import asyncio


async def worker_1(barrier):
    print("worker_1: waiting for the barrier")
    await barrier.wait()
    print("worker_1: barrier passed")


async def worker_2(barrier):
    print("worker_2: waiting for the barrier")
    await barrier.wait()
    print("worker_2: barrier passed")


async def main():
    barrier = asyncio.Barrier(2)
    await asyncio.gather(worker_1(barrier), worker_2(barrier))


asyncio.run(main())

# example of using queue
import asyncio


async def worker_1(queue):
    print("worker_1: waiting for the queue")
    await queue.put(1)
    print("worker_1: item added to the queue")


async def worker_2(queue):
    print("worker_2: waiting for the queue")
    item = await queue.get()
    print("worker_2: got item from the queue")


async def main():
    queue = asyncio.Queue()
    await asyncio.gather(worker_1(queue), worker_2(queue))


asyncio.run(main())

# example of using stream
import asyncio


async def worker_1(stream):
    print("worker_1: waiting for the stream")
    await stream.write(b"hello")
    print("worker_1: wrote to the stream")


async def worker_2(stream):
    print("worker_2: waiting for the stream")
    data = await stream.read(5)
    print("worker_2: read from the stream")


async def main():
    stream = asyncio.StreamReader()
    await asyncio.gather(worker_1(stream), worker_2(stream))


asyncio.run(main())

# example of using future
import asyncio


async def worker_1(future):
    print("worker_1: waiting for the future")
    await future
    print("worker_1: future is done")


async def worker_2(future):
    print("worker_2: setting the future")
    future.set_result("the result")


async def main():
    future = asyncio.Future()
    await asyncio.gather(worker_1(future), worker_2(future))


asyncio.run(main())

# example of using task
import asyncio


async def worker_1():
    print("worker_1: doing some work")
    await asyncio.sleep(0.1)
    print("worker_1: work complete")


async def worker_2():
    print("worker_2: doing some work")
    await asyncio.sleep(0.1)
    print("worker_2: work complete")


async def main():
    task1 = asyncio.create_task(worker_1())
    task2 = asyncio.create_task(worker_2())
    await task1
    await task2


asyncio.run(main())

# example of using executor
import asyncio


async def worker_1():
    print("worker_1: doing some work")
    await asyncio.sleep(0.1)
    print("worker_1: work complete")


async def worker_2():
    print("worker_2: doing some work")
    await asyncio.sleep(0.1)
    print("worker_2: work complete")


async def main():
    loop = asyncio.get_running_loop()
    await asyncio.gather(
        loop.run_in_executor(None, worker_1),
        loop.run_in_executor(None, worker_2),
    )


asyncio.run(main())


# example of using barrier
async def example_barrier():
    # barrier with 3 parties
    b = asyncio.Barrier(3)

    # create 2 new waiting tasks
    asyncio.create_task(b.wait())
    asyncio.create_task(b.wait())

    await asyncio.sleep(0)
    print(b)

    # The third .wait() call passes the barrier
    await b.wait()
    print(b)
    print("barrier passed")

    await asyncio.sleep(0)
    print(b)


asyncio.run(example_barrier())
