import pygame, sys, json, os
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN
from src.gui.user_page import user_page

# Define the temporary JSON file for the leaderboard.
LEADERBOARD_FILE = "temp_leaderboard.json"

def load_leaderboard():
    """
    Loads the leaderboard data from a JSON file.
    If the file doesn't exist, create it with default data.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        # Default temporary leaderboard data
        default_data = [
            {"username": "Player1", "tokens": 150},
            {"username": "Player2", "tokens": 100},
            {"username": "Player3", "tokens": 200}
        ]
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    else:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
        return data

def save_leaderboard(data):
    """
    Saves the leaderboard data to the JSON file.
    """
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

def leaderboard(mainMenu):
    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        # Scale the background to fit the current screen size.
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        SCREEN.blit(scaled_bg, (0, 0))

        # Create a transparent textbox with rounded edges.
        textbox_width = int(screen_width * 0.9)
        textbox_height = int(screen_height * 0.8)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.10)
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100),   # Black with alpha=100 (semi-transparent)
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Draw the "Leaderboard" title.
        title_text = get_font(50).render("Top Earners", True, "Dark Green")
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(title_text, title_rect)

        # Load leaderboard data from our temporary JSON file.
        leaderboard_data = load_leaderboard()

        # Display each leaderboard entry within the textbox.
        entry_font = get_font(30)
        for i, entry in enumerate(leaderboard_data):
            # Format each entry as "Rank. Username - Tokens"
            entry_str = f"{i+1}. {entry['username']} - {entry['tokens']}"
            entry_surface = entry_font.render(entry_str, True, "White")
            # Position entries with a margin and spacing.
            entry_x = textbox_x + 20  # 20 pixels from the left edge of the textbox.
            entry_y = textbox_y + 50 + i * 40  # Starting 50 pixels down from the top.
            SCREEN.blit(entry_surface, (entry_x, entry_y))

        # Define buttons with their labels and associated actions.
        buttons = [
            ("USER", user_page),
            ("HOME", mainMenu)
        ]

        # Calculate vertical spacing for the buttons.
        button_count = len(buttons)
        button_height = screen_height / (button_count + 3)

        # Create and display buttons.
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 3) * button_height
            button = Button(
                pos=(screen_width / 2, button_y), 
                text_input=text, 
                font=get_font(30), 
                base_colour="White", 
                hovering_colour="Light Green",
                image=None
            )
            button.changecolour(SETTINGS_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Process events (clicks, quits, etc.).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(SETTINGS_MOUSE_POS):
                        # Depending on the action associated with the button, call the function.
                        if action == sys.exit:
                            pygame.quit()
                            sys.exit()
                        elif action == mainMenu:
                            mainMenu()
                        else:
                            action(mainMenu)

        # Update the display.
        pygame.display.update()
