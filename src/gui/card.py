import pygame

card_width = 70
card_height = 105
screen_width = 1280
screen_height = 720

class Card(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # Store the scaled image as the original image.
        self.original_image = pygame.transform.scale(image, (card_width, card_height))
        self.image = self.original_image
        self.type_card = ''
        self.rect = self.image.get_rect()

    def xCords(self, width_space):
        """
        Calculate x-coordinates for card positions in the center.
        """
        x_coef = [-2 + i for i in range(5)]
        return [screen_width // 2 + coef * (card_width + width_space) for coef in x_coef]


    def putInPlace(self):
        x_c = self.xCords(0)

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

        if self.type_card in positions:
            pos = positions[self.type_card]

            if self.type_card in ['first_card_player', 'second_card_player',
                                'first_card_opponent', 'second_card_opponent']:
                tilt_angles = {
                    'first_card_player': 10,
                    'second_card_player': -10,
                    'first_card_opponent': 10,
                    'second_card_opponent': -10,
                }
                angle = tilt_angles.get(self.type_card, 0)
                # Rotate using the original image to avoid cumulative errors
                self.image = pygame.transform.rotate(self.original_image, angle)
            else:
                self.image = self.original_image

            self.rect = self.image.get_rect()
            self.rect.centerx = pos[0]
            self.rect.bottom = pos[1]
