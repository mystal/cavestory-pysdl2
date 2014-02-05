from collections import namedtuple

from animated_sprite import AnimatedSprite
import game
from sprite import Sprite

SLOWDOWN_FACTOR = 0.8
WALKING_ACCELERATION = 0.0012 # (pixels / ms) / ms
MAX_SPEED_X = 0.325 # pixels / ms

class MotionType:
    STANDING = 0
    WALKING = 1

class HorizontalFacing:
    LEFT = 0
    RIGHT = 1

class SpriteState(namedtuple('SpriteState',
                             ['motionType', 'horizontalFacing'])):
    def __new__(cls, motionType=MotionType.STANDING,
                 horizontalFacing=HorizontalFacing.LEFT):
        return super().__new__(cls, motionType, horizontalFacing)

class Player:
    def __init__(self, graphics, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0.0
        self.accelerationX = 0.0

        self.horizontalFacing = HorizontalFacing.LEFT
        self.sprites = {}
        self.initializeSprites(graphics)

    def initializeSprites(self, graphics):
        spriteState = SpriteState(MotionType.STANDING,
                                  HorizontalFacing.LEFT)
        self.sprites[spriteState] = Sprite(
                graphics, b'content/MyChar.bmp', 0, 0, game.TILE_SIZE,
                game.TILE_SIZE)
        spriteState = SpriteState(MotionType.WALKING,
                                  HorizontalFacing.LEFT)
        self.sprites[spriteState] = AnimatedSprite(
                graphics, b'content/MyChar.bmp', 0, 0, game.TILE_SIZE,
                game.TILE_SIZE, 15, 3)

        spriteState = SpriteState(MotionType.STANDING,
                                  HorizontalFacing.RIGHT)
        self.sprites[spriteState] = Sprite(
                graphics, b'content/MyChar.bmp', 0, game.TILE_SIZE, game.TILE_SIZE,
                game.TILE_SIZE)
        spriteState = SpriteState(MotionType.WALKING,
                                  HorizontalFacing.RIGHT)
        self.sprites[spriteState] = AnimatedSprite(
                graphics, b'content/MyChar.bmp', 0, game.TILE_SIZE, game.TILE_SIZE,
                game.TILE_SIZE, 15, 3)

    def getSpriteState(self):
        return SpriteState(MotionType.STANDING if self.accelerationX == 0
                           else MotionType.WALKING,
                           self.horizontalFacing)

    def update(self, elapsedTime):
        self.sprites[self.getSpriteState()].update(elapsedTime)

        self.x += round(self.velocityX * elapsedTime)
        self.velocityX += self.accelerationX * elapsedTime

        if self.accelerationX > 0:
            self.velocityX = max(self.velocityX, -MAX_SPEED_X)
        elif self.accelerationX < 0:
            self.velocityX = min(self.velocityX, MAX_SPEED_X)
        else:
            self.velocityX *= SLOWDOWN_FACTOR

    def draw(self, graphics):
        self.sprites[self.getSpriteState()].draw(graphics, self.x, self.y)

    def startMovingLeft(self):
        self.accelerationX = -WALKING_ACCELERATION
        self.horizontalFacing = HorizontalFacing.LEFT

    def startMovingRight(self):
        self.accelerationX = WALKING_ACCELERATION
        self.horizontalFacing = HorizontalFacing.RIGHT

    def stopMoving(self):
        self.accelerationX = 0
