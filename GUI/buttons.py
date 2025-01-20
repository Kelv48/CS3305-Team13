
""" This module provides button related functionality """

import pygame

# ...existing code...

class Button:
    def __init__(self, x, y, width, height, text, callback, image=None, scale=1):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font('graphics/fonts/PixelatedDisplay.ttf', 50)

        # if image:
        #     image_width = image.get_width()
        #     image_height = image.get_height()
        #     self.image = pygame.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        #     self.rect = self.image.get_rect()
        #     self.rect.topleft = (x, y)
        # self.clicked = False

    """ Draws the button on the given surface """
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect.topleft)  # Draw the image if one is set
        else:
            pygame.draw.rect(surface, (0, 255, 0), self.rect)  # Draw green rectangle if no image

        # Render the text and calculate its center position
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)  # Center the text inside the button
        surface.blit(text_surf, text_rect.topleft)

    """ Checks if the button is clicked and calls the callback function if it is """
    def is_clicked(self, mouse_pos):  # Renamed method to avoid conflicts
        if self.rect.collidepoint(mouse_pos):
            self.callback()

    """ Sets the position of the button based on x, y for top-left corner """
    def set_position(self, x, y):
        self.rect.topleft = (x, y)  # Set top-left corner of the button at (x, y)

    def center_button(self, resWidth, resHeight):
        self.rect.topleft = (resWidth * 0.4, resHeight * 0.4)
    def setButtonSize(self, width, height):
        self.rect.width = width
        self.rect.height = height
    def getButtonSize(self):
        return self.rect.width, self.rect.height