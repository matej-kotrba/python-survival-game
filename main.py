import pygame
import pymunk
import pymunk.pygame_util
from classes.enemies.basic import BasicEnemy
from classes.structures.structures import Wall
from classes.player.player import Player
from classes.weapons.pistol import Pistol
from classes.inventory.inventory import Inventory
from classes.ammo.bullet import MediumBullet

from functions.angle import get_angle

pygame.init()

class Game:
    isRunning = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    window = None
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = 0.4

    collision_types = {
        "PLAYER": 1,
        "STRUCTURE": 2,
        "ENEMY": 3,
        "PROJECTILE": 4
    }

    player_start_cord = {
        "x": 500,
        "y": 500
    }

    camera = {
        "x": 500,
        "y": 500,
    }

    inputs = {
        "A": False,
        "D": False,
        "W": False,
        "S": False
    }

    mouse_angle = 0

    def __init__(self, width, height, fps):
        assert(type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.inventory = Inventory(self.window)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.fps = fps

        self.player = Player(self, self.space, (self.player_start_cord["x"], self.player_start_cord["y"]))

        self.enemies = [BasicEnemy(self, self.space, 40, (300, 300)), BasicEnemy(self, self.space, 40, (500, 300))]
        self.structures = [Wall(self, self.space, (400, 775), (800, 50))]
        self.weapons = [Pistol((600, 300)), Pistol((600, 400))]
        self.projectiles = []

        self.space.add_collision_handler(self.collision_types["ENEMY"],
                                         self.collision_types["PROJECTILE"]).begin = self.item_projectile_hit
    def draw(self):
        self.window.fill("royalblue")
        # pygame.display.update()
        # for item in self.structures:
        #     self.window.blit(item, (item.body.position.x - self.camera["x"], item.body.position.y - self.camera["y"]))
        # for item in self.enemies:
        #     self.window.blit(item, (item.body.position.x - self.camera["x"], item.body.position.y - self.camera["y"]))
        # self.window.blit(self.player, (self.player.body.position.x - self.camera["x"],
        #                                self.player.body.position.y - self.camera["y"]))
        # self.space.debug_draw(self.draw_options)

        for item in self.structures:
            item.update(self)

        for item in self.weapons:
            item.update(self)

        for item in self.enemies:
            item.update(self)

        for item in self.projectiles:
            item.movement()
            item.collision()

        self.player.update(self)
        self.player.display_item_in_hand(self, self.inventory.slots[self.inventory.selected_slot])

        for item in self.projectiles:
            item.draw()

        self.inventory.draw()

        pygame.display.flip()

    def run(self):

        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.inputs["D"] = True
                    if event.key == pygame.K_a:
                        self.inputs["A"] = True
                    if event.key == pygame.K_w:
                        self.inputs["W"] = True
                    if event.key == pygame.K_s:
                        self.inputs["S"] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.inputs["D"] = False
                    if event.key == pygame.K_a:
                        self.inputs["A"] = False
                    if event.key == pygame.K_w:
                        self.inputs["W"] = False
                    if event.key == pygame.K_s:
                        self.inputs["S"] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.inventory.slots[self.inventory.selected_slot] is None:
                            return
                        self.inventory.slots[self.inventory.selected_slot]\
                            .attack_event(game, (self.player.body.position.x, self.player.body.position.y))
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.inventory.selected_slot += 1
                        if self.inventory.selected_slot >= len(self.inventory.slots):
                            self.inventory.selected_slot = 0
                    if event.y < 0:
                        self.inventory.selected_slot -= 1
                        if self.inventory.selected_slot < 0:
                            self.inventory.selected_slot = len(self.inventory.slots) - 1
            self.mouse_angle = get_angle(pygame.mouse.get_pos(),
                                         (self.player_start_cord["x"], self.player_start_cord["y"]))
            self.player.move_player(self.inputs)
            # for item in self.enemies:
            #     item.body.position = (item.body.position.x + self.player.body.position.x - self.player_start_cord["x"],
            #                           item.body.position.y + self.player.body.position.y - self.player_start_cord["y"])
            # for item in self.structures:
            #     item.body.position = (item.body.position.x + self.player.body.position.x - self.player_start_cord["x"],
            #                           item.body.position.y + self.player.body.position.y - self.player_start_cord["y"])
            self.draw()
            self.space.step(self.dt)
            self.clock.tick(self.fps)

    def get_position_by_player(self, pos):
        return self.player_start_cord["x"] - self.camera["x"] + pos[0], self.player_start_cord["y"] - self.camera["y"] + pos[1]


    def item_projectile_hit(self, arbiter, b, data):
        shapeA, shapeB = arbiter.shapes
        for item in self.projectiles:
            if item.shape == shapeB:
                self.projectiles.remove(item)
                break
        return False

if __name__ == "__main__":
    game = Game(1000, 1000, 60)
    game.run()