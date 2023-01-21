import pygame
import pymunk
import pymunk.pygame_util
from functions.math import get_distance
from functions.angle import get_angle

import os
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

class KnifeAttack:
    def __init__(self, game, body, angle, owner, attack_time):
        self.game = game
        self.sticked_body = body
        self.pos = (0, 0)
        self.body = pymunk.Body()
        self.body.position = self.pos
        # self.body.filter = pymunk.ShapeFilter(categories=self.game.collision_types["PROJECTILE"], mask=0b11110)
        self.size = (90, 30)
        self.damage = 5

        self.xs = -math.cos(angle)
        self.ys = -math.sin(angle)
        self.s = 10

        self.reverse_counter = 0
        self.reverse_counter_breakpoint = attack_time / 2
        self.is_reversing = False

        self.initial_angle = get_angle((self.game.player_start_cord["x"] + self.xs,
                                      self.game.player_start_cord["y"] + self.ys),
                                     (self.game.player_start_cord["x"],
                                      self.game.player_start_cord["y"]))

        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.collision_type = game.collision_types["PROJECTILE"]
        self.shape.mass = 1
        self.shape.elasticity = 0.01

        game.space.add(self.body, self.shape)

        self.bullet_owner = owner # player | enemy

        self.original_image = pygame.image.load(os.path.join("imgs", "knife.png"))
        self.image = pygame.transform.scale(self.original_image, self.size)
        self.rect = self.image.get_rect()

    def draw(self):
        self.rect.center = self.game.get_position_by_player(self.body.position)
        self.image = pygame.transform.scale(self.image, self.size)
        rotated_image = pygame.transform.rotate\
            (self.image,
             -math.degrees(self.initial_angle) + 180)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        self.game.window.blit(rotated_image, new_rect)

    def movement(self):
        if self.reverse_counter >= self.reverse_counter_breakpoint and not self.is_reversing:
            self.is_reversing = True
            self.reverse_counter = 0
            self.xs *= -1
            self.ys *= -1
        elif self.reverse_counter >= self.reverse_counter_breakpoint and self.is_reversing:
            self.game.projectiles.remove(self)
        self.pos = (self.pos[0] + self.xs * self.s, self.pos[1] + self.ys * self.s)
        self.body.position = (self.sticked_body.position[0] + self.pos[0], self.sticked_body.position[1] + self.pos[1])
        self.reverse_counter += 1

    def range_despawn(self):
        if get_distance(self.body.position, self.game.player.body.position) > self.game.player_start_cord["x"] + 250:
            self.game.projectiles.pop(self.game.projectiles.index(self))
        return

    def __del__(self):
        self.game.space.remove(self.body, self.shape)