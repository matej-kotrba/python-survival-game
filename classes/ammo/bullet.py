import pygame
import pymunk
import pymunk.pygame_util

BULLETS_TYPES = {
    "light": {
        "size": 4,
        "damage": 3,
        "color": (247, 111, 84)
    },
    "medium": {
        "size": 6,
        "damage": 6,
        "color": (92, 91, 91)
    },
    "heavy": {
        "size": 10,
        "damage": 12,
        "color": (168, 44, 44)
    }
}


class Bullet:
    body = pymunk.Body()

    def __init__(self, bullet_type, pos):
        self.body.position = pos
        self.size = bullet_type["size"]
        self.shape = pymunk.Circle(self.body, self.size)
        self.shape.mass = self.size / 1.2
        self.damage = bullet_type["damage"]
        self.color = bullet_type["color"]

        self.surface = pygame.Surface(size=(self.size * 2, self.size * 2))
        self.rect = self.surface.get_rect()

    def draw(self, game):
        pygame.draw.circle(self.surface, self.color, (self.size, self.size), self.size)
        self.rect.center = game.get_position_by_player(self.body.position)
        new_rect = self.surface.get_rect(center=self.rect.center)
        game.window.blit(self.surface, new_rect)


class LightBullet(Bullet):
    def __init__(self, pos):
        super().__init__(BULLETS_TYPES["light"], pos)


class MediumBullet(Bullet):
    def __init__(self, pos):
        super().__init__(BULLETS_TYPES["medium"], pos)

