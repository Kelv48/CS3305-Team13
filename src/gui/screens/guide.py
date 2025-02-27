import os
import sys
import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN as INITIAL_SCREEN, scaled_cursor


def run_guide_screen(title, guide_text, main_menu_callback, beginner_callback, intermediate_callback, advanced_callback):

    screen = INITIAL_SCREEN
    pygame.display.set_caption(title)

    # Absolute path for the theme file
    manager = pygame_gui.UIManager(screen.get_size(), 'assets/embedded_images_theme.json')

    clock = pygame.time.Clock()
    is_running = True

    def create_text_box():
        sw, sh = screen.get_size()
        rect = pygame.Rect(int(sw * 0.1), int(sh * 0.1), int(sw * 0.8), int(sh * 0.75))
        return UITextBox(
            guide_text,
            rect,
            manager=manager,
            object_id=ObjectID(class_id='@text_box', object_id='#text_box')
        )

    def create_buttons():
        sw, sh = screen.get_size()
        y_pos = int(sh * 0.9)

        back_button = Button(
            pos=(sw * 0.2, y_pos),
            text_input="HOME",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)

        beginner_button = Button(
            pos=(sw * 0.4, y_pos),
            text_input="BEGINNER",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)

        intermediate_button = Button(
            pos=(sw * 0.6, y_pos),
            text_input="INTERMEDIATE",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)

        advanced_button = Button(
            pos=(sw * 0.8, y_pos),
            text_input="ADVANCED",
            font=screen_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)

        return back_button, beginner_button, intermediate_button, advanced_button

    text_box = create_text_box()
    back_button, beginner_button, intermediate_button, advanced_button = create_buttons()

    while is_running:
        sw, sh = screen.get_size()
        scaled_bg = pygame.transform.scale(BG, (sw, sh))
        screen.blit(scaled_bg, (0, 0))

        screen_width, screen_height = screen.get_size()
        # Transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.8)      # 80% of screen width
        textbox_height = int(screen_height * 0.1)      # 10% of screen height
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.85)          # 85% down from the top

        # Create a new Surface with per-pixel alpha (using SRCALPHA).
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        # Draw a filled rounded rectangle on the textbox_surface.
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=30
        )
        # Blit the textbox to the main screen.
        INITIAL_SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        title_surface = screen_font(45).render(title, True, "Gold")
        title_rect = title_surface.get_rect(center=(sw / 2, sh / 15))
        screen.blit(title_surface, title_rect)

        # Update button positions
        back_button.pos = (sw * 0.2, int(sh * 0.9))
        beginner_button.pos = (sw * 0.4, int(sh * 0.9))
        intermediate_button.pos = (sw * 0.6, int(sh * 0.9))
        advanced_button.pos = (sw * 0.8, int(sh * 0.9))

        for button in (back_button, beginner_button, intermediate_button, advanced_button):
            button.changecolour(pygame.mouse.get_pos())
            button.update(screen)

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                manager.set_window_resolution((event.w, event.h))
                text_box.kill()
                text_box = create_text_box()
                back_button, beginner_button, intermediate_button, advanced_button = create_buttons()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.checkForInput(mouse_pos):
                    is_running = False
                    main_menu_callback()
                elif beginner_button.checkForInput(mouse_pos):
                    is_running = False
                    beginner_callback()
                elif intermediate_button.checkForInput(mouse_pos):
                    is_running = False
                    intermediate_callback()
                elif advanced_button.checkForInput(mouse_pos):
                    is_running = False
                    advanced_callback()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        # *** Draw the custom cursor last so it’s always on top ***
        current_mouse_pos = pygame.mouse.get_pos()
        INITIAL_SCREEN.blit(scaled_cursor, current_mouse_pos)

        pygame.display.update()


