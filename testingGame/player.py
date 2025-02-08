import pygame
from testingGame.constant import BLACK, WIDTH, HEIGHT, label_player_image, BEIGE


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
        font = pygame.font.SysFont('comicsans', 20)
        text1 = font.render(str(self.name), True, BLACK)

        text2 = font.render(str(self.stack)+'$', True, BLACK)
        width = WIDTH * 0.1
        height = HEIGHT * 0.1
        image = pygame.transform.scale(label_player_image, (width, height))

        if self == self.player_list_chair[0]:
            x, y = 750, 550
        elif self == self.player_list_chair[1]:
            x, y = 750, 50
        elif self == self.player_list_chair[2]:
            x, y = 200, 200
        elif self == self.player_list_chair[3]:
            x, y = 1000, 200
        elif self == self.player_list_chair[4]:
            x, y = 200, 500
        elif self == self.player_list_chair[5]:
            x, y = 1000, 500


        win.blit(image, (x, y))
        win.blit(text1,
                 (x + (width // 2 - text1.get_width() // 2),
                  y + (height // 4 - text1.get_height() // 3)))
        win.blit(text2,
                 (x + (width // 2 - text1.get_width() // 3)-10,
                  y + (3 * height // 4 - text1.get_height() // 1.5)))
        





    def drawBet(self, win):
        """
        :param win:
        :return: displays bet of players
        """
        if self.bet_auction > 0:

            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(str(self.bet_auction)+'$', True, BEIGE)

            if self == self.player_list_chair[0]:
                x, y = (WIDTH - text.get_width()) // 2, 470
            elif self == self.player_list_chair[1]:
                x, y = (WIDTH - text.get_width()) // 2, 220
            elif self == self.player_list_chair[2]:
                x, y = (WIDTH - text.get_width()) // 500, 1000
            elif self == self.player_list_chair[3]:
                x, y = (WIDTH - text.get_width()) // 500, 900
            elif self == self.player_list_chair[4]:
                x, y = (WIDTH - text.get_width()) // 500, 700
            elif self == self.player_list_chair[5]:
                x, y = (WIDTH - text.get_width()) // 500, 800

            win.blit(text, (x, y))





    # @staticmethod
    # def draw_pot(win):
    #     # display pot for entire table
    #     input_stack = sum([player.input_stack for player in Player.player_list])
    #     bets = sum([player.bet_auction for player in Player.player_list])
    #     font = pygame.font.SysFont('comicsans', 20)
    #     text = font.render('Pot: {}$'.format(str(input_stack - bets)), True, BEIGE)
    #     x, y = (WIDTH - text.get_width()) // 2, 270
    #     win.blit(text, (x, y))



    @staticmethod
    def drawPot(win):
        # Calculate the pot from all players
        input_stack = sum(player.input_stack for player in Player.player_list)
        bets = sum(player.bet_auction for player in Player.player_list)
        # Get the current width and height of the window
        width = win.get_width()
        height = win.get_height()






        # Optionally, scale the font size based on the screen size (e.g., 5% of screen height)
        font_size = max(10, int(height * 0.02))  # Ensures the font doesn't get too small
        font = pygame.font.SysFont('comicsans', font_size)
        # Render the text
        pot_text = f'Pot: {input_stack - bets}$'
        text_surface = font.render(pot_text, True, BEIGE)#
        
        # Center the text on the screen
        x = (width - text_surface.get_width()) // 2
        y = (height - text_surface.get_height()) // 2.5
        
        # Draw the text on the window
        win.blit(text_surface, (x, y))

