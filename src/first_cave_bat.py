from collections import namedtuple
import math

from rectangle import Rectangle
from sprite import AnimatedSprite
import units

FLY_FPS = 13 # units.FPS
NUM_FLY_FRAMES = 3 # units.Frame

ANGULAR_VELOCITY = 120.0 / 1000 # units.AngularVelocity

class Facing:
    LEFT = 0
    RIGHT = 1
    COUNT = 2

class SpriteState(namedtuple('SpriteState',
                             ['facing'])):
    def __new__(cls, facing=Facing.LEFT):
        return super().__new__(cls, facing)

class FirstCaveBat:
    def __init__(self, graphics, x, y):
        self.centerY = y # units.Game
        self.x = x # units.Game
        self.y = y # units.Game
        self.facing = Facing.RIGHT
        self.flight_angle = 0.0 # units.Degrees

        self.sprites = {}
        self.initializeSprites(graphics)

    def initializeSprites(self, graphics):
        for facing in range(Facing.COUNT):
            spriteState = SpriteState(facing)
            self.initializeSprite(graphics, spriteState)

    def initializeSprite(self, graphics, spriteState):
        tileY = 3 if spriteState.facing == Facing.RIGHT else 2
        self.sprites[spriteState] = AnimatedSprite(
                graphics, b'assets/NpcCemet.bmp',
                units.tileToPixel(2), units.tileToPixel(tileY),
                units.tileToPixel(1), units.tileToPixel(1),
                FLY_FPS, NUM_FLY_FRAMES)

    def getSpriteState(self):
        return SpriteState(self.facing)

    def draw(self, graphics):
        self.sprites[self.getSpriteState()].draw(graphics, self.x, self.y)

    def update(self, elapsedTime, playerX):
        self.flight_angle += ANGULAR_VELOCITY * elapsedTime

        self.facing = Facing.LEFT if self.x + units.tileToGame(1) / 2 > playerX else Facing.RIGHT

        self.y = self.centerY + units.tileToGame(5) / 2 * math.sin(
                math.radians(self.flight_angle))

        self.sprites[self.getSpriteState()].update(elapsedTime)

    def damageRect(self):
        return Rectangle(self.x + units.tileToGame(1) / 2,
                         self.y + units.tileToGame(1) / 2,
                         0, 0)
