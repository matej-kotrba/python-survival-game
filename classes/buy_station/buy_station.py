import os

import pygame


class BuyStation:

    size = (150, 80)

    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))
    image = pygame.transform.scale(original_image, size)

    def __init__(self, game, pos, item_to_buy, cost):
        self.game = game
        self.pos = pos
        self.item_to_buy = item_to_buy
        self.cost = cost
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        self.game.window.blit(self.image, self.rect)