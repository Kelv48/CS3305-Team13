import random
from src.singleplayer_game.game_gui.player import Player
from src.singleplayer_game.auction import auction
from src.singleplayer_game.poker_score import players_score
from src.singleplayer_game.game_gui.utils import recapRound as recap_round, splitPot, onePlayerWin, changePlayersPositions
from src.gui.utils.constants import SB, BB

def poker_round():
    player_list_chair = Player.player_list_chair
    player_list = Player.player_list
    num_players = len(player_list)
    
    dealer_index = Player.dealer_index
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

    deck = [
        '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD'
    ]

    for player in player_list_chair:
        player.cards = random.sample(deck, 2)
        for card in player.cards:
            deck.remove(card)

    try:
        auction()
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return
        flop = random.sample(deck, 3)
        for card in flop:
            deck.remove(card)
        auction(flop)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return
        turn = random.sample(deck, 1)
        deck.remove(turn[0])
        common_cards = flop + turn
        auction(common_cards)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return
        river = random.sample(deck, 1)
        deck.remove(river[0])
        common_cards += river
        auction(common_cards)
        if sum(p.live for p in player_list) + sum(p.alin for p in player_list) == 1:
            list_winner = onePlayerWin()
            recap_round(list_winner)
            return
        players_score(player_list_chair, common_cards)
        list_winner = splitPot()
        recap_round(list_winner, common_cards)
    finally:
        changePlayersPositions()

def ev_round(round_number):
    import random, time, pygame
    from src.singleplayer_game.game_gui.player import Player
    from src.EV_game.game_gui.utils import recapRoundEV, arrangeRoom, drawPlayer
    from src.EV_game.game_gui.game_button import buttons
    from src.gui.utils.constants import SCREEN, BG

    # Simulate EV round parameters
    pot_size = random.randint(50, 500)
    num_bot_raises = random.randint(2, 5)
    bot_raises = [random.randint(10, max(10, pot_size // 3)) for _ in range(num_bot_raises)]
    total_bot_raise = sum(bot_raises)
    
    # Draw the room instead of a plain black screen.
    SCREEN.fill((0, 0, 0))
    arrangeRoom(None)   # Draw table, background and other UI elements
    drawPlayer()        # Draw player and bot labels

    # Draw round info at the top.
    font = pygame.font.Font(None, 36)
    info_text = f"Round {round_number}: Pot=${pot_size}, {num_bot_raises} bots raised (${total_bot_raise} total)"
    info_surface = font.render(info_text, True, (255, 255, 255))
    SCREEN.blit(info_surface, (50, 50))

    # Draw each bot's simulated call/raise amount.
    bot_font = pygame.font.Font(None, 24)
    # Fixed positions for up to five bots (adjust as needed)
    bot_positions = [(180, 480), (180, 160), (580, 80), (980, 160), (980, 480)]
    for i, bot in enumerate(Player.player_list_chair[1:]):
        if i < num_bot_raises:
            bot_text = f"Raise: ${bot_raises[i]}"
            pos = bot_positions[i] if i < len(bot_positions) else (100, 100)
            bot_surface = bot_font.render(bot_text, True, (255, 215, 0))
            SCREEN.blit(bot_surface, pos)

    pygame.display.flip()
    time.sleep(2)

    options = {'fold': True, 'call': True, 'raise': True, 'all-in': True, 'check': False}
    call_value = 0
    player = Player.player_list_chair[0]
    min_raise = 10
    max_raise = player.stack if player.stack > 0 else 0

    decision, chip_amount = wait_for_player_ev_decision(buttons, options, min_raise, max_raise)
    ev_change = compute_ev_outcome(decision, player.position, num_bot_raises, pot_size)
    recapRoundEV(ev_change, round_number)
    player.stack += int(ev_change)
    return ev_change


def wait_for_player_ev_decision(buttons, options, min_raise, max_raise):
    import pygame, time
    from src.EV_game.game_gui.utils import drawButtons  # helper to redraw buttons
    start = time.time()
    # Activate all buttons so they are visible and clickable.
    for button in buttons:
        button.active = True
    while True:
        # Continuously redraw the buttons.
        drawButtons(buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.isOver(pos) and button.active:
                        decision = button.name
                        amt = min_raise if decision == 'raise' else 0
                        return decision, amt
        if time.time() - start > 20:
            return 'fold', 0
        pygame.display.update()

def compute_ev_outcome(decision, position, num_raises, pot):
    import random
    if decision == 'fold':
        return -0.1 * pot
    elif decision == 'call':
        return random.uniform(-0.5, 0.5) * pot * (1 + num_raises * 0.05)
    elif decision == 'raise':
        bonus = 1 + (position / 10)
        return random.uniform(-1.0, 1.5) * pot * (1 + num_raises * 0.1) * bonus
    elif decision == 'all-in':
        bonus = 1 + (position / 10)
        return random.uniform(-1.5, 2.0) * pot * (1 + num_raises * 0.15) * bonus
    else:
        return 0