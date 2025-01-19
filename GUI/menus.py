
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


def start_menu(game_state):
    """
    Displays start menu which displays buttons for
        - Play
        - Setting
        - Guide
    Handles button clicks and toggles fullscreen mode when ESC is pressed
    """
    menu_text = game_state.font.render("Start Menu", False, (0, 0, 0), None)
    button_image = helpers.load_image('graphics/buttons/greenButton.png')
    
    btns = [
        Button(0, 0, 200, 75, "Play", lambda: game_options(game_state), image=button_image),
        Button(0, 0, 200, 75, "Settings", lambda: settings_menu(game_state)),
        Button(0, 0, 200, 75, "Guide", lambda: guide_menu(game_state))
    ]

    while True:
        game_state.clock.tick(60)
        game_state.draw_background()
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()






def game_options(game_state):
    """
    Displays game options menu which displays buttons for
        - Fair poker
        - Unfair poker
        - Bots
    """
    menu_text = game_state.font.render("Pick a mode", False, (0, 0, 0))
    btns = [
        Button(165, 125, 200, 75, "Normal Poker", lambda: poker_options(game_state)),
        Button(165, 225, 200, 75, "Unfair Poker", lambda: unfair_poker_options(game_state)),
        Button(165, 325, 200, 75, "Bots", lambda: bot_options(game_state))
    ]
    
    background_image = helpers.load_image('graphics/images/background.png')
    pygame.display.set_caption("Game Options") 
    
    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()






def settings_menu(game_state):
    """
    Displays the settings menu which displays buttons for
        - Sound button
        - Buttons to return to main screen
        - ETC - MORE FEATURS
    """
    menu_text = game_state.font.render("Options Menu", False, (0, 0, 0))
    background_image = helpers.load_image('graphics/images/background.png')

    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state.current_screen = start_menu
                return

        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()






def guide_menu(game_state):
    """
    Displays the guide menu 
        - Will display whole guide on how to play
        - Buttons to return to main screen
        - Maybe buttons to go to play section
    """
    menu_text = game_state.font.render("Guide Menu", False, (0, 0, 0))
    background_image = helpers.load_image('graphics/images/background.png')

    while True:
        game_state.clock.tick(60)
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state.current_screen = start_menu
                return

        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()





def poker_options(game_state):
    """
    Displays the poker options menu which displays buttons for
        - Create game
        - Join game
    """
    menu_text = game_state.font.render("Pick a mode", False, (0, 0, 0))
    btns = [
        Button(165, 125, 200, 75, "Create Game", lambda: main_game(game_state)),
        Button(165, 225, 200, 75, "Join Game", lambda: main_game(game_state))
    ]
    
    background_image = helpers.load_image('graphics/images/background.png')
    
    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

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
    menu_text = game_state.font.render("Pick a mode", False, (0, 0, 0))
    btns = [
        Button(165, 125, 200, 75, "Create Game", lambda: main_game(game_state)),
        Button(165, 225, 200, 75, "Join Game", lambda: main_game(game_state))
    ]

    background_image = helpers.load_image('graphics/images/background.png')

    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

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
    menu_text = game_state.font.render("Pick a mode", False, (0, 0, 0))
    btns = [
        Button(165, 125, 200, 75, "Easy", lambda: main_game(game_state)),
        Button(165, 225, 200, 75, "Advanced", lambda: main_game(game_state))
    ]

    background_image = helpers.load_image('graphics/images/background.png')

    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()





def main_game(game_state):
    """
    Displays the main game menu which displays buttons for
        - 2-6 players
    """
    menu_text = game_state.font.render("Pick a mode", False, (0, 0, 0))
    btns = [
        Button(165, 125, 200, 75, "2 Players", lambda: poker_redraw()),
        Button(165, 225, 200, 75, "3 Players", lambda: poker_redraw()),
        Button(165, 325, 200, 75, "4 Players", lambda: poker_redraw()),
        Button(165, 425, 200, 75, "5 Players", lambda: poker_redraw()),
        Button(165, 525, 200, 75, "6 Players", lambda: poker_redraw())
    ]

    background_image = helpers.load_image('graphics/images/background.png')

    while True:
        game_state.clock.tick(60)
        game_state.win.fill(BG_COLOUR)
        game_state.win.blit(menu_text, (165, 20))
        background_image_scaled = pygame.transform.scale(background_image, (game_state.win.get_width(), game_state.win.get_height()))
        game_state.win.blit(background_image_scaled, (0, 0))
        helpers.center_buttons(game_state.win, btns)

        for event in pygame.event.get():
            helpers.handle_quit_event(event)

        for btn in btns:
            btn.draw(game_state.win)
        helpers.draw_centered_text(game_state.win, menu_text, 20)
        pygame.display.update()