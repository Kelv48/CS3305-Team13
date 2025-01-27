import asyncio
import json

async def test_server(host, port, message, client_num):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"Client {client_num}: connected to the server")

        writer.write(json.dumps(message).encode())
        await writer.drain()
        print(f"Client {client_num}: Sent message")

        data = await reader.read(100)
        print(f"Client {client_num}: received message ")

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Client {client_num}: Error {e}")


async def invoke_server_test():
    host  = "localhost"
    port = 80
    message = {
        'm_type': 'protocol.call',
        'data': "player has called", 
        'gameID': 5
    }

    num_clients = 500

    tasks = [test_server(host, port, message, i) for i in range(num_clients)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(invoke_server_test())