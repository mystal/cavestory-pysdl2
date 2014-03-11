# Types
#float Game # Float for extra position. Intrinsic units of position.
#int Pixel # Integer for discrete units for the screen. Pixel values can be positive or negative.
#unsigned int Tile # Also discrete, but non-negative.
#unsigned int Frame # Discrete. Non-negative.

#float Velocity # Games / MS
#float Acceleration # Games / MS^2

#unsigned int MS # Discrete Milliseconds.
#unsigned int FPS # Frames per second (Hz, 1 / Second)

# Constants
TILE_SIZE = 32 # Pixels

# Conversion functions
def gameToPixel(game):
    # TODO: stop assuming 16x16
    return round(game / 2)

def gameToTile(game):
    return int(game / TILE_SIZE)

def tileToGame(tile):
    return float(tile * TILE_SIZE)

def tileToPixel(tile):
    return gameToPixel(tileToGame(tile))
