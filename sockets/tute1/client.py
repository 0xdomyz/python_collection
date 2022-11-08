import asyncio

import websockets


async def test():
    async with websockets.connect(
        "wss://demo.piesocket.com/v3/channel_1?api_key=YOUR_API_KEY"
    ) as websocket:
        await websocket.send("hello")
        response = await websocket.recv()
        print(response)


asyncio.get_event_loop().run_until_complete(test())
