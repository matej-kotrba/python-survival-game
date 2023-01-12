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

    def __init__(self, window):
        self.surface = window

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