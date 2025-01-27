import pygame, sys
from button import Button
from utils import BG, get_font, SCREEN
from single_player import single_player
from settings import settings
from multi_player import multi_player
from guide import guide


def main_menu():
    while True:
        MAIN_MOUSE_POS = pygame.mouse.get_pos()


        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) # Scale the background to fit the screen
        SCREEN.blit(scaled_bg, (0, 0))

        

        MENU_TEXT = get_font(50).render("Poker", True, "Dark Green")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Define button labels and functions
        buttons = [
            ("SINGLE PLAYER", single_player),
            ("MULTI PLAYER", multi_player),
            ("GUIDE", guide),
            ("SETTINGS", settings),
            ("QUIT", sys.exit)
        ]

        # Calculate vertical spacing with closer spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 4) # Change number bigger to make the buttons closer

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 3) * button_height        # Change number to make buttons go down on y axis
            button = Button(
                pos=(screen_width / 2, button_y), 
                text_input=text, 
                font=get_font(30), 
                base_color="White", 
                hovering_color="Light Green"
            )
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
                            action(main_menu)
            # Toggle fullscreen on 'F' key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()

main_menu()