import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN

def sound(mainMenu):
    while True:
        SOUND_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        SOUND_width, SOUND_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (SOUND_width, SOUND_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        SOUND_TEXT = get_font(45).render("This is the SOUND screen.", True, "White")
        SOUND_RECT = SOUND_TEXT.get_rect(center=(SOUND_width / 2, SOUND_height / 8))
        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        SOUND_BACK = Button(
            pos=(SOUND_width / 2, SOUND_height * 2 / 2.5), 
            text_input="HOME", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green")

        SOUND_BACK.changeColor(SOUND_MOUSE_POS)
        SOUND_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SOUND_BACK.checkForInput(SOUND_MOUSE_POS):
                    mainMenu()

        pygame.display.update()