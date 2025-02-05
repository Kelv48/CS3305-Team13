import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN

def settings(mainMenu):
    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        SETTINGS_TEXT = get_font(45).render("This is the SETTINGS screen.", True, "White")
        SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)

        SETTINGS_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 2.5), 
            text_input="BACK", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green")

        SETTINGS_BACK.changeColor(SETTINGS_MOUSE_POS)
        SETTINGS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                    mainMenu()

        pygame.display.update()