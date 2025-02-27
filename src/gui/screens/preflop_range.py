import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor

# ================================================================
# 1. Helper Functions for Valid Positions  
# ================================================================

def get_valid_hero_positions(scenario):
    """
    Returns a list of valid Hero seats for the given scenario.
    """
    if scenario == "Open":
        return ["LJ", "HJ", "CO", "BTN", "SB"]
    elif scenario == "vs raise":
        return ["HJ", "CO", "BTN", "SB", "BB"]
    elif scenario == "vs 3bet":
        return ["LJ", "HJ", "CO", "BTN", "SB"]
    elif scenario == "vs 4bet":
        return ["HJ", "CO", "BTN", "SB", "BB"]
    elif scenario == "vs 5bet":
        return ["LJ", "HJ", "CO", "BTN", "SB"]
    else:
        return []

def get_valid_villain_positions(scenario, hero):
    """
    Returns a list of valid Villain seats for the given scenario and Hero seat.
    """
    if scenario == "Open":
        return []
    elif scenario in ["vs raise", "vs 4bet"]:
        # For these scenarios, the valid positions are those used in the data.
        valid_positions = ["HJ", "CO", "BTN", "SB", "BB"]
        # Return all valid positions except the hero.
        return [pos for pos in valid_positions if pos != hero]
    elif scenario == "vs 3bet":
        if hero == "LJ":   return ["HJ", "CO", "BTN", "SB", "BB"]
        if hero == "HJ":   return ["CO", "BTN", "SB", "BB"]
        if hero == "CO":   return ["BTN", "SB", "BB"]
        if hero == "BTN":  return ["SB", "BB"]
        if hero == "SB":   return ["BB"]
    elif scenario == "vs 5bet":
        if hero == "LJ":   return ["HJ", "CO", "BTN", "SB", "BB"]
        if hero == "HJ":   return ["CO", "BTN", "SB", "BB"]
        if hero == "CO":   return ["BTN", "SB", "BB"]
        if hero == "BTN":  return ["SB", "BB"]
        if hero == "SB":   return ["BB"]
    return []

# ================================================================
# 2. Functions to Update and Determine Visible Options
# ================================================================

def update_visible_options(options_data):
    """
    Updates the valid hero and villain options in options_data based on the
    current scenario and hero selection.
    """
    scenario_sel = options_data["Scenario"]["selected"]

    # Update hero (player) options.
    valid_heroes = get_valid_hero_positions(scenario_sel)
    hero_sel = options_data["player"]["selected"]
    if hero_sel not in valid_heroes:
        hero_sel = valid_heroes[0] if valid_heroes else None
    options_data["player"]["options"] = valid_heroes
    options_data["player"]["selected"] = hero_sel

    # Update villain (opponent) options.
    valid_villains = []
    if hero_sel:
        valid_villains = get_valid_villain_positions(scenario_sel, hero_sel)
    opp_sel = options_data["opponent"]["selected"]
    if opp_sel not in valid_villains and valid_villains:
        opp_sel = valid_villains[0]
    options_data["opponent"]["options"] = valid_villains
    options_data["opponent"]["selected"] = opp_sel

def get_visible_categories(options_data):
    """
    Returns a list of option categories to display.
    Always show Scenario and player; show opponent only if there are valid options.
    """
    visible = ["Scenario", "player"]
    if options_data["opponent"]["options"]:
        visible.append("opponent")
    return visible

# ================================================================
# 3. Preflop Range Visualizer Code
# ================================================================

