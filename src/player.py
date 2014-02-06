from collections import namedtuple

from animated_sprite import AnimatedSprite
import game
from sprite import Sprite

SLOWDOWN_FACTOR = 0.8
WALKING_ACCELERATION = 0.0012 # (pixels / ms) / ms
MAX_SPEED_X = 0.325 # pixels / ms

GRAVITY = 0.0012 # (pixels / ms) / ms
JUMP_SPEED = 0.325 # pixels / ms
MAX_SPEED_Y = 0.325 # pixels / ms
JUMP_TIME = 275 # ms

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

class Jump:
    def __init__(self):
        self.timeRemaining = 0
        self.active = False

    def update(self, elapsedTime):
        if self.active:
            self.timeRemaining -= elapsedTime
            if self.timeRemaining <= 0:
                self.active = False

    def reset(self):
        self.timeRemaining = JUMP_TIME
        self.reactivate()

    def reactivate(self):
        self.active = self.timeRemaining > 0

    def deactivate(self):
        self.active = False

class Player:
    def __init__(self, graphics, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0.0
        self.velocityY = 0.0
        self.accelerationX = 0.0

        self.horizontalFacing = HorizontalFacing.LEFT
        self._onGround = False

        self.jump = Jump()

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
        self.jump.update(elapsedTime)

        self.x += round(self.velocityX * elapsedTime)
        self.velocityX += self.accelerationX * elapsedTime

        if self.accelerationX > 0:
            self.velocityX = max(self.velocityX, -MAX_SPEED_X)
        elif self.accelerationX < 0:
            self.velocityX = min(self.velocityX, MAX_SPEED_X)
        elif self._onGround:
            self.velocityX *= SLOWDOWN_FACTOR

        self.y += round(self.velocityY * elapsedTime)
        if not self.jump.active:
            self.velocityY += GRAVITY * elapsedTime
            self.velocityY = min(self.velocityY, MAX_SPEED_Y)

        # TODO: remove this hack
        if self.y >= 320:
            self.y = 320
            self.velocityY = 0.0
        self._onGround = self.y == 320

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

    def startJump(self):
        if self.onGround():
            self.jump.reset()
            self.velocityY = -JUMP_SPEED
        elif self.velocityY > 0:
            self.jump.reactivate()

    def stopJump(self):
        self.jump.deactivate()

    def onGround(self):
        return self._onGround
