from animated_sprite import AnimatedSprite
import game

SLOWDOWN_FACTOR = 0.8
WALKING_ACCELERATION = 0.0012 # (pixels / ms) / ms
MAX_SPEED_X = 0.325 # pixels / ms

class Player:
    def __init__(self, graphics, x, y):
        self.x = x
        self.y = y
        self.velocityX = 0.0
        self.accelerationX = 0.0
        self.sprite = AnimatedSprite(graphics, b'content/MyChar.bmp', 0, 0,
                                     game.TILE_SIZE, game.TILE_SIZE, 15, 3)

    def update(self, elapsedTime):
        self.sprite.update(elapsedTime)

        self.x += round(self.velocityX * elapsedTime)
        self.velocityX += self.accelerationX * elapsedTime

        if self.accelerationX > 0:
            self.velocityX = max(self.velocityX, -MAX_SPEED_X)
        elif self.accelerationX < 0:
            self.velocityX = min(self.velocityX, MAX_SPEED_X)
        else:
            self.velocityX *= SLOWDOWN_FACTOR

    def draw(self, graphics):
        self.sprite.draw(graphics, self.x, self.y)

    def startMovingLeft(self):
        self.accelerationX = -WALKING_ACCELERATION

    def startMovingRight(self):
        self.accelerationX = WALKING_ACCELERATION

    def stopMoving(self):
        self.accelerationX = 0

    def cleanUp(self):
        self.sprite.cleanUp()
