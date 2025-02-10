import itertools
from collections import Counter

# Global mapping from card figures to numbers.
CARD_MAPPING = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def parseCards(cards):
    """
    Convert a list of card strings into a sorted list of figure values and a list of suits.

    Args:
        cards (list): List of card strings (e.g. ['2D', 'AH', ...]).

    Returns:
        tuple: (sorted list of figures as ints, list of suits)
    """
    figures = []
    suits = []
    for card in cards:
        # Convert the first character using the mapping (or directly if numeric) and extract suit.
        figure = int(CARD_MAPPING.get(card[0], card[0]))
        figures.append(figure)
        suits.append(card[1])
    return sorted(figures), suits


def isStraight(figures):
    """
    Check if the sorted list of card figures forms a straight.

    Args:
        figures (list): Sorted list of card figures (ints).

    Returns:
        bool: True if figures form a straight, False otherwise.
    """
    # Standard straight (consecutive numbers)
    if figures == list(range(figures[0], figures[0] + 5)):
        return True
    # Special case: Ace can act as 1 in a 5-high straight (A,2,3,4,5)
    if figures == [2, 3, 4, 5, 14]:
        return True
    return False


def hand(composition):
    """
    Calculate the score of a poker hand composition.
    The score is relative: better hands receive a higher score.

    Args:
        composition (list): List of five card strings, e.g. ['2D', '3C', 'AH', 'AC', '7D'].

    Returns:
        tuple: (score, hand ranking name)
    """
    figures, suits = parseCards(composition)
    count = Counter(figures)
    freqs = sorted(count.values(), reverse=True)
    flush = (len(set(suits)) == 1)
    straight_flag = isStraight(figures)

    # Royal Flush: 10, J, Q, K, A all in the same suit.
    if flush and figures == [10, 11, 12, 13, 14]:
        return 180, 'Royal flush'

    # Straight Flush: A straight with all cards in the same suit.
    if flush and straight_flag:
        return 160 + figures[-1], 'Straight Flush'

    # Four of a Kind: Four cards with the same figure.
    if 4 in freqs:
        four = next(val for val, cnt in count.items() if cnt == 4)
        kicker = next(val for val, cnt in count.items() if cnt == 1)
        return 140 + four + kicker / 100, 'Four of kind'

    # Full House: Three of a kind and a pair.
    if sorted(count.values()) == [2, 3]:
        triple = next(val for val, cnt in count.items() if cnt == 3)
        pair = next(val for val, cnt in count.items() if cnt == 2)
        return 120 + triple + pair / 100, 'Full house'

    # Flush: All cards are of the same suit.
    if flush:
        score = (100 +
                 figures[4] / 10 +
                 figures[3] / 100 +
                 figures[2] / 1000 +
                 figures[1] / 10000 +
                 figures[0] / 100000)
        return score, 'Flush'

    # Straight: Cards form a consecutive sequence.
    if straight_flag:
        score = 80 if figures == [2, 3, 4, 5, 14] else 80 + figures[-1]
        return score, 'Straight'

    # Three of a Kind: Three cards of the same figure.
    if 3 in freqs and len(count) == 3:
        triple = next(val for val, cnt in count.items() if cnt == 3)
        kickers = sorted((val for val, cnt in count.items() if cnt == 1), reverse=True)
        return 60 + triple + kickers[0] / 100 + kickers[1] / 1000, 'Three of kind'

    # Two Pair: Two different pairs.
    if list(count.values()).count(2) == 2:
        pairs = sorted(val for val, cnt in count.items() if cnt == 2)
        kicker = next(val for val, cnt in count.items() if cnt == 1)
        return 40 + pairs[1] + pairs[0] / 10 + kicker / 100, 'Two pair'

    # Pair: One pair.
    if len(count) == 4:
        pair = next(val for val, cnt in count.items() if cnt == 2)
        kickers = sorted((val for val, cnt in count.items() if cnt == 1), reverse=True)
        return 20 + pair + kickers[0] / 100 + kickers[1] / 10000 + kickers[2] / 100000, 'Pair'

    # High Card: None of the above.
    score = (figures[4] +
             figures[3] / 10 +
             figures[2] / 100 +
             figures[1] / 1000 +
             figures[0] / 10000)
    return score, 'High card'


def playerScore(player_list, common_cards):
    """
    Calculate and assign each player a score for his best hand made from his cards combined with the common cards.
    This function updates each player object with a 'score' and 'hand' attribute.

    Args:
        player_list (list): List of player objects. Each player must have a 'cards' attribute.
        common_cards (list): List of common card strings.
    """
    for player in player_list:
        best_score = 0
        best_hand = ''
        # Evaluate all possible 5-card combinations from the union of player's cards and common cards.
        for combination in itertools.combinations(common_cards + player.cards, 5):
            combination_score, combination_name = hand(combination)
            if combination_score > best_score:
                best_score = combination_score
                best_hand = combination_name
        player.score = best_score
        player.hand = best_hand



