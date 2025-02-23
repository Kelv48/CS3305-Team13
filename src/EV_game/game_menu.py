import pygame, sys
import pygame.transform
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, FPS
from src.singleplayer_game.game_gui.utils import changePlayersPositions
from src.singleplayer_game.game_gui.player import Player
from src.singleplayer_game.poker_round import poker_round

def gameMenuEV(mainMenu):
    screen_width = 1280
    screen_height = 720
    START_STACK = 5000
    pygame.init()
    clock = pygame.time.Clock()
    home_button_rect = pygame.Rect(10, 10, 150, 50)
    while True:
        Player.player_list_chair.clear()
        start_choice = menuStart(mainMenu)
        if start_choice == "HOME":
            mainMenu()
            return
        if start_choice == "EV":
            expectedValueGame(mainMenu)
            return
        Player('Player 1', START_STACK, 'human')
        for i in range(start_choice):
            Player(f'Bot {i+1}', START_STACK, 'AI')
        game_running = True
        while game_running and len(Player.player_list_chair) > 1:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_button_rect.collidepoint(event.pos):
                        mainMenu()
                        return
            poker_round()
            for player in Player.player_list_chair:
                player.nextRound()
            for player in Player.player_list_chair[:]:
                if player.stack == 0:
                    rebuy = menuEnd(mainMenu)
                    if rebuy:
                        for p in Player.player_list_chair:
                            p.stack = START_STACK
                    else:
                        Player.player_list_chair.remove(player)
            if len(Player.player_list_chair) == 1:
                game_running = False
        restart = menuEnd(mainMenu)
        if not restart:
            mainMenu()
            return

def menuStart(mainMenu):
    screen_width = 1280
    screen_height = 720
    while True:
        mouse_pos = pygame.mouse.get_pos()
        scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
        SCREEN.blit(scaled_bg, (0, 0))
        textbox_width = int(screen_width * 0.25)
        textbox_height = int(screen_height * 0.7)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.15)
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))
        title_text = screen_font(45).render("This is the GAME START screen.", True, "White")
        title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 8))
        SCREEN.blit(title_text, title_rect)
        buttons = [
            ("EV Game", "EV"),
            ("1 Bot", 1),
            ("2 Bots", 2),
            ("3 Bots", 3),
            ("4 Bots", 4),
            ("5 Bots", 5),
            ("HOME", mainMenu)
        ]
        button_objects = []
        button_spacing = textbox_height / (len(buttons) + 0.5)
        textbox_center_x = textbox_x + textbox_width / 2
        for index, (text, action) in enumerate(buttons):
            button_y = (index + 2) * button_spacing
            button_obj = Button(
                pos=(textbox_center_x, button_y),
                text_input=text,
                font=screen_font(30),
                base_colour="White",
                hovering_colour="Light Green",
                image=None
            )
            button_obj.changecolour(mouse_pos)
            button_obj.update(SCREEN)
            button_objects.append((button_obj, action))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainMenu()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_obj, action in button_objects:
                    if button_obj.checkForInput(mouse_pos):
                        if action == "quit":
                            mainMenu()
                            return "quit"
                        else:
                            return action
        pygame.display.update()

def menuEnd(mainMenu, ev_results=None, final_ev=None):
    from src.singleplayer_game.game_gui.player import Player
    screen_width = 1280
    screen_height = 720
    # Determine the winner from the human (or any remaining player)
    winner = next((player.name for player in Player.player_list_chair if player.stack != 0), "No Winner")
    scaled_bg = pygame.transform.scale(BG, (screen_width, screen_height))
    SCREEN.blit(scaled_bg, (0, 0))
    font = screen_font(60)
    win_text = font.render(f'{winner} won the game!', True, "White")
    SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))
    
    if ev_results is not None:
        font_ev = screen_font(30)
        y_offset = 200
        # Display each round's EV outcome
        for i, ev in enumerate(ev_results, start=1):
            color = (0, 255, 0) if ev >= 0 else (255, 0, 0)
            ev_text = font_ev.render(f"Round {i} EV: {ev:+.2f}", True, color)
            SCREEN.blit(ev_text, (50, y_offset))
            y_offset += ev_text.get_height() + 5
        # Display the final EV outcome
        total_color = (0, 255, 0) if final_ev >= 0 else (255, 0, 0)
        total_text = font_ev.render(f"Final EV: {final_ev:+.2f}", True, total_color)
        SCREEN.blit(total_text, (50, y_offset))
    
    button_new_game = Button(
        pos=(screen_width / 2, 300),
        text_input="NEW GAME",
        font=screen_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None
    )
    button_exit = Button(
        pos=(screen_width / 2, 500),
        text_input="HOME",
        font=screen_font(30),
        base_colour="White",
        hovering_colour="Light Green",
        image=None
    )
    restart = False    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(scaled_bg, (0, 0))
        SCREEN.blit(win_text, ((screen_width - win_text.get_width()) // 2, 100))
        if ev_results is not None:
            y_offset = 200
            for i, ev in enumerate(ev_results, start=1):
                color = (0, 255, 0) if ev >= 0 else (255, 0, 0)
                ev_text = font_ev.render(f"Round {i} EV: {ev:+.2f}", True, color)
                SCREEN.blit(ev_text, (50, y_offset))
                y_offset += ev_text.get_height() + 5
            total_color = (0, 255, 0) if final_ev >= 0 else (255, 0, 0)
            total_text = font_ev.render(f"Final EV: {final_ev:+.2f}", True, total_color)
            SCREEN.blit(total_text, (50, y_offset))
        button_new_game.changecolour(mouse_pos)
        button_new_game.update(SCREEN)
        button_exit.changecolour(mouse_pos)
        button_exit.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainMenu()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.checkForInput(mouse_pos):
                    restart = True
                    waiting = False
                if button_exit.checkForInput(mouse_pos):
                    mainMenu()
                    return False
        pygame.display.update()
    return restart
def expectedValueGame(mainMenu):
    from src.singleplayer_game.game_gui.player import Player
    START_STACK = 5000
    import random
    from src.EV_game.poker_round import ev_round

    ev_results = []  # Store each round's EV outcome

    # Preserve the human player's chip stack if it exists; otherwise create a new one.
    if Player.player_list_chair and Player.player_list_chair[0].kind == 'human':
        human = Player.player_list_chair[0]
    else:
        Player.player_list_chair.clear()
        human = Player('Player 1', START_STACK, 'human')

    # Run 10 rounds, re-randomize bots each round.
    for round_number in range(1, 11):
        # Keep only the human; remove previous bots.
        Player.player_list_chair = [human]
        # Randomly generate between 2 and 5 bots for this round.
        num_bots = random.randint(2, 5)
        for i in range(num_bots):
            Player(f'Bot {i+1}', START_STACK, 'AI')
        # Run the EV round and save the EV result.
        result = ev_round(round_number)
        ev_results.append(result)
        human.nextRound()

    final_ev = sum(ev_results)
    restart = menuEnd(mainMenu, ev_results, final_ev)
    if restart:
        expectedValueGame(mainMenu)
    else:
        mainMenu()