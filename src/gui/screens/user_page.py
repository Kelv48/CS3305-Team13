import pygame
import sys
import json
import os
import requests
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS

BASE_URL = "http://84.8.144.77:5000"
LOCAL_FILE = "local.json"

def load_user_data():
    """
    Loads username from local.json and sends a request to the server.
    If local.json doesn't exist or is invalid, returns None.
    """
    if not os.path.exists(LOCAL_FILE):
        return None  # No user data → Redirect

    try:
        with open(LOCAL_FILE, "r") as file:
            data = json.load(file)
            username = data.get("username")
            if not username:
                return None  # Invalid file structure
    except (json.JSONDecodeError, KeyError):
        return None  # Invalid JSON → Redirect

    # Send request to the server
    response = requests.post(f"{BASE_URL}/stats", json={"username": username})
    if response.status_code == 200:
        return response.json()
    
    return None  # Server request failed → Redirect

def user_page(mainMenu):
    user_data = load_user_data()
    if not user_data:
        mainMenu()
        return

    username = user_data.get("username", "User")  # Get username or fallback to "User"
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        USER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((0, 0, 0))  # Clear screen

        screen_width, screen_height = SCREEN.get_size()

        # Background
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        USER_TEXT = screen_font(50).render("USER INFO", True, "Gold")
        USER_RECT = USER_TEXT.get_rect(center=(screen_width / 2, screen_height / 13))
        SCREEN.blit(USER_TEXT, USER_RECT)

     
        # User info container
        box_width, box_height = int(screen_width * 0.8), int(screen_height * 0.8)
        box_x, box_y = (screen_width - box_width) // 2, int(screen_height * 0.1)
        info_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(info_surface, (0, 0, 0, 150), (0, 0, box_width, box_height), border_radius=30)
        SCREEN.blit(info_surface, (box_x, box_y))

        # Display user stats in a formatted way
        data_font = screen_font(25)
        line_spacing = 50
        col_spacing = box_width // 2 - 50  # Two-column layout
        data_x, data_y = box_x + 40, box_y + 30
        current_line = 0

        stats = list(user_data.items())
        half = len(stats) // 2

        for i, (key, value) in enumerate(stats):
            x_offset = col_spacing if i >= half else 0
            y_offset = (i % half) * line_spacing

            # Background card for each stat
            stat_bg = pygame.Surface((col_spacing - 20, 40), pygame.SRCALPHA)
            pygame.draw.rect(stat_bg, (255, 255, 255, 50), (0, 0, col_spacing - 20, 40), border_radius=15)
            SCREEN.blit(stat_bg, (data_x + x_offset, data_y + y_offset))

            # Render stat text
            key_surface = data_font.render(f"{key}: {value}", True, "White")
            SCREEN.blit(key_surface, (data_x + 10 + x_offset, data_y + y_offset + 5))

        # "Back" Button with glowing effect
        USER_BACK = Button(
            pos=(screen_width / 2, screen_height * 0.8),
            text_input="HOME",
            font=screen_font(35),
            base_colour="White",
            hovering_colour="Light Green",
            image=None,
        )

        USER_BACK.changecolour(USER_MOUSE_POS)
        USER_BACK.update(SCREEN)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and USER_BACK.checkForInput(USER_MOUSE_POS):
                mainMenu()

        # Custom cursor
        SCREEN.blit(scaled_cursor, USER_MOUSE_POS)
        pygame.display.update()