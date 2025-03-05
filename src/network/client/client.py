import json
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed, InvalidURI
from src.network.server.protocol import Protocols

class Client:
    def __init__(self, websocket=None):
        self.client = websocket
        self.id = None
        self.sessionID = None

    @classmethod
    def connect(cls, host, port):
        try:
            websocket = connect(f"ws://{host}:{port}")
            return cls(websocket)
        except InvalidURI as e:
            print(e)

    def send(self, m_type, data=None):
        try:
            message = {
                'm_type': m_type,
                'data': data,
                'sessionID': self.getSessionID(),
                'userID': self.id
            }
            self.client.send(json.dumps(message).encode())
            print(f"{self.id} is sending {message}")
        except ConnectionError as e:
            print(e)

    def receive(self):
        try:
            print(f"{self.id} is waiting for a message")
            message = self.client.recv()
            print(f"{self.id} received message: {message}")
            der = json.loads(message)
            
            match der['m_type']:
                case Protocols.Response.REDIRECT:
                    self.redirect(der['data']['host'], der['data']['port'])
                case Protocols.Response.SESSION_ID:
                    self.setSessionID(der['data'])
            
            return der['data']
        except ConnectionClosed as e:
            print("Client connection closed")

    def redirect(self, host, port):
        self.disconnect()
        print("Client redirected")
        self.client = connect(f"ws://{host}:{port}")

    def disconnect(self):
        self.client.send(Protocols.Request.LEAVE)
        self.client.close()

    def resetClient(self):
        self.setID(None)
        self.setSessionID(None)

    def getSessionID(self):
        return self.sessionID
    
    def setSessionID(self, code):
        self.sessionID = code

    def getID(self):
        return self.id 
    
    def setID(self, id):
        self.id = id 

# Testing synchronous version
def test_local():
    c1, c2 = None, None
    try:
        c1 = Client.connect('localhost', 80)
        c2 = Client.connect("localhost", 80)
        
        c1.setID("c1")
        c2.setID("c2")
        
        c1.send(Protocols.Request.CREATE_GAME, 3)
        c1.receive()
        
        c2.send(Protocols.Request.JOIN_GAME, c1.getSessionID())
        c2.receive()
        
        c1.send(Protocols.Request.START_GAME_EARLY_VOTE)
        c2.receive()
        
        c2.send(Protocols.Request.START_GAME_EARLY_VOTE)
        c1.receive()
        
        c1.receive()
        c2.receive()
        
        c1.send(Protocols.Request.CALL)
        c2.send(Protocols.Request.FOLD)
        
        while True:
            pass
    except KeyboardInterrupt:
        return  

def test_remote():
    c1 = None
    try:
        c1 = Client.connect("84.8.144.77", 8000)
        c1.setID("c1")
        await c1.send(Protocols.Request.CREATE_GAME, 3)
        await c1.receive()
        await asyncio.sleep(5)


    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    asyncio.run(main())  # Run the async main() function