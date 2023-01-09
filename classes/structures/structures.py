import pymunk
import pymunk.pygame_util


class Wall:
    color = (255, 0, 255, 100)
    body = pymunk.Body(body_type=pymunk.Body.STATIC)

    def __init__(self, space, pos, size, **other):
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 0.4
        self.shape.friction = 1
        color = other.get("color", None)
        if color is not None:
            self.color = color
            self.shape.color = color
        space.add(self.body, self.shape)