import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS


from src.singleplayer_game.game_menu import gameMenu


def singlePlayer(mainMenu):
    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        SINGLE_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        SCREEN.blit(scaled_bg, (0, 0))



        # Transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.25)      # 20% of screen width
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
            (0, 0, 0, 150), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        # Blit the textbox to the main screen.
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))


        
        # Calculate positions based on current screen size
        SINGLE_TEXT = screen_font(50).render("SINGLEPLAYER", True, "Gold")
        SINGLE_RECT = SINGLE_TEXT.get_rect(center=(screen_width / 2, screen_height / 9))
        SCREEN.blit(SINGLE_TEXT, SINGLE_RECT)

        # Define button labels and functions
        buttons = [
            ("BOT GAME", gameMenu),
            ("HOME", mainMenu)]

        # Calculate vertical spacing with closer spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 1.2) # Change number bigger to make the buttons closer

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 1.5) * button_height        # Change number bigger to make buttons go down on y axis
            button = Button(
                pos=(screen_width / 2, button_y), 
                text_input=text, 
                font=screen_font(30), 
                base_colour="White", 
                hovering_colour="Gold",
                image=None)
            
            button.changecolour(SINGLE_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(SINGLE_MOUSE_POS):
                        if action == sys.exit:
                            pygame.quit()
                            sys.exit()
                        elif action == gameMenu:
                            gameMenu(mainMenu)
                        else:
                            action()

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (SINGLE_MOUSE_POS[0], SINGLE_MOUSE_POS[1]))

        # Update the display
        pygame.display.update()
