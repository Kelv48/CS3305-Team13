
"""
This module provides functionality for creating and managing menus 
including initializing the menu, drawing the menu, handling input
and transitioning between screens.
    - Start menu
    - Game options
        - Fair poker
            - 2-6 players
        - Unfair poker
            - 2-6 players
        - Bots
            - Easy-Advanced
    - Settings menu
    - Guide menu
"""


import pygame
from buttons import Button
from settings import *
import helpers



def back_button(game_state, previous_screen):
    """
    Creates a back button to return to the previous screen.
    """
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    return Button(10, 10, 150, 50, "Back", lambda: previous_screen(game_state), image=button_image)




def start_menu(game_state):
    """
    Displays the start menu which displays buttons for:
        - Play
        - Settings
        - Guide
    Handles button clicks and toggles fullscreen mode when ESC is pressed.
    """
    menu_text = game_state.font.render("Poker Showdown!", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Poker Showdown!") 

    # Define the buttons and their functionality
    btns = [Button(0, 0, 200, 75, "Play", lambda: play_menu(game_state), image=button_image),
            Button(0, 0, 200, 75, "Settings", lambda: settings_menu(game_state), image=button_image),
            Button(0, 0, 200, 75, "Guide", lambda: guide_menu(game_state), image=button_image),]

    # Calculate the position and center buttons
    screen_width, screen_height = game_state.win.get_size()

    # Here is where the button will be centered
    for btn in btns:
        # Center each button horizontally and vertically
        btn.set_position((screen_width * 0.4), (screen_height * 0.4))

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        
        helpers.center_buttons(game_state.win, btns)  # Center buttons if required

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  # Use updated is_clicked()

        for btn in btns:
            btn.draw(game_state.win)  # Draw the buttons
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()






def play_menu(game_state):
    """
    Displays game options menu which displays buttons for
        - Fair poker
        - Unfair poker
        - Bots
    """
    menu_text = game_state.font.render("Play Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Play menu") 

    btns = [Button(165, 125, 200, 75, "Normal Poker", lambda: poker_options(game_state), image=button_image),
            Button(165, 225, 200, 75, "Unfair Poker", lambda: unfair_poker_options(game_state), image=button_image),
            Button(165, 325, 200, 75, "Bots", lambda: bot_options(game_state), image=button_image),
            back_button(game_state, start_menu)]

    
    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()


   

    
    
    



def poker_options(game_state):
    """
    Displays the poker options menu which displays buttons for
        - Create game
        - Join game
    """
    menu_text = game_state.font.render("Game Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Game Options") 

    btns = [
        Button(165, 125, 200, 75, "Create Game", lambda: main_game(game_state), image=button_image),
        Button(165, 225, 200, 75, "Join Game", lambda: main_game(game_state), image=button_image),
        back_button(game_state, start_menu)
    ]
    
    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()





def unfair_poker_options(game_state):
    """
    Displays the unfair poker options menu which displays buttons for
        - Create game
        - Join game
    """
    menu_text = game_state.font.render("Start Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Game Options") 

    btns = [
        Button(165, 125, 200, 75, "Create Game", lambda: main_game(game_state), image=button_image),
        Button(165, 225, 200, 75, "Join Game", lambda: main_game(game_state), image=button_image),
        back_button(game_state, start_menu)
    ]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()





def bot_options(game_state):
    """
    Displays the bot poker options menu which displays buttons for
        - Easy
        - Advanced
    """
    menu_text = game_state.font.render("Start Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Game Options") 

    btns = [
        Button(165, 125, 200, 75, "Easy", lambda: main_game(game_state), image=button_image),
        Button(165, 225, 200, 75, "Advanced", lambda: main_game(game_state), image=button_image),
        back_button(game_state, start_menu)
    ]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()



# development credits
def credits():
    pass




def chatbox():
    pass







def main_game(game_state):
    """
    Displays the main game menu which displays buttons for
        - 2-6 players
    """

    menu_text = game_state.font.render("Start Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Game Options") 

    btns = [
        Button(165, 125, 200, 75, "2 Players", lambda: poker_game(game_state), image=button_image),
        Button(165, 225, 200, 75, "3 Players", lambda: poker_game(game_state), image=button_image),
        Button(165, 325, 200, 75, "4 Players", lambda: poker_game(game_state), image=button_image),
        Button(165, 425, 200, 75, "5 Players", lambda: poker_game(game_state), image=button_image),
        Button(165, 525, 200, 75, "6 Players", lambda: poker_game(game_state), image=button_image),
        back_button(game_state, start_menu)
    ]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()





def poker_game(game_state):
    """
    Displays the poker game screen with resized card images.
    """

    pygame.display.set_caption("Poker Game")

    # Card dimensions (width, height) after resizing
    card_width, card_height = 60, 90

    # Load and resize card images
    card_images = {
        f"{rank}{suit}": pygame.transform.scale(
            helpers.load_image(f"graphics/cards/{rank}{suit}.png"),
            (card_width, card_height)
        )
        for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for suit in ["H", "D", "C", "S"]
    }

    # Example cards for user and community
    user_cards = ["AH", "KS"]  # Ace of Hearts, King of Spades
    community_cards = ["2D", "3C", "9S", "QD", "10H"]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()

        # Handle events
        for event in pygame.event.get():
            helpers.handle_quit_event(event)

        # Draw user cards
        user_card_x = 50  # Starting x-position for user cards
        user_card_y = game_state.win.get_height() - 150  # Bottom of screen
        card_spacing = card_width + 10  # Space between cards (adjusted for new size)
        for i, card in enumerate(user_cards):
            game_state.win.blit(card_images[card], (user_card_x + i * card_spacing, user_card_y))

        # Draw community cards
        community_card_x = 150  # Starting x-position for community cards
        community_card_y = game_state.win.get_height() // 2 - card_height // 2  # Center vertically
        card_spacing = card_width + 20  # Space between cards (adjusted for new size)
        for i, card in enumerate(community_cards):
            game_state.win.blit(card_images[card], (community_card_x + i * card_spacing, community_card_y))

        # Update the screen
        pygame.display.update()








# from PIL import Image
# import os

# input_folder = "graphics/cards/"
# output_folder = "graphics/cards_resized/"

# # Resize dimensions
# card_width, card_height = 60, 90

# # Resize all images in the folder
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# for filename in os.listdir(input_folder):
#     if filename.endswith(".png"):
#         img = Image.open(os.path.join(input_folder, filename))
#         img = img.resize((card_width, card_height))
#         img.save(os.path.join(output_folder, filename))










# Add sound slider 
# Add sfx slider 
# Mute both / Turn on both
# Themed cards
# Light / Dark theme
# Reset to default




def settings_menu(game_state):
    """
    Displays the settings menu which includes:
        - Music volume slider
        - SFX volume slider
        - Button to return to the main menu
    """
    menu_text = game_state.font.render("Settings Menu", True, (255, 255, 255))#
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Settings Menu")

    btns = [
        back_button(game_state, start_menu)
    ]

    # Default volume (50%)
    default_volume = 50

    # Slider settings
    slider_width = 300
    slider_height = 10
    handle_width = 15
    handle_height = 20
    text_area_height = 40  # Height for clearing the text area

    # Music slider
    music_slider_x = 150
    music_slider_y = 200
    music_handle_x = music_slider_x + int((slider_width - handle_width) * (default_volume / 100))
    music_volume = default_volume
    pygame.mixer.music.set_volume(music_volume / 100)
    music_dragging = False

    # SFX slider
    sfx_slider_x = 150
    sfx_slider_y = 300
    sfx_handle_x = sfx_slider_x + int((slider_width - handle_width) * (default_volume / 100))
    sfx_volume = default_volume
    if hasattr(game_state, "sfx_sounds"):
        for sfx in game_state.sfx_sounds:
            sfx.set_volume(sfx_volume / 100)
    sfx_dragging = False

    
    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)


    

        # Adjusted positioning for text to be right above the sliders
        music_text = game_state.font.render(f"Music Volume: {music_volume}%", True, (255, 255, 255))
        music_text_x = game_state.win.get_width() // 2 - music_text.get_width() // 2  # Centered X position
        game_state.win.blit(music_text, (music_text_x, music_slider_y - 40))

        sfx_text = game_state.font.render(f"SFX Volume: {sfx_volume}%", True, (255, 255, 255))
        sfx_text_x = game_state.win.get_width() // 2 - sfx_text.get_width() // 2  # Centered X position
        game_state.win.blit(sfx_text, (sfx_text_x, sfx_slider_y - 40))

        # Center the sliders below the text
        music_slider_x = game_state.win.get_width() // 2 - slider_width // 2  # Centered X position for the music slider
        sfx_slider_x = game_state.win.get_width() // 2 - slider_width // 2  # Centered X position for the SFX slider

        # Handle positions calculated based on the volume percentages
        music_handle_x = music_slider_x + int((slider_width - handle_width) * (music_volume / 100))  # Center handle at 50% of volume
        sfx_handle_x = sfx_slider_x + int((slider_width - handle_width) * (sfx_volume / 100))  # Center handle at 50% of volume

        # Draw the music slider (background and handle)
        pygame.draw.rect(game_state.win, (200, 200, 200), (music_slider_x, music_slider_y, slider_width, slider_height))
        pygame.draw.rect(game_state.win, (0, 200, 0), (music_handle_x, music_slider_y - (handle_height // 2), handle_width, handle_height))

        # Draw the SFX slider (background and handle)
        pygame.draw.rect(game_state.win, (200, 200, 200), (sfx_slider_x, sfx_slider_y, slider_width, slider_height))
        pygame.draw.rect(game_state.win, (0, 200, 0), (sfx_handle_x, sfx_slider_y - (handle_height // 2), handle_width, handle_height))



        for event in pygame.event.get():
            helpers.handle_quit_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for Music Slider Drag
                if music_handle_x <= event.pos[0] <= music_handle_x + handle_width and \
                   music_slider_y - (handle_height // 2) <= event.pos[1] <= music_slider_y + (handle_height // 2):
                    music_dragging = True

                # Check for SFX Slider Drag
                if sfx_handle_x <= event.pos[0] <= sfx_handle_x + handle_width and \
                   sfx_slider_y - (handle_height // 2) <= event.pos[1] <= sfx_slider_y + (handle_height // 2):
                    sfx_dragging = True

                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

            if event.type == pygame.MOUSEBUTTONUP:
                music_dragging = False
                sfx_dragging = False

            if event.type == pygame.MOUSEMOTION:
                # Adjust Music Slider Handle
                if music_dragging:
                    music_handle_x = max(music_slider_x, min(event.pos[0], music_slider_x + slider_width - handle_width))
                # Adjust SFX Slider Handle
                if sfx_dragging:
                    sfx_handle_x = max(sfx_slider_x, min(event.pos[0], sfx_slider_x + slider_width - handle_width))

        # Update Music Volume
        music_volume = int(((music_handle_x - music_slider_x) / (slider_width - handle_width)) * 100)
        pygame.mixer.music.set_volume(music_volume / 100)

        # Update SFX Volume
        sfx_volume = int(((sfx_handle_x - sfx_slider_x) / (slider_width - handle_width)) * 100)
        if hasattr(game_state, "sfx_sounds"):
            for sfx in game_state.sfx_sounds:
                sfx.set_volume(sfx_volume / 100)

        # Draw buttons
        for btn in btns:
            btn.draw(game_state.win)

        helpers.draw_centered_text(game_state.win, menu_text, 20)

        pygame.display.update()





# Hand rankings
# How to play


def guide_menu(game_state):
    """
    Displays the guide menu 
        - Will display whole guide on how to play
        - Buttons to return to main screen
        - Maybe buttons to go to play section
    """
    menu_text = game_state.font.render("Guide Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    pygame.display.set_caption("Guide Menu") 
    btns = [
        back_button(game_state, start_menu)
    ]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.is_clicked(pygame.mouse.get_pos())  

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()




# Text to speech

# Table:
    # Community Cards: Place for five community cards (flop, turn, river).
    # Player Spots: Place each player's avatar or text (e.g., "Player 1", "Bot 1").
    # Player’s Cards: Two private cards (either face-down or face-up, depending on the stage).
    # Player Stack (Chips): Show total chips the player has in front of their name/slot.


# Action Buttons for Players:
    # Fold: Option to fold the hand.
    # Check: If possible, checking action button.
    # Bet: Open a menu to input the desired bet value.
    # Call: To call the current bet.
    # Raise: To raise the current bet, with input field (or a slider).
    # All-In: Button for going all-in.


# Status Information:
    # Pot: Amount of chips in the pot, displayed at the center or top of the screen.
    # Blinds: Show small blind, big blind, and any ante amounts.
    # Active Player Indicator: Highlighted border or animation around the active player.
    # Turn Timer: A timer showing the remaining time a player has to act.
    # Round Info: Informational text like “Flop Dealt”, “Betting Round 1”, “You Win”.
    # Actions Area (for active players):
    # A fixed section of buttons (check, bet, call, fold, etc.), or these could float near the player’s seat.


# Bot Area:
    # Bot Chips: If playing against bots, a simple icon or label like "Bot 1", "Bot 2".
    # Bot Actions: Bots should either do automated actions like folding, calling, or raising based on predefined AI logic. Display an animation when bots take actions



def table():
    pass