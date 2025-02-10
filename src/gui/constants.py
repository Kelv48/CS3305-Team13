import pygame
from os import path
from src.game.card import Card

pygame.init()

# Color RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (225, 198, 153)
RED = (255, 0, 0)

# Screen settings
FPS = 60
WIDTH = 1280
HEIGHT = 720
SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE) # Allow the window to be resizable

# Blinds
SB, BB = 25, 50

# Load images
buttons_folder = path.join(path.dirname(__file__), '../../assets/buttons')
cards_folder = path.join(path.dirname(__file__),   '../../assets/cards')
fonts_folder = path.join(path.dirname(__file__),   '../../assets/fonts')
images_folder = path.join(path.dirname(__file__),  '../../assets/images')
music_folder = path.join(path.dirname(__file__),   '../../assets/music')
sfx_folder = path.join(path.dirname(__file__),     '../../assets/sfx')


# Background
BG = pygame.image.load(path.join(images_folder, 'Background.jpg')).convert_alpha()
BG.set_colorkey(WHITE)

# Icon
icon = pygame.image.load(path.join(images_folder,'poker_cards_icon.png'))
pygame.display.set_icon(icon)

# Button
button_image = pygame.image.load(path.join(buttons_folder, 'button.png')).convert_alpha()
button_image.set_colorkey(WHITE)

# Label player
label_player_image = pygame.image.load(path.join(buttons_folder, 'label_player.png')).convert_alpha()
label_player_image.set_colorkey(WHITE)



# Background music
pygame.mixer.music.load(path.join(music_folder,'Los Santos.mp3')) # Background music file


# Sound effect
button_click_sound = pygame.mixer.Sound(path.join(sfx_folder, 'chips.mp3'))  # Sound effect file
winner_sound = pygame.mixer.Sound(path.join(sfx_folder, 'winner.mp3')) # Winner sound effect file


# Play background music
pygame.mixer.music.play(-1)  # Loop indefinitely


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(path.join(fonts_folder, 'calibri_bold.ttf'), size)



def play_button_click_sound():
    button_click_sound.play()  # Play sound effect when button is clicked



def play_winner_sound():
    winner_sound.play()  # Play winner sound effect








# ALL CARDS

deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS',
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD']

cards_list_images = ['2C.png', '3C.png', '4C.png', '5C.png', '6C.png', '7C.png', '8C.png', '9C.png', 'TC.png', 'JC.png', 'QC.png', 'KC.png', 'AC.png', 
                     '2S.png', '3S.png', '4S.png', '5S.png', '6S.png', '7S.png', '8S.png', '9S.png', 'TS.png', 'JS.png', 'QS.png', 'KS.png', 'AS.png', 
                     '2H.png', '3H.png', '4H.png', '5H.png', '6H.png', '7H.png', '8H.png', '9H.png', 'TH.png', 'JH.png', 'QH.png', 'KH.png', 'AH.png', 
                     '2D.png', '3D.png', '4D.png', '5D.png', '6D.png', '7D.png', '8D.png', '9D.png', 'TD.png', 'JD.png', 'QD.png', 'KD.png', 'AD.png']




cards_images = []
for img in cards_list_images:
    card_img = pygame.image.load(path.join(cards_folder, img)).convert_alpha()
    cards_images.append(card_img)

# Dictionary with cards object
cards_object = {}
for i in range(len(cards_images)):
    name = deck[i]
    cards_object[name] = Card(cards_images[i])

# Opponent cards
card_reverse_image = pygame.image.load(path.join(cards_folder, 'red_back.png')).convert_alpha()
cards_object['reverse_1'] = Card(card_reverse_image)
cards_object['reverse_2'] = Card(card_reverse_image)












