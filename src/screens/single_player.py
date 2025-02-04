import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN

# Global dictionary to store game settings
game_settings = {
    "difficulty": None,
    "multiplier": None,
    "number_of_players": None,
    "starting_money": None
}

def difficulties(mainMenu):
    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size() 
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Display difficulty selection text
        DIFFICULTY_TEXT = get_font(45).render("Select your difficulty.", True, "White")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        # Define button labels and functions
        buttons = [
            ("EASY", lambda: setDifficultyAndContinue(mainMenu, "Easy", 1.25)),
            ("MEDIUM", lambda: setDifficultyAndContinue(mainMenu, "Normal", 1.5)),
            ("HARD", lambda: setDifficultyAndContinue(mainMenu, "Hard", 2)),
            ("Back", mainMenu)]

        # Calculate vertical spacing with closer spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 4)

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 3) * button_height
            button = Button(
                pos=(screen_width / 2, button_y), 
                text_input=text, 
                font=get_font(30), 
                base_color="White", 
                hovering_color="Light Green"
            )
            button.changeColor(MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(MOUSE_POS):
                        action()
   
        pygame.display.update()

def setDifficultyAndContinue(mainMenu, difficulty_level, multiplier):
    # Update game settings with selected difficulty
    game_settings["difficulty"] = difficulty_level
    game_settings["multiplier"] = multiplier
    numberOfPlayers(mainMenu)

def numberOfPlayers(mainMenu):
    while True:
        NUMBER_OF_PLAYERS_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Display text for selecting number of players
        PLAYERS_TEXT = get_font(45).render("Select number of players.", True, "White")
        PLAYERS_RECT = PLAYERS_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(PLAYERS_TEXT, PLAYERS_RECT)

        # Define button labels and functions for 2 to 6 players
        buttons = [
            ("2 Players", lambda: setPlayersAndContinue(mainMenu, 2)),
            ("3 Players", lambda: setPlayersAndContinue(mainMenu, 3)),
            ("4 Players", lambda: setPlayersAndContinue(mainMenu, 4)),
            ("5 Players", lambda: setPlayersAndContinue(mainMenu, 5)),
            ("6 Players", lambda: setPlayersAndContinue(mainMenu, 6)),
            ("Back", lambda: difficulties(mainMenu))]

        # Calculate vertical spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 4)

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 3) * button_height
            button = Button(
                pos=(screen_width / 2, button_y),
                text_input=text,
                font=get_font(30),
                base_color="White",
                hovering_color="Light Green"
            )
            button.changeColor(NUMBER_OF_PLAYERS_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(NUMBER_OF_PLAYERS_MOUSE_POS):
                        action()

        pygame.display.update()

def setPlayersAndContinue(mainMenu, player_count):
    # Update game settings with selected number of players
    game_settings["number_of_players"] = player_count
    selectStartingMoney(mainMenu)

def selectStartingMoney(mainMenu):
    while True:
        MONEY_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Display text for selecting starting money
        MONEY_TEXT = get_font(45).render("Select starting money.", True, "White")
        MONEY_RECT = MONEY_TEXT.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(MONEY_TEXT, MONEY_RECT)

        # Define button labels and functions for different starting money amounts
        money_options = [100, 200, 300, 400, 500]  # Example amounts
        buttons = [(f"${amount}", lambda: setMoneyAndStartGame(mainMenu, amount)) for amount in money_options]
        buttons.append(("Back", lambda: numberOfPlayers(mainMenu)))

        # Calculate vertical spacing
        button_count = len(buttons)
        button_height = screen_height / (button_count + 4)

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 3) * button_height
            button = Button(
                pos=(screen_width / 2, button_y),
                text_input=text,
                font=get_font(30),
                base_color="White",
                hovering_color="Light Green"
            )
            button.changeColor(MONEY_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(MONEY_MOUSE_POS):
                        action()

        pygame.display.update()

def setMoneyAndStartGame(mainMenu, starting_money):
    # Update game settings with selected starting money
    game_settings["starting_money"] = starting_money
    startGame(mainMenu)

def startGame(mainMenu):
    # Use the game settings to start the game
    print(f"Starting game with settings: {game_settings}")
    # Reset game settings for the next game
    resetGameSettings()
   

def resetGameSettings():
    # Reset the game settings to default values
    game_settings["difficulty"] = None
    game_settings["multiplier"] = None
    game_settings["number_of_players"] = None
    game_settings["starting_money"] = None