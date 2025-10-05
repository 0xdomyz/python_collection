# example of using asyncio to run a number of tasks in the background
import asyncio
import time


async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        await asyncio.sleep(delay)
        print(f"Task {name} complete")


if __name__ == "__main__":
    # Create the queue of work
    work_queue = asyncio.Queue()

    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        work_queue.put_nowait(work)

    # Run the tasks
    asyncio.run(
        asyncio.gather(
            task("One", work_queue),
            task("Two", work_queue),
        )
    )
