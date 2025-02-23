import itertools

def hand(composition):
    handFigure = [card[0] for card in composition]
    handColor = [card[1] for card in composition]
    dict_figure = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    handFigure = [dict_figure.get(handFigure[i], handFigure[i]) for i in range(5)]
    handFigure = sorted([int(handFigure[i]) for i in range(5)])
    if [handFigure[i] - handFigure[0] for i in range(5)] == [0, 1, 2, 3, 4] or handFigure == [2, 3, 4, 5, 14]:
        straight = True
    else:
        straight = False
    if handFigure == [10, 11, 12, 13, 14] and len(set(handColor)) == 1:
        score = 180
        name_poker_hand = 'Royal flush'
    elif straight is True and len(set(handColor)) == 1:
        score = 160 + handFigure[4]
        name_poker_hand = "Straight Flush"
    elif handFigure.count(handFigure[2]) == 4:
        if handFigure.count(handFigure[0]) == 1:
            score = 140 + handFigure[1] + handFigure[0] / 100
        else:
            score = 140 + handFigure[0] + handFigure[4] / 100
        name_poker_hand = 'Four of kind'
    elif len(set(handFigure)) == 2 and handFigure.count(handFigure[2]) != 4:
        if handFigure.count(handFigure[0]) == 2:
            score = 120 + handFigure[2] + handFigure[0] / 100
        else:
            score = 120 + handFigure[0] + handFigure[3] / 100
        name_poker_hand = "Full house"
    elif len(set(handColor)) == 1:
        score = 100 + handFigure[4] / 10 + handFigure[3] / 100 + handFigure[2] / 1000 + handFigure[1] / 10000 + handFigure[0] / 100000
        name_poker_hand = "Flush"
    elif straight is True:
        if handFigure == [2, 3, 4, 5, 14]:
            score = 80
        else:
            score = 80 + handFigure[4]
        name_poker_hand = "Straight"
    elif handFigure.count(handFigure[2]) == 3 and len(set(handFigure)) == 3:
        handFigure_set = list(set(handFigure))
        handFigure_set.remove(handFigure[2])
        score = 60 + handFigure[2] + handFigure_set[1] / 100 + handFigure_set[0] / 1000
        name_poker_hand = 'Three of kind'
    elif handFigure.count(handFigure[1]) == 2 and handFigure.count(handFigure[3]) == 2:
        handFigure_set = list(set(handFigure))
        handFigure_set.remove(handFigure[1])
        handFigure_set.remove(handFigure[3])
        score = 40 + handFigure[3] + handFigure[1] / 10 + handFigure_set[0] / 100
        name_poker_hand = "Two pair"
    elif len(set(handFigure)) == 4:
        if handFigure.count(handFigure[1]) == 2:
            handFigure_set = list(set(handFigure))
            handFigure_set.remove(handFigure[1])
            score = 20 + handFigure[1] + handFigure_set[2] / 100 + handFigure_set[1] / 10000 + handFigure_set[0] / 100000
        elif handFigure.count(handFigure[3]) == 2:
            handFigure_set = list(set(handFigure))
            handFigure_set.remove(handFigure[3])
            score = 20 + handFigure[3] + handFigure_set[2] / 100 + handFigure_set[1] / 10000 + handFigure_set[0] / 100000
        name_poker_hand = "Pair"
    elif len(set(handFigure)) == 5:
        score = handFigure[4] + handFigure[3] / 10 + handFigure[2] / 100 + handFigure[1] / 1000 + handFigure[0] / 10000
        name_poker_hand = "High card"
    return score, name_poker_hand

def players_score(player_list, common_cards):
    for player in player_list:
        best_score, best_hand = 0, ''
        cards_combinations = list(itertools.combinations(common_cards + player.cards, 5))
        for combination in cards_combinations:
            combination_score, combination_name = hand(combination)
            if combination_score > best_score:
                best_score = combination_score
                player.score, player.hand = best_score, combination_name