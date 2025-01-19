
""" 
This module provides helper functions for:
    - loading images
    - drawing text
    - centering buttons 
    - handling quit events  
"""

import pygame
import sys


# Layering 
# Draw images first
# Then load text over images


""" Loads an image and scales it """
def load_image(path, scale=None): 
    image = pygame.image.load(path)
    if scale:
        image = pygame.transform.scale(image, scale)
    return image


""" Renders text to a surface and blits it onto given surface """
def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color) # Render the text to a surface
    surface.blit(text_surface, position) # Blit the text surface onto given surface


""" Centers buttons on the window """
def center_buttons(win, btns, btn_width=200, btn_height=75, btn_spacing=20):
    # Calculate center position of the screen
    screen_center_x = win.get_width() // 2
    screen_center_y = win.get_height() // 2
    
    # Position each button to the center of the screen
    for i, btn in enumerate(btns):
        btn_x = screen_center_x - btn_width // 2
        btn_y = screen_center_y - (len(btns) * btn_height // 2) + i * (btn_height + btn_spacing)
        btn.set_position(btn_x, btn_y)


""" Draws text centered horizontally on the window """
def draw_centered_text(win, text_surface, y_position):
    screen_center_x = win.get_width() // 2 # Calculate the center position of text
    text_x = screen_center_x - text_surface.get_width() // 2
    win.blit(text_surface, (text_x, y_position)) # Blit the text surface at y position


def handle_quit_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()  # Quit pygame
        sys.exit()     # Exit program




