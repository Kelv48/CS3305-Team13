#For testing run file in main.py
#TODO: Add locks to actions writing to activeSessions
import json
import redis
import asyncio
import logging
import threading
#from game import game_class    #There are import errors in this module need to make stuff a package 
from string import Template
from matchmaking.protocol import Protocols
from websockets.exceptions import ConnectionClosedError, ConnectionClosed
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
host = "0.0.0.0"
port = 8001
activeSessions = {}                                             #Key:pair Game ID → set of connected clients
template = Template('{"m_type": "$m_type", "data": "$data"}')   #This is a template for message to be sent to clients

#Redis pub/sub setup 
channel = 'activeSessions'
r = redis.Redis('localhost', 6379)
pubsub = r.pubsub()

#Redis client setup
redisClient = redis.Redis(host='localhost', port=6379, decode_responses=True)   #Used to manipulate player stats/Player wallet

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
    currentSessionID = None
    userID =None
    while True:
        try:
            print(activeSessions)
            logger.info(f"Received message from client: {websocket.remote_address}")
            data = await websocket.recv(100)
            logger.info(f"message revived: {data}")

            if not data:
                logger.error(f"Faulty/Missing message from client {websocket.remote_address}")
                await clientLeave(websocket)
                break

            message = json.loads(data)

            #This if statement prevents sessionID and username from being overridden by empty data messages
            if message['sessionID']!= None and message['userID'] != None:
                currentSessionID = message['sessionID']
                userID = message['userID']

            logger.debug(f"Received: {message}")

            #If clients username isn't in session add them userID → serverConnection
            if message['userID'] not in activeSessions[message['sessionID']]['clients']:
                with lock:
                    activeSessions[message['sessionID']]['clients'][userID] = websocket     #Adds serverConnection to the appropriate session
                    print(activeSessions)


            match message['m_type']:
                case Protocols.Request.FOLD:
                    logger.info(f"client is folding")
                    await foldClient(websocket, message['sessionID'], userID)

                case Protocols.Request.RAISE:
                    await raiseClient(websocket, message['sessionID'], userID)

                case Protocols.Request.CHECK:
                    await clientCheck(websocket, message['sessionID'], userID)

                case Protocols.Request.CALL:
                    await clientCall(websocket, message['sessionID'], userID)

                case Protocols.Request.BAILOUT:
                    await clientBailout(websocket,message['sessionID'], userID, message['data'])

                case Protocols.Request.LEAVE:
                    #TODO:redo this so that message and update is broadcast to all players in the current game
                    await clientLeave(websocket, message['userID'], message['sessionID'])
                    print("Client has disconnected: ")
                    break
                
        except ConnectionResetError as e:   #Occurs if client or server closes connection without sending close frame
            print(f"disconnected from {websocket.remote_address}")
            await clientLeave(websocket, userID, currentSessionID)
            break

        except KeyError as e:
            error_message = template.substitute(m_type=Protocols.Response.ERROR, data=json.dumps("Invalid session ID"))
            await websocket.send(error_message.encode())

        except ConnectionClosedError as e:  #Raised when trying to interact with a closed connection
            print(f"disconnected from {websocket.remote_address}")
            await clientLeave(websocket, userID, currentSessionID)
            break

        except UnboundLocalError as e:  #Can occur if connection  is closed with no close frame received or sent
            break
        
#TODO: Look over this code cuz this might be shite
async def clientBailout(websocket, sessionID, userID, data):
    '''
    This method withdraws money from player's account wallet  and adds it to their 
    game wallet 
    1. Query redis to get users account entry
    2. Subtract the requested amount from the wallet 
    3. Update the account entry to store the new total
    '''
    logger.info("Withdrawing money from redis")
    key = f'user:{userID}'
    user = await json.loads(redisClient.get(key))
    #Add withdraw to player game wallet 
    user['wallet'] = user['wallet'] - data
    await redisClient.set(key, json.dumps(user))

    #Broadcast info all clients in the session to update their game
    logger.info("broadcast message that player has been bailed out")
    for client_writer in activeSessions[sessionID]['clients'].values():
        if client_writer != websocket:
            try:
                await client_writer.send("player has bailed out".encode())

            except ConnectionClosedError:    #If a player has disconnected 
                #Broadcast info to the other players and remove data from game and server
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID, userID)
    


