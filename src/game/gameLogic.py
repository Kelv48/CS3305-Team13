import ai_player, dealer, deck, player
import handEvaluation as hEval

class GameLogic():
    def __init__(self):
        self.ready = False          #Boolean value that is true if game is ready to be played (all players have joined)
        self.playerWent = "LL"      #Idea is that each index represents a player there will be a func that will dynamically add boolean 
        self.communityCards = []    #Array containing community cards
        self.playersCards = []     
        self.gameDeck = deck.Deck()       
        self.activePlayers = []     #List of players that are still in the game

    def preFlop(self):
        for p in self.activePlayers:
            card1 = self.gameDeck.dealCard()
            card2 = self.gameDeck.dealCard()
            p.addCard(card1)
            p.addCard(card2)

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


# Pot only exists when game logic exist, game logic only exists if the game is started, hence pot only exists if and only if the game is ran
class Pot:
    """Represents the betting pot for all users"""
    def __init__(self):
        self.total = 0
    
    def addToPot(self, amount: int):
        """Adds chips to the pot"""
        self.total += amount

    def resetPot(self):
        """Resets the pot at the end of a round"""
        self.total = 0