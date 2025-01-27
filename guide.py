import pygame, sys
from button import Button
from utils import BG, get_font, SCREEN

def guide(main_menu):
    while True:
        GUIDE_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        # Scale the background to fit the screen
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        GUIDE_TEXT = get_font(45).render("This is the GUIDE screen.", True, "White")
        GUIDE_RECT = GUIDE_TEXT.get_rect(center=(screen_width / 2, screen_height / 3))
        SCREEN.blit(GUIDE_TEXT, GUIDE_RECT)

        GUIDE_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 3), 
            text_input="BACK", 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green"
        )

        GUIDE_BACK.changeColor(GUIDE_MOUSE_POS)
        GUIDE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GUIDE_BACK.checkForInput(GUIDE_MOUSE_POS):
                    main_menu()
            # Toggle fullscreen on 'F' key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

        pygame.display.update()