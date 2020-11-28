import pygame
import numpy as np
import librosa
import time
import soundfile
import random
from sprite import *
class startScreen:
    orig_sound = []
    num_pitches = -1
    score = None
    clicked = False
    possible_pitches = {"C4":262,
                           "D4":293,
                           "E4":329,
                           "F4":349,
                           "G4":392,
                           "A4":440,
                           "B4":494,
                           "C5":523,
                           "D5":587,
                           "E5":659,
                           "F5":699,
                           "G5":784,
                           "A5":880,
                           "B5":989}
    notes = []
    def __init__(self):
        pass
        
    def pitchMaker(self,frequency=262,magnitude = 1,time = 1,sr = 22050):
        t = np.arange(0, time,1/sr)
        data = magnitude*np.sin(2*np.pi*frequency*t)
        return data
    
    def playSound(self,data,sr=22050):
        soundfile.write("assets/orig_sound.wav",data,sr)
        sound = pygame.mixer.Sound('assets/orig_sound.wav')
        sound.set_volume(0.5)
        sound.play()
        time.sleep(3)
        
    def playConstructed(self,sprites,sr=22050):
        freq1 = int(sprites['b1'].text.split(" ")[0])
        freq2 = int(sprites['b2'].text.split(" ")[0])
        freq3 = int(sprites['b3'].text.split(" ")[0])
        data1 = np.array(self.pitchMaker(freq1,time=2))
        data2 = np.array(self.pitchMaker(freq2,time=2))
        data3 = np.array(self.pitchMaker(freq3,time=2))
        data = data1+data2+data3
        soundfile.write("assets/constructed_sound.wav",data,sr)
        sound = pygame.mixer.Sound('assets/constructed_sound.wav')
        sound.set_volume(0.5)
        sound.play()
        time.sleep(3)
        
    def drawSprites(self, screen, sprites):
        for sprite in sprites:
            sprites[sprite].drawSprite(screen)

    def add_sprite(self,id,s,sprites):
        if not id in sprites.keys():
            sprites[id] = s
        return sprites
    
    def updateFrequency(self,current, direction):
        values = sorted(self.possible_pitches.values())
        if direction == "up":
            offset = 1
        elif direction == "down":
            offset = -1
        for idx,freq in enumerate(values):
            if str(freq) in current:
                next_idx = idx+offset
                if next_idx < 0:
                    next_idx = 0
                elif next_idx >= len(values):
                    next_idx = len(values)-1
                next_freq = str(values[next_idx])+" Hz"
        return next_freq
    
    def scoreGuess(self,sprites):
        freqs_guess = [int(sprites['b1'].text.split(" ")[0]),int(sprites['b2'].text.split(" ")[0]),int(sprites['b3'].text.split(" ")[0])]
        freqs_guess = sorted(freqs_guess)
        freqs_gt = sorted([self.possible_pitches[note] for note in self.notes])
        guess = []
        gt = []
        frequencies = sorted(self.possible_pitches.values())
        for freq in freqs_guess:
            guess.append(frequencies.index(freq))
        for freq in freqs_gt:
            gt.append(frequencies.index(freq))
        score = np.abs(guess[0]-gt[0])+ np.abs(guess[1]-gt[1])+ np.abs(guess[2]-gt[2])
        points = (20-score)*50
        if point < 0:
            points = 0
        print(points)
        return points

    def buttonListener(self,clicked_sprites,sprites):
        if 'next' in clicked_sprites:
            self.clicked = True
        return sprites
    
    def defineSprites(self, middle_X, middle_Y):
        sprites = {}
        offset = 300
        r = pygame.Rect(0,0,1,1)
        scoreSprite = Sprite(rect = r, rectColor = (173, 216, 230),text = f'Fourier Game', textPos = (middle_X-offset-10,middle_Y/2), textColor = (0,0,128),textFontSize=100)
        sprites = self.add_sprite("score",scoreSprite, sprites)
        
        r = pygame.Rect(0,0,1,1)
        nameSprite = Sprite(rect = r, rectColor = (173, 216, 230),text = f'by Daniel Yang, Thomas Fleming, Xander Hirsch', textPos = (middle_X-550,middle_Y/2+120), textColor = (0,0,0))
        sprites = self.add_sprite("names",nameSprite, sprites)
        
        r = pygame.Rect(middle_X-offset,3*middle_Y/2,offset*2,60)
        continueSprite = Sprite(rect = r, rectColor = (0,255,0),text = f'Play', textPos = (middle_X-offset+250,3*middle_Y/2), textColor = (0,0,0))
        sprites = self.add_sprite("next",continueSprite, sprites)
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
            if self.clicked:
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

            # Fill the background with white
            screen.fill((173, 216, 230))

            # Draw sprites
            self.drawSprites(screen, sprites)
            
            # Update sprites
            for sprite in sprites:
                sprites[sprite].update()

            # Flip the display
            pygame.display.flip()