def guide_beginner(main_menu):
    # Beginner guide focuses on the fundamentals with 3 images:
    beginner_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<h2>How to Play Poker – Beginner Guide</h2>'
        '<img src="assets/images/BeginnerOverview.png" style="display:block; margin:0 auto 20px auto;" alt="Beginner Overview">'
        '<p>Learning how to play poker can be quick, easy and fun. The objective of poker is to either create the highest-ranking hand or convince all other players to fold – thereby winning the pot.</p>'
        '<h3>Poker Rules for Beginners: Step-by-Step Guide</h3>'
        '<ol>'
        '<li><b>Shuffle:</b> The dealer shuffles the deck well between every hand. In Texas Hold’em, each player is dealt two hole cards (or more in other variants).'
        '<img src="assets/images/ShuffleCards.png" style="float:left; padding:5px 10px 5px 5px; margin-right:10px;" alt="Shuffle Cards">'
        '</li>'
        '<li><b>Pre-Flop:</b> The initial betting round. Players have the option to call, raise, re-raise, or fold based on the potential of their starting hands.</li>'
        '<li><b>Flop:</b> Three community cards are revealed in the centre of the table. Players now start building their hands.</li>'
        '<li><b>Turn:</b> The fourth community card is dealt face-up, making the strength of your hand clearer.</li>'
        '<li><b>River:</b> The fifth and final community card is placed on the board.</li>'
        '<li><b>Showdown:</b> All remaining players reveal their cards, and the best hand wins the pot.</li>'
        '</ol>'
        '<h3>Types of Plays and Bets</h3>'
        '<img src="assets/images/PokerActions.png" style="float:right; padding:5px 10px 5px 5px; margin-left:10px;" alt="Poker Actions">'
        '<p>Get familiar with the basic actions at the poker table:</p>'
        '<ul>'
        '<li><b>Check:</b> Passing the action without placing a bet.</li>'
        '<li><b>Fold:</b> Discarding your cards when you believe your hand isn’t strong enough.</li>'
        '<li><b>Bet:</b> Placing a wager when no bet has yet been made.</li>'
        '<li><b>Call:</b> Matching an existing bet to continue playing.</li>'
        '<li><b>Raise:</b> Increasing the amount of the current bet.</li>'
        '</ul>'
        '<p>Forced bets such as the small blind (usually 50 percent of the big blind) and the big blind (set amount) are required to encourage action.</p>'
        '<p>For further details on hand strengths, refer to our poker hand rankings guide.</p>'
        '</font>'
    )
    run_guide_screen(
        title="Beginner Poker Guide",
        guide_text=beginner_text,
        main_menu_callback=main_menu,
        beginner_callback=lambda: guide_beginner(main_menu),
        intermediate_callback=lambda: guide_intermediate(main_menu),
        advanced_callback=lambda: guide_advanced(main_menu)
    )


def guide_intermediate(main_menu):
    # Intermediate guide with 3 images focusing on starting hands, pot equity, and matchups:
    intermediate_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<h2>How to Play Poker – Intermediate Guide</h2>'
        '<img src="assets/images/IntermediateOverview.png" style="display:block; margin:0 auto 20px auto;" alt="Intermediate Overview">'
        '<p>After mastering the basics, it’s time to refine your game. In this section, we focus on understanding starting hands, calculating pot equity, and using statistics to improve your decision-making.</p>'
        '<h3>Starting Poker Hands</h3>'
        '<img src="assets/images/StartingHands.png" style="float:left; padding:5px 10px 5px 5px; margin-right:10px;" alt="Starting Hands">'
        '<p>There are many possible starting hand combinations. Some of the key rankings include:</p>'
        '<ul>'
        '<li><b>Royal Flush:</b> A, K, Q, J, 10 of the same suit – the best hand possible.</li>'
        '<li><b>Straight Flush:</b> Five consecutive cards of the same suit.</li>'
        '<li><b>Four of a Kind:</b> Four cards of the same rank.</li>'
        '<li><b>Full House:</b> Three cards of one rank and two cards of another.</li>'
        '<li><b>Flush:</b> Any five cards of the same suit, not in sequence.</li>'
        '<li><b>Straight:</b> Five consecutive cards in mixed suits.</li>'
        '<li><b>Three of a Kind, Two Pair, One Pair, and High Card</b> – in descending order of strength.</li>'
        '</ul>'
        '<h3>Playing Your Hands and Pot Equity</h3>'
        '<img src="assets/images/PotEquity.png" style="float:right; padding:5px 10px 5px 5px; margin-left:10px;" alt="Pot Equity">'
        '<p>Knowing when to play a hand is crucial. Calculate your poker equity – the percentage chance of winning the pot based on your hand and the community cards – to guide your decision to bet or fold.</p>'
        '<h3>Pre-Flop Matchups and Hand Improvements</h3>'
        '<img src="assets/images/MatchupStats.png" style="display:block; margin:20px auto;" alt="Pre-Flop Matchups">'
        '<p>Learn about match-ups such as an overpair versus an underpair and understand the probability of flopping a set (three of a kind) or a full house. Such statistics are essential for determining whether to invest in a hand.</p>'
        '</font>'
    )
    run_guide_screen(
        title="Intermediate Poker Guide",
        guide_text=intermediate_text,
        main_menu_callback=main_menu,
        beginner_callback=lambda: guide_beginner(main_menu),
        intermediate_callback=lambda: guide_intermediate(main_menu),
        advanced_callback=lambda: guide_advanced(main_menu)
    )


