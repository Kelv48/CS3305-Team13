import os
import sys
import pygame
import pygame_gui

from pygame_gui.elements import UITextBox
from pygame_gui.core import ObjectID

from src.gui.button import Button
from src.gui.utils import BG, get_font, SCREEN as INITIAL_SCREEN


def run_guide_screen(title, guide_text, back_callback, next_callback):

    screen = INITIAL_SCREEN
    pygame.display.set_caption(title)

    # Absolute path for the theme file 
    theme_path = os.path.join(os.path.dirname(__file__), 'embedded_images_theme.json')
    manager = pygame_gui.UIManager(screen.get_size(), theme_path)

    clock = pygame.time.Clock()
    is_running = True

    def create_text_box():
        sw, sh = screen.get_size()
        rect = pygame.Rect(10, int(sh * 0.2), sw - 20, int(sh * 0.6))
        return UITextBox(
            guide_text,
            rect,
            manager=manager,
            object_id=ObjectID(class_id='@text_box', object_id='#text_box')
        )

    def create_buttons():
        sw, sh = screen.get_size()
        back_button = Button(
            pos=(sw * 0.25, int(sh * 0.85)),
            text_input="BACK",
            font=get_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)
        next_button = Button(
            pos=(sw * 0.75, int(sh * 0.85)),
            text_input="NEXT",
            font=get_font(30),
            base_colour="White",
            hovering_colour="Light Green",
            image=None)
        return back_button, next_button

    text_box = create_text_box()
    back_button, next_button = create_buttons()

    while is_running:
        # Update screen dimensions and draw the background.
        sw, sh = screen.get_size()
        scaled_bg = pygame.transform.scale(BG, (sw, sh))
        screen.blit(scaled_bg, (0, 0))

        # Draw screen title.
        title_surface = get_font(45).render(title, True, "White")
        title_rect = title_surface.get_rect(center=(sw / 2, sh / 9))
        screen.blit(title_surface, title_rect)

        # Update button positions in case the window has been resized
        back_button.pos = (sw * 0.25, int(sh * 0.85))
        next_button.pos = (sw * 0.75, int(sh * 0.85))
        back_button.changecolour(pygame.mouse.get_pos())
        next_button.changecolour(pygame.mouse.get_pos())
        back_button.update(screen)
        next_button.update(screen)

        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                # Update the display and UI manager resolution.
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                manager.set_window_resolution((event.w, event.h))
                # Recreate the text box and buttons with the new dimensions.
                text_box.kill()
                text_box = create_text_box()
                back_button = Button(
                    pos=(event.w * 0.25, int(event.h * 0.85)),
                    text_input="BACK",
                    font=get_font(30),
                    base_colour="White",
                    hovering_colour="Light Green",
                    image=None)
                next_button = Button(
                    pos=(event.w * 0.75, int(event.h * 0.85)),
                    text_input="NEXT",
                    font=get_font(30),
                    base_colour="White",
                    hovering_colour="Light Green",
                    image=None)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.checkForInput(mouse_pos):
                    is_running = False
                    back_callback()
                elif next_button.checkForInput(mouse_pos):
                    is_running = False
                    next_callback()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


# --- Guide Screens --- #

def guide_beginner(main_menu):
    """Beginner Guide: BACK returns to main_menu, NEXT goes to Intermediate guide."""
    beginner_text = (
        '<font face=calibri_bold size=3 colour=#FFFFFF>'
        '<b>Beginner Poker Guide</b><br><br>'
        'Learn the basics of poker including rules, hand rankings, and simple strategies. '
        'This guide is perfect for those just starting out.'
        '</font>'
    )
    run_guide_screen(
        title="Beginner Poker Guide",
        guide_text=beginner_text,
        back_callback=main_menu,
        next_callback=lambda: guide_intermediate(main_menu)
    )


def guide_intermediate(main_menu):
    """Intermediate Guide: BACK goes back to Beginner, NEXT goes to Advanced."""
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
        back_callback=lambda: guide_beginner(main_menu),
        next_callback=lambda: guide_advanced(main_menu)
    )


def guide_advanced(main_menu):
    """Advanced Guide: BACK goes back to Intermediate, NEXT returns to main_menu."""
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
        back_callback=lambda: guide_intermediate(main_menu),
        next_callback=main_menu
    )
