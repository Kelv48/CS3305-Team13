import socket
import json
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

    def send(self,m_type, data):
        #Sends JSON message to server
        #m_type tells the server what kind of message it is and what actions its should except to do
        #signature is there for validation to ensure that no bad actors manipulate messages
        message = {
            "m_type":m_type, 
            "data": data, 
            "signature": self.id
        }
        self.client.send(json.dumps(message).encode())
    

    def receive(self):
        #receives JSON message from server
        message = self.client.recv(1024).decode()
        return json.loads(message)
       
    def disconnect(self):
        self.client.close()


    def getCards(self):
        return self.clientHand
    
    def setHand(self, hand):
        self.clientHand = hand

if __name__ == "__main__":
    der = Client("localhost", 80)
    der.send("test", "How are we")
    while True:
        try:
            message = input("Type a message: ")
            der.send("test", message)
            print(der.receive())
        except KeyboardInterrupt:
            break