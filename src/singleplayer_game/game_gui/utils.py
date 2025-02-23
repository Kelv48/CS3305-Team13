import pygame
import pygame_widgets
from src.gui.utils.constants import game_font

def showdown(common_cards):
    """
    Displays the showdown by drawing the player's cards, all active opponents' cards, 
    and the community cards (flop, turn, river) on the screen.

    :param common_cards: List of common card identifiers.
                         Expected order: [flop1, flop2, flop3, turn, river]
    """
    from src.singleplayer_game.game_gui.player import Player
    from src.gui.utils.constants import SCREEN

    player_list_chair = Player.player_list_chair
    cards_group = pygame.sprite.Group()

    # Draw player cards if the player is active.
    if player_list_chair[0].live or player_list_chair[0].alin:
        for card in giveCard('player', player_list_chair[0].cards):
            cards_group.add(card)

    # Dynamically draw opponent cards for each opponent if they haven't folded.
    # Opponents are stored starting from index 1.
    for idx, opponent in enumerate(player_list_chair[1:], start=1):
        if opponent.live or opponent.alin:
            opponent_type = f'opponent{idx}'
            for card in giveCard(opponent_type, opponent.cards):
                cards_group.add(card)

    # Draw community cards:
    # Flop cards (first three common cards)
    for card in giveCard('flop', common_cards[0:3]):
        cards_group.add(card)
    # Turn card (fourth common card)
    for card in giveCard('turn', [common_cards[3]]):
        cards_group.add(card)
    # River card (fifth common card)
    for card in giveCard('river', [common_cards[4]]):
        cards_group.add(card)

    # Draw all card sprites on the screen and update the display.
    cards_group.draw(SCREEN)
    drawPlayer()
    pygame.display.flip()




