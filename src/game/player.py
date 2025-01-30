


from card import Card

class Player:
    """Represents a player in the game"""
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.hand = []  # Players hand
        self.currentBet = 0  # Current bet amount
        self.folded = False  # Checks if player has folded
    
    def placeBet(self, amount: int):
        """Places a bet which reduces chip count"""
        if amount > self.chips:
            raise ValueError("Not enough chips blud")
        self.chips -= amount
        self.currentBet += amount
    
    def fold(self):
        """Player folds which ends his round"""
        self.folded = True
    
    def receiveCards(self, cards: list[Card]):
        """Receives new hole cards"""
        self.hand = cards
    
    def reset(self):
        """Resets player state for next round"""
        self.currentBet = 0
        self.folded = False
        self.hand = []
