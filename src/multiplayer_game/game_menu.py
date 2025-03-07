import pygame
import pygame.transform
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, FPS, scaled_cursor
from src.multiplayer_game.game_gui.player import Player
from src.multiplayer_game.poker_round import poker_round

screen_width = 1280
screen_height = 720
START_STACK = 5000

def gameMenu(mainMenu, playerList, client):
    """Starts the game loop and keeps it running consistently."""
    pygame.init()
    multiplayer_list = playerList # list of str
    # player_1 = player_list[0]
    clock = pygame.time.Clock()

    # Define the home button rectangle (assumed same as in arrangeRoom)
    home_button_rect = pygame.Rect(10, 10, 150, 50)  # (x, y, width, height)

    while True:  # Outer loop to restart the game
        # Reset players for a new game
        Player.player_list_chair.clear()

        # Show start menu and get user choice
        start_choice = menuStart(mainMenu)

        if start_choice == "HOME":
            mainMenu()   # Return to home screen if "HOME" is chosen
            return

        # Create a lobby of players
        for i in range(len(multiplayer_list)):
            Player(multiplayer_list[i], START_STACK, 'human', False)

        game_running = True
        while game_running and len(Player.player_list_chair) > 1:
            clock.tick(FPS)

            # Handle events (including checking for Home button clicks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button_rect.collidepoint(event.pos):
                        mainMenu()  # Go to home screen if the Home button is pressed
                        return

            # Execute a round of poker and update player positions
            poker_round(multiplayer_list) # takes in multiplayer_list to check if it is the player's turn
            for player in Player.player_list_chair:
                player.nextRound()

            # Check for players with zero stack and offer a rebuy or exit to home menu.
            for player in Player.player_list_chair[:]:
                if player.stack == 0:
                    rebuy = menuEnd(mainMenu)
                    if rebuy:
                        for p in Player.player_list_chair:
                            p.stack = START_STACK
                    else:
                        Player.player_list_chair.remove(player)

            if len(Player.player_list_chair) == 1:
                game_running = False  # End this game session

        # After the game session ends, prompt to restart or exit (to main menu)
        restart = menuEnd(mainMenu)
        if not restart:
            mainMenu()  # Exit to mainMenu if user did not choose "New Game"
            return



def menuStart(mainMenu):
    """Displays the start menu and returns a choice: number of bots or 'quit'."""
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Draw background
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))
        
        # Create a semi-transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.25)
        textbox_height = int(screen_height * 0.7)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.15)

        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Title text
        title_text = screen_font(45).render("This is the GAME START screen.", True, "White")
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(title_text, title_rect)

        # Buttons definition
        buttons = [
            ("2 Players", 2),
            ("3 Players", 3),
            ("4 Players", 4),
            ("5 Players", 5),
            ("6 Players", 6),
            ("HOME", mainMenu)
        ]
        button_objects = []
        button_spacing = textbox_height / (len(buttons) + 0.5)
        textbox_center_x = textbox_x + textbox_width / 2

        # Create and update buttons
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 2) * button_spacing
            button_obj = Button(
                pos=(textbox_center_x, button_y),
                text_input=text,
                font=screen_font(30),
                base_colour="White",
                hovering_colour="Light Green",
                image=None
            )
            button_obj.changecolour(mouse_pos)
            button_obj.update(SCREEN)
            button_objects.append((button_obj, action))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainMenu()  # Instead of quitting, call mainMenu
                return  # Return after calling mainMenu
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_obj, action in button_objects:
                    if button_obj.checkForInput(mouse_pos):
                        if action == "quit":
                            mainMenu()  # Call mainMenu if the "Quit" button is clicked
                            return "quit"
                        else:
                            return action
                        
        # *** Draw the custom cursor last so it’s always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)


        pygame.display.update()

def menuEnd(mainMenu):
    """Displays the end menu and returns True to restart or exits to mainMenu."""
    winner = next((player.name for player in Player.player_list_chair if player.stack != 0), "No Winner")
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))
    font = screen_font(60)

    win_text = font.render(f'{winner} won the game!', True, "White")
    SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))

    # Define buttons for "New Game" and "Exit"
    button_new_game = Button(
        pos=(screen_width / 2, 300),
        text_input="NEW GAME",
        font=screen_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None
    )
    button_exit = Button(
        pos=(screen_width / 2, 500),
        text_input="HOME",
        font=screen_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None
    )

    restart = False    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))
        
        button_new_game.changecolour(mouse_pos)
        button_new_game.update(SCREEN)
        button_exit.changecolour(mouse_pos)
        button_exit.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainMenu()  # Call mainMenu if the window is closed
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.checkForInput(mouse_pos):
                    restart = True
                    waiting = False
                if button_exit.checkForInput(mouse_pos):
                    mainMenu()  # Call mainMenu if "Exit" is clicked
                    return False
                

        # *** Draw the custom cursor last so it’s always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)

        
        pygame.display.update()
    
    return restart
