#!/usr/bin/env python
# https://dokk.org/documentation/python-websockets/10.4/intro/tutorial1/

import asyncio
import sys
import websockets

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# manages conn: iterating over messages received on the connection until the client disconnects
async def handler(websocket):
    async for message in websocket:
        print(f"{message}")


async def main():
    # create conn from specified handler, interface, port
    # invoking serve as async cm
    async with websockets.serve(handler, "", 54321):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())  # event loop, run main coroutine
