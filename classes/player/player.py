import pymunk
import pymunk.pygame_util


class Player:
    body = pymunk.Body()
    color = (111, 56, 214, 100)
    radius = 50

    PLAYER_SPEED_LIMIT = 350

    def __init__(self, space, pos):
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.8
        # self.shape.friction = 0.1
        self.shape.mass = self.radius / 10
        self.shape.color = self.color
        space.add(self.body, self.shape)
    def move_player(self, inputs):
        hor_speed = self.body.velocity
        # print(self.body.position)
        if inputs["A"]:
            # self.body.position = (self.body.position.x - 5, self.body.position.y)
            self.body.apply_force_at_local_point((-2500, 0), (0, 0))
        if inputs["D"]:
            # self.body.position = (self.body.position.x + 5, self.body.position.y)
            self.body.apply_force_at_local_point((2500, 0), (0, 0))
        if inputs["W"]:
            # self.body.position = (self.body.position.x, self.body.position.y - 5)
            self.body.apply_force_at_local_point((0, -2500), (0, 0))
        if inputs["S"]:
            # self.body.position = (self.body.position.x, self.body.position.y + 5)
            self.body.apply_force_at_local_point((0, 2500), (0, 0))

