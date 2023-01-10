import os
import math

import pymunk
import pymunk.pygame_util
import pygame




class Player:
    body = pymunk.Body()
    color = (111, 56, 214, 100)
    radius = 50
    angle = 0
    original_image = pygame.image.load(os.path.join("imgs", "player.png"))
    image = pygame.transform.scale(original_image, (radius * 2, radius * 2))

    rect = image.get_rect()

    PLAYER_SPEED_LIMIT = 350

    def __init__(self, space, pos):
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.8
        # self.shape.friction = 0.1
        self.shape.mass = self.radius / 10
        self.shape.color = self.color
        self.rect.center = self.body.position[0], self.body.position[1] #self.body.position[0] - self.radius, self.body.position[1] - self.radius

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

    def update(self, game):
        game.camera["x"] = self.body.position.x
        game.camera["y"] = self.body.position.y
        self.rect.center = self.body.position
        self.image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(game.mouse_angle) + 180)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        game.window.blit(rotated_image, new_rect)
