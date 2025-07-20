import asyncio
import websockets
import json

async def get_watch_data(exc="NSEFO", secid="71441", limit=5):
    uri = 'wss://wss1.multitrade.tech:15208'
    watch_data_list = []

    try:
        async with websockets.connect(uri) as websocket:
            # Wait for handshake
            response = await websocket.recv()
            if "HandShake" in response:
                # Send Watch request
                watch_request = {
                    "Message": "Watch",
                    "EXC": exc,
                    "SECID": secid
                }
                await websocket.send(json.dumps(watch_request))

                # Collect a few Watch responses
                while len(watch_data_list) < limit:
                    response = await websocket.recv()
                    if "\"Watch\"" in response:
                        try:
                            parsed = json.loads(response)
                            watch_data_list.append(parsed)
                        except json.JSONDecodeError:
                            continue  # skip malformed JSON

            else:
                return {"error": "Handshake failed"}

    except Exception as e:
        return {"error": str(e)}

    return watch_data_list