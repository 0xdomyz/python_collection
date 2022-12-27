import asyncio


async def func():
    res = await mygen()
    return res


async def mygen():
    return 1, 2, 3


async def main():
    res = await func()
    print(res)


if __name__ == "__main__":
    asyncio.run(func())

    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(func())
    # finally:
    #     loop.close()

    # not do much until event loop
    import asyncio

    async def main():
        print("Hello ...")
        await asyncio.sleep(1)
        print("World!")

    routine = main()
    routine

    asyncio.run(routine)

    #
