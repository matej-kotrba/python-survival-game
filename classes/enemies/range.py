import os
import random

import pygame
import pymunk
from classes.enemies.basic import Enemy
from classes.ammo.bullet import MediumBullet
from functions.angle import get_angle
from functions.math import get_distance

class RangeEnemy(Enemy):
    color = (255, 250, 0, 100)
    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))
    collision_damage = 2

    spawn_cost = 3

    def __init__(self, game, space, radius, pos):
        super().__init__(game, space, radius, pos)
        self.max_hp = 10
        self.hp = 10
        self.special_attack_charge = 100
        self.special_attack_charge_current = 0

    def special_attack(self):
        if get_distance(self.body.position, self.game.player.body.position) < self.game.window.get_width()/2 + 100 and self.special_attack_charge_current >= self.special_attack_charge:
            self.game.projectiles.append(MediumBullet(self.game, self.body.position,
                                                      get_angle(self.game.player.body.position,
                                                                self.body.position) + (random.random() - 0.5) * 0.3, "enemy"))
            self.special_attack_charge_current = 0
        else:
            self.special_attack_charge_current += 1
