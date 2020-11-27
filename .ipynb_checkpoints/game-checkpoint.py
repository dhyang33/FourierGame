import pygame
import argparse
import time
from pitchGame1 import *
from pitchGame2 import *
from scoreScreen import *
parser = argparse.ArgumentParser()
#parser.add_argument('-d','--difficulty',dest = "difficulty",action="store", help='difficulty level')    
    

def main():
    pygame.font.init() 
    pygame.mixer.init()
    pygame.init()
           
    X,Y = 1360,768
    middle_X = X/2
    middle_Y = Y/2

    # Set up the drawing window
    window = pygame.display.set_mode((X, Y), pygame.DOUBLEBUF)
    screen = pygame.display.get_surface()
    pygame.display.set_caption('Fourier Game') 
    
    game = PitchGame1(3)
    game.run(screen)
    score1 = game.score
    game = scoreScreen(score1)
    game.run(screen)
    
    game = PitchGame2(3)
    game.run(screen)
    score2 = game.score
    game = scoreScreen(score2)
    game.run(screen)
if __name__ == "__main__":
    args = parser.parse_args()
    main()