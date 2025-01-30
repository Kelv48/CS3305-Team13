import socket
import json
from protocol_temp import Protocols
from random import randint
class Client(object):
    '''
    Needs to connect to server
    Request authentication 
    Receive messages from server and return them 
    Send messages to server
    Disconnect from the server in a non-volatile manner
    '''
    def __init__(self, host_ip, port):
        #Creates a TCP socket that supports IPv4 & IPv6
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        #Connects client to server
        self.client.connect((host_ip, port))
        self.id = None       #This will be the SQL id linking client to an account/ JWT??? that will act as an signature for JSON messages
        self.clientHand = [] #List that will hold the cards sent by server
        self.gameCode = 1 #This will contain the game code associate with the game that the client is currently playing. Default: None  


    def send(self,m_type, data):
        #Sends JSON message to server
        #m_type tells the server what kind of message it is and what actions its should except to do
        #signature is there for validation to ensure that no bad actors manipulate messages
        message = {
            'm_type':m_type, 
            'data': data,
            'gameID': self.gameCode,  
            'signature': self.id
        }
        self.client.send(json.dumps(message).encode())
    

    def receive(self):
        #receives JSON message from server
        message = self.client.recv(1024).decode()
        #return json.loads(message)
        return message
       
    def disconnect(self):
        self.client.close()


    def getCards(self):
        return self.clientHand
    
    def setHand(self, hand):
        self.clientHand = hand

    def getGameCode(self):
        return self.gameCode
    
    def setGameCode(self, code):
        self.gameCode = code

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