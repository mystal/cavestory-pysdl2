from sdl2 import *

class Sprite:
    def __init__(self, graphics, filePath, sourceX, sourceY, width, height):
        self.spriteSheet = graphics.loadImage(filePath)
        self.sourceRect = SDL_Rect()
        self.sourceRect.x = sourceX
        self.sourceRect.y = sourceY
        self.sourceRect.w = width
        self.sourceRect.h = height

    def update(self, elapsedTime):
        pass

    def draw(self, graphics, x, y):
        destinationRect = SDL_Rect()
        destinationRect.x = x
        destinationRect.y = y
        graphics.blitSurface(self.spriteSheet, self.sourceRect, destinationRect)
