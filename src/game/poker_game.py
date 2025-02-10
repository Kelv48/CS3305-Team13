from player import Player
from gameLogic import *
import random

class PokerGame:
    """Manages the poker game flow"""
    def __init__(self, players: list[Player]):
        self.players = players
        self.pot = Pot()
        self.currentBet = 0
        self.activePlayers = players[:]
        self.gameLogic = GameLogic()
        self.communityCards = []  
        self.playersCards = {} 

    def startRound(self):
        """Starts a new poker round with blinds"""
        self.currentBet = 0
        self.pot.resetPot()
        self.activePlayers = [player for player in self.players if player.chips > 0]
        self.gameLogic.activePlayers = self.activePlayers

        # Deal hole cards
        self.playersCards = self.gameLogic.preFlop()

        # Assign small and big blinds
        sb = self.activePlayers[1 % len(self.activePlayers)]  # Small blind
        bb = self.activePlayers[2 % len(self.activePlayers)]  # Big blind

        small_blind_amount = 10
        big_blind_amount = 20

        sb.placeBet(small_blind_amount)
        bb.placeBet(big_blind_amount)
        self.pot.addToPot(small_blind_amount + big_blind_amount)
        self.currentBet = big_blind_amount

        print(f"{sb.name} posts small blind ({small_blind_amount} chips)")
        print(f"{bb.name} posts big blind ({big_blind_amount} chips)")

        self.gameLogic.preFlop()

    def bettingRound(self):
        """Handles a betting round"""
        players_to_remove = []
        for player in self.activePlayers:
            if player.folded:
                continue  # Skip folded players

            actions = ["fold", "call", f"raise {self.currentBet + 10}"]
            decision = random.choice(actions)

            if decision == "fold":
                player.folded = True
                players_to_remove.append(player)
                print(f"{player.name} folds.")
            elif decision == "call":
                bet = min(self.currentBet, player.chips)
                player.placeBet(bet)
                self.pot.addToPot(bet)
                print(f"{player.name} calls with {bet} chips.")
            elif decision.startswith("raise"):
                amount = int(decision.split(" ")[1])
                raise_amount = min(amount, player.chips)
                self.currentBet = raise_amount
                player.placeBet(raise_amount)
                self.pot.addToPot(raise_amount)
                print(f"{player.name} raises to {raise_amount} chips.")

        for player in players_to_remove:
            self.activePlayers.remove(player)

    def evaluateWinner(self):
        """Determines the winner based on hand strength"""
        if len(self.activePlayers) == 1:
            winner = self.activePlayers[0]
            print(f"{winner.name} wins by default as all others folded.")
            return winner

        winner = None
        currentMax = 0
        for player in self.activePlayers:
            player_hand = self.communityCards + self.playersCards.get(player.player_id, [])
            hand_strength = hEval.handEvaluation(player_hand)  # Returns an int representing hand strength
            if hand_strength > currentMax:
                winner = player
                currentMax = hand_strength

        return winner

    def showdown(self):
        """Determines the winner at the end of the round"""
        winner = self.evaluateWinner()
        if winner:
            print(f"{winner.name} wins the pot of {self.pot.total} chips!")
            winner.chips += self.pot.total  # Award the winner
        else:
            print("No winner determined.")
        self.pot.resetPot()

    def playRound(self):
        """Plays a full poker round"""
        self.startRound()

        # Community cards and betting rounds
        self.gameLogic.dealCommunityCards(3)  # Flop
        self.communityCards = self.gameLogic.communityCards
        print(f"Community cards: {self.communityCards}")
        self.bettingRound()

        self.gameLogic.dealCommunityCards(1)  # Turn
        self.communityCards = self.gameLogic.communityCards
        print(f"Community cards: {self.communityCards}")
        self.bettingRound()

        self.gameLogic.dealCommunityCards(1)  # River
        self.communityCards = self.gameLogic.communityCards
        print(f"Community cards: {self.communityCards}")
        self.bettingRound()

        self.showdown()

if __name__ == "__main__":
    players = [Player(i, f"Player {i+1}", chips=1000) for i in range(6)]
    game = PokerGame(players)
    game.playRound()
