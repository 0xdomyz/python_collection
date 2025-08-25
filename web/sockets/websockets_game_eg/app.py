#!/usr/bin/env python
# https://dokk.org/documentation/python-websockets/10.4/intro/tutorial1/

import asyncio
import websockets

import logging
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# manages conn: iterating over messages received on the connection until the client disconnects
# async def handler(websocket):
#     async for message in websocket:
#         print(f"{message}")


import json

from connect4 import PLAYER1, PLAYER2, Connect4

async def handler(websocket):

    # Initialize a Connect Four game.
    game = Connect4()
    player = PLAYER1 if game.last_player == PLAYER2 else PLAYER2

    async for message in websocket:
        data = json.loads(message)

        # parse an event of type "play", the only type of event that the user interface sends;
        if data["type"] == "play":
            column = data["column"]
            
            # play the move in the board with the play() method, alternating between the two players;
            # if play() raises RuntimeError because the move is illegal, send an event of type "error";
            try:
                row = game.play(player, column)
                player = PLAYER1 if player == PLAYER2 else PLAYER2
            except RuntimeError as e:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e),
                }))
                continue

            # else, send an event of type "play" to tell the user interface where the checker lands;
            await websocket.send(json.dumps({
                "type": "play",
                "player": game.last_player,
                "column": column,
                "row": row,
            }))
            
            # if the move won the game, send an event of type "win".
            if game.last_player_won:
                await websocket.send(json.dumps({
                    "type": "win",
                    "player": game.last_player,
                }))
                break
        else:
            raise RuntimeError(f"Unsupported event: {data['type']}")

async def main():
    # create conn from specified handler, interface, port
    # invoking serve as async cm
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())  # event loop, run main coroutine
