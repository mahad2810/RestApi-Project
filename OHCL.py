import asyncio
import websockets
import json

async def get_ohlcl_data(exc="NSEFO", secid="35707", limit=3):
    uri = 'wss://wss1.multitrade.tech:15208'
    ohlcl_data_list = []

    try:
        async with websockets.connect(uri) as websocket:
            # Wait for handshake
            response = await websocket.recv()
            if "HandShake" in response:
                # Send OHLCL request
                request_msg = {
                    "Message": "OHLCL",
                    "EXC": exc,
                    "SECID": secid
                }
                await websocket.send(json.dumps(request_msg))

                while len(ohlcl_data_list) < limit:
                    response = await websocket.recv()
                    if "\"OHLCL\"" in response:
                        try:
                            parsed_data = json.loads(response)
                            ohlcl_data_list.append(parsed_data)
                        except json.JSONDecodeError:
                            continue  # Skip malformed data

            else:
                return {"error": "Handshake failed"}

    except Exception as e:
        return {"error": str(e)}

    return ohlcl_data_list