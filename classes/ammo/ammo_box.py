import os

import pygame

class AmmoBox:

    original_image = pygame.image.load(os.path.join("imgs/ammo", "ammo_box"))

    def __init__(self, game, ammo_type, ammo_count):
        self.game = game
        self.ammo_type = ammo_type
        self.ammo_count = ammo_count
