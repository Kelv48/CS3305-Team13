import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor



def poker_hand_visualizer(mainMenu):
    pygame.init()

    #
    # 1. Strategy Data (Replace with your real solver outputs or strategy)
    #
    strat_data = {
        ("Open", "LJ", "BB"): {
            "raise": {
                "AA","KK","QQ","JJ","TT","99","88","77","66",
                "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs","T9s","98s"
            },
            "call": set()
        },
        ("Open", "HJ", "BB"): {
            "raise": {
                "AA","KK","QQ","JJ","TT","99","88","77","66",
                "AKs","AQs","AJs","ATs","KQs","KJs","QJs","JTs","T9s","98s"
            },
            "call": set()
        },
        ("vs 3bet", "LJ", "BB"): {
            "raise": {"AA","KK","QQ","AKs","AQs","AJs"},
            "call": {"JJ","TT","99","88","77","AQo","AJo","KQs","QJs","JTs"}
        },
        ("vs 3bet", "BTN", "SB"): {
            "raise": {"AA","KK","QQ","JJ","AKs","AQs","AJs","KQs","A5s"},
            "call": {"TT","99","88","77","AQo","AJo","KJs","QJs","JTs","T9s"}
        },
        ("vs 5bet", "SB", "BB"): {
            "raise": {"AA","KK","AKs","A5s"},
            "call": {"QQ","JJ"}
        },
    }

    #
    # 2. Equity Dictionary (for reference; not used in strategy lookup)
    #
    hand_equities = {
        # Pairs
        "AA": 85.2, "KK": 82.1, "QQ": 79.9, "JJ": 77.5, "TT": 75.2,
        "99": 71.9, "88": 68.5, "77": 65.2, "66": 61.7, "55": 58.3,
        "44": 54.9, "33": 51.3, "22": 47.9,
        # A-combos
        "AKs": 66.2, "AKo": 65.3,
        "AQs": 65.0, "AQo": 64.1,
        "AJs": 63.0, "AJo": 62.0,
        "ATs": 61.0, "ATo": 60.1,
        "A9s": 59.0, "A9o": 57.9,
        "A8s": 58.2, "A8o": 56.9,
        "A7s": 57.3, "A7o": 55.9,
        "A6s": 56.2, "A6o": 54.7,
        "A5s": 55.0, "A5o": 53.5,
        "A4s": 54.0, "A4o": 52.5,
        "A3s": 53.2, "A3o": 51.7,
        "A2s": 52.5, "A2o": 51.0,
        # K-combos
        "KQs": 59.0, "KQo": 57.5,
        "KJs": 57.9, "KJo": 56.4,
        "KTs": 56.8, "KTo": 55.2,
        "K9s": 55.3, "K9o": 53.8,
        "K8s": 54.2, "K8o": 52.6,
        "K7s": 53.1, "K7o": 51.4,
        "K6s": 52.0, "K6o": 50.3,
        "K5s": 51.0, "K5o": 49.3,
        "K4s": 50.2, "K4o": 48.5,
        "K3s": 49.6, "K3o": 47.8,
        "K2s": 48.9, "K2o": 47.0,
        # Q-combos
        "QJs": 56.2, "QJo": 54.7,
        "QTs": 55.1, "QTo": 53.5,
        "Q9s": 53.7, "Q9o": 52.1,
        "Q8s": 52.6, "Q8o": 50.9,
        "Q7s": 51.5, "Q7o": 49.8,
        "Q6s": 50.4, "Q6o": 48.6,
        "Q5s": 49.3, "Q5o": 47.4,
        "Q4s": 48.2, "Q4o": 46.3,
        "Q3s": 47.2, "Q3o": 45.3,
        "Q2s": 46.3, "Q2o": 44.4,
        # J-combos
        "JTs": 54.1, "JTo": 52.5,
        "J9s": 52.7, "J9o": 51.0,
        "J8s": 51.4, "J8o": 49.6,
        "J7s": 50.1, "J7o": 48.2,
        "J6s": 48.8, "J6o": 47.0,
        "J5s": 47.5, "J5o": 45.6,
        "J4s": 46.2, "J4o": 44.2,
        "J3s": 45.0, "J3o": 43.0,
        "J2s": 44.0, "J2o": 42.0,
        # T-combos
        "T9s": 51.6, "T9o": 50.0,
        "T8s": 50.3, "T8o": 48.6,
        "T7s": 49.0, "T7o": 47.2,
        "T6s": 47.7, "T6o": 45.8,
        "T5s": 46.3, "T5o": 44.4,
        "T4s": 45.0, "T4o": 43.1,
        "T3s": 43.7, "T3o": 41.7,
        "T2s": 42.4, "T2o": 40.4,
        # 9-combos
        "98s": 49.0, "98o": 47.1,
        "97s": 47.6, "97o": 45.6,
        "96s": 46.2, "96o": 44.2,
        "95s": 44.8, "95o": 42.8,
        "94s": 43.4, "94o": 41.3,
        "93s": 42.0, "93o": 40.0,
        "92s": 40.7, "92o": 38.6,
        # 8-combos
        "87s": 46.3, "87o": 44.3,
        "86s": 44.8, "86o": 42.7,
        "85s": 43.4, "85o": 41.2,
        "84s": 42.0, "84o": 39.8,
        "83s": 40.7, "83o": 38.4,
        "82s": 39.4, "82o": 37.1,
        # 7-combos
        "76s": 43.8, "76o": 41.5,
        "75s": 42.4, "75o": 40.1,
        "74s": 41.0, "74o": 38.7,
        "73s": 39.7, "73o": 37.3,
        "72s": 38.3, "72o": 35.9,
        # 6-combos
        "65s": 41.3, "65o": 38.9,
        "64s": 39.9, "64o": 37.5,
        "63s": 38.5, "63o": 36.1,
        "62s": 37.2, "62o": 34.7,
        # 5-combos
        "54s": 39.0, "54o": 36.5,
        "53s": 37.6, "53o": 35.1,
        "52s": 36.3, "52o": 33.7,
        # 4-combos
        "43s": 35.0, "43o": 32.4,
        "42s": 33.7, "42o": 31.0,
        # 3-combos
        "32s": 32.4, "32o": 29.6
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

    header_text = "This is the HAND VISUALIZER screen."
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
                mx, my = event.pos

                # Check if the back button was clicked.
                if back_button_rect.collidepoint(mx, my):
                    mainMenu()
                    running = False
                    

                # Check clicks on visible side-panel buttons.
                for category, rect_list in side_panel_buttons:
                    for (rect, opt) in rect_list:
                        if rect.collidepoint(mx, my):
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

if __name__ == "__main__":
    poker_hand_visualizer()
