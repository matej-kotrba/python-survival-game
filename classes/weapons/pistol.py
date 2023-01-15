import os

import pygame
from classes.ammo.bullet import MediumBullet


class Pistol:

    size = (90, 30)

    def __init__(self, pos):
        self.original_image = pygame.image.load(os.path.join("imgs", "pistol.png"))
        self.image = pygame.transform.scale(self.original_image, self.size)

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def interaction(self, game):
        for i in range(len(game.inventory.slots)):
            if game.inventory.slots[i] is None:
                game.inventory.slots[i] = PistolItem()
                game.weapons.remove(self)
                return
        print("Inventory is full notification")


    def update(self, game):
        self.rect.center = game.get_position_by_player(self.pos)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)


class PistolItem(Pistol):
    ammo = {
        "max": 6,
        "current": 6
    }

    def __init__(self):
        super()
        self.original_image = pygame.image.load(os.path.join("imgs", "pistol.png"))
        self.image = pygame.transform.scale(self.original_image, self.size)

    def attack_event(self, game, pos):
        game.projectiles.append(MediumBullet(game, pos, game.mouse_angle))

