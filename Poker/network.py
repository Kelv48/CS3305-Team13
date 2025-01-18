import websockets

class Network(object):
    def __init__(self):
        self.server = "[INSERT IP OF SERVER]"
        self.port = "[INSERT PORT NUMBER]"
        self.addr = (self.server, self.addr)
        #self.client This will be the socket that is used to send messages to server 
        self.p = self.connect() #Connects to server. The server response by assigning a player number which determines if player is p1, p2, etc

    def getP(self):
        return self.p
    
    def connect(self):
        """Connects client to server and returns a player ID"""
        # Tries to connect to server with self.addr
        # Returns the response from the server 
        
        pass

    def send(self, data):
        """Sends message to server"""
        pass
