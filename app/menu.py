import pygame, sys
import pygame.transform
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN, FPS

from src.gui import changePlayersPositions
from src.gui import Player
from src.gui import pokerRound
from src.gui import FPS



START_STACK = 5000

def gameMenu():
    """Starts the game loop and keeps it running consistently."""
    pygame.init()
    clock = pygame.time.Clock()
    while True:  # Outer loop to restart the game
        # Reset players for a new game
        Player.player_list_chair.clear()
        Player('Player 1', START_STACK, 'human')
        Player('Bot 1', START_STACK, 'AI')
        # Player('Bot 2', START_STACK, 'AI')
        # Player('Bot 3', START_STACK, 'AI')
        # Player('Bot 4', START_STACK, 'AI')
        # Player('Bot 5', START_STACK, 'AI')
        player_list_chair = Player.player_list_chair

        # Show start menu and get user choice
        start_choice = menuStart()
        if start_choice == "quit":
            break  # Exit the game


        # Game loop
        game_running = True
        while game_running and len(player_list_chair) > 1:
            clock.tick(FPS)
            pokerRound()
            changePlayersPositions(shift=1)
            for player in player_list_chair:
                player.nextRound()
            
            # Check for players with zero stack
            for player in player_list_chair[:]:
                if player.stack == 0:
                    rebuy = menuEnd()
                    if rebuy:
                        for p in player_list_chair:
                            p.stack = START_STACK
                    else:
                        player_list_chair.remove(player)
            
            if len(player_list_chair) == 1:
                game_running = False  # End this game session

        # After game ends, prompt to restart or quit
        restart = menuEnd()
        if not restart:
            break  # Exit the outer loop


    pygame.quit()
    sys.exit()

def menuStart():
    """Displays the start menu and returns 'play' or 'quit'."""
    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen_width, screen_height = SCREEN.get_size()

        # Draw background
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))
        
        
        # Title
        title_text = get_font(45).render("This is the GAME START screen.", True, "White")
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(title_text, title_rect)

        # Buttons
        buttons = [
            ("Play", "play"),
            ("Quit", "quit")
        ]
        button_objects = []
        button_spacing = screen_height / (len(buttons) + 3)

        # Create buttons
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 2.5) * button_spacing
            button_obj = Button(
                pos=(screen_width / 2, button_y),
                text_input=text,
                font=get_font(30),
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_obj, action in button_objects:
                    if button_obj.checkForInput(mouse_pos):
                        return action  # Return 'play' or 'quit'

        pygame.display.update()

def menuEnd():
    """Displays the end menu and returns True to restart, False to quit."""
    winner = next((player.name for player in Player.player_list_chair if player.stack != 0), "No Winner")
    SCREEN.blit(BG, (0, 0))
    font = pygame.font.SysFont('comicsans', 60)

    win_text = font.render(f'{winner} won the game!', True, "White")
    SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))

    screen_width, screen_height = SCREEN.get_size()
    
    # Buttons
    button_new_game = Button(
        pos=(screen_width / 2, 300),
        text_input="New Game",
        font=get_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None

    )
    button_exit = Button(
        pos=(screen_width / 2, 500),
        text_input="Exit",
        font=get_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None

    )
    
    waiting = True
    restart = False
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))
        
        button_new_game.changecolour(mouse_pos)
        button_new_game.update(SCREEN)
        button_exit.changecolour(mouse_pos)
        button_exit.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.checkForInput(mouse_pos):
                    restart = True
                    waiting = False
                if button_exit.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.update()
    
    return restart