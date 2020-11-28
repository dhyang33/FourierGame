import pygame
class Sprite:
    rect = None
    image = None
    imagePos = None
    rectColor = None
    origColor = None
    text = None
    textpos = None
    timer = -1
    count = 0
    textFontSize = 50
    def __init__(self,rect=None, image=None, imagePos=None, rectColor=None, text = None, textPos = None, textColor = None, textFontSize=50):
        self.rect = rect
        self.image = image
        self.imagePos = imagePos
        self.rectColor = rectColor
        self.text = text
        self.textPos = textPos
        self.textColor = textColor
        self.textFontSize = textFontSize
    
    def timedColorChange(self,newColor,numFrames):
        self.timer = numFrames
        self.count = 0
        self.origColor = self.rectColor
        self.rectColor = newColor
            
    def drawSprite(self,screen):
        if self.rect!=None:
            pygame.draw.rect(screen, self.rectColor, self.rect)
        if self.image != None:
            screen.blit(self.image, self.imagePos)
        if self.text != None:
            myfont = pygame.font.SysFont('Arial', self.textFontSize)
            screen.blit(myfont.render(self.text, False, self.textColor), self.textPos)
            
    
    def update(self):
        if self.timer!=-1:
            if self.count < self.timer:
                self.count+=1
            else:
                self.rectColor = self.origColor
                self.count = 0
                self.timer = -1