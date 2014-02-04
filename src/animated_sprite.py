from sprite import Sprite

class AnimatedSprite(Sprite):
    def __init__(self, graphics, filePath, sourceX, sourceY, width, height,
                 fps, numFrames):
        super().__init__(graphics, filePath, sourceX, sourceY, width, height)
        self.frameTime = 1000 // fps
        self.numFrames = numFrames
        self.currentFrame = 0
        self.elapsedTime = 0 # Elapsed time since last frame change

    def update(self, elapsedTime):
        self.elapsedTime += elapsedTime
        if self.elapsedTime > self.frameTime:
            self.currentFrame += 1
            self.elapsedTime = 0

            # Move the source rectangle in the sprite sheet
            if self.currentFrame < self.numFrames:
                self.sourceRect.x += self.sourceRect.w
            else:
                self.sourceRect.x -= self.sourceRect.w * (self.numFrames - 1)
                self.currentFrame = 0
