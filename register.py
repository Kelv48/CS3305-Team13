import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN
import requests, json, os

base_url = 'http://127.0.0.1:5000'
local_storage = "local.json"

def save_user(username, password):
    # to be updated to store a hash when security is implemented in db/redis
    with open(local_storage, 'w') as f:
        json.dump({"username": username, "password": password}, f)

def load_user():
    try:
        with open(local_storage, 'r') as f:
            data = json.load(f)
            return data["username"]  # Only return the username
    except FileNotFoundError:
        return None


def render_screen(title, username, password, active_input, button_actions, message=""):
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    TITLE_TEXT = get_font(45).render(title, True, "White")
    TITLE_RECT = TITLE_TEXT.get_rect(center=(screen_width / 2, screen_height / 9))
    SCREEN.blit(TITLE_TEXT, TITLE_RECT)

    # Draw input boxes
    username_box = pygame.Rect(screen_width / 2 - 100, screen_height / 4, 200, 40)
    password_box = pygame.Rect(screen_width / 2 - 100, screen_height / 2.5, 200, 40)
    pygame.draw.rect(SCREEN, "White", username_box, 2)
    pygame.draw.rect(SCREEN, "White", password_box, 2)

    # Render text above input boxes
    labels = [("Username", username_box), ("Password", password_box)]
    for label, box in labels:
        label_text = get_font(30).render(label, True, "White")
        label_rect = label_text.get_rect(center=(box.centerx, box.y - 20))
        SCREEN.blit(label_text, label_rect)

    # User input
    SCREEN.blit(get_font(30).render(username, True, "White"), (username_box.x + 5, username_box.y + 5))
    SCREEN.blit(get_font(30).render('*' * len(password), True, "White"), (password_box.x + 5, password_box.y + 5))

    # Error/msg
    if message:
        msg_text = get_font(25).render(message, True, "Red")
        SCREEN.blit(msg_text, (screen_width / 2 - msg_text.get_width() / 2, screen_height / 1.3))

    # Create and position buttons
    button_objects = []
    for index, (text, action) in enumerate(button_actions):
        button_y = (index + 2.5) * (screen_height / (len(button_actions) + 2))
        button = Button(
            pos=(screen_width / 2, button_y), 
            text_input=text, 
            font=get_font(30), 
            base_color="White", 
            hovering_color="Light Green")
        
        button.changeColor(pygame.mouse.get_pos())
        button.update(SCREEN)
        button_objects.append((button, action))

    return username_box, password_box, button_objects


def register(mainMenu):
    username = ""
    password = ""
    active_input = None
    message = ""

    while True:
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        username_box, password_box, button_objects = render_screen("Register", username, password, active_input, [
            ("Enter", register_user),
            ("Switch to Login Page", login),
            ("BACK", mainMenu)
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
                        elif action == register_user:
                            register_user(username, password)
                if username_box.collidepoint(REGISTER_MOUSE_POS):
                    active_input = "username"
                elif password_box.collidepoint(REGISTER_MOUSE_POS):
                    active_input = "password"
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        pygame.display.update()


def register_user(user_name, password):
    url = f"{base_url}/create_user"
    payload = {"username": user_name, "password": password}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201:
        print(f"User {user_name} registered successfully!")
    else:
        print(f"Failed to register: {response.json()}")


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
        username_box, password_box, button_objects = render_screen("Login", username, password, active_input, [
            ("Enter", login_user),
            ("Switch to Register Page", register),
            ("BACK", mainMenu)
        ], message)

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
                        elif action == login_user:
                                login_user(username, password)
                if username_box.collidepoint(LOGIN_MOUSE_POS):
                    active_input = "username"
                elif password_box.collidepoint(LOGIN_MOUSE_POS):
                    active_input = "password"
            if event.type == pygame.KEYDOWN:
                if active_input == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
        pygame.display.update()


def login_user(user_name, password):
    url = f"{base_url}/user"

    payload = {
        "username": user_name, 
        "password": password
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        if user_data["password"] == password:
            print(f"User {user_name} logged in successfully!")
            save_user(user_name, password)
        else:
            print("Incorrect password")
    else:
        print(f"Login failed: {response.json()}")


def logout_screen(user_name, mainMenu):
    while True:
        SCREEN.fill("black")  # Clear screen

        # Only show the username
        TEXT = get_font(45).render(f"Welcome, {user_name}", True, "White")
        SCREEN.blit(TEXT, (SCREEN.get_width() / 2 - 100, SCREEN.get_height() / 4))

        LOGOUT_BUTTON = Button(
            pos=(SCREEN.get_width() / 2, SCREEN.get_height() / 2),
            text_input="Logout",
            font=get_font(30),
            base_color="White",
            hovering_color="Red"
        )
        
        LOGOUT_BUTTON.changeColor(pygame.mouse.get_pos())
        LOGOUT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOGOUT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    logout_user()  # Remove local session
                    return mainMenu()  # Go back to main menu

        pygame.display.update()


def logout_user(mainMenu):
    """Log out user and return to the main menu."""
    try:
        os.remove(local_storage)  # Remove the session file
    except FileNotFoundError:
        pass

    print("User logged out successfully!")
    mainMenu()