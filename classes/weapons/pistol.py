import os

import pygame
from classes.ammo.bullet import MediumBullet

class Pistol:

    size = (90, 30)

    original_image = pygame.image.load(os.path.join("imgs", "pistol.png"))
    image = pygame.transform.scale(original_image, size)

    rect = image.get_rect()

    def __init__(self, pos):
        self.rect.center = pos

    def pick_item(self):
        pass

    def update(self, game):
        self.rect.center = game.get_position_by_player(self.size)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)


class PistolItem(Pistol):
    ammo = {
        "max": 6,
        "current": 6
    }

    def __init__(self):
        super()

    def attack_event(self, game, pos):
        game.projectiles.append(MediumBullet(pos))

