import pygame
import pymunk
import pymunk.pygame_util
from functions.math import get_distance

import math

BULLETS_TYPES = {
    "light": {
        "size": 4,
        "speed": 13,
        "damage": 3,
        "color": (247, 111, 84)
    },
    "medium": {
        "size": 6,
        "speed": 10,
        "damage": 6,
        "color": (92, 91, 91)
    },
    "heavy": {
        "size": 10,
        "speed": 8,
        "damage": 12,
        "color": (168, 44, 44)
    }
}


class Bullet:

    def __init__(self, game, bullet_type, pos, angle, owner):
        self.game = game
        self.body = pymunk.Body()
        self.body.position = pos
        # self.body.filter = pymunk.ShapeFilter(categories=self.game.collision_types["PROJECTILE"], mask=0b11110)
        self.size = bullet_type["size"]
        self.damage = bullet_type["damage"]
        self.color = bullet_type["color"]

        self.xs = -math.cos(angle)
        self.ys = -math.sin(angle)
        self.s = bullet_type["speed"]

        self.shape = pymunk.Circle(self.body, self.size)
        self.shape.collision_type = game.collision_types["PROJECTILE"]
        self.shape.mass = 1
        self.shape.elasticity = 0.01
        self.shape.color = self.color

        game.space.add(self.body, self.shape)

        self.bullet_owner = owner # player | enemy

        self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA, 32)
        self.surface = self.surface.convert_alpha()
        self.rect = self.surface.get_rect()

    def draw(self):
        pygame.draw.circle(self.surface, (0, 0, 0), (self.size, self.size), self.size)
        pygame.draw.circle(self.surface, self.color, (self.size, self.size), self.size - 1)
        self.rect.center = self.game.get_position_by_player(self.body.position)
        new_rect = self.surface.get_rect(center=self.rect.center)
        self.game.window.blit(self.surface, new_rect)

    def movement(self):
        self.body.position = (self.body.position[0] + self.xs * self.s, self.body.position[1] + self.ys * self.s)

    def range_despawn(self):
        if get_distance(self.body.position, self.game.player.body.position) > self.game.player_start_cord["x"] + 250:
            self.game.projectiles.pop(self.game.projectiles.index(self))
        return

    def __del__(self):
        self.game.space.remove(self.body, self.shape)

class LightBullet(Bullet):
    def __init__(self, game, pos, angle, owner):
        super().__init__(game, BULLETS_TYPES["light"], pos, angle, owner)


class MediumBullet(Bullet):
    def __init__(self, game, pos, angle, owner):
        super().__init__(game, BULLETS_TYPES["medium"], pos, angle, owner)

