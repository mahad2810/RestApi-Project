import asyncio
import websockets
import json

async def get_vwap_updates(limit=5):
    uri = 'wss://wss1.multitrade.tech:15208'
    vwap_updates = []
    OldVWAP = -1

    try:
        async with websockets.connect(uri) as websocket:
            # Wait for handshake
            response = await websocket.recv()
            if "HandShake" in response:
                # Send Broadcast message
                sc = {
                    "Message": "Broadcast",
                    "EXC": "NSECM",
                    "SECID": "3045"
                }
                await websocket.send(json.dumps(sc))

                # Continuously receive data
                while len(vwap_updates) < limit:
                    response = await websocket.recv()
                    
                    if "\"Broadcast\"" in response:
                        responses = response.strip().split("\n\n")

                        for res in responses:
                            data = json.loads(res)

                            if "LTP" in data and "VWAP" in data:
                                if data["VWAP"] != OldVWAP:
                                    OldVWAP = data["VWAP"]
                                    vwap_updates.append(data)

            else:
                return {"error": "Handshake failed"}

    except Exception as e:
        return {"error": str(e)}

    return vwap_updates
