





# # import ctypes
# import pygame
# import sys
# from settings import *


# # Ensure correct DPI handling in Windows to prevent display scaling issues
# # ctypes.windll.user32.SetProcessDPIAware()

# class Game:
#     def __init__(self):
#         # General setup
#         pygame.init()
#         pygame.display.set_caption("Poker :)")
#         self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
#         self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
#         self.clock = pygame.time.Clock()
#         self.fullscreen = False

#         # Load resources
#         self.card_img = pygame.image.load('cards.png').convert()
#         self.card_img = pygame.transform.scale(
#             self.card_img,
#             (self.card_img.get_width() * 2, self.card_img.get_height() * 2)
#         )
#         # Mouse click sound effects
#         self.card_img.set_colorkey((0, 0, 0))
#         self.chips_sound = pygame.mixer.Sound('chips.mp3')

#         # Initialize and play background music
#         pygame.mixer.music.load('poker_face.wav')  # Replace with your music file path
#         pygame.mixer.music.play(-1)  # Loop the music indefinitely

#         # Game state
#         self.mouse_down = False




#     def toggle_fullscreen(self):
#         """Toggle between fullscreen and resizable window."""
#         self.fullscreen = not self.fullscreen
#         if self.fullscreen:
#             self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
#         else:
#             self.screen = pygame.display.set_mode((self.screen.get_width(), self.screen.get_height()), pygame.RESIZABLE)

#     def run(self):
#         while True:
#             self.screen.fill(BG_COLOUR)

#             # Draw red rectangle at the top-right corner
#             pygame.draw.rect(
#                 self.screen,
#                 (255, 0, 0),
#                 pygame.Rect(
#                     self.screen.get_width() - 5 - (self.screen.get_width() / 5), 
#                     50, 
#                     self.screen.get_width() / 5, 
#                     50
#                 )
#             )

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#                 if event.type == pygame.VIDEORESIZE:
#                     if not self.fullscreen:
#                         self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE:
#                         pygame.quit()
#                         sys.exit()
#                     if event.key == pygame.K_f:
#                         self.toggle_fullscreen()

#                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     self.mouse_down = True
#                     self.chips_sound.play()  # Play sound on left mouse click

#                 if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                     if self.mouse_down:
#                         self.mouse_down = False

#             # Render game content
#             self.screen.blit(self.card_img, (100, 100))  # Example position
#             pygame.display.update()
#             self.clock.tick(60)

# if __name__ == '__main__':
#     game = Game()
#     game.run()






















import pygame
import sys
from button import *
from settings import *


pygame.init()   #Initializes pygame 
win = pygame.display.set_mode((WIDTH, HEIGHT))  #Creates game window
pygame.display.set_caption("Poker :)") 
clock = pygame.time.Clock()                     #Creates instances of clock class 

font = pygame.font.Font(None, 35)




monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
fullscreen = False

# Load resources
# card_img = pygame.image.load('./graphics/images/cards.png').convert()
# card_img = pygame.transform.scale(
#     card_img,
#     (card_img.get_width() * 2, card_img.get_height() * 2)
# )
# # Mouse click sound effects
# card_img.set_colorkey((0, 0, 0))
chips_sound = pygame.mixer.Sound('./audio/chips.mp3')

# Initialize and play background music
pygame.mixer.music.load('./audio/poker_face.wav')  # Replace with your music file path
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Game state
mouse_down = False







def toggle_fullscreen():
        """Toggle between fullscreen and resizable window."""
        fullscreen = not fullscreen
        if fullscreen:
            screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)


def startMenu():

    #Renders start up menu 
    #options to play different game modes (normal, unfair poker)
    #options button to adjust volume ??
    menuText = font.render("Start Menu", False, (0,0,0),None)
    btns = [Button(165, 125, 200, 75, "Play Poker", gameOptions), 
            Button(165, 225, 200, 75, "Settings", settingsMenu),
            Button(165, 325, 200, 75, "Guide Page", guidePage)] #An array containing all the buttons 
    

    while True:
        global BG_COLOUR
        clock.tick(60)
        win.fill(BG_COLOUR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:  #If mouse is clicked 
               
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos()) #Checks each button if it has been pressed
            
        for btn in btns:
            btn.draw(win)        

        win.blit(menuText, (165, 20))
        pygame.display.update()




def gameOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Normal Poker", pokerOptions), 
                    Button(165, 225, 200, 75, "Unfair Poker", unfairPokerOptions),
                    Button(165, 325, 200, 75, "Bots", botOptions)]
    while True:
        screen.fill(BG_COLOUR)
        # win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()


            elif event.type == pygame.MOUSEBUTTONDOWN:  #If mouse is clicked 
               
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos()) #Checks each button if it has been pressed
            
            for btn in btns:
                btn.draw(win)            

        for btn in btns:
            btn.draw(win)       
        pygame.display.update()





def settingsMenu():
    # Will contain options to adjust game settings
    menuText = font.render("Options Menu", False, (0,0,0))
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()
            
            elif event.type == pygame.K_RETURN:    #Return to the previous screen
                print("exit")

                return

        pygame.display.update()



def guidePage():
    # Will contain options to adjust game settings
    menuText = font.render("Options Menu", False, (0,0,0))
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()
            
            elif event.type == pygame.K_RETURN:    #Return to the previous screen
                print("exit")

                return

        pygame.display.update()






def pokerOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Create Game", main), 
                    Button(165, 225, 200, 75, "Join Game", main)]
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()

        for btn in btns:
            btn.draw(win)
        pygame.display.update()
    


def unfairPokerOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Create Game", main), 
                    Button(165, 225, 200, 75, "Join Game", main)]
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()

        for btn in btns:
            btn.draw(win)
        pygame.display.update()
    




def botOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Easy", main), 
                    Button(165, 225, 200, 75, "Advanced", main)]
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()

        for btn in btns:
            btn.draw(win)
        pygame.display.update()
    















def main():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Table", main), 
                    Button(165, 225, 200, 75, "Table2", main)]
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()

        for btn in btns:
            btn.draw(win)
        pygame.display.update()











def pokerRedraw(data=None):
    #Will take data from received from client and draw it 
    #This will most likely be player names, players money and state (folded or not)
    pass










if __name__ == "__main__":
    startMenu()