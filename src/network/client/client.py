import json
import asyncio
from websockets.asyncio.client import connect,ClientConnection
from websockets.exceptions import ConnectionClosed, InvalidURI
from src.network.server.protocol import Protocols
#from protocol import Protocols
class Client(object):
    '''
    Needs to connect to server
    Request authentication 
    Receive messages from server and return them 
    Send messages to server
    Disconnect from the server in a non-volatile manner
    '''
    def __init__(self,websocket=None):
        
        self.client:ClientConnection = websocket
        self.id = None                                          #This will be the SQL id linking client to an account/ JWT??? that will act as an signature for JSON messages
        self.sessionID = None                                   #This will contain the game code associate with the game that the client is currently playing. Default: None  


    @classmethod
    async def connect(cls, host, port):
        try:
            #Creates client connection - https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html
            websocket = await connect(f"ws://{host}:{port}")  #Connects to server with the given uri. It should be to the auth server port need to further discuss it.
            return cls(websocket)
        
        except InvalidURI as e:
            print(e)


    async def send(self,m_type, data=None):
        #Sends JSON message to server
        #m_type tells the server what kind of message it is and what actions its should except to do
        #signature is there for validation to ensure that no bad actors manipulate messages
        try:
            message = {
                'm_type':m_type, 
                'data': data,
                'sessionID': self.getSessionID(),  
                'userID': self.id
            }
            await self.client.send(json.dumps(message).encode())
            print(f"{self.id} is sending {message}")
        
        #TODO: write better error handling 
        except ConnectionError as e:
            print(e)
    

    async def receive(self):
        #receives JSON message from server
        try:
            print(f"{self.id} is waiting for a message")
            message = await self.client.recv(True)
            print(f"{self.id} received message: {message}")
            der = json.loads(message)

            #This code should be in the game script displaying game info
            match der['m_type']:
                case Protocols.Response.REDIRECT:
                    #create new socket to new port
                    await self.redirect(der['data']['host'], der['data']['port'])

                case Protocols.Response.SESSION_ID:
                    self.setSessionID(der['data'])


            #return json.loads(message)
            return message
         
        #TODO: write better error handling 
        except ConnectionClosed as e:
            print("whoops")
       
 
    async def redirect(self, host, port):
        #This method is for creating a new websocket to connect to the appropriate server script/port 
        await self.disconnect()
        print("Client redirected")
        self.client = await connect(f"ws://{host}:{port}")
        #For a secure connection need to use wss, but need to config server for SSL/TLS before we can do that 
        #For local development us ws 



    async def disconnect(self):
        #disconnects websocket from server
        await self.client.send(Protocols.Request.LEAVE)
        await self.client.close()

    def resetClient(self):
        #This method is used to remove any data linking the client to a game that it may have left or disconnected from 
        self.setID(None)
        self.setSessionID(None)


    #Getters/Setters
    def getSessionID(self):
        return self.sessionID
    
    def setSessionID(self, code):
        self.sessionID = code

    def getID(self):
        return self.id 
    
    def setID(self, id):
        self.id = id 

    # sessionID = property(getSessionID, setSessionID)
    # id = property(getID, setID)

async def main():
    clients = []
    game_protocols = [
        Protocols.Request.RAISE, Protocols.Request.CHECK, Protocols.Request.CALL,
        Protocols.Request.FOLD, Protocols.Request.LEAVE
    ]

    matchMaking_protocols = [Protocols.Request.CREATE_GAME, Protocols.Request.JOIN_GAME, Protocols.Request.LEAVE]
    
        
    # Await the connection if it's an async method


#This is for testing purposes
async def test_local():
    c1, c2 = None, None  # Ensure variables exist before assignment

    try:
        #c1 = await Client.connect("84.8.144.77", 8000)  
        c1 =  await Client.connect('localhost', 80)
        await asyncio.sleep(2)

        c2  = await Client.connect("localhost", 80)
        
        await asyncio.sleep(2)

        c1.setID("c1")
        c2.setID("c2")

        await c1.send(Protocols.Request.CREATE_GAME, 3)
        await c1.receive()
        await asyncio.sleep(5)

        await c2.send(Protocols.Request.JOIN_GAME, c1.getSessionID())
        await c2.receive()
        await asyncio.sleep(2)

        await c1.send(Protocols.Request.START_GAME_EARLY_VOTE)
        await c2.send(Protocols.Request.START_GAME_EARLY_VOTE)

        await c1.receive()
        await c2.receive()

        
        await c1.receive()
        await c2.receive()

        await c1.send(Protocols.Request.CALL)

        await c2.send(Protocols.Request.FOLD)
        await asyncio.sleep(2)
        while True:
            pass

    except KeyboardInterrupt:
       
        return  # Exit gracefully
    
async def test_remote():
    c1 = None
    try:
        c1 = await Client.connect("84.8.144.77", 8000)  
        await asyncio.sleep(2)

        c1.setID("c1")
        await c1.send(Protocols.Request.CREATE_GAME, 3)
        await c1.receive()
        await asyncio.sleep(5)


    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    asyncio.run(main())  # Run the async main() function