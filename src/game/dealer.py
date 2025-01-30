


from player import Player
from deck import Deck

class Dealer:
    """Handles deck shuffling and card dealing"""
    def __init__(self):
        self.deck = Deck()
        self.community_cards = []
    
    def deal_hands(self, players: list[Player]):
        """Deals two cards to each player"""
        for player in players:
            player.receive_cards(self.deck.deal(2))
    
    def deal_community_cards(self, num: int):
        """Deals community cards (flop, turn, river)"""
        self.community_cards.extend(self.deck.deal(num))
    
    def reset_deck(self):
        """Resets and shuffles the deck"""
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []


