import pygame
import argparse
from pitchGame import *
parser = argparse.ArgumentParser()
#parser.add_argument('-d','--difficulty',dest = "difficulty",action="store", help='difficulty level')

def main(difficulty):
    freqs = [262]
    game = PitchGame(difficulty)
    game.run()
    
if __name__ == "__main__":
    args = parser.parse_args()
    main(3)