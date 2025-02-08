import pygame
from src.gui.constants import SCREEN

card_width = 70
card_height = 105
screen_width, screen_height = SCREEN.get_size()

# class Card:
class Card(pygame.sprite.Sprite):
    def __init__(self, image, type_card=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (card_width, card_height))
        self.type_card = ''
        self.rect = self.image.get_rect()

    def _x_cor(self, width_space):
        x_coef = [-2 + i for i in range(5)]
        x_coor = []
        for i in range(5):
            x_coor.append(screen_width // 2 + x_coef[i] * (card_width + width_space))
        return x_coor

    def putInPlace(self):
        """
        function place card
        :return:
        """
        x_c = self._x_cor(10)
        if self.type_card == 'first_card_player':

            self.rect.centerx = (screen_width - card_width) // 2
            self.rect.bottom = screen_height - 80

        
        elif self.type_card == 'first_card_opponent':
            self.rect.centerx = (screen_width - card_width) // 2
            self.rect.bottom = 150


        elif self.type_card == 'second_card_player':
            self.rect.centerx = (screen_width + card_width) // 2
            self.rect.bottom = screen_height - 80


        elif self.type_card == 'second_card_opponent':
            self.rect.centerx = (screen_width + card_width) // 2
            self.rect.bottom = 150

        
        
       



        elif self.type_card == 'first_card_flop':
            self.rect.centerx = x_c[0]
            self.rect.bottom = screen_height // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'second_card_flop':
            self.rect.centerx = x_c[1]
            self.rect.bottom = screen_height // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'third_card_flop':
            self.rect.centerx = x_c[2]
            self.rect.bottom = screen_height // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'turn_card':
            self.rect.centerx = x_c[3]
            self.rect.bottom = screen_height // 2 + self.image.get_height() // 2 + 30

        elif self.type_card == 'river_card':
            self.rect.centerx = x_c[4]
            self.rect.bottom = screen_height // 2 + self.image.get_height() // 2 + 30












        # Player_card_1 = pygame.transform.rotate(Player_card_1, 10)    
        # elif self.type_card == 'second_card_player':
        #     self.rect.centerx = (WIDTH + card_width) // 2 + 5
        #     self.rect.bottom = HEIGHT - 80

        # elif self.type_card == 'second_card_opponent':
        #     self.rect.centerx = (WIDTH + card_width) // 2 + 5
        #     self.rect.bottom = 150

        # win.blit(self.image, (self.rect.centerx, self.rect.top))





