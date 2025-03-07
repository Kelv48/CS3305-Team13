import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS
import threading
import json
from src.multiplayer_game.game_menu import gameMenu
from src.multiplayer_game.network.client.client import Client
from src.multiplayer_game.network.server.protocol import Protocols
from websockets.exceptions import ConnectionClosed

def create_game(mainMenu, c=None):
    print("CREATE GAME SCREEN")
    global vote_start_count, num_players, listening
    vote_start_count = 0  # Default value
    num_players = 1       #Default value 

    #Thread config 
    stop_thread = threading.Event() #Used to stop thread from calling itself
    lock = threading.Lock()         #Used to prevent race conditions/deadlocks


    #Retrieve username from login file
    with open('local.json', 'r') as f:
        data = json.load(f)
        username = data['username']

    # Connect to the server
    if not c:
        client =  Client.connect("84.8.144.77", 8000)
        #client = Client.connect('localhost', 80)
        client.setID(username)  #sets clients username 
        client.send(Protocols.Request.CREATE_GAME, 6)
    else:
         client = c
    
    def listener_thread():
        global vote_start_count, num_players
        
        #If it is set the escape the threaded method
        if stop_thread.is_set():
            print("AAAAAA Thread is stopped")
            return

      
        #It is getting stuck here so it isn't properly exiting when application is closed 
        try:
            msg = client.receive()
        except ConnectionClosed as e:
            print("Client connection closed. Leaving thread")
            stop_thread.is_set()
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
                
                case Protocols.Response.CLIENT_LIST:
                            
                            client.set_main_menu(mainMenu)

                    
                            client.receive()        #redirects client to game_server
                            stop_thread.set()    #Stops the thread from being called again
                            client.run_game(3)      #Move to game screen
                #             return  #Exit the thread
                # case Protocols.Response.SESSION_ID:
                #         client.setSessionID(msg['data'])

      
        # Schedule the function to run again in 1 second
        threading.Timer(5, listener_thread).start()
        print("AAAAAAAA calling thread function again")
    

    listener_thread()
    clock = pygame.Clock()
    while True:
        #print("AAAAAA WHY AREN'T YOU RENDERING ;)")
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


        # Calculate positions based on current screen size
        GAME_CODE_TEXT = screen_font(50).render("Game Code", True, "Gold")
        GAME_CODE_RECT = GAME_CODE_TEXT.get_rect(center=(screen_width / 2, screen_height / 3))
        SCREEN.blit(GAME_CODE_TEXT, GAME_CODE_RECT)

        # Display game code
        game_code = client.getSessionID()  # placeholder game code
        code_text = screen_font(40).render(game_code, True, "White")
        code_rect = code_text.get_rect(center=(screen_width / 2, screen_height / 2.5))
        SCREEN.blit(code_text, code_rect)

        # Display start game votes on the left and number of players on the right (both out of 6 max)

       #with lock:
        votes_text = screen_font(30).render(f"Votes: {vote_start_count}/6", True, "Gold")
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
                            stop_thread.set()
                            pygame.quit()
                            sys.exit()
                        elif action == "start_game_early":
                            print("Starting game early")
                            client.send(Protocols.Request.START_GAME_EARLY_VOTE) # Send the vote to the server
                        
                        else:
                            client.disconnect()
                            stop_thread.set()
                            action()

        # readable, _, _ = select.select([client.client.socket], [], [], 0.1)
        # print(client.client.socket)
        # # for s in readable:
        # #     if s == client.websocket:
        # if  not readable:
        #         print("AAAAAAAAA MESSAGE ME")
        #         msg = client.receive(5)  # Receive message from WebSocket
        #         if msg:
        #             msg_data = json.loads(msg)
        #             match msg_data.get('type'):
        #                 case 'FORCE_START':
        #                     vote_start_count = msg_data.get('data')
        #                     print(f"Vote count: {vote_start_count}")
        #                 case 'UPDATE_PLAYERS':
        #                     num_players = msg_data.get('data', 0)
        #                     print(f"Number of players: {num_players}")

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (LOBBY_MOUSE_POS[0], LOBBY_MOUSE_POS[1]))
    
        # Update the display
        pygame.display.update()
