import asyncio
import websockets
import json

async def get_ltp_updates(exc="NSEFO", secid="35020", limit=5):
    uri = 'wss://wss1.multitrade.tech:15208'
    ltp_data_list = []

    try:
        async with websockets.connect(uri) as websocket:
            try:
                # Wait for handshake (5-second timeout)
                response = await asyncio.wait_for(websocket.recv(), timeout=5)

                if "HandShake" in response:
                    # Send LTP request
                    ltp_request = json.dumps({
                        "Message": "LTP",
                        "EXC": exc,
                        "SECID": secid
                    })
                    await websocket.send(ltp_request)

                    while len(ltp_data_list) < limit:
                        data = await websocket.recv()

                        if "\"LTP\"" in data:
                            parsed = json.loads(data)
                            ltp_data_list.append(parsed)
                        else:
                            continue  # Skip non-LTP messages

                else:
                    return {"error": "Unexpected handshake message"}

            except asyncio.TimeoutError:
                return {"error": "Handshake timed out. Server didn't respond."}

    except Exception as e:
        return {"error": f"WebSocket error: {str(e)}"}

    return ltp_data_list