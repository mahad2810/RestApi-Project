import asyncio
import websockets
import json

async def connect_to_server():
    uri = 'wss://wss1.multitrade.tech:15208'

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")

            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print("Handshake received:", response)

                if "HandShake" in response:
                    # Send LTP request
                    ltp_request = json.dumps({
                        "Message": "LTP",
                        "EXC": "NSEFO",
                        "SECID": "35020"
                    })
                    await websocket.send(ltp_request)
                    print("LTP request sent.")

                    while True:
                        data = await websocket.recv()
                        if "\"LTP\"" in data:
                            print("LTP Data:", data)
                        else:
                            print("Other Message:", data)

                else:
                    print("Unexpected handshake message")

            except asyncio.TimeoutError:
                print("Handshake timed out. Server didn't respond.")

    except Exception as e:
        print("WebSocket error:", str(e))

# Run the event loop
try:
    asyncio.run(connect_to_server())
except KeyboardInterrupt:
    print("\nDisconnected by user")
