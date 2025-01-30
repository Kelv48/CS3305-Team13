

from player import Player

class AIPlayer(Player):
    """Represents an AI-controlled player"""
    def __init__(self, name: str, chips: int):
        super().__init__(name, chips)
    
    def decideAction(self, minBet: int):
        """AI decision-making for betting"""
   



