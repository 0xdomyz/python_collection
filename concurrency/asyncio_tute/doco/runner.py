import asyncio


# run
async def main():
    await asyncio.sleep(1)
    print("hello")


asyncio.run(main())

asyncio.run(main(), debug=True)


# runner in 3.11
