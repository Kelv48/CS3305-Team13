import pygame
import sys, os
import requests
import json
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS
from werkzeug.security import generate_password_hash, check_password_hash

BASE_URL = 'http://84.8.144.77:5000'
LOCAL_FILE = "local.json"

def render_screen(title, username, password, active_input, button_actions, message=""):
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    textbox_width = int(screen_width * 0.25)
    textbox_height = int(screen_height * 0.7)
    textbox_x = int((screen_width - textbox_width) / 2)
    textbox_y = int(screen_height * 0.15)

    textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
    pygame.draw.rect(
        textbox_surface, (0, 0, 0, 150), (0, 0, textbox_width, textbox_height), border_radius=50
    )
    SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
    
    title_text = screen_font(45).render(title, True, "Gold")
    title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 9))
    SCREEN.blit(title_text, title_rect)

    # Display message if any
    if message:
        message_text = screen_font(25).render(message, True, "Red")
        message_rect = message_text.get_rect(center=(screen_width / 2, screen_height / 1.95))
        SCREEN.blit(message_text, message_rect)

    username_box = pygame.Rect(screen_width / 2 - 100, screen_height / 4, 200, 40)
    password_box = pygame.Rect(screen_width / 2 - 100, screen_height / 2.7, 200, 40)

    username_colour = "Green" if active_input == "username" else "White"
    password_colour = "Green" if active_input == "password" else "White"

    pygame.draw.rect(SCREEN, username_colour, username_box, 2)
    pygame.draw.rect(SCREEN, password_colour, password_box, 2)

    username_label = screen_font(30).render("Username", True, "White")
    username_label_rect = username_label.get_rect(center=(username_box.centerx, username_box.y - 20))
    SCREEN.blit(username_label, username_label_rect)

    password_label = screen_font(30).render("Password", True, "White")
    password_label_rect = password_label.get_rect(center=(password_box.centerx, password_box.y - 20))
    SCREEN.blit(password_label, password_label_rect)

    username_text = screen_font(30).render(username, True, "White")
    SCREEN.blit(username_text, (username_box.x + 5, username_box.y + 5))
    
    if active_input == "username":
        text_width = username_text.get_width()
        cursor_x = username_box.x + 5 + text_width
        cursor_y_top = username_box.y + 5
        cursor_y_bottom = username_box.y + 1 + username_text.get_height()
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(SCREEN, "White", (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

    masked_password = '*' * len(password)
    password_text = screen_font(30).render(masked_password, True, "White")
    password_text_pos = (password_box.x + 5, password_box.y + 5)
    SCREEN.blit(password_text, password_text_pos)
    
    if active_input == "password":
        text_width = password_text.get_width()
        cursor_x = password_box.x + 5 + text_width
        cursor_y_top = password_box.y + 5
        cursor_y_bottom = password_box.y + 1 + password_text.get_height()
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(SCREEN, "White", (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

    button_objects = []
    button_spacing_factor = 2

    for index, (text, action) in enumerate(button_actions):
        button_y = (index + 3.2) * (screen_height / (len(button_actions) * button_spacing_factor + 0.8))
        
        button = Button(
            pos=(screen_width / 2, button_y), 
            text_input=text, 
            font=screen_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
            image=None
        )
        
        button.changecolour(pygame.mouse.get_pos())
        button.update(SCREEN)
        button_objects.append((button, action))

    return username_box, password_box, button_objects

# Register Functionality
def register(mainMenu):
    username = ""
    password = ""
    active_input = None
    message = ""

    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        username_box, password_box, button_objects = render_screen("Register", username, password, active_input, [
            ("Enter", registerUser),
            ("Switch to Login Page", login),
            ("HOME", mainMenu)
        ], message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(REGISTER_MOUSE_POS):
                        if action == mainMenu:
                            mainMenu()
                        elif action == login:
                            login(mainMenu)
                        elif action == registerUser:  # Check for Enter button action
                            message = registerUser(username, password)
                if username_box.collidepoint(REGISTER_MOUSE_POS):
                    active_input = "username"
                elif password_box.collidepoint(REGISTER_MOUSE_POS):
                    active_input = "password"
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif len(username) < 10 and event.unicode.isalnum():
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif len(password) < 10 and event.unicode.isalnum():
                        password += event.unicode

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (REGISTER_MOUSE_POS[0], REGISTER_MOUSE_POS[1]))

        pygame.display.update()

def registerUser(username, password):
    url = f"{BASE_URL}/register"
    payload = {"username" : username, "password" : password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201:
        return f"User {username} registered successfully!"
    else:
        return f"Failed to register user {username}!"

# Login Functionality
def login(mainMenu):
    username = load_user()
    if username:
        return mainMenu()
    
    username = ""
    password = ""
    active_input = None
    message = ""

    while True:
        LOGIN_MOUSE_POS = pygame.mouse.get_pos()
        button_actions = [
            ("Enter", loginUser),
            ("Switch to Register Page", register),
            ("HOME", mainMenu)
        ]

        username_box, password_box, button_objects = render_screen(
            "Login", username, password, active_input, button_actions, message
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(LOGIN_MOUSE_POS):
                        if action == mainMenu:
                            mainMenu()
                        elif action == register:
                            register(mainMenu)
                        elif action == loginUser:
                            message = loginUser(username, password)
                        elif action == logout:
                            logout(mainMenu)
                if username_box.collidepoint(LOGIN_MOUSE_POS):
                    active_input = "username"
                elif password_box.collidepoint(LOGIN_MOUSE_POS):
                    active_input = "password"
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif len(username) < 12 and event.unicode.isalnum():
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif len(password) < 12 and event.unicode.isalnum():
                        password += event.unicode

        SCREEN.blit(scaled_cursor, (LOGIN_MOUSE_POS[0], LOGIN_MOUSE_POS[1]))
        pygame.display.update()

def loginUser(username, password):
    url = f"{BASE_URL}/login"
    payload = {"username" : username, "password" : password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        userdata = response.json()
        if check_password_hash(userdata["password"], password):
            wallet = userdata["wallet"]
            save_user(username, wallet)
            return f"User {username} logged in successfully!"
        else:
            return f"Incorrect credentials"
    else:
        return f"Failed to login"

def logout(mainMenu):
    username = load_user()
    if not username:
        print("No user logged in.")
        return mainMenu()

    url = f"{BASE_URL}/logout"
    payload = {"username": username}  # Ensure username is being sent as part of the payload
    headers = {"Content-Type": "application/json"}  # Ensure correct content type

    try:
        # Send a POST request with JSON data
        response = requests.post(url, json=payload, headers=headers)  # Use json=payload instead of data=json.dumps(payload)

        print(f"Raw server response: {response.text}")  # Debugging: Print response before parsing

        if response.status_code == 200:
            try:
                response_data = response.json()  # Try parsing JSON
                print(f"Logout successful: {response_data}")
                delete_user()  # Delete the local user file
            except json.JSONDecodeError:
                print("Logout successful but server returned an empty response.")
                delete_user()
        else:
            try:
                error_message = response.json()
            except json.JSONDecodeError:
                error_message = f"Server error: {response.status_code}, Response: {response.text}"
            print(f"Failed to log out: {error_message}")

    except requests.exceptions.RequestException as e:
        print(f"Error during logout: {e}")

    mainMenu()

# Temp functions
def save_user(username, wallet):
    # to be updated to store a hash when security is implemented in db/redis
    with open(LOCAL_FILE, 'w') as f:
        json.dump({"username": username, "wallet": wallet}, f)

def load_user():
    try:
        # Assuming you're loading from a JSON file or something similar
        with open('local.json', 'r') as file:  # Adjust path if necessary
            data = json.load(file)
            return data.get("username")  # Use .get() to avoid KeyError if 'username' is not found
    except FileNotFoundError:
        return None  # If the file is not found, return None
    except json.JSONDecodeError:
        return None  # If the JSON is corrupted, return None
    
def delete_user():
    try:
        os.remove('local.json')  # Remove the file that contains the user data
    except FileNotFoundError:
        pass  # If the file doesn't exist, do nothing