def guide_advanced(main_menu):
    # Advanced guide with 4 images on betting strategies, bluffing, and tips:
    advanced_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<h2>How to Play Poker – Advanced Guide</h2>'
        '<img src="assets/images/AdvancedOverview.png" style="display:block; margin:0 auto 20px auto;" alt="Advanced Overview">'
        '<p>For the experienced player, advanced strategies can make all the difference. This section covers sophisticated betting techniques, bluffing, and adjustments for different poker variations.</p>'
        '<h3>Advanced Betting Strategies</h3>'
        '<img src="assets/images/BettingStrategies.png" style="float:left; padding:5px 10px 5px 5px; margin-right:10px;" alt="Betting Strategies">'
        '<p>Improve your game with techniques such as:</p>'
        '<ul>'
        '<li><b>Raising:</b> Increasing the pot size to put pressure on opponents.</li>'
        '<li><b>Check-Raising:</b> Initially checking then raising after an opponent bets, maximizing value when holding a strong hand.</li>'
        '<li><b>Slow Playing:</b> Playing a strong hand deceptively to encourage opponents to commit more chips.</li>'
        '<li><b>Exploitative Betting:</b> Adjusting your strategy to capitalize on predictable patterns in your opponents’ play.</li>'
        '</ul>'
        '<h3>Bluffing Techniques</h3>'
        '<img src="assets/images/BluffingTechniques.png" style="float:right; padding:5px 10px 5px 5px; margin-left:10px;" alt="Bluffing Techniques">'
        '<p>Bluffing is about making bets that force your opponents to fold superior hands. Consider semi-bluffing (betting on a draw) when you have potential to improve your hand.</p>'
        '<h3>Top 10 Poker Tips</h3>'
        '<img src="assets/images/PokerTips.png" style="display:block; margin:20px auto;" alt="Poker Tips">'
        '<ol>'
        '<li>Research and learn the game before playing for money.</li>'
        '<li>Practice with free games to build your skills.</li>'
        '<li>Observe your opponents and note their tendencies.</li>'
        '<li>Keep your table image unpredictable.</li>'
        '<li>Memorize hand rankings and stick to your strategy.</li>'
        '<li>Manage your bankroll carefully.</li>'
        '<li>Don’t overcommit to a weak hand.</li>'
        '<li>Extract maximum value from strong hands.</li>'
        '<li>Play fewer hands but play them aggressively.</li>'
        '<li>Remember: Poker should be fun. Stay calm and focused.</li>'
        '</ol>'
        '</font>'
    )
    run_guide_screen(
        title="Advanced Poker Guide",
        guide_text=advanced_text,
        main_menu_callback=main_menu,
        beginner_callback=lambda: guide_beginner(main_menu),
        intermediate_callback=lambda: guide_intermediate(main_menu),
        advanced_callback=lambda: guide_advanced(main_menu)
    )
