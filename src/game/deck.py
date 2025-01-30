



class Deck:
    """Represents a deck of 52 cards"""
    suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
    
    def deal(self, num: int) -> list[Card]:
        """Deals 'num' amount of cards from the deck"""
        return [self.cards.pop() for _ in range(num)]
    
    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)




