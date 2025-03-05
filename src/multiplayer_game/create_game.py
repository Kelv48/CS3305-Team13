import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor

import json
import asyncio
from src.multiplayer_game.network.client.client import Client
from src.multiplayer_game.network.server.protocol import Protocols

# def create_game_async():
#     print("CREATE GAME SCREEN")

#     # Connect to the server
#     client =  Client.connect("localhost", 80)
#     client.send(Protocols.Request.CREATE_GAME, 3)

#     msg =  client.receive()  # Get the vote count from the server
#     vote_start_count = 0  # Default value
#     print("AHAHAHHHAHAHA", type(msg), "||||", msg)
#     if msg:
#         print(msg)
#         match msg['m_type']:
#             case Protocols.Response.FORCE_START:
#                 # vote_start_count = int(msg.get('data'))  # Ensure conversion to int
#                 vote_start_count = msg.get('data')
#                 print(f"Vote count: {vote_start_count}")

def create_game(mainMenu):
    print("CREATE GAME SCREEN")
    #Retrieve username
    with open('local.json', 'r') as f:
        data = json.load(f)
        username = data['username']
    # Connect to the server
    client =  Client.connect("localhost", 80)
    client.setID(username)
    client.send(Protocols.Request.CREATE_GAME, 3)

    msg =  client.receive()  # Get the vote count from the server
    vote_start_count = 0  # Default value
    print("AHAHAHHHAHAHA", type(msg), "||||", msg)
    if msg:
        print(msg)
        match msg['m_type']:
            case Protocols.Response.FORCE_START:
                # vote_start_count = int(msg.get('data'))  # Ensure conversion to int
                vote_start_count = msg.get('data')
                print(f"Vote count: {vote_start_count}")

    while True:
        LOBBY_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        SCREEN.blit(scaled_bg, (0, 0))



        # Transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.9)      # 20% of screen width
        textbox_height = int(screen_height * 0.85)      # 70% of screen height
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.1)          # Start 15% down from the top

        # Create a new Surface with per-pixel alpha (using SRCALPHA).
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        # Draw a filled rounded rectangle on the textbox_surface.
        # The colour (0, 0, 0, 100) is black with an alpha value of 100 (semi-transparent).
        # Adjust the border_radius (here, 20) to control the roundness of the corners.
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        # Blit the textbox to the main screen.
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        
        # Calculate positions based on current screen size
        LOBBY_TEXT = screen_font(50).render("Lobby", True, "Gold")
        LOBBY_RECT = LOBBY_TEXT.get_rect(center=(screen_width / 2, screen_height / 13))
        SCREEN.blit(LOBBY_TEXT, LOBBY_RECT)


        # Calculate positions based on current screen size
        GAME_CODE_TEXT = screen_font(50).render("Game Code", True, "Gold")
        GAME_CODE_RECT = GAME_CODE_TEXT.get_rect(center=(screen_width / 2, screen_height / 3))
        SCREEN.blit(GAME_CODE_TEXT, GAME_CODE_RECT)

        # Display game code
        game_code = "ABC123"  # placeholder game code
        code_text = screen_font(40).render(game_code, True, "White")
        code_rect = code_text.get_rect(center=(screen_width / 2, screen_height / 2.5))
        SCREEN.blit(code_text, code_rect)

        # Display start game votes on the left and number of players on the right (both out of 6 max)
        start_votes = 2  # placeholder for current vote count
        num_players = 4  # placeholder for current number of players
        
        votes_text = screen_font(30).render(f"Votes: {start_votes}/6", True, "Gold")
        players_text = screen_font(30).render(f"Players: {num_players}/6", True, "Gold")
        votes_rect = votes_text.get_rect(midleft=(200, screen_height / 2))
        players_rect = players_text.get_rect(midright=(screen_width - 200, screen_height / 2))
        SCREEN.blit(votes_text, votes_rect)
        SCREEN.blit(players_text, players_rect)

        # Define button labels and functions
        buttons = [
            ("LEAVE LOBBY", mainMenu),
            ("VOTE START", "start_game_early")]

        # Calculate horizontal spacing for buttons
        button_count = len(buttons)
        button_x_spacing = screen_width / (button_count + 1)
        fixed_y = screen_height * 0.85  # Fixed vertical position for the buttons, adjust as needed

        # Create and position buttons horizontally
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_x = (index + 1) * button_x_spacing
            button = Button(
                pos=(button_x, fixed_y), 
                text_input=text, 
                font=screen_font(30), 
                base_colour="White", 
                hovering_colour="Light Green",
                image=None)

            button.changecolour(LOBBY_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in button_objects:
                    if button.checkForInput(LOBBY_MOUSE_POS):
                        if action == sys.exit:
                            pygame.quit()
                            sys.exit()
                        elif action == "start_game_early":
                            print("Starting game early")
                            client.send(Protocols.Request.START_GAME_EARLY_VOTE) # Send the vote to the server

                            #print(data)
                        else:
                            action()

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (LOBBY_MOUSE_POS[0], LOBBY_MOUSE_POS[1]))

        # Update the display
        pygame.display.update()
