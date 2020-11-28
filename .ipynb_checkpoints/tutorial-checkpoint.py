import pygame
import numpy as np
import librosa
import time
import soundfile
import random
from sprite import *
from textBox import *

level1 = "Attention all Analysts! We have received a mysterious " + \
        "signal from Galaxy 131. It appears to be some combination of " + \
        "sinusoidal waves. Can you listen to the signal and identify the " + \
        "component frequencies?"

level2 = "We've received a call from mathmatician Joseph Fourier. He has analyzed the " + \
    "time-domain signal with his Discrete Fourier Transform (DFT) and provided us with " + \
    "a frequency-domain plot. Now can you identify the notes?"

level3 = "Code Blue! We have received a more complex signal: four notes in " + \
    "sequence! We're trying to contact Fourier, but until we can reach " + \
    "him, can you try to identify the pitches from the audio signal?"

level4 = "We have finally reached Fourier. He has provided us with a " + \
    "spectrogram of the signal. Now are you able to determine the sequence " + \
    "of notes?"

class TutorialScreen:

    tutorialText = None

    next = False

    def __init__(self, text):
        self.tutorialText = text
        pass

    def drawSprites(self, screen, sprites):
        for sprite in sprites:
            sprites[sprite].drawSprite(screen)

    def add_sprite(self, id, s, sprites):
        if not id in sprites.keys():
            sprites[id] = s
        return sprites

    def buttonListener(self, clicked_sprites, sprites):
        if 'next' in clicked_sprites:
            self.next = True
        return sprites

    def getNextSprite(self, middle_X):
        length = 250
        width = 70
        X = middle_X
        Y = 680
        spriteX = X + 3 * length/2
        spriteY = Y
        offset = 64
        r = pygame.Rect(spriteX, spriteY, length, width)
        nextButton = Sprite(rect = r, rectColor = (0, 255, 0), \
            text = "Next", \
            textPos = (spriteX + length/2 - offset/2-20, spriteY+10), \
            textColor = (0, 0, 0))
        return nextButton
    
    def getTextBox(self, middle_X):
        length = 1200
        width = 300
        X = middle_X
        Y = 200
        spriteX = X - length/2
        spriteY = Y
        r = pygame.Rect(spriteX, spriteY, length, width)

        textBox = TextBox(rect = r, rectColor = (255, 0, 0), \
            text = self.tutorialText, \
            textPos = (spriteX, spriteY), \
            textColor = (0, 0, 0))
        return textBox

    def defineSprites(self, middle_X, middle_Y):
        sprites = {}

        nextSprite = self.getNextSprite(middle_X)
        sprites = self.add_sprite('next', nextSprite, sprites)

        textSprite = self.getTextBox(middle_X)
        sprites = self.add_sprite('text', textSprite, sprites)

        return sprites
    
    def run(self,screen):
        X,Y = 1360,768
        middle_X = X/2
        middle_Y = Y/2

        # Define sprites
        sprites = self.defineSprites(middle_X, middle_Y)
            
        # Run until the user asks to quit
        running = True
        while running:
            if self.next:
                pygame.display.flip()
                break
            
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprites if sprites[s].rect.collidepoint(pos)]
                    sprites = self.buttonListener(clicked_sprites,sprites)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

            # Fill the background with blue
            screen.fill((173, 216, 230))

            # Draw sprites
            self.drawSprites(screen, sprites)
            
            # Update sprites
            for sprite in sprites:
                sprites[sprite].update()

            # Flip the display
            pygame.display.flip()
