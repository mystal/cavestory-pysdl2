import game
from sprite import Sprite

class Map:
    def __init__(self):
        self.foregroundSprites = []

    @staticmethod
    def createTestMap(graphics):
        ret = Map()

        numRows = 15 # 15 * 32 = 480
        numCols = 20 # 20 * 32 = 640
        # Ensure foregroundSprites is numRows x numCols in size
        ret.foregroundSprites = [[None]*numCols for _ in range(numRows)]

        sprite = Sprite(graphics,
                        b'content/PrtCave.bmp',
                        game.TILE_SIZE, 0,
                        game.TILE_SIZE, game.TILE_SIZE)
        row = 11
        for col in range(numCols):
            ret.foregroundSprites[row][col] = sprite
        ret.foregroundSprites[10][5] = sprite
        ret.foregroundSprites[9][4] = sprite
        ret.foregroundSprites[8][3] = sprite
        ret.foregroundSprites[7][2] = sprite
        ret.foregroundSprites[10][3] = sprite

        return ret

    def update(self, elapsedTime):
        for row in range(len(self.foregroundSprites)):
            for col in range(len(self.foregroundSprites[row])):
                if self.foregroundSprites[row][col]:
                    self.foregroundSprites[row][col].update(elapsedTime)

    def draw(self, graphics):
        for row in range(len(self.foregroundSprites)):
            for col in range(len(self.foregroundSprites[row])):
                if self.foregroundSprites[row][col]:
                    self.foregroundSprites[row][col].draw(
                            graphics, col*game.TILE_SIZE, row*game.TILE_SIZE)
