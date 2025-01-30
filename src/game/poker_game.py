

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
        self.current_bet = 0
        self.active_players = players[:]
    
    def start_round(self):
        """Starts a new poker round"""
        self.dealer.reset_deck()  # Refresh deck
        self.dealer.deal_hands(self.players)
        self.current_bet = 0
        for player in self.players:
            player.reset()
        self.pot.reset_pot()
    
    def betting_round(self):
        """Handles a betting round"""
        for player in self.active_players:
            if not player.folded:

                # Placeholder for real betting logic
                bet = min(self.current_bet, player.chips)
                player.place_bet(bet)
                self.pot.add_to_pot(bet)
    
    def deal_flop(self):
        """Deals the first 3 community cards"""
        self.dealer.deal_community_cards(3)
    
    def deal_turn(self):
        """Deals the 4th community card"""
        self.dealer.deal_community_cards(1)
    
    def deal_river(self):
        """Deals the 5th / final community card"""
        self.dealer.deal_community_cards(1)
    
    def showdown(self):
        """Determines the winner at the end of the round"""
        # Placeholder for hand evaluation logic
        winner = random.choice(self.active_players)
        winner.chips += self.pot.total
        self.pot.reset_pot()
        print(f"{winner.name} wins the pot")
    
    def eliminate_players(self):
        """Removes players with zero chips"""
        self.players = [player for player in self.players if player.chips > 0]

