
# import pygame
# import json

# pygame.init()

# # Screen dimensions
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Register & Login")

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (200, 200, 200)
# BLUE = (0, 122, 255)

# # Fonts
# FONT = pygame.font.Font(None, 36)

# # Helper functions
# def draw_text(text, font, color, surface, x, y):
#     text_obj = font.render(text, True, color)
#     text_rect = text_obj.get_rect(center=(x, y))
#     surface.blit(text_obj, text_rect)

# # User authentication functions
# def load_users(file="users.json"):
#     try:
#         with open(file, "r") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {}

# def save_users(users, file="users.json"):
#     with open(file, "w") as f:
#         json.dump(users, f)

# # Input box class
# class InputBox:
#     def __init__(self, x, y, w, h, text=""):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.color = GRAY
#         self.text = text
#         self.txt_surface = FONT.render(text, True, BLACK)
#         self.active = False

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             # Toggle active state
#             self.active = self.rect.collidepoint(event.pos)
#             self.color = BLUE if self.active else GRAY
#         if event.type == pygame.KEYDOWN and self.active:
#             if event.key == pygame.K_RETURN:
#                 self.text = ""
#             elif event.key == pygame.K_BACKSPACE:
#                 self.text = self.text[:-1]
#             else:
#                 self.text += event.unicode
#             self.txt_surface = FONT.render(self.text, True, BLACK)

#     def draw(self, screen):
#         # Draw rectangle and text
#         pygame.draw.rect(screen, self.color, self.rect, 2)
#         screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

# # Buttons
# def button(screen, text, x, y, w, h, color, callback=None):
#     rect = pygame.Rect(x, y, w, h)
#     pygame.draw.rect(screen, color, rect)
#     draw_text(text, FONT, WHITE, screen, x + w // 2, y + h // 2)
#     return rect

# # Main game loop
# def main():
#     clock = pygame.time.Clock()
#     users = load_users()
#     running = True
#     login_mode = True

#     username_box = InputBox(300, 200, 200, 50)
#     password_box = InputBox(300, 300, 200, 50)
#     message = ""

#     while running:
#         screen.fill(WHITE)
#         draw_text("Login" if login_mode else "Register", FONT, BLACK, screen, WIDTH // 2, 50)
        
#         # Draw input boxes
#         username_box.draw(screen)
#         password_box.draw(screen)

#         # Buttons
#         if button(screen, "Submit", 300, 400, 100, 50, GRAY).collidepoint(pygame.mouse.get_pos()):
#             if pygame.mouse.get_pressed()[0]:  # On left click
#                 username = username_box.text
#                 password = password_box.text
#                 if login_mode:
#                     # Handle login
#                     if username in users and users[username] == password:
#                         message = "Login successful!"
#                     else:
#                         message = "Invalid credentials!"
#                 else:
#                     # Handle registration
#                     if username in users:
#                         message = "User already exists!"
#                     else:
#                         users[username] = password
#                         save_users(users)
#                         message = "Registration successful!"
#         if button(screen, "Switch", 500, 400, 100, 50, GRAY).collidepoint(pygame.mouse.get_pos()):
#             if pygame.mouse.get_pressed()[0]:  # On left click
#                 login_mode = not login_mode
#                 username_box.text = ""
#                 password_box.text = ""
#                 message = ""

#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             username_box.handle_event(event)
#             password_box.handle_event(event)

#         # Display message
#         draw_text(message, FONT, BLACK, screen, WIDTH // 2, HEIGHT - 50)

#         pygame.display.flip()
#         clock.tick(30)

#     pygame.quit()

# if __name__ == "__main__":
#     main()
