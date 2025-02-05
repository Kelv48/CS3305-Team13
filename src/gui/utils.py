import pygame

pygame.init()

# Allow the window to be resizable
SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
BG = pygame.image.load("assets/images/extra/Background.jpg")
FPS = 60

GAME_BG = pygame.image.load("assets/images/extra/Table.png")

pygame.display.set_caption("Menu")

icon = pygame.image.load("assets/images/extra/poker_cards_icon.png")
pygame.display.set_icon(icon)


# Load background music and sound effect
pygame.mixer.music.load("assets/audio/music/Los Santos.mp3")  # Background music file
button_click_sound = pygame.mixer.Sound("assets/audio/sfx/chips.mp3")  # Sound effect file
winner_sound = pygame.mixer.Sound("assets/audio/sfx/winner.mp3")  # Winner sound effect file


# Play background music
pygame.mixer.music.play(-1)  # Loop indefinitely





def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/fonts/calibri_bold.ttf", size)



def play_button_click_sound():
    button_click_sound.play()  # Play sound effect when button is clicked



def play_winner_sound():
    winner_sound.play()  # Play winner sound effect
















# BASE_IMG_PATH = 'assets/'

# def load_image(path):
#     '''
#     short cut to load a single image, removes the background and increasing preformance
#     (file path) -> (img)
#     '''
#     img = pygame.image.load(BASE_IMG_PATH + path).convert() # helps preformance when rendering
#     img.set_colorkey((0, 0, 0)) # removes the background in png images
#     return img

# def load_images(path):
#     images = []
#     for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
#         if img_name == '.DS_Store':
#             pass
#         else:
#             images.append(load_image(path + '/' + img_name))
#     return images