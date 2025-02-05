from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
import json
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
    async def __init__(self, host_ip, port):
        #Creates client connection
        #https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html
        self.client = await connect(f"wss://{host_ip}:{port}") #Connects to server with the given uri. It should be to the auth server port need to further discuss it.
        self.id = None                          #This will be the SQL id linking client to an account/ JWT??? that will act as an signature for JSON messages
        self.sessionID = None                   #This will contain the game code associate with the game that the client is currently playing. Default: None  


    def send(self,m_type, data):
        #Sends JSON message to server
        #m_type tells the server what kind of message it is and what actions its should except to do
        #signature is there for validation to ensure that no bad actors manipulate messages
        message = {
            'm_type':m_type, 
            'data': data,
            'sessionID': self.sessionID,  
            'signature': self.id
        }
        self.client.send(json.dumps(message).encode())
    

    def receive(self):
        #receives JSON message from server
        try:
            message = self.client.recv(True)
            der = json.loads(message)

            #This code should be in the game script displaying game info
            if der['m_type'] == Protocols.Response.REDIRECT:
                self.disconnect()
                #create new socket to new port
                self.redirect('localhost', der['data'])

            elif der['m_type'] == Protocols.Response.SESSION_ID:
                self.setSessionID(der['data'])


            #return json.loads(message)
            return message
        except ConnectionClosed as e:
            print("fuck")
       
    def redirect(self, host, port):
        #This method is for creating a new websocket to connect to the appropriate server script/port 
        self.client

    def disconnect(self):
        #disconnects websocket
        self.client.close()

    def getSessionID(self):
        return self.gameCode
    
    def setSessionID(self, code):
        self.gameCode = code

    def getID(self):
        return self.id 
    
    def setID(self, id):
        self.id = id 

if __name__ == '__main__':
    
    clients = []
    protocols = [Protocols.Request.RAISE, Protocols.Request.CHECK, Protocols.Request.CALL, Protocols.Request.FOLD, 
                  Protocols.Request.LEAVE]
    while True:
        der = Client("localhost", 80)
        clients.append(der)
        for client in clients:
            try:
                m_type = protocols[randint(0, len(protocols)-1)]
                print(f"m_type: {m_type}")
                message = input('Type a message: ')
                der.send(m_type, message)
                print(der.receive())
            except KeyboardInterrupt:
                print(f"The number of clients {len(clients)}")
                break