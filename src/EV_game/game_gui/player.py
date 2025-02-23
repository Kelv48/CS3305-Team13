import pygame
from src.gui.utils.constants import BLACK, WIDTH, HEIGHT, label_player_image, BEIGE, game_font, dealer_icon, sb_icon, bb_icon

class Player(object):
    # Fixed on-screen list vs. logical order.
    player_list = []
    player_list_chair = []
    _position = 0
    dealer_index = 0

    def __init__(self, name, stack, kind='human'):
        self.__class__.player_list.append(self)
        self.__class__.player_list_chair.append(self)
        self.name = name
        self.kind = kind  # 'human' or 'AI'
        self.stack = stack
        self.position = Player._position
        self.live = True
        self.alin = False
        self.cards = ''
        self.score = 0
        self.hand = ''
        self.input_stack = 0
        self.bet_auction = 0
        self.win_chips = 0
        self.decision = False
        self.action_history = []
        Player._position += 1

    def allin(self):
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

    def get_role(self):
        num_players = len(Player.player_list_chair)
        fixed_index = Player.player_list_chair.index(self)
        relative_index = (fixed_index - (Player.dealer_index % num_players)) % num_players
        if num_players == 2:
            roles = ["SB/BTN", "BB"]
        elif num_players == 3:
            roles = ["SB/BTN", "BB", "UTG"]
        elif num_players == 4:
            roles = ["BTN", "SB", "BB", "UTG"]
        elif num_players == 5:
            roles = ["BTN", "SB", "BB", "UTG", "HJ"]
        elif num_players == 6:
            roles = ["BTN", "SB", "BB", "UTG", "HJ", "CO"]
        else:
            roles = ["" for _ in range(num_players)]
        return roles[relative_index]

    def playerLabel(self, win):
        font = game_font(20)
        text1 = font.render(str(self.name), True, BLACK)
        text2 = font.render('$' + str(self.stack), True, BLACK)
        width_img = int(WIDTH * 0.1)
        height_img = int(HEIGHT * 0.1)
        image = pygame.transform.scale(label_player_image, (width_img, height_img))
        
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
        else:
            x, y = 0, 0

        win.blit(image, (x, y))
        win.blit(text1, (x + (width_img // 2 - text1.get_width() // 2),
                         y + (height_img // 4 - text1.get_height() // 3)))
        win.blit(text2, (x + (width_img // 2 - text1.get_width() // 3) - 10,
                         y + (3 * height_img // 4 - text1.get_height() // 1.5)))
        role = self.get_role()
        role_text = font.render(role, True, BLACK)
        text_offset_x = x - role_text.get_width() - 10  
        text_offset_y = y + (height_img // 2 - role_text.get_height() // 2)
        win.blit(role_text, (text_offset_x, text_offset_y))
        
        role_icon_x = x + width_img - 30
        role_icon_y = y - 35
        if role in ["BTN", "SB/BTN"]:
            win.blit(dealer_icon, (role_icon_x, role_icon_y))
        elif role == "SB":
            win.blit(sb_icon, (role_icon_x, role_icon_y))
        elif role == "BB":
            win.blit(bb_icon, (role_icon_x, role_icon_y))

    def drawBet(self, win):
        if self.bet_auction > 0:
            font = game_font(20)
            text = font.render('$' + str(self.bet_auction), True, BEIGE)
            if self == self.player_list_chair[0]:
                bet_x, bet_y = 610, 510
            elif self == self.player_list_chair[1]:
                bet_x, bet_y = 310, 440
            elif self == self.player_list_chair[2]:
                bet_x, bet_y = 310, 270
            elif self == self.player_list_chair[3]:
                bet_x, bet_y = 610, 210
            elif self == self.player_list_chair[4]:
                bet_x, bet_y = 920, 270
            elif self == self.player_list_chair[5]:
                bet_x, bet_y = 920, 440
            padding = 10
            oval_width = text.get_width() + padding * 2
            oval_height = text.get_height() + padding * 2
            oval_surface = pygame.Surface((oval_width, oval_height), pygame.SRCALPHA)
            oval_color = (0, 0, 0, 128)
            pygame.draw.ellipse(oval_surface, oval_color, (0, 0, oval_width, oval_height))
            oval_x = bet_x + text.get_width() // 2 - oval_width // 2
            oval_y = bet_y + text.get_height() // 2 - oval_height // 2
            win.blit(oval_surface, (oval_x, oval_y))
            win.blit(text, (bet_x, bet_y))

    @staticmethod
    def drawPot(win):
        input_stack = sum(player.input_stack for player in Player.player_list)
        bets = sum(player.bet_auction for player in Player.player_list)
        width_win = win.get_width()
        height_win = win.get_height()
        font_size = max(20, int(height_win * 0.02))
        font = game_font(font_size)
        pot_text = f'Pot: ${input_stack - bets}'
        text_surface = font.render(pot_text, True, BEIGE)
        x = (width_win - text_surface.get_width()) // 2
        y = int((height_win - text_surface.get_height()) // 2.3)
        padding = 10
        oval_width = text_surface.get_width() + padding * 2
        oval_height = text_surface.get_height() + padding * 2
        oval_surface = pygame.Surface((oval_width, oval_height), pygame.SRCALPHA)
        oval_color = (0, 0, 0, 128)
        pygame.draw.ellipse(oval_surface, oval_color, (0, 0, oval_width, oval_height))
        oval_x = x + (text_surface.get_width() // 2) - (oval_width // 2)
        oval_y = y + (text_surface.get_height() // 2) - (oval_height // 2)
        win.blit(oval_surface, (oval_x, oval_y))
        win.blit(text_surface, (x, y))