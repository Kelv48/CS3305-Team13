from src.game import ai_player, card, dealer, deck, player, pot
import handEvaluation as hEval

class GameLogic():
    def __init__(self):
        self.ready = False          #Boolean value that is true if game is ready to be played (all players have joined)
        self.playerWent = "LL"      #Idea is that each index represents a player there will be a func that will dynamically add boolean 
        self.communityCards = []    #Array containing community cards
        self.playersCards = []     
        self.deck = deck.Deck()       
        self.activePlayers = []     #List of players that are still in the game

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

    def evaluateWinner(self):
        winner = None
        currentMax = 0
        for player in self.activePlayers:
            player.hand = self.communityCards + self.playersCards[player]
            player.hand = hEval.handEvaluation(player.hand) # Returns an int of players hand strength
            if player.hand > currentMax:
                winner = player.getName()
                currentMax = player.hand
        return winner

    def reset(self):
        """resets variables for new round"""
        pass

    def addPlayer(self, p):
        """Adds a new player hand to playerCards
            Might be unnecessary"""
        self.playersCards[p] = []