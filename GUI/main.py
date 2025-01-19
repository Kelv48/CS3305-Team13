import pygame
import sys
from GUI.buttons import *
from settings import *

# # Ensure correct DPI handling in Windows to prevent display scaling issues
# # ctypes.windll.user32.SetProcessDPIAware()


pygame.init()   #Initializes pygame 
win = pygame.display.set_mode((WIDTH, HEIGHT))  #Creates game window
pygame.display.set_caption("Poker :)") 
clock = pygame.time.Clock()                     #Creates instances of clock class 

font = pygame.font.Font(None, 35)



monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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
# pygame.mixer.music.load('./audio/poker_face.wav')  # Replace with your music file path
# pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Game state
mouse_down = False




def toggle_fullscreen():
    """Toggle between fullscreen and resizable window."""
    global fullscreen, win
    fullscreen = not fullscreen
    if fullscreen:
        win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
    else:
        win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


def startMenu():
    menuText = font.render("Start Menu", False, (0, 0, 0), None)

    button_image = pygame.image.load('graphics/buttons/greenButton.png')
    
    btns = [
        Button(0, 0, 200, 75, "Play", gameOptions, image=button_image),
        Button(0, 0, 200, 75, "Settings", settingsMenu),
        Button(0, 0, 200, 75, "Guide Page", guidePage)
    ]

    


    # Load and scale the background image to the current screen size
    background_image = pygame.image.load('graphics/images/background.png')

    while True:
        clock.tick(60)

        # Scale the background image to fit the screen
        background_image_scaled = pygame.transform.scale(background_image, (win.get_width(), win.get_height()))
        win.blit(background_image_scaled, (0, 0))  # Draw the scaled background image

        # Calculate the center of the screen
        screen_center_x = win.get_width() // 2
        screen_center_y = win.get_height() // 2

        # Position buttons so they're centered on the screen
        btn_spacing = 20  # Vertical space between buttons
        btn_width = 200
        btn_height = 75

        # Center the buttons dynamically by calculating positions
        for i, btn in enumerate(btns):
            # Calculate X position for horizontal centering
            btn_x = screen_center_x - btn_width // 2  
            # Calculate Y position for vertical distribution, ensuring it's centered
            btn_y = screen_center_y - (len(btns) * btn_height // 2) + i * (btn_height + btn_spacing)  
            
            # Set the position of each button using set_position()
            btn.set_position(btn_x, btn_y)

        # Check for events (quitting, mouse clicks, key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Shutting down")
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    toggle_fullscreen()

        # Draw the buttons
        for btn in btns:
            btn.draw(win)

        # Draw the menu title at the top center
        win.blit(menuText, (screen_center_x - menuText.get_width() // 2, 20))  # Centered

        # Update the window display
        pygame.display.update()







def gameOptions():
    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Normal Poker", pokerOptions), 
                    Button(165, 225, 200, 75, "Unfair Poker", unfairPokerOptions),
                    Button(165, 325, 200, 75, "Bots", botOptions)
                    ]
    
    background_image = pygame.image.load('graphics/images/background.png')
    pygame.display.set_caption("game options") 
    
    while True:
        win.fill(BG_COLOUR)
        win.blit(menuText, (165, 20))

        background_image_scaled = pygame.transform.scale(background_image, (win.get_width(), win.get_height()))
        win.blit(background_image_scaled, (0, 0))  # Draw the scaled background image
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

    background_image = pygame.image.load('graphics/images/background.png')

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

    background_image = pygame.image.load('graphics/images/background.png')
    
    # Will contain options to adjust game settings
    menuText = font.render("Options Menu", False, (0,0,0))
    while True:

        background_image_scaled = pygame.transform.scale(background_image, (win.get_width(), win.get_height()))
        win.blit(background_image_scaled, (0, 0))  # Draw the scaled background image

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
    
    background_image = pygame.image.load('graphics/images/background.png')
    
    while True:
        win.fill(BG_COLOUR)
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
    








def unfairPokerOptions():

    background_image = pygame.image.load('graphics/images/background.png')

    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "Create Game", main), 
                    Button(165, 225, 200, 75, "Join Game", main)
    ]

    while True:
        win.fill(BG_COLOUR)
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
    




def botOptions():

    background_image = pygame.image.load('graphics/images/background.png')

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

            elif event.type == pygame.MOUSEBUTTONDOWN:  #If mouse is clicked 
               
                for btn in btns:
                    btn.clicked(pygame.mouse.get_pos()) #Checks each button if it has been pressed
            
            for btn in btns:
                btn.draw(win)   

        for btn in btns:
            btn.draw(win)
        pygame.display.update()
    
    
# Join - Game - enter code - sends back msg either full or join game

# Create game
# 2-6 people text box







def main():

    background_image = pygame.image.load('graphics/images/background.png')

    #Used to create and join games when user selects game mode
    menuText = font.render("Pick a mode", False, (0,0,0))
    btns =  btns = [Button(165, 125, 200, 75, "2 Players", main), 
                    Button(165, 225, 200, 75, "3 Players", main),
                    Button(165, 325, 200, 75, "4 Players", main), 
                    Button(165, 425, 200, 75, "5 Players", main),
                    Button(165, 525, 200, 75, "6 Players", main)]
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