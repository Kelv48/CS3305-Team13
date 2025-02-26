import pygame
import sys
import requests
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor

# Flask API base URL (update if needed)
BASE_URL = "http://84.8.144.77:5000"

def get_leaderboard():
    """
    Fetches leaderboard data from the Flask API.
    """
    try:
        response = requests.get(f"{BASE_URL}/leaderboard")
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching leaderboard: {e}")
        return []

def leaderboard(mainMenu):
    """
    Renders the leaderboard screen.
    """
    while True:
        MOUSE_POS = pygame.mouse.get_pos()

        # Scale the background to fit the screen size.
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Create a semi-transparent leaderboard box.
        textbox_width = int(screen_width * 0.9)
        textbox_height = int(screen_height * 0.8)
        textbox_x = (screen_width - textbox_width) // 2
        textbox_y = int(screen_height * 0.10)
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(textbox_surface, (0, 0, 0, 150), (0, 0, textbox_width, textbox_height), border_radius=30)
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Title
        title_text = screen_font(50).render("Top Earners", True, "Dark Green")
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(title_text, title_rect)

        # Fetch leaderboard data
        leaderboard_data = get_leaderboard()

        # Display leaderboard entries as a table
        entry_font = screen_font(30)
        column_spacing = 200  # Space between columns
        start_x = textbox_x + 50
        start_y = textbox_y + 60

        # Table Headers
        headers = ["Rank", "Username", "Wins", "Losses", "Earnings"]
        for i, header in enumerate(headers):
            header_surface = entry_font.render(header, True, "Yellow")
            SCREEN.blit(header_surface, (start_x + i * column_spacing, start_y))

        # Display leaderboard entries
        for i, entry in enumerate(leaderboard_data[:10]):  # Show only top 10
            row_y = start_y + (i + 1) * 40
            row_data = [str(entry["rank"]), entry["username"], str(entry["wins"]), str(entry["losses"]), str(entry["earnings"])]

            for j, cell in enumerate(row_data):
                cell_surface = entry_font.render(cell, True, "White")
                SCREEN.blit(cell_surface, (start_x + j * column_spacing, row_y))

        # Create buttons
        home_button = Button(
            pos=(screen_width / 2, screen_height - 80),
            text_input="HOME",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None
        )
        home_button.changecolour(MOUSE_POS)
        home_button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.checkForInput(MOUSE_POS):
                    mainMenu()

        # Draw cursor
        SCREEN.blit(scaled_cursor, (MOUSE_POS[0], MOUSE_POS[1]))

        # Update display
        pygame.display.update()
