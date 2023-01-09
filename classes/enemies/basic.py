import pymunk
import pymunk.pygame_util


class BasicEnemy:
    body = pymunk.Body()
    body.position = (300, 300)
    color = (255, 0, 0, 100)

    def __init__(self, space, radius):
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.mass = radius / 2
        self.shape.color = self.color
        space.add(self.body, self.shape)

