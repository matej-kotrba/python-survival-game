import pygame
from classes.enemies.basic import BasicEnemy
from classes.enemies.range import RangeEnemy

import math
import random

ALLOWED_ENEMIES = [BasicEnemy, RangeEnemy]

class Wave:
    def __init__(self, game, number):
        self.game = game
        self.number = number
        self.active = False
        self.wave_start_counter = self.game.fps * 2
        self.counter = self.wave_start_counter
        self.points_on_spawn = self.number * 1.4 + 5

        self.overview_surface = pygame.surface.Surface((200, 60))
        self.rect = self.overview_surface.get_rect()

        self.font = pygame.font.Font(None, 22)

    def check_status(self):
        if self.active and self.counter <= 0 and len(self.game.enemies) <= 0:
            self.game.wave = Wave(self.game, self.number + 1)
        elif not self.active and self.counter <= 0:
            self.active = True
            self.counter -= 1
            # SPAWN ENEMIES
            while True:
                available_enemies = [item for item in ALLOWED_ENEMIES if item.spawn_cost <= self.points_on_spawn]
                if len(available_enemies) == 0:
                    break
                enemy_class_to_spawn = available_enemies[round(random.randrange(len(available_enemies))) if len(available_enemies) > 1 else 0]
                location_to_spawn = self.game.spawners[round(random.randrange(len(self.game.spawners))) if len(self.game.spawners) > 1 else 0]
                enemy = enemy_class_to_spawn(self.game, self.game.space, 30, location_to_spawn.pos)
                self.points_on_spawn -= enemy_class_to_spawn.spawn_cost
                self.game.enemies.append(enemy)
        else:
            self.counter -= 1


    def display_overview(self):
        self.overview_surface.fill((53, 53, 53))

        text = self.font.render(f"Wave {self.number}, status - {'ACTIVE' if self.active else math.floor(self.counter / 60)}", True, (255, 255, 255))

        text_rect = text.get_rect()

        self.overview_surface.blit(text, ((200 - text_rect.width) / 2, (60 - text_rect.height / 2) / 2))
        self.game.window.blit(self.overview_surface, (self.game.window.get_width() - self.rect.width,
                              self.game.window.get_height() - self.rect.height))

    def __del__(self):
        print(f"Wave {self.number} has been completed !")