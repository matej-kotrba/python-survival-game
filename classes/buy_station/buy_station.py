import os

import pygame


class BuyStation:

    size = (150, 80)

    original_image = pygame.image.load(os.path.join("imgs", "buy_station.png"))
    image = pygame.transform.scale(original_image, size)

    shut_original_image = pygame.image.load(os.path.join("imgs", "buy_station_shut.png"))
    shut_image = pygame.transform.scale(shut_original_image, size)

    def __init__(self, game, pos, item_to_buy, cost, close, consumable):
        self.game = game
        self.pos = pos
        self.item_to_buy = item_to_buy
        self.cost = cost
        self.rect = self.image.get_rect()
        self.close_after_buy = close
        self.used = False
        self.consumable = consumable

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        self.game.window.blit(self.image, self.rect)

    def interaction(self):
        if (self.used and self.close_after_buy and self.game.inventory.coins >= self.cost) or self.game.inventory.coins >= self.cost:
            if self.consumable:
                self.item_to_buy.interaction()
                self.game.inventory.coins -= self.cost
                self.used = True
                return
            empty_slot_i = self.game.inventory.get_inventory_space_index()
            if empty_slot_i == -1:
                return
            self.game.inventory.slots[empty_slot_i] = self.item_to_buy
            self.game.inventory.coins -= self.cost
            self.used = True
