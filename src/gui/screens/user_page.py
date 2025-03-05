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
    # Load user data, if invalid → Go back to main menu
    user_data = load_user_data()
    if not user_data:
        mainMenu()
        return

    clock = pygame.time.Clock()
    
    while True:
        clock.tick(FPS)
        USER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill((0, 0, 0))  # Clear screen
        
        # Background
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Semi-transparent textbox
        textbox_width, textbox_height = int(screen_width * 0.9), int(screen_height * 0.8)
        textbox_x, textbox_y = (screen_width - textbox_width) // 2, int(screen_height * 0.1)
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(textbox_surface, (0, 0, 0, 100), (0, 0, textbox_width, textbox_height), border_radius=50)
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Header
        header_text = screen_font(45).render("USER PAGE", True, "Gold")
        header_rect = header_text.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(header_text, header_rect)

        # Display user data
        data_font = screen_font(20)
        line_spacing = 30
        data_x, data_y = textbox_x + 20, textbox_y + 20
        current_line = 0

        for key, value in user_data.items():
            key_surface = data_font.render(f"{key}:", True, "White")
            SCREEN.blit(key_surface, (data_x, data_y + current_line * line_spacing))
            current_line += 1

            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    sub_surface = data_font.render(f"   {sub_key}: {sub_value}", True, "White")
                    SCREEN.blit(sub_surface, (data_x + 10, data_y + current_line * line_spacing))
                    current_line += 1
            else:
                value_surface = data_font.render(f"   {value}", True, "White")
                SCREEN.blit(value_surface, (data_x + 10, data_y + current_line * line_spacing))
                current_line += 1

        # "Back" Button
        USER_BACK = Button(
            pos=(screen_width / 2, screen_height * 2 / 2.5),
            text_input="HOME",
            font=screen_font(30),
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
