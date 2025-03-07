import sys
import pygame
from src.gui.utils.constants import SCREEN, BG, screen_font, scaled_cursor, FPS, WHITE
from src.gui.utils.button import Button

def hand_equity_visualizer(mainMenu):
    pygame.init()
    clock = pygame.time.Clock()
    clock.tick(FPS)

    #
    # 1. Complete Equity Dictionary (all 169 combos).
    #
    hand_equities = {
    # Pairs
    "AA": 85.0, "KK": 82.0, "QQ": 80.0, 
    "JJ": 77.0, "TT": 75.0, "99": 72.0, 
    "88": 69.0, "77": 66.0, "66": 63.0, 
    "55": 60.0, "44": 57.0, "33": 54.0, "22": 50.0,

    # A-combos
    "AKs": 67.2, "AKo": 65.3,
    "AQs": 66.0, "AQo": 64.1,
    "AJs": 64.0, "AJo": 62.0,
    "ATs": 62.0, "ATo": 60.1,
    "A9s": 60.0, "A9o": 57.9,
    "A8s": 59.2, "A8o": 56.9,
    "A7s": 58.3, "A7o": 55.9,
    "A6s": 57.2, "A6o": 54.7,
    "A5s": 56.0, "A5o": 53.5,
    "A4s": 55.0, "A4o": 52.5,
    "A3s": 54.2, "A3o": 51.7,
    "A2s": 53.5, "A2o": 51.0,

    # K-combos
    "KQs": 60.0, "KQo": 57.5,
    "KJs": 58.9, "KJo": 56.4,
    "KTs": 57.8, "KTo": 55.2,
    "K9s": 56.3, "K9o": 53.8,
    "K8s": 55.2, "K8o": 52.6,
    "K7s": 54.1, "K7o": 51.4,
    "K6s": 53.0, "K6o": 50.3,
    "K5s": 52.0, "K5o": 49.3,
    "K4s": 51.2, "K4o": 48.5,
    "K3s": 50.6, "K3o": 47.8,
    "K2s": 49.9, "K2o": 47.0,

    # Q-combos
    "QJs": 57.2, "QJo": 54.7,
    "QTs": 56.1, "QTo": 53.5,
    "Q9s": 54.7, "Q9o": 52.1,
    "Q8s": 53.6, "Q8o": 50.9,
    "Q7s": 52.5, "Q7o": 49.8,
    "Q6s": 51.4, "Q6o": 48.6,
    "Q5s": 50.3, "Q5o": 47.4,
    "Q4s": 49.2, "Q4o": 46.3,
    "Q3s": 48.2, "Q3o": 45.3,
    "Q2s": 47.3, "Q2o": 44.4,

    # J-combos
    "JTs": 55.1, "JTo": 52.5,
    "J9s": 53.7, "J9o": 51.0,
    "J8s": 52.4, "J8o": 49.6,
    "J7s": 51.1, "J7o": 48.2,
    "J6s": 49.8, "J6o": 47.0,
    "J5s": 48.5, "J5o": 45.6,
    "J4s": 47.2, "J4o": 44.2,
    "J3s": 46.0, "J3o": 43.0,
    "J2s": 45.0, "J2o": 42.0,

    # T-combos
    "T9s": 52.6, "T9o": 50.0,
    "T8s": 51.3, "T8o": 48.6,
    "T7s": 50.0, "T7o": 47.2,
    "T6s": 48.7, "T6o": 45.8,
    "T5s": 47.3, "T5o": 44.4,
    "T4s": 46.0, "T4o": 43.1,
    "T3s": 44.7, "T3o": 41.7,
    "T2s": 43.4, "T2o": 40.4,

    # 9-combos
    "98s": 50.0, "98o": 47.1,
    "97s": 48.6, "97o": 45.6,
    "96s": 47.2, "96o": 44.2,
    "95s": 45.8, "95o": 42.8,
    "94s": 44.4, "94o": 41.3,
    "93s": 43.0, "93o": 40.0,
    "92s": 41.7, "92o": 38.6,

    # 8-combos
    "87s": 47.3, "87o": 44.3,
    "86s": 45.8, "86o": 42.7,
    "85s": 44.4, "85o": 41.2,
    "84s": 43.0, "84o": 39.8,
    "83s": 41.7, "83o": 38.4,
    "82s": 40.4, "82o": 37.1,

    # 7-combos
    "76s": 44.8, "76o": 41.5,
    "75s": 43.4, "75o": 40.1,
    "74s": 42.0, "74o": 38.7,
    "73s": 40.7, "73o": 37.3,
    "72s": 39.3, "72o": 35.9,

    # 6-combos
    "65s": 42.3, "65o": 38.9,
    "64s": 40.9, "64o": 37.5,
    "63s": 39.5, "63o": 36.1,
    "62s": 38.2, "62o": 34.7,

    # 5-combos
    "54s": 40.0, "54o": 36.5,
    "53s": 38.6, "53o": 35.1,
    "52s": 37.3, "52o": 33.7,

    # 4-combos
    "43s": 36.0, "43o": 32.4,
    "42s": 34.7, "42o": 31.0,

    # 3-combos
    "32s": 33.4, "32o": 29.6
}



    # Grab screen dimensions and draw background
    screen_width, screen_height = SCREEN.get_size()
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))

    # Create a centered textbox background (90% width, 80% height)
    textbox_width = int(screen_width * 0.95)
    textbox_height = int(screen_height * 0.85)
    textbox_x = (screen_width - textbox_width) // 2
    textbox_y = (screen_height - textbox_height) // 2
    textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
    pygame.draw.rect(
        textbox_surface,
        (0, 0, 0, 180),  # black semi-transparent background
        (0, 0, textbox_width, textbox_height),
        border_radius=50
    )
    SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

    # Place header text near the top of the textbox
    header_text = "HAND EQUITY"
    HAND_VISUALIZER_TEXT = screen_font(45).render(header_text, True, "Gold")
    header_y = textbox_y - 20
    HAND_VISUALIZER_RECT = HAND_VISUALIZER_TEXT.get_rect(center=(textbox_x + textbox_width // 2, header_y))
    SCREEN.blit(HAND_VISUALIZER_TEXT, HAND_VISUALIZER_RECT)




    #
    # 2. Grid/Slider Parameters
    #
    GRID_SIZE = 13
    CELL_SIZE = 43
    MARGIN = 0
    GRID_WIDTH = MARGIN + (CELL_SIZE + MARGIN) * GRID_SIZE
    GRID_HEIGHT = MARGIN + (CELL_SIZE + MARGIN) * GRID_SIZE
    SLIDER_AREA_HEIGHT = 70

    

    # colours
    BLACK = (0, 0, 0)
    GREEN = (50, 164, 49)
    LIGHT_GREY = (220, 220, 220)
    VERY_LIGHT_GREY = (240, 240, 240)
    PAIR_GREY = (200, 200, 200)
    SLIDER_TRACK_COLOUR = (180, 180, 180)
    SLIDER_KNOB_COLOUR = (255, 0, 0)

    # Ranks (index 0 = A, 1 = K, ..., 12 = 2)
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    font = pygame.font.SysFont(None, 24)
    home_font = pygame.font.SysFont(None, 34)
    slider_font = pygame.font.SysFont(None, 34)

    # Data structure to hold which cells are selected
    selected = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # We'll start the slider at 100% (select everything)
    slider_value = 0
    slider_dragging = False

    # Container for the grid + slider
    container_width = GRID_WIDTH
    container_height = GRID_HEIGHT + SLIDER_AREA_HEIGHT
    container_x = 70
    container_y = 80

    # Slider geometry
    slider_x = 700
    slider_y = 600
    slider_width = 200 - 2 * MARGIN
    slider_height = SLIDER_AREA_HEIGHT - 2 * MARGIN
    track_height = 4
    knob_radius = 10

    #
    # Add Text Input Box for Percentage Entry
    #
    input_box_rect = pygame.Rect(slider_x + slider_width + 20, slider_y, 100, 30)
    input_text = str(round(slider_value)) + "%"
    input_active = False

    # Define colours for the text box (inactive/active)
    TEXT_BOX_colour = (255, 255, 255)
    TEXT_BOX_ACTIVE_colour = (200, 200, 200)

    #
    # 3. Helper Functions
    #
    def get_hand_notation(row, col):
        """Return e.g. 'QQ', 'AKs', 'AKo' based on row/col indices."""
        if row == col:
            return ranks[row] + ranks[col]         # e.g. "QQ"
        elif row < col:
            return ranks[row] + ranks[col] + "s"     # e.g. "AQs"
        else:
            return ranks[col] + ranks[row] + "o"     # e.g. "AQo"

    def hand_strength_score(row, col):
        """Look up the hand's equity in the dictionary."""
        notation = get_hand_notation(row, col)
        return hand_equities.get(notation, 0.0)

    # Build a list of all 169 combos with their scores
    ordered_cells = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            score = hand_strength_score(row, col)
            ordered_cells.append((score, row, col))
    # Sort descending by score
    ordered_cells.sort(key=lambda x: x[0], reverse=True)

    def update_range_from_slider():
        """Select the top X% of combos based on slider_value."""
        nonlocal selected
        total = len(ordered_cells)  # should be 169
        count = round((slider_value / 100.0) * total)
        selected = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(count):
            _, r, c = ordered_cells[i]
            selected[r][c] = True

    # Initialize selection at 100%
    update_range_from_slider()

    # Create a transparent black background surface for the back button
    button_bg_width = 100
    button_bg_height = 40
    button_bg = pygame.Surface((button_bg_width, button_bg_height), pygame.SRCALPHA)
    pygame.draw.rect(
        button_bg,
        (0, 0, 0, 180),  # black with 180 alpha (semi-transparent)
        (0, 0, button_bg_width, button_bg_height),
        border_radius=10
    )

    # Define a back button using the Button class
    back_button = Button(
        pos=(60, 35),
        text_input="HOME",
        font=home_font,
        base_colour="White",
        hovering_colour="Gold",
        image=button_bg
    )

    # Define explanatory text
    explanation_font = pygame.font.SysFont(None, 28)
    explanations = [
        "How to Read the Grid:",
        "• Each cell represents your two starting cards",
        "• 's' means suited (same suit)",
        "• 'o' means offsuit (different suits)",
        "• Pairs are when both cards are the same",
        "Examples:",
        "• AKs = Ace-King suited",
        "• JTo = Jack-Ten offsuit",
        "• QQ = Queen-Queen pair",
        "",
        # "Understanding Equity:",
        # "• Numbers show winning chances vs random hands",
        # "• Higher % = stronger starting hand",
        # "• Pairs (AA=85%) are strongest",
        # "• Suited hands are stronger than offsuit",
        # "• Connected cards (next to each other) are strong",
        # "",
        "Using Hand Ranges:",
        "• The slider selects hands by strength",
        "• 20% = top 20% strongest hands",
        "• Selected hands shown in green",
        "• Tighter range = stronger hands only",
        "• Connected cards (next to each other) are strong"
    ]

    clock = pygame.time.Clock()
    running = True

    #
    # 4. Main Loop
    #
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if the back button was clicked using the Button class
                if back_button.checkForInput(event.pos):
                    mainMenu()
                    running = False

                # Check if the text box was clicked.
                if input_box_rect.collidepoint(mouse_x, mouse_y):
                    input_active = True
                else:
                    input_active = False
                    # Check if slider area was clicked.
                    if slider_y <= mouse_y <= slider_y + SLIDER_AREA_HEIGHT:
                        slider_dragging = True
                        relative_x = mouse_x - slider_x
                        relative_x = max(0, min(relative_x, slider_width))
                        slider_value = (relative_x / slider_width) * 100
                        update_range_from_slider()
                    else:
                        # Check if grid area was clicked.
                        if (container_x <= mouse_x <= container_x + GRID_WIDTH and 
                            container_y <= mouse_y <= container_y + GRID_HEIGHT):
                            col = (mouse_x - (container_x + MARGIN)) // (CELL_SIZE + MARGIN)
                            row = (mouse_y - (container_y + MARGIN)) // (CELL_SIZE + MARGIN)
                            if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                                selected[row][col] = not selected[row][col]

            elif event.type == pygame.MOUSEBUTTONUP:
                slider_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging:
                    mouse_x, _ = event.pos
                    relative_x = mouse_x - slider_x
                    relative_x = max(0, min(relative_x, slider_width))
                    slider_value = (relative_x / slider_width) * 100
                    update_range_from_slider()

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Validate and update the slider_value from the text input.
                        try:
                            # Remove the % symbol before converting to float
                            new_val = float(input_text.rstrip('%'))
                        except ValueError:
                            new_val = slider_value
                        new_val = max(0, min(new_val, 100))  # Clamp between 0 and 100.
                        slider_value = new_val
                        update_range_from_slider()
                        input_text = str(round(slider_value)) + "%"
                        input_active = False  # Exit text input mode.
                    elif event.key == pygame.K_BACKSPACE:
                        if len(input_text) > 1:  # Keep at least 1 character + %
                            input_text = input_text[:-2] + "%"
                    else:
                        # Only allow digits for percentage entry
                        if event.unicode.isdigit() and len(input_text.rstrip('%')) < 3:  # Limit to 3 digits
                            input_text = input_text.rstrip('%') + event.unicode + "%"

        # Redraw background, textbox, and header text.
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        SCREEN.blit(HAND_VISUALIZER_TEXT, HAND_VISUALIZER_RECT)

        # Update and draw the back button
        back_button.changecolour(pygame.mouse.get_pos())
        back_button.update(SCREEN)

        # Draw the 13x13 grid.
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = container_x + MARGIN + col * (CELL_SIZE + MARGIN)
                y = container_y + MARGIN + row * (CELL_SIZE + MARGIN)
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if selected[row][col]:
                    colour = GREEN
                else:
                    if row == col:
                        colour = PAIR_GREY
                    elif row < col:
                        colour = LIGHT_GREY
                    else:
                        colour = VERY_LIGHT_GREY

                pygame.draw.rect(SCREEN, colour, cell_rect)
                pygame.draw.rect(SCREEN, BLACK, cell_rect, 1)

                text_surface = font.render(get_hand_notation(row, col), True, BLACK)
                text_rect = text_surface.get_rect(center=cell_rect.center)
                SCREEN.blit(text_surface, text_rect)

        # Draw the slider.
        pygame.draw.rect(
            SCREEN,
            SLIDER_TRACK_COLOUR,
            (slider_x, slider_y + slider_height // 2 - track_height // 2, slider_width, track_height)
        )
        pygame.draw.circle(
            SCREEN,
            SLIDER_KNOB_COLOUR,
            (int(slider_x + (slider_value / 100.0) * slider_width), int(slider_y + slider_height // 2)),
            knob_radius
        )
        slider_text = slider_font.render(f"Hand Range: {slider_value:.0f}%", True, WHITE)
        SCREEN.blit(slider_text, (slider_x, slider_y - 10))

        # Draw the text input box next to the slider.
        if not input_active:
            input_text = str(round(slider_value)) + "%"
        box_colour = TEXT_BOX_ACTIVE_colour if input_active else TEXT_BOX_colour
        pygame.draw.rect(SCREEN, box_colour, input_box_rect)
        pygame.draw.rect(SCREEN, BLACK, input_box_rect, 2)  # Border
        input_surface = slider_font.render(input_text, True, BLACK)
        SCREEN.blit(input_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

        # Draw explanatory text
        y_offset = container_y
        for line in explanations:
            text_surface = explanation_font.render(line, True, "White")
            SCREEN.blit(text_surface, (container_x + GRID_WIDTH + 50, y_offset))
            y_offset += 30

        # *** Draw the custom cursor last so it's always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_cursor, current_mouse_pos)

        pygame.display.flip()
    pygame.quit()
    sys.exit()
