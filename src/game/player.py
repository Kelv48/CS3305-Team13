import pygame
from src.gui.constants import BLACK, WIDTH, HEIGHT, label_player_image, BEIGE, game_font


class Player(object):
    # player_list_chair and player_list is list of all players the difference is that the order in player_list
    # will be change after each round, order of player_list_chair are steal this same
    player_list = []
    player_list_chair = []
    _position = 0

    def __init__(self, name, stack, kind='human'):
        self.__class__.player_list.append(self)
        self.__class__.player_list_chair.append(self)
        self.name = name
        self.kind = kind  # human or AI
        self.stack = stack
        self.position = Player._position
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0  # how much $ player bet in round
        self.bet_auction = 0  # how much $ player bet in one auction, after each auction this attribute will be reset
        self.win_chips = 0
        self.decision = False
        self.action_history = []
        Player._position += 1

    def allin(self):
        # player will not be asked in the auction
        self.live = False
        self.alin = True
        self.decision = True

    def win(self, chips):
        self.stack += int(chips)
        self.win_chips += chips

    def drop(self, chips):
        self.stack -= int(chips)
        self.input_stack += chips
        self.decision = True
        self.bet_auction += chips

    def blind(self, chips):
        self.stack -= chips
        self.input_stack += chips
        self.bet_auction += chips

    def nextRound(self):
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0
        self.win_chips = 0
        self.decision = False
        
    def fold(self):
        self.live = False
        self.score = 0
        self.decision = True

    def nextAuction(self):
        self.bet_auction = 0
        self.action_history = []

    def playerLabel(self, win):
        """
        :param win: window object
        :return: displays label
        """
        font = game_font(20)
        text1 = font.render(str(self.name), True, BLACK)
        text2 = font.render('$'+ str(self.stack), True, BLACK)
        width = WIDTH * 0.1
        height = HEIGHT * 0.1
        image = pygame.transform.scale(label_player_image, (width, height))
        if self == self.player_list_chair[0]:
            x, y = 580, 620
        elif self == self.player_list_chair[1]:
            x, y = 180, 500
        elif self == self.player_list_chair[2]:
            x, y = 180, 200
        elif self == self.player_list_chair[3]:
            x, y = 580, 120
        elif self == self.player_list_chair[4]:
            x, y = 980, 200
        elif self == self.player_list_chair[5]:
            x, y = 980, 500
        win.blit(image, (x, y))
        win.blit(text1,
                 (x + (width // 2 - text1.get_width() // 2),
                  y + (height // 4 - text1.get_height() // 3)))
        win.blit(text2,
                 (x + (width // 2 - text1.get_width() // 3)-10,
                  y + (3 * height // 4 - text1.get_height() // 1.5)))
        
    def drawBet(self, win):
        """
        :param win: window object
        :return: displays bet of players slightly below the player's label with a semi-transparent oval underneath,
                using hardcoded positions.
        """
        if self.bet_auction > 0:
            font = game_font(20)
            text = font.render('$' + str(self.bet_auction), True, BEIGE)
            
            # Hardcode bet positions based on player's position in player_list_chair
            if self == self.player_list_chair[0]:
                bet_x, bet_y = 620, 510  # example coordinates for player 0's bet text

            elif self == self.player_list_chair[1]:
                bet_x, bet_y = 310, 440  # example coordinates for player 1's bet text
            elif self == self.player_list_chair[2]:
                bet_x, bet_y = 310, 270  # example coordinates for player 2's bet text
            elif self == self.player_list_chair[3]:
                bet_x, bet_y = 580, 205  # example coordinates for player 3's bet text
            elif self == self.player_list_chair[4]:
                bet_x, bet_y = 980, 265  # example coordinates for player 4's bet text
            elif self == self.player_list_chair[5]:
                bet_x, bet_y = 980, 565  # example coordinates for player 5's bet text

            # Create a surface for the semi-transparent oval
            padding = 10  # extra space around the text inside the oval
            oval_width = text.get_width() + padding * 2
            oval_height = text.get_height() + padding * 2
            oval_surface = pygame.Surface((oval_width, oval_height), pygame.SRCALPHA)
            
            # Define a semi-transparent color (RGBA)
            oval_color = (0, 0, 0, 128)  # black with 50% transparency
            
            # Draw the oval on the oval_surface
            pygame.draw.ellipse(oval_surface, oval_color, (0, 0, oval_width, oval_height))
            
            # Calculate the oval's position so that it's centered on the bet text
            oval_x = bet_x + text.get_width() // 2 - oval_width // 2
            oval_y = bet_y + text.get_height() // 2 - oval_height // 2
            
            # Blit the oval first, then the bet text on top
            win.blit(oval_surface, (oval_x, oval_y))
            win.blit(text, (bet_x, bet_y))





    @staticmethod
    def drawPot(win):
        # Calculate the pot from all players
        input_stack = sum(player.input_stack for player in Player.player_list)
        bets = sum(player.bet_auction for player in Player.player_list)
        
        # Get the current width and height of the window
        width = win.get_width()
        height = win.get_height()
        
        # Scale the font size based on the screen size (e.g., 2% of screen height)
        font_size = max(20, int(height * 0.02))  # Ensures the font doesn't get too small
        font = game_font(font_size)
        
        # Render the text
        pot_text = f'Pot: ${input_stack - bets}'
        text_surface = font.render(pot_text, True, BEIGE)
        
        # Center the text on the screen
        x = (width - text_surface.get_width()) // 2
        y = int((height - text_surface.get_height()) // 2.3)
        
        # Create a surface for the semi-transparent oval
        padding = 10  # extra space around the text inside the oval
        oval_width = text_surface.get_width() + padding * 2
        oval_height = text_surface.get_height() + padding * 2
        oval_surface = pygame.Surface((oval_width, oval_height), pygame.SRCALPHA)
        
        # Define a semi-transparent color (RGBA) - black with 50% transparency
        oval_color = (0, 0, 0, 128)
        
        # Draw the oval on the oval_surface
        pygame.draw.ellipse(oval_surface, oval_color, (0, 0, oval_width, oval_height))
        
        # Calculate the oval's position so that it's centered behind the text
        oval_x = x + (text_surface.get_width() // 2) - (oval_width // 2)
        oval_y = y + (text_surface.get_height() // 2) - (oval_height // 2)
        
        # Blit the oval first, then the pot text on top
        win.blit(oval_surface, (oval_x, oval_y))
        win.blit(text_surface, (x, y))
