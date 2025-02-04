import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN

def user_page(mainMenu):
    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        USER_TEXT = get_font(45).render("This is the USER screen.", True, "White")
        USER_RECT = USER_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(USER_TEXT, USER_RECT)

        USER_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 2.5), 
            text_input="HOME", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green")

        USER_BACK.changeColor(USER_MOUSE_POS)
        USER_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if USER_BACK.checkForInput(USER_MOUSE_POS):
                    mainMenu()

        pygame.display.update()