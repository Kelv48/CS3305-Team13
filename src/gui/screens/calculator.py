import pygame
import sys
import random
import itertools
from collections import Counter
from src.gui.utils.constants import screen_font, BG, SCREEN, scaled_cursor, FPS
pygame.init()

# ----- Global Constants & Settings -----
BG_COLOR = pygame.Color('white')
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
BUTTON_COLOR = pygame.Color('gray')
TEXT_COLOR = pygame.Color('white')
FONT = screen_font(32)
BIG_FONT = screen_font(48)

# Overlay colors for each group (RGBA where A is transparency)
PLAYER_OVERLAY_COLOR = (0, 0, 255, 100)     # Blue semi-transparent
OPPONENT_OVERLAY_COLOR = (255, 0, 0, 100)     # Red semi-transparent
BOARD_OVERLAY_COLOR = (0, 255, 0, 100)        # Green semi-transparent

# ----- Button Class -----
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.txt_surface = FONT.render(text, True, TEXT_COLOR)
        self.color = BUTTON_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ----- Card Parsing & Simulation Functions -----
def parse_card(card_str):
    card_str = card_str.strip().upper()
    if len(card_str) == 3:  # e.g., "10H"
        rank = card_str[:2]
        suit = card_str[2]
    elif len(card_str) == 2:
        rank = card_str[0]
        suit = card_str[1]
        if rank == 'T':  # Allow T as shorthand for 10.
            rank = '10'
    else:
        return None
    rank_dict = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    if rank not in rank_dict or suit not in ['S', 'H', 'D', 'C']:
        return None
    return (rank_dict[rank], suit)

def get_deck():
    deck = []
    for rank in range(2, 15):
        for suit in ['S', 'H', 'D', 'C']:
            deck.append((rank, suit))
    return deck

def evaluate_5card_hand(hand):
    hand = sorted(hand, key=lambda card: card[0], reverse=True)
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    is_flush = len(set(suits)) == 1
    unique_ranks = sorted(set(ranks), reverse=True)
    is_straight = False
    top_straight = None
    if len(unique_ranks) == 5:
        if unique_ranks[0] - unique_ranks[4] == 4:
            is_straight = True
            top_straight = unique_ranks[0]
        if unique_ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            top_straight = 5
    count = Counter(ranks)
    freq = sorted(count.items(), key=lambda x: (x[1], x[0]), reverse=True)
    if is_flush and is_straight:
        return (8, top_straight)
    if freq[0][1] == 4:
        kicker = [r for r in ranks if r != freq[0][0]][0]
        return (7, freq[0][0], kicker)
    if freq[0][1] == 3 and len(freq) > 1 and freq[1][1] >= 2:
        return (6, freq[0][0], freq[1][0])
    if is_flush:
        return (5, ranks)
    if is_straight:
        return (4, top_straight)
    if freq[0][1] == 3:
        kickers = sorted([r for r in ranks if r != freq[0][0]], reverse=True)
        return (3, freq[0][0], kickers)
    if freq[0][1] == 2 and len(freq) > 1 and freq[1][1] == 2:
        pair1 = max(freq[0][0], freq[1][0])
        pair2 = min(freq[0][0], freq[1][0])
        kicker = [r for r in ranks if r != freq[0][0] and r != freq[1][0]][0]
        return (2, (pair1, pair2), kicker)
    if freq[0][1] == 2:
        kickers = sorted([r for r in ranks if r != freq[0][0]], reverse=True)
        return (1, freq[0][0], kickers)
    return (0, ranks)

def best_hand(cards):
    best = None
    for combo in itertools.combinations(cards, 5):
        ranking = evaluate_5card_hand(list(combo))
        if best is None or ranking > best:
            best = ranking
    return best

def simulate_win_rate(my_cards, board_cards, opp_cards=None, num_simulations=1000):
    wins = 0
    ties = 0
    losses = 0
    deck = get_deck()
    used_cards = my_cards + board_cards
    if opp_cards is not None:
        used_cards += opp_cards
    for card in used_cards:
        if card in deck:
            deck.remove(card)
    remaining_board = 5 - len(board_cards)
    for _ in range(num_simulations):
        deck_copy = deck[:]
        random.shuffle(deck_copy)
        sim_board = board_cards[:] 
        sim_board += deck_copy[:remaining_board] 
        deck_remaining = deck_copy[remaining_board:]
        if opp_cards is None:
            sim_opp_cards = deck_remaining[:2]
        else:
            sim_opp_cards = opp_cards
        my_best = best_hand(my_cards + sim_board)
        opp_best = best_hand(sim_opp_cards + sim_board)
        if my_best > opp_best:
            wins += 1
        elif my_best == opp_best:
            ties += 1
        else:
            losses += 1
    total = wins + ties + losses
    win_rate = wins / total * 100
    tie_rate = ties / total * 100
    loss_rate = losses / total * 100
    return win_rate, tie_rate, loss_rate

