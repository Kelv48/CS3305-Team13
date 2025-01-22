
    
""" The main function to initialize the game and start the main loop """
    

import pygame
from src.gui.game_state import GameState
from src.gui.screens.menus import start_menu

def main():
    pygame.init()
    pygame.display.set_caption("Poker Showdown!")
    game_state = GameState()
    game_state.current_screen = start_menu

    while True:
        game_state.current_screen(game_state)
        pygame.display.update()

if __name__ == "__main__":
    main()




