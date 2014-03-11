from sdl2 import SDL_Rect

from graphics import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE

BACKGROUND_SIZE = TILE_SIZE * 4 # pixels

class Backdrop:
    def draw(self, graphics):
        raise NotImplementedError

class FixedBackdrop(Backdrop):
    def __init__(self, path, graphics):
        self.surfaceId = graphics.loadImage(path)

    def draw(self, graphics):
        destRect = SDL_Rect()
        for x in range(0, SCREEN_WIDTH, BACKGROUND_SIZE):
            for y in range(0, SCREEN_HEIGHT, BACKGROUND_SIZE):
                destRect.x = x
                destRect.y = y
                destRect.w = destRect.h = BACKGROUND_SIZE
                graphics.blitSurface(self.surfaceId, None, destRect)
