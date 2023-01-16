import os

import pygame
from classes.weapons.pistol import PistolItem


class Inventory:
    size = (300, 50)
    pos = (0, 0)
    slots = [PistolItem(), None, None, None, None, None]
    selected_slot = 0
    tile_size = 70
    tile_gap = 2
    tile_color = (156, 156, 156)
    tile_selected_color = (235, 172, 0)

    ammo_images = {
        "light": pygame.image.load(os.path.join("imgs/ammo", "light.png")),
        "medium": pygame.image.load(os.path.join("imgs/ammo", "medium.png")),
        "heavy": pygame.image.load(os.path.join("imgs/ammo", "heavy.png"))
    }

    coin_image_original = pygame.image.load(os.path.join("imgs", "coin.png"))
    coin_image = pygame.transform.scale(coin_image_original, (60, 60))

    def __init__(self, game):
        self.game = game
        self.surface = game.window
        self.ammo = {
            "light": 0,
            "medium": 10,
            "heavy": 0
        }
        self.coins = 0
        self.ammo_surface = pygame.surface.Surface((180, 60))
        self.coins_surface = pygame.surface.Surface((60, 60))
        self.font = pygame.font.Font(None, 30)
        self.font_outline = pygame.font.Font(None, 55)

    def draw(self):
        pygame.draw.rect(self.surface, (92, 90, 90),
                         pygame.Rect(0, 0, self.tile_size * len(self.slots) + 4 + self.tile_gap * (len(self.slots) - 1),
                                     self.tile_size + 4))
        [pygame.draw.rect(self.surface, self.tile_selected_color if i == self.selected_slot else self.tile_color,
                          pygame.Rect(2 + i * (self.tile_size + self.tile_gap), 2, self.tile_size, self.tile_size))
         for i in range(len(self.slots))]

        # Render items in slots
        for index, item in enumerate(self.slots):
            if item is None:
                continue
            new_image = pygame.transform.scale(item.image, (item.size[0] / item.size[0] * self.tile_size,
                                                            item.size[1] / item.size[0] * self.tile_size)
                                               if item.size[0] > item.size[1] else (item.size[0] / item.size[1]
                                                                                    * self.tile_size,
                                                                                    item.size[1] / item.size[1]
                                                                                    * self.tile_size))
            self.surface.blit(new_image, (index * (self.tile_size + self.tile_gap) + self.tile_gap +
                                          (self.tile_size - new_image.get_width()) / 2,
                                          2 + (self.tile_size - new_image.get_height()) / 2))

            pygame.draw.rect(self.ammo_surface, (92, 90, 90), (0, 0, 180, 60))

            resized_images = []

            for image in self.ammo_images:
                resized_images.append({"item": pygame.transform.scale(self.ammo_images[image], (58, 58)),
                                       "type": image})
            self.surface.blit(self.ammo_surface, (0, self.tile_size + self.tile_gap * 2))

            for i in range(len(resized_images)):
                self.surface.blit(resized_images[i]["item"], (60 * i, self.tile_size + self.tile_gap * 2 + 2, 56, 56))
                text = self.font.render(f"{self.ammo[resized_images[i]['type']]}", True, (255, 255, 255))
                text_outline = self.font.render(f"{self.ammo[resized_images[i]['type']]}", True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = (60 * i + 30, self.tile_size + self.tile_gap * 2 + 30)
                rect_outline = text.get_rect()
                rect_outline.center = (60 * i + 30, self.tile_size + self.tile_gap * 2 + 30)
                self.surface.blit(text_outline, rect_outline)
                self.surface.blit(text, rect)

            self.surface.blit(self.coin_image, (self.game.window.get_width() - 60, 40))
            text = self.font_outline.render(f"{self.coins}", True, (252, 189, 15))
            rect = text.get_rect()
            rect.center = (self.game.window.get_width() - 75 - 10 * (len(str(self.coins)) - 1), 72)
            self.surface.blit(text, rect)