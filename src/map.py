import backdrop
from graphics import TILE_SIZE
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
        self.backdrop = None
        self.tiles = []
        self.backgroundTiles = []

    @staticmethod
    def createTestMap(graphics):
        ret = Map()

        ret.backdrop = backdrop.FixedBackdrop(b'assets/bkBlue.bmp', graphics)

        numRows = 15 # 15 * 32 = 480
        numCols = 20 # 20 * 32 = 640
        # Ensure tiles and backgroundTiles are numRows x numCols in size
        ret.tiles = [[Tile() for _ in range(numCols)] for _ in range(numRows)]
        ret.backgroundTiles = [[None for _ in range(numCols)] for _ in range(numRows)]

        sprite = Sprite(graphics,
                        b'assets/PrtCave.bmp',
                        TILE_SIZE, 0,
                        TILE_SIZE, TILE_SIZE)
        tile = Tile(TileType.WALL_TILE, sprite)
        row = 11
        for col in range(numCols):
            ret.tiles[row][col] = tile
        ret.tiles[10][5] = tile
        ret.tiles[9][4] = tile
        ret.tiles[8][3] = tile
        ret.tiles[7][2] = tile
        ret.tiles[10][3] = tile

        chainTop = Sprite(graphics,
                          b'assets/PrtCave.bmp',
                          11*TILE_SIZE, 2*TILE_SIZE,
                          TILE_SIZE, TILE_SIZE)
        chainMiddle = Sprite(graphics,
                             b'assets/PrtCave.bmp',
                             12*TILE_SIZE, 2*TILE_SIZE,
                             TILE_SIZE, TILE_SIZE)
        chainBottom = Sprite(graphics,
                             b'assets/PrtCave.bmp',
                             13*TILE_SIZE, 2*TILE_SIZE,
                             TILE_SIZE, TILE_SIZE)

        ret.backgroundTiles[8][2] = chainTop
        ret.backgroundTiles[9][2] = chainMiddle
        ret.backgroundTiles[10][2] = chainBottom

        return ret

    def getCollidingTiles(self, rectangle):
        firstRow = rectangle.top() // TILE_SIZE
        lastRow = rectangle.bottom() // TILE_SIZE
        firstCol = rectangle.left() // TILE_SIZE
        lastCol = rectangle.right() // TILE_SIZE

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

    def drawBackground(self, graphics):
        self.backdrop.draw(graphics)
        for row in range(len(self.backgroundTiles)):
            for col in range(len(self.backgroundTiles[row])):
                if self.backgroundTiles[row][col]:
                    self.backgroundTiles[row][col].draw(
                            graphics, col*TILE_SIZE, row*TILE_SIZE)

    def draw(self, graphics):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].sprite:
                    self.tiles[row][col].sprite.draw(
                            graphics, col*TILE_SIZE, row*TILE_SIZE)
