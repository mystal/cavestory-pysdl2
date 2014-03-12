from sprite import Sprite
import units

SPRITE_PATH = b'assets/TextBox.bmp'

SOURCE_Y = units.gameToPixel(7 * units.HALF_TILE) # units.Game
SOURCE_WIDTH = units.HALF_TILE # units.Game
SOURCE_HEIGHT = units.HALF_TILE # units.Game

RADIX = 10

class NumberSprite:
    def __init__(self, graphics, number, numDigits=0):
        # If numDigits is 0, we ignore it
        assert number >= 0

        # Sprites are stored in reverse order
        # e.g. for 1234, sprites = [4, 3, 2, 1]
        self.sprites = []

        digit = number % RADIX
        self.sprites.append(Sprite(
                graphics, SPRITE_PATH,
                units.gameToPixel(digit * units.HALF_TILE),
                units.gameToPixel(SOURCE_Y),
                units.gameToPixel(SOURCE_WIDTH),
                units.gameToPixel(SOURCE_HEIGHT)))
        number //= RADIX
        while number != 0:
            digit = number % RADIX
            self.sprites.append(Sprite(
                    graphics, SPRITE_PATH,
                    units.gameToPixel(digit * units.HALF_TILE),
                    units.gameToPixel(SOURCE_Y),
                    units.gameToPixel(SOURCE_WIDTH),
                    units.gameToPixel(SOURCE_HEIGHT)))
            number //= RADIX

        if numDigits > 0:
            digitCount = len(self.sprites)
            assert numDigits >= digitCount
            self.padding = units.HALF_TILE * (numDigits - digitCount)
        else:
            self.padding = 0

    def draw(self, graphics, gameX, gameY):
        for i, sprite in enumerate(self.sprites):
            offset = units.HALF_TILE * (len(self.sprites) - 1 - i)
            sprite.draw(graphics, gameX + offset + self.padding, gameY)
