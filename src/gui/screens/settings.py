import pygame, sys
from src.gui.utils.button import Button
from src.gui.utils.constants import BG, screen_font, SCREEN, scaled_cursor, FPS

class Slider:
    def __init__(self, pos, width, initial_value=0.5):
        self.rect = pygame.Rect(pos[0], pos[1], width, 10)
        self.value = initial_value
        self.dragging = False  # Track if the slider is being dragged

    def draw(self, screen):
        pygame.draw.rect(screen, "White", self.rect)
        pygame.draw.rect(
            screen, 
            "Gold", 
            (self.rect.x + self.value * self.rect.width - 5, self.rect.y - 5, 10, 20)
        )

    def update(self, mouse_pos):
        if self.dragging:
            self.value = (mouse_pos[0] - self.rect.x) / self.rect.width
            self.value = max(0, min(self.value, 1))  # Clamp value between 0 and 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

class Dropdown:
    def __init__(self, x, y, w, h, options, font, main_color, hover_color, text_color, visible_options=5):
        """
        options: list of dictionaries, each with keys 'name' and 'path'
        visible_options: number of options to show at once when expanded
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = font
        self.main_color = main_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.active = False  # Is the dropdown expanded?
        self.selected_index = 0  # Index of the current selection
        self.visible_options = visible_options  # How many options to display at once
        self.start_index = 0  # Scrolling offset

        # For middle mouse dragging scrolling
        self.middle_dragging = False
        self.middle_drag_start_y = 0
        self.initial_start_index = 0

    def draw(self, screen):
        # Draw black outline for main dropdown box
        pygame.draw.rect(screen, pygame.Color("Black"), self.rect.inflate(2, 2))
        # Draw the main dropdown box (always visible)
        pygame.draw.rect(screen, self.main_color, self.rect)
        selected_text = self.font.render(self.options[self.selected_index]["name"], True, self.text_color)
        text_rect = selected_text.get_rect(center=self.rect.center)
        screen.blit(selected_text, text_rect)

        # If active, draw only the visible subset of options below the main box
        if self.active:
            for i in range(self.visible_options):
                option_index = self.start_index + i
                if option_index >= len(self.options):
                    break
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.bottom + i * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                # Draw black outline for each option
                pygame.draw.rect(screen, pygame.Color("Black"), option_rect.inflate(2, 2))
                # Change color on hover
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    color = self.hover_color
                else:
                    color = self.main_color
                pygame.draw.rect(screen, color, option_rect)
                option_text = self.font.render(self.options[option_index]["name"], True, self.text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Left click for toggling or selecting options
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                elif self.active:
                    # Check if any visible option was clicked with left button
                    for i in range(self.visible_options):
                        option_index = self.start_index + i
                        if option_index >= len(self.options):
                            break
                        option_rect = pygame.Rect(
                            self.rect.x,
                            self.rect.bottom + i * self.rect.height,
                            self.rect.width,
                            self.rect.height
                        )
                        if option_rect.collidepoint(event.pos):
                            self.selected_index = option_index
                            break
                    # Close the dropdown regardless of click outcome
                    self.active = False

            # Middle mouse button pressed starts dragging for scrolling
            elif event.button == 2:
                if self.active:
                    self.middle_dragging = True
                    self.middle_drag_start_y = event.pos[1]
                    self.initial_start_index = self.start_index

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                self.middle_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.middle_dragging and self.active:
                # Calculate vertical movement to adjust start_index.
                # Each option's height is self.rect.height; moving that many pixels shifts one option.
                dy = event.pos[1] - self.middle_drag_start_y
                shift = int(dy / self.rect.height)
                new_index = self.initial_start_index - shift
                max_start = max(0, len(self.options) - self.visible_options)
                self.start_index = max(0, min(new_index, max_start))

        elif event.type == pygame.MOUSEWHEEL and self.active:
            # Use mouse wheel to scroll the options as well.
            self.start_index -= event.y  # event.y > 0 scrolls up, < 0 scrolls down.
            max_start = max(0, len(self.options) - self.visible_options)
            self.start_index = max(0, min(self.start_index, max_start))

    def get_selected_option(self):
        return self.options[self.selected_index]

def settings(mainMenu):
    music_volume = 0  # Default music volume
    sfx_volume = 0    # Default sound effects volume
    pygame.mixer.music.set_volume(music_volume)  # Set initial music volume

    music_volume_slider = Slider(pos=(0, 0), width=250)
    sfx_volume_slider = Slider(pos=(0, 0), width=250)

    # Define the playlist with 20 songs for the dropdown playlist
    playlist = [
    {"name": "Los Santos", "path": "assets/music/Los Santos.mp3"},
    {"name": "Poker Face", "path": "assets/music/poker_face.wav"},
    {"name": "After Hours", "path": "assets/music/After Hours.mp3"},
    {"name": "Bumpin On Sunset", "path": "assets/music/Bumpin On Sunset.mp3"},
    {"name": "Desafinado", "path": "assets/music/Desafinado.mp3"},
    {"name": "In A Sentimental Mood", "path": "assets/music/In A Sentimental Mood.mp3"},
    {"name": "Lenny", "path": "assets/music/Lenny.mp3"},
    {"name": "Lets Go Gambling", "path": "assets/music/Lets Go Gambling.mp3"},
    {"name": "Manhattan", "path": "assets/music/Manhattan.mp3"},
    {"name": "Midnight Blue", "path": "assets/music/Midnight Blue.mp3"},
    {"name": "Mood Indigo", "path": "assets/music/Mood Indigo.mp3"},
    {"name": "So What", "path": "assets/music/So What.mp3"},
    {"name": "Take Five", "path": "assets/music/Take Five.mp3"},
    {"name": "Sea Shanty", "path": "assets/music/Sea Shanty.mp3"},
    {"name": "Circus Theme", "path": "assets/music/Circus Theme.mp3"}
    ]


    # Create the dropdown menu for songs
    dropdown_font = screen_font(25)
    dropdown_width = 250
    dropdown_height = 40
    # Position it below the sfx slider (adjust as needed)
    dropdown_x = SCREEN.get_width() // 2 + dropdown_width // 4
    dropdown_y = SCREEN.get_height() / 2 - 190  
    song_dropdown = Dropdown(
        dropdown_x, dropdown_y, dropdown_width, dropdown_height,
        playlist, dropdown_font, pygame.Color("White"), pygame.Color("Gold"), pygame.Color("Black"),
        visible_options=5  # Adjust this to how many options you want visible at once
    )

    while True:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        SOUND_MOUSE_POS = pygame.mouse.get_pos()

        # Scale and draw background
        SOUND_width, SOUND_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (SOUND_width, SOUND_height))
        SCREEN.blit(scaled_bg, (0, 0))

        screen_width, screen_height = SCREEN.get_size()
        # Transparent textbox with rounded edges
        textbox_width = int(screen_width * 0.60)
        textbox_height = int(screen_height * 0.7)
        textbox_x = int((screen_width - textbox_width) / 2)
        textbox_y = int(screen_height * 0.15)
    
        textbox_surface = pygame.Surface((textbox_width, textbox_height), pygame.SRCALPHA)
        pygame.draw.rect(
            textbox_surface, 
            (0, 0, 0, 150), 
            (0, 0, textbox_width, textbox_height), 
            border_radius=50
        )
        SCREEN.blit(textbox_surface, (textbox_x, textbox_y))

        # Center sliders
        music_volume_slider.rect.x = SOUND_width / 2.8 - music_volume_slider.rect.width / 2
        music_volume_slider.rect.y = SOUND_height / 3.5
        sfx_volume_slider.rect.x = SOUND_width / 2.8 - sfx_volume_slider.rect.width / 2
        sfx_volume_slider.rect.y = SOUND_height / 2

        # Render slider labels
        music_label = screen_font(30).render("MUSIC VOLUME", True, "White")
        sfx_label = screen_font(30).render("SFX VOLUME", True, "White")
        music_label_rect = music_label.get_rect(center=(SOUND_width / 2.8, music_volume_slider.rect.y - 20))
        sfx_label_rect = sfx_label.get_rect(center=(SOUND_width / 2.8, sfx_volume_slider.rect.y - 20))
        SCREEN.blit(music_label, music_label_rect)
        SCREEN.blit(sfx_label, sfx_label_rect)

        # Render slider percentage texts
        music_percentage = f"{int(music_volume_slider.value * 100)}%"
        sfx_percentage = f"{int(sfx_volume_slider.value * 100)}%"
        music_percentage_label = screen_font(30).render(music_percentage, True, "White")
        sfx_percentage_label = screen_font(30).render(sfx_percentage, True, "White")
        music_percentage_rect = music_percentage_label.get_rect(center=(SOUND_width / 2.8, music_volume_slider.rect.y + 40))
        sfx_percentage_rect = sfx_percentage_label.get_rect(center=(SOUND_width / 2.8, sfx_volume_slider.rect.y + 40))
        SCREEN.blit(music_percentage_label, music_percentage_rect)
        SCREEN.blit(sfx_percentage_label, sfx_percentage_rect)

        # Render main text
        SOUND_TEXT = screen_font(45).render("SETTINGS", True, "Gold")
        SOUND_RECT = SOUND_TEXT.get_rect(center=(SOUND_width / 2, SOUND_height / 8))
        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        # Create a Home button to return to the main menu
        SOUND_BACK = Button(
            pos=(SOUND_width / 2, SOUND_height * 2 / 2.5), 
            text_input="HOME", 
            font=screen_font(30), 
            base_colour="White", 
            hovering_colour="Gold",
            image=None
        )
        SOUND_BACK.changecolour(SOUND_MOUSE_POS)
        SOUND_BACK.update(SCREEN)

        # Draw and update sliders
        music_volume_slider.draw(SCREEN)
        sfx_volume_slider.draw(SCREEN)
        music_volume_slider.update(SOUND_MOUSE_POS)
        sfx_volume_slider.update(SOUND_MOUSE_POS)

        # Update volumes based on slider values
        music_volume = music_volume_slider.value
        sfx_volume = sfx_volume_slider.value
        pygame.mixer.music.set_volume(music_volume)

        # Draw the dropdown for song selection
        song_dropdown.draw(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Home button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SOUND_BACK.checkForInput(SOUND_MOUSE_POS):
                    mainMenu()

            # Handle slider events
            music_volume_slider.handle_event(event)
            sfx_volume_slider.handle_event(event)

            # Handle dropdown events (with updated middle mouse behavior)
            song_dropdown.handle_event(event)
            # When the left mouse button is released, load the newly selected song
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                selected_song = song_dropdown.get_selected_option()
                try:
                    pygame.mixer.music.load(selected_song["path"])
                    pygame.mixer.music.play(-1)  # Loop the song
                except Exception as e:
                    print(f"Error loading {selected_song['path']}: {e}")

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (SOUND_MOUSE_POS[0], SOUND_MOUSE_POS[1]))

        pygame.display.update()
