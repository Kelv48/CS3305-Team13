
""" 
This module handles the game state which includes: 
    - initializing the game
    - drawing background
    - toggling fullscreen mode
    - handling events 
"""


import pygame
import sys
from settings import *

class GameState:
    def __init__(self):

        """ 
        Initializes the game state
        - Display
        - Clock
        - Font
        - Background image
        - Music and starts playing Also starts playing
        """
    
        self.fullscreen = False
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('graphics/fonts/PixelatedDisplay.ttf', 20)
        self.background_image = pygame.image.load('graphics/images/background.png')
        self.music = pygame.mixer.music.load('./audio/poker_face.wav')  
        pygame.mixer.music.play(-1)  # Loops music continuously
        self.current_screen = None


    """ Draws the background image then scaled to fit the current window size """
    def draw_background(self):
        background_image_scaled = pygame.transform.scale(self.background_image, (self.win.get_width(), self.win.get_height()))
        self.win.blit(background_image_scaled, (0, 0))


    """
    Toggles fullscreen mode. 
    If fullscreen mode is enabled then set the display to the monitors full resolution. 
    Else set the display to the predefined WIDTH and HEIGHT. 
    """
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
            self.win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
        else:
            self.win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

  
    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Fullscreen when ESC key is pressed
                self.toggle_fullscreen()



# Load resources
# card_img = pygame.image.load('./graphics/images/cards.png').convert()
# card_img = pygame.transform.scale(
#     card_img,
#     (card_img.get_width() * 2, card_img.get_height() * 2)
# )
# # Mouse click sound effects
# card_img.set_colorkey((0, 0, 0))
# chips_sound = pygame.mixer.Sound('./audio/chips.mp3')

# Initialize and play background music
# pygame.mixer.music.load('./audio/poker_face.wav')  # Replace with your music file path
# pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Game state
# mouse_down = False