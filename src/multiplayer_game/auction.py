from src.multiplayer_game.game_gui.player import Player
from src.multiplayer_game.game_gui.game_button import buttons
import pickle

from src.multiplayer_game.game_gui.utils import playerDecision, arrangeRoom, drawPlayer
<<<<<<< HEAD
from src.gui.utils.constants import BB, RED, SCREEN, game_font
import pygame
=======
import time
>>>>>>> 7f13688833a75241e830a6b9364c74a131d5001e


def auction(common_cards=None, multi_list=None):
    """
    Displays each player's available options for the auction round.
    """
<<<<<<< HEAD
    player_list = [player for player in Player.player_list if player.live] 
    number_player = len(player_list)
    every_fold = False
    mutliplayer_list = multi_list

=======
    player_list = [player for player in Player.player_list if player.live]
    client = c_param
    user_turn = client.getID()
    every_fold = False
    
>>>>>>> 7f13688833a75241e830a6b9364c74a131d5001e
    while not all(player.decision for player in player_list) and not every_fold:
        for player in player_list:
            if player.name == user_turn and not player.decision and player.live:
                options, call_value, min_raise, max_raise, pot = getPlayerOptions(player, player_list)
                decision, chips = getPlayerDecision(player, options, min_raise, max_raise, common_cards, call_value, pot, player_list)
                processDecision(decision, chips, player, player_list)
                updateUI(common_cards)
                
                if checkSinglePlayerRemaining(player_list):
                    every_fold = True
                    break
                
                client.send(pickle.dumps(player))
            else:
                print("Not your turn")

    for player in player_list:
        player.nextAuction()
        if player.live:
            player.decision = False
        client.send(pickle.dumps(player))

def getPlayerOptions(player, player_list):
    """
    Determine available auction options for a player.
    """
    input_stack_list = [p.input_stack for p in player_list]
    bet_list = [p.bet_auction for p in player_list]
    
    call_value = max(input_stack_list) - player.input_stack
    sorted_bets = sorted(bet_list, reverse=True)
<<<<<<< HEAD
    if len(sorted_bets) < 2:
        min_raise = call_value + (sorted_bets[0] if sorted_bets else 0)
    else:
        min_raise = call_value + sorted_bets[0] - sorted_bets[1]
    if min_raise < BB:
        min_raise = BB

=======
    min_raise = call_value + (sorted_bets[0] - sorted_bets[1] if len(sorted_bets) > 1 else sorted_bets[0] if sorted_bets else 0)
>>>>>>> 7f13688833a75241e830a6b9364c74a131d5001e
    max_raise = player.stack
    pot = sum(input_stack_list)
    
    options = {'fold': True, 'all-in': True, 'call': False, 'check': False, 'raise': False}
    if player.input_stack == max(input_stack_list):
        options['check'] = True
    elif player.stack >= call_value:
        options['call'] = True
    if player.stack >= min_raise:
        options['raise'] = True
    
    return options, call_value, min_raise, max_raise, pot

def getPlayerDecision(player, options, min_raise, max_raise, common_cards, call_value, pot, player_list):
    """
    Get the player's decision with a timeout mechanism.
    """
<<<<<<< HEAD
    if player.kind == 'human':
        decision = playerDecision(buttons, options, min_raise, max_raise, common_cards)
    else:
        # ... existing AI decision code ...
        
        # Display AI decision on screen
        decision_text = f"{player.name} {decision[0]}"
        if decision[0] == 'raise':
            decision_text += f" ${decision[1]}"
        text_surface = game_font(20).render(decision_text, True, RED)
        
        # Position the text based on player position
        text_positions = {
            0: (580, 450),
            1: (360, 400),
            2: (380, 300),
            3: (580, 280),
            4: (780, 300),
            5: (800, 400)
        }
        player_index = player_list.index(player)
        text_pos = text_positions.get(player_index, (580, 450))
        
        SCREEN.blit(text_surface, text_pos)
        pygame.display.flip()
        pygame.time.delay(1000)  # Show the decision for 1 second

    # decision is expected to be a two-element sequence; extract chips if needed
=======
    decision = None
    start_time = time.time()
    timeout = 15  # 30-second limit
    
    while time.time() - start_time < timeout:
        if player.kind == 'human':
            decision = playerDecision(buttons, options, min_raise, max_raise, common_cards)
            if decision:
                break
    
    if not decision:
        decision = ('fold', None)  # Auto-fold if timeout
    
>>>>>>> 7f13688833a75241e830a6b9364c74a131d5001e
    chips = int(decision[1]) if decision[0] == 'raise' else None
    return decision[0], chips

def processDecision(decision, chips, player, player_list):
    """
    Update the player's state based on their decision.
    """
    if decision == 'call':
        processCall(player, player_list)
    elif decision == 'fold':
        player.fold()
    elif decision == 'check':
        player.decision = True
    elif decision == 'all-in':
        processAllIn(player, player_list)
    elif decision == 'raise':
        processRaise(player, chips, player_list)

def processCall(player, player_list):
    required = max(p.input_stack for p in player_list) - player.input_stack
    player.drop(min(required, player.stack))
    if player.stack == 0:
        player.allin()

def processAllIn(player, player_list):
    player.drop(player.stack)
    resetLowerDecisions(player, player_list)
    player.allin()

def processRaise(player, chips, player_list):
    resetAllDecisions(player_list)
    player.drop(min(chips, player.stack))
    if player.stack == 0:
        player.allin()

def resetLowerDecisions(player, player_list):
    for p in player_list:
        if p.live and p.decision and p.input_stack < player.input_stack:
            p.decision = False

def resetAllDecisions(player_list):
    for p in player_list:
        if p.live and p.decision:
            p.decision = False

def updateUI(common_cards):
    arrangeRoom(common_cards)
    drawPlayer()

def checkSinglePlayerRemaining(player_list):
    """
    Check if only one live, non-all-in player remains.
    """
    live_players = [p for p in player_list if p.live]
    return len(live_players) == 1 and not any(p.allin for p in live_players)
