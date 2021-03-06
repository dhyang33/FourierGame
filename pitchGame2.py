import pygame
import numpy as np
import librosa
import time
import soundfile
import random
import matplotlib
import matplotlib.pyplot as plt
import scipy
import scipy.fftpack
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import os
import sys
from sprite import *

def resource_path(relative_path):
    base_path = os.path.abspath("./assets")
    return os.path.join(base_path, relative_path)

class PitchGame2:
    orig_sound = []
    score = None
    clicked = False
    num_pitches = -1
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
    DFT1 = None
    DFT2 = None
    def __init__(self,num_pitches):
        self.num_pitches = num_pitches
        self.notes = []
        while(self.notes == [] or 
              (self.possible_pitches[self.notes[1]]-self.possible_pitches[self.notes[0]])/self.possible_pitches[self.notes[0]]< 0.2 or
              (self.possible_pitches[self.notes[2]]-self.possible_pitches[self.notes[1]])/self.possible_pitches[self.notes[1]]< 0.2):
            self.notes = random.sample(self.possible_pitches.keys(),self.num_pitches)
        freqs = [self.possible_pitches[note] for note in self.notes]
        amplitudes = []
        for i in range(len(freqs)):
            #random_amp = random.random()
            random_amp = 1
            amplitudes.append(random_amp)
        
        for freq,amplitude in zip(freqs,amplitudes):
            note = np.array(self.pitchMaker(freq,amplitude,2))
            if self.orig_sound == []:
                self.orig_sound = note
            else:
                self.orig_sound += note
        self.DFT1 = np.abs(scipy.fftpack.fft(self.orig_sound[:22050]))
        self.DFT2 = self.DFT1[:1000]
        
        
        
    def pitchMaker(self,frequency=262,magnitude = 1,time = 1,sr = 22050):
        t = np.arange(0, time,1/sr)
        data = magnitude*np.sin(2*np.pi*frequency*t)
        return data
    
    def playSound(self,data,sr=22050):
        self.clicked = True
        soundfile.write(resource_path("orig_sound.wav"),data,sr)
        sound = pygame.mixer.Sound(resource_path('orig_sound.wav'))
        sound.set_volume(0.5)
        sound.play()
        time.sleep(4)
        self.clicked = False
        
    def playConstructed(self,sprites,sr=22050):
        freq1 = int(sprites['b1'].text.split(" ")[0])
        freq2 = int(sprites['b2'].text.split(" ")[0])
        freq3 = int(sprites['b3'].text.split(" ")[0])
        data1 = np.array(self.pitchMaker(freq1,time=2))
        data2 = np.array(self.pitchMaker(freq2,time=2))
        data3 = np.array(self.pitchMaker(freq3,time=2))
        data = data1+data2+data3
        self.clicked = True
        soundfile.write(resource_path("constructed_sound.wav"),data,sr)
        sound = pygame.mixer.Sound(resource_path('constructed_sound.wav'))
        sound.set_volume(0.5)
        sound.play()
        time.sleep(4)
        self.clicked = False
        
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
        if points < 0:
            points = 0
        return points

    def buttonListener(self,clicked_sprites,sprites):
        if 'soundIcon' in clicked_sprites:
            #sprites['soundIcon'].timedColorChange((255,190,0),30)
            self.playSound(self.orig_sound)
        if 'u1' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b1'].text,"up")
            sprites['b1'].text = nextFreq
        if 'd1' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b1'].text,"down")
            sprites['b1'].text = nextFreq
        if 'u2' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b2'].text,"up")
            sprites['b2'].text = nextFreq
        if 'd2' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b2'].text,"down")
            sprites['b2'].text = nextFreq
        if 'u3' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b3'].text,"up")
            sprites['b3'].text = nextFreq
        if 'd3' in clicked_sprites:
            nextFreq = self.updateFrequency(sprites['b3'].text,"down")
            sprites['b3'].text = nextFreq
        if 'play' in clicked_sprites:
            #sprites['play'].timedColorChange((225,0,0),30)
            self.playConstructed(sprites)
        if 'score' in clicked_sprites:
            self.score = self.scoreGuess(sprites)
        return sprites
       
        
    def getSoundSprite(self,middle_X):
        X = middle_X
        Y = 200
        soundIcon_image = pygame.image.load(resource_path('sound.png'))
        soundIcon_image = pygame.transform.scale(soundIcon_image, (100,100))
        soundIcon_rect = soundIcon_image.get_rect().size
        r = pygame.Rect(X-soundIcon_rect[0]/2-10, Y-soundIcon_rect[1]/2-10-20,soundIcon_rect[0]+20,soundIcon_rect[1]+20)
        soundIcon = Sprite(r, soundIcon_image, (X-soundIcon_rect[0]/2, Y-soundIcon_rect[1]/2-20), (255,153,0))
        return soundIcon
    
    def getTitleSprite(self, middle_X):
        r = pygame.Rect(0,0,0,0)
        length = 800
        return Sprite(rect = r, rectColor = (255,255,255), text = "Identify the frequencies in the sound.", textPos = (middle_X-length/2,20), textColor = (0,0,0))
    
    def getPitchSprites(self, middle_X):
        buttons = []
        for i in range(self.num_pitches):
            offset = 230
            delta = 450
            length = 250
            width = 100
            X = delta*i+offset-20
            Y = 500
            r = pygame.Rect(X-length/2, Y-width/2+100,length, width)
            buttons.append(Sprite(rect = r, rectColor = (255,255,255), text = "262 Hz", textPos = (X-length/4-20,Y-width/4+100), textColor = (0,0,0)))
        return buttons
    
    def getUpButtonSprites(self, middle_X):
        buttons = []
        for i in range(self.num_pitches):
            offset = 230
            delta = 450
            length = 250
            width = 100
            X = delta*i+offset-20
            Y = 500
            r = pygame.Rect(X+length/2, Y-width/2+100,40, 40)
            uparrow_image = pygame.image.load(resource_path('uparrow-removebg.png'))
            uparrow_image = pygame.transform.scale(uparrow_image, (40,40))
            buttons.append(Sprite(rect = r, rectColor = (173, 216, 230), image = uparrow_image, imagePos = (X+length/2, Y-width/2+100)))
        return buttons
    
    def getDownButtonSprites(self, middle_X):
        buttons = []
        for i in range(self.num_pitches):
            offset = 230
            delta = 450
            length = 250
            width = 100
            X = delta*i+offset-20
            Y = 500
            r = pygame.Rect(X+length/2, Y+10+100,40, 40)
            downarrow_image = pygame.image.load(resource_path('downarrow-removebg.png'))
            downarrow_image = pygame.transform.scale(downarrow_image, (40,40))
            buttons.append(Sprite(rect = r, rectColor = (173, 216, 230), image = downarrow_image, imagePos = (X+length/2, Y+10+100)))
        return buttons
    
    def getPlaySprite(self,middle_X):
        length = 250
        width = 70
        X = middle_X
        Y = 680
        r = pygame.Rect(X-3*length/2, Y, length, width)
        playButton = Sprite(rect = r, rectColor = (255,0,0), text = "Test Sound", textPos = (X-3*length/2, Y+10), textColor = (0,0,0))
        return playButton
    
    def getScoreSprite(self,middle_X):
        length = 250
        width = 70
        X = middle_X
        Y = 680
        offset = 32
        r = pygame.Rect(X+length/2-offset/2, Y, length+offset*2, width)
        playButton = Sprite(rect = r, rectColor = (0,255,0), text = "Submit Sound", textPos = (X+length/2-offset/2, Y+10), textColor = (0,0,0))
        return playButton
    
    def getGraphSprite1(self, middle_X):
        fig = pylab.figure(figsize=[6, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
        ax = fig.gca()
        ax.plot(self.DFT1)
        ax.set_xlabel('Frequency (HZ)')
        ax.set_ylabel('Magnitude of X_k')
        ax.set_title("DFT of Sound Signal")
        
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        img = pygame.image.fromstring(raw_data, size, "RGB")
        
        offset_X = 20
        offset_Y = 20
        r = pygame.Rect(0,0,1,1)
        graphSprite = Sprite(rect = r, rectColor = (173, 216, 230),image = img, imagePos = (offset_X,offset_Y+100))
        return graphSprite
    
    def getGraphSprite2(self, middle_X):
        fig = pylab.figure(figsize=[6, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
        ax = fig.gca()
        ax.plot(self.DFT2)
        ax.set_xlabel('Frequency (HZ)')
        ax.set_ylabel('Magnitude of X_k')
        ax.set_title("Zoomed In DFT of Sound Signal")
        
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        img = pygame.image.fromstring(raw_data, size, "RGB")
        
        offset_X = 1360-20-600
        offset_Y = 20
        r = pygame.Rect(0,0,1,1)
        graphSprite = Sprite(rect = r, rectColor = (173, 216, 230),image = img, imagePos = (offset_X,offset_Y+100))
        return graphSprite

    
    def defineSprites(self, middle_X, middle_Y):
        sprites = {}
        titleSprite = self.getTitleSprite(middle_X)
        sprites = self.add_sprite("title",titleSprite, sprites)
        
        soundIcon = self.getSoundSprite(middle_X)
        sprites = self.add_sprite("soundIcon",soundIcon, sprites)
        
        graph = self.getGraphSprite1(middle_X)
        sprites = self.add_sprite("graph1",graph,sprites)
        
        graph = self.getGraphSprite2(middle_X)
        sprites = self.add_sprite("graph2",graph,sprites)
        
        buttons = self.getPitchSprites(middle_X)
        for idx, button in enumerate(buttons):
            sprites = self.add_sprite(f"b{idx+1}",button,sprites)
                           
        buttons = self.getUpButtonSprites(middle_X)
        for idx, button in enumerate(buttons):
            sprites = self.add_sprite(f"u{idx+1}",button,sprites)                   
        
        buttons = self.getDownButtonSprites(middle_X)
        for idx, button in enumerate(buttons):
            sprites = self.add_sprite(f"d{idx+1}",button,sprites) 
        
        playSprite = self.getPlaySprite(middle_X)
        sprites = self.add_sprite("play",playSprite,sprites)
        
        scoreSprite = self.getScoreSprite(middle_X)
        sprites = self.add_sprite("score",scoreSprite,sprites)
        return sprites
    
    def run(self,screen):
        pygame.font.init() 
        pygame.mixer.init()
        pygame.init()
           
        X,Y = 1360,768
        middle_X = X/2
        middle_Y = Y/2
        
        # Define sprites
        sprites = self.defineSprites(middle_X, middle_Y)
            
        # Run until the user asks to quit
        running = True
        while running:
            if self.score!=None:
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
