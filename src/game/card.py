




class Card:
    """ Represents a single playing card """
    def __init__(self, suit: str, rank: str):
        self.suit = suit  # Clubs, Diamonds, Hearts, Spades --- C, D, H, S
        self.rank = rank  # 2-14 --- 2-T, J, Q, K, A
    
    def __repr__(self):
        return f"{self.rank}{self.suit[0]}"   # Example: 2C, 3D, 4H, 5S