def recapRound(list_winner, common_cards=None):
    """
    Function displays the round summary
    :param list_winner: list_winner = [(player1, win_value1),(player2, win_value2)]
    :param common_cards:
    :return:
    """


    from src.gui.utils.constants import SCREEN, WIDTH, HEIGHT, BEIGE, GAME_BG
    font = game_font(20) 



    screen_width, screen_height = SCREEN.get_size()
    # SCREEN.fill("black")

    # Draw background
    scaled_bg = pygame.transform.scale(GAME_BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    poker_table_image = pygame.image.load("assets/images/Table.png")
    poker_table_image = pygame.transform.scale(poker_table_image, (700, 400)) 
    poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 1.9))
    SCREEN.blit(poker_table_image, poker_table_rect)
    drawPlayer()


    def y_coordinate(HEIGHT, text_height, space_height, space_bottom, n_winner):
        # calculates the height position for the round summary subtitles
        w = [n_winner - 1 - i for i in range(n_winner)]
        x = HEIGHT - text_height - space_bottom
        y_co = []
        for i in range(len(w)):
            y_co.append(x - w[i] * (text_height + space_height))
        return y_co

    # Display who, how much win
    if len(list_winner) == 1:
        text = '{} won ${}'.format(str(list_winner[0][0].name), str(list_winner[0][1]))
        text = font.render(text, True, BEIGE)
        y_c = y_coordinate(HEIGHT, text.get_height(), text.get_height() // 2, HEIGHT * 0.1, len(list_winner))
        x, y = WIDTH * 0.05, y_c[0]
        SCREEN.blit(text, (x, y))
        pygame.display.flip()
        pygame.time.delay(1000)
    else:
        showdown(common_cards)


        text = ''
        text = font.render(text, True, BEIGE)
        y_c = y_coordinate(HEIGHT, text.get_height(), text.get_height() // 2, HEIGHT * 0.1, len(list_winner))
        for i in range(len(list_winner)):
            text = '{} won ${} with {}'.format(str(list_winner[i][0].name), str(list_winner[i][1]),
                                               str(list_winner[i][0].hand))
            text = font.render(text, True, BEIGE)
            x, y = WIDTH * 0.05, y_c[i]
            SCREEN.blit(text, (x, y))
        pygame.display.flip()
        # Take a second pause

        pygame.time.delay(3000) # Time between each round. Adjust higher if needed


def drawPlayer():
    # Function displays player labels and bet information
    from src.singleplayer_game.game_gui.player import Player
    from src.gui.utils.constants import SCREEN
    player_list_chair = Player.player_list_chair
    for player in player_list_chair:

        player.playerLabel(SCREEN)
        player.drawBet(SCREEN)
    pygame.display.flip()






def giveCard(type_card, cards):
    """
    Function put the cards on the right place and return group of cards sprite.

    :param type_card: type of card, one of these player, opponent, flop, turn, river
    :param cards: list of cards ex. ['2S', '3C']
    :return:group of cards sprite
    """

    import pygame
    from src.gui.utils.constants import cards_object


    dict_cards = {'player': ['first_card_player', 'second_card_player'],
                  'opponent1': ['first_card_opponent1', 'second_card_opponent1'],
                  'opponent2': ['first_card_opponent2', 'second_card_opponent2'],
                  'opponent3': ['first_card_opponent3', 'second_card_opponent3'],
                  'opponent4': ['first_card_opponent4', 'second_card_opponent4'],
                  'opponent5': ['first_card_opponent5', 'second_card_opponent5'],
                  'flop': ['first_card_flop', 'second_card_flop', 'third_card_flop'],
                  'turn': ['turn_card'],
                  'river': ['river_card']}

    sub_cards = pygame.sprite.Group()
    list_cards = dict_cards[type_card]  # 'first_card_player', 'second_card_player'
    



    for i in range(len(list_cards)):
        card_object = cards_object[cards[i]]
        card_object.type_card = list_cards[i]
        card_object.putInPlace()
        sub_cards.add(card_object)
    return sub_cards



# def event_ESC_pressed(get_pressed):
#     if get_pressed[pygame.K_ESCAPE]:
#         exit()



def coverUpCards(player_list):
    """
    Returns a sprite group of reverse (face-down) cards for opponents who have not folded.
    
    :param player_list: List of player objects. Opponents are assumed to be indices 1 and onward.
    """
    import pygame
    from src.gui.utils.constants import cards_object
    from src.singleplayer_game.game_gui.card import Card  # Adjust the import path if needed

    reverse_cards = pygame.sprite.Group()
    base_reverse_card_1 = cards_object['reverse_1']
    base_reverse_card_2 = cards_object['reverse_2']

    # Iterate over opponents (assumed indices 1..n)
    for i in range(1, len(player_list)):
        # Only add reverse cards if the opponent is active (has not folded)
        if player_list[i].live or player_list[i].alin:
            new_reverse_card_1 = Card(base_reverse_card_1.original_image)
            new_reverse_card_2 = Card(base_reverse_card_2.original_image)

            new_reverse_card_1.type_card = f'first_card_opponent{i}'
            new_reverse_card_2.type_card = f'second_card_opponent{i}'

            new_reverse_card_1.putInPlace()
            new_reverse_card_2.putInPlace()

            reverse_cards.add(new_reverse_card_1)
            reverse_cards.add(new_reverse_card_2)
    return reverse_cards





def drawButtons(buttons):
    # Function displays buttons
    from src.gui.utils.constants import SCREEN


    [button.draw(SCREEN) for button in buttons if button.active]



def arrangeRoom(mainMenu, common_cards=None):
    """
    Draws the game room background, cards, and a Main Menu button.
    Only active players (not folded) have their cards displayed.
    """
    import pygame
    from src.gui.utils.constants import SCREEN, GAME_BG
    from src.singleplayer_game.game_gui.player import Player

    player_list_chair = Player.player_list_chair
    screen_width, screen_height = SCREEN.get_size()

    # Draw background and table.
    scaled_bg = pygame.transform.scale(GAME_BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))
    poker_table_image = pygame.image.load("assets/images/Table.png")
    poker_table_image = pygame.transform.scale(poker_table_image, (700, 400))
    poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 1.9))
    SCREEN.blit(poker_table_image, poker_table_rect)

    cards = pygame.sprite.Group()

    # Draw player's cards if active.
    if player_list_chair[0].live or player_list_chair[0].alin:
        sub_card = giveCard('player', player_list_chair[0].cards)
        for card in sub_card:
            cards.add(card)

    # Draw opponent cards for indices 1 to 4.
    for i, opponent_type in enumerate(['opponent1'], start=1):
        if player_list_chair[i].live or player_list_chair[i].alin:
            sub_card = giveCard(opponent_type, player_list_chair[i].cards)
            for card in sub_card:
                cards.add(card)

    # Add reverse (face-down) cards only for active opponents.
    reverse_cards = coverUpCards(player_list_chair)
    for card in reverse_cards:
        cards.add(card)
    
    # Draw all card sprites.
    cards.draw(SCREEN)

    # Draw community cards (if provided) and update the display.
    if common_cards is not None:
        from src.singleplayer_game.game_gui.player import Player
        Player.drawPot(SCREEN)
        sub_card = giveCard('flop', common_cards[0:3])
        for card in sub_card:
            cards.add(card)
        cards.draw(SCREEN)
        if len(common_cards) >= 4:
            sub_card = giveCard('turn', [common_cards[3]])
            for card in sub_card:
                cards.add(card)
            cards.draw(SCREEN)
        if len(common_cards) == 5:
            sub_card = giveCard('river', [common_cards[4]])
            for card in sub_card:
                cards.add(card)
            cards.draw(SCREEN)

    # ----- Add Main Menu Button -----
    # Define the button rectangle (positioned at top left)
    button_rect = pygame.Rect(10, 10, 150, 50)  # (x, y, width, height)
    # Draw the button (using a simple color fill)
    pygame.draw.rect(SCREEN, (200, 0, 0), button_rect)  # red button
    # Draw the text on the button
    font = pygame.font.Font(None, 36)
    text = font.render("Main Menu", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    SCREEN.blit(text, text_rect)

    # Optionally, you might return the button's rect so your event loop can access it.
    return button_rect





import time
from src.gui.utils.constants import SCREEN, BEIGE, GREEN
from src.singleplayer_game.game_gui.game_button import x_buttons, y_button, width_button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

def playerDecision(buttons, dict_options, min_raise, max_raise, common_cards=None):
    """
    Display GUI for a player and return their action.
    
    :param buttons: buttons object
    :param dict_options: dict with information about which buttons are active
    :param min_raise: minimum raise value
    :param max_raise: maximum raise value
    :param common_cards: list of common cards (if any)
    :return: a list with the decision; if 'raise' is chosen, also returns the raise amount.
             If no action is made within 20 seconds, returns ['fold'].
    """

    # Fixed position for the slider (independent from x_buttons)
    x_slider = 1070  # Fixed x position for the slider
    y_slider = 650   # Fixed y position (adjust based on layout)

    # Slider setup (decoupled from button positions)
    slider = Slider(SCREEN, x_slider, y_slider, width_button * 2, 40,
                    min=0, max=max_raise - min_raise, initial=0, step=1,
                    colour=(94, 151, 82), handleColour=BEIGE, handleRadius=19)

    # Fixed position for the output text box
    x_output = 1060  # Fixed x position for the output box
    y_output = 590   # Fixed y position (adjust as needed)

    font = game_font(20)
    output = TextBox(SCREEN, x_output, y_output, 100, 50, fontSize=20,
                     colour=GREEN, textColour=BEIGE, font=font)
    output.setText('1')
    output.disable()

    # Activate proper buttons based on options
    for button in buttons:
        button.active = dict_options.get(button.name, False)

    # Arrange common cards and update player display (assumes these functions are defined elsewhere)
    arrangeRoom(common_cards)
    drawPlayer()

    pause_action = True
    start_time = time.time()
    decision = None

    while pause_action:
        # Check if 20 seconds have elapsed and auto-fold if so.
        if time.time() - start_time >= 5:
            decision = ['fold']
            pause_action = False
            break

        drawButtons(buttons)

        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.isOver(mouse_position) and button.active:
                        if button.name == 'raise':
                            decision = [button.name, slider.getValue() + min_raise]
                        else:
                            decision = [button.name]
                        pause_action = False
                        break  # Exit the inner loop once a decision is made

            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.active:
                        button.bigger(mouse_position)

            # For the raise button, update the slider output display if active
            for button in buttons:
                if button.name == 'raise' and button.active:
                    output.setText('$' + str(slider.getValue() + min_raise))
                    pygame_widgets.update(event)
                pygame.display.update()

    return decision


def splitPot():
    """
    Adjusts each player's chip stack and returns a list of tuples containing
    the player and the chips they win (from opponents’ bets) for the round.
    """
    from itertools import groupby
    from src.singleplayer_game.game_gui.player import Player

    # Filter out players who have folded (both 'live' and 'alin' are False)
    players = [p for p in Player.player_list_chair if p.live or p.alin]
    if not players:
        return []

    # Sort players by descending score; for ties, by ascending bet.
    players.sort(key=lambda p: (-p.score, p.input_stack))
    n = len(players)
    scores = [p.score for p in players]
    # Copy bets for local processing (chips each player put into the pot)
    bets = [p.input_stack for p in players]

    # --- Helper 1: Compute each player's own returned chips ---
    global_max = max(scores)

    def compute_input_in_game(i):
        # Players with the global max score get back all of their bet.
        if scores[i] == global_max:
            return bets[i]
        # Otherwise, subtract the largest bet from any higher‐ranked player with a different score.
        prev_bets = [bets[j] for j in range(i) if scores[j] != scores[i]]
        deduction = max(prev_bets) if prev_bets else 0
        return bets[i] - deduction if bets[i] > deduction else 0

    input_in_game = [compute_input_in_game(i) for i in range(n)]

    # --- Helper 2: Distribute side-pot winnings using groups by score ---
    def distribute_side_pots(scores, bets):
        win_list = [0] * len(scores)
        # Group indices of players by score (players are already sorted)
        groups = [list(group) for score, group in groupby(range(len(scores)), key=lambda i: scores[i])]
        for g_idx, group in enumerate(groups):
            group_count = len(group)
            # For each lower-scoring group, process each player in that group.
            for lower_group in groups[g_idx + 1:]:
                for j in lower_group:
                    # Each player in the current group wins from the lower-scoring player's bet.
                    # The win is either the full bet from j (if the current player's bet is high enough)
                    # or as much as the current player's own bet.
                    for i in group:
                        if bets[i] >= bets[j]:
                            win_list[i] += bets[j] / group_count
                            bets[j] = 0
                        else:
                            win_list[i] += bets[i] / group_count
                            bets[j] -= bets[i]
            # Equalize winnings among players in the same group and adjust their bets.
            base_win = win_list[group[0]]
            for i in group[1:]:
                win_list[i] = base_win
                bets[i] -= bets[group[0]]
        return win_list

    win_list = distribute_side_pots(scores, bets)

    # --- Finalize: Update players and build return list ---
    winners = []
    for i in range(n):
        total_win = input_in_game[i] + win_list[i]
        players[i].win(total_win)
        winners.append((players[i], int(win_list[i])))

    return winners


def onePlayerWin():
    #  Function changing player stack who win, and return list tuple who win and how much
    from src.singleplayer_game.game_gui.player import Player
    player_list = Player.player_list_chair.copy()
    list_winner = []
    for player in player_list:


        if player.live or player.alin:
            win_value = sum([player.input_stack for player in player_list])
            player.win(win_value)
            list_winner.append((player, win_value - player.input_stack))
    return list_winner


def changePlayersPositions():
    """
    Advance the dealer index by one seat clockwise.
    This rotates the roles (dealer, SB, BB) without affecting the on-screen positions.
    """
    from src.singleplayer_game.game_gui.player import Player
    num_players = len(Player.player_list)
    Player.dealer_index = (Player.dealer_index + 1) % num_players  