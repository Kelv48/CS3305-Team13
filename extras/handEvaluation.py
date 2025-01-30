from itertools import combinations
from evaluationLogic import *

def handEvaluation(inputDeck):  # takes 7 cards as input
    """
    Evaluates a hand to determine if it qualifies for a flush, royal flush, or straight flush.
    Returns the strongest hand's point value or None if no flush exists.
    """
    strongestHand = None

    # Get all possible combinations of 5 cards
    allCombinations = list(combinations(inputDeck, 5))

    for c in allCombinations: # each combination is a tuple
        c = list(c) # Convert tuple to list for manipulation
        rankDeck = valueToRank(removeSuits(c)) # Convert card values to ranks
        suitDeck = removeValues(c) # Extract suits
        highestCardRank = max(rankDeck)

        if isFlush(suitDeck): # Flush check
            if isRoyalFlush(rankDeck, suitDeck): # Royal flush check
                return handToPoints("RF", highestCardRank)
            elif isStraightFlush(rankDeck, suitDeck): # Straight flush check
                currentHandPoints = handToPoints("SF", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
        else:
            if is4K(rankDeck): # 4K
                currentHandPoints = handToPoints("4K", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif isFullHouse(rankDeck): # Full House
                currentHandPoints = handToPoints("FH", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif isFlush(suitDeck): # Flush
                currentHandPoints = handToPoints("F", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif isStraight(rankDeck): # Straight
                currentHandPoints = handToPoints("S", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif is3K(rankDeck): # 3K
                currentHandPoints = handToPoints("3K", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif is2K(rankDeck): # 2K
                currentHandPoints = handToPoints("2K", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            elif is1K(rankDeck): # 1K
                currentHandPoints = handToPoints("1K", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints
            else: # High Card
                currentHandPoints = handToPoints("HC", highestCardRank)
                if strongestHand is None or strongestHand < currentHandPoints:
                    strongestHand = currentHandPoints

    return strongestHand


# @return int -> power of hand
def handToPoints(stringHand, cardRank):
    match stringHand:
        case "RF": # Royal Flush
            return 126
        case "SF": # Straight Flush
            return 112 + cardRank
        case "4K": # Four of a Kind
            return 98 + cardRank
        case "FH": # Full House
            return 84 + cardRank
        case "F": # Flush
            return 70 + cardRank
        case "S": # Straight 
            return 56 + cardRank
        case "3K": # Three of a Kind, 3x K -> 3K
           return 42 + cardRank
        case "2K": # Two Pair of two of a kind, 2x K -> 2K
            return 28 + cardRank
        case "1K": # One Pair of two of a kind, 1x K -> 1K
            return 14 + cardRank
        case "HC": # High Card
            return cardRank