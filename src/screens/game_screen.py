

import pygame, sys
import math  
from src.gui.button import Button
from src.gui.utils import  SCREEN, BG, GAME_BG, get_font, play_button_click_sound, play_winner_sound


screen_width, screen_height = SCREEN.get_size()
card_width = 100
card_height = 150

def game_screen(mainMenu):
    community_cards = []  # Initialize community cards within the function
    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()


        screen_width, screen_height = SCREEN.get_size()
        SCREEN.fill("black")

        ## Background Image
        # scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        # SCREEN.blit(scaled_bg, (0, 0))

        SCREEN.fill("black")

        # Load and display the poker table image
        poker_table_image = pygame.image.load("assets/images/extra/OGTable.png") 
        poker_table_image = pygame.transform.scale(poker_table_image, (900, 600)) 
        poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 2))
        SCREEN.blit(poker_table_image, poker_table_rect)

        # Draw 6 players evenly around the table in an elliptical formation
        num_players = 6  # Number of players
        radius_x = 460  # Radius along the x-axis
        radius_y = 280  # Radius along the y-axis
        center_x, center_y = screen_width / 2, screen_height / 2  # Center of the table

        player_positions = []  # Store player positions for card placement

        for i in range(num_players):
            angle = i * (360 / num_players)  # Angle for each player
            player_x = center_x + radius_x * math.cos(math.radians(angle))  # Use radius_x
            player_y = center_y + radius_y * math.sin(math.radians(angle))  # Use radius_y
            
            # Draw player (as a simple circle for this example)
            pygame.draw.circle(SCREEN, "Red", (int(player_x), int(player_y)), 20)  
            player_positions.append((player_x, player_y))  # Store player position

        # Load player card images (placeholder paths)
        player_card_images = [
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
        ]

        # Scale player cards to fit
        card_width = 100
        card_height = 150
        player_card_images = [pygame.transform.scale(card, (card_width, card_height)) for card in player_card_images]

        # Calculate positions for each player's cards
        for i in range(num_players):
            player_x, player_y = player_positions[i]
            card_spacing = 10  # Space between cards
            # Calculate card positions
            for j in range(2):  # Two cards per player
                card_x = player_x + (j - 0.5) * (card_width + card_spacing)  # Center the cards around the player
                card_y = player_y - card_height / 2  # Position above the player
                SCREEN.blit(player_card_images[i * 2 + j], (card_x, card_y))  # Draw player card

        # Define action buttons
        buttons = [
            ("Fold", "fold_action"),  
            ("Call", "call_action"),  
            ("Raise", "raise_action"),
            ("Flop", flop),  
            ("Turn", turn),  
            ("River", river),
            ("Clear", clear_community_cards)

        ]

        # Calculate vertical spacing for buttons
        button_count = len(buttons)
        button_height = 50  # Fixed height for buttons
        button_y = screen_height - button_height - 30  # 30 pixels from the bottom

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_x = (screen_width / 2) + (index - 1) * (button_height + 50)  # Centered with spacing
            button = Button(
                pos=(button_x, button_y), 
                text_input=text, 
                font=get_font(30), 
                base_color="White", 
                hovering_color="Light Green"
            )
            
            button.changeColor(GAME_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Load community card images (placeholder paths)
        community_card_images = [
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png"),
            pygame.image.load("assets/images/cards/red_back.png")
        ]

        # Scale community cards to fit
        community_card_images = [pygame.transform.scale(card, (card_width, card_height)) for card in community_card_images]

        # Calculate positions for community cards
        card_spacing = 10
        start_x = (screen_width - (5 * card_width + 4 * card_spacing)) / 2  # Center the cards

        for index, card in enumerate(community_cards):
            card_x = start_x + index * (card_width + card_spacing)
            card_y = (screen_height / 2) - (card_height / 2)  # Center vertically
            SCREEN.blit(card, (card_x, card_y))  # Draw community card

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(GAME_MOUSE_POS):
                        if action == flop:
                            community_cards = flop()  # Update community cards with flop
                        elif action == turn:
                            community_cards = turn(community_cards)  # Pass current cards to turn
                        elif action == river:
                            community_cards = river(community_cards)  # Pass current cards to river
                        elif action == clear_community_cards:
                            community_cards = clear_community_cards()  # Clear community cards
                        else:
                            mainMenu()  # Return to main menu if needed

                        # Check for specific actions to play sound
                        if action == "call_action" or action == "raise_action":
                            play_button_click_sound()  # Play sound effect for Call or Raise


        # Calculate positions based on current screen size
        GAME_TEXT = get_font(45).render("This is the GAME screen.", True, "White")
        GAME_RECT = GAME_TEXT.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(GAME_TEXT, GAME_RECT)

        pygame.display.update()






def flop():
    # Load flop card images (placeholder paths)
    flop_card_images = [
        pygame.image.load("assets/images/cards/2C.png"),
        pygame.image.load("assets/images/cards/3C.png"),
        pygame.image.load("assets/images/cards/4C.png"),
    ]
    
    # Scale flop cards to fit
    flop_card_images = [pygame.transform.scale(card, (card_width, card_height)) for card in flop_card_images]

    return flop_card_images  # Return the list of flop card images

def turn(community_cards):
    # Load turn card image (placeholder path)
    turn_card_image = pygame.image.load("assets/images/cards/5C.png")
    
    # Scale turn card to fit
    turn_card_image = pygame.transform.scale(turn_card_image, (card_width, card_height))

    return community_cards + [turn_card_image]  # Append turn card to existing cards

def river(community_cards):
    # Load river card image (placeholder path)
    river_card_image = pygame.image.load("assets/images/cards/6C.png")
    
    # Scale river card to fit
    river_card_image = pygame.transform.scale(river_card_image, (card_width, card_height))

    return community_cards + [river_card_image]  # Append river card to existing cards



def clear_community_cards():
    return []  # Return an empty list to clear community cards






        # GAME_BACK = Button(
        #     pos=(screen_width / 2, screen_height * 2 / 2.2), 
        #     text_input="BACK", 
        #     font=get_font(30), 
        #     base_color="White", 
        #     hovering_color="Light Green")

        # GAME_BACK.changeColor(GAME_MOUSE_POS)
        # GAME_BACK.update(SCREEN)

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if GAME_BACK.checkForInput(GAME_MOUSE_POS):
        #             mainMenu()

        # pygame.display.update()