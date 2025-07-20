import asyncio
import websockets
import json

async def get_market_data():
    uri = 'wss://wss1.multitrade.tech:15208'
    try:
        async with websockets.connect(uri) as websocket:
            response = await websocket.recv()

            if "HandShake" in response:
                request_payload = {
                    "Message": "Broadcast",
                    "EXC": "NSECM",
                    "SECID": "3045"
                }
                await websocket.send(json.dumps(request_payload))

                response = await websocket.recv()
                if "\"Broadcast\"" in response:
                    return json.loads(response)
                else:
                    return {"error": "Broadcast not received"}
            else:
                return {"error": "Handshake failed"}

    except Exception as e:
        return {"error": str(e)}