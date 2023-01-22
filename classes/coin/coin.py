import os

import pygame
import pymunk
import pymunk.pygame_util


class Coin:

    radius = 20
    value = 10

    original_image = pygame.image.load(os.path.join("imgs", "coin.png"))
    image = pygame.transform.scale(original_image, (radius * 2, radius * 2))

    def __init__(self, game, pos):
        self.game = game
        self.body = pymunk.body.Body()
        self.body.position = pos
        self.shape = pymunk.shapes.Circle(self.body, self.radius)
        self.shape.collision_type = game.collision_types["COIN"]
        self.shape.elasticity = 0.8
        self.shape.friction = 1
        self.shape.mass = 0.1
        self.game.space.add(self.body, self.shape)
        self.rect = self.image.get_rect()

    def draw(self):
        # image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))
        # self.game.window.blit(self.image, self.game.get_position_by_player(self.body.position))
        self.rect.center = self.game.get_position_by_player(self.body.position)
        new_rect = self.image.get_rect(center=self.rect.center)
        self.game.window.blit(self.image, new_rect)

    def __del__(self):
        self.game.space.remove(self.body, self.shape)