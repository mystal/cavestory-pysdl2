# TODO: consider making a namedtuple?
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x # units.Game
        self.y = y # units.Game
        self.width = width # units.Game
        self.height = height # units.Game

    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def collidesWith(self, other):
        return (self.right() >= other.left() and
                self.left() <= other.right() and
                self.top() <= other.bottom() and
                self.bottom() >= other.top())
