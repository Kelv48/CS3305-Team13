from src.multiplayer_game.game_gui.player import Player
from src.multiplayer_game.game_gui.game_button import buttons

# Player decisions => fold, call, check, raise, all-in
from src.multiplayer_game.game_gui.utils import playerDecision, arrangeRoom, drawPlayer
from src.gui.utils.constants import BB

def auction(common_cards=None, multi_list=None):
    """
    Displays each player's available options for the auction round.
    Once a player selects an option, their attributes are updated.
    The auction ends when every player has made a decision or all but one fold.
    """
    player_list = [player for player in Player.player_list if player.live] 
    number_player = len(player_list)
    every_fold = False
    mutliplayer_list = multi_list

    while not all(player.decision for player in player_list) and not every_fold:
        for player in player_list:
            if not player.decision and player.live:
                options, call_value, min_raise, max_raise, pot = getPlayerOptions(player, player_list)
                decision, chips = getPlayerDecision(player, options, min_raise, max_raise, common_cards, call_value, pot, player_list, number_player, is_turn=True)
                processDecision(decision, chips, player, player_list)
                updateUI(common_cards)

            if checkSinglePlayerRemaining(player_list):
                every_fold = True
                break

    for player in player_list:
        player.nextAuction()
        if player.live:
            player.decision = False

def getPlayerOptions(player, player_list):
    """
    Calculate betting parameters and determine which auction options are available.
    """
    input_stack_list = [p.input_stack for p in player_list]
    bet_list = [p.bet_auction for p in player_list]

    call_value = max(input_stack_list) - player.input_stack
    
    sorted_bets = sorted(bet_list, reverse=True)
    min_raise = call_value + (sorted_bets[0] if len(sorted_bets) < 2 else sorted_bets[0] - sorted_bets[1])
    min_raise = max(min_raise, BB)
    
    max_raise = player.stack
    pot = sum(input_stack_list)
    
    options = {'fold': True, 'all-in': True, 'call': False, 'check': False, 'raise': False}
    if player.input_stack == max(input_stack_list):
        options['check'] = True
    elif player.stack > (max(input_stack_list) - player.input_stack):
        options['call'] = True
    if player.stack > min_raise:
        options['raise'] = True
    
    return options, call_value, min_raise, max_raise, pot

def getPlayerDecision(player, options, min_raise, max_raise, common_cards, call_value, pot, player_list, number_player, is_turn=False):
    """
    Get the decision from a human or AI player only when it's their turn.
    """
    decision = ('fold', None)  # Default decision
    if is_turn and player.kind == 'human':
        decision = playerDecision(buttons, options, min_raise, max_raise, common_cards)

    chips = int(decision[1]) if decision[0] == 'raise' else None
    return decision[0], chips

def processDecision(decision, chips, player, player_list):
    """
    Process the player's decision and update the player's state.
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
    player.drop(min(player.stack, required))
    if player.stack == 0:
        player.allin()

def processAllIn(player, player_list):
    player.drop(player.stack)
    resetLowerDecisions(player, player_list)
    player.allin()

def processRaise(player, chips, player_list):
    resetAllDecisions(player_list)
    player.drop(min(player.stack, chips))
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
    """Update the room and player displays."""
    arrangeRoom(common_cards)
    drawPlayer()

def checkSinglePlayerRemaining(player_list):
    sum_live = sum(1 for p in player_list if p.live)
    sum_allin = sum(1 for p in player_list if p.allin)
    return sum_live == 1 and sum_allin == 0
