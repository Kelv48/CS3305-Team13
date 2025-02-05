import pygame
from app.constant import BLACK, label_player_image, WIDTH, HEIGHT


class PlayerLabel:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        font = pygame.font.SysFont('comicsans', 20)
        self.text1 = font.render(str(player.name), True, BLACK)
        self.text2 = font.render(str(player.stack), True, BLACK)
        #self.image = label_player_image
        self.width = WIDTH * 0.1
        self.height = HEIGHT * 0.1
        self.image = pygame.transform.scale(label_player_image, (self.width, self.height))
        #self.rect = self.image.get_rect()

    def draw(self, win):
        # Displays player label
        win.blit(self.image, (self.x, self.y))
        win.blit(self.text1,
                 (self.x + (self.width // 2 - self.text1.get_width() // 2),
                  self.y + (self.height // 4 - self.text1.get_height() // 3)))

        win.blit(self.text2,
                 (self.x + (self.width // 2 - self.text1.get_width() // 3),
                  self.y + (3 * self.height // 4 - self.text1.get_height() // 1.5)))