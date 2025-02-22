import pygame, sys
from src.gui.button import Button
from src.gui.constants import BG, screen_font, SCREEN, screen_font, scaled_cursor

class Slider:
    def __init__(self, pos, width, initial_value=0.5):
        self.rect = pygame.Rect(pos[0], pos[1], width, 10)
        self.value = initial_value
        self.dragging = False  # Track if the slider is being dragged

    def draw(self, screen):
        pygame.draw.rect(screen, "White", self.rect)
        pygame.draw.rect(screen, "Light Green", (self.rect.x + self.value * self.rect.width - 5, self.rect.y - 5, 10, 20))

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
    def __init__(self, x, y, w, h, options, font, main_color, hover_color, text_color):
        """
        options: list of dictionaries, each with keys 'name' and 'path'
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.font = font
        self.main_color = main_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.active = False  # Is the dropdown expanded?
        self.selected_index = 0  # Index of the current selection

        # Pre-create rects for each option (positioned below the main rectangle)
        self.option_rects = []
        for i in range(len(options)):
            option_rect = pygame.Rect(x, y + (i + 1) * h, w, h)
            self.option_rects.append(option_rect)

    def draw(self, screen):
        # Draw the main dropdown box (always visible)
        pygame.draw.rect(screen, self.main_color, self.rect)
        selected_text = self.font.render(self.options[self.selected_index]["name"], True, self.text_color)
        text_rect = selected_text.get_rect(center=self.rect.center)
        screen.blit(selected_text, text_rect)

        # If active, draw all options below
        if self.active:
            for i, option_rect in enumerate(self.option_rects):
                # Change color on hover
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    color = self.hover_color
                else:
                    color = self.main_color
                pygame.draw.rect(screen, color, option_rect)
                option_text = self.font.render(self.options[i]["name"], True, self.text_color)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If clicking the main box, toggle the dropdown
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            elif self.active:
                # Check if any option was clicked
                clicked_option = False
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        clicked_option = True
                        break
                # Close the dropdown whether or not an option was clicked
                self.active = False

    def get_selected_option(self):
        return self.options[self.selected_index]

def sound(mainMenu):
    music_volume = 0.5  # Default music volume
    sfx_volume = 0.5    # Default sound effects volume
    pygame.mixer.music.set_volume(music_volume)  # Set initial music volume

    music_volume_slider = Slider(pos=(0, 0), width=250)
    sfx_volume_slider = Slider(pos=(0, 0), width=250)

    # Define the playlist with song names and file paths
    playlist = [
        {"name": "Song 1", "path": "assets/music/Los Santos.mp3"},
        {"name": "Song 2", "path": "assets/music/poker_face.wav"},
        {"name": "Song 3", "path": "assets/music/Los Santos.mp3"},
    ]

    # Create the dropdown menu for songs
    dropdown_font = screen_font(25)
    dropdown_width = 250
    dropdown_height = 40
    # Position it below the sfx slider (adjust as needed)
    dropdown_x = SCREEN.get_width() // 2 - dropdown_width // 2
    dropdown_y = SCREEN.get_height() / 2 + 80  
    song_dropdown = Dropdown(
        dropdown_x, dropdown_y, dropdown_width, dropdown_height,
        playlist, dropdown_font, pygame.Color("White"), pygame.Color("LightGreen"), pygame.Color("Black")
    )

    while True:
        SOUND_MOUSE_POS = pygame.mouse.get_pos()

        # Scale and draw background
        SOUND_width, SOUND_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (SOUND_width, SOUND_height))
        SCREEN.blit(scaled_bg, (0, 0))

        screen_width, screen_height = SCREEN.get_size()
        # Transparent textbox with rounded edges
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

        # Center sliders
        music_volume_slider.rect.x = SOUND_width / 2 - music_volume_slider.rect.width / 2
        music_volume_slider.rect.y = SOUND_height / 3.5
        sfx_volume_slider.rect.x = SOUND_width / 2 - sfx_volume_slider.rect.width / 2
        sfx_volume_slider.rect.y = SOUND_height / 2

        # Render slider labels
        music_label = screen_font(30).render("Music Volume", True, "White")
        sfx_label = screen_font(30).render("Sound Effects Volume", True, "White")
        music_label_rect = music_label.get_rect(center=(SOUND_width / 2, music_volume_slider.rect.y - 20))
        sfx_label_rect = sfx_label.get_rect(center=(SOUND_width / 2, sfx_volume_slider.rect.y - 20))
        SCREEN.blit(music_label, music_label_rect)
        SCREEN.blit(sfx_label, sfx_label_rect)

        # Render slider percentage texts
        music_percentage = f"{int(music_volume_slider.value * 100)}%"
        sfx_percentage = f"{int(sfx_volume_slider.value * 100)}%"
        music_percentage_label = screen_font(30).render(music_percentage, True, "White")
        sfx_percentage_label = screen_font(30).render(sfx_percentage, True, "White")
        music_percentage_rect = music_percentage_label.get_rect(center=(SOUND_width / 2, music_volume_slider.rect.y + 40))
        sfx_percentage_rect = sfx_percentage_label.get_rect(center=(SOUND_width / 2, sfx_volume_slider.rect.y + 40))
        SCREEN.blit(music_percentage_label, music_percentage_rect)
        SCREEN.blit(sfx_percentage_label, sfx_percentage_rect)

        # Render main text
        SOUND_TEXT = screen_font(45).render("This is the SOUND screen.", True, "White")
        SOUND_RECT = SOUND_TEXT.get_rect(center=(SOUND_width / 2, SOUND_height / 8))
        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        # Create a Home button to return to the main menu
        SOUND_BACK = Button(
            pos=(SOUND_width / 2, SOUND_height * 2 / 2.5), 
            text_input="HOME", 
            font=screen_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
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

        # # Draw the dropdown for song selection
        # song_dropdown.draw(SCREEN)

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

            # Handle dropdown events
            song_dropdown.handle_event(event)
            # When the mouse button is released, load the newly selected song
            if event.type == pygame.MOUSEBUTTONUP:
                selected_song = song_dropdown.get_selected_option()
                try:
                    pygame.mixer.music.load(selected_song["path"])
                    pygame.mixer.music.play(-1)  # Loop the song
                except Exception as e:
                    print(f"Error loading {selected_song['path']}: {e}")

        # Draw the scaled cursor image at the mouse position
        SCREEN.blit(scaled_cursor, (SOUND_MOUSE_POS[0], SOUND_MOUSE_POS[1]))

        pygame.display.update()
