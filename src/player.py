from collections import namedtuple

from map import TileType
from rectangle import Rectangle
from sprite import Sprite, AnimatedSprite
import units

# Walk Motion
WALKING_ACCELERATION = 0.00083007812 # units.Acceleration
MAX_SPEED_X = 0.15859375 # units.Velocity
FRICTION = 0.00049804687 # units.Acceleration

# Fall Motion
GRAVITY = 0.00078125 # units.Acceleration
MAX_SPEED_Y = 0.2998046875 # units.Velocity

# Jump Motion
JUMP_SPEED = 0.25 # units.Velocity
AIR_ACCELERATION = 0.0003125 # units.Acceleration
JUMP_GRAVITY = 0.0003125 # units.Acceleration

# Sprites
SPRITE_FILE_PATH = b'assets/MyChar.bmp'

# Sprite Frames
CHARACTER_FRAME = 0 # Which Quote "costume" to use

WALK_FRAME = 0 # units.Frame
STAND_FRAME = 0 # units.Frame
JUMP_FRAME = 1 # units.Frame
FALL_FRAME = 2 # units.Frame
UP_FRAME_OFFSET = 3 # units.Frame
DOWN_FRAME = 6 # units.Frame
BACK_FRAME = 7 # units.Frame

# Walk Animation
NUM_WALK_FRAMES = 3 # units.Frame
WALK_FPS = 15 # units.FPS

# Collision Rectangle
COLLISION_X = Rectangle(6, 10, 20, 12) # units.Game
COLLISION_Y = Rectangle(10, 2, 12, 30) # units.Game

class MotionType:
    STANDING = 0
    INTERACTING = 1
    WALKING = 2
    JUMPING = 3
    FALLING = 4
    COUNT = 5

class HorizontalFacing:
    LEFT = 0
    RIGHT = 1
    COUNT = 2

class VerticalFacing:
    UP = 0
    DOWN = 1
    HORIZONTAL = 2
    COUNT = 3

def getWallCollisionInfo(map, rectangle):
    collided = False
    row = col = 0

    tiles = map.getCollidingTiles(rectangle)
    for tile in tiles:
        if tile.tileType == TileType.WALL_TILE:
            collided = True
            row = tile.row # units.Tile
            col = tile.col # units.Tile
            break

    return (collided, row, col)

class SpriteState(namedtuple('SpriteState',
                             ['motionType',
                              'horizontalFacing',
                              'verticalFacing'])):
    def __new__(cls, motionType=MotionType.STANDING,
                horizontalFacing=HorizontalFacing.LEFT,
                verticalFacing=VerticalFacing.HORIZONTAL):
        return super().__new__(
                cls, motionType, horizontalFacing, verticalFacing)

