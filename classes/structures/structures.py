import pymunk
import pymunk.pygame_util
import pygame
import os

class Object:

    def __init__(self, game, space, pos, size, **other):
        self.game = game
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.collision_type = game.collision_types["STRUCTURE"]
        self.shape.elasticity = 0.4
        self.shape.friction = 1
        self.size = size
        self.image = pygame.transform.scale(self.original_image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        color = other.get("color", None)
        if color is not None:
            self.color = color
            self.shape.color = color
        space.add(self.body, self.shape)
    def update(self, game):
        self.rect.center = game.get_position_by_player(self.body.position)
        new_rect = self.image.get_rect(center=self.rect.center)
        game.window.blit(self.image, new_rect)

    def __del__(self):
        self.game.space.remove(self.body, self.shape)

class Wall(Object):
    color = (255, 0, 255, 100)
    original_image = pygame.image.load(os.path.join("imgs", "wall.png"))

    def __init__(self, game, space, pos, size, **other):
        super().__init__(game, space, pos, size, **other)



# class Door(Object):
#     color = (255, 0, 255, 100)
