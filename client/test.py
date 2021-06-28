import asyncio
import websockets
import json
#import key_lookup as kl
import gnupg
import os

def register_server(socket, spk):
    try:
        fp = gpg.import_keys(spk).fingerprints[0]
        pk = [item for item in gpg.list_keys() if item["fingerprint"] == fp][0]
        print(fp)
        print(pk)
        print(socket.remote_address)
        server = {
            "ws": socket,
            "pub": pk,
            "fin": fp,
            "name": 
                f"ws://{socket.remote_address[0]}:{socket.remote_address[1]}"

            #"fin": kl.get_key(pk)["fingerprint"],
            #"name": kl.get_key(pk)["fingerprint"]
        }
        print(server)
        CONNS.append(server)
    finally:
        pass

async def connect(uri, identity):
    async with websockets.connect(uri) as ws:
        await handshake(ws, identity["pub"])
        while True:
            #parse_message(await ws.recv())
            pass

async def handshake(ws, identity):
    try:
        req = {
            "type": "ClientHello"
        }
        await ws.send(json.dumps(req))
        
        msg = json.loads(await ws.recv())
        spk = msg["spk"]
        print(msg)
        print(spk)
        register_server(ws, spk)
        #print("CONNS: ", CONNS)
        req = {
            "type": "ClientKey",
            "cpk": gpg.export_keys(identity["fingerprint"])
        }
        await ws.send(json.dumps(req))
        
        msg = json.loads(await ws.recv())
        if msg["type"] != "Ready":
            sys.exit("shits broken yo")

        print("Completed handshake!")
    finally:
        pass
    pass


gpg = gnupg.GPG(gnupghome = os.getcwd() + '/../.gnupg')
gpg.encoding = 'utf-8'

# list of active connections (servers)
CONNS = []
# find private keys (our identities)
# might have to be changed; answer question:
# will we have private keys that do not correspond to one of our identities?
identities = {
    "pub": {},
    "sec": {}
}
for sec_key in gpg.list_keys(True):
    fp = sec_key["fingerprint"]
    identities["sec"][fp] = sec_key
    pk = None
    pub_keys = gpg.list_keys()
    for pub_key in pub_keys:
        if pub_key["fingerprint"] == fp:
            pk = pub_key
    identities["pub"][fp] = pk

print(identities)
current_id = {
        "sec": [k for k in identities["sec"].items()][0][1],
        "pub": [k for k in identities["pub"].items()][0][1]
}
print("Current identity: ", current_id)

# temporary, for testing purposes
c = input("create key? ")
if c == "y":
    uname = input("username: ")
    passphrase = input("passphrase: ")
    kl.create_key(uname, passphrase)

### This will probably get removed
# with open("keys.json", "r") as key_json:
#     fingerprints = json.loads(key_json.read())["keys"]
#     key_json.close()
#
# for fingerprint in fingerprints:
#     KEY_DATAS[fingerprint] = kl.get_key_data(fingerprint)
#
# print(KEY_DATAS)
###

asyncio.get_event_loop().run_until_complete(
    connect("ws://localhost:8765", current_id)
)
