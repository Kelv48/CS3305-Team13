import pygame, sys
import math  
from src.gui.button import Button
from src.gui.constants import SCREEN, BG, screen_font, play_button_click_sound, play_winner_sound

screen_width, screen_height = SCREEN.get_size()
card_width = 70
card_height = 105

def game_screen(mainMenu):

    community_cards = []  # Initialize community cards within the function

    # Preload the label image for player info (replace the path with your image file)
    player_label_image = pygame.image.load("assets/buttons/action_button.png")
    # Set desired dimensions for the label image (adjust as needed)
    label_width, label_height = 180, 80
    player_label_image = pygame.transform.scale(player_label_image, (label_width, label_height))

    # For example, load your image file:
    button_image = pygame.image.load("assets/buttons/Asset 4.png").convert_alpha()
    # Scale the image 
    button_image = pygame.transform.scale(button_image, (150, 50))

    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()

        screen_width, screen_height = SCREEN.get_size()
        SCREEN.fill("black")

        ## Background Image (optional)
        # scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        # SCREEN.blit(scaled_bg, (0, 0))

        # Load and display the poker table image
        poker_table_image = pygame.image.load("assets/images/Table.png") 
        poker_table_image = pygame.transform.scale(poker_table_image, (800, 500)) 
        poker_table_rect = poker_table_image.get_rect(center=(screen_width / 2, screen_height / 1.9))
        SCREEN.blit(poker_table_image, poker_table_rect)

        # Draw 6 players evenly around the table in an elliptical formation
        num_players = 6  # Number of players
        radius_x = 550  # Radius along the x-axis
        radius_y = 270  # Radius along the y-axis
        center_x, center_y = screen_width / 2, screen_height / 2  # Center of the table

        player_positions = []  # Store player positions for card placement

        rotation_offset = +90  # Rotate all players by 90 degrees clockwise

        for i in range(num_players):
            # Calculate angle with the rotation offset
            angle = i * (360 / num_players) + rotation_offset  
            player_x = center_x + radius_x * math.cos(math.radians(angle))
            player_y = center_y + radius_y * math.sin(math.radians(angle))
            # (Optional: you can draw a marker here for debugging)
            # pygame.draw.circle(SCREEN, "Red", (int(player_x), int(player_y)), 20)
            player_positions.append((player_x, player_y))  # Store player position

        

        # Load player card images (placeholder paths)
        player_card_images = [
            pygame.image.load("assets/cards/AC.png"),
            pygame.image.load("assets/cards/AS.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
            pygame.image.load("assets/cards/red_back.png"),
        ]

        # Scale player cards to fit (updated sizes)
        card_width = 70
        card_height = 105
        player_card_images = [pygame.transform.scale(card, (card_width, card_height)) for card in player_card_images]


        for i in range(num_players):
            player_x, player_y = player_positions[i]
            card_spacing = -20  # Space between cards
            total_cards_width = 2 * card_width + card_spacing
            start_x = player_x - total_cards_width / 2
            card_y = player_y - card_height / 2

            for j in range(2):
                card_x = start_x + j * (card_width + card_spacing)
                # Set the tilt angle: left card +10°, right card -10°
                angle = 20 if j == 0 else -10

                # Rotate the card image
                rotated_card = pygame.transform.rotate(player_card_images[i * 2 + j], angle)
                
                # Recalculate the rectangle so that the rotated image is centered
                rotated_rect = rotated_card.get_rect(center=(card_x + card_width/2, card_y + card_height/2))
                
                # Draw the rotated card onto the screen
                SCREEN.blit(rotated_card, rotated_rect.topleft)


            # First, get the label image's rect so that we know where it is.
            label_rect = player_label_image.get_rect(center=(player_x, card_y + card_height + 15))
            SCREEN.blit(player_label_image, label_rect)

            # Now render the player info text.
            user_name = f"Player {i+1}"
            user_money = "$1000"  # Update dynamically as needed.
            text_box = f"{user_name} | {user_money}"
            text_surface = screen_font(20).render(text_box, True, "White")
            # Position the text surface so that its center is the same as the label's center.
            text_rect = text_surface.get_rect(center=label_rect.center)
            SCREEN.blit(text_surface, text_rect)


        # Define action buttons (using your existing Button class)
        buttons = [
            ("Fold", "fold_action"),
            ("Call", "call_action"),
            ("Raise", "raise_action"),
            ("Flop", flop),
            # ("Turn", turn),
            # ("River", river),
            # ("Clear", clear_community_cards)
        ]

        button_count = len(buttons)

        # Define fixed dimensions for the buttons and spacing
        button_height = 50
        button_width = 150  # Set the width for each button (adjust as needed)
        spacing = 10        # Space between buttons

        # Calculate the total width required for all buttons and the spacing between them
        total_buttons_width = button_count * button_width + (button_count - 1) * spacing

        # Compute the starting x-coordinate so that the buttons are centered horizontally
        start_x = (screen_width - total_buttons_width) / 1.01

        # Define the y-coordinate (30 pixels from the bottom as before)
        button_y = screen_height - button_height - 30  # button_height was defined earlier (or adjust as needed)

        # Create and position buttons
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            # Calculate x-position for the current button
            button_x = start_x + index * (button_width + spacing)
            
            button = Button(
                pos=(button_x, button_y),
                text_input=text,
                font=screen_font(30),
                base_colour="White",
                hovering_colour="Light Green",
                image=button_image
            )
            button.changecolour(GAME_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Calculate positions for community cards
        card_spacing = 0
        start_x = (screen_width - (5 * card_width + 4 * card_spacing)) / 2  # Center the cards horizontally

        for index, card in enumerate(community_cards):
            card_x = start_x + index * (card_width + card_spacing)
            card_y = (screen_height / 1.9) - (card_height / 2)  # Center vertically
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
                            community_cards = turn(community_cards)  # Append turn card
                        elif action == river:
                            community_cards = river(community_cards)  # Append river card
                        elif action == clear_community_cards:
                            community_cards = clear_community_cards()  # Clear community cards
                        else:
                            mainMenu()  # Return to main menu if needed

                        # Play sound for Call or Raise actions
                        if action == "call_action" or action == "raise_action":
                            play_button_click_sound()

        # Draw game text at the top of the screen
        GAME_TEXT = screen_font(30).render("Poker game", True, "White")
        GAME_RECT = GAME_TEXT.get_rect(center=(screen_width / 2, screen_height / 15))
        SCREEN.blit(GAME_TEXT, GAME_RECT)

        pygame.display.update()




def flop():
    # Load flop card images (placeholder paths)
    flop_card_images = [
        pygame.image.load("assets/cards/2C.png"),
        pygame.image.load("assets/cards/3C.png"),
        pygame.image.load("assets/cards/4C.png"),
    ]
    
    # Scale flop cards to fit
    flop_card_images = [pygame.transform.scale(card, (card_width, card_height)) for card in flop_card_images]

    return flop_card_images  # Return the list of flop card images

def turn(community_cards):
    # Load turn card image (placeholder path)
    turn_card_image = pygame.image.load("assets/cards/5C.png")
    
    # Scale turn card to fit
    turn_card_image = pygame.transform.scale(turn_card_image, (card_width, card_height))

    return community_cards + [turn_card_image]  # Append turn card to existing community cards

def river(community_cards):
    # Load river card image (placeholder path)
    river_card_image = pygame.image.load("assets/cards/6C.png")
    
    # Scale river card to fit
    river_card_image = pygame.transform.scale(river_card_image, (card_width, card_height))

    return community_cards + [river_card_image]  # Append river card to existing community cards

def clear_community_cards():
    return []  # Return an empty list to clear community card