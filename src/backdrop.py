from sdl2 import SDL_Rect

import game
import units

BACKGROUND_SIZE = 4 # units.Tile

class Backdrop:
    def draw(self, graphics):
        raise NotImplementedError

class FixedBackdrop(Backdrop):
    def __init__(self, path, graphics):
        self.surfaceId = graphics.loadImage(path)

    def draw(self, graphics):
        destRect = SDL_Rect()
        for tileX in range(0, game.SCREEN_WIDTH, BACKGROUND_SIZE):
            for tileY in range(0, game.SCREEN_HEIGHT, BACKGROUND_SIZE):
                destRect.x = units.tileToPixel(tileX)
                destRect.y = units.tileToPixel(tileY)
                destRect.w = destRect.h = units.tileToPixel(BACKGROUND_SIZE)
                graphics.blitSurface(self.surfaceId, None, destRect)
