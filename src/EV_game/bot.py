import random
from src.gui.utils.constants import BB, GAME_MODE

class Bot:
    def __init__(self):
        self.cards = ''
        self.score = 0
        self.hand = ''

class AI:
    def __init__(self, own_cards, dict_options, call_value, min_raise, max_raise, pot, n_players, common_cards=None):
        self.own_cards = own_cards
        self.common_cards = common_cards
        self.dict_options = dict_options
        self.call_value = call_value
        self.min_raise = min_raise
        self.max_raise = max_raise
        self.pot = pot
        self.n_players = n_players

    def probabilityWin(self):
        import random
        from src.singleplayer_game.poker_score import players_score as playerScore
        number_games = 500
        n_win = 0
        n_tie = 0
        ai = Bot()
        ai.cards = self.own_cards
        deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
                '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
                '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
                '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']
        for card in ai.cards:
            deck.remove(card)
        if self.common_cards is not None:
            for card in self.common_cards:
                deck.remove(card)
        list_bots = []
        for _ in range(self.n_players - 1):
            list_bots.append(Bot())
        if not list_bots:
            return 1.0, 0.0
        for i in range(number_games):
            bot_deck = deck.copy()
            for bot in list_bots:
                bot.cards = random.sample(bot_deck, 2)
                for card in bot.cards:
                    bot_deck.remove(card)
            if self.common_cards is None:
                table = random.sample(bot_deck, 5)
            else:
                table = self.common_cards + random.sample(bot_deck, 5 - len(self.common_cards))
            playerScore(list_bots, table)
            playerScore([ai], table)
            list_score = [bot.score for bot in list_bots]
            if ai.score > max(list_score):
                n_win += 1
            elif ai.score == max(list_score):
                n_tie += 1
        return n_win / number_games, n_tie / number_games

    def decision(self):
        if GAME_MODE == "EV":
            import random
            action = random.choice(['fold', 'call', 'raise', 'all-in'])
            if action == 'raise':
                amount = random.randint(self.min_raise, self.max_raise)
                return ['raise', amount]
            return [action, 0]
        p_win, p_tie = self.probabilityWin()
        print('p win', p_win)
        if p_win > 0.5:
            return self._strong_hand_decision(BB, p_win)
        return self._weak_hand_decision(p_win, p_tie)

    def _strong_hand_decision(self, BB, p_win):
        if self.dict_options['raise']:
            factor = int(max(BB, self.pot / 8))
            rais = int((12 * p_win - 5) * factor) if p_win < 0.75 else int((-12 * p_win + 13) * factor)
            if rais < self.min_raise:
                return ['raise', self.min_raise]
            if rais > self.max_raise:
                return ['all-in', self.max_raise]
            return ['raise', rais]
        return ['all-in', self.max_raise]

    def _weak_hand_decision(self, p_win, p_tie):
        max_call = int(p_win * self.pot + (p_tie * self.pot) / self.n_players)
        if self.dict_options['check']:
            import random
            if random.randint(1, 10) > 8 and self.min_raise < max_call:
                return ['raise', min(max_call, self.max_raise)]
            return ['check', 0]
        if max_call < self.call_value:
            return ['fold', 0]
        import random
        if random.randint(1, 10) > 8 and self.min_raise < max_call:
            return ['raise', min(max_call, self.max_raise)]
        decision = 'call' if self.call_value < self.max_raise else 'all-in'
        return [decision, 0]