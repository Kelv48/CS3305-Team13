import asyncio
import websockets

async def test_connection():
    uri = "ws://localhost:8000"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            await websocket.send("ping")  # Send a simple message or ping
            response = await websocket.recv()
            print(f"Received response: {response}")
    except Exception as e:
        print(f"Error connecting to WebSocket server: {e}")

asyncio.run(test_connection())
