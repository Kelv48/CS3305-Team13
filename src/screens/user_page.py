import pygame, sys, json, os
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN

# Define the temporary JSON file for user data.
USER_DATA_FILE = "temp_user_data.json"

def load_user_data():
    """
    Loads the user data from a JSON file. If the file does not exist,
    create it with default values.
    """
    if not os.path.exists(USER_DATA_FILE):
        default_data = {
            "actions": {"Fold": 0, "Call": 0, "Raise": 0},
            "bankroll": 1000,
            "stats": {"Money_won_loss": 0, "Win_percentage": 0},
            "player_profiles": {
                "Aggressive": "Neutral", 
                "Passive": "Neutral", 
                "Loose": "Neutral", 
                "Tight": "Neutral"
            },
            "logging_metrics": {
                "Games_played": 0, 
                "Average_bet": 0, 
                "Performance_rating": "N/A"
            }
        }
        with open(USER_DATA_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    else:
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
        return data

def save_user_data(data):
    """
    Saves the provided user data to the JSON file.
    """
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

def user_page(mainMenu):
    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()

        # Get the current screen dimensions.
        screen_width, screen_height = SCREEN.get_size()

        # Scale and blit the background to fit the screen.
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Create a transparent textbox with rounded edges.
        # Create a transparent textbox with rounded edges.
        textbox_width = int(screen_width * 0.9)
        textbox_height = int(screen_height * 0.8)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.10)
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100),   # Black with an alpha value of 100 (semi-transparent)
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Display header text.
        header_text = get_font(45).render("This is the USER screen.", True, "White")
        header_rect = header_text.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(header_text, header_rect)

        # Load temporary user data from JSON.
        user_data = load_user_data()

        # Set up a font and starting coordinates for the user data.
        data_font = get_font(20)
        line_spacing = 30
        current_line = 0
        data_x = textbox_x + 20
        data_y = textbox_y + 20

        # Display each key/value pair from the user data.
        for key, value in user_data.items():
            # Render and display the key.
            key_surface = data_font.render(f"{key}:", True, "White")
            SCREEN.blit(key_surface, (data_x, data_y + current_line * line_spacing))
            current_line += 1

            # If the value is a dictionary, iterate through its items.
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    sub_surface = data_font.render(f"   {sub_key}: {sub_value}", True, "White")
                    SCREEN.blit(sub_surface, (data_x + 10, data_y + current_line * line_spacing))
                    current_line += 1
            else:
                # If the value is not a dictionary, render it directly.
                value_surface = data_font.render(f"   {value}", True, "White")
                SCREEN.blit(value_surface, (data_x + 10, data_y + current_line * line_spacing))
                current_line += 1

        # Create the "BACK" button.
        USER_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 2.5), 
            text_input="BACK", 
            font=get_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
            image=None
        )

        USER_BACK.changecolour(USER_MOUSE_POS)
        USER_BACK.update(SCREEN)

        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if USER_BACK.checkForInput(USER_MOUSE_POS):
                    mainMenu()

        pygame.display.update()
