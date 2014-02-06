import ctypes
from sdl2 import *

from graphics import Graphics
from input import Input
from player import Player
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

        self.player = Player(graphics, 320, 240)

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

            # Player horizontal movement
            if input.isKeyHeld(SDLK_LEFT) and input.isKeyHeld(SDLK_RIGHT):
                self.player.stopMoving()
            elif input.isKeyHeld(SDLK_LEFT):
                self.player.startMovingLeft()
            elif input.isKeyHeld(SDLK_RIGHT):
                self.player.startMovingRight()
            else:
                self.player.stopMoving()

            # Player jump
            if input.wasKeyPressed(SDLK_z):
                self.player.startJump()
            elif input.wasKeyReleased(SDLK_z):
                self.player.stopJump()

            currentTime = SDL_GetTicks()
            self.update(currentTime - lastUpdateTime)
            lastUpdateTime = currentTime

            self.draw(graphics)

            # This loop lasts 1/60th of a second, or 1000/60th ms
            elapsedTime = SDL_GetTicks() - startTime
            SDL_Delay((1000 // FPS) - elapsedTime)

        graphics.cleanUp()

    def update(self, elapsedTime):
        self.player.update(elapsedTime)

    def draw(self, graphics):
        graphics.clear()
        self.player.draw(graphics)
        graphics.flip()
