import pygame

class Button():
    def __init__(self, x, y, width, height, text, onclickFunction, font=None, fontSize=50, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclick = onclickFunction
        self.image = image  # Image for the button background
        
        self.font = pygame.font.Font(font, fontSize)
        self.buttonSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Supports transparency
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(self.text, True, (0, 0, 0))

    # Draw the button to the window
    def draw(self, win):
        # If there's an image, use it; otherwise, draw a plain rectangle
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
            self.buttonSurface.blit(scaled_image, (0, 0))
        else:
            self.buttonSurface.fill((255, 255, 255))  # Fill with a default color

        # Draw the text on the button
        text_x = self.buttonRect.width / 2 - self.buttonSurf.get_width() / 2
        text_y = self.buttonRect.height / 2 - self.buttonSurf.get_height() / 2
        self.buttonSurface.blit(self.buttonSurf, (text_x, text_y))
        
        # Draw the button onto the screen
        win.blit(self.buttonSurface, self.buttonRect)

    # Check if the button has been clicked
    def clicked(self, pos):
        if self.buttonRect.collidepoint(pos):
            print("I've been clicked")
            self.onclick()  # Call the button's associated function
        else:
            return False

    def set_position(self, x, y):
        """Set the button's position to new coordinates."""
        self.x = x
        self.y = y
        self.buttonRect.topleft = (x, y)