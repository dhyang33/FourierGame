import pygame
import argparse
import time
import tutorial
from pitchGame1 import *
from pitchGame2 import *
from pitchGame3 import *
from pitchGame4 import *
from scoreScreen import *
from startScreen import *
from endScreen import *
parser = argparse.ArgumentParser()
#parser.add_argument('-d','--difficulty',dest = "difficulty",action="store", help='difficulty level')    
    
import sys
import os


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

    
    game = startScreen()
    game.run(screen)
    
    # Game 1
    game = tutorial.TutorialScreen(tutorial.level1)
    game.run(screen)
    game = PitchGame1(3)
    game.run(screen)
    score1 = game.score
    game = scoreScreen(score1)
    game.run(screen)
    
    
    #Game 2
    game = tutorial.TutorialScreen(tutorial.level2)
    game.run(screen)
    game = PitchGame2(3)
    game.run(screen)
    score2 = game.score
    game = scoreScreen(score2)
    game.run(screen)
    
    #Game 3
    game = tutorial.TutorialScreen(tutorial.level3)
    game.run(screen)
    game = PitchGame3(4)
    game.run(screen)
    score3 = game.score
    game = scoreScreen(score3)
    game.run(screen)
    
    #Game 4
    game = tutorial.TutorialScreen(tutorial.level4)
    game.run(screen)
    game = PitchGame4(4)
    game.run(screen)
    score4 = game.score
    game = scoreScreen(score4)
    game.run(screen)
    
    score_total = score1+score2+score3+score4
    
    game = endScreen(1000)
    game.run(screen)
    
    
    pygame.quit()
    
if __name__ == "__main__":
    args = parser.parse_args()
    main()