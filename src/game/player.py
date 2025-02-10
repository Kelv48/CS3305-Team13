import deck

class Player:
    __slots__ = ['player_id', 'name', 'chips', 'hand', 'folded']
    
    def __init__(self, player_id: int, name: str, chips: int):
        self.player_id = player_id
        self.name = name
        self.chips = chips
        self.hand = []  # Players hand
        self.folded = False  # Checks if player has folded

    def addCard(self, card: deck.Card):
        self.hand.append(card) #find a way to add just the rank and suit

    def getHand(self):
        return self.hand
    
    def placeBet(self, amount: int):
        if amount > self.chips:
            amount = self.chips
            print("Nice try, you don't have enough chips. All in!")
        self.chips -= amount
        return amount
    
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
        return self.player_id
    

    def __str__(self):
        return f"{self.name} (Chips: {self.chips})"   
    def __repr__(self):
        return f"Player({self.playerID}, {self.name}, Chips: {self.chips})"