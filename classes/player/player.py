import os
import math

import pymunk
import pymunk.pygame_util
import pygame
from pygame.math import Vector2


class Player:
    body = pymunk.Body()
    color = (111, 56, 214, 100)
    radius = 50
    angle = 0
    original_image = pygame.image.load(os.path.join("imgs", "player.png"))
    image = pygame.transform.scale(original_image, (radius * 2, radius * 2))

    rect = image.get_rect()

    PLAYER_SPEED_LIMIT = 350

    max_hp = 50
    hp = 50

    health_bar_size = (350, 40)
    health_bar = pygame.surface.Surface(health_bar_size)

    def __init__(self, game, space, pos):
        self.game = game
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.collision_type = game.collision_types["PLAYER"]
        self.shape.elasticity = 0.8
        # self.shape.friction = 1
        self.shape.mass = self.radius / 10
        self.shape.color = self.color
        self.rect.center = self.body.position[0], self.body.position[1] #self.body.position[0] - self.radius, self.body.position[1] - self.radius

        space.add(self.body, self.shape)

        self.immune = False
        self.immunity_timer = 0

    def move_player(self, inputs):
        if inputs["A"]:
            # self.body.position = (self.body.position.x - 5, self.body.position.y)
            self.body.apply_force_at_local_point((-1800, 0), (0, 0))
        if inputs["D"]:
            # self.body.position = (self.body.position.x + 5, self.body.position.y)
            self.body.apply_force_at_local_point((1800, 0), (0, 0))
        if inputs["W"]:
            # self.body.position = (self.body.position.x, self.body.position.y - 5)
            self.body.apply_force_at_local_point((0, -1800), (0, 0))
        if inputs["S"]:
            # self.body.position = (self.body.position.x, self.body.position.y + 5)
            self.body.apply_force_at_local_point((0, 1800), (0, 0))

    def display_item_in_hand(self, game, displayed_item):
        if displayed_item is None:
            return
        # rotate_point = Vector2(50, 50)
        #
        # offset = Vector2(-rotate_point.x, -rotate_point.y)
        # translated_image = pygame.Surface.copy(displayed_item.image)
        # translated_image.blit(displayed_item.image, offset)
        #
        rotated_image = pygame.transform.rotate(displayed_item.image, -math.degrees(game.mouse_angle) + 180)
        #
        # offset = Vector2(rotate_point.x, rotate_point.y)
        # rotated_image = pygame.Surface.copy(rotated_image)
        # rotated_image.blit(rotated_image, offset)

        new_rect = rotated_image.get_rect(center=self.rect.center)
        game.window.blit(rotated_image, new_rect)

    def show_hp(self):
        pygame.draw.rect(self.health_bar, (0, 0, 0), (0, 0, self.health_bar_size[0], self.health_bar_size[1]))
        pygame.draw.rect(self.health_bar, (35, 189, 26), (2, 2, (self.health_bar_size[0] - 4) * (self.hp / self.max_hp),
                                                          self.health_bar_size[1] - 4))
        self.game.window.blit(self.health_bar, (self.game.window.get_width() - self.health_bar_size[0], 0))

    def after_damage_immunity(self):
        self.immune = True

    def immunity_delay(self):
        if self.immunity_timer < 100:
            self.immunity_timer += 1.5
        else:
            self.immune = False
            self.immunity_timer = 0

    def update(self, game):
        game.camera["x"] = self.body.position.x
        game.camera["y"] = self.body.position.y
        self.rect.center = (game.window.get_width() / 2, game.window.get_height() / 2)
        self.image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))
        rotated_image = pygame.transform.rotate(self.image, -math.degrees(game.mouse_angle) + 180)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        game.window.blit(rotated_image, new_rect)
