import pygame, sys
from src.gui.button import Button
from src.gui.constants import BG, get_font, SCREEN

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

def sound(mainMenu):
    music_volume = 0.5  # Default music volume
    sfx_volume = 0.5    # Default sound effects volume
    pygame.mixer.music.set_volume(music_volume)  # Set initial music volume

    music_volume_slider = Slider(pos=(0, 0), width=300)
    sfx_volume_slider = Slider(pos=(0, 0), width=300)

    while True:
        SOUND_MOUSE_POS = pygame.mouse.get_pos()

        # Calculate positions based on current screen size
        SOUND_width, SOUND_height = SCREEN.get_size()
        scaled_bg = pygame.transform.scale(BG, (SOUND_width, SOUND_height))
        SCREEN.blit(scaled_bg, (0, 0))

        # Center sliders
        music_volume_slider.rect.x = SOUND_width / 2 - music_volume_slider.rect.width / 2
        music_volume_slider.rect.y = SOUND_height / 3.5
        sfx_volume_slider.rect.x = SOUND_width / 2 - sfx_volume_slider.rect.width / 2
        sfx_volume_slider.rect.y = SOUND_height / 2

        # Render text for sliders
        music_label = get_font(30).render("Music Volume", True, "White")
        sfx_label = get_font(30).render("Sound Effects Volume", True, "White")
        
        # Position text above sliders
        music_label_rect = music_label.get_rect(center=(SOUND_width / 2, music_volume_slider.rect.y - 20))
        sfx_label_rect = sfx_label.get_rect(center=(SOUND_width / 2, sfx_volume_slider.rect.y - 20))

        SCREEN.blit(music_label, music_label_rect)
        SCREEN.blit(sfx_label, sfx_label_rect)

        # Render percentage text
        music_percentage = f"{int(music_volume_slider.value * 100)}%"
        sfx_percentage = f"{int(sfx_volume_slider.value * 100)}%"
        
        music_percentage_label = get_font(30).render(music_percentage, True, "White")
        sfx_percentage_label = get_font(30).render(sfx_percentage, True, "White")

        # Position percentage text below sliders
        music_percentage_rect = music_percentage_label.get_rect(center=(SOUND_width / 2, music_volume_slider.rect.y + 40))
        sfx_percentage_rect = sfx_percentage_label.get_rect(center=(SOUND_width / 2, sfx_volume_slider.rect.y + 40))

        SCREEN.blit(music_percentage_label, music_percentage_rect)
        SCREEN.blit(sfx_percentage_label, sfx_percentage_rect)

        # Render main text
        SOUND_TEXT = get_font(45).render("This is the SOUND screen.", True, "White")
        SOUND_RECT = SOUND_TEXT.get_rect(center=(SOUND_width / 2, SOUND_height / 8))
        SCREEN.blit(SOUND_TEXT, SOUND_RECT)

        SOUND_BACK = Button(
            pos=(SOUND_width / 2, SOUND_height * 2 / 2.5), 
            text_input="HOME", 
            font=get_font(30), 
            base_colour="White", 
            hovering_colour="Light Green",
            image=None)

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
        pygame.mixer.music.set_volume(music_volume)  # Update music volume
        # Method to set SFX volume
        # set_sfx_volume(sfx_volume) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SOUND_BACK.checkForInput(SOUND_MOUSE_POS):
                    mainMenu()
            # Handle slider events
            music_volume_slider.handle_event(event)
            sfx_volume_slider.handle_event(event)

        pygame.display.update()