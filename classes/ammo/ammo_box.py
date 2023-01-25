import os

import pygame


class AmmoBox:

    size = (80, 80)

    original_image = pygame.image.load(os.path.join("imgs/ammo", "ammo_box.png"))
    image = pygame.transform.scale(original_image, size)

    def __init__(self, game, pos, ammo_type, ammo_count):
        self.game = game
        self.ammo_type = ammo_type
        self.ammo_count = ammo_count
        self.pos = pos
        self.surface = pygame.surface.Surface((150, 150))
        self.rect = self.image.get_rect()

    def interaction(self):
        self.game.inventory.ammo[self.ammo_type] += self.ammo_count
        if self in self.game.ground_items:
            self.game.ground_items.remove(self)

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        new_rect = self.image.get_rect(center=self.rect.center)
        self.game.window.blit(self.image, new_rect)
