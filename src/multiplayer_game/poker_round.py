import random
from src.multiplayer_game.game_gui.player import Player
from src.multiplayer_game.auction import auction
from src.multiplayer_game.poker_score import players_score
from src.multiplayer_game.game_gui.utils import recapRound as recap_round, splitPot, onePlayerWin, changePlayersPositions
from src.gui.utils.constants import SB, BB

def initialize_deck():
    """Creates and returns a shuffled deck of cards."""
    return [f'{rank}{suit}' for suit in 'CSHD' for rank in '23456789TJQKA']

def deal_cards(deck, player_list):
    """Distributes two cards to each player."""
    for player in player_list:
        player.cards = random.sample(deck, 2)
        for card in player.cards:
            deck.remove(card)

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
    deal_cards(deck, player_list)
    
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




# def poker_round(multiplayer_list, client_param):
#     """
#     Play one round of poker.
#     Players remain in the same on-screen (chair) positions.
#     Only the roles (SB and BB) rotate one seat clockwise per round.
#     This function guarantees that changePlayersPositions() is called exactly once
#     at the end of the round (even for early exits).
#     Multiplayer_list is a list of player usernames, it is then used in auction to determine if a player's turn is theirs or not. 
#     """
#     # Fixed on-screen positions
#     player_list_chair = Player.player_list_chair
#     # Logical order (same order as chair) used for role assignment
#     player_list = Player.player_list
#     num_players = len(player_list)
#     multiplayer_list = multiplayer_list
#     client = client_param
    
#     # Retrieve the current dealer index.
#     dealer_index = Player.dealer_index  # Initially set in the Player class (e.g., -1)

#     # Compute SB and BB indices.
#     sb_index = (dealer_index + 1) % num_players
#     bb_index = (dealer_index + 2) % num_players

#     # Assign blinds.
#     sb_player = player_list[sb_index]
#     bb_player = player_list[bb_index]

#     if sb_player.stack > SB:
#         sb_player.blind(SB)
#     else:
#         sb_player.blind(sb_player.stack)
#         sb_player.allin()

#     if bb_player.stack > BB:
#         bb_player.blind(BB)
#     else:
#         bb_player.blind(bb_player.stack)
#         bb_player.allin()

#     # Create a deck of cards.
#     deck = [
#         '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
#         '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
#         '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
#         '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD'
#     ]

#     if client.getSessionID() == multiplayer_list[0]:    #If user is player one send deck
#         # Deal two cards to each player (screen positions remain unchanged).
#         for player in player_list_chair:
#             player.cards = random.sample(deck, 2)
#             client.send(None, {'player':player})
#             for card in player.cards:
#                 deck.remove(card)
#     else:
#         #Blocks the code waiting for the message
#         client.receive()

#     # Use try...finally to ensure roles are rotated exactly once.
#     # if client.getSessionID() == multiplayer_list[0]:
#     try:
#         if client.getID() == multiplayer_list[0]:
#             # Pre-flop auction.
#             auction(None, multiplayer_list, client)
#             if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
#                 list_winner = onePlayerWin()
#                 recap_round(list_winner)
#                 return
#         else: 
#             # Pre-flop auction.
#             auction(None, multiplayer_list, client)
#             if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
#                 list_winner = onePlayerWin()
#                 recap_round(list_winner)
#                 return
                            

#         if client.getID() == multiplayer_list[0]:
#             # Flop.
#             flop = random.sample(deck, 3)
#             for card in flop:
#                 deck.remove(card)
#             auction(flop, multiplayer_list, client)
#             if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
#                 list_winner = onePlayerWin()
#                 recap_round(list_winner)
#                 return

#         if client.getID() == multiplayer_list[0]:
#             # Turn.
#             turn = random.sample(deck, 1)
#             deck.remove(turn[0])
#             common_cards = flop + turn
#             auction(common_cards, multiplayer_list, client)
#             if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
#                 list_winner = onePlayerWin()
#                 recap_round(list_winner)
#                 return
        
#         if client.getID() == multiplayer_list[0]:
#             # River.
#             river = random.sample(deck, 1)
#             deck.remove(river[0])
#             common_cards += river
#             auction(common_cards, multiplayer_list, client)
#             if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
#                 list_winner = onePlayerWin()
#                 recap_round(list_winner)
#                 return

#         # Final showdown.
#         players_score(player_list_chair, common_cards)
#         list_winner = splitPot()
#         recap_round(list_winner, common_cards)
#     finally:
#         # This call happens exactly once per round (even if we exit early above).
#         changePlayersPositions()