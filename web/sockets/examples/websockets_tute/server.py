#!/usr/bin/env python

"""
interactive client::

    python3.9 -m websockets ws://localhost:8765/
    Connected to ws://localhost:8765/.
    > Hello world!
    < Hello world!
    Connection closed: 1000 (OK).
"""

import asyncio

import websockets


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
