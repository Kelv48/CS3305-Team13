

from player import Player
from dealer import Dealer
from pot import Pot
import random



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
    def __init__(self, players: list[Player]):
        self.players = players
        self.dealer = Dealer()
        self.pot = Pot()
        self.currentBet = 0
        self.activePlayers = players[:]

    def startRound(self):
        """Starts a new poker round"""
        self.dealer.resetDeck()  # Refresh deck
        self.dealer.dealHands(self.players)
        self.currentBet = 0
        for player in self.players:
            player.reset()
        self.pot.resetPot()
    
    def bettingRound(self):
        """Handles a betting round"""
        for player in self.activePlayers:
            if not player.folded:

                # Placeholder for real betting logic
                bet = min(self.currentBet, player.chips)
                player.placeBet(bet)
                self.pot.addToPot(bet)
    
    def dealFlop(self):
        """Deals the first 3 community cards"""
        self.dealer.dealCommunityCards(3)
    
    def dealTurn(self):
        """Deals the 4th community card"""
        self.dealer.dealCommunityCards(1)
    
    def dealRiver(self):
        """Deals the 5th / final community card"""
        self.dealer.dealCommunityCards(1)
    
    def showdown(self):
        """Determines the winner at the end of the round"""
        # Placeholder for hand evaluation logic
        winner = random.choice(self.activePlayers)
        winner.chips += self.pot.total
        self.pot.resetPot()
        print(f"{winner.name} wins the pot")
    
    def eliminatePlayers(self):
        """Removes players with zero chips"""
        self.players = [player for player in self.players if player.chips > 0]


    # Multiplayer   
    def addPlayer(self, p):
        """Adds a new player hand to playerCards
            Might be unnecessary"""
        self.playersCards[p] = []
