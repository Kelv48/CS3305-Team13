import random
from src.gui.utils.constants import BB

class Bot:
    def __init__(self):
        self.cards = ''
        self.score = 0
        self.hand = ''

class AI:
    def __init__(self, own_cards, dict_options, call_value, min_raise, max_raise, pot, n_players, common_cards=None, risk_tolerance=1.0, position="other"):
        """
        risk_tolerance: Higher values make the bot more aggressive.
        position: Should be "SB", "BB", or "other". Bots not in the blinds will call more often.
        """
        self.own_cards = own_cards      # e.g. ['2C', '3C']
        self.common_cards = common_cards
        self.dict_options = dict_options
        self.call_value = call_value
        self.min_raise = min_raise
        self.max_raise = max_raise
        self.pot = pot
        self.n_players = n_players
        self.risk_tolerance = risk_tolerance
        self.position = position

    def probabilityWin(self):
        """
        Simulates a number of games to calculate win and tie probabilities.
        Returns: (p_win, p_tie)
        """
        from src.singleplayer_game.poker_score import players_score as playerScore
        number_games = 500
        n_win = 0
        n_tie = 0

        ai = Bot()
        ai.cards = self.own_cards

        # Build the deck.
        deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
                '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
                '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
                '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

        # Remove AI's own cards.
        for card in ai.cards:
            deck.remove(card)

        # Remove any community cards already on the table.
        if self.common_cards is not None:
            for card in self.common_cards:
                deck.remove(card)

        # Create bots for opponents.
        list_bots = [Bot() for _ in range(self.n_players - 1)]
        if not list_bots:
            return 1.0, 0.0

        # Run simulations.
        for _ in range(number_games):
            bot_deck = deck.copy()
            for bot in list_bots:
                bot.cards = random.sample(bot_deck, 2)
                for card in bot.cards:
                    bot_deck.remove(card)
            if self.common_cards is None:
                table = random.sample(bot_deck, 5)
            else:
                table = self.common_cards + random.sample(bot_deck, 5 - len(self.common_cards))
            # Evaluate scores for all bots.
            playerScore(list_bots, table)
            playerScore([ai], table)
            list_score = [bot.score for bot in list_bots]
            if ai.score > max(list_score):
                n_win += 1
            elif ai.score == max(list_score):
                n_tie += 1

        return n_win / number_games, n_tie / number_games

    def expected_value(self, p_win, p_tie):
        """
        Calculates the expected value (EV) of calling.
        """
        return p_win * (self.pot + self.call_value) + p_tie * ((self.pot + self.call_value) / 2) - self.call_value

    def decision(self):
        """
        Returns a decision based on win probability, tie probability, pot odds, and expected value.
        The decision is returned as a list: [action (str), amount (int)].
        """
        p_win, p_tie = self.probabilityWin()
        print('Win probability:', p_win, 'Tie probability:', p_tie)
        ev = self.expected_value(p_win, p_tie)
        print('Expected value of call:', ev)
        
        # Compute the pot odds threshold (minimum win probability to justify a call).
        pot_odds_threshold = self.call_value / (self.pot + self.call_value) if (self.pot + self.call_value) > 0 else 0
        # Adjust based on the number of opponents and risk tolerance.
        adjusted_threshold = pot_odds_threshold * (1 + (self.n_players - 2) * 0.05) / self.risk_tolerance

        # If win probability is clearly high, use strong-hand logic.
        if p_win > adjusted_threshold + 0.1:
            return self._strong_hand_decision(p_win, ev)
        else:
            return self._weak_hand_decision(p_win, p_tie, ev)

    def _strong_hand_decision(self, p_win, ev):
        """
        Strong-hand logic: calculates an aggressive raise based on win probability and EV.
        """
        base_factor = max(BB, self.pot / 8)
        if p_win > 0.75:
            aggression = (p_win - 0.75) * 2  # More aggressive when p_win is very high.
        else:
            aggression = (p_win - 0.5) * 2
        raise_amount = int(self.min_raise + aggression * base_factor + ev * 0.05)
        if raise_amount < self.min_raise:
            raise_amount = self.min_raise
        if raise_amount > self.max_raise:
            return ['all-in', self.max_raise]
        return ['raise', raise_amount]

    def _weak_hand_decision(self, p_win, p_tie, ev):
        """
        Weak-hand logic: uses a tolerance factor to decide whether to call, raise, check, or fold.
        The tolerance factor is increased if the bot is not in the blinds.
        """
        max_call = int(p_win * self.pot + (p_tie * self.pot) / self.n_players)
        # Use a higher tolerance factor for non-SB/BB positions.
        if self.position in ["SB", "BB"]:
            tolerance_factor = 1.2  # Standard tolerance for blinds.
        else:
            tolerance_factor = 2.5  # Looser criteria for other positions.
        
        if self.dict_options.get('check', False):
            # Occasionally try to raise even when checking is allowed.
            if random.randint(1, 10) > 8 and self.min_raise < max_call:
                return ['raise', min(max_call, self.max_raise)]
            return ['check', 0]
        
        # If even with tolerance the acceptable call is below the call_value...
        if max_call * tolerance_factor < self.call_value:
            # ...if the EV is still positive, we might risk a call.
            if ev > 0:
                return ['call', 0]
            return ['fold', 0]
        
        # Occasionally try to raise instead of simply calling.
        if random.randint(1, 10) > 8 and self.min_raise < max_call:
            return ['raise', min(max_call, self.max_raise)]
        
        decision = 'call' if self.call_value < self.max_raise else 'all-in'
        return [decision, 0]
