
"""
This module contains configuration settings
"""


# Window settings
TITLE = 'Poker Showdown'
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Colors
BG_COLOR = (30, 120, 60)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Asset paths
FONTS = {
    'PIXEL': 'assets/fonts/Pixel.ttf',
    'PIXELATED_DISPLAY': 'assets/fonts/PixelatedDisplay.ttf'
}

AUDIO = {
    'MUSIC': 'assets/audio/music/poker_face.wav',
    'SFX': {
        'CHIPS': 'assets/audio/sfx/chips.mp3'
    }
}

IMAGES = {
    'BACKGROUND': 'assets/images/extra/background.png',
    'BUTTON': 'assets/images/buttons/greenButton.png'
}

# Game settings
DEFAULT_VOLUME = 50