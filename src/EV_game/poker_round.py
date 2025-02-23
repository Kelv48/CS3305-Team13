# src/EV_game/poker_round.py
import random, time, pygame
from src.singleplayer_game.game_gui.player import Player
from src.EV_game.game_gui.utils import recapRoundEV, arrangeRoom, drawPlayer, drawButtons
from src.EV_game.game_gui.game_button import buttons
from src.gui.utils.constants import SCREEN, BG

def ev_round(round_number):
    pot_size = random.randint(50, 500)
    num_bot_raises = random.randint(2, 5)
    bot_raises = [random.randint(10, max(10, pot_size // 3)) for _ in range(num_bot_raises)]
    total_bot_raise = sum(bot_raises)
    
    SCREEN.fill((0, 0, 0))
    arrangeRoom(None)
    drawPlayer()

    font = pygame.font.Font(None, 36)
    info_text = f"Round {round_number}: Pot=${pot_size}, {num_bot_raises} bots raised (${total_bot_raise} total)"
    info_surface = font.render(info_text, True, (255, 255, 255))
    SCREEN.blit(info_surface, (50, 50))

    bot_font = pygame.font.Font(None, 24)
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
    player = Player.player_list_chair[0]
    min_raise = 10
    max_raise = player.stack if player.stack > 0 else 0

    decision, chip_amount = wait_for_player_ev_decision(buttons, options, min_raise, max_raise)
    ev_change = compute_ev_outcome(decision, player.position, num_bot_raises, pot_size)
    recapRoundEV(ev_change, round_number)
    player.stack += int(ev_change)
    return ev_change

def wait_for_player_ev_decision(buttons, options, min_raise, max_raise):
    import time
    start = time.time()
    for button in buttons:
        button.active = True
    while True:
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