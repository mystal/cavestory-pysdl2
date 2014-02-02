from sdl2 import *

class Sprite:
    def __init__(self, filePath, sourceX, sourceY, width, height):
        self.spriteSheet = SDL_LoadBMP(filePath)
        self.sourceRect = SDL_Rect()
        self.sourceRect.x = sourceX
        self.sourceRect.y = sourceY
        self.sourceRect.w = width
        self.sourceRect.h = height

    def cleanUp(self):
        SDL_FreeSurface(self.spriteSheet)

    def update(self, elapsedTime):
        pass

    def draw(self, graphics, x, y):
        destinationRect = SDL_Rect()
        destinationRect.x = x
        destinationRect.y = y
        graphics.blitSurface(self.spriteSheet, self.sourceRect, destinationRect)
