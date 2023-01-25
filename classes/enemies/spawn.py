import os

import pygame

class Spawn:

    size = (160, 120)

    original_image = pygame.image.load(os.path.join("imgs", "spawner.png"))
    image = pygame.transform.scale(original_image, size)

    def __init__(self, game, pos):
        self.game = game
        self.pos = pos

        self.rect = self.image.get_rect()
    def draw(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        self.game.window.blit(self.image, self.rect)