async def foldClient(websocket: ServerConnection, sessionID, userID):
    print("player has folded")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]
    #game.foldPlayer()
    
    #Broadcast messages to all other players 
    logger.info("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients'].values():
        if client_writer != websocket:
            try:
                await client_writer.send("player has folded".encode())

            except ConnectionClosedError:    #If a player has disconnected 
                #Broadcast info to the other players and remove data from game and server
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID, userID)
    
    print("end of function")


async def raiseClient(websocket: ServerConnection, sessionID, userID):
    print("player has raise")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.info("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients'].values():
        if client_writer != websocket:
            try:
                await client_writer.send("player has raise the pot by __".encode())

            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID, userID)
    print("end of function")


async def clientCheck(websocket: ServerConnection, sessionID, userID):
    print("player has checked")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.info("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients'].values():
        if client_writer != websocket:
            try:
                await client_writer.send("player has checked".encode())
        
            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID, userID)

    print("end of function")

async def clientCall(websocket: ServerConnection, sessionID, userID):
    logger.info("player has called")
    #GameLogic manipulation 
    #game = games_dict[sessionID]['gameObj]

    logger.info("starting to broadcast message")
    for client_writer in activeSessions[sessionID]['clients'].values():
        if client_writer != websocket:
            try:
                await client_writer.send("player has called".encode())

            except ConnectionClosedError:
                print("client has disconnected during broadcast")
                await clientLeave(client_writer, sessionID, userID)


async def closeClient(websocket: ServerConnection, sessionID=None, redirect=False):
    #If client is in a game then invoke leaveGame()
    #else disconnect the bastard
    try:
        if sessionID in activeSessions:
            await clientLeave(websocket, sessionID, redirect)
        else:
            logger.info(f"{websocket.remote_address} has been closed")
            await websocket.close()

    except ConnectionClosed as e:
        print(f"Issue sending data to client {e}")

    except ConnectionClosedError as e:
        print(f"Issue sending data to client {e}")

    except KeyError as e:
        return
    
#TODO: Add code that sends relevant player info to DB i.e. player wallet 
async def clientLeave(websocket: ServerConnection, userID, sessionID):
    try:
        logger.info(f"user leaving: {userID}")
        await websocket.close()
        #Update game object to reflect new players 

        #Upload money to player wallet
        logger.info("Uploading players money via Redis")
        key = f'user:{userID}'
        user = json.loads(redisClient.get(key)) #entry in redis db
        #user['wallet'] += gameObj.getMoney(userID) - 500
        redisClient.set(key, json.dumps(user))

        #Upload to earnings

        with lock:
            #removed closed client from session
            activeSessions[sessionID]['clients'].pop(userID)
            logger.info(f"Current active sessions {activeSessions}")
            if len(activeSessions[sessionID]['clients']) == 0:    #Deletes session if no WebSockets are left
                    del activeSessions[sessionID]
                    logger.info(f"session {sessionID} is deleted")
                    return


            #Tell each client to remove player from their game 
            logger.info("Broadcasting change ")
            for client_writer in activeSessions[sessionID]['clients'].values():    
                #Send them the updated game state        
                await client_writer.send("player has left")

    except ConnectionClosedError as e:
        print("Error in clientLeave")
    



async def main():
    logger.info("server has started")
    async with serve(handleClient, host, port) as server:
        await server.serve_forever()
    

if __name__ == "__main__":
    try:
        #Server thread that will be using asyncio and handling messages 
        # serverThread = threading.Thread(target=lambda: asyncio.run(main()), daemon=True)
        # serverThread.start()

        asyncio.run(main())

        #Merge Thread back into the main thread
        # serverThread.join()
        print("event_loop ended")

    except KeyboardInterrupt:
        print("We are ending test")