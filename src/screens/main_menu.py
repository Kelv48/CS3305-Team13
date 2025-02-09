import pygame, sys
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN
from src.screens.single_player import difficulties
from src.screens.settings import settings
from src.screens.multi_player import multiPlayer
from src.screens.guide import guide_beginner
from src.screens.leaderboard import leaderboard
from src.screens.register import register
from src.screens.game_screen import game_screen

from src.game.menu import gameMenu

def mainMenu():
    while True:
        MAIN_MOUSE_POS = pygame.mouse.get_pos()
        screen_width, screen_height = SCREEN.get_size()

        ### 1. BLURRED BACKGROUND ###
        # First, scale the background to the screen size.
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        # To blur, downscale the background significantly then upscale it back.
        blur_scale = 1  # Adjust between 0 and 1; lower values give more blur.
        small_bg = pygame.transform.smoothscale(
            scaled_bg, 
            (max(1, int(screen_width * blur_scale)), max(1, int(screen_height * blur_scale)))
        )
        blurred_bg = pygame.transform.smoothscale(small_bg, (screen_width, screen_height))
        SCREEN.blit(blurred_bg, (0, 0))

        # Transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.2)      # 20% of screen width
        textbox_height = int(screen_height * 0.7)      # 70% of screen height
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.15)          # Start 15% down from the top

        # Create a new Surface with per-pixel alpha (using SRCALPHA).
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        # Draw a filled rounded rectangle on the textbox_surface.
        # The colour (0, 0, 0, 100) is black with an alpha value of 100 (semi-transparent).
        # Adjust the border_radius (here, 20) to control the roundness of the corners.
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        # Blit the textbox to the main screen.
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        MAIN_TEXT = get_font(50).render("Poker", True, "Dark Green")
        MAIN_RECT = MAIN_TEXT.get_rect(center=(screen_width // 2, screen_height // 9))
        SCREEN.blit(MAIN_TEXT, MAIN_RECT)

        # Define button labels and functions.
        buttons = [
            ("Bot Game", gameMenu),
            ("GAME SCREEN TEST", game_screen),
            ("REGISTER & LOGIN", register),
            ("SINGLE PLAYER", difficulties),
            ("MULTI PLAYER", multiPlayer),
            ("GUIDE", guide_beginner),
            ("SETTINGS", settings),
            ("LEADERBOARD", leaderboard),
            ("QUIT", sys.exit)
        ]

        button_count = len(buttons)
        button_spacing = textbox_height / (button_count + 1)  # Calculate spacing so buttons are evenly distributed inside the textbox.
        textbox_center_x = textbox_x + textbox_width / 2  # Center of the textbox horizontally.

        button_objects = []
        for index, (text, action) in enumerate(buttons):
            # Place each button relative to the top of the textbox.
            button_y = textbox_y + (index + 1) * button_spacing
            button = Button(
                pos=(textbox_center_x, button_y),
                text_input=text,
                font=get_font(30),
                base_colour="White",
                hovering_colour="Light Green",
                image=None)
            button.changecolour(MAIN_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(MAIN_MOUSE_POS):
                        if action == sys.exit:
                            pygame.quit()
                            sys.exit()
                        elif action == gameMenu:
                            gameMenu()
                        else:
                            action(mainMenu)


        pygame.display.update()
