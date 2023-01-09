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
        self.shape.elasticity = 1.2
        # self.shape.friction = 0.1
        self.shape.mass = self.radius / 10
        self.shape.color = self.color
        space.add(self.body, self.shape)
    def move_player(self, inputs):
        hor_speed = self.body.velocity
        # print(hor_speed)
        if inputs["A"]:
            self.body.apply_force_at_local_point((-1000, 0), (0, 0))
        if inputs["D"]:
            self.body.apply_force_at_local_point((1000, 0), (0, 0))
        print(self.body.velocity)