import pygame, sys
import threading
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS
from src.multiplayer_game.network.server.protocol import Protocols

# #Temp import
# from src.gui.screens.main_menu import mainMenu

from src.multiplayer_game.network.client.client import Client

# Dummy lobby data
DUMMY_LOBBIES = [
    {"CODE": "ABC123", "players": 2, "max_players": 6, "status": "Waiting"},
    {"CODE": "DEF456", "players": 3, "max_players": 6, "status": "Waiting"},
    {"CODE": "GHI789", "players": 1, "max_players": 6, "status": "Waiting"},
    {"CODE": "JKL012", "players": 6, "max_players": 6, "status": "Full"},
    {"CODE": "MNO345", "players": 4, "max_players": 6, "status": "Waiting"},
    {"CODE": "PQR678", "players": 2, "max_players": 6, "status": "Waiting"},
    {"CODE": "STU901", "players": 5, "max_players": 6, "status": "Waiting"},
    {"CODE": "VWX234", "players": 1, "max_players": 6, "status": "Waiting"},
    {"CODE": "YZA567", "players": 3, "max_players": 6, "status": "Waiting"},
    {"CODE": "BCD890", "players": 4, "max_players": 6, "status": "Waiting"}
]

def join_game(mainMenu):
    print("JOIN GAME SCREEN")
    c = Client.connect("localhost", 80)

    # #Thread config 
    # stop_thread = threading.Event() #Used to stop thread from calling itself
    # lock = threading.Lock()         #Used to prevent race conditions/deadlocks
    # def listener_thread():
    #     global vote_start_count, num_players
        
    #     #If it is set the escape the threaded method
    #     if stop_thread.is_set():
    #         print("AAAAAA Thread is stopped")
    #         return

      
    #     #It is getting stuck here so it isn't properly exiting when application is closed 
    #     msg = c.receive()
    #     if msg:
    #         data = msg  # Assuming msg is already a dictionary
    #         match data['m_type']:
    #             case Protocols.Response.FORCE_START:
    #                 with lock:
    #                         vote_start_count = data['data']
    #                         print(f"Vote count updated: {vote_start_count}")
    #             case Protocols.Response.LOBBY_UPDATE:
    #                     with lock:
    #                         num_players = data.get("data")
    #                         print(f"Number of players updated: {num_players}")
                
    #             case Protocols.Response.REDIRECT:
    #                         c.redirect(msg['data']['host'], msg['data']['port'])
    #                         return  #Exit the thread
    #             case Protocols.Response.SESSION_ID:
    #                     c.setSessionID(msg['data'])

      
    #     # Schedule the function to run again in 1 second
    #     threading.Timer(5, listener_thread).start()
    #     print("AAAAAAAA calling thread function again")

    # listener_thread()
    clock = pygame.Clock()
    selected_lobby = None
    scroll_position = 0
    scroll_speed = 30  # Pixels per scroll
    visible_lobbies = 5  # Number of lobbies visible at once
    
    # Text input variables
    input_text = ""
    input_active = False
    input_rect = None
    input_font = screen_font(30)

    while True:
        clock.tick(FPS)
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

        # Add manual lobby code input section
        input_label = input_font.render("Enter Lobby Code:", True, "White")
        SCREEN.blit(input_label, (textbox_x + 70, textbox_y + 40))

        # Create input box
        input_box_width = 200
        input_box_height = 40
        input_box_x = textbox_x + 300
        input_box_y = textbox_y + 35
        input_rect = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        
        # Draw input box with border
        input_box_colour = "Green" if input_active else "White"
        pygame.draw.rect(SCREEN, input_box_colour, input_rect, 2)
        
        # Render input text
        text_surface = input_font.render(input_text, True, "White")
        SCREEN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        
        # Draw cursor when input is active
        if input_active:
            text_width = text_surface.get_width()
            cursor_x = input_rect.x + 5 + text_width
            cursor_y_top = input_rect.y + 5
            cursor_y_bottom = input_rect.y + 1 + text_surface.get_height()
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.line(SCREEN, "White", (cursor_x, cursor_y_top), (cursor_x, cursor_y_bottom), 2)

        # Display lobbies
        lobby_font = screen_font(30)
        lobby_height = 60
        start_y = textbox_y + 100
        spacing = 20

        # Add header text
        header_font = screen_font(25)
        headers = ["Lobby Code", "Players", "Status"]
        header_x_positions = [
            textbox_x + 70,
            textbox_x + textbox_width - 300,
            textbox_x + textbox_width - 150
        ]
        
        for i, header in enumerate(headers):
            header_text = header_font.render(header, True, "Gold")
            SCREEN.blit(header_text, (header_x_positions[i], textbox_y + 70))

        # Calculate scrollbar dimensions
        scrollbar_width = 25  # Increased width for better visibility
        scrollbar_height = (textbox_height - 100) * (visible_lobbies / len(DUMMY_LOBBIES))
        scrollbar_x = textbox_x + textbox_width - scrollbar_width - 15  # Adjusted position
        scrollbar_y = textbox_y + 100
        scrollbar_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        
        # Draw scrollbar track (background)
        track_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, textbox_height - 100)
        pygame.draw.rect(SCREEN, (100, 100, 100, 100), track_rect, border_radius=15)  # Darker track
        pygame.draw.rect(SCREEN, (255, 255, 255, 100), track_rect, 2, border_radius=15)  # White border
        
        # Draw scrollbar thumb
        scrollbar_pos = scrollbar_y + (scroll_position / (len(DUMMY_LOBBIES) - visible_lobbies)) * (textbox_height - 100 - scrollbar_height)
        thumb_rect = pygame.Rect(scrollbar_x, scrollbar_pos, scrollbar_width, scrollbar_height)
        pygame.draw.rect(SCREEN, (200, 200, 200, 200), thumb_rect, border_radius=15)  # Lighter thumb
        pygame.draw.rect(SCREEN, (255, 255, 255, 255), thumb_rect, 2, border_radius=15)  # White border

        # Display visible lobbies based on scroll position
        for i in range(visible_lobbies):
            lobby_index = i + int(scroll_position / (lobby_height + spacing))
            if lobby_index >= len(DUMMY_LOBBIES):
                break
                
            lobby = DUMMY_LOBBIES[lobby_index]
            lobby_y = start_y + (i * (lobby_height + spacing))
            
            # Create lobby entry background
            entry_surface = pygame.Surface((textbox_width - 100, lobby_height), pygame.SRCALPHA)
            
            # Check if this lobby is selected
            is_selected = selected_lobby == lobby_index
            highlight_color = (0, 255, 0, 50) if is_selected else (255, 255, 255, 30)
            
            pygame.draw.rect(entry_surface, highlight_color, (0, 0, textbox_width - 100, lobby_height), border_radius=10)
            SCREEN.blit(entry_surface, (textbox_x + 50, lobby_y))

            # Lobby code
            code_text = lobby_font.render(lobby["CODE"], True, "White")
            SCREEN.blit(code_text, (textbox_x + 70, lobby_y + 15))

            # Player count
            player_text = lobby_font.render(f"{lobby['players']}/{lobby['max_players']}", True, "White")
            SCREEN.blit(player_text, (textbox_x + textbox_width - 300, lobby_y + 15))

            # Status
            status_color = "Green" if lobby["status"] == "Waiting" else "Red"
            status_text = lobby_font.render(lobby["status"], True, status_color)
            SCREEN.blit(status_text, (textbox_x + textbox_width - 150, lobby_y + 15))

            # Check if mouse is over this lobby
            lobby_rect = pygame.Rect(textbox_x + 50, lobby_y, textbox_width - 100, lobby_height)
            if lobby_rect.collidepoint(LOBBY_MOUSE_POS):
                pygame.draw.rect(entry_surface, (255, 255, 255, 70), (0, 0, textbox_width - 100, lobby_height), border_radius=10)
                SCREEN.blit(entry_surface, (textbox_x + 50, lobby_y))

        # Define button labels and functions
        buttons = [
            ("LEAVE LOBBY", mainMenu),
            ("JOIN GAME", lambda: print(f"Joining lobby: {input_text if input_text else DUMMY_LOBBIES[selected_lobby]['CODE']}") if selected_lobby is not None or input_text else None)
        ]

        # Calculate horizontal spacing for buttons
        button_count = len(buttons)
        button_x_spacing = screen_width / (button_count + 1)
        fixed_y = screen_height * 0.85  # Fixed vertical position for the buttons

        # Create and position buttons horizontally
        button_objects = []
        for index, (text, action) in enumerate(buttons):
            button_x = (index + 1) * button_x_spacing
            button = Button(
                pos=(button_x, fixed_y), 
                text_input=text, 
                font=screen_font(30), 
                base_colour="White" if text != "JOIN GAME" or selected_lobby is not None or input_text else "Gray", 
                hovering_colour="Light Green" if text != "JOIN GAME" or selected_lobby is not None or input_text else "Gray",
                image=None)

            button.changecolour(LOBBY_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks, lobby selection, and scrolling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for input box click
                if input_rect and input_rect.collidepoint(LOBBY_MOUSE_POS):
                    input_active = True
                    selected_lobby = None  # Clear lobby selection when input is active
                else:
                    input_active = False

                # Check for scrollbar click
                if scrollbar_rect.collidepoint(LOBBY_MOUSE_POS):
                    # Calculate new scroll position based on click
                    relative_y = LOBBY_MOUSE_POS[1] - scrollbar_y
                    scroll_position = (relative_y / (textbox_height - 100)) * (len(DUMMY_LOBBIES) - visible_lobbies) * (lobby_height + spacing)
                    scroll_position = max(0, min(scroll_position, (len(DUMMY_LOBBIES) - visible_lobbies) * (lobby_height + spacing)))

                # Check for lobby selection
                for i in range(visible_lobbies):
                    lobby_index = i + int(scroll_position / (lobby_height + spacing))
                    if lobby_index >= len(DUMMY_LOBBIES):
                        break
                    lobby_y = start_y + (i * (lobby_height + spacing))
                    lobby_rect = pygame.Rect(textbox_x + 50, lobby_y, textbox_width - 100, lobby_height)
                    if lobby_rect.collidepoint(LOBBY_MOUSE_POS):
                        selected_lobby = lobby_index
                        input_active = False  # Clear input when selecting a lobby
                        input_text = ""  # Clear input text when selecting a lobby
                        break

                # Check for button clicks
                for button, action in button_objects:
                    if button.checkForInput(LOBBY_MOUSE_POS):
                        if action == sys.exit:
                            pygame.quit()
                            sys.exit()
                        elif action == "start_game_early":
                            print("Starting game early")
                        elif action is not None:  # Only execute if action is not None
                            #stop_thread.is_set()
                            action()

            # Handle text input
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        # Handle enter key - you can add specific logic here
                        print(f"Entered lobby code: {input_text}")
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Only allow alphanumeric characters
                        if event.unicode.isalnum() and len(input_text) < 6:
                            input_text += event.unicode.upper()

            # Handle mouse wheel scrolling
            if event.type == pygame.MOUSEWHEEL:
                scroll_position -= event.y * scroll_speed
                # Clamp scroll position
                max_scroll = (len(DUMMY_LOBBIES) - visible_lobbies) * (lobby_height + spacing)
                scroll_position = max(0, min(scroll_position, max_scroll))

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (LOBBY_MOUSE_POS[0], LOBBY_MOUSE_POS[1]))

        # Update the display
        pygame.display.update()