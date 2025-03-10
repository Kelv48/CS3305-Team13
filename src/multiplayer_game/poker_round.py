import random
from src.multiplayer_game.game_gui.player import Player
from src.multiplayer_game.auction import auction
from src.multiplayer_game.poker_score import players_score
from src.multiplayer_game.game_gui.utils import recapRound as recap_round, splitPot, onePlayerWin, changePlayersPositions
from src.gui.utils.constants import SB, BB

def initialize_deck():
    """Creates and returns a shuffled deck of cards."""
    return [f'{rank}{suit}' for suit in 'CSHD' for rank in '23456789TJQKA']

# def deal_cards(deck, player_list):
#     """Distributes two cards to each player."""
#     for player in player_list:
#         player.cards = random.sample(deck, 2)
#         for card in player.cards:
#             deck.remove(card)

def deal_cards(deck, player):
    """Distributes two cards to a single player."""
    player.cards = random.sample(deck, 2)
    for card in player.cards:
        deck.remove(card)

def deal_two_cards(deck):
    """Removes two cards from the deck and returns them."""
    dealt_cards = random.sample(deck, 2)
    for card in dealt_cards:
        deck.remove(card)
    return dealt_cards

def assign_blinds(player_list, dealer_index):
    """Assigns small and big blinds."""
    num_players = len(player_list)
    sb_index = (dealer_index + 1) % num_players
    bb_index = (dealer_index + 2) % num_players
    
    sb_player = player_list[sb_index]
    bb_player = player_list[bb_index]
    
    if sb_player.stack > SB:
        sb_player.blind(SB)
    else:
        sb_player.blind(sb_player.stack)
        sb_player.allin()
    
    if bb_player.stack > BB:
        bb_player.blind(BB)
    else:
        bb_player.blind(bb_player.stack)
        bb_player.allin()

def execute_betting_round(community_cards, multiplayer_list, client):
    """Handles betting rounds and determines if the game should continue."""
    auction(community_cards, multiplayer_list, client)
    return sum(p.live for p in Player.player_list) + sum(p.alin for p in Player.player_list) > 1

def flop(deck, multiplayer_list, client):
    """Handles the flop round."""
    flop_cards = random.sample(deck, 3)
    for card in flop_cards:
        deck.remove(card)
    if not execute_betting_round(flop_cards, multiplayer_list, client):
        recap_round(onePlayerWin())
        return None
    return flop_cards

def turn(deck, common_cards, multiplayer_list, client):
    """Handles the turn round."""
    turn_card = random.sample(deck, 1)
    deck.remove(turn_card[0])
    common_cards += turn_card
    if not execute_betting_round(common_cards, multiplayer_list, client):
        recap_round(onePlayerWin())
        return None
    return common_cards

def river(deck, common_cards, multiplayer_list, client):
    """Handles the river round."""
    river_card = random.sample(deck, 1)
    deck.remove(river_card[0])
    common_cards += river_card
    if not execute_betting_round(common_cards, multiplayer_list, client):
        recap_round(onePlayerWin())
        return None
    return common_cards

def showdown(player_list, common_cards):
    """Handles the final showdown and determines the winner."""
    players_score(player_list, common_cards)
    recap_round(splitPot(), common_cards)

def poker_round(multiplayer_list, client):
    """Manages a single round of poker without UI handling."""
    player_list = Player.player_list
    dealer_index = Player.dealer_index
    
    # Assign blinds
    assign_blinds(player_list, dealer_index)
    
    # Initialize deck
    deck = initialize_deck()
    
    # Deal cards
    # deal_cards(deck, player_list)
    
    try:
        if not execute_betting_round(None, multiplayer_list, client):
            recap_round(onePlayerWin())
            return
        
        # Flop
        common_cards = flop(deck, multiplayer_list, client)
        if common_cards is None:
            return
        
        # Turn
        common_cards = turn(deck, common_cards, multiplayer_list, client)
        if common_cards is None:
            return
        
        # River
        common_cards = river(deck, common_cards, multiplayer_list, client)
        if common_cards is None:
            return
        
        # Final showdown
        showdown(player_list, common_cards)
    
    finally:
        changePlayersPositions()



