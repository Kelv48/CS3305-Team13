import deck

class Player:
    def __init__(self, playerID: int, name: str, chips: int):
        self.playerID = playerID
        self.name = name
        self.chips = chips
        self.hand = []  # Players hand
        self.currentBet = 0  # Current bet amount
        self.folded = False  # Checks if player has folded

    def addCard(self, card: deck.Card):
        self.hand.append(card)

    def getHand(self):
        return self.hand
    
    def placeBet(self, amount: int):
        if amount > self.chips:
            raise ValueError("Not enough chips blud")
        self.chips -= amount
        self.currentBet += amount
    
    def fold(self):
        self.folded = True
    
    def reset(self):
        self.currentBet = 0
        self.folded = False
        self.hand = []

    def addChips(self, amount: int):
        if amount > 0:
            self.chips += amount
        else:
            raise ValueError("Amount must be greater than 0")

    def getPlayerName(self):
        return self.name
    def getPlayerID(self):
        return self.playerID
    

    def __str__(self):
        return f"{self.name} (Chips: {self.chips})"   
    def __repr__(self):
        return f"Player({self.playerID}, {self.name}, Chips: {self.chips})"