import random
class Deck():
    def __init__(self):
        self._deck = []            #Stack that represents the deck of cards

    
    def getTopCard(self):
        """Pops off the card at the top of the deck and returns it to caller"""
        return self._deck.pop()
    
    def addCard(self, card):
        """Adds card to Deck  """
        pass

    def shuffle(self):
        """Shuffles up deck and returns it to caller
            This generates a deck of cards. Only the minimum amount of cards needed to be generated (2 *num_of player) + 5
        """
        pass
    
    def getDeckSize(self):
        """returns the size of the deck"""
        return len(self._deck)

    
