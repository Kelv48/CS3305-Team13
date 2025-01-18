import pygame

class Button():
    def __init__(self, x, y, width, height, text, onclickFunction, font=None, fontSize=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclick = onclickFunction
        
        self.font = pygame.font.Font(font, fontSize)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(self.text, False, (0,0,0), (255, 255, 255))

    def draw(self, win):
        #Used to redraw the button each frame
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        win.blit(self.buttonSurface, self.buttonRect)

    def clicked(self, pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height:
            print("I've been clicked")
            self.onclick()
        
        else:
            return False