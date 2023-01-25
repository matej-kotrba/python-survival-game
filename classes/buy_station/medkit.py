import os

import pygame


class Medkit:

    size = (80, 80)

    original_image = pygame.image.load(os.path.join("imgs", "medkit.png"))
    image = pygame.transform.scale(original_image, size)

    value = 10

    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.surface = pygame.surface.Surface((150, 150))
        self.rect = self.image.get_rect()

    def interaction(self):
        self.game.player.hp += self.value
        if self.game.player.hp > self.game.player.max_hp:
            self.game.player.hp = self.game.player.max_hp
        if self in self.game.ground_items:
            self.game.ground_items.remove(self)

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        new_rect = self.image.get_rect(center=self.rect.center)
        self.game.window.blit(self.image, new_rect)
