import asyncio
import websockets

async def connect_to_server():
    async with websockets.connect('wss://wss1.multitrade.tech:15208') as websocket:
        response = await websocket.recv()
        if "HandShake" in response:
          
            sc = "{\"Message\":\"Broadcast\",\"EXC\":\"NSECM\",\"SECID\":\"3045\"}"
            await websocket.send(sc)
            response = await websocket.recv()
            if "\"Broadcast\"" in response:
                  print(response)
        else:
            print("WebSocket connection failed")

asyncio.run(connect_to_server())