# ----- Load Card Images -----
def load_card_images(card_width, card_height):
    card_images = {}
    rank_to_str = {11: "J", 12: "Q", 13: "K", 14: "A"}
    for rank in range(2, 15):
        for suit in ['S', 'H', 'D', 'C']:
            # For the 10 card, use "T" as the filename label.
            if rank == 10:
                rank_str = "T"
            elif rank < 10:
                rank_str = str(rank)
            else:
                rank_str = rank_to_str[rank]
            # File path updated to assets/cards
            filename = f"assets/cards/{rank_str}{suit}.png"
            try:
                image = pygame.image.load(filename).convert_alpha()
                image = pygame.transform.scale(image, (card_width, card_height))
            except Exception as e:
                # If the image file is not found, create a placeholder.
                image = pygame.Surface((card_width, card_height))
                image.fill(pygame.Color("white"))
                pygame.draw.rect(image, pygame.Color("black"), image.get_rect(), 2)
                text_surf = FONT.render(f"{rank_str}{suit}", True, TEXT_COLOR)
                image.blit(text_surf, (5, card_height // 2 - text_surf.get_height() // 2))
            card_images[(rank, suit)] = image
    return card_images

# ----- Main GUI Loop with Card Selection -----
def run_poker_calculator(mainMenu, num_simulations=1000):
    clock = pygame.time.Clock()
    clock.tick(FPS)

    # Dimensions for card images and grid layout.
    CARD_WIDTH, CARD_HEIGHT = 60, 90
    GRID_MARGIN_X, GRID_MARGIN_Y = 5, 5
    GRID_START_X, GRID_START_Y = 80, 90

    # Load all card images (from files or placeholders)
    card_images = load_card_images(CARD_WIDTH, CARD_HEIGHT)
    
    # Build a list for the 52-card grid.
    suit_order = ['C', 'H', 'S', 'D']  # Clubs, Hearts, Spades, Diamonds
    card_grid = []
    for row_index, suit in enumerate(suit_order):
        for col_index, rank in enumerate(range(2, 15)):
            card = (rank, suit)
            x = GRID_START_X + col_index * (CARD_WIDTH + GRID_MARGIN_X)
            y = GRID_START_Y + row_index * (CARD_HEIGHT + GRID_MARGIN_Y)
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            card_grid.append({"card": card, "rect": rect, "image": card_images[card]})
    
    # Create buttons for selecting which set to assign to.
    group_buttons = {}
    button_width, button_height = 120, 32
    group_buttons["player"] = Button(100, 550 - button_height - 10, button_width, button_height, "Player")
    group_buttons["opponent"] = Button(300, 550 - button_height - 10, button_width, button_height, "Opponent")
    group_buttons["board"] = Button(500, 550 - button_height - 10, button_width, button_height, "Board")

    # Calculate button.
    calculate_button = Button(900, 550 - button_height - 10, 120, 32, "Calculate")
    
    # ----- Back Button Setup -----
    back_button = Button(20, 20, 80, 30, "HOME")
    
    # Dictionary to hold card assignments.
    assignments = {
        "player": [None, None],       # exactly 2 cards required
        "opponent": [None, None],     # either leave blank or exactly 2 cards
        "board": [None, None, None, None, None]  # up to 5 cards; simulation will fill the rest
    }
    
    active_group = "player"  # which group is currently “active” for card selection
    result_text = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # Check if the back button was clicked.
                if back_button.is_clicked(pos):
                    mainMenu()	
                    return
                
                # Check if a group button was clicked.
                for group, button in group_buttons.items():
                    if button.is_clicked(pos):
                        active_group = group
                # Check if the Calculate button was clicked.
                if calculate_button.is_clicked(pos):
                    player_cards = [c for c in assignments["player"] if c is not None]
                    opp_cards = [c for c in assignments["opponent"] if c is not None]
                    board_cards = [c for c in assignments["board"] if c is not None]
                    if len(player_cards) != 2:
                        result_text = "Select exactly 2 cards for Player."
                    elif len(opp_cards) not in (0, 2):
                        result_text = "Select exactly 2 cards for Opponent or leave blank."
                    elif len(board_cards) > 5:
                        result_text = "Board can have at most 5 cards."
                    else:
                        result_text = "Running simulation..."
                        pygame.display.flip()  # Update display before simulation.
                        win_rate, tie_rate, loss_rate = simulate_win_rate(
                            player_cards, board_cards, opp_cards if opp_cards else None, num_simulations)
                        result_text = (f"Win: {win_rate:.1f}%\n"
                                       f"Tie: {tie_rate:.1f}%\n"
                                       f"Lose: {loss_rate:.1f}%")
                # Check if a card in the grid was clicked.
                for item in card_grid:
                    if item["rect"].collidepoint(pos):
                        card = item["card"]
                        # If the card is already assigned anywhere, remove it.
                        removed = False
                        for grp in assignments:
                            for idx, assigned_card in enumerate(assignments[grp]):
                                if assigned_card == card:
                                    assignments[grp][idx] = None
                                    removed = True
                        # If it wasn’t removed, assign it to the active group if a slot is free.
                        if not removed:
                            for i in range(len(assignments[active_group])):
                                if assignments[active_group][i] is None:
                                    assignments[active_group][i] = card
                                    break

        # ----- Drawing the UI -----
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Create a centered textbox background (95% width, 85% height)
        textbox_width = int(screen_width * 0.95)
        textbox_height = int(screen_height * 0.85)
        textbox_x = (screen_width - textbox_width) // 2
        textbox_y = (screen_height - textbox_height) // 2
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface,
            (0, 0, 0, 100),  # black with alpha=100 (semi-transparent)
            (0, 0, textbox_width, textbox_height),
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Place header text near top of textbox
        header_text = "EQUITY CALCULATOR"
        CALCULATOR_TEXT = screen_font(45).render(header_text, True, "Gold")
        header_y = 30
        CALCULATOR_RECT = CALCULATOR_TEXT.get_rect(center=(textbox_x + textbox_width // 2, header_y))
        SCREEN.blit(CALCULATOR_TEXT, CALCULATOR_RECT)
        
        # Draw group selection buttons (highlight the active one)
        for group, button in group_buttons.items():
            orig_color = button.color
            button.color = COLOR_ACTIVE if group == active_group else BUTTON_COLOR
            button.draw(SCREEN)
            button.color = orig_color  # restore original

        # --- Player Cards ---
        for i, card in enumerate(assignments["player"]):
            slot_x = 100 + i * (CARD_WIDTH + 10)
            slot_y = 550
            rect = pygame.Rect(slot_x, slot_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(SCREEN, TEXT_COLOR, rect, 2)
            if card is not None:
                SCREEN.blit(card_images[card], (slot_x, slot_y))

        # --- Opponent Cards ---
        for i, card in enumerate(assignments["opponent"]):
            slot_x = 300 + i * (CARD_WIDTH + 10)
            slot_y = 550
            rect = pygame.Rect(slot_x, slot_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(SCREEN, TEXT_COLOR, rect, 2)
            if card is not None:
                SCREEN.blit(card_images[card], (slot_x, slot_y))

        # --- Board Cards ---
        for i, card in enumerate(assignments["board"]):
            slot_x = 500 + i * (CARD_WIDTH + 10)
            slot_y = 550
            rect = pygame.Rect(slot_x, slot_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(SCREEN, TEXT_COLOR, rect, 2)
            if card is not None:
                SCREEN.blit(card_images[card], (slot_x, slot_y))
        
        # Draw the Calculate button.
        calculate_button.draw(SCREEN)
        # Draw the simulation result.
        result_surface = FONT.render(result_text, True, TEXT_COLOR)
        SCREEN.blit(result_surface, (900, 550 - button_height + 30))
        
        # Draw the full grid of 52 card images with overlay based on group assignment.
        for item in card_grid:
            SCREEN.blit(item["image"], item["rect"].topleft)
            overlay_color = None
            card = item["card"]
            if card in assignments["player"]:
                overlay_color = PLAYER_OVERLAY_COLOR
            elif card in assignments["opponent"]:
                overlay_color = OPPONENT_OVERLAY_COLOR
            elif card in assignments["board"]:
                overlay_color = BOARD_OVERLAY_COLOR

            if overlay_color:
                overlay = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
                overlay.fill(overlay_color)
                SCREEN.blit(overlay, item["rect"].topleft)
        
        # Draw the back button.
        back_button.draw(SCREEN)
        
        # *** Draw the custom cursor last so it’s always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)
        
        pygame.display.flip()