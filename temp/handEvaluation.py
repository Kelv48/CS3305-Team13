from src.game.evaluationLogic import *

def handEvaluation(inputDeck): 
    values = removeSuits(inputDeck)
    suits = removeValues(inputDeck)
    rankDeck = valueToRank(values)

    # Check for Royal Flush
    stateRF, _ = isRoyalFlush(rankDeck, suits)
    if stateRF:
        return 1260, "Royal Flush"

    # Check for Straight Flush
    stateSF, cardRank = isStraightFlush(rankDeck, suits)
    if stateSF:
        return 1120 + cardRank, "Straight Flush"

    # Check for Four of a Kind
    state4K, cardRank = is4K(rankDeck)
    if state4K:
        return 980 + cardRank, "Four of a Kind"

    # Check for Full House
    stateFH, cardRank = isFullHouse(rankDeck)
    if stateFH:
        return 840 + cardRank, "Full House"

    # Check for Flush
    stateF, cardRank = isFlush(suits, rankDeck)
    if stateF:
        return 700 + cardRank, "Flush"

    # Check for Straight
    stateS, cardRank = isStraight(rankDeck)
    if stateS:
        return 560 + cardRank, "Straight"

    # Check for Three of a Kind
    state3K, cardRank = is3K(rankDeck)
    if state3K:
        return 420 + cardRank, "Three of a Kind"

    # Check for Two Pairs
    state2K, cardRank = is2K(rankDeck)
    if state2K:
        return 280 + cardRank, "Two Pairs"

    # Check for One Pair
    state1K, cardRank = is1K(rankDeck)
    if state1K:
        return 140 + cardRank, "One Pair"

    # # Otherwise, High Card
    return getHighCard(rankDeck), "High Card"
