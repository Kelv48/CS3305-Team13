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

        title_surface = screen_font(45).render(title, True, "White")
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
    beginner_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<img src="assets/images/HandRankings.png" '
                     'float=right '
                     'padding="5px 10px 5px 5px">'
        '<h2>Beginner Poker Guide</h2>'
        '<p><b>Overview:</b> This guide is designed for players who are new to poker. It covers the basics, including rules, hand rankings, and simple strategies.</p>'
        '<p><b>Key Topics:</b></p>'
        '<ul>'
        '<li><b>Poker Basics & Rules:</b> Learn the common rules of popular variants like Texas Hold’em, including betting rounds, blinds, and game flow.</li>'
        '<li><b>Hand Rankings:</b> Understand the hierarchy of hands—from high card to royal flush—with visual aids to help you remember.</li>'
        '<li><b>Basic Terminology:</b> Get familiar with essential poker terms like call, raise, fold, bluff, and pot odds.</li>'
        '<li><b>Simple Strategies:</b> Start with fundamentals such as playing tight, understanding position, and knowing when to fold.</li>'
        '<li><b>Practical Examples:</b> Walk through sample hands to learn decision-making at various stages of a game.</li>'
        '</ul>'
        '<p>Additional tips: observe experienced players, practice in low-stakes games, and use free online tutorials for extra help.</p>'
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
    intermediate_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<h2>Intermediate Poker Guide</h2>'
        '<p><b>Overview:</b> This guide helps you refine your skills and dive into more nuanced poker strategies beyond the basics.</p>'
        '<p><b>Key Topics:</b></p>'
        '<ul>'
        '<li><b>Advanced Betting Strategies:</b> Learn when to bet, raise, or fold based on your hand, table position, and opponent behavior.</li>'
        '<li><b>Bluffing & Reading Opponents:</b> Develop techniques for effective bluffing and for interpreting betting patterns and tells.</li>'
        '<li><b>Positional Awareness:</b> Understand the advantages of acting later in a hand and how to use that information to your benefit.</li>'
        '<li><b>Introduction to Pot Odds:</b> Start calculating pot odds to make more informed decisions regarding calls and raises.</li>'
        '<li><b>Game Dynamics:</b> Learn how different formats—cash games versus tournaments—and varying stack sizes affect your strategy.</li>'
        '</ul>'
        '<p>Enhance your learning with interactive scenarios, hand analysis, and simulated practice rounds.</p>'
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
    advanced_text = (
        '<font face="calibri_bold" size="3" color="#FFFFFF">'
        '<h2>Advanced Poker Guide</h2>'
        '<p><b>Overview:</b> For experienced players, this guide delves into high-level tactics including mathematical analysis, game theory, and psychological strategies.</p>'
        '<p><b>Key Topics:</b></p>'
        '<ul>'
        '<li><b>Mathematical Foundations:</b> Understand expected value (EV) calculations, variance, and risk management for long-term success.</li>'
        '<li><b>Game Theory Optimal (GTO) Play:</b> Learn strategies to make your play unexploitable, striking a balance between exploitative and GTO approaches.</li>'
        '<li><b>Advanced Bluffing Techniques:</b> Master semi-bluffs and refine the timing of your bluffs for maximum effect.</li>'
        '<li><b>Psychological Strategies:</b> Develop mental toughness, manage tilt, and exploit opponents’ psychological weaknesses.</li>'
        '<li><b>Range Analysis & Bet Sizing:</b> Hone your ability to assign plausible hand ranges to opponents and choose optimal bet sizes.</li>'
        '<li><b>Tournament vs. Cash Game Nuances:</b> Understand the strategic adjustments required for tournament play versus cash games.</li>'
        '</ul>'
        '<p>Utilize in-depth case studies, detailed hand histories, and simulation tools to further refine your advanced tactics.</p>'
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
