from sdl2 import *

import units

class Sprite:
    def __init__(self, graphics, filePath, sourceX, sourceY, width, height):
        self.spriteSheet = graphics.loadImage(filePath, blackIsTransparent=True)
        self.sourceRect = SDL_Rect()
        self.sourceRect.x = sourceX # units.Pixel
        self.sourceRect.y = sourceY # units.Pixel
        self.sourceRect.w = width # units.Pixel
        self.sourceRect.h = height # units.Pixel

    def update(self, elapsedTime):
        pass

    def draw(self, graphics, gameX, gameY):
        destinationRect = SDL_Rect()
        destinationRect.x = units.gameToPixel(gameX)
        destinationRect.y = units.gameToPixel(gameY)
        destinationRect.w = self.sourceRect.w
        destinationRect.h = self.sourceRect.h
        graphics.blitSurface(self.spriteSheet, self.sourceRect, destinationRect)

class AnimatedSprite(Sprite):
    def __init__(self, graphics, filePath, sourceX, sourceY, width, height,
                 fps, numFrames):
        super().__init__(graphics, filePath, sourceX, sourceY, width, height)
        self.frameTime = 1000 // fps # units.MS
        self.numFrames = numFrames # units.Frame
        self.currentFrame = 0 # units.Frame
        self.elapsedTime = 0 # units.MS, Elapsed time since last frame change

    def update(self, elapsedTime):
        self.elapsedTime += elapsedTime
        if self.elapsedTime > self.frameTime:
            self.currentFrame += 1
            self.elapsedTime = 0

            # Move the source rectangle in the sprite sheet
            if self.currentFrame < self.numFrames:
                self.sourceRect.x += self.sourceRect.w
            else:
                self.sourceRect.x -= self.sourceRect.w * (self.numFrames - 1)
                self.currentFrame = 0
