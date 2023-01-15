import pymunk
import pymunk.pygame_util
import pygame
import os

class BasicEnemy():
    color = (255, 250, 0, 100)
    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))

    def __init__(self, game, space, radius, pos):
        self.body = pymunk.Body()
        self.body.position = pos
        self.radius = radius
        self.image = pygame.transform.scale(self.original_image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect()
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.collision_type = game.collision_types["ENEMY"]
        self.shape.elasticity = 0.8
        self.shape.friction = 1
        self.shape.mass = radius / 10
        self.shape.color = self.color
        space.add(self.body, self.shape)

    def update(self, game):
        self.rect.center = game.get_position_by_player(self.body.position)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)