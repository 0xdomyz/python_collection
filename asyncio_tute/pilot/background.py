# example of using asyncio to run a task in the background
import asyncio
import time


async def my_task():
    while True:
        print("Hello")
        await asyncio.sleep(1)


async def main():
    asyncio.create_task(my_task())
    await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
