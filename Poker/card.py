from Poker.rank import Rank
import pygame

class Card():
    def __init__(self, suit: str, rank: Rank):
        '''
        S: Spade
        C: Clubs 
        D: Diamonds
        H: Hearts 
        '''
        self._suit = suit 
        self._rank = rank 

    def getSuit(self):
        return self._suit
    
    def setSuit(self, suit):
        self._suit = suit


    def getRank(self):
        return self._rank.value
    
    def setRank(self, rank: Rank):
        self._rank = rank 

    def __str__(self):
        return str((self._suit, self._rank.name))

    suit = property(getSuit, setSuit)
    rank = property(getRank, setRank)

if __name__ == "__main__":
    der = Card("S",Rank.ACE)

    print(der)

    




# def load_card_image(card: Card):
#     
#     return pygame.transform.scale(
#         pygame.image.load("./assets/" + str(card) + ".png"),
#         scale_tuple((263 / 3, 376 / 3), scale_factor),
#     )