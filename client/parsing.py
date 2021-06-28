async def parse_message(m):
    t = m["type"]
    res = None

    if t == "ClientHello":
        return {
            "type": "ServerHello",
            "pk": None
        }
    else:
        return {
            "type": "TBD",
            "message": "TBD"
        }
