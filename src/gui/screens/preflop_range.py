import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor



def preflop_range_visualizer(mainMenu):
    pygame.init()

    #
# Example of a “full” 6-max strategy data structure in Python.
# Replace these sets with your real solver outputs or personal strategy.
#

    strat_data = {
        # ------------------
        # 1) OPEN RANGES
        # ------------------
        #
        # Open from UTG vs BB
        ("Open", "UTG", "BB"): {
            "raise": {
                # Pairs
                "AA","KK","QQ","JJ","TT","99","88","77",
                # Suited Broadways
                "AKs","AQs","AJs","KQs",
                # Offsuit Broadways
                "AKo","AQo",
                # Suited Connectors / Others
                "A5s","A4s","KJs","QJs","JTs","T9s","98s","87s"
            },
            "call": set()  # Usually no limp/call range preflop when open-raising
        },

        # Open from LJ vs BB
        ("Open", "LJ", "BB"): {
            "raise": {
                # Slightly wider than UTG
                "AA","KK","QQ","JJ","TT","99","88","77","66","55",
                "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs","T9s","98s",
                "AKo","AQo","KQo","A5s","A4s"
            },
            "call": set()
        },

        # Open from HJ vs BB
        ("Open", "HJ", "BB"): {
            "raise": {
                # Wider still than LJ
                "AA","KK","QQ","JJ","TT","99","88","77","66","55","44",
                "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs","T9s","98s","87s",
                "AKo","AQo","AJo","KQo","KJo","A5s","A4s","A3s"
            },
            "call": set()
        },

        # Open from CO vs BB
        ("Open", "CO", "BB"): {
            "raise": {
                "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33",
                "AKs","AQs","AJs","ATs","A9s","KQs","KJs","QJs","JTs","T9s","98s",
                "87s","76s","A5s","A4s","A3s","A2s",
                "AKo","AQo","AJo","KQo","KJo","QJo","JTo"
            },
            "call": set()
        },

        # Open from BTN vs BB
        ("Open", "BTN", "BB"): {
            "raise": {
                # Very wide; typical BTN opening range
                "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
                "AKs","AQs","AJs","ATs","A9s","A8s","A5s","A4s","A3s","A2s",
                "KQs","KJs","KTs","K9s",
                "QJs","QTs","Q9s","JTs","J9s","T9s","98s","87s","76s","65s",
                "AKo","AQo","AJo","KQo","KJo","QJo","JTo","T9o","98o"
            },
            "call": set()
        },

        # Open from SB vs BB
        ("Open", "SB", "BB"): {
            "raise": {
                # The SB open-raise range can be very wide in modern strategy
                "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
                "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
                "KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s",
                "QJs","QTs","Q9s","Q8s","Q7s","JTs","J9s","J8s","T9s","T8s","98s","87s",
                "76s","65s","54s",
                "AKo","AQo","AJo","KQo","KJo","KTo","QJo","QTo","JTo","T9o","98o","87o"
            },
            "call": set()
        },

        # ------------------------------------------------
        # 2) VS 3BET (Facing a 3bet after we open-raised)
        # ------------------------------------------------
        #
        # UTG vs 3bet from BB
        ("vs 3bet", "UTG", "BB"): {
            "raise": {
                # Typical 4-bet (value + a few semi-bluffs)
                "AA","KK","QQ","AKs","A5s"
            },
            "call": {
                # Hands that continue by calling
                "JJ","TT","99","AQs","AJs","KQs","AKo","AQo"
            }
        },

        # LJ vs 3bet from BB
        ("vs 3bet", "LJ", "BB"): {
            "raise": {
                # This matches your snippet example but you can adjust
                "AA","KK","QQ","AKs","AQs","AJs"
            },
            "call": {
                "JJ","TT","99","88","77","AQo","AJo","KQs","QJs","JTs"
            }
        },

        # HJ vs 3bet from BB
        ("vs 3bet", "HJ", "BB"): {
            "raise": {
                "AA","KK","QQ","AKs","AQs","A5s","A4s"
            },
            "call": {
                "JJ","TT","99","88","77","AQo","AJo","AJs","KQs","QJs","JTs","T9s"
            }
        },

        # CO vs 3bet from BB
        ("vs 3bet", "CO", "BB"): {
            "raise": {
                "AA","KK","QQ","JJ","AKs","AQs","A5s"
            },
            "call": {
                "TT","99","88","77","AQo","AJo","AJs","KQs","KJs","QJs","JTs","T9s","98s"
            }
        },

        # BTN vs 3bet from SB (from your snippet)
        ("vs 3bet", "BTN", "SB"): {
            "raise": {
                "AA","KK","QQ","JJ","AKs","AQs","AJs","KQs","A5s"
            },
            "call": {
                "TT","99","88","77","AQo","AJo","KJs","QJs","JTs","T9s"
            }
        },

        # (Example) BTN vs 3bet from BB
        ("vs 3bet", "BTN", "BB"): {
            "raise": {
                "AA","KK","QQ","JJ","AKs","A5s","AQs"
            },
            "call": {
                "TT","99","88","77","AQo","AJo","AJs","KQs","KJs","QJs",
                "JTs","T9s","98s","87s"
            }
        },

        # ------------------------------------------------
        # 3) VS 5BET (Facing a 5bet after we 4-bet)
        # ------------------------------------------------
        #
        # SB vs 5bet from BB (from your snippet)
        ("vs 5bet", "SB", "BB"): {
            "raise": {"AA","KK","AKs","A5s"},
            "call":  {"QQ","JJ"} 
        },

        # (Example) BTN vs 5bet from BB
        ("vs 5bet", "BTN", "BB"): {
            "raise": {"AA","KK","AKs","A5s"},   # Shove (or 6-bet)
            "call":  {"QQ","JJ","AKo","AQs"}    # Might flat or go with it depending on stack sizes
        }
    }



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
    HAND_VISUALIZER_TEXT = screen_font(45).render(header_text, True, "White")
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
    # 5. Radio Buttons for Side Panel (Scenario, Hero, Villain)
    #
    options_data = {
        "Scenario": {
            "options": ["Open", "vs raise", "vs 3bet", "vs 4bet", "vs 5bet"],
            "selected": "Open"
        },
        "Hero": {
            "options": ["LJ", "HJ", "CO", "BTN", "SB"],
            "selected": "LJ"
        },
        "Villain": {
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
        visible_categories = ["Scenario", "Hero", "Villain"]
        if options_data["Scenario"]["selected"] == "Open":
            visible_categories.remove("Villain")
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
        hero_sel     = options_data["Hero"]["selected"]
        villain_sel  = options_data["Villain"]["selected"] if "Villain" in [cat for (cat, _) in side_panel_buttons] else "BB"

        strategy_key = (scenario_sel, hero_sel, villain_sel)
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

