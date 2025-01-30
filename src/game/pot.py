


class Pot:
    """Represents the betting pot for all users"""
    def __init__(self):
        self.total = 0
    
    def addToPot(self, amount: int):
        """Adds chips to the pot"""
        self.total += amount

    def resetPot(self):
        """Resets the pot at the end of a round"""
        self.total = 0
