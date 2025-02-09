import random

from src.game.player import Player
from src.game.pokerScore import playerScore

# Test, how many rounds should be played to see which probability given hand is to win flop
deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']


start_stack = 100
Player1 = Player('Player 1', start_stack, 0)
Bot1 = Player('Bot 1', start_stack, 1)
players_list = [Player1, Bot1]



Player1.cards = ['JC', '5C']

number_round = 5000
n_win = 0
n_tie = 0
history = [i for i in range(number_round)]
history_win = [0 for _ in range(number_round)]

flop = ['2D', '9D', 'AD']
for i in range(number_round):
    deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
            '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
            '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
            '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

    Bot1.cards = random.sample(deck, 2)
    [deck.remove(Bot1.cards[i]) for i in range(2)]

    table = random.sample(deck, 2)
    [deck.remove(table[i]) for i in range(2)]
    table += flop

    playerScore(players_list, table)
    if Player1.score > Bot1.score:
        n_win += 1
    elif Player1.score == Bot1.score:
        n_tie += 1

    history_win[i] = n_win / (i + 1)
print(history_win[number_round-1])


'''
import matplotlib.pyplot as plt
import numpy as np

#mean = np.mean(history_win[5000:])
#median = np.median(history_win[5000:])
mean = np.mean(history_win[1000:])
median = np.median(history_win[1000:])
print('mean: ', mean * 100)
print('median: ', median * 100)

#plt.plot(history[5000:], history_win[5000:])
plt.axhline(y=mean, color='blue', linestyle='--')
plt.axhline(y=median, color='black', linestyle=':')
plt.plot(history, history_win)
plt.xlabel('number of rounds')
plt.ylabel('percent of wins')
plt.show()

'''
