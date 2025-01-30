




class Card:
    """ Represents a single playing card """
    def __init__(self, suit: str, rank: str):
        self.suit = suit  # Clubs, Diamonds, Hearts, Spades --- C, D, H, S
        self.rank = rank  # 2-14 --- 2-T, J, Q, K, A
    
    def __repr__(self):
        return f"{self.rank}{self.suit[0]}"   # Example: 2C, 3D, 4H, 5S
    
    def getSuit(self):
        return self.suit
    
    def getRank(self):
        rankDict = {
            2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 
            8: "8", 9: "9", 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"
        }
        return rankDict[self.rank]