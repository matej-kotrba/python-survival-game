import pymunk
import pymunk.pygame_util
import pygame
from classes.ammo.ammo_box import AmmoBox
from classes.coin.coin import Coin

import os
import random
import math
from functions.math import get_xys, get_distance

class Enemy:
    def __init__(self, game, space, radius, pos):
        self.game = game
        self.body = pymunk.Body()
        self.body.position = pos
        self.radius = 20
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

        self.s = 3

        # IMPLEMENTING PATH FINDING
        # self.graph = graph
        self.game.graph.A_star(
            self.game.graph.map[round(self.body.position[0] // self.game.TILE_SIZE)][
                round(self.body.position[1] // self.game.TILE_SIZE)],
            self.game.graph.map[round(self.game.player.body.position[0] // self.game.TILE_SIZE)][
                round(self.game.player.body.position[1] // self.game.TILE_SIZE)]
        )
        # print(self.game.graph.A_star(
        #     self.game.graph.map[round(self.body.position[0] // self.game.TILE_SIZE)][
        #         round(self.body.position[1] // self.game.TILE_SIZE)],
        #     self.game.graph.map[round(self.game.player.body.position[0] // self.game.TILE_SIZE)][
        #         round(self.game.player.body.position[1] // self.game.TILE_SIZE)]
        # )[self.game.graph.map[round(self.body.position[0] // self.game.TILE_SIZE)][
        #         round(self.body.position[1] // self.game.TILE_SIZE)]])
        self.path = []
        self.create_path()
        print(len(self.path))

    def create_path(self):
        routes = self.game.graph.A_star(
            self.game.graph.map[round(self.body.position[0] // self.game.TILE_SIZE)][
                round(self.body.position[1] // self.game.TILE_SIZE)],
            self.game.graph.map[round(self.game.player.body.position[0] // self.game.TILE_SIZE)][
                round(self.game.player.body.position[1] // self.game.TILE_SIZE)]
        )
        node = routes[self.game.graph.map[round(self.game.player.body.position[0] // self.game.TILE_SIZE)][
                round(self.game.player.body.position[1] // self.game.TILE_SIZE)]]
        while node is not None:
            self.path.append(node)
            node = routes[node]
        self.path.pop()

    def move(self):
        # for item in self.path:
        #     x,y = self.game.get_position_by_player((item.x * self.game.TILE_SIZE,
        #                                                        item.y * self.game.TILE_SIZE))
        #     pygame.draw.rect(self.game.window, (0, 255, 0),
        #                      (round(x), round(y), self.game.TILE_SIZE, self.game.TILE_SIZE))
        self.create_path()
        if len(self.path) <= 0:
            return
        xy = (self.path[-1].x * self.game.TILE_SIZE + self.game.TILE_SIZE / 2, self.path[-1].y * self.game.TILE_SIZE + self.game.TILE_SIZE / 2)
        xs, ys = get_xys(self.body.position, xy)
        self.body.position = (self.body.position.x + xs * self.s, self.body.position.y + ys * self.s)
        if get_distance(self.body.position, xy) < self.radius:
            self.path.pop()

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
