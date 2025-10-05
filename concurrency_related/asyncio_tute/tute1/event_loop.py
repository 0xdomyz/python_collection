import asyncio


async def func():
    res = await mygen()
    return res


async def mygen():
    return 1, 2, 3


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(func())
    finally:
        loop.close()
