class Button:
    def __init__(self, pos, text_input, font, base_colour, hovering_colour, image=None):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_colour = base_colour
        self.hovering_colour = hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_colour)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.image = image

        # If an image is provided, get its rect and center it on the button position.
        if self.image is not None:
            self.image_rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def checkForInput(self, position):
        return self.rect.collidepoint(position)
  
    def update(self, screen):
        """Draws the button on the screen."""
        # If an image is provided, draw it first (so it appears underneath the text).
        if self.image is not None:
            screen.blit(self.image, self.image_rect)
        # Then draw the text.
        screen.blit(self.text, self.rect)
    
    def changecolour(self, position):
        """Changes the button's text colour based on whether the mouse is hovering over it."""
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)
