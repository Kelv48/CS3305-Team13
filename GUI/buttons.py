
""" This module provides button related functionality """

import pygame

class Button:
    def __init__(self, x, y, width, height, text, callback, image=None):
        
        self.image = image  
        self.rect = pygame.Rect(x, y, width, height)  
        self.text = text  
        self.callback = callback  
        self.font = pygame.font.Font('graphics/fonts/PixelatedDisplay.ttf', 50) 


    """ Draws the button on the given surface """
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect.topleft) # Draw image
        else:
            pygame.draw.rect(surface, (0, 255, 0), self.rect) # If no image then draw green rectangle

        # Draw text on the button
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, self.rect.topleft)


    """ Checks if the button is clicked and calls the callback function if it is """
    def clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()


    """ Sets the position of the button """
    def set_position(self, x, y):
        self.rect.topleft = (x, y)  # Update top left position of rectangle