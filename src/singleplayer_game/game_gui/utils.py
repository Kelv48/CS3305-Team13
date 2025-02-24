import pygame
import pygame_widgets
from src.gui.utils.constants import game_font, scaled_cursor, GAME_BG

def showdown(common_cards):
    """
    Displays the showdown by drawing the player's cards, all active opponents' cards, 
    and the community cards (flop, turn, river).
    """
    from src.singleplayer_game.game_gui.player import Player
    from src.gui.utils.constants import SCREEN

    player_list_chair = Player.player_list_chair
    cards_group = pygame.sprite.Group()

    # Draw player cards if the player is active.
    if player_list_chair[0].live or player_list_chair[0].alin:
        for card in giveCard('player', player_list_chair[0].cards):
            cards_group.add(card)

    # Draw opponent cards if they are active.
    for idx, opponent in enumerate(player_list_chair[1:], start=1):
        if opponent.live or opponent.alin:
            opponent_type = f'opponent{idx}'
            for card in giveCard(opponent_type, opponent.cards):
                cards_group.add(card)

    # Draw community cards.
    for card in giveCard('flop', common_cards[0:3]):
        cards_group.add(card)
    for card in giveCard('turn', [common_cards[3]]):
        cards_group.add(card)
    for card in giveCard('river', [common_cards[4]]):
        cards_group.add(card)

    cards_group.draw(SCREEN)
    drawPlayer()
    pygame.display.flip()

def recapRound(list_winner, common_cards=None):
    """
    Displays the round summary.
    """
    from src.gui.utils.constants import SCREEN, WIDTH, HEIGHT, BEIGE, GAME_BG
    font = game_font(20) 
    screen_width, screen_height = SCREEN.get_size()

    # Draw background.
    scaled_bg = pygame.transform.scale(GAME_BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    poker_table_image = pygame.image.load("assets/images/Table.png")
    poker_table_image = pygame.transform.scale(poker_table_image, (700, 400)) 
    poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 1.9))
    SCREEN.blit(poker_table_image, poker_table_rect)
    drawPlayer()

    def y_coordinate(HEIGHT, text_height, space_height, space_bottom, n_winner):
        # Calculates the y-coordinate for round summary subtitles.
        w = [n_winner - 1 - i for i in range(n_winner)]
        x = HEIGHT - text_height - space_bottom
        y_co = []
        for i in range(len(w)):
            y_co.append(x - w[i] * (text_height + space_height))
        return y_co

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
        y_c = y_coordinate(HEIGHT, 20, 10, HEIGHT * 0.1, len(list_winner))
        for i in range(len(list_winner)):
            text = '{} won ${} with {}'.format(str(list_winner[i][0].name), str(list_winner[i][1]),
                                               str(list_winner[i][0].hand))
            text = font.render(text, True, BEIGE)
            x, y = WIDTH * 0.05, y_c[i]
            SCREEN.blit(text, (x, y))
        pygame.display.flip()
        pygame.time.delay(3000)

def drawPlayer():
    """
    Displays player labels and their bet information.
    """
    from src.singleplayer_game.game_gui.player import Player
    from src.gui.utils.constants import SCREEN
    player_list_chair = Player.player_list_chair
    for player in player_list_chair:
        player.playerLabel(SCREEN)
        player.drawBet(SCREEN)
    pygame.display.flip()

def giveCard(type_card, cards):
    """
    Places the cards in their designated positions and returns a group of card sprites.
    """
    import pygame
    from src.gui.utils.constants import cards_object

    dict_cards = {
        'player': ['first_card_player', 'second_card_player'],
        'opponent1': ['first_card_opponent1', 'second_card_opponent1'],
        'opponent2': ['first_card_opponent2', 'second_card_opponent2'],
        'opponent3': ['first_card_opponent3', 'second_card_opponent3'],
        'opponent4': ['first_card_opponent4', 'second_card_opponent4'],
        'opponent5': ['first_card_opponent5', 'second_card_opponent5'],
        'flop': ['first_card_flop', 'second_card_flop', 'third_card_flop'],
        'turn': ['turn_card'],
        'river': ['river_card']
    }

    sub_cards = pygame.sprite.Group()
    list_cards = dict_cards[type_card]

    for i in range(len(list_cards)):
        card_object = cards_object[cards[i]]
        card_object.type_card = list_cards[i]
        card_object.putInPlace()
        sub_cards.add(card_object)
    return sub_cards

def coverUpCards(player_list):
    """
    Returns a sprite group of face-down cards for opponents who have not folded.
    """
    import pygame
    from src.gui.utils.constants import cards_object
    from src.singleplayer_game.game_gui.card import Card

    reverse_cards = pygame.sprite.Group()
    base_reverse_card_1 = cards_object['reverse_1']
    base_reverse_card_2 = cards_object['reverse_2']

    for i in range(1, len(player_list)):
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
    """
    Displays buttons on the screen.
    """
    from src.gui.utils.constants import SCREEN
    [button.draw(SCREEN) for button in buttons if button.active]