class Player:
    def __init__(self, graphics, x, y):
        self.x = x # units.Game
        self.y = y # units.Game
        self.velocityX = 0.0 # units.Velocity
        self.velocityY = 0.0 # units.Velocity
        self.accelerationX = 0

        self.horizontalFacing = HorizontalFacing.LEFT
        self.verticalFacing = VerticalFacing.HORIZONTAL
        self._onGround = False

        self.jumpActive = False
        self.interacting = False

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
            tileY = CHARACTER_FRAME
        else:
            tileY = (CHARACTER_FRAME + 1)

        if spriteState.motionType == MotionType.WALKING:
            tileX = WALK_FRAME
        elif spriteState.motionType == MotionType.STANDING:
            tileX = STAND_FRAME
        elif spriteState.motionType == MotionType.INTERACTING:
            tileX = BACK_FRAME
        elif spriteState.motionType == MotionType.JUMPING:
            tileX = JUMP_FRAME
        elif spriteState.motionType == MotionType.FALLING:
            tileX = FALL_FRAME
        else:
            # TODO: error!
            pass

        if spriteState.verticalFacing == VerticalFacing.UP:
            tileX += UP_FRAME_OFFSET

        if spriteState.motionType == MotionType.WALKING:
            self.sprites[spriteState] = AnimatedSprite(
                graphics, SPRITE_FILE_PATH,
                units.tileToPixel(tileX), units.tileToPixel(tileY),
                units.tileToPixel(1), units.tileToPixel(1),
                WALK_FPS, NUM_WALK_FRAMES)
        else:
            if (spriteState.verticalFacing == VerticalFacing.DOWN and
                spriteState.motionType in (MotionType.JUMPING, MotionType.FALLING)):
                tileX = DOWN_FRAME
            self.sprites[spriteState] = Sprite(
                graphics, SPRITE_FILE_PATH,
                units.tileToPixel(tileX), units.tileToPixel(tileY),
                units.tileToPixel(1), units.tileToPixel(1))

    def getSpriteState(self):
        if self.interacting:
            motion = MotionType.INTERACTING
        elif self.onGround():
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

        self.updateX(elapsedTime, map)
        self.updateY(elapsedTime, map)

    def updateX(self, elapsedTime, map):
        # Update Velocity
        accelerationX = (WALKING_ACCELERATION if self.onGround()
                                              else AIR_ACCELERATION)
        self.velocityX += self.accelerationX * accelerationX * elapsedTime

        if self.accelerationX < 0:
            self.velocityX = max(self.velocityX, -MAX_SPEED_X)
        elif self.accelerationX > 0:
            self.velocityX = min(self.velocityX, MAX_SPEED_X)
        elif self._onGround:
            if self.velocityX > 0:
                self.velocityX = max(0.0, self.velocityX - FRICTION * elapsedTime)
            else:
                self.velocityX = min(0.0, self.velocityX + FRICTION * elapsedTime)

        # Calculate Delta
        delta = self.velocityX * elapsedTime # units.Game
        if delta > 0:
            # Check collision in the direction of delta
            collided, row, col = getWallCollisionInfo(
                    map, self.rightCollision(delta))
            # React to collision
            if collided:
                self.x = units.tileToGame(col) - COLLISION_X.right()
                self.velocityX = 0
            else:
                self.x += delta

            # Check collision in other direction
            collided, row, col = getWallCollisionInfo(
                    map, self.leftCollision(0))
            if collided:
                self.x = units.tileToGame(col) + COLLISION_X.right()
        else:
            # Check collision in the direction of delta
            collided, row, col = getWallCollisionInfo(
                    map, self.leftCollision(delta))
            # React to collision
            if collided:
                self.x = units.tileToGame(col) + COLLISION_X.right()
                self.velocityX = 0
            else:
                self.x += delta

            # Check collision in other direction
            collided, row, col = getWallCollisionInfo(
                    map, self.rightCollision(0))
            if collided:
                self.x = units.tileToGame(col) - COLLISION_X.right()

    def updateY(self, elapsedTime, map):
        # Update Velocity
        gravity = (JUMP_GRAVITY if self.jumpActive and self.velocityY < 0
                                else GRAVITY)
        self.velocityY += gravity * elapsedTime
        self.velocityY = min(self.velocityY, MAX_SPEED_Y)

        # Calculate Delta
        delta = self.velocityY * elapsedTime # units.Game
        if delta > 0:
            # Check collision in the direction of delta
            collided, row, col = getWallCollisionInfo(
                    map, self.bottomCollision(delta))
            # React to collision
            if collided:
                self.y = units.tileToGame(row) - COLLISION_Y.bottom()
                self.velocityY = 0
                self._onGround = True
            else:
                self.y += delta
                self._onGround = False

            # Check collision in other direction
            collided, row, col = getWallCollisionInfo(
                    map, self.topCollision(0))
            if collided:
                self.y = units.tileToGame(row) + COLLISION_Y.height
        else:
            # Check collision in the direction of delta
            collided, row, col = getWallCollisionInfo(
                    map, self.topCollision(delta))
            # React to collision
            if collided:
                self.y = units.tileToGame(row) + COLLISION_Y.height
                self.velocityY = 0
            else:
                self.y += delta
                self._onGround = False

            # Check collision in other direction
            collided, row, col = getWallCollisionInfo(
                    map, self.bottomCollision(0))
            if collided:
                self.y = units.tileToGame(row) - COLLISION_Y.bottom()
                self._onGround = True

    def draw(self, graphics):
        self.sprites[self.getSpriteState()].draw(graphics, self.x, self.y)

    def startMovingLeft(self):
        self.accelerationX = -1
        self.horizontalFacing = HorizontalFacing.LEFT
        self.interacting = False

    def startMovingRight(self):
        self.accelerationX = 1
        self.horizontalFacing = HorizontalFacing.RIGHT
        self.interacting = False

    def stopMoving(self):
        self.accelerationX = 0

    def lookUp(self):
        self.verticalFacing = VerticalFacing.UP
        self.interacting = False

    def lookDown(self):
        if self.verticalFacing == VerticalFacing.DOWN:
            return
        self.verticalFacing = VerticalFacing.DOWN
        self.interacting = self.onGround()

    def lookHorizontal(self):
        self.verticalFacing = VerticalFacing.HORIZONTAL

    def startJump(self):
        self.jumpActive = True
        if self.onGround():
            self.velocityY = -JUMP_SPEED
        self.interacting = False

    def stopJump(self):
        self.jumpActive = False

    def onGround(self):
        return self._onGround

    def damageRect(self):
        return Rectangle(self.x + COLLISION_X.left(),
                         self.y + COLLISION_Y.top(),
                         COLLISION_X.width,
                         COLLISION_Y.height)

    def centerX(self):
        return self.x + units.tileToGame(1) / 2
