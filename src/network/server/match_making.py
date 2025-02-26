'''
This server script will be responsible for match making 
A client will send a request to either create or join a game 
If the client creates the game the are given a game code which is the ID of the game stored in redis 
If client joins the game then they are add to the list of clients in the game with the corresponding ID in redis 

Each redis entry should have GameCode: list of clients connected 
When lobby is full then a subprocess is launched which will handle gameplay 

GameIDs are random ints that are hashed with a salt value
'''
import asyncio
import base64
import redis
import json
import logging
#from game import game_class
from string import Template
from json import JSONDecodeError
from random import randint, randbytes
from protocol import Protocols
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from  websockets.asyncio.server import serve, ServerConnection

# Server attributes
host ="localhost"
port = 80
template = Template('{"m_type": "$m_type", "data": $data}')   #This is a template for message to be sent to clients
activeSessions = {}  

#Redis setup
r = redis.Redis('localhost', 6379)
channel = 'activeSessions'

#Configure logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generateSessionCode():
    #Generates the number hashes it and returns it as game code
    hash = randbytes(randint(1, 128))
    return base64.b64encode(hash).decode('utf-8')[0:6]

async def createGame(websocket:ServerConnection, maxPlayer:int):
    print(type(maxPlayer))
    logger.info("Creating new session")
    sessionID = generateSessionCode() #ID of the game 
    activeSessions[sessionID] = {
        'clients': {websocket}, 
        'gameObj': None,    #Can get rid of this
        'maxPlayer': maxPlayer, 
        'forceStart': set(), 
        'numPlayer': 1, 
        'ready': False
    }
    print(f"Game Session created\n {activeSessions[sessionID]}")
    message = template.substitute(m_type=Protocols.Response.SESSION_ID, data=json.dumps(sessionID))
    logger.debug(f"sending message: {message}")
    await websocket.send(message.encode())


#TODO: Figure out how to get a player to join game that is already running
#TODO: Need to disconnect ServerConnections properly
async def joinGame(websocket: ServerConnection, sessionID):
    logger.info(f"adding {websocket.remote_address} to session:{sessionID}")

    try:

        if activeSessions[sessionID]['numPlayer'] < activeSessions[sessionID]['maxPlayer']: 

            activeSessions[sessionID]['numPlayer']+=1
            activeSessions[sessionID]['clients'].add(websocket)

            join_message = template.substitute(m_type=Protocols.Response.SESSION_ID, data=json.dumps(sessionID))
            await websocket.send(join_message)

            #If lobby is filled up then launch the game. How do join a client to a game in progress. Maybe we redirect them and send them game instance 
            if activeSessions[sessionID]['numPlayer'] >= activeSessions[sessionID]['maxPlayer']:
                logger.debug(f"session: {sessionID} is ready to be played")
                # Create game instance and store in active sessions


                #Redirect each client in lobby to game server 
                redirectMessage = template.substitute(m_type=Protocols.Response.REDIRECT, data=json.dumps({"host":"localhost", "port":443}))
                for serverConnection in activeSessions[sessionID]['clients']:
                    await serverConnection.send(redirectMessage)

                #Publish relevant info to redis server
                data = {'sessionID':sessionID, 'clients':{}, 'gameObj':activeSessions[sessionID]['gameObj']}
                r.publish(channel, json.dumps(data))

                return  #Exit out of function
                

            logger.info("Broadcasting to clients in lobby")
            message = template.substitute(m_type=Protocols.Response.LOBBY_UPDATE, data=activeSessions[sessionID]['numPlayer'])
            for serverConnection in  activeSessions[sessionID]['clients']:  #Broadcast info to other clients in lobby
                if serverConnection != websocket:
                    await serverConnection.send(message.encode())
        
        #If there isn't any room to join game tell player 
        else:
            error_message = template.substitute(m_type=Protocols.Response.ERROR, data="The game that you are trying to join is full")
            await websocket.send(error_message.encode())

    except KeyError as e:
        error_message = template.substitute(m_type=Protocols.Response.ERROR, data="The game that you are trying to join does not exist")
        await websocket.send(error_message.encode())

    except ConnectionClosed as e:
        print("Error occurred trying to send message to client")
        
        


async def voteStart(websocket: ServerConnection, sessionID):
    logger.info("vote to start has been counted")
    try:
        activeSessions[sessionID]['forceStart'].add(websocket)
        logger.info(f"Votes: {len(activeSessions[sessionID]['forceStart'])}")
        if len(activeSessions[sessionID]['forceStart']) >= activeSessions[sessionID]['numPlayer'] and activeSessions[sessionID]['numPlayer'] > 1:
            await redirect(sessionID) 
            return  #Exit function 
        
    
        #Broadcast new info to other clients in lobby 
        logger.debug("Broadcasting vote to start game")  
        message = template.substitute(m_type=Protocols.Response.FORCE_START, data=len(activeSessions[sessionID]['forceStart']))
        for serverConnection in activeSessions[sessionID]['clients']:
            if serverConnection != websocket:
                await serverConnection.send(message)

    except KeyError as e:
        error_message = template.substitute(m_type=Protocols.Response.ERROR, data="The game that you are trying to vote does not exist")
        await websocket.send(error_message)

    except ConnectionClosed as e:
        print("Error occurred trying to send message to client")
      