def arrangeRoom(mainMenu, common_cards=None):
    """
    Draws the game room background, table, cards, and a Main Menu button.
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

    if player_list_chair[0].live or player_list_chair[0].alin:
        sub_card = giveCard('player', player_list_chair[0].cards)
        for card in sub_card:
            cards.add(card)

    for i, opponent_type in enumerate(['opponent1'], start=1):
        if player_list_chair[i].live or player_list_chair[i].alin:
            sub_card = giveCard(opponent_type, player_list_chair[i].cards)
            for card in sub_card:
                cards.add(card)

    reverse_cards = coverUpCards(player_list_chair)
    for card in reverse_cards:
        cards.add(card)
    
    cards.draw(SCREEN)

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

    # Draw Main Menu Button.
    button_rect = pygame.Rect(10, 10, 150, 50)
    pygame.draw.rect(SCREEN, (200, 0, 0), button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Main Menu", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    SCREEN.blit(text, text_rect)
    return button_rect

import time
from src.gui.utils.constants import SCREEN, BEIGE, GREEN
from src.singleplayer_game.game_gui.game_button import x_buttons, y_button, width_button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

def playerDecision(buttons, dict_options, min_raise, max_raise, common_cards=None):
    """
    Displays the GUI for a player's decision and returns their action.
    If no action is received within a set time, auto-fold is returned.
    """

    # Set up slider and output for raising.
    x_slider = 1070
    y_slider = 650
    slider = Slider(SCREEN, x_slider, y_slider, width_button * 2, 40,
                    min=0, max=max_raise - min_raise, initial=0, step=1,
                    colour=(94, 151, 82), handleColour=BEIGE, handleRadius=19)

    x_output = 1060
    y_output = 590
    font = game_font(20)
    output = TextBox(SCREEN, x_output, y_output, 100, 50, fontSize=20,
                     colour=GREEN, textColour=BEIGE, font=font)
    output.setText('1')
    output.disable()

    # Set the active status for the buttons.
    for button in buttons:
        button.active = dict_options.get(button.name, False)

    # Draw the common background elements once before the loop.
    arrangeRoom(common_cards)
    drawPlayer()

    pause_action = True
    start_time = time.time()
    decision = None

    while pause_action:
        # Clear the frame by redrawing the background and players.
        # (Replace BG below with your background if needed)
        # Draw background.
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(GAME_BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))
        arrangeRoom(common_cards)
        drawPlayer()
        drawButtons(buttons)

        # Process events.
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
                        break
            if event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    if button.active:
                        button.bigger(mouse_position)
            # Update slider output if needed.
            for button in buttons:
                if button.name == 'raise' and button.active:
                    output.setText('$' + str(slider.getValue() + min_raise))
                    pygame_widgets.update(event)

        # Draw slider and output text.
        slider.draw()   # Ensure your Slider class has a draw method.
        output.draw()   # And your TextBox class as well.

        # Finally, draw the custom cursor once per frame.
        drawCustomCursor()
        # One display update per frame.
        pygame.display.update()

        # # Check for timeout.
        # if time.time() - start_time >= 5:
        #     decision = ['fold']
        #     pause_action = False

    return decision

def splitPot():
    """
    Adjusts each player's chip stack and returns a list of tuples
    with the player and the chips they win for the round.
    """
    from itertools import groupby
    from src.singleplayer_game.game_gui.player import Player

    players = [p for p in Player.player_list_chair if p.live or p.alin]
    if not players:
        return []

    players.sort(key=lambda p: (-p.score, p.input_stack))
    n = len(players)
    scores = [p.score for p in players]
    bets = [p.input_stack for p in players]

    global_max = max(scores)

    def compute_input_in_game(i):
        if scores[i] == global_max:
            return bets[i]
        prev_bets = [bets[j] for j in range(i) if scores[j] != scores[i]]
        deduction = max(prev_bets) if prev_bets else 0
        return bets[i] - deduction if bets[i] > deduction else 0

    input_in_game = [compute_input_in_game(i) for i in range(n)]

    def distribute_side_pots(scores, bets):
        win_list = [0] * len(scores)
        groups = [list(group) for score, group in groupby(range(len(scores)), key=lambda i: scores[i])]
        for g_idx, group in enumerate(groups):
            group_count = len(group)
            for lower_group in groups[g_idx + 1:]:
                for j in lower_group:
                    for i in group:
                        if bets[i] >= bets[j]:
                            win_list[i] += bets[j] / group_count
                            bets[j] = 0
                        else:
                            win_list[i] += bets[i] / group_count
                            bets[j] -= bets[i]
            base_win = win_list[group[0]]
            for i in group[1:]:
                win_list[i] = base_win
                bets[i] -= bets[group[0]]
        return win_list

    win_list = distribute_side_pots(scores, bets)

    winners = []
    for i in range(n):
        total_win = input_in_game[i] + win_list[i]
        players[i].win(total_win)
        winners.append((players[i], int(win_list[i])))


    return winners

def onePlayerWin():
    """
    Processes a round where a single player wins by taking all chips.
    """
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
    Advances the dealer index by one seat clockwise.
    """
    from src.singleplayer_game.game_gui.player import Player
    num_players = len(Player.player_list)
    Player.dealer_index = (Player.dealer_index + 1) % num_players  
    


def drawCustomCursor():
    """
    Draws the custom cursor image at the current mouse position.
    Call this function after all other drawing calls (i.e., at the end of your main loop)
    so that it always appears on top.
    """
    from src.gui.utils.constants import SCREEN, scaled_cursor
    # *** Draw the custom cursor last so it’s always on top ***
    current_mouse_pos = pygame.mouse.get_pos()
    SCREEN.blit(scaled_cursor, current_mouse_pos)