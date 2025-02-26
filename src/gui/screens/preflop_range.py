import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor



def preflop_range_visualizer(mainMenu):
    pygame.init()

    
# Example of a “full” 6-max strategy data structure in Python.
# Replace these sets with your real solver outputs or personal strategy.
#

    # 6-max preflop strategy ranges based on recent online GTO solver outputs.
# These ranges are approximate and meant for educational purposes.
# Adjust them as needed for your specific game and solver outputs.

    # Define the available radio button options.
    scenarios = ["Open", "vs raise", "vs 3bet", "vs 4bet", "vs 5bet"]
    players    = ["LJ", "HJ", "CO", "BTN", "SB"]
    opponents  = ["HJ", "CO", "BTN", "SB", "BB"]

    strat_data = {}

    # 1) For the "Open" scenario, use your original ranges per player.
    open_ranges = {
        "LJ": {
            "raise": {
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                "QJs", "QTs", "Q9s",
                "JTs",

                "AKo", "AQo", "AJo", "ATo", 
                "KQo", "KJo",
                "QJo"
            },
            "call": set()
        },
        "HJ": {
            "raise": {
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s",
                "QJs", "QTs", "Q9s", "Q8s",
                "JTs",

                "AKo", "AQo", "AJo", "ATo", "A9o",
                "KQo", "KJo", "KTo",
                "QJo", "QTo"
            },
            "call": set()
        },
        "CO": {
            "raise": {
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s",
                "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s",
                "JTs", "J9s", "J8s", "J7s",
                "T9s", "T8s", 
                "98s", 

                "AKo", "AQo", "AJo", "ATo", "A9o", "A8o",
                "KQo", "KJo", "KTo", "K9o",
                "QJo", "QTo",
                "JTo"
            },
            "call": set()
        },
        "BTN": {
            "raise": {
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
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
                "T9o",
            },
            "call": set()
        },
        "SB": {
            "raise": {
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
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
                "T9o",
            },
            "call": set()
        }
    }

    # For "Open", the opponent position typically doesn't affect your range,
    # so assign the same open_ranges for every opponent.
    for player in players:
        for opponent in opponents:
            strat_data[("Open", player, opponent)] = open_ranges[player]



   # Template for "vs raise"
    vs_raise_data = {
        "LJ": {
            "raise": {
                "AA", "KK", "QQ", "JJ",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A5s", "A4s",
                "KQs", "KJs", "KTs",
                "QJs",

                "AKo", "AQo",
                "KQo", "KJo"
                },
            "call":  {"<LJ_vs_raise_call_hand1>", "<LJ_vs_raise_call_hand2>", "..."}
        },
        "HJ": {
            "raise": {"<HJ_vs_raise_raise_hand1>", "<Hj_vs_raise_raise_hand2>", "..."},
            "call":  {"<HJ_vs_raise_call_hand1>", "<HJ_vs_raise_call_hand2>", "..."}
        },
        "CO": {
            "raise": {"<CO_vs_raise_raise_hand1>", "<CO_vs_raise_raise_hand2>", "..."},
            "call":  {"<CO_vs_raise_call_hand1>", "<CO_vs_raise_call_hand2>", "..."}
        },
        "BTN": {
            "raise": {"<BTN_vs_raise_raise_hand1>", "<BTN_vs_raise_raise_hand2>", "..."},
            "call":  {"<BTN_vs_raise_call_hand1>", "<BTN_vs_raise_call_hand2>", "..."}
        },
        "SB": {
            "raise": {"<SB_vs_raise_raise_hand1>", "<SB_vs_raise_raise_hand2>", "..."},
            "call":  {"<SB_vs_raise_call_hand1>", "<SB_vs_raise_call_hand2>", "..."}
        }
    }

    # Template for "vs 3bet"
    vs_3bet_data = {
        "LJ": {
            "raise": {"<LJ_vs_3bet_raise_hand1>", "<LJ_vs_3bet_raise_hand2>", "..."},
            "call":  {"<LJ_vs_3bet_call_hand1>", "<LJ_vs_3bet_call_hand2>", "..."}
        },
        "HJ": {
            "raise": {"<HJ_vs_3bet_raise_hand1>", "<HJ_vs_3bet_raise_hand2>", "..."},
            "call":  {"<HJ_vs_3bet_call_hand1>", "<HJ_vs_3bet_call_hand2>", "..."}
        },
        "CO": {
            "raise": {"<CO_vs_3bet_raise_hand1>", "<CO_vs_3bet_raise_hand2>", "..."},
            "call":  {"<CO_vs_3bet_call_hand1>", "<CO_vs_3bet_call_hand2>", "..."}
        },
        "BTN": {
            "raise": {"<BTN_vs_3bet_raise_hand1>", "<BTN_vs_3bet_raise_hand2>", "..."},
            "call":  {"<BTN_vs_3bet_call_hand1>", "<BTN_vs_3bet_call_hand2>", "..."}
        },
        "SB": {
            "raise": {"<SB_vs_3bet_raise_hand1>", "<SB_vs_3bet_raise_hand2>", "..."},
            "call":  {"<SB_vs_3bet_call_hand1>", "<SB_vs_3bet_call_hand2>", "..."}
        }
    }

    # Template for "vs 4bet"
    vs_4bet_data = {
        "LJ": {
            "raise": {"<LJ_vs_4bet_raise_hand1>", "<LJ_vs_4bet_raise_hand2>", "..."},
            "call":  {"<LJ_vs_4bet_call_hand1>", "<LJ_vs_4bet_call_hand2>", "..."}
        },
        "HJ": {
            "raise": {"<HJ_vs_4bet_raise_hand1>", "<HJ_vs_4bet_raise_hand2>", "..."},
            "call":  {"<HJ_vs_4bet_call_hand1>", "<HJ_vs_4bet_call_hand2>", "..."}
        },
        "CO": {
            "raise": {"<CO_vs_4bet_raise_hand1>", "<CO_vs_4bet_raise_hand2>", "..."},
            "call":  {"<CO_vs_4bet_call_hand1>", "<CO_vs_4bet_call_hand2>", "..."}
        },
        "BTN": {
            "raise": {"<BTN_vs_4bet_raise_hand1>", "<BTN_vs_4bet_raise_hand2>", "..."},
            "call":  {"<BTN_vs_4bet_call_hand1>", "<BTN_vs_4bet_call_hand2>", "..."}
        },
        "SB": {
            "raise": {"<SB_vs_4bet_raise_hand1>", "<SB_vs_4bet_raise_hand2>", "..."},
            "call":  {"<SB_vs_4bet_call_hand1>", "<SB_vs_4bet_call_hand2>", "..."}
        }
    }

    # Template for "vs 5bet"
    vs_5bet_data = {
        "LJ": {
            "raise": {"<LJ_vs_5bet_raise_hand1>", "<LJ_vs_5bet_raise_hand2>", "..."},
            "call":  {"<LJ_vs_5bet_call_hand1>", "<LJ_vs_5bet_call_hand2>", "..."}
        },
        "HJ": {
            "raise": {"<HJ_vs_5bet_raise_hand1>", "<HJ_vs_5bet_raise_hand2>", "..."},
            "call":  {"<HJ_vs_5bet_call_hand1>", "<HJ_vs_5bet_call_hand2>", "..."}
        },
        "CO": {
            "raise": {"<CO_vs_5bet_raise_hand1>", "<CO_vs_5bet_raise_hand2>", "..."},
            "call":  {"<CO_vs_5bet_call_hand1>", "<CO_vs_5bet_call_hand2>", "..."}
        },
        "BTN": {
            "raise": {"<BTN_vs_5bet_raise_hand1>", "<BTN_vs_5bet_raise_hand2>", "..."},
            "call":  {"<BTN_vs_5bet_call_hand1>", "<BTN_vs_5bet_call_hand2>", "..."}
        },
        "SB": {
            "raise": {"<SB_vs_5bet_raise_hand1>", "<SB_vs_5bet_raise_hand2>", "..."},
            "call":  {"<SB_vs_5bet_call_hand1>", "<SB_vs_5bet_call_hand2>", "..."}
        }
    }

    # -------------------------------------
    # 3) Assign the custom ranges to strat_data for every player and opponent.
    # -------------------------------------
    for scenario, data in [
        ("vs raise", vs_raise_data),
        ("vs 3bet", vs_3bet_data),
        ("vs 4bet", vs_4bet_data),
        ("vs 5bet", vs_5bet_data)
    ]:
        for player in players:
            for opponent in opponents:
                strat_data[(scenario, player, opponent)] = data[player]

    # Now strat_data contains an entry for every combination:
    #  - "Open" (using open_ranges) for all player/opponent pairs.
    #  - "vs raise", "vs 3bet", "vs 4bet", and "vs 5bet" with your custom data for each player.

        #
    # 3. Window Setup and Overlay
    #
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    textbox_width = int(screen_width * 0.95)
    textbox_height = int(screen_height * 0.85)
    textbox_x = (screen_width - textbox_width) // 2
    textbox_y = (screen_height - textbox_height) // 2
    textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
    pygame.draw.rect(textbox_surface, (0, 0, 0, 100), (0, 0, textbox_width, textbox_height), border_radius=50)
    SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

    header_text = "This is the PREFLOP RANGE screen."
    HAND_VISUALIZER_TEXT = screen_font(45).render(header_text, True, "Gold")
    header_y = textbox_y - 20
    HAND_VISUALIZER_RECT = HAND_VISUALIZER_TEXT.get_rect(center=(textbox_x + textbox_width // 2, header_y))
    SCREEN.blit(HAND_VISUALIZER_TEXT, HAND_VISUALIZER_RECT)

    #
    # 4. Grid Layout
    #
    GRID_SIZE = 13
    CELL_SIZE = 43
    MARGIN = 0
    GRID_WIDTH = MARGIN + (CELL_SIZE + MARGIN) * GRID_SIZE
    GRID_HEIGHT = MARGIN + (CELL_SIZE + MARGIN) * GRID_SIZE

    container_x = 60
    container_y = 70

    # Updated colors
    RAISE_COLOR = (255, 0, 0)      # bright red
    CALL_COLOR  = (0, 200, 0)      # green
    FOLD_COLOR  = (100, 100, 100)  # dark grey
    BLACK       = (0, 0, 0)

    font = screen_font(20)

    #
    # 5. Radio Buttons for Side Panel (Scenario, player, opponent)
    #
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

    side_panel_buttons = []

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

    def draw_side_panel():
        side_panel_buttons.clear()
        panel_x = container_x + GRID_WIDTH + 50
        panel_y = container_y
        visible_categories = ["Scenario", "player", "opponent"]
        if options_data["Scenario"]["selected"] == "Open":
            visible_categories.remove("opponent")
        offset_y = 0
        for cat in visible_categories:
            cat_rects = draw_radio_buttons(
                cat, panel_x, panel_y + offset_y,
                options_data[cat]["options"],
                options_data[cat]["selected"]
            )
            side_panel_buttons.append((cat, cat_rects))
            offset_y += 180

    #
    # 6. Back Button Setup
    #
    # Define a back button rectangle (e.g., top-left corner)
    back_button_rect = pygame.Rect(20, 20, 80, 30)
    back_button_color = (180, 180, 180)
    back_button_text = font.render("HOME", True, BLACK)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)

    #
    # 7. Main Loop
    #
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if the back button was clicked.
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    mainMenu()
                    running = False
                    

                # Check clicks on visible side-panel buttons.
                for category, rect_list in side_panel_buttons:
                    for (rect, opt) in rect_list:
                        if rect.collidepoint(mouse_x, mouse_y):
                            options_data[category]["selected"] = opt

        # Redraw background and overlay.
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        SCREEN.blit(HAND_VISUALIZER_TEXT, HAND_VISUALIZER_RECT)

        # Draw the back button.
        pygame.draw.rect(SCREEN, back_button_color, back_button_rect, border_radius=5)
        pygame.draw.rect(SCREEN, BLACK, back_button_rect, 1, border_radius=5)
        SCREEN.blit(back_button_text, back_button_text_rect)

        # Draw side panel based on current selections.
        draw_side_panel()

        # Retrieve current selections.
        scenario_sel = options_data["Scenario"]["selected"]
        player_sel     = options_data["player"]["selected"]
        opponent_sel  = options_data["opponent"]["selected"] if "opponent" in [cat for (cat, _) in side_panel_buttons] else "BB"

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
            ranks = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]
            if r == c:
                return ranks[r] + ranks[c]
            elif r < c:
                return ranks[r] + ranks[c] + "s"
            else:
                return ranks[c] + ranks[r] + "o"

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
                text_surface = font.render(hand_str, True, BLACK)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                SCREEN.blit(text_surface, text_rect)

        raise_pct = 100.0 * raise_count / total_combos
        call_pct  = 100.0 * call_count / total_combos
        fold_pct  = 100.0 - (raise_pct + call_pct)
        stats_font = pygame.font.SysFont(None, 28)
        stats_text = stats_font.render(
            f"Raise ({raise_pct:.1f}%) | Call ({call_pct:.1f}%) | Fold ({fold_pct:.1f}%)",
            True, (255,255,255)
        )
        SCREEN.blit(stats_text, (container_x, container_y + GRID_HEIGHT + 15))

        # *** Draw the custom cursor last so it’s always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)

        pygame.display.flip()
        clock.tick(30)


    pygame.quit()
    sys.exit()

