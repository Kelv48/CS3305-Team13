import json
import asyncio
from websockets.asyncio.client import connect,ClientConnection
from websockets.exceptions import ConnectionClosed, InvalidURI
from network.server.protocol import Protocols
from random import randint
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


    async def send(self,m_type, data):
        #Sends JSON message to server
        #m_type tells the server what kind of message it is and what actions its should except to do
        #signature is there for validation to ensure that no bad actors manipulate messages
        try:
            message = {
                'm_type':m_type, 
                'data': data,
                'sessionID': self.sessionID,  
                'signature': self.id
            }
            await self.client.send(json.dumps(message).encode())
            #TODO: write better error handling 
        except ConnectionError as e:
            print(e)
    

    async def receive(self):
        #receives JSON message from server
        try:
            message = await self.client.recv(True)
            der = json.loads(message)

            #This code should be in the game script displaying game info
            match der['m_type']:
                case Protocols.Response.REDIRECT:
                    self.disconnect()
                    #create new socket to new port
                    self.redirect('localhost', der['data']['host'], der['data']['port'])

                case Protocols.Response.SESSION_ID:
                    self.setSessionID(der['data'])


            #return json.loads(message)
            return message
         
        #TODO: write better error handling 
        except ConnectionClosed as e:
            print("whoops")
       
    #TODO: Test code
    async def redirect(self, host, port):
        #This method is for creating a new websocket to connect to the appropriate server script/port 
        await self.disconnect()
        self.client = await connect(f"ws://{host}:{port}")
        #For a secure connection need to use wss, but need to config server for SSL/TLS before we can do that 
        #For local development us ws 



    async def disconnect(self):
        #disconnects websocket
        await self.client.close()

    def resetClient(self):
        #This method is used to remove any data linking the client to a game that it may have left or disconnected from 
        self.setID(None)
        self.setSessionID(None)


    #Getters/Setters
    def getSessionID(self):
        return self.gameCode
    
    def setSessionID(self, code):
        self.gameCode = code

    def getID(self):
        return self.id 
    
    def setID(self, id):
        self.id = id 

    sessionID = property(getSessionID, setSessionID)
    id = property(getID, setID)

async def main():
    clients = []
    game_protocols = [
        Protocols.Request.RAISE, Protocols.Request.CHECK, Protocols.Request.CALL,
        Protocols.Request.FOLD, Protocols.Request.LEAVE
    ]

    matchMaking_protocols = [Protocols.Request.CREATE_GAME, Protocols.Request.JOIN_GAME, Protocols.Request.LEAVE]
    
    
    der = await Client.connect("localhost", 80 )  
    #clients.append(der)
    while True:
        # Await the connection if it's an async method
        try:
                index = input('0 or 1: ')
                m_type = matchMaking_protocols[int(index)]
                print(f"m_type: {m_type}")

                message = input("What message do you want to send: ")
                if int(index) == 0:
                    message = int(message)

                print(f"message data type {type(message)}")
                # Awaiting asynchronous send and receive methods
                await der.send(m_type, message)
                response = await der.receive()  
                print(response)

                print(der.sessionID)
        except KeyboardInterrupt:
                print(f"The number of clients: {len(clients)}")
                return  # Exit gracefully

if __name__ == '__main__':
    asyncio.run(main())  # Run the async main() function