


import pygame
from src.gui.utils.constants import BLACK, WIDTH, HEIGHT, label_player_image, BEIGE, game_font, dealer_icon, sb_icon, bb_icon

class Player(object):
    # Fixed on-screen list vs. logical order.
    player_list = []
    player_list_chair = []
    _position = 0
    dealer_index = -1  # For role assignment; see explanation below.

    def __init__(self, name, stack, kind='human', turn=False):
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
        self.turn = turn 
        self.action_history = []
        Player._position += 1

    def set_turn(self, state):
        self.turn = state

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
        """
        Returns a role string based on the player's fixed (on-screen) position
        and the current dealer index.
        """
        num_players = len(Player.player_list_chair)
        # Get this player's fixed index.
        fixed_index = Player.player_list_chair.index(self)
        # Compute relative index based on current dealer_index.
        relative_index = (fixed_index - (Player.dealer_index % num_players)) % num_players

        # Define roles based on number of players.
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
        """
        Displays the player's label (name and chip count) at a fixed on-screen position.
        Also draws:
        - The role text (for all six positions) to the left of the player's label.
        - For roles with icons (BTN/SB/BTN, SB, BB), the corresponding icon is drawn
            at the original (icon) position.
        """
        font = game_font(20)
        text1 = font.render(str(self.name), True, BLACK)
        text2 = font.render('$' + str(self.stack), True, BLACK)
        width = int(WIDTH * 0.1)
        height = int(HEIGHT * 0.1)
        image = pygame.transform.scale(label_player_image, (width, height))
        
        # Fixed on-screen positions.
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
            x, y = 0, 0  # Fallback position

        # Draw the player's label (image and text).
        win.blit(image, (x, y))
        win.blit(text1, (x + (width // 2 - text1.get_width() // 2),
                        y + (height // 4 - text1.get_height() // 3)))
        win.blit(text2, (x + (width // 2 - text1.get_width() // 3) - 10,
                        y + (3 * height // 4 - text1.get_height() // 1.5)))
                        
        # Get the player's role.
        role = self.get_role()
        
        # ------------------------
        # Draw the role text for all positions to the left of the player label.
        role_text = font.render(role, True, BLACK)
        # Adjust offset as needed (here, 10 pixels padding to the left)
        text_offset_x = x - role_text.get_width() - 10  
        text_offset_y = y + (height // 2 - role_text.get_height() // 2)
        win.blit(role_text, (text_offset_x, text_offset_y))
        # ------------------------
        
        # For roles that have icons, also draw the icon at the original designated position.
        role_icon_x = x + width - 30  # position remains unchanged
        role_icon_y = y - 35
        if role in ["BTN", "SB/BTN"]:
            win.blit(dealer_icon, (role_icon_x, role_icon_y))
        elif role == "SB":
            win.blit(sb_icon, (role_icon_x, role_icon_y))
        elif role == "BB":
            win.blit(bb_icon, (role_icon_x, role_icon_y))

                
    
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
                bet_x, bet_y = 610, 510  # example coordinates for player 0's bet text

            elif self == self.player_list_chair[1]:
                bet_x, bet_y = 310, 440  # example coordinates for player 1's bet text
            elif self == self.player_list_chair[2]:
                bet_x, bet_y = 310, 270  # example coordinates for player 2's bet text
            elif self == self.player_list_chair[3]:
                bet_x, bet_y = 610, 210  # example coordinates for player 3's bet text
            elif self == self.player_list_chair[4]:
                bet_x, bet_y = 920, 270  # example coordinates for player 4's bet text
            elif self == self.player_list_chair[5]:
                bet_x, bet_y = 920, 440  # example coordinates for player 5's bet text

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
        # (Pot drawing remains unchanged.)
        input_stack = sum(player.input_stack for player in Player.player_list)
        bets = sum(player.bet_auction for player in Player.player_list)
        width = win.get_width()
        height = win.get_height()
        font_size = max(20, int(height * 0.02))
        font = game_font(font_size)
        pot_text = f'Pot: ${input_stack - bets}'
        text_surface = font.render(pot_text, True, BEIGE)
        x = (width - text_surface.get_width()) // 2
        y = int((height - text_surface.get_height()) // 2.3)
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
