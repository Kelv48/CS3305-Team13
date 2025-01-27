import pygame, sys
from button import Button
from utils import BG, get_font, SCREEN

def multi_player(main_menu):
    while True:
        MULTI_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        # Scale the background to fit the screen
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        MULTI_TEXT = get_font(45).render("This is the MULTI PLAYER screen.", True, "White")
        MULTI_RECT = MULTI_TEXT.get_rect(center=(screen_width / 2, screen_height / 3))
        SCREEN.blit(MULTI_TEXT, MULTI_RECT)

        MULTI_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 3), 
            text_input="BACK", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green"
        )

        MULTI_BACK.changeColor(MULTI_MOUSE_POS)
        MULTI_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MULTI_BACK.checkForInput(MULTI_MOUSE_POS):
                    main_menu()
            # Toggle fullscreen on 'F' key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()