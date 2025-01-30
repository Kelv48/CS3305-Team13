import pygame

pygame.init()

# Allow the window to be resizable
SCREEN = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
BG = pygame.image.load("assets/images/extra/B1.jpg")
FPS = 60

pygame.display.set_caption("Menu")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/fonts/calibri_bold.ttf", size)