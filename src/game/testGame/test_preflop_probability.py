import random
import time

from src.game.player import Player
from src.game.pokerScore import playerScore

# Test, how many rounds should be played to see which probability given hand is to win pre-flop
deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']


start = time.time()
start_stack = 100
Player1 = Player('Player1', start_stack)
Bot1 = Player('Bot1', start_stack)
players_list = [Player1, Bot1]

Player1.cards = ['AC', 'AD']

number_round = 5000
n_win = 0
n_tie = 0

for i in range(number_round):
    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
            '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
            '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
            '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

    Bot1.cards = random.sample(deck, 2)
    [deck.remove(Bot1.cards[i]) for i in range(2)]
    table = random.sample(deck, 5)
    [deck.remove(table[i]) for i in range(5)]
    playerScore(players_list, table)
    if Player1.score > Bot1.score:
        n_win += 1
    elif Player1.score == Bot1.score:
        n_tie += 1
stop = time.time()

print(n_win / number_round)

print('Time: ', stop - start)

