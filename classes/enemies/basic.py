import pymunk
import pymunk.pygame_util
import pygame
import os

class BasicEnemy():
    color = (255, 250, 0, 100)
    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))

    def __init__(self, game, space, radius, pos):
        self.game = game
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

        self.max_hp = 15
        self.hp = 15

        self.health_bar = pygame.surface.Surface((120, 30))
        self.health_bar_size = (120, 30)

    def update(self, game):
        self.rect.center = game.get_position_by_player(self.body.position)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)

    def show_hp(self, game):
        pygame.draw.rect(self.health_bar, (0, 0, 0), (0, 0, self.health_bar_size[0], self.health_bar_size[1]))
        pygame.draw.rect(self.health_bar, (35, 189, 26), (2, 2, (self.health_bar_size[0] - 4) * (self.hp / self.max_hp),
                                                          self.health_bar_size[1] - 4))
        x, y = game.get_position_by_player(self.body.position)
        game.window.blit(self.health_bar, (x - 60, y - self.radius * 2 - 10))

    def __del__(self):
        self.game.space.remove(self.body, self.shape)