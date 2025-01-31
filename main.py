import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN
from single_player import difficulties
from src.gui.settings import settings
from src.gui.multi_player import multiPlayer
from src.gui.guide import guide
from leaderboard import leaderboard
from register import register, load_user, logout_user


def mainMenu():
    while True:
        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        SCREEN.blit(scaled_bg, (0, 0))
        
        # Calculate positions based on current screen size
        MAIN_TEXT = get_font(50).render("Poker", True, "Dark Green")
        MAIN_RECT = MAIN_TEXT.get_rect(center=(screen_width / 2, screen_height / 9))
        SCREEN.blit(MAIN_TEXT, MAIN_RECT)

        username = load_user()

        if username:
            login_text = f"LOGOUT"
            login_action = logout_user
        else:
            login_text = "REGISTER & LOGIN"
            login_action = register


        # Define button labels and functions
        buttons = [
            (login_text, login_action),
            ("SINGLE PLAYER", difficulties),
            ("MULTI PLAYER", multiPlayer),
            ("GUIDE", guide),
            ("SETTINGS", settings),
            ("LEADERBOARD", leaderboard),
            ("QUIT", sys.exit)]

        # Calculate vertical spacing with closer spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 3) # Change number bigger to make the buttons closer

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 2.5) * button_height        # Change number bigger to make buttons go down on y axis
            button = Button(
                pos=(screen_width / 2, button_y), 
                text_input=text, 
                font=get_font(30), 
                base_color="White", 
                hovering_color="Light Green")
            
            button.changeColor(MAIN_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
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

        # Update the display
        pygame.display.update()

mainMenu()