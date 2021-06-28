async def parse_message(m):
    t = m["type"]
    res = None

    if t == "ClientHello":
        return {
            "type": "ServerHello",
            "spk": None
        }
    elif t == "ClientKey":
        return {
            "type": "Ready",
            "r_cpk": m["cpk"]
        }
    else:
        return {
            "type": "TBD",
            "m_cpk": "TBD",
            "message": "TBD",
        }
