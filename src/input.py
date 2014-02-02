from collections import defaultdict

class Input:
    def __init__(self):
        self.heldKeys = defaultdict(bool)
        self.pressedKeys = defaultdict(bool)
        self.releasedKeys = defaultdict(bool)

    def beginNewFrame(self):
        self.pressedKeys.clear()
        self.releasedKeys.clear()

    def keyDownEvent(self, event):
        self.pressedKeys[event.key.keysym.sym] = True
        self.heldKeys[event.key.keysym.sym] = True

    def keyUpEvent(self, event):
        self.releasedKeys[event.key.keysym.sym] = True
        self.heldKeys[event.key.keysym.sym] = False

    def wasKeyPressed(self, key):
        return self.pressedKeys[key]

    def wasKeyReleased(self, key):
        return self.releasedKeys[key]

    def isKeyHeld(self, key):
        return self.heldKeys[key]
