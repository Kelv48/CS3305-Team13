import pygame, sys
from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN



def render_screen(title, username, password, active_input, button_actions):
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
    USERNAME_LABEL = get_font(30).render("Username", True, "White")
    USERNAME_LABEL_RECT = USERNAME_LABEL.get_rect(center=(username_box.centerx, username_box.y - 20))
    SCREEN.blit(USERNAME_LABEL, USERNAME_LABEL_RECT)

    USERNAME_TEXT = get_font(30).render(username, True, "White")
    SCREEN.blit(USERNAME_TEXT, (username_box.x + 5, username_box.y + 5))

    PASSWORD_LABEL = get_font(30).render("Password", True, "White")
    PASSWORD_LABEL_RECT = PASSWORD_LABEL.get_rect(center=(password_box.centerx, password_box.y - 20))
    SCREEN.blit(PASSWORD_LABEL, PASSWORD_LABEL_RECT)

    PASSWORD_TEXT = get_font(30).render('*' * len(password), True, "White")
    SCREEN.blit(PASSWORD_TEXT, (password_box.x + 5, password_box.y + 5))

    # Create and position buttons
    button_objects = []
    for index, (text, action) in enumerate(button_actions):
        button_y = (index + 2.5) * (screen_height / (len(button_actions) + 2))
        button = Button(
            pos=(screen_width / 2, button_y), 
            text_input=text, 
            font=get_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
            image=None)
        
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
                    else:
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
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
                    else:
                        username += event.unicode
                elif active_input == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        pygame.display.update()




def registerUser():
    pass

def loginUser():
    pass

