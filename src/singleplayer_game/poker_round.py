import random
from src.singleplayer_game.game_gui.player import Player
from src.singleplayer_game.auction import auction
from src.singleplayer_game.poker_score import players_score
from src.singleplayer_game.game_gui.utils import recapRound as recap_round, splitPot, onePlayerWin, changePlayersPositions
from src.gui.utils.constants import SB, BB

def poker_round():
    """
    Play one round of poker.
    Players remain in the same on-screen (chair) positions.
    Only the roles (SB and BB) rotate one seat clockwise per round.
    This function guarantees that changePlayersPositions() is called exactly once
    at the end of the round (even for early exits).
    """
    # Fixed on-screen positions
    player_list_chair = Player.player_list_chair
    # Logical order (same order as chair) used for role assignment
    player_list = Player.player_list
    num_players = len(player_list)
    
    # Retrieve the current dealer index.
    dealer_index = Player.dealer_index  # Initially set in the Player class (e.g., -1)

    # Compute SB and BB indices.
    sb_index = (dealer_index + 1) % num_players
    bb_index = (dealer_index + 2) % num_players

    # Assign blinds.
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

    # Create a deck of cards.
    deck = [
        '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD'
    ]

    # Deal two cards to each player (screen positions remain unchanged).
    for player in player_list_chair:
        player.cards = random.sample(deck, 2)
        for card in player.cards:
            deck.remove(card)

    # Use try...finally to ensure roles are rotated exactly once.
    try:
        # Pre-flop auction.
        auction()
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return

        # Flop.
        flop = random.sample(deck, 3)
        for card in flop:
            deck.remove(card)
        auction(flop)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return

        # Turn.
        turn = random.sample(deck, 1)
        deck.remove(turn[0])
        common_cards = flop + turn
        auction(common_cards)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return

        # River.
        river = random.sample(deck, 1)
        deck.remove(river[0])
        common_cards += river
        auction(common_cards)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return

        # Final showdown.
        players_score(player_list_chair, common_cards)
        list_winner = splitPot()
        recap_round(list_winner, common_cards)
    finally:
        # This call happens exactly once per round (even if we exit early above).
        changePlayersPositions()





# def pokerRound():
#     """
#     Function play one round of dealing cards.
#     """

#     # In player_list players order will change after each round
#     player_list_chair = Player.player_list_chair
#     player_list = Player.player_list

#     # Take blinds from players
#     if player_list[-1].stack > BB:
#         player_list[-1].blind(BB)
#     else:
#         player_list[-1].blind(player_list[-1].stack)
#         player_list[-1].allin()

#     if player_list[-2].stack > SB:
#         player_list[-2].blind(SB)
#     else:
#         player_list[-2].blind(player_list[-2].stack)
#         player_list[-2].allin()

#     # Create a deck of cards
#     deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', '2S', '3S', '4S', '5S', '6S',
#             '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH',
#             'QH', 'KH', 'AH', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

#     # Deal the cards to the player
#     for player in player_list_chair:
#         player.cards = random.sample(deck, 2)
#         [deck.remove(player.cards[i]) for i in range(2)]

#     # First auction
#     auction()

#     # Check how many players are in the game and all-in
#     number_live_players = sum([player.live for player in player_list])
#     number_allin_players = sum([player.alin for player in player_list])

#     # change order decision player
#     if len(player_list_chair) == 2:
#         shift_decision = -1
#     else:
#         shift_decision = -2

#     # If there is only one player left in the game, he wins
#     if number_live_players + number_allin_players == 1:
#         list_winner = onePlayerWin()
#         recapRound(list_winner)
#     else:
#         # Flop

#         flop = random.sample(deck, 3)
#         [deck.remove(flop[i]) for i in range(3)]

#         # Change order decision players
#         changePlayersPositions(shift_decision)


#         if number_live_players > 1:
#             # Second auction
#             auction(flop)

#         # Check how many players are in the game and all-in
#         number_live_players = sum([player.live for player in player_list])
#         number_allin_players = sum([player.alin for player in player_list])

#         # If there is only one player left in the game, he wins
#         if number_live_players + number_allin_players == 1:
#             list_winner = onePlayerWin()
#             recapRound(list_winner)
#             # Return to the original position
#             changePlayersPositions(shift_decision)

#         else:
#             # Deal the cards to the turn
#             turn = random.sample(deck, 1)
#             deck.remove(turn[0])
#             common_cards = flop + turn

#             if number_live_players > 1:
#                 # Third auction
#                 auction(common_cards)

#             # Check how many players are in the game and all-in
#             number_live_players = sum([player.live for player in player_list])
#             number_allin_players = sum([player.alin for player in player_list])

#             # If there is only one player left in the game, he wins
#             if number_live_players + number_allin_players == 1:
#                 list_winner = onePlayerWin()
#                 recapRound(list_winner)
#                 # Return to the original position
#                 changePlayersPositions(shift_decision)
#             else:


#                 # Deal the cards to the river
#                 river = random.sample(deck, 1)
#                 deck.remove(river[0])
#                 common_cards += river

#                 if number_live_players > 1:
#                     # Last auction
#                     auction(common_cards)

#                 # Check how many players are in the game and all-in
#                 number_live_players = sum([player.live for player in player_list])
#                 number_allin_players = sum([player.alin for player in player_list])

#                 # If there is only one player left in the game, he wins
#                 if number_live_players + number_allin_players == 1:
#                     list_winner = onePlayerWin()
#                     recapRound(list_winner)
#                     # Return to the original position
#                     changePlayersPositions(shift_decision)
#                 else:
#                     # Calculate score players

#                     players_score(player_list_chair, common_cards)
#                     # Split pot
#                     list_winner = splitPot()
#                     recapRound(list_winner, common_cards)
#                     # Return players to the original position
#                     changePlayersPositions(shift_decision)


