import pygame
import pymunk
import pymunk.pygame_util
from classes.enemies.basic import BasicEnemy
from classes.structures.structures import Wall
from classes.player.player import Player
from classes.weapons.pistol import Pistol
from classes.inventory.inventory import Inventory
from classes.ammo.ammo_box import AmmoBox
from classes.coin.coin import Coin

from functions.angle import get_angle
from functions.math import get_distance

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
        "PROJECTILE": 4,
        "COIN": 5
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
        "S": False,
        "E": False,
        "R": False
    }

    mouse_angle = 0

    def __init__(self, width, height, fps):
        assert (type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.inventory = Inventory(self)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.fps = fps

        self.player = Player(self, self.space, (self.player_start_cord["x"], self.player_start_cord["y"]))

        self.enemies = [BasicEnemy(self, self.space, 40, (300, 300)), BasicEnemy(self, self.space, 40, (500, 300))]
        self.structures = [Wall(self, self.space, (400, 775), (800, 50))]
        self.ground_items = [Pistol(self, (500, 500)), Pistol(self, (800, 400)), AmmoBox(self, (300, 500), "medium", 10)]
        self.projectiles = []
        self.coins = [Coin(self, (800, 500))]

        self.closest_item = None
        # closest_item = {"item": weapon, "range": int}

        # Collisions functions
        self.space.add_collision_handler(self.collision_types["ENEMY"],
                                         self.collision_types["PROJECTILE"]).begin \
            = lambda arbiter, space, data: self.enemy_projectile_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["STRUCTURE"],
                                         self.collision_types["PROJECTILE"]).begin \
            = lambda arbiter, space, data: self.structure_projectile_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["ENEMY"],
                                         self.collision_types["PLAYER"]).begin \
            = lambda arbiter, space, data: self.enemy_player_hit(arbiter, space, data)

        self.action_key_surface = pygame.surface.Surface((70, 70))

        self.font = pygame.font.Font(None, 50)

    def draw(self):
        self.closest_item = None

        self.window.fill("royalblue")

        debug_options = pymunk.pygame_util.DrawOptions(self.window)
        self.space.debug_draw(debug_options)

        for item in self.structures:
            item.update(self)

        for item in self.ground_items:
            item.update()
            distance = get_distance(self.get_position_by_player(item.pos), (500, 500))
            if distance < 100:
                if self.closest_item is None or self.closest_item["range"] > distance:
                    self.closest_item = {
                        "item": item,
                        "range": distance
                    }

        for item in self.coins:
            item.draw()

        for item in self.enemies:
            item.update(self)

        for item in self.projectiles:
            item.movement()
            item.range_despawn()

        for item in self.enemies:
            item.show_hp(self)

        self.player.immunity_delay()
        self.player.update(self)
        self.player.display_item_in_hand(self, self.inventory.slots[self.inventory.selected_slot])

        for item in self.projectiles:
            item.draw()

        if self.closest_item is not None:
            surface_width = self.action_key_surface.get_width()
            surface_height = self.action_key_surface.get_height()
            text = self.font.render("E", True, (255, 255, 255))
            rect = text.get_rect()
            pygame.draw.rect(self.action_key_surface, (53, 53, 53),
                             (0, 0, surface_width, surface_height))
            self.action_key_surface.blit(text, (surface_width / 2 - rect.width / 2, surface_height / 2 - rect.height / 2))
            self.window.blit(self.action_key_surface,
                             (self.window.get_width() / 2 - surface_width / 2, self.window.get_height() / 2 - 150))

        self.inventory.draw()
        if self.inventory.slots[self.inventory.selected_slot] is not None:
            self.inventory.slots[self.inventory.selected_slot].show_ammo(self)
        self.player.show_hp()

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
                    if event.key == pygame.K_e:
                        if self.closest_item and not self.inputs["E"]:
                            self.closest_item["item"].interaction()
                        self.inputs["E"] = True
                    if event.key == pygame.K_r:
                        if self.inventory.slots[self.inventory.selected_slot] is not None and not self.inputs["R"]:
                            self.inventory.slots[self.inventory.selected_slot].reload(self)
                        self.inputs["R"] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.inputs["D"] = False
                    if event.key == pygame.K_a:
                        self.inputs["A"] = False
                    if event.key == pygame.K_w:
                        self.inputs["W"] = False
                    if event.key == pygame.K_s:
                        self.inputs["S"] = False
                    if event.key == pygame.K_r:
                        self.inputs["R"] = False
                    if event.key == pygame.K_e:
                        self.inputs["E"] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.inventory.slots[self.inventory.selected_slot] is not None:
                            self.inventory.slots[self.inventory.selected_slot] \
                                .attack_event(game, (self.player.body.position.x, self.player.body.position.y))
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.inventory.selected_slot += 1
                        if self.inventory.selected_slot >= len(self.inventory.slots):
                            self.inventory.selected_slot = 0
                    if event.y > 0:
                        self.inventory.selected_slot -= 1
                        if self.inventory.selected_slot < 0:
                            self.inventory.selected_slot = len(self.inventory.slots) - 1

            self.mouse_angle = get_angle(pygame.mouse.get_pos(),
                                         (self.player_start_cord["x"], self.player_start_cord["y"]))
            self.player.move_player(self.inputs)
            self.draw()
            self.space.step(self.dt)
            self.clock.tick(self.fps)

    def get_position_by_player(self, pos):
        return self.player_start_cord["x"] - self.camera["x"] + pos[0], self.player_start_cord["y"] - self.camera["y"] + \
               pos[1]

    # def item_projectile_hit(self, arbiter, space, data, array, callback):
    #     '''
    #     :param arbiter: objets which collided
    #     :param space: space
    #     :param data: data
    #     :param callback: function which will apply on item of the array which collided
    #     :param array: array of items we want to go through, shape must be included
    #     :return:
    #     '''
    #     shapeA, shapeB = arbiter.shapes
    #     for item in array:
    #         if item.shape == shapeB:
    #             callback(item, shapeA)
    #             break
    #     return False

    def enemy_projectile_hit(self, arbiter, space, data):
        # lambda item, shape:
        # for enemy in self.enemies:
        #     print("asd")
        # self.projectiles.remove(item))
        shapeA, shapeB = arbiter.shapes
        bullet = None
        for projectile in self.projectiles:
            if projectile.shape == shapeB:
                bullet = projectile
                break
        for enemy in self.enemies:
            if enemy.shape == shapeA:
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
                break
        self.projectiles.remove(bullet)
        return False

    def structure_projectile_hit(self, arbiter, space, data):
        shapeA, shapeB = arbiter.shapes
        bullet = None
        for projectile in self.projectiles:
            if projectile.shape == shapeB:
                bullet = projectile
                break
                break
        self.projectiles.remove(bullet)
        return False

    def enemy_player_hit(self, arbiter, space, data):
        if self.player.immune:
            return True
        shapeA, shapeB = arbiter.shapes
        enemy_object = None
        for enemy in self.enemies:
            if shapeA == enemy.shape:
                enemy_object = enemy
                break
        self.player.hp -= enemy_object.collision_damage
        self.player.after_damage_immunity()
        return True

    def player_coin_hit(self, arbiter, space, data):


if __name__ == "__main__":
    game = Game(1000, 1000, 60)
    game.run()
