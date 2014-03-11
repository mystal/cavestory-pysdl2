from sdl2 import *

class Graphics:
    def __init__(self, screenWidth, screenHeight):
        self.window = SDL_CreateWindow(b'cavestory-pysdl2',
                                       SDL_WINDOWPOS_UNDEFINED,
                                       SDL_WINDOWPOS_UNDEFINED,
                                       screenWidth,
                                       screenHeight,
                                       SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1, 0)
        SDL_SetRelativeMouseMode(True)

        self.spriteSheets = {}

    def cleanUp(self):
        for spriteSheet in self.spriteSheets.values():
            SDL_DestroyTexture(spriteSheet)
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)

    def loadImage(self, filePath, blackIsTransparent=False):
        spriteSheet = self.spriteSheets.get(filePath)
        if not spriteSheet:
            surface = SDL_LoadBMP(filePath)
            if blackIsTransparent:
                SDL_SetColorKey(surface, SDL_TRUE, 0)
            spriteSheet = SDL_CreateTextureFromSurface(self.renderer, surface)
            self.spriteSheets[filePath] = spriteSheet
            SDL_FreeSurface(surface)
        return spriteSheet

    def blitSurface(self, source, srcRect, dstRect):
        SDL_RenderCopy(self.renderer, source, srcRect, dstRect)

    def clear(self):
        SDL_RenderClear(self.renderer)

    def flip(self):
        SDL_RenderPresent(self.renderer)
