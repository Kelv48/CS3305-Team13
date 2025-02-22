#For testing run file in main.py
#TODO: Add locks to actions writing to activeSessions
import json
import redis
import asyncio
import logging
import threading
#from game import game_class    #There are import errors in this module need to make stuff a package 
from string import Template
from protocol import Protocols
from websockets.exceptions import ConnectionClosedError
from websockets.asyncio.server import serve, ServerConnection

'''
What do I need server_socket to do?
I need server to accept incoming connections 
Handle match making process
fetch and store data in db
Store instances of games and players in them as another process is initialising the game

When a client leaves what needs to happen?
1.    references to the client need to be removed from the activeSession dictionary and the game object 
2a.   other clients in the game need to be sent the new game object 
2b.   If there is no one left in the session remove it from the dictionary
3     Close ServerConnection and push and relevant info like player wallet to the db 

'''
#Server setup
host = "localhost"
port = 443
activeSessions = {}                                             #Key:pair Game ID → set of connected clients + gameObj + queue 
template = Template('{"m_type": "$m_type", "data": "$data"}')   #This is a template for message to be sent to clients

#Redis pub/sub setup 
channel = 'activeSessions'
r = redis.Redis('localhost', 6379)
pubsub = r.pubsub()

def addActiveSession(message):
    '''This method is for adding new active game sessions created by match_making.py
    to the activeSessions dict. This method is for initialising new sessions and NOT
    for updating already tracked sessions'''

    if message['type'] == 'message':
            data = json.loads(message['data'])
            sessionID = data.get('sessionID')
            with lock:
                activeSessions[sessionID] = {'clients':data['clients'], 'gameObj': data['gameObj']}
                print(activeSessions)

thread = pubsub.subscribe(**{channel: addActiveSession})
pubsub.run_in_thread(1, True)
#How do we get the server to update activeSessions parallel to message handling?
    #Threads will have to be used but that only provides concurrent execution 

#Config Thread
lock = threading.Lock() #Prevents deadlocks and race conditions 

#Configure logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def handleClient(websocket: ServerConnection): #ConnectionClosedError maybe raised do this in try block do avoid exceptions being raised
    logger.info(f"Connection from {websocket.remote_address}")
    while True:
        try:
            
            logger.info(f"Received message from client: {websocket.remote_address}")
            data = await websocket.recv(100)
            
            if not data:
                logger.error(f"Faulty/Missing message from client {websocket.remote_address}")
                await clientLeave(websocket)
                break

            message = json.loads(data.decode())
            logger.debug(f"Received: {message}")

            with lock:
                activeSessions[message['sessionID']]['clients'].add(websocket)       #Adds serverConnection to the appropriate session

            match message['m_type']:
                case Protocols.Request.FOLD:
                    logger.info(f"client is folding")
                    await foldClient(websocket, message['sessionID'])

                case Protocols.Request.RAISE:
                    await raiseClient(websocket, message['sessionID'])

                case Protocols.Request.CHECK:
                    await clientCheck(websocket, message['sessionID'])

                case Protocols.Request.CALL:
                    await clientCall(websocket, message['sessionID'])

                case Protocols.Request.LEAVE:
                    #TODO:redo this so that message and update is broadcast to all players in the current game
                    await clientLeave(websocket, message['sessionID'])
                    print("Client has disconnected: ")
                    break
                
        except ConnectionResetError as e:   #Occurs if client or server closes connection without sending close frame
            print(f"disconnected from {websocket.remote_address}")
            await clientLeave(websocket, message['sessionID'])
            break

        except KeyError as e:
            error_message = template.substitute(m_type=Protocols.Response.ERROR, data='Invalid session ID')
            await websocket.send(error_message.encode())

        except ConnectionClosedError as e:  #Raised when trying to interact with a closed connection
            print(f"disconnected from {websocket.remote_address}")
            await clientLeave(websocket, message['sessionID'])
            break
        


async def foldClient(websocket: ServerConnection, sessionID):
    print("player has folded")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]
    #game.foldPlayer()
    
    #Broadcast messages to all other players 
    logger.debug("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients']:
        if client_writer != websocket:
            try:
                await client_writer.send("player has folded".encode())

            except ConnectionClosedError:    #If a player has disconnected 
                #Broadcast info to the other players and remove data from game and server
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID)
    
    print("end of function")


async def raiseClient(websocket: ServerConnection, sessionID):
    print("player has raise")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.debug("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients']:
        if client_writer != websocket:
            try:
                await client_writer.send("player has raise the pot by __".encode())

            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID)
    print("end of function")


async def clientCheck(websocket: ServerConnection, sessionID):
    print("player has checked")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.debug("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients']:
        if client_writer != websocket:
            try:
                await client_writer.send("player has checked".encode())
        
            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID)

    print("end of function")

async def clientCall(websocket: ServerConnection, sessionID):
    print("player has called")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.debug("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients']:
        if client_writer != websocket:
            try:
                await client_writer.send("player has called".encode())

            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID)



#TODO: add code that sends relevant player info to DB i.e. player wallet 
async def clientLeave(websocket: ServerConnection, sessionID=None):
    
    if sessionID != None:   #If the client is in a game 
        
        #Update game object to reflect new players 

        #Tell each client to remove player from their game 
        for client_writer in activeSessions[sessionID]['clients']:
            if client_writer != websocket:
                #Send them the updated game state        
                await client_writer.send("player has left".encode())

        #This statement was partially generated by ChatGTP
        with lock:
            if websocket in activeSessions[sessionID].get('clients', set()):    #Removes websocket from set
                activeSessions[sessionID]['clients'].discard(websocket)

            if not activeSessions[sessionID].get('clients'):    #Deletes session if no WebSockets are left
                activeSessions.pop(sessionID, None)

    await websocket.close()
    



async def main():
    logger.info("server has started")
    async with serve(handleClient, host, port) as server:
        await server.serve_forever()
    

if __name__ == "__main__":
    try:
        #Server thread that will be using asyncio and handling messages 
        serverThread = threading.Thread(target=lambda: asyncio.run(main()), daemon=True)
        serverThread.start()


        #Merge Thread back into the main thread
        serverThread.join()
        print("event_loop ended")

    except KeyboardInterrupt:
        print("We are ending test")

