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

card = [2, 2, 2, 3, 4, 5, 6]

print(isStraight(card)) # True