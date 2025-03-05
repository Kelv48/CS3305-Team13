import pygame, sys
import asyncio
import math
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor

from src.multiplayer_game.network.client.client import Client

# #Temp import
# from src.gui.screens.main_menu import mainMenu

def loading_screen(mainMenu):
    print("LOADING SCREEN")
    c = asyncio.run(Client.connect("localhost", 80))

    # Initialize animation variables
    angle = 0
    wheel_radius = 60
    rotation_speed = 3  # Degrees per frame
    num_segments = 12  # Number of segments in the wheel
    
    # Colors for the wheel
    colors = ["Red", "Black"]  # Alternating colors for segments
    
    while True:
        LOBBY_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size    # Scale the background to fit the screen
        screen_width, screen_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height)) 
        SCREEN.blit(scaled_bg, (0, 0))
        
        # Calculate positions based on current screen size
        LOBBY_TEXT = screen_font(50).render("Loading...", True, "Gold")
        LOBBY_RECT = LOBBY_TEXT.get_rect(center=(screen_width / 2, screen_height / 13))
        SCREEN.blit(LOBBY_TEXT, LOBBY_RECT)

        # Draw roulette wheel
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Draw wheel segments
        for i in range(num_segments):
            segment_angle = 360 / num_segments
            start_angle = math.radians(angle + (i * segment_angle))
            end_angle = math.radians(angle + ((i + 1) * segment_angle))
            
            # Calculate points for the segment
            start_x = center_x + wheel_radius * math.cos(start_angle)
            start_y = center_y + wheel_radius * math.sin(start_angle)
            end_x = center_x + wheel_radius * math.cos(end_angle)
            end_y = center_y + wheel_radius * math.sin(end_angle)
            
            # Draw segment
            pygame.draw.polygon(SCREEN, colors[i % 2], [
                (center_x, center_y),
                (start_x, start_y),
                (end_x, end_y)
            ])
            
            # Draw segment border
            pygame.draw.line(SCREEN, "Gold", (center_x, center_y), (start_x, start_y), 2)
            pygame.draw.line(SCREEN, "Gold", (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.line(SCREEN, "Gold", (end_x, end_y), (center_x, center_y), 2)
            
            # Draw numbers
            number = str(i + 1)
            number_angle = start_angle + (end_angle - start_angle) / 2
            number_x = center_x + (wheel_radius * 0.7) * math.cos(number_angle)
            number_y = center_y + (wheel_radius * 0.7) * math.sin(number_angle)
            number_text = screen_font(15).render(number, True, "White")
            number_rect = number_text.get_rect(center=(number_x, number_y))
            SCREEN.blit(number_text, number_rect)
        
        # Draw center circle
        pygame.draw.circle(SCREEN, "Gold", (center_x, center_y), 10)
        
        # Update angle for next frame
        angle = (angle + rotation_speed) % 360

        # Define button labels and functions
        buttons = [
            ("LEAVE LOBBY", mainMenu)]

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
                        else:
                            action()
        
        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (LOBBY_MOUSE_POS[0], LOBBY_MOUSE_POS[1]))

        # Update the display
        pygame.display.update()