import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {"data": []}

USERS = set()


def state_event():
    return json.dumps({**STATE})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def sync_server(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            STATE["data"] = data
            await notify_state()
    finally:
        await unregister(websocket)


start_server = websockets.serve(sync_server, "0.0.0.0", 9000, max_size=1000000000000000, ping_interval=None)


while True:
    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except Exception:
        print(Exception)
