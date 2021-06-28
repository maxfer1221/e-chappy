import asyncio
import websockets
import json
import gnupg
import os
import key_lookup as kl
from parsing import *

gpg = gnupg.GPG(gnupghome = os.getcwd() + '/../.gnupg')
gpg.encoding = 'utf-8'

KEYS = {
    "sec": None,
    "pub": None,
    "fin": None,
    "exp": None 
}

# initialize key values
while KEYS["sec"] == None:
    KEYS["sec"] = kl.get_sk('ServerMaster')

KEYS["pub"] = kl.get_pk('ServerMaster')
KEYS["fin"] = KEYS["sec"]["fingerprint"]
KEYS["exp"] = gpg.export_keys(KEYS["fin"])

HOST = 'localhost'
PORT = 8765

USERS = []

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_users():
    if USERS:
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def message_users(m):
    if USERS:
        await asyncio.wait([user.send(m) for user in USERS])

async def register(websocket, pk):
    USERS.append({
        "ws": websocket,
        "pk": gpg.import_keys(pk).fingerprints[0]
    })
    #await notify_users()

async def unregister(websocket, fp):  
    print("fp inside: ", fp)
    gpg.delete_keys(fp)
    return [i for i in USERS if i.ws != ws]
    #await notify_users()

async def handler(ws, path):
    #await register(ws)
    try:
        fp = None
        async for message in ws:
            res = await parse_message(json.loads(message))
            for key in res:
                if key == "spk":
                    print(KEYS["exp"])
                    res[key] = KEYS["exp"]
                if key == "r_cpk":
                    print("res['r_cpk']: ", res[key])
                    fp = res.pop(key, None)["fingerprint"]
                    register(ws, pk)
            await ws.send(json.dumps(res))
            print(fp)
    finally:
        USERS = await unregister(ws, fp)
#
#async def server(ws, path):
#    async for message in ws:
#        res = parse_message(message)
#        for key in res:
#            if key == "pk":
#                res[key] = KEY["exp"]
#        print(json.dumps(res))
#        await message_users(json.dumps(res))

start_server = websockets.serve(handler, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
