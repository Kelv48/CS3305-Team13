import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS

TEXT_COLOR = pygame.Color('white')
FONT = screen_font(28)
BIG_FONT = screen_font(48)

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


def hand_rankings(mainMenu):
    CARD_WIDTH, CARD_HEIGHT = 60, 73  # Smaller cards for this screen
    card_images = load_card_images(CARD_WIDTH, CARD_HEIGHT)

    # Define hand rankings with examples
    rankings = [
        {
            "name": "Royal Flush",
            "desc": "A-K-Q-J-10 of same suit",
            "cards": [(14,'H'), (13,'H'), (12,'H'), (11,'H'), (10,'H')]
        },
        {
            "name": "Straight Flush",
            "desc": "Five sequential cards, same suit",
            "cards": [(9,'S'), (8,'S'), (7,'S'), (6,'S'), (5,'S')]
        },
        {
            "name": "Four of a Kind",
            "desc": "Four cards of same rank",
            "cards": [(8,'H'), (8,'D'), (8,'S'), (8,'C'), (13,'H')]
        },
        {
            "name": "Full House",
            "desc": "Three of a kind with a pair",
            "cards": [(11,'H'), (11,'D'), (11,'S'), (4,'C'), (4,'H')]
        },
        {
            "name": "Flush",
            "desc": "Five cards of same suit",
            "cards": [(14,'D'), (10,'D'), (7,'D'), (6,'D'), (2,'D')]
        },
        {
            "name": "Straight",
            "desc": "Five sequential cards",
            "cards": [(9,'H'), (8,'S'), (7,'D'), (6,'C'), (5,'H')]
        },
        {
            "name": "Three of a Kind",
            "desc": "Three cards of same rank",
            "cards": [(7,'H'), (7,'D'), (7,'S'), (13,'C'), (2,'H')]
        },
        {
            "name": "Two Pair",
            "desc": "Two different pairs",
            "cards": [(13,'H'), (13,'D'), (8,'S'), (8,'C'), (3,'H')]
        },
        {
            "name": "One Pair",
            "desc": "One pair of same rank",
            "cards": [(10,'H'), (10,'D'), (14,'S'), (7,'C'), (2,'H')]
        },
        {
            "name": "High Card",
            "desc": "Highest card wins",
            "cards": [(14,'H'), (10,'D'), (8,'S'), (6,'C'), (2,'H')]
        }
    ]

    # Calculate grid layout
    grid_margin = 20  # Space between grid items
    grid_height = 120  # Height of each grid cell

    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        SINGLE_MOUSE_POS = pygame.mouse.get_pos()

        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Create main container
        textbox_width = int(screen_width * 0.9)
        textbox_height = int(screen_height * 0.8)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.1)

        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 150), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Title
        TITLE_TEXT = screen_font(50).render("HAND RANKINGS", True, "Gold")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(screen_width / 2, screen_height / 13))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)

        grid_width = textbox_width / 3 - grid_margin  # Width of each grid cell
        # Start position for the grid
        grid_start_x = textbox_x + grid_margin
        grid_start_y = textbox_y + 40

        for i, ranking in enumerate(rankings):
            if i < 9:  # First 9 rankings in 3x3 grid
                # Calculate grid position
                row = i // 3
                col = i % 3

                # Calculate position for this grid cell
                cell_x = grid_start_x + col * (grid_width + grid_margin)
                cell_y = grid_start_y + row * (grid_height + grid_margin)

                # Ranking name
                name_text = screen_font(25).render(f"{i+1}. {ranking['name']}", True, "Gold")
                name_rect = name_text.get_rect(center=(cell_x + grid_width/2, cell_y))
                SCREEN.blit(name_text, name_rect)

                # Ranking description
                desc_text = screen_font(20).render(f"{ranking['desc']}", True, "White")
                desc_rect = desc_text.get_rect(center=(cell_x + grid_width/2, cell_y + 20))
                SCREEN.blit(desc_text, desc_rect)

                # Display cards
                card_start_x = cell_x + (grid_width - (len(ranking['cards']) * (CARD_WIDTH + 10))) / 2
                for j, card in enumerate(ranking['cards']):
                    card_x = card_start_x + j * (CARD_WIDTH + 10)
                    SCREEN.blit(card_images[card], (card_x, cell_y + 30))

            else:  # Last ranking (High Card) centered below the grid
                last_cell_y = grid_start_y + 3 * (grid_height + grid_margin)

                # Ranking name
                name_text = screen_font(25).render(f"{i+1}. {ranking['name']}", True, "Gold")
                name_rect = name_text.get_rect(center=(textbox_x + textbox_width/2, last_cell_y))
                SCREEN.blit(name_text, name_rect)

                # Ranking description
                desc_text = screen_font(20).render(f"{ranking['desc']}", True, "White")
                desc_rect = desc_text.get_rect(center=(textbox_x + textbox_width/2, last_cell_y + 20))
                SCREEN.blit(desc_text, desc_rect)

                # Display cards
                card_start_x = textbox_x + (textbox_width - (len(ranking['cards']) * (CARD_WIDTH + 10))) / 2
                for j, card in enumerate(ranking['cards']):
                    card_x = card_start_x + j * (CARD_WIDTH + 10)
                    SCREEN.blit(card_images[card], (card_x, last_cell_y + 30))

        # Create HOME button
        HOME_BUTTON = Button(
            pos=(60, 35),  # Moved to top left corner
            text_input="HOME",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Gold",
            image=pygame.Surface((120, 45), pygame.SRCALPHA)  # Create transparent surface for background
        )
        # Add semi-transparent black background to button image
        pygame.draw.rect(HOME_BUTTON.image, (0, 0, 0, 128), HOME_BUTTON.image.get_rect(), border_radius=10)

        HOME_BUTTON.changecolour(SINGLE_MOUSE_POS)
        HOME_BUTTON.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and HOME_BUTTON.checkForInput(SINGLE_MOUSE_POS):
                mainMenu()

        # Draw cursor
        SCREEN.blit(scaled_cursor, (SINGLE_MOUSE_POS[0], SINGLE_MOUSE_POS[1]))

        # Update display
        pygame.display.update()
