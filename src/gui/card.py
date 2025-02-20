import pygame

card_width = 60
card_height = 90
screen_width = 1280
screen_height = 720

class Card(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface) -> None:
        """
        Initialize a Card sprite with a scaled image.

        :param image: The original image surface for the card.
        """
        super().__init__()
        # Scale the image to the desired card size.
        self.original_image = pygame.transform.scale(image, (card_width, card_height))
        self.image = self.original_image
        self.type_card: str = ''
        self.rect = self.image.get_rect()

    def xCords(self, width_space: int) -> list[int]:
        """
        Calculate x-coordinates for card positions centered on the screen.

        :param width_space: The space between cards.
        :return: List of calculated x-coordinates.
        """
        x_coef = [-2 + i for i in range(5)]  # Coefficients for 5 positions: [-2, -1, 0, 1, 2]
        return [screen_width // 2 + coef * (card_width + width_space) for coef in x_coef]

    def putInPlace(self) -> None:
        """
        Position the card sprite based on its type.
        
        This method assigns the card's image (rotating if necessary) and positions its rect
        attribute according to pre-defined positions.
        """
        # Calculate x-coordinates for community cards using a defined spacing.
        x_c = self.xCords(5)

        # Offset used to adjust player and opponent cards closer to the center.
        offset = -10

        positions = {
        # Player cards (positioned near the bottom center)
        'first_card_player':  (620, 660),
        'second_card_player': (660, 660),

        # Opponent cards with hardcoded positions
        'first_card_opponent1':  (220, 530),
        'second_card_opponent1': (260, 530),

        'first_card_opponent2':  (220, 230),
        'second_card_opponent2': (260, 230),

        'first_card_opponent3':  (620, 150),
        'second_card_opponent3': (660, 150),

        'first_card_opponent4':  (1020, 530),
        'second_card_opponent4': (1060, 530),

        'first_card_opponent5':  (1020, 230),
        'second_card_opponent5': (1060, 230),
    

            # Community cards (flop, turn, river) positioned based on xCords.
            'first_card_flop':      (x_c[0], screen_height // 2 + self.image.get_height() // 2 + 30),
            'second_card_flop':     (x_c[1], screen_height // 2 + self.image.get_height() // 2 + 30),
            'third_card_flop':      (x_c[2], screen_height // 2 + self.image.get_height() // 2 + 30),
            'turn_card':            (x_c[3], screen_height // 2 + self.image.get_height() // 2 + 30),
            'river_card':           (x_c[4], screen_height // 2 + self.image.get_height() // 2 + 30),
        }

        # If the card's type isn't in our positions dictionary, do nothing.
        if self.type_card not in positions:
            return

        pos = positions[self.type_card]

        # Define tilt angles for various card types.
        tilt_angles = {
            'first_card_player': 15,
            'second_card_player': -15,
            'first_card_opponent': 15,
            'second_card_opponent': -15,
            'first_card_opponent1': 15,
            'second_card_opponent1': -15,
            'first_card_opponent2': 15,
            'second_card_opponent2': -15,
            'first_card_opponent3': 15,
            'second_card_opponent3': -15,
            'first_card_opponent4': 15,
            'second_card_opponent4': -15,
            'first_card_opponent5': 15,
            'second_card_opponent5': -15,
        }
        # Get the rotation angle; default is 0 if not specified.
        angle = tilt_angles.get(self.type_card, 0)
        if angle:
            self.image = pygame.transform.rotate(self.original_image, angle)
        else:
            self.image = self.original_image

        # After a rotation, update the sprite's rect.
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.bottom = pos[1]
