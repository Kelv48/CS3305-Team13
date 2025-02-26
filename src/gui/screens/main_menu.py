import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor
from src.gui.screens.singleplayer import singlePlayer
from src.gui.screens.settings import settings
from src.gui.screens.multiplayer import multiPlayer
from src.gui.screens.guide import guide_beginner
from src.gui.screens.leaderboard import leaderboard
from src.gui.screens.register import register, logout, load_user
from src.gui.screens.user_page import user_page
from src.gui.screens.tools import tools



def mainMenu():
    logged_in = load_user() is not None

    while True:
        MAIN_MOUSE_POS = pygame.mouse.get_pos()
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Transparent textbox
        textbox_width = int(screen_width * 0.25)
        textbox_height = int(screen_height * 0.7)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.15)

        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(textbox_surface, (0, 0, 0, 100), (0, 0, textbox_width, textbox_height), border_radius=50)
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        MAIN_TEXT = screen_font(50).render("Poker", True, "Dark Green")
        MAIN_RECT = MAIN_TEXT.get_rect(center=(screen_width // 2, screen_height // 9))
        SCREEN.blit(MAIN_TEXT, MAIN_RECT)

        # Define button labels and functions
        buttons = [
            ("USER", user_page),
            ("SINGLEPLAYER", singlePlayer),
            ("MULTIPLAYER", multiPlayer),
            ("GUIDE", guide_beginner),
            ("SETTINGS", settings),
            ("TOOLS", tools),
            ("LEADERBOARD", leaderboard),
            ("QUIT", sys.exit)
        ]

        if logged_in:
            buttons.insert(0, ("LOGOUT", logout))  # Logout button
        else:
            buttons.insert(0, ("REGISTER & LOGIN", register))

        button_count = len(buttons)
        button_spacing = textbox_height / (button_count + 1)
        textbox_center_x = textbox_x + textbox_width / 2

        button_objects = []
        #For loop draws buttons
        for index, (text, action) in enumerate(buttons):
            button_y = textbox_y + (index + 1) * button_spacing
            button = Button(
                pos=(textbox_center_x, button_y),
                text_input=text,
                font=screen_font(30),
                base_colour="White",
                hovering_colour="Light Green",
                image=None
            )
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
                        else:
                            action(mainMenu)

        SCREEN.blit(scaled_cursor, (MAIN_MOUSE_POS[0], MAIN_MOUSE_POS[1]))

        pygame.display.update()

if __name__ == "__main__":
    mainMenu()

