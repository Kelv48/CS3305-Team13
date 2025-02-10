import deck, player, handEvaluation as hEval

class GameLogic():
    def __init__(self):
        self.ready = False          #Boolean value that is true if game is ready to be played (all players have joined)
        #self.playerWent = "LL"      #Idea is that each index represents a player there will be a func that will dynamically add boolean 
        self.communityCards = []    #Array containing community cards
        self.playersCards = {} 
        self.gameDeck = deck.Deck()       
        self.activePlayers = []     #List of players that are still in the game

    def preFlop(self):
        for player in self.activePlayers:
            player.addCard(self.gameDeck.dealCard())
            player.addCard(self.gameDeck.dealCard())
            print(f"Player {player.getPlayerName()} cards: {player.getHand()}")

    def dealCommunityCards(self, num):
        "Deals a specified number of community cards"
        for _ in range(num):
            self.communityCards.append(self.gameDeck.dealCard())

    def collect(self):
        """Removes cards from players possession"""
        pass

    def evaluateWinner(self):
        winner = None
        currentMax = 0
        for player in self.activePlayers:
            if player.player_id not in self.playersCards:  
                continue
            player_hand = self.communityCards + self.playersCards[player.player_id]
            hand_strength = hEval.handEvaluation(player_hand) # Returns an int of players hand strength
            if hand_strength > currentMax:
                winner = player
                currentMax = hand_strength
        if not self.activePlayers:
            print("All players folded. No showdown.")
            return None 
        return winner

    def reset(self):
        """resets variables for new round"""
        pass

    def addPlayer(self, player):
        """Adds a new player hand to playerCards
            Might be unnecessary"""
        self.playersCards[player.player_id] = []


# Pot only exists when game logic exist, game logic only exists if the game is started, hence pot only exists if and only if the game is ran
class Pot:
    """Represents the poker pot that accumulates bets."""
    
    def __init__(self):
        self.total = 0  # Total chips in the pot
    
    def addToPot(self, amount: int):
        """Adds chips to the pot."""
        self.total += amount

    def distributePot(self, winners: list):
        """Distributes the pot among winners.
        If there are multiple winners, the pot is split evenly.
        """
        if not winners:
            print("No winners to distribute the pot to.")
            return

        split_amount = self.total // len(winners)
        remainder = self.total % len(winners)  # Handle odd chip distribution
        
        for winner in winners:
            winner.chips += split_amount

        # Give leftover chips to the first winner (if any)
        if remainder > 0:
            winners[0].chips += remainder

        print(f"Pot of {self.total} chips split among {len(winners)} players.")
        self.resetPot()

    def resetPot(self):
        """Resets the pot for a new round."""
        self.total = 0
