import asyncio
import websockets
import json

async def test():
    driver_id = "15f3e1d1-5a48-47dc-910d-df5f231cf821"
    uri = f"ws://localhost:8001/drivers/ws/{driver_id}"
    print(f"Connecting to {uri}")
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"lat": 12.9750, "lng": 77.5960}))
        response = await ws.recv()
        print("Response:", response)

asyncio.run(test())
