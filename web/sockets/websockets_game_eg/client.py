#!/usr/bin/env python

import asyncio

import websockets


async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        # receive the message back from the server
        res = await websocket.recv()
        return res


res = asyncio.run(hello())

print(res)
