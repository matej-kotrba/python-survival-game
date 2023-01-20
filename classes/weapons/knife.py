import os

import pygame
from classes.ammo.bullet import KnifeAttack

pygame.init()

class Knife:

    size = (90, 30)

    def __init__(self, game, pos):
        self.game = game

        self.original_image = pygame.image.load(os.path.join("imgs", "knife.png"))
        self.image = pygame.transform.scale(self.original_image, self.size)

        self.pos = pos

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def interaction(self):
        i = self.game.inventory.get_inventory_space_index()
        if i == -1:
            return
        self.game.inventory.slots[i] = KnifeItem()
        self.game.ground_items.remove(self)

    def update(self):
        self.rect.center = self.game.get_position_by_player(self.pos)
        new_rect = self.image.get_rect(center=self.rect.center)
        self.game.window.blit(self.image, new_rect)


class KnifeItem(Knife):
    ammo_surface_size = (150, 50)
    ammo_surface = pygame.surface.Surface(ammo_surface_size, pygame.SRCALPHA, 32)

    reload_time = 0.5

    font = pygame.font.Font(None, 50)

    def __init__(self):
        self.original_image = pygame.image.load(os.path.join("imgs", "knife.png"))
        self.image = pygame.transform.scale(self.original_image, self.size)

        self.move_knife = (0, 0)

    def attack_event(self, game, pos):
        game.projectiles.append(KnifeAttack(game, pos, game.mouse_angle, "player"))

    def show_ammo(self, game):
        self.ammo_surface.fill((0, 0, 0, 0))
        text = self.font.render(f" ∞ / ∞", False, (255, 255, 255))
        rect = text.get_rect()
        self.ammo_surface.blit(text, (self.ammo_surface_size[0] / 2 - rect.width / 2, self.ammo_surface_size[1] / 2 - rect.height / 2))
        game.window.blit(self.ammo_surface, (0, 150))

    def reload(self, game):
        pass
