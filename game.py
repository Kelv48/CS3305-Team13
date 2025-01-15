from deck import Deck
class Game():
    def __init__(self):
        self.ready = False          #Boolean value that is true if game is ready to be played (all players have joined)
        self.playerWent = "LL"      #Idea is that each index represents a player there will be a func that will dynamically add boolean 
        self.communityCards = []    #Array containing community cards
        self.playersCards = {}      #Stores player cards {id:[card]} pairs 
        self.deck = Deck()          

    def preFlop(self):
        """hands out 2 cards to player """
        pass

    def flop(self):
        """reveals/draws three community cards """
        pass

    def dealTurnCard(self):
        """reveals/draws 4th community card """
        pass

    def dealRiverCard(self):
        """reveals/draws 5th community card """
        pass

    def collect(self):
        """Removes cards from players possession"""
        pass

    def winner(self):
        """evaluates players cards and determines a winner"""
        pass

    def reset(self):
        """resets variables for new round"""
        pass

    def addPlayer(self, p):
        """Adds a new player hand to playerCards
            Might be unnecessary"""
        self.playersCards[p] = []
