import asyncio
import websockets
import json

async def connect_to_server():
    async with websockets.connect('wss://wss1.multitrade.tech:15208') as websocket:
        response = await websocket.recv()
        if "HandShake" in response:

            sc = "{\"Message\":\"Broadcast\",\"EXC\":\"NSECM\",\"SECID\":\"3045\"}"
            await websocket.send(sc)

        OldVWAP = -1
        while True:
            response = await websocket.recv()
            if "\"Broadcast\"" in response:
                response_string = response
                responses = response_string.strip().split("\n\n")

            for res in responses:
                data = json.loads(res)
                if "LTP" in data:
                    if (OldVWAP != data["VWAP"] ):
                      OldVWAP = data["VWAP"]
                      print("VWAP:", data["VWAP"])

asyncio.run(connect_to_server())