# Can evaluate 7 cards at once.  @returns the hand score + hand type
from src.singleplayer_game.handEvaluation import handEvaluation as evaluateCards
from src.singleplayer_game.evaluationLogic import removeSuits, valueToRank
import itertools


def playerScore(playerList, tableCards):
    """
    Calculate and assign each player a score for his best hand made from his cards combined with the common cards.
    This function updates each player object with a 'score' and 'hand' attribute.

    Args:
        playerList (list): List of player objects. Each player must have a 'cards' attribute.
        tableCards (list): List of cards on the table.
    """

    for player in playerList:
        bestScore = 0
        bestHand = ""

        # Evaluate all possible 5-card combinations from the union of player's cards and common cards.
        for combination in itertools.combinations(tableCards + player.cards, 5):
            handScore, handName = evaluateCards(list(combination))
            if handScore > bestScore:
                bestScore = handScore
                bestHand = handName
        player.score = bestScore
        player.hand = bestHand
