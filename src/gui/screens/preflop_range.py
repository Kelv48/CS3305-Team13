import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor, FPS
from src.gui.screens.ranges_data import template_data, open_ranges

# Helper Functions for Valid Positions
def get_valid_hero_positions(scenario):
    if scenario == "Open":
        return ["LJ", "HJ", "CO", "BTN", "SB"]
    elif scenario in ["vs raise", "vs 4bet"]:
        return ["HJ", "CO", "BTN", "SB", "BB"]
    elif scenario in ["vs 3bet", "vs 5bet"]:
        return ["LJ", "HJ", "CO", "BTN", "SB"]
    else:
        return []

def get_valid_villain_positions(scenario, hero):
    seating_order = ["LJ", "HJ", "CO", "BTN", "SB", "BB"]
    if scenario == "Open":
        return []
    if scenario in ["vs raise", "vs 4bet"]:
        hero_index = seating_order.index(hero)
        return seating_order[:hero_index]
    elif scenario in ["vs 3bet", "vs 5bet"]:
        hero_index = seating_order.index(hero)
        return seating_order[hero_index+1:]
    else:
        return []

# Functions to Update and Determine Visible Options
def update_visible_options(options_data):
    scenario_sel = options_data["Scenario"]["selected"]
    valid_heroes = get_valid_hero_positions(scenario_sel)
    hero_sel = options_data["player"]["selected"]
    if hero_sel not in valid_heroes:
        hero_sel = valid_heroes[0] if valid_heroes else None
    options_data["player"]["options"] = valid_heroes
    options_data["player"]["selected"] = hero_sel

    valid_villains = []
    if hero_sel:
        valid_villains = get_valid_villain_positions(scenario_sel, hero_sel)
    opp_sel = options_data["opponent"]["selected"]
    if opp_sel not in valid_villains and valid_villains:
        opp_sel = valid_villains[0]
    options_data["opponent"]["options"] = valid_villains
    options_data["opponent"]["selected"] = opp_sel

def get_visible_categories(options_data):
    visible = ["Scenario", "player"]
    if options_data["opponent"]["options"]:
        visible.append("opponent")
    return visible

# Preflop Range Visualizer Code
def preflop_range_visualizer(mainMenu):
    clock = pygame.time.Clock()
    clock.tick(FPS)
    
    # Window and Asset Setup
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    
    # Create an overlay textbox.
    textbox_width = int(screen_width * 0.95)
    textbox_height = int(screen_height * 0.85)
    textbox_x = (screen_width - textbox_width) // 2
    textbox_y = (screen_height - textbox_height) // 2
    textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
    pygame.draw.rect(textbox_surface, (0, 0, 0, 150), (0, 0, textbox_width, textbox_height), border_radius=50)
    
    # Header text.
    header_text = "PREFLOP RANGE"
    HAND_VISUALIZER_TEXT = screen_font(45).render(header_text, True, "Gold")
    header_rect = HAND_VISUALIZER_TEXT.get_rect(center=(textbox_x + textbox_width // 2, textbox_y - 20))
    
    # Grid Layout Settings
    GRID_SIZE = 13
    CELL_SIZE = 43
    MARGIN = 0
    GRID_WIDTH = (CELL_SIZE + MARGIN) * GRID_SIZE
    GRID_HEIGHT = (CELL_SIZE + MARGIN) * GRID_SIZE
    container_x = 60
    container_y = 70
    
    # Colors and font.
    RAISE_COLOR = (255, 0, 0)
    CALL_COLOR  = (0, 200, 0)
    FOLD_COLOR  = (100, 100, 100)
    BLACK       = (0, 0, 0)
    font = screen_font(20)
    
    # Build the complete strategy data dictionary.
    strat_data = {}
    open_opponents = ["HJ", "CO", "BTN", "SB", "BB"]
    for player in open_ranges:
        for opponent in open_opponents:
            strat_data[("Open", player, opponent)] = open_ranges[player]
    strat_data.update(template_data)
    
    # Side Panel Setup
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
            "options": [],
            "selected": ""
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
    
    # Main Loop
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
                            if category in ["Scenario", "player"]:
                                update_visible_options(options_data)
    
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        SCREEN.blit(HAND_VISUALIZER_TEXT, header_rect)
        pygame.draw.rect(SCREEN, back_button_color, back_button_rect, border_radius=5)
        pygame.draw.rect(SCREEN, BLACK, back_button_rect, 1, border_radius=5)
        SCREEN.blit(back_button_text, back_button_text_rect)
    
        draw_side_panel()
    
        scenario_sel = options_data["Scenario"]["selected"]
        player_sel = options_data["player"]["selected"]
        if scenario_sel == "Open":
            opponent_sel = open_opponents[0]
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
            True, (255, 255, 255)
        )
        SCREEN.blit(stats_text, (container_x, container_y + GRID_HEIGHT + 15))
    
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)
    
        pygame.display.flip()

    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Dummy mainMenu for testing purposes
    def mainMenu():
        print("Returning to main menu...")
    preflop_range_visualizer(mainMenu)
