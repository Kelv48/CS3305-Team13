import json
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed, InvalidURI
from src.multiplayer_game.network.server.protocol import Protocols

class Client:
    def __init__(self, websocket=None):
        self.client = websocket
        self.id = None
        self.sessionID = None
        self.create_game_screen = None
        self.lobby_screen = None
        self.main_menu = None
        self.join_game_screen = None
        self.loading_screen = None

    def set_loading_screen(self, action):
        self.loading_screen = action

    def set_create_game_screen(self, action):
        self.create_game_screen = action

    def set_main_menu(self, action):
        self.main_menu = action

    def load_main_menu(self):
        self.main_menu()

    def set_lobby_screen(self, action):
        self.lobby_screen = action

    def set_join_game_screen(self, action):
        self.join_game_screen = action

    def run_game(self, option):
        if option == 0:
            self.create_game_screen()
        if option == 1:
            self.join_game_screen()
        if option == 2:
            self.loading_screen()


        msg = self.receive()
        match msg['m_type']:
            case Protocols.Response.START_GAME_EARLY_VOTE:
                vote_start_count = int(msg['data'])

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
            message = self.client.recv(10)
            #print(f"{self.id} received message: {message}")
            der = json.loads(message)
            
            match der['m_type']:
                case Protocols.Response.REDIRECT:
                    self.redirect(der['data']['host'], der['data']['port'])
                case Protocols.Response.SESSION_ID:
                    self.setSessionID(der['data'])
            
            return der
        except ConnectionClosed as e:
            print("Client connection closed")

        #If no message is received within time-limit
        except TimeoutError as e:
            print("AAAAAA I'M FUCKING OFF RECEIVING THE MESSAGE ")
            return

    def redirect(self, host, port):
        self.disconnect()
        print("Client redirected")
        self.client = connect(f"ws://{host}:{port}")

    def disconnect(self):
        self.client.send(Protocols.Request.LEAVE)
        self.resetClient()
        self.client.close()

    def resetClient(self):
        self.setSessionID(None)

    def getSessionID(self):
        return self.sessionID
    
    def setSessionID(self, code):
        self.sessionID = code

    def getID(self):
        return self.id 
    
    def setID(self, id):
        self.id = id 

def test_local():
    c1, c2 = None, None
    try:
        c1 = Client.connect('localhost', 80)
        c2 = Client.connect("localhost", 80)
        
        c2.setID("c2")
        c2.send(Protocols.Request.JOIN_GAME, "BQN/V0")
        c2.receive()
        
        c2.send(Protocols.Request.START_GAME_EARLY_VOTE)
        c2.receive()
        c2.receive()
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
        c1.send(Protocols.Request.CREATE_GAME, 3)
        c1.receive()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    test_local()