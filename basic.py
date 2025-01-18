# Card.py 
import random

class Card():
    def __init__(self, suit, value, img):
        self.suit = suit
        self.value = value
        self.img = None

    def __repr__(self):
        valueNames = {11 : "J", 12 : "Q", 13 : "K", 14 : "A"}
        valueStr = valueNames.get(self.value, str(self.value))
        return f"{valueStr} of {self.suit}"
    
    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
# Tests
flush_hand = [
    Card('H', 2, None),
    Card('H', 3, None),
    Card('H', 4, None),
    Card('H', 5, None),
    Card('H', 6, None),
]

non_flush_hand = [
    Card('H', 2, None),
    Card('H', 4, None),
    Card('H', 6, None),
    Card('D', 8, None),
    Card('C', 10, None),
] 

class Deck():
    def __init__(self):
        self.suits = ['H', 'D', 'C', 'S']
        self.values = list(range(2, 15)) 
        self.deck = self.createDeck()
        self.img = None

    def createDeck(self):
        return [Card(suit, value, None) for suit in self.suits for value in self.values]
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        if not self.deck:
            raise IndexError("Deck is empty")
        return self.deck.pop()
    
    # Test method
    def reset(self):
        self.deck = self.createDeck()
        self.shuffle()

    def __repr__(self):
        return f"Deck with {len(self.deck)} cards remaining."
    
    def remainingCards(self):
        return len(self.deck)


# Yang Code
def isFlush(Deck): 
    state = False
    flushCount = 0 # Must be 4 or greater to qualify for a flush
    ranks = []
    for card in Deck:
        ranks.append(card.getValue())
    ranks.sort() # Sort the cards in ascending order
    
    for i in range(len(ranks) - 1, 0, -1): # Range: start stop step
        if ranks[i] - ranks[i - 1] != 1: # If the difference between the two cards is not 1 then it's not a flush
            flushCount = 0 # Reset the flush counter to 0 as it breaks the steps
        else:
            flushCount += 1
    
    # flushCount >= 4 means that there are 5 cards in a row
    if flushCount >= 4:
        state = True
    else:
        state = False

    return state

# ahh = Deck()
# deck = ahh.createDeck()
# state = isFlush(deck)
# print(state) 



# Flush test
print("Flush Hand Test:")
print(flush_hand) 
print(isFlush(flush_hand)) 

# Non-flush test
print("\nNon-Flush Hand Test:")
print(non_flush_hand) 
print(isFlush(non_flush_hand))  

    # Methods from Yang's card class that i believe should be standalone or as part of the game class 
    #     def combineCards(playerCards, tableCards):
    #     combinedCards = []
    #     for card in playerCards:
    #         combinedCards.append(card)
    #     for card in tableCards:
    #         combinedCards.append(card)
        
    #     return combinedCards
    
    # def removeSuits(inputDeck):
    #     deckWithoutSuits = []
    #     for card in inputDeck:
    #         for key in card:
    #             deckWithoutSuits.append(key)
    #     return deckWithoutSuits



# Tests
# deck = Deck()
# print(deck)  
# deck.shuffle()
# card1 = deck.deal()
# print(f"Dealt card: {card1}")  
# card2 = deck.deal()
# print(f"Dealt card: {card2}")  
# print(deck)  
# deck.reset()
# print(deck)  