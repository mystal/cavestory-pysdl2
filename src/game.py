import ctypes
import sdl2

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

class Game:
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        sdl2.SDL_SetRelativeMouseMode(True)
        self.window = sdl2.SDL_CreateWindow(b'',
                                            sdl2.SDL_WINDOWPOS_UNDEFINED,
                                            sdl2.SDL_WINDOWPOS_UNDEFINED,
                                            SCREEN_WIDTH,
                                            SCREEN_HEIGHT,
                                            sdl2.SDL_WINDOW_SHOWN)

    def cleanUp(self):
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def eventLoop(self):
        running = True
        event = sdl2.SDL_Event()

        while running:
            startTime = sdl2.SDL_GetTicks()
            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False

            self.update()
            self.draw()

            # This loop lasts 1/60th of a second, or 1000/60th ms
            elapsedTime = sdl2.SDL_GetTicks() - startTime
            sdl2.SDL_Delay((1000 // FPS) - elapsedTime)

    def update(self):
        pass

    def draw(self):
        pass
