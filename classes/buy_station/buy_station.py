import os

import pygame


class BuyStation:

    size = (150, 80)

    original_image = pygame.image.load(os.path.join("imgs", "basic.png"))
    image = pygame.transform.scale(original_image, size)

    def __init__(self, game, pos, item_to_buy, cost, close):
        self.game = game
        self.pos = pos
        self.item_to_buy = item_to_buy
        self.cost = cost
        self.rect = self.image.get_rect()
        self.close_after_buy = close

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        self.game.window.blit(self.image, self.rect)

    def interaction(self):
        if self.game.inventory.coins >= self.cost:
            if type(self.item_to_buy).__name__ == "AmmoBox":
                return
            empty_slot_i = self.game.inventory.get_inventory_space_index()
            if empty_slot_i == -1:
                return
            self.game.inventory.slots[empty_slot_i] = self.item_to_buy
            self.game.inventory.coins -= self.cost
