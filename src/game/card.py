import pygame

card_width = 70
card_height = 105
screen_width = 1280
screen_height = 720

class Card(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (card_width, card_height))
        self.type_card = ''
        self.rect = self.image.get_rect()

    def xCords(self, width_space):
        """
        Calculate x-coordinates for card positions in the center.
        """
        x_coef = [-2 + i for i in range(5)]
        return [screen_width // 2 + coef * (card_width + width_space) for coef in x_coef]

    def putInPlace(self):
        """
        Place the card on the screen based on its type.
        """
        x_c = self.xCords(10)

        # Define positioning data for each card type
        positions = {
            'first_card_player':    ((screen_width - card_width) // 2, screen_height - 30),
            'first_card_opponent':  ((screen_width - card_width) // 2, 150),
            'second_card_player':   ((screen_width + card_width) // 2, screen_height - 30),
            'second_card_opponent': ((screen_width + card_width) // 2, 150),
            'first_card_flop':      (x_c[0], screen_height // 2 + self.image.get_height() // 2 + 30),
            'second_card_flop':     (x_c[1], screen_height // 2 + self.image.get_height() // 2 + 30),
            'third_card_flop':      (x_c[2], screen_height // 2 + self.image.get_height() // 2 + 30),
            'turn_card':            (x_c[3], screen_height // 2 + self.image.get_height() // 2 + 30),
            'river_card':           (x_c[4], screen_height // 2 + self.image.get_height() // 2 + 30),
        }

        # Place the card if the type matches one of the defined positions
        if self.type_card in positions:
            self.rect.centerx, self.rect.bottom = positions[self.type_card]
