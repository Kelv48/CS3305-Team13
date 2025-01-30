import random
from card import Card

class Deck:
    """Represents a deck of 52 cards"""
    # suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    suits = ['C', 'D', 'H', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
    
    def shuffleDeck(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def dealCard(self):
        """Deals a card from the deck."""
        if len(self.cards) != 0:
            self.shuffleDeck()
            return self.cards.pop()
        else:
            print("Deck is empty!")