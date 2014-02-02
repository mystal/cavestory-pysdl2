import ctypes
from sdl2 import *

from animated_sprite import AnimatedSprite
from graphics import Graphics
from input import Input
from sprite import Sprite

FPS = 60
TILE_SIZE = 32

class Game:
    def __init__(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        SDL_SetRelativeMouseMode(True)

    def cleanUp(self):
        SDL_Quit()

    def eventLoop(self):
        graphics = Graphics()
        input = Input()
        event = SDL_Event()

        self.sprite = AnimatedSprite(b'content/MyChar.bmp', 0, 0,
                                     TILE_SIZE, TILE_SIZE, 15, 3)

        running = True
        lastUpdateTime = SDL_GetTicks()
        while running:
            startTime = SDL_GetTicks()
            input.beginNewFrame()
            while SDL_PollEvent(ctypes.byref(event)):
                if event.type == SDL_KEYDOWN:
                    input.keyDownEvent(event)
                elif event.type == SDL_KEYUP:
                    input.keyUpEvent(event)

            if input.wasKeyPressed(SDLK_ESCAPE):
                running = False

            currentTime = SDL_GetTicks()
            self.update(currentTime - lastUpdateTime)
            lastUpdateTime = currentTime

            self.draw(graphics)

            # This loop lasts 1/60th of a second, or 1000/60th ms
            elapsedTime = SDL_GetTicks() - startTime
            SDL_Delay((1000 // FPS) - elapsedTime)

        self.sprite.cleanUp()
        graphics.cleanUp()

    def update(self, elapsedTime):
        self.sprite.update(elapsedTime)

    def draw(self, graphics):
        self.sprite.draw(graphics, 320, 240)
        graphics.flip()
