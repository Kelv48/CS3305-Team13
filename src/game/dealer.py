

""" Can just get rid of this and merge with poker_game.py """

from player import Player
from deck import Deck

class Dealer:
    """Handles deck shuffling and card dealing"""
    def __init__(self):
        self.deck = Deck()
        self.communityCards = []
    
    def dealHands(self, players: list[Player]):
        """Deals two cards to each player"""
        for player in players:
            player.receiveCards(self.deck.deal(2))
    
    def dealCommunityCards(self, num: int):
        """Deals community cards (flop, turn, river)"""
        self.dealCommunityCards.extend(self.deck.deal(num))
    
    def reset_deck(self):
        """Resets and shuffles the deck"""
        self.deck = Deck()
        self.deck.shuffle()
        self.communityCards = []


