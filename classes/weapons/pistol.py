import os

import pygame

class Pistol:

    size = (90, 30)

    original_image = pygame.image.load(os.path.join("imgs", "pistol.png"))
    image = pygame.transform.scale(original_image, size)

    rect = image.get_rect()

    def __init__(self, pos):
        self.rect.center = pos

    def update(self, game):
        self.rect.center = game.get_position_by_player(self.size)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)