def preflop_range_visualizer(mainMenu):
    pygame.init()
    
    # ----------------------------------------------------------------
    # Window and Asset Setup
    # ----------------------------------------------------------------
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    
    # Create an overlay textbox.
    textbox_width = int(screen_width * 0.95)
    textbox_height = int(screen_height * 0.85)
    textbox_x = (screen_width - textbox_width) // 2
    textbox_y = (screen_height - textbox_height) // 2
    textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
    pygame.draw.rect(textbox_surface, (0, 0, 0, 100), (0, 0, textbox_width, textbox_height), border_radius=50)
    
    # Header text.
    header_text = "This is the PREFLOP RANGE screen."
    HAND_VISUALIZER_TEXT = screen_font(45).render(header_text, True, "White")
    header_rect = HAND_VISUALIZER_TEXT.get_rect(center=(textbox_x + textbox_width // 2, textbox_y - 20))
    
    # ----------------------------------------------------------------
    # Grid Layout Settings
    # ----------------------------------------------------------------
    GRID_SIZE = 13
    CELL_SIZE = 43
    MARGIN = 0
    GRID_WIDTH = (CELL_SIZE + MARGIN) * GRID_SIZE
    GRID_HEIGHT = (CELL_SIZE + MARGIN) * GRID_SIZE
    container_x = 60
    container_y = 70
    
    # Colors and font.
    RAISE_COLOR = (255, 0, 0)      # bright red
    CALL_COLOR  = (0, 200, 0)      # green
    FOLD_COLOR  = (100, 100, 100)  # dark grey
    BLACK       = (0, 0, 0)
    font = screen_font(20)
    
    # ----------------------------------------------------------------
    # Strategy Data Setup (strat_data)
    # ----------------------------------------------------------------
    # Define full player options for open/3bet/5bet and vs raise/4bet.
    players_open = ["LJ", "HJ", "CO", "BTN", "SB"]
    players_raise = ["HJ", "CO", "BTN", "SB", "BB"]
    opponents = ["HJ", "CO", "BTN", "SB", "BB"]
    strat_data = {}
    
    # Open ranges for each hero position.
    open_ranges = {
        "LJ": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                         "QJs", "QTs", "Q9s",
                         "JTs",
                         "AKo", "AQo", "AJo", "ATo",
                         "KQo", "KJo", "QJo"},
                 "call": set()},
        "HJ": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                         "QJs", "QTs", "Q9s", "Q8s",
                         "JTs",
                         "AKo", "AQo", "AJo", "ATo", "A9o",
                         "KQo", "KJo", "KTo", "QJo", "QTo"},
                 "call": set()},
        "CO": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s",
                         "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s",
                         "JTs", "J9s", "J8s", "J7s",
                         "T9s", "T8s",
                         "98s",
                         "AKo", "AQo", "AJo", "ATo", "A9o", "A8o",
                         "KQo", "KJo", "KTo", "K9o",
                         "QJo", "QTo", "JTo"},
                 "call": set()},
        "BTN": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                          "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                          "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                          "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                          "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s",
                          "T9s", "T8s", "T7s", "T6s",
                          "98s", "97s", "96s",
                          "87s", "86s",
                          "76s", "75s",
                          "65s",
                          "54s",
                          "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o",
                          "KQo", "KJo", "KTo", "K9o", "K8o",
                          "QJo", "QTo", "Q9o",
                          "JTo", "J9o",
                          "T9o"},
                 "call": set()},
        "SB": {"raise": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                         "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                         "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                         "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                         "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s",
                         "T9s", "T8s", "T7s", "T6s",
                         "98s", "97s", "96s",
                         "87s", "86s",
                         "76s", "75s",
                         "65s",
                         "54s",
                         "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o",
                         "KQo", "KJo", "KTo", "K9o", "K8o",
                         "QJo", "QTo", "Q9o",
                         "JTo", "J9o",
                         "T9o"},
                 "call": set()}
    }
    # For "Open", assign open_ranges for every opponent.
    for player in players_open:
        for opponent in opponents:
            strat_data[("Open", player, opponent)] = open_ranges[player]
    

    # --- vs raise Scenario ---
    # Player options: HJ, CO, BTN, SB, BB
    vs_raise_data = {
        "BB": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AQs", "AJs", "ATs"},
            "call": {"TT", "99", "88", "77"}
        },
        "HJ": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AQs"},
            "call": {"TT", "99", "AQo", "KQs"}
        },
        "CO": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AQs"},
            "call": {"TT", "99", "AJo", "KQs"}
        },
        "BTN": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AQs", "AJs"},
            "call": {"TT", "99", "AQo", "KQs"}
        },
        "SB": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AQs"},
            "call": {"TT", "99", "AJo", "KQs"}
        }
    }

    # --- vs 3bet Scenario ---
    # Player options: LJ, HJ, CO, BTN, SB
    vs_3bet_data = {
        "LJ": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "99", "AQs", "AJs", "KQs"}
        },
        "HJ": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo", "AQs"},
            "call": {"JJ", "TT", "99", "AQo", "KQs", "JTs"}
        },
        "CO": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AKo", "AQs"},
            "call": {"TT", "99", "88", "AJs", "KQs", "JTs"}
        },
        "BTN": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo", "AQs", "AJs"},
            "call": {"JJ", "TT", "99", "88", "KQs", "JTs"}
        },
        "SB": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "99", "AQs", "KQs"}
        }
    }
    
    
    # --- vs 4bet Scenario ---
    # Player options: HJ, CO, BTN, SB, BB
    vs_4bet_data = {
        "BB": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "AQs", "AJs"}
        },
        "HJ": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "99", "AQs", "AJs", "KQs"}
        },
        "CO": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AKo"},
            "call": {"TT", "99", "88", "AQs", "AJs", "KQs", "KQo"}
        },
        "BTN": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AKo", "AQs"},
            "call": {"TT", "99", "88", "77", "AJs", "KQs", "QJs"}
        },
        "SB": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "99", "AQs", "AJs"}
        }
    }
    
    # --- vs 5bet Scenario ---
    # Player options: LJ, HJ, CO, BTN, SB
    vs_5bet_data = {
        "LJ": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT"}
        },
        "HJ": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT"}
        },
        "CO": {
            "raise": {"AA", "KK", "QQ", "JJ", "AKs", "AKo"},
            "call": {"TT", "99"}
        },
        "BTN": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT", "99"}
        },
        "SB": {
            "raise": {"AA", "KK", "QQ", "AKs", "AKo"},
            "call": {"JJ", "TT"}
        }
    }
    
    
    
    # Populate strat_data with the proper keys based on the scenario.
    for scenario, data in [
        ("vs raise", vs_raise_data),
        ("vs 3bet", vs_3bet_data),
        ("vs 4bet", vs_4bet_data),
        ("vs 5bet", vs_5bet_data)
    ]:
        # Use the correct player keys for each scenario.
        if scenario in ["vs raise", "vs 4bet"]:
            scenario_players = players_raise
        else:
            scenario_players = players_open
        for player in scenario_players:
            for opponent in opponents:
                strat_data[(scenario, player, opponent)] = data[player]
    
    # ----------------------------------------------------------------
    # 4. Side Panel Setup
    # ----------------------------------------------------------------
    # Initial options_data for side panel.
    options_data = {
        "Scenario": {
            "options": ["Open", "vs raise", "vs 3bet", "vs 4bet", "vs 5bet"],
            "selected": "Open"
        },
        "player": {
            "options": ["LJ", "HJ", "CO", "BTN", "SB"],
            "selected": "LJ"
        },
        "opponent": {
            "options": ["HJ", "CO", "BTN", "SB", "BB"],
            "selected": "BB"
        }
    }
    
    def draw_radio_buttons(label, x_start, y_start, options_list, selected_option):
        button_rects = []
        label_surf = font.render(label, True, (255, 255, 255))
        SCREEN.blit(label_surf, (x_start, y_start))
        spacing_y = 30
        btn_y = y_start + 25
        for opt in options_list:
            color = (100, 200, 100) if opt == selected_option else (200, 200, 200)
            rect = pygame.Rect(x_start, btn_y, 110, 25)
            pygame.draw.rect(SCREEN, color, rect, border_radius=5)
            pygame.draw.rect(SCREEN, BLACK, rect, 1, border_radius=5)
            text_surf = font.render(opt, True, BLACK)
            text_rect = text_surf.get_rect(center=rect.center)
            SCREEN.blit(text_surf, text_rect)
            button_rects.append((rect, opt))
            btn_y += spacing_y
        return button_rects
    
    side_panel_buttons = []
    def draw_side_panel():
        side_panel_buttons.clear()
        panel_x = container_x + GRID_WIDTH + 50
        panel_y = container_y
        visible_categories = ["Scenario", "player"]
        if options_data["Scenario"]["selected"] != "Open":
            visible_categories.append("opponent")
        offset_y = 0
        for cat in visible_categories:
            # Update options when Scenario or player change.
            if cat in ["Scenario", "player"]:
                update_visible_options(options_data)
            cat_rects = draw_radio_buttons(
                cat,
                panel_x,
                panel_y + offset_y,
                options_data[cat]["options"],
                options_data[cat]["selected"]
            )
            side_panel_buttons.append((cat, cat_rects))
            offset_y += 180
    
    # Back button setup.
    back_button_rect = pygame.Rect(20, 20, 80, 30)
    back_button_color = (180, 180, 180)
    back_button_text = font.render("HOME", True, BLACK)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    
    # ----------------------------------------------------------------
    # 5. Main Loop
    # ----------------------------------------------------------------
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    mainMenu()
                    running = False
                for category, rect_list in side_panel_buttons:
                    for (rect, opt) in rect_list:
                        if rect.collidepoint(mouse_x, mouse_y):
                            options_data[category]["selected"] = opt
                            # Update options when Scenario or player changes.
                            if category in ["Scenario", "player"]:
                                update_visible_options(options_data)
    
        # Draw background, overlay, and header.
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        SCREEN.blit(HAND_VISUALIZER_TEXT, header_rect)
        pygame.draw.rect(SCREEN, back_button_color, back_button_rect, border_radius=5)
        pygame.draw.rect(SCREEN, BLACK, back_button_rect, 1, border_radius=5)
        SCREEN.blit(back_button_text, back_button_text_rect)
    
        draw_side_panel()
    
        # Retrieve current selections.
        scenario_sel = options_data["Scenario"]["selected"]
        player_sel = options_data["player"]["selected"]
        if scenario_sel == "Open":
            # For Open, default opponent (since no villain selection is shown)
            opponent_sel = opponents[0]
        else:
            opponent_sel = options_data["opponent"]["selected"]
    
        strategy_key = (scenario_sel, player_sel, opponent_sel)
        if strategy_key in strat_data:
            raise_set = strat_data[strategy_key]["raise"]
            call_set = strat_data[strategy_key]["call"]
        else:
            raise_set = set()
            call_set = set()
    
        total_combos = 169
        raise_count = 0
        call_count = 0
    
        def get_hand_notation(r, c):
            ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
            if r == c:
                return ranks[r] + ranks[c]
            elif r < c:
                return ranks[r] + ranks[c] + "s"
            else:
                return ranks[c] + ranks[r] + "o"
    
        # Draw the 13x13 grid.
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                hand_str = get_hand_notation(row, col)
                if hand_str in raise_set:
                    color = RAISE_COLOR
                    raise_count += 1
                elif hand_str in call_set:
                    color = CALL_COLOR
                    call_count += 1
                else:
                    color = FOLD_COLOR
                x = container_x + col * (CELL_SIZE + MARGIN)
                y = container_y + row * (CELL_SIZE + MARGIN)
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, color, cell_rect)
                pygame.draw.rect(SCREEN, BLACK, cell_rect, 1)
                text_surf = font.render(hand_str, True, BLACK)
                text_rect = text_surf.get_rect(center=cell_rect.center)
                SCREEN.blit(text_surf, text_rect)
    
        raise_pct = 100.0 * raise_count / total_combos
        call_pct  = 100.0 * call_count / total_combos
        fold_pct  = 100.0 - (raise_pct + call_pct)
        stats_font = pygame.font.SysFont(None, 28)
        stats_text = stats_font.render(
            f"Raise ({raise_pct:.1f}%) | Call ({call_pct:.1f}%) | Fold ({fold_pct:.1f}%)",
            True, (255,255,255)
        )
        SCREEN.blit(stats_text, (container_x, container_y + GRID_HEIGHT + 15))
    
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)
    
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()
