import ctypes
from sdl2 import *

from graphics import Graphics
from sprite import Sprite

FPS = 60

class Game:
    def __init__(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        SDL_SetRelativeMouseMode(True)

    def cleanUp(self):
        SDL_Quit()

    def eventLoop(self):
        graphics = Graphics()
        event = SDL_Event()

        self.sprite = Sprite(b'content/MyChar.bmp', 0, 0, 32, 32)

        running = True
        while running:
            startTime = SDL_GetTicks()
            while SDL_PollEvent(ctypes.byref(event)):
                if event.type == SDL_KEYDOWN:
                    if event.key.keysym.sym == SDLK_ESCAPE:
                        running = False

            self.update()
            self.draw(graphics)

            # This loop lasts 1/60th of a second, or 1000/60th ms
            elapsedTime = SDL_GetTicks() - startTime
            SDL_Delay((1000 // FPS) - elapsedTime)

        self.sprite.cleanUp()
        graphics.cleanUp()

    def update(self):
        pass

    def draw(self, graphics):
        self.sprite.draw(graphics, 320, 240)
        graphics.flip()