async def redirect(sessionID):
    activeSessions[sessionID]['ready'] = True
    #Create game object 

    #Redirect each client in lobby to game server 
    redirectMessage = json.dumps({"m_type": Protocols.Response.REDIRECT, "data": {"host": "localhost", "port": 443}})
    for serverConnection in activeSessions[sessionID]['clients']:                
        await serverConnection.send(redirectMessage)
                


         #Publish relevant info to redis server
    data = {'sessionID':sessionID, 'clients':{}, 'gameObj':activeSessions[sessionID]['gameObj']}
    r.publish(channel, json.dumps(data))

async def leaveGame(websocket: ServerConnection, sessionID, redirect=False):
    #This method removes a player if they choose to leave the game 
    logger.info(f"{websocket.remote_address} is leaving the game")
    try:
        
        logger.info("client has left lobby")
        activeSessions[sessionID]['numPlayer'] -=1 
        activeSessions[sessionID]['clients'].remove(websocket)
        await websocket.close()

        if len(activeSessions[sessionID]['clients'])==0:
            logger.info(f"{sessionID} has been deleted")
            #Need to remove any involvement that this player has had on the lobby
            del activeSessions[sessionID]
            logger.info(f"Active sessions left {activeSessions}")
            return
        
        #If lobby isn't being redirected then update other clients in the lobby
        if not redirect:
            message = template.substitute(m_type=Protocols.Response.LOBBY_UPDATE, data=activeSessions[sessionID])
            logger.info(f"broadcasting {websocket.remote_address} has left game")
            #Broadcasting new player count in lobby to other clients 
            for serverConnection in  activeSessions[sessionID]['clients']:
                if serverConnection != websocket:
                    await serverConnection.send(message)

            logger.info(f"{websocket.remote_address} has been closed")

        logger.debug(f"active sessions left: {activeSessions}")

    except KeyError as e:
        error_message = template.substitute(m_type=Protocols.Response.ERROR, data="The game that you are trying to leave does not exist")
        await websocket.send(error_message)

    except ConnectionClosed as e:
        print("Error occurred trying to send message to client")        


async def closeClient(websocket: ServerConnection, sessionID=None, redirect=False):
    #If client is in a game then invoke leaveGame()
    #else disconnect the bastard
    try:
        if sessionID in activeSessions:
            await leaveGame(websocket, sessionID, redirect)
        else:
            logger.info(f"{websocket.remote_address} has been closed")
            await websocket.close()

    except ConnectionClosed as e:
        print(f"Issue sending data to client {e}")

    except ConnectionClosedError as e:
        print(f"Issue sending data to client {e}")

    except KeyError as e:
        return

 
async def handleClient(websocket: ServerConnection):
    #Read and handle messages
    print(f"client has connected: {websocket.remote_address}") 
    currentSessionID = None #This tracks the latest sessionID associated to the client
    while True:
        try:

            data = await websocket.recv()                       #Receives messages from client 

            if not data:                                        #If there is not message or message lost disconnect client 
                #Leave infinite loop an disconnect client
                logger.error("message is ost or corrupted")
                await closeClient(websocket, currentSessionID)
                break

            message = json.loads(data)
            currentSessionID = message['sessionID']
            logger.info(f"message received: {message}")

            match message['m_type']:
                
                case Protocols.Request.CREATE_GAME:
                    await createGame(websocket, message['data'])

                case Protocols.Request.JOIN_GAME:
                    await joinGame(websocket, message['data'])

                case Protocols.Request.START_GAME_EARLY_VOTE:
                    await voteStart(websocket, message['sessionID'])

                case Protocols.Request.LEAVE:
                    await closeClient(websocket, message['sessionID'])

        except ConnectionError as e:
            print(f"Whoops\n{e}")
            await leaveGame(websocket, message['sessionID'])
            break

        except ConnectionClosedError as e:
            await websocket.close()
            break

        except JSONDecodeError as e:
            #This error an occur if json.loads() is given an empty string
            #This may as occur after closing ServerConnection
            await closeClient(websocket, currentSessionID, True)
            break

        except ConnectionClosedOK as e: #Connection has been closed properly on client side
            await websocket.close()
            break




async def main():
    logger.info("server has started")
    async with serve(handleClient, host, port, ping_timeout=180) as server:
        await server.serve_forever()


# start_server = websockets.asyncio.server(handleClient, host, port)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
