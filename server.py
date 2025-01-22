import asyncio
import json
from protocol import Protocols
from gameLogic import GameLogic

'''
What do I need server_socket to do?
I need server to accept incoming connections 
Handle match making process
fetch and store data in db
Store instances of games and players in them as another process is initialising the game
'''
#Server setup
host = "localhost"
port = 80
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setblocking(False)
# server_socket.bind((host, port))    
# server_socket.listen()


            
async def handleClient(reader, writer): #ConnectionResetError maybe raised do this in try block do avoid exceptions being raised 
    while True:
        try:
            data = await reader.read(100)
            if not data:
                break

            message = json.loads(data.decode())
            print(message)
            

            writer.write(message)
            await writer.drain()
        except ConnectionResetError as e:
            print(f"disconnected from {writer.get_extra_info('peername')}")
            writer.close()
            await writer.wait_closed()

    writer.close()
    await writer.wait_closed()


async def main():
    server_socket = await asyncio.start_server(handleClient, host, port)
    
    addr = server_socket.sockets[0].getsockname()
    print(f"serving on {addr}")

    async with server_socket:
        await server_socket.serve_forever()

if __name__ == "__main__":
    try:
        #Need to use tasks or TaskGroups to utilise concurrency 
        asyncio.run(main())
        print("event_loop ended")

    except KeyboardInterrupt:
        print("We are ending test")

