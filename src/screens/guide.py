import os
import sys
import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN as INITIAL_SCREEN


def run_guide_screen(title, guide_text, main_menu_callback, beginner_callback, intermediate_callback, advanced_callback):

    screen = INITIAL_SCREEN
    pygame.display.set_caption(title)

    # Absolute path for the theme file
    manager = pygame_gui.UIManager(screen.get_size(), 'src/screens/embedded_images_theme.json')

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
        spacing = sw * 0.2  # Space between buttons
        y_pos = int(sh * 0.9)

        back_button = Button(
            pos=(sw * 0.2, y_pos),
            text_input="BACK",
            font=get_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)


        beginner_button = Button(
            pos=(sw * 0.4, y_pos),
            text_input="BEGINNER",
            font=get_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)


        intermediate_button = Button(
            pos=(sw * 0.6, y_pos),
            text_input="INTERMEDIATE",
            font=get_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)


        advanced_button = Button(
            pos=(sw * 0.8, y_pos),
            text_input="ADVANCED",
            font=get_font(30),
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
        textbox_width = int(screen_width * 0.8)      # 20% of screen width
        textbox_height = int(screen_height * 0.1)      # 70% of screen height
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.85)          # 80% down from the top


        # Create a new Surface with per-pixel alpha (using SRCALPHA).
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        # Draw a filled rounded rectangle on the textbox_surface.
        # The colour (0, 0, 0, 100) is black with an alpha value of 100 (semi-transparent).
        # Adjust the border_radius (here, 20) to control the roundness of the corners.
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 100), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=30
        )
        # Blit the textbox to the main screen.
        INITIAL_SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        title_surface = get_font(45).render(title, True, "White")
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
        pygame.display.update()


# --- Guide Screens --- #

def guide_beginner(main_menu):
    beginner_text = (
        '<font face="noto_sans" size="3" color="#FFFFFF">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        '<img src="src/screens/HandRankings.png"  float:right; padding:5px 10px 5px 5px;">'
        'Some test text in a box that will '
        'This guide is perfect for those just starting out. '
        'Learn the basics of poker including rules, hand rankings, and simple strategies. '
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
        '<font face=calibri_bold size=3 colour=#FFFFFF>'
        '<b>Intermediate Poker Guide</b><br><br>'
        'Build on your fundamentals with topics like betting strategies, bluffing, and reading opponents. '
        'Take your game to the next level with these tips.'
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
        '<font face=calibri_bold size=3 colour=#FFFFFF>'
        '<b>Advanced Poker Guide</b><br><br>'
        'Delve into high-level tactics including pot odds, expected value calculations, '
        'and advanced psychological strategies. Ideal for serious players.'
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
