import ctypes
from sdl2 import *

from first_cave_bat import FirstCaveBat
from graphics import Graphics
from input import Input
from map import Map
from player import Player
from sprite import Sprite
import units

FPS = 60 # units.FPS
MAX_FRAME_TIME = int(5 * (1000 / FPS))

SCREEN_WIDTH = 20 # units.Tile
SCREEN_HEIGHT = 15 # units.Tile

class Game:
    def __init__(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def cleanUp(self):
        SDL_Quit()

    def eventLoop(self):
        graphics = Graphics(units.tileToPixel(SCREEN_WIDTH),
                            units.tileToPixel(SCREEN_HEIGHT))
        input = Input()
        event = SDL_Event()

        self.player = Player(graphics,
                             units.tileToGame(SCREEN_WIDTH // 2),
                             units.tileToGame(SCREEN_HEIGHT // 2))
        self.bat = FirstCaveBat(graphics,
                                units.tileToGame(5),
                                units.tileToGame(SCREEN_HEIGHT // 2))
        self.map = Map.createTestMap(graphics)

        running = True
        lastUpdateTime = SDL_GetTicks() # units.MS
        while running:
            startTime = SDL_GetTicks() # units.MS
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

            # Player look
            if input.isKeyHeld(SDLK_UP) and input.isKeyHeld(SDLK_DOWN):
                self.player.lookHorizontal()
            elif input.isKeyHeld(SDLK_UP):
                self.player.lookUp()
            elif input.isKeyHeld(SDLK_DOWN):
                self.player.lookDown()
            else:
                self.player.lookHorizontal()

            # Player jump
            if input.wasKeyPressed(SDLK_z):
                self.player.startJump()
            elif input.wasKeyReleased(SDLK_z):
                self.player.stopJump()

            currentTime = SDL_GetTicks() # units.MS
            elapsedTime = currentTime - lastUpdateTime # units.MS
            self.update(min(elapsedTime, MAX_FRAME_TIME))
            lastUpdateTime = currentTime

            self.draw(graphics)

            # This loop lasts 1/60th of a second, or 1000/60th ms
            msPerFrame = 1000 // FPS # units.MS
            elapsedTime = SDL_GetTicks() - startTime # units.MS
            if elapsedTime < msPerFrame:
                SDL_Delay(msPerFrame - elapsedTime)

        graphics.cleanUp()

    def update(self, elapsedTime):
        self.player.update(elapsedTime, self.map)
        self.bat.update(elapsedTime, self.player.centerX())
        self.map.update(elapsedTime)

    def draw(self, graphics):
        graphics.clear()
        self.map.drawBackground(graphics)
        self.bat.draw(graphics)
        self.player.draw(graphics)
        self.map.draw(graphics)
        graphics.flip()
