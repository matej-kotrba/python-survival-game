import pygame
import pymunk
import pymunk.pygame_util
from classes.enemies.spawn import Spawn
from classes.structures.structures import Wall
from classes.player.player import Player
from classes.weapons.pistol import Pistol
from classes.weapons.knife import Knife
from classes.inventory.inventory import Inventory
from classes.ammo.ammo_box import AmmoBox
from classes.coin.coin import Coin
from classes.buy_station.buy_station import BuyStation
from classes.enemies.wave import Wave

from functions.angle import get_angle
from functions.math import get_distance
import random

pygame.init()


class Game:
    is_running = True
    is_paused = False
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    window = None
    space = pymunk.Space()
    space.gravity = (0, 0)
    space.damping = 0.4

    TILE_SIZE = 40
    MAP_TILES_LENGTH = 80
    WALL_MAP_NUMBER = 1
    EMPTY_MAP_NUMBER = 0
    MAP_STRUCTURES_LENGTH = 9
    MAP_STRUCTURES = [
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    ]

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
    point = (0, 0)

    def __init__(self, width, height, fps):
        assert (type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.inventory = Inventory(self)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.fps = fps

        self.player = Player(self, self.space, (self.player_start_cord["x"], self.player_start_cord["y"]))

        self.enemies = []
        # BasicEnemy(self, self.space, 40, (300, 300)), BasicEnemy(self, self.space, 40, (500, 300)),
        # RangeEnemy(self, self.space, 25, (750, 500))
        self.spawners = [Spawn(self, (400, 800))]
        self.structures = [Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH / 2, -self.TILE_SIZE / 2),
                                (self.TILE_SIZE * self.MAP_TILES_LENGTH, self.TILE_SIZE)),
                           Wall(self, self.space, (-self.TILE_SIZE / 2, self.TILE_SIZE * self.MAP_TILES_LENGTH / 2),
                                (self.TILE_SIZE, self.TILE_SIZE * self.MAP_TILES_LENGTH)),
                           Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH + self.TILE_SIZE / 2, self.TILE_SIZE * self.MAP_TILES_LENGTH / 2),
                                (self.TILE_SIZE, self.TILE_SIZE * self.MAP_TILES_LENGTH)),
                           Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH / 2, self.TILE_SIZE * self.MAP_TILES_LENGTH + self.TILE_SIZE / 2),
                                (self.TILE_SIZE * self.MAP_TILES_LENGTH, self.TILE_SIZE))]

        self.map = []
        for i in range(self.MAP_TILES_LENGTH):
            self.map.append([])
            for k in range(self.MAP_TILES_LENGTH):
                self.map[i].append(0)
        for i in range(0, self.MAP_TILES_LENGTH, self.MAP_STRUCTURES_LENGTH):
            for k in range(0, self.MAP_TILES_LENGTH, self.MAP_STRUCTURES_LENGTH):
                if random.random() > 0.7:
                    index = random.randrange(len(self.MAP_STRUCTURES))
                    for j in range(len(self.MAP_STRUCTURES[index])):
                        for g in range(len(self.MAP_STRUCTURES[0][j])):
                            if i + j > self.MAP_TILES_LENGTH - 1 or k + g > self.MAP_TILES_LENGTH - 1:
                                continue
                            symbol = self.MAP_STRUCTURES[index][j][g]
                            self.map[i + j][k + g] = symbol
                            if symbol == 1:
                                self.structures.append(Wall(self, self.space, ((i + j) * self.TILE_SIZE + self.TILE_SIZE / 2,
                                                                               (k + g) * self.TILE_SIZE + self.TILE_SIZE / 2),
                                                            (self.TILE_SIZE, self.TILE_SIZE)))

        self.ground_items = [Pistol(self, (500, 500)), Pistol(self, (800, 400)), Knife(self, (200, 200)),
                             AmmoBox(self, (300, 500), "medium", 10),
                             BuyStation(self, (800, 600), AmmoBox(self, (0, 0), "medium", 10), 15, True, True)]
        self.projectiles = []
        self.coins = [Coin(self, (800, 500))]

        self.closest_item = None
        # closest_item = {"item": weapon, "range": int}

        # Collisions functions
        self.space.add_collision_handler(self.collision_types["ENEMY"],
                                         self.collision_types["PROJECTILE"]).begin \
            = lambda arbiter, space, data: self.enemy_projectile_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["PLAYER"],
                                         self.collision_types["PROJECTILE"]).begin \
            = lambda arbiter, space, data: self.player_projectile_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["STRUCTURE"],
                                         self.collision_types["PROJECTILE"]).begin \
            = lambda arbiter, space, data: self.structure_projectile_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["ENEMY"],
                                         self.collision_types["PLAYER"]).begin \
            = lambda arbiter, space, data: self.enemy_player_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["COIN"],
                                         self.collision_types["PLAYER"]).begin \
            = lambda arbiter, space, data: self.player_coin_hit(arbiter, space, data)
        self.space.add_collision_handler(self.collision_types["COIN"],
                                         self.collision_types["ENEMY"]).begin \
            = lambda a, b, c: False

        self.action_key_surface = pygame.surface.Surface((70, 70))

        self.font = pygame.font.Font(None, 50)
        self.font_smaller = pygame.font.Font(None, 30)

        self.wave = Wave(self, 1)

        self.death_screen_surface = pygame.surface.Surface(self.window.get_size(), pygame.SRCALPHA, 32)
        self.death_screen_surface.convert_alpha()

    def draw(self):
        self.closest_item = None

        self.window.fill("royalblue")

        # debug_options = pymunk.pygame_util.DrawOptions(self.window)
        # self.space.debug_draw(debug_options)

        self.wave.check_status()

        for item in self.spawners:
            item.draw()

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
            item.special_attack()
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
            text_second = None
            if type(self.closest_item["item"]).__name__ == "BuyStation":
                extra_text = ""
                if (type(self.closest_item["item"].item_to_buy).__name__ == "AmmoBox"):
                   extra_text = f"{self.closest_item['item'].item_to_buy.ammo_type} - {self.closest_item['item'].item_to_buy.ammo_count}"
                text_second = self.font_smaller\
                    .render(f"{type(self.closest_item['item'].item_to_buy).__name__.replace('Item', '')}, {extra_text} cost = {self.closest_item['item'].cost}",
                                                True, (255, 255, 255))
            rect = text.get_rect()
            pygame.draw.rect(self.action_key_surface, (53, 53, 53),
                             (0, 0, surface_width, surface_height))
            self.action_key_surface.blit(text, (surface_width / 2 - rect.width / 2, surface_height / 2 - rect.height / 2))
            if text_second is not None:
                rect_second = text_second.get_rect()
                rect_second.midleft = (10, self.window.get_height() - 30)
                pygame.draw.rect(self.window, (53, 53, 53), (0, self.window.get_height() - 60, text_second.get_width() + 20, 60))
                self.window.blit(text_second, rect_second)
                # self.action_key_surface.blit(text_second,
                #                              (surface_width / 2 - rect_second.width / 2, surface_height / 2 - rect_second.height / 2 + 15))
            self.window.blit(self.action_key_surface,
                             (self.window.get_width() / 2 - surface_width / 2, self.window.get_height() / 2 - 150))

        self.inventory.draw()
        if self.inventory.slots[self.inventory.selected_slot] is not None:
            self.inventory.slots[self.inventory.selected_slot].show_ammo(self)
        self.wave.display_overview()
        self.player.show_hp()

    def run(self):

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
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
            self.point = pygame.mouse.get_pos()

            if not self.is_paused:
                self.player.move_player(self.inputs)
                self.draw()
                self.space.step(self.dt)
                self.clock.tick(self.fps)
            else:
                self.death_screen_surface.fill((0, 0, 0, 1))
                font = pygame.font.Font(None, 80)
                text = font.render("You died", True, (255, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (self.window.get_width() / 2, self.window.get_height() / 2)
                self.death_screen_surface.blit(text, text_rect)
                restart_button = pygame.Rect(self.window.get_width() / 2, self.window.get_height() / 2 + 100, 0, 0).inflate(250, 90)
                self.window.fill((33, 33, 33) if not restart_button.collidepoint(self.point) else (255, 255, 255), restart_button)
                restart_button_text = self.font.render("Restart", True, (255, 255, 255) if not restart_button.collidepoint(self.point) else (33, 33, 33))
                restart_button_text_rect = restart_button_text.get_rect()
                restart_button_text_rect.center = (self.window.get_width() / 2, self.window.get_height() / 2 + 100)
                self.window.blit(restart_button_text, restart_button_text_rect)
                # restart_button_rect = restart_button.get_rect()
                # restart_button_rect.center = (self.window.get_width() / 2, self.window.get_height() / 2 + 100)
                # self.death_screen_surface.blit(restart_button, restart_button_rect)
                self.window.blit(self.death_screen_surface, (0, 0))

                if restart_button.collidepoint(self.point) and pygame.mouse.get_pressed()[0]:
                    self.restart_game()

            pygame.display.flip()

    def restart_game(self):

        f = open("scoreboard.txt", "a")
        f.write(f"Player made it into Wave {self.wave.number}")
        f.close()

        self.inventory = Inventory(self)
        self.player = Player(self, self.space, (self.player_start_cord["x"], self.player_start_cord["y"]))

        self.enemies = []
        # BasicEnemy(self, self.space, 40, (300, 300)), BasicEnemy(self, self.space, 40, (500, 300)),
        # RangeEnemy(self, self.space, 25, (750, 500))
        self.spawners = [Spawn(self, (400, 800))]
        self.structures = [Wall(self, self.space, (400, 775), (800, 50))]
        self.ground_items = [Pistol(self, (500, 500)), Pistol(self, (800, 400)), Knife(self, (200, 200)),
                             AmmoBox(self, (300, 500), "medium", 10),
                             BuyStation(self, (800, 600), AmmoBox(self, (0, 0), "medium", 10), 15, True, True)]
        self.projectiles = []
        self.coins = [Coin(self, (800, 500))]

        self.wave = Wave(self, 1)

        self.closest_item = None
        self.is_paused = False


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
        if bullet is None or bullet.bullet_owner != "player":
            return False
        for enemy in self.enemies:
            if enemy.shape == shapeA:
                enemy.hp -= bullet.damage
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
                break
        self.projectiles.remove(bullet)
        return False

    def player_projectile_hit(self, arbiter, space, data):
        shapeA, shapeB = arbiter.shapes
        bullet = None
        for projectile in self.projectiles:
            if projectile.shape == shapeB:
                bullet = projectile
                break
        if bullet.bullet_owner != "enemy":
            return False
        self.player.hp -= bullet.damage
        self.projectiles.remove(bullet)
        return False

    def structure_projectile_hit(self, arbiter, space, data):
        shapeA, shapeB = arbiter.shapes
        bullet = None
        for projectile in self.projectiles:
            if projectile.shape == shapeB:
                bullet = projectile
                break
        if bullet is None:
            return False
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
        shapeA, shapeB = arbiter.shapes
        coin = None
        for item in self.coins:
            if item.shape == shapeA:
                coin = item
                break
        if coin is None:
            return False
        self.inventory.coins += coin.value
        self.coins.remove(coin)
        return False


if __name__ == "__main__":
    game = Game(1000, 1000, 60)
    game.run()
