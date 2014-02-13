import game
from sprite import Sprite

class TileType:
    AIR_TILE = 0
    WALL_TILE = 1
    COUNT = 2

class Tile:
    def __init__(self, tileType=TileType.AIR_TILE, sprite=None):
        self.tileType = tileType
        self.sprite = sprite

class CollisionTile:
    def __init__(self, row, col, tileType):
        self.row = row
        self.col = col
        self.tileType = tileType

class Map:
    def __init__(self):
        self.tiles = []

    @staticmethod
    def createTestMap(graphics):
        ret = Map()

        numRows = 15 # 15 * 32 = 480
        numCols = 20 # 20 * 32 = 640
        # Ensure tiles is numRows x numCols in size
        ret.tiles = [[Tile() for _ in range(numCols)] for _ in range(numRows)]

        sprite = Sprite(graphics,
                        b'content/PrtCave.bmp',
                        game.TILE_SIZE, 0,
                        game.TILE_SIZE, game.TILE_SIZE)
        tile = Tile(TileType.WALL_TILE, sprite)
        row = 11
        for col in range(numCols):
            ret.tiles[row][col] = tile
        ret.tiles[10][5] = tile
        ret.tiles[9][4] = tile
        ret.tiles[8][3] = tile
        ret.tiles[7][2] = tile
        ret.tiles[10][3] = tile

        return ret

    def getCollidingTiles(self, rectangle):
        firstRow = rectangle.top() // game.TILE_SIZE
        lastRow = rectangle.bottom() // game.TILE_SIZE
        firstCol = rectangle.left() // game.TILE_SIZE
        lastCol = rectangle.right() // game.TILE_SIZE

        collisionTiles = []
        for row in range(firstRow, lastRow + 1):
            for col in range(firstCol, lastCol + 1):
                tileType = self.tiles[row][col].tileType
                collisionTiles.append(CollisionTile(row, col, tileType))

        return collisionTiles

    def update(self, elapsedTime):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].sprite:
                    self.tiles[row][col].sprite.update(elapsedTime)

    def draw(self, graphics):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].sprite:
                    self.tiles[row][col].sprite.draw(
                            graphics, col*game.TILE_SIZE, row*game.TILE_SIZE)
