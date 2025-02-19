from collections import Counter

def removeSuits(inputDeck):
    """
    Extracts the suits from the deck.
    """
    return [card[0] for card in inputDeck]

def removeValues(inputDeck):
    """
    Extracts the values from the deck (removes the suits).
    """
    return [card[1] for card in inputDeck]

def valueToRank(inputDeck):
    """
    Converts card values to numerical rank values.
    """
    valueDict = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
        "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }
    return [valueDict[cardValue] for cardValue in inputDeck]

def isFlush(inputValues, inputSuits):
    """
    Checks if the hand is a flush and returns the highest card in the flush.
    """
    if len(set(inputSuits)) == 1:
        return True, max(inputValues)  # Return True and the highest card in the flush
    return False, None

def isRoyalFlush(inputValues, inputSuits):
    """
    Checks if the hand is a royal flush and returns the highest card (Ace).
    """
    if sorted(inputValues) == [10, 11, 12, 13, 14] and len(set(inputSuits)) == 1:
        return True, None
    return False, None

def isStraightFlush(inputValues, inputSuits):
    """
    Checks if the hand is a straight flush and returns the highest card in the hand.
    """
    stateFlush, _ = isFlush(inputSuits, inputValues)
    if stateFlush and isStraight(inputValues):
        return True, max(inputValues)
    return False, None

def isStraight(rankDeck):
    """
    Checks if the hand is a straight and returns the highest card.
    """
    if sorted(rankDeck) == list(range(rankDeck[0], rankDeck[0] + 5)):
        return True, max(rankDeck)
    elif sorted(rankDeck) == [2, 3, 4, 5, 14]:
        return True, 5  # Ace acts as 1 in a 5-high straight
    return False, None

def is4K(rankDeck):
    """
    Checks if the hand is Four of a Kind, returns True and the rank of the four cards.
    """
    count = Counter(rankDeck)
    for rank, rankFrequency in count.items():
        if rankFrequency == 4:
            return True, rank
    return False, None

def isFullHouse(rankDeck):
    """
    Checks if the hand is a Full House, which is a Three of a Kind and a Pair.
    """
    state3K, rank3K = is3K(rankDeck)
    state1K, _ = is1K(rankDeck) # _ is used as a placeholder

    if state3K and state1K:
        return True, rank3K  # Return True and the rank of the three of a kind
    return False, None

def is3K(rankDeck):
    """
    Checks if the hand is Three of a Kind and returns the highest card.
    """
    count = Counter(rankDeck)
    for rank, rankFrequency in count.items():
        if rankFrequency == 3:
            return True, rank  # Return True and the rank of the three cards
    return False, None

def is2K(rankDeck):
    """
    Checks if the hand contains exactly two pairs and returns the highest card.
    """
    count = Counter(rankDeck)
    pairs = sum(1 for rankFrequency in count.values() if rankFrequency == 2)
    if pairs == 2:
        # Get all ranks that appear exactly twice (pairs)
        cardPairs = [rank for rank, rankFrequency in count.items() if rankFrequency == 2]
        # Return True and the highest rank among the two pairs
        return True, max(cardPairs)
    
    return False, None

def is1K(rankDeck):
    """
    Checks if the hand contains exactly one pair and returns the highest card.
    """
    count = Counter(rankDeck)
    for rank, rankFrequency in count.items():
        if rankFrequency == 2:
            return True, rank  # Return True and the rank of the pair
    return False, None

def getHighCard(rankDeck):
    return max(rankDeck)
