from player import Player
import random
import deck 
import handEvaluation as hEval 

""" 
    Game starts
    Dealer is set to P1
    Small blind is set to P2  
    Big blind is set to P3 --- Big blind is 2x the small blind
    And then dealer, Small blind and Big blind are incremented by 1
    SB and BB are forced to bet the small blind and big blind

    4 Betting rounds
    Every player dealt two hole cards
    Player 1 can fold, call, or raise
    Player 2-6 does the same / can also reraise 

    These steps repeat until 4 betting rounds are complete
    - Preflop
    - Flop
    - Turn
    - River

    If draw then split pot
"""

class PokerGame:
    """Manages the poker game flow"""

    def __init__(self, players):
        self.ready = False          #Boolean value that is true if game is ready to be played (all players have joined)
        #self.playerWent = "LL"      #Idea is that each index represents a player there will be a func that will dynamically add boolean 
        self.communityCards = []    #Array containing community cards
        self.gameDeck = deck.Deck()       
        self.activePlayers = []     #List of players that are still in the game
        self.players = players
        self.pot = Pot()
        self.currentBet = 0


    def startRound(self):
        """Starts a new poker round"""
        self.currentBet = 0
        self.pot.resetPot()
        self.activePlayers = [player for player in self.players if player.chips > 0]
        self.gameLogic.activePlayers = self.activePlayers
        self.gameLogic.preFlop()
    

    def bettingRound(self):
        """Handles a betting round"""
        for player in self.activePlayers:
            if not player.folded:
                actions = ["fold", "call", f"raise {self.currentBet + 10}"]
                decision = random.choice(actions)

                if decision == "fold":
                    player.folded = True
                    self.activePlayers.remove(player)
                elif decision == "call":
                    bet = min(self.currentBet, player.chips)
                    player.placeBet(bet)
                    self.pot.addToPot(bet)
                    print(f"{player.name} calls with {bet} chips.")  # Debugging print
                elif decision.startswith("raise"):
                    amount = int(decision.split(" ")[1])
                    raise_amount = min(amount, player.chips)
                    self.currentBet = raise_amount
                    player.placeBet(raise_amount)
                    self.pot.addToPot(raise_amount)
                    print(f"{player.name} raises to {raise_amount} chips.")  # Debugging print
   
    def evaluateWinner(self):
        winner = None
        currentMax = 0
        for player in self.activePlayers:
            if player.player_id not in self.players:  
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
    
    def showdown(self):
        """Determines the winner at the end of the round"""
        winner = self.evaluateWinner()
        if winner:
            print(f"{winner} wins the pot of {self.pot.total} chips!")
            winner.chips += self.pot.total  # Make sure the winner gets the pot
        else:
            print("No winner determined.")  # Debugging print
        self.pot.resetPot()
    

    # def eliminatePlayers(self):
    #     """Removes players with zero chips"""
    #     self.players = [player for player in self.players if player.chips > 0]


    def playRound(self):
        """Plays a full poker round"""
        self.startRound()

        # Community cards and betting rounds
        self.gameLogic.dealCommunityCards(3) # Flop
        print(f"Community cards: {self.gameLogic.communityCards}")
        self.bettingRound()
        self.gameLogic.dealCommunityCards(1) # Turn
        print(f"Community cards: {self.gameLogic.communityCards}")
        self.bettingRound()
        self.gameLogic.dealCommunityCards(1) # River
        print(f"Community cards: {self.gameLogic.communityCards}")
        self.bettingRound()

        # Showdown and elimination
        self.showdown()

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
       


if __name__ == "__main__":
    players = [Player(i, f"Player {i+1}", chips=1000) for i in range(6)]
    # Start game
    game = PokerGame(players)
    # Play one round
    game.playRound()