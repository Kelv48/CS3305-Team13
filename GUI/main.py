
    
""" The main function to initialize the game and start the main loop """
    

import pygame
from game_state import GameState
from menus import start_menu

def main():
    pygame.init()
    game_state = GameState()
    game_state.current_screen = start_menu # Set initial screen as start menu

    while True:
        game_state.current_screen(game_state)
        pygame.display.update()

if __name__ == "__main__":
    main()  





