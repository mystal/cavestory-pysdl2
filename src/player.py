from collections import namedtuple

from animated_sprite import AnimatedSprite
import game
from rectangle import Rectangle
from sprite import Sprite

# Walk Motion
SLOWDOWN_FACTOR = 0.8
WALKING_ACCELERATION = 0.0012 # (pixels / ms) / ms
MAX_SPEED_X = 0.325 # pixels / ms

# Fall Motion
GRAVITY = 0.0012 # (pixels / ms) / ms
MAX_SPEED_Y = 0.325 # pixels / ms

# Jump Motion
JUMP_SPEED = 0.325 # pixels / ms
JUMP_TIME = 275 # ms

# Sprites
SPRITE_FILE_PATH = b'content/MyChar.bmp'

# Sprite Frames
CHARACTER_FRAME = 0 # Which Quote "costume" to use

WALK_FRAME = 0
STAND_FRAME = 0
JUMP_FRAME = 1
FALL_FRAME = 2
UP_FRAME_OFFSET = 3
DOWN_FRAME = 6
BACK_FRAME = 7

# Walk Animation
NUM_WALK_FRAMES = 3
WALK_FPS = 15

# Collision Rectangle
COLLISION_X = Rectangle(6, 10, 20, 12)
COLLISION_Y = Rectangle(10, 2, 12, 30)

class MotionType:
    STANDING = 0
    WALKING = 1
    JUMPING = 2
    FALLING = 3
    COUNT = 4

class HorizontalFacing:
    LEFT = 0
    RIGHT = 1
    COUNT = 2

class VerticalFacing:
    UP = 0
    DOWN = 1
    HORIZONTAL = 2
    COUNT = 3

class SpriteState(namedtuple('SpriteState',
                             ['motionType',
                              'horizontalFacing',
                              'verticalFacing'])):
    def __new__(cls, motionType=MotionType.STANDING,
                horizontalFacing=HorizontalFacing.LEFT,
                verticalFacing=VerticalFacing.HORIZONTAL):
        return super().__new__(
                cls, motionType, horizontalFacing, verticalFacing)

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
        self.verticalFacing = VerticalFacing.HORIZONTAL
        self._onGround = False

        self.jump = Jump()

        self.sprites = {}
        self.initializeSprites(graphics)

    def initializeSprites(self, graphics):
        for motionType in range(MotionType.COUNT):
            for horizontalFacing in range(HorizontalFacing.COUNT):
                for verticalFacing in range(VerticalFacing.COUNT):
                    spriteState = SpriteState(motionType,
                                              horizontalFacing,
                                              verticalFacing)
                    self.initializeSprite(graphics, spriteState)

    def initializeSprite(self, graphics, spriteState):
        if spriteState.horizontalFacing == HorizontalFacing.LEFT:
            sourceY = CHARACTER_FRAME * game.TILE_SIZE
        else:
            sourceY = (CHARACTER_FRAME + 1) * game.TILE_SIZE

        if spriteState.motionType == MotionType.WALKING:
            sourceX = WALK_FRAME * game.TILE_SIZE
        elif spriteState.motionType == MotionType.STANDING:
            sourceX = STAND_FRAME * game.TILE_SIZE
        elif spriteState.motionType == MotionType.JUMPING:
            sourceX = JUMP_FRAME * game.TILE_SIZE
        elif spriteState.motionType == MotionType.FALLING:
            sourceX = FALL_FRAME * game.TILE_SIZE
        else:
            # TODO: error!
            pass

        if spriteState.verticalFacing == VerticalFacing.UP:
            sourceX += UP_FRAME_OFFSET * game.TILE_SIZE

        if spriteState.motionType == MotionType.WALKING:
            self.sprites[spriteState] = AnimatedSprite(
                graphics, SPRITE_FILE_PATH, sourceX, sourceY,
                game.TILE_SIZE, game.TILE_SIZE, WALK_FPS, NUM_WALK_FRAMES)
        else:
            if spriteState.verticalFacing == VerticalFacing.DOWN:
                if spriteState.motionType == MotionType.STANDING:
                    sourceX = BACK_FRAME * game.TILE_SIZE
                else:
                    sourceX = DOWN_FRAME * game.TILE_SIZE
            self.sprites[spriteState] = Sprite(
                graphics, SPRITE_FILE_PATH, sourceX, sourceY,
                game.TILE_SIZE, game.TILE_SIZE)

    def getSpriteState(self):
        motion = None
        if self.onGround():
            motion = MotionType.STANDING if self.accelerationX == 0 else MotionType.WALKING
        else:
            motion = MotionType.JUMPING if self.velocityY < 0 else MotionType.FALLING
        return SpriteState(motion, self.horizontalFacing, self.verticalFacing)

    def leftCollision(self, delta):
        assert delta <= 0
        return Rectangle(self.x + COLLISION_X.left() + delta,
                         self.y + COLLISION_X.top(),
                         COLLISION_X.width // 2 - delta,
                         COLLISION_X.height)

    def rightCollision(self, delta):
        assert delta >= 0
        return Rectangle(self.x + COLLISION_X.left() + COLLISION_X.width // 2,
                         self.y + COLLISION_X.top(),
                         COLLISION_X.width // 2 + delta,
                         COLLISION_X.height)

    def topCollision(self, delta):
        assert delta <= 0
        return Rectangle(self.x + COLLISION_Y.left(),
                         self.y + COLLISION_Y.top() + delta,
                         COLLISION_Y.width,
                         COLLISION_Y.height // 2 - delta)

    def bottomCollision(self, delta):
        assert delta >= 0
        return Rectangle(self.x + COLLISION_Y.left(),
                         self.y + COLLISION_Y.top() + COLLISION_Y.height // 2,
                         COLLISION_Y.width,
                         COLLISION_Y.height // 2 + delta)

    def update(self, elapsedTime, map):
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

    def lookUp(self):
        self.verticalFacing = VerticalFacing.UP

    def lookDown(self):
        self.verticalFacing = VerticalFacing.DOWN

    def lookHorizontal(self):
        self.verticalFacing = VerticalFacing.HORIZONTAL

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
