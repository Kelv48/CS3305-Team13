# src/EV_game/game_gui/utils.py
import pygame
from src.gui.utils.constants import SCREEN, GAME_BG, BEIGE, GREEN, game_font
from src.singleplayer_game.game_gui.player import Player

def recapRoundEV(ev_change, round_number):
    import time
    font = game_font(20)
    color = GREEN if ev_change >= 0 else (255, 0, 0)
    text = f"Round {round_number}: EV outcome = {ev_change:+.2f}"
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, (50, SCREEN.get_height() - 100))
    pygame.display.flip()
    time.sleep(2)

def drawButtons(buttons):
    for button in buttons:
        if button.active:
            button.draw(SCREEN)

def arrangeRoom(mainMenu, common_cards=None):
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(GAME_BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))
    try:
        poker_table_image = pygame.image.load("assets/images/Table.png")
        poker_table_image = pygame.transform.scale(poker_table_image, (700, 400))
        poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 1.9))
        SCREEN.blit(poker_table_image, poker_table_rect)
    except Exception:
        pass
    return

def drawPlayer():
    player_list_chair = Player.player_list_chair
    for player in player_list_chair:
        player.playerLabel(SCREEN)
        player.drawBet(SCREEN)
    pygame.display.flip()

def drawCustomCursor():
    """
    Draws the custom cursor image at the current mouse position.
    Call this function after all other drawing calls (i.e., at the end of your main loop)
    so that it always appears on top.
    """
    from src.gui.utils.constants import SCREEN, scaled_cursor
    current_mouse_pos = pygame.mouse.get_pos()
    SCREEN.blit(scaled_cursor, current_mouse_pos)
