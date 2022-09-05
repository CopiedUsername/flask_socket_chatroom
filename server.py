import asyncio
import itertools
import json
import websockets
import socket

STATE = {"value": 0}
USERS = set()
usernames = {}
sessions = {}

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users(message, websocket):
    if USERS:  # asyncio.wait doesn't accept an empty list
        for user in USERS:
            if user in sessions.get(str(message.get('ID'))) and message.get('msg'):
                if user == websocket:
                    await user.send(json.dumps({'msg': message['msg'], 'usr': usernames[websocket], 'type': 'self'}))
                else:
                    await user.send(json.dumps({'msg':message['msg'], 'usr': usernames[websocket], 'type': 'other'}))

async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users("", websocket)

async def handler(websocket, path):

    if websocket not in USERS:

        message = await websocket.recv()
        message = json.loads(message)
        username = message['username']
        usernames[websocket] = username
        if message['type'] == 'create':
            if message['ID'] not in sessions:
                sessions[message['ID']] = []
                sessions[message['ID']].append(websocket)
            else:
                print("ID ALREADY EXISTS")
        if message['type'] == 'join':
            if message['ID'] in sessions:
                sessions[message['ID']].append(websocket)
            else:
                print("ID DOESN'T EXIST")
    await register(websocket)
    try:
        async for message in websocket:
            message = json.loads(message)
            await notify_users(message, websocket)
    finally:
        await unregister(websocket)



async def main():

    async with websockets.serve(handler, "0.0.0.0", 38249):

        await asyncio.Future()  # run forever



if __name__ == "__main__":
    asyncio.run(main())