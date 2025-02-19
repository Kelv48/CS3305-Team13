import pygame, sys
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN

def render_screen(title, username, password, active_input, button_actions):
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    # Transparent textbox with rounded edges
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
    
    TITLE_TEXT = get_font(45).render(title, True, "White")
    TITLE_RECT = TITLE_TEXT.get_rect(center=(screen_width / 2, screen_height / 9))
    SCREEN.blit(TITLE_TEXT, TITLE_RECT)

    # Define input boxes
    username_box = pygame.Rect(screen_width / 2 - 100, screen_height / 4, 200, 40)
    password_box = pygame.Rect(screen_width / 2 - 100, screen_height / 2.5, 200, 40)

    # Set the border color: red if active, white if inactive
    username_color = "Green" if active_input == "username" else "White"
    password_color = "Green" if active_input == "password" else "White"

    # Draw the input boxes with the selected colors
    pygame.draw.rect(SCREEN, username_color, username_box, 2)
    pygame.draw.rect(SCREEN, password_color, password_box, 2)

    # Render labels for input boxes
    USERNAME_LABEL = get_font(30).render("Username", True, "White")
    USERNAME_LABEL_RECT = USERNAME_LABEL.get_rect(center=(username_box.centerx, username_box.y - 20))
    SCREEN.blit(USERNAME_LABEL, USERNAME_LABEL_RECT)

    PASSWORD_LABEL = get_font(30).render("Password", True, "White")
    PASSWORD_LABEL_RECT = PASSWORD_LABEL.get_rect(center=(password_box.centerx, password_box.y - 20))
    SCREEN.blit(PASSWORD_LABEL, PASSWORD_LABEL_RECT)

    # Render the username text and draw a blinking cursor if active.
    USERNAME_TEXT = get_font(30).render(username, True, "White")
    username_text_pos = (username_box.x + 5, username_box.y + 5)
    SCREEN.blit(USERNAME_TEXT, username_text_pos)
    
    if active_input == "username":
        # Calculate cursor position based on rendered text width
        text_width = USERNAME_TEXT.get_width()
        cursor_x = username_box.x + 5 + text_width
        cursor_y_top = username_box.y + 5
        cursor_y_bottom = username_box.y + 1 + USERNAME_TEXT.get_height()
        # Blinking effect: visible for 500ms, then hidden for 500ms
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(SCREEN, "White", (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

    # Render the password text (masked) and draw a blinking cursor if active.
    masked_password = '*' * len(password)
    PASSWORD_TEXT = get_font(30).render(masked_password, True, "White")
    password_text_pos = (password_box.x + 5, password_box.y + 5)
    SCREEN.blit(PASSWORD_TEXT, password_text_pos)
    
    if active_input == "password":
        text_width = PASSWORD_TEXT.get_width()
        cursor_x = password_box.x + 5 + text_width
        cursor_y_top = password_box.y + 5
        cursor_y_bottom = password_box.y + 1 + PASSWORD_TEXT.get_height()
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.line(SCREEN, "White", (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

    # Create and position buttons
    button_objects = []
    button_spacing_factor = 2  # Adjust this factor to control vertical spacing

    for index, (text, action) in enumerate(button_actions):
        button_y = (index + 4) * (screen_height / (len(button_actions) * button_spacing_factor + 2))
        
        button = Button(
            pos=(screen_width / 2, button_y), 
            text_input=text, 
            font=get_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
            image=None
        )
        
        button.changecolour(pygame.mouse.get_pos())
        button.update(SCREEN)
        button_objects.append((button, action))

    return username_box, password_box, button_objects



def register(mainMenu):
    username = ""
    password = ""
    active_input = None

    while True:
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        username_box, password_box, button_objects = render_screen("Register", username, password, active_input, [
            ("Enter", registerUser),
            ("Switch to Login Page", login),
            ("BACK", mainMenu)
        ])

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
                            print("Registering user:", username)  # Placeholder action
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

        pygame.display.update()

def login(mainMenu):
    username = ""
    password = ""
    active_input = None

    while True:
        LOGIN_MOUSE_POS = pygame.mouse.get_pos()
        username_box, password_box, button_objects = render_screen("Login", username, password, active_input, [
            ("Enter", loginUser),
            ("Switch to Register Page", register),
            ("BACK", mainMenu)
        ])

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
                        elif action == loginUser:  # Check for Enter button action
                            print("Logging in user:", username)  # Placeholder action
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

        pygame.display.update()


def registerUser():
    pass

def loginUser():
    pass

