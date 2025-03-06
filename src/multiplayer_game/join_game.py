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
    {"CODE": "JKL012", "players": 6, "max_players": 6, "status": "Full"}
]

def join_game(mainMenu):
    print("JOIN GAME SCREEN")
    c = Client.connect("localhost", 80)

    #Thread config 
    stop_thread = threading.Event() #Used to stop thread from calling itself
    lock = threading.Lock()         #Used to prevent race conditions/deadlocks
    def listener_thread():
        global vote_start_count, num_players
        
        #If it is set the escape the threaded method
        if stop_thread.is_set():
            print("AAAAAA Thread is stopped")
            return

      
        #It is getting stuck here so it isn't properly exiting when application is closed 
        msg = c.receive()
        if msg:
            data = msg  # Assuming msg is already a dictionary
            match data['m_type']:
                case Protocols.Response.FORCE_START:
                    with lock:
                            vote_start_count = data['data']
                            print(f"Vote count updated: {vote_start_count}")
                case Protocols.Response.LOBBY_UPDATE:
                        with lock:
                            num_players = data.get("data")
                            print(f"Number of players updated: {num_players}")
                
                case Protocols.Response.REDIRECT:
                            c.redirect(msg['data']['host'], msg['data']['port'])
                            return  #Exit the thread
                case Protocols.Response.SESSION_ID:
                        c.setSessionID(msg['data'])

      
        # Schedule the function to run again in 1 second
        threading.Timer(5, listener_thread).start()
        print("AAAAAAAA calling thread function again")

    listener_thread()
    clock = pygame.Clock()
    selected_lobby = None
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

        # Display dummy lobbies
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

        for i, lobby in enumerate(DUMMY_LOBBIES):
            lobby_y = start_y + (i * (lobby_height + spacing))
            
            # Create lobby entry background
            entry_surface = pygame.Surface((textbox_width - 100, lobby_height), pygame.SRCALPHA)
            
            # Check if this lobby is selected
            is_selected = selected_lobby == i
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
            ("JOIN GAME", lambda: print(f"Joining lobby: {DUMMY_LOBBIES[selected_lobby]['CODE']}") if selected_lobby is not None else None)
        ]

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
                base_colour="White" if text != "JOIN GAME" or selected_lobby is not None else "Gray", 
                hovering_colour="Light Green" if text != "JOIN GAME" or selected_lobby is not None else "Gray",
                image=None)

            button.changecolour(LOBBY_MOUSE_POS)
            button.update(SCREEN)
            button_objects.append((button, action))

        # Check for button clicks and lobby selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for lobby selection
                for i, lobby in enumerate(DUMMY_LOBBIES):
                    lobby_y = start_y + (i * (lobby_height + spacing))
                    lobby_rect = pygame.Rect(textbox_x + 50, lobby_y, textbox_width - 100, lobby_height)
                    if lobby_rect.collidepoint(LOBBY_MOUSE_POS):
                        selected_lobby = i
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
                            stop_thread.is_set()
                            action()

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (LOBBY_MOUSE_POS[0], LOBBY_MOUSE_POS[1]))

        # Update the display
        pygame.display.update()