from sdl2 import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Graphics:
    def __init__(self):
        self.window = SDL_CreateWindow(b'My Cave Story',
                                       SDL_WINDOWPOS_UNDEFINED,
                                       SDL_WINDOWPOS_UNDEFINED,
                                       SCREEN_WIDTH,
                                       SCREEN_HEIGHT,
                                       SDL_WINDOW_SHOWN)
        SDL_SetRelativeMouseMode(True)

        self.spriteSheets = {}

    def cleanUp(self):
        SDL_DestroyWindow(self.window)
        for spriteSheet in self.spriteSheets.values():
            SDL_FreeSurface(spriteSheet)

    def loadImage(self, filePath, blackIsTransparent=False):
        spriteSheet = self.spriteSheets.get(filePath)
        if not spriteSheet:
            spriteSheet = SDL_LoadBMP(filePath)
            self.spriteSheets[filePath] = spriteSheet
            if blackIsTransparent:
                SDL_SetColorKey(spriteSheet, SDL_TRUE, 0)
        return spriteSheet

    def blitSurface(self, source, sourceRectangle, destinationRectangle):
        windowSurface = SDL_GetWindowSurface(self.window)
        SDL_BlitSurface(source, sourceRectangle, windowSurface,
                        destinationRectangle)

    def clear(self):
        windowSurface = SDL_GetWindowSurface(self.window)
        SDL_FillRect(windowSurface, None, 0)

    def flip(self):
        SDL_UpdateWindowSurface(self.window)
