'''
This server script will be responsible for match making 
A client will send a request to either create or join a game 
If the client creates the game the are given a game code which is the ID of the game stored in redis 
If client joins the game then they are add to the list of clients in the game with the corresponding ID in redis 

Each redis entry should have GameCode: list of clients connected 
When lobby is full then a subprocess is launched which will handle gameplay 

GameIDs are random ints that are hashed with a salt value
'''

import base64
import json
import logging
from string import Template
from  websockets.asyncio.server import serve, ServerConnection, broadcast
from network.server.protocol import Protocols
from random import randint, randbytes

# Server attributes
host ="localhost"
port = 80
template = Template('{"m_type": "$m_type", "data": "$data"}')   #This is a template for message to be sent to clients
activeSessions = {}  

#Configure logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generateSessionCode():
    #Generates the number hashes it and returns it as game code
    hash = randbytes(randint(1, 128))
    return base64.b64encode(hash).decode('utf-8')[0:6]

def createGame(websocket:ServerConnection, maxPlayer:int):
    logger.info("Creating new session")
    session_id = generateSessionCode() #ID of the game 
    activeSessions[session_id] = {
        'clients': [], 
        'game': None,
        'maxPlayer': maxPlayer, 
        'forceStart': 0, 
        'numPlayer': 1, 
        'ready': False
    }
    print("Game Session created")
    message = template.substitute(m_type=Protocols.Response.SESSION_ID, data=session_id)
    logger.debug(f"sending message to {websocket.remote_address}")
    websocket.send(message.encode())


async def joinGame(websocket: ServerConnection, sessionID):
    # activeSessions[sessionID]['clients'].append(player)
    #Needs to alter or add info to game instance 
    logger.info(f"adding {websocket.remote_address} to session:{sessionID}")

    activeSessions[sessionID]['numPlayer']+=1
    activeSessions[sessionID]['clients'].add(websocket)
    if activeSessions[sessionID]['numPlayer'] >= activeSessions[sessionID]['maxPlayer']:
        logger.debug(f"session: {sessionID} is ready to be played")
        activeSessions[sessionID]['ready'] = True
        #Launch game server as subprocess ??
        #Or we can start creating the games instance when the lobby is ready
        pass

    logger.info("Broadcasting to clients in lobby")
    message = template.substitute(m_type=Protocols.Response.LOBBY_UPDATE, data=activeSessions[sessionID]['numPlayer'])
    for serverConnection in  activeSessions[sessionID]['clients']:  #Broadcast info to other clients in lobby
        #if serverConnection != websocket:
        await serverConnection.send(message)
        

#TODO: figure out how to link vote to a specific client because they could leave but there vote to start remains 
#TODO: Have a check to see if sessionID exists  
async def voteStart(websocket: ServerConnection, sessionID):
    logger.info("vote to start has been counted")
    activeSessions[sessionID]['forceStart']+=1
    if activeSessions[sessionID]['forceStart'] >= activeSessions[sessionID]['numPlayer']:
        activeSessions[sessionID]['ready'] = True
        #Launch game server as subprocess???
        pass
    
    logger.debug("Broadcasting vote to start game")  
    message = template.substitute(m_type=Protocols.Response.FORCE_START, data=activeSessions[sessionID]['forceStart'])
    for serverConnection in activeSessions[sessionID]['clients']:  #Broadcast new info to other clients in lobby 
        #if serverConnection != websocket:
        await serverConnection.send(message)

    #await broadcast(activeSessions[sessionID]['clients'], str(activeSessions[sessionID]['forceStart']).encode(), True)

async def leaveGame(websocket: ServerConnection, sessionID):
    #This method removes a player if they choose to leave the game 
    logger.info(f"{websocket.remote_address} is leaving the game")
    if sessionID not in activeSessions:
        logger.error("invalid sessionID")
        print('invalid sessionID')
        return
    
    print("client has left lobby")
    activeSessions[sessionID]['numPlayer'] -=1 
    activeSessions[sessionID]['clients'].remove(websocket)
    if len( activeSessions[sessionID]['clients'])==0:
        logger.info(f"{sessionID} has been deleted")
        #Need to remove any involvement that this player has had on the lobby
        del activeSessions[sessionID]
        return
    

    message = template.substitute(m_type=Protocols.Response.LOBBY_UPDATE, data=activeSessions[sessionID]['numPlayer'])

    logger.info(f"broadcasting {websocket.remote_address} has left game")
    #Broadcasting new player count in lobby to other clients 
    for serverConnection in  activeSessions[sessionID]['clients']:
        #if serverConnection != websocket:
        await serverConnection.send(message)

    logger.info(f"{websocket.remote_address} has been closed")
    await websocket.close()


async def closeClient(websocket: ServerConnection, sessionID=None):
    #If client is in a game then invoke leaveGame()
    #else disconnect the bastard
    if sessionID in activeSessions:
        await leaveGame(websocket, sessionID)
    else:
        logger.info(f"{websocket.remote_address} has been closed")
        await websocket.close()

 
async def handleClient(websocket: ServerConnection, path):
    #Read and handle messages
    print(f"client has connected: {websocket.remote_address}") 
    currentSessionID = None #This tracks the latest sessionID associated to the client
    while True:
        try:
            logger.info("message received")
            data = await websocket.recv()                       #Receives messages from client 

            if not data:                                        #If there is not message or message lost disconnect client 
                #Leave infinite loop an disconnect client
                logger.error("message is ost or corrupted")
                await closeClient(websocket, currentSessionID)
                break

            message = json.loads(data.decode())
            currentSessionID = message['sessionID']
            logger.info("message received")
            match message['m_type']:
                
                case Protocols.Request.CREATE_GAME:
                    await createGame(websocket, message['data'])

                case Protocols.Request.JOIN_GAME:
                    await joinGame(websocket, message['sessionID'])

                case Protocols.Request.LEAVE:
                    await leaveGame(websocket, message['sessionID'])

        except ConnectionError as e:
            print(f"Whoops\n{e}")
            await leaveGame(websocket)




async def main():
    logger.info("server has started")
    async with serve(handleClient, host, port) as server:
        await server.serve_forever()


# start_server = websockets.asyncio.server(handleClient, host, port)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
    print("Game Code: ", generateSessionCode())
