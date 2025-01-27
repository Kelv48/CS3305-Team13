import pygame, sys
from button import Button
from utils import BG, get_font, SCREEN




def single_player(main_menu):
    while True:
        SINGLE_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        # Scale the background to fit the screen
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        PLAY_TEXT = get_font(45).render("This is the SINGLE PLAYER screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(screen_width / 2, screen_height / 3))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 3), 
            text_input="BACK", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green"
        )

        PLAY_BACK.changeColor(SINGLE_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(SINGLE_MOUSE_POS):
                    main_menu()
            # Toggle fullscreen on 'F' key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()