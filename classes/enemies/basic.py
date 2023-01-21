import pymunk
import pymunk.pygame_util
import pygame
from classes.ammo.ammo_box import AmmoBox
from classes.coin.coin import Coin

import os
import random
import math

class Node:
    def __init__(self):
        self.nodes = []


class Graph:
    def __init__(self, game):
        self.map = []
        self.max_length = game.MAP_TILES_LENGTH
        for i in range(len(game.map)):
            self.map.append([])
            for k in range(len(game.map[i])):
                self.map[i].append(Node())
        for i in range(len(game.map)):
            for k in range(len(game.map[i])):
                if self.check_index_range(k - 1) and game.map[i][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i][k - 1], 1))
                if self.check_index_range(k + 1) and game.map[i][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i][k + 1], 1))
                if self.check_index_range(i - 1) and game.map[i - 1][k] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k], 1))
                if self.check_index_range(i + 1) and game.map[i + 1][k] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k], 1))
                if self.check_index_range(k - 1) and self.check_index_range(i - 1) and game.map[i][k - 1] == 0 and game.map[i - 1][k] == 0 and game.map[i - 1][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k - 1], math.sqrt(2)))
                if self.check_index_range(k + 1) and self.check_index_range(i - 1) and game.map[i][k + 1] == 0 and game.map[i - 1][k] == 0 and game.map[i - 1][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k + 1], math.sqrt(2)))
                if self.check_index_range(k + 1) and self.check_index_range(i + 1) and game.map[i][k + 1] == 0 and game.map[i + 1][k] == 0 and game.map[i + 1][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k + 1], math.sqrt(2)))
                if self.check_index_range(k - 1) and self.check_index_range(i + 1) and game.map[i][k - 1] == 0 and game.map[i + 1][k] == 0 and game.map[i + 1][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k - 1], math.sqrt(2)))

    def check_index_range(self, index):
        return 0 <= index < self.max_length

    def neighbours(self, node):
        return node.nodes


class Enemy:
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
        if random.random() > 0.6:
            self.game.ground_items.append(AmmoBox(self.game, self.body.position, "medium", random.randrange(1, 6)))
        for i in range(4):
            self.game.coins.append(Coin(self.game,
                                        (self.body.position.x + 100 * (random.random() - 0.5),
                                         self.body.position.y + (100 * random.random() * 0.5))))
        self.game.space.remove(self.body, self.shape)

    def special_attack(self):
        pass

class BasicEnemy(Enemy):
    color = (255, 250, 0, 100)
    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))
    collision_damage = 5

    spawn_cost = 2

    def __init__(self, game, space, radius, pos):
        super().__init__(game, space, radius, pos)
        self.max_hp = 15
        self.hp = 15
