

from player import Player

class AIPlayer(Player):
    """Represents an AI-controlled player"""
    def __init__(self, name: str, chips: int):
        super().__init__(name, chips)
    
    def decide_action(self, min_bet: int):
        """AI decision-making for betting"""
   



