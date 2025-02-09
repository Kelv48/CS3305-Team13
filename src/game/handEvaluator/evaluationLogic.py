# @param inputDeck: list of sets, can get replaced in class using .getValues()
def removeSuits(inputDeck):
    return [card[0] for card in inputDeck]

# @param inputDeck: list of sets, can get replaced in class using .getSuits()
def removeValues(inputDeck):
    return [card[-1] for card in inputDeck]

# @param inputDeck: list of sets, can get replaced in class using .getValues()
def valueToRank(inputDeck):
    valueDict = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
        "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }
    return [valueDict[cardValue] for cardValue in inputDeck]

def isFlush(inputDeck):
    if len(set(inputDeck)) == 1:
        return True
    else :
        return False
    
def isRoyalFlush(inputValues, inputSuits):
    if inputValues == [10, 11, 12, 13, 14] and isFlush(inputSuits):
        return True
    return False

def isStraightFlush(inputValues, inputSuits):
    if isFlush(inputSuits) and isStraight(inputValues):
        return True
    else:
        return False
    
def isStraight(rankDeck):
    """
    Checks if ranks form a consecutive sequence
    """
    sortedRanks = sorted(rankDeck)
    for i in range(len(sortedRanks) - 1):
        if sortedRanks[i + 1] - sortedRanks[i] != 1:
            return False
    return True

def is4K(rankDeck):
    """
    Checks if there are four cards of the same rank
    """
    for i in range(len(rankDeck)):
        if rankDeck.count(rankDeck[i]) == 4:
            return True
    return False

def isFullHouse(rankDeck):
    """
    Checks if there is a three of a kind and a pair
    """
    if is3K(rankDeck) and is1K(rankDeck):
        return True
    return False

def is3K(rankDeck):
    """
    Checks if there are three cards of the same rank
    """
    for i in range(len(rankDeck)):
        if rankDeck.count(rankDeck[i]) == 3:
            return True
    return False

def is2K(rankDeck):
    """
    Checks if there are two pairs of cards of the same rank
    """
    pairCount = 0
    for i in range(len(rankDeck)):
        if rankDeck.count(rankDeck[i]) == 2:
            pairCount += 1
    if pairCount == 2:
        return True
    return False

def is1K(rankDeck):
    """
    Checks if there are two cards of the same rank
    """
    for i in range(len(rankDeck)):
        if rankDeck.count(rankDeck[i]) == 2:
            return True
    return False

def getHighCard(rankDeck):
    """
    Returns the highest card in the deck
    """
    return max(rankDeck)

# @return the highest flushList
def straightFlushComparison(sF1, sF2): # sF1, sF2 -> 5 cards list each
    if sF1[-1] > sF2[-1]:
        return sF1
    elif sF1[-1] < sF2[-1]:
        return sF2
    else:
        return None
