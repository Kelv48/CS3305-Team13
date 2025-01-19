import pygame
import sys
from UI.button import Button


pygame.init()   #Initialises pygame 
height = 500
width = 500
win = pygame.display.set_mode((width, height))  #Creates game window
pygame.display.set_caption("Poker") 
clock = pygame.time.Clock()                     #Creates instances of clock class 
bgcolour = (255, 255, 255)
font = pygame.font.Font(None, 35)

def startMenu():
    #Renders start up menu 
    #options to play different game modes (normal, unfair poker)
    #options button to adjust volume ??
    menuText = font.render("Start Menu", False, (0,0,0),None)
    btns = [Button(165, 125, 200, 75, "Play Poker", gameOptions), Button(165, 225, 200, 75, "Options", optionsMenu)] #An array containing all the buttons 
    while True:
        global bgcolour
        clock.tick(60)
        win.fill(bgcolour)
        
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
    btns =  btns = [Button(165, 125, 200, 75, "Normal Poker", pokerOptions), Button(165, 225, 200, 75, "Unfair Poker", unfairPokerOptions)]

    while True:
        win.fill(bgcolour)
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
        pygame.display.update()

def optionsMenu():
    #will contain options to adjust game settings
    menuText = font.render("Options Menu", False, (0,0,0))
    while True:
        win.fill(bgcolour)
        win.blit(menuText, (165, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("shutting down")
                sys.exit()
            
            elif event.type == pygame.K_RETURN:    #Return to the previous screen
                print("exit")

        pygame.display.update()

def pokerOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Create Game", main), Button(165, 225, 200, 75, "Join Game", main)]
    while True:
        win.fill(bgcolour)
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
    btns =  btns = [Button(165, 125, 200, 75, "Create Game", main), Button(165, 225, 200, 75, "Join Game", main)]
    while True:
        win.fill(bgcolour)
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
    #Used to display graphics for poker game 
    pass

def pokerRedraw(data=None):
    #Will take data from received from client and draw it 
    #This will most likely be player names, players money and state (folded or not)
    pass



if __name__ == "__main__":
    startMenu()