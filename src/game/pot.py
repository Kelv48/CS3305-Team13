


class Pot:
    """Represents the betting pot for all users"""
    def __init__(self):
        self.total = 0
    
    def add_to_pot(self, amount: int):
        """Adds chips to the pot"""
        self.total += amount

    def reset_pot(self):
        """Resets the pot at the end of a round"""
        self.total = 0
