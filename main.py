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
from classes.weapons.pistol import PistolItem
from classes.weapons.shotgun import ShotgunItem
from classes.buy_station.medkit import Medkit

from functions.angle import get_angle
from functions.math import get_distance
import random
import heapq
import math

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
        self.spawners = [Spawn(self, (400, 800)), Spawn(self, (2500, 250)), Spawn(self, (2800, 2800)), Spawn(self, (1200, 2800)), Spawn(self, (3000, 1500))]
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
                if random.random() > 0.65:
                    index = random.randrange(len(self.MAP_STRUCTURES))
                    structure = self.rotate_map_structure(self.MAP_STRUCTURES[index])
                    for j in range(len(structure)):
                        for g in range(len(structure[j])):
                            if i + j > self.MAP_TILES_LENGTH - 1 or k + g > self.MAP_TILES_LENGTH - 1:
                                continue
                            symbol = structure[j][g]
                            self.map[i + j][k + g] = symbol
                            if symbol == 1:
                                self.structures.append(Wall(self, self.space, ((i + j) * self.TILE_SIZE + self.TILE_SIZE / 2,
                                                                               (k + g) * self.TILE_SIZE + self.TILE_SIZE / 2),
                                                            (self.TILE_SIZE, self.TILE_SIZE)))

        self.ground_items = [Knife(self, (self.player_start_cord["x"] + 100, self.player_start_cord["y"])),
                             BuyStation(self, (1800, 2500), PistolItem(), 45, True, False),
                             BuyStation(self, (700, 200), ShotgunItem(), 100, True, False),
                             BuyStation(self, (400, 1800), AmmoBox(self, (0, 0), "medium", 10), 15, False, True),
                             BuyStation(self, (2100, 400), AmmoBox(self, (0, 0), "light", 3), 15, False, True),
                             BuyStation(self, (1100, 1400), Medkit(self, (0, 0)), 15, False, True)]
        # self.ground_items = [Knife()]
        # self.ground_items = [Pistol(self, (500, 500)), Pistol(self, (800, 400)), Knife(self, (200, 200)),
        #                      AmmoBox(self, (300, 500), "medium", 10),
        #                      BuyStation(self, (800, 600), AmmoBox(self, (0, 0), "medium", 10), 15, True, True)]
        self.projectiles = []
        self.coins = []

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

        self.in_menu = True
        self.menu_surface = pygame.surface.Surface(self.window.get_size())

        #IMPLEMENTING PATH FINDING GRAPH
        self.graph = Graph(self)

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
            item.move()
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

            if self.in_menu:
                self.menu_surface.fill((0, 0, 0))
                menu_rect = self.menu_surface.get_rect()
                font = pygame.font.Font(None, 80)
                text_title = font.render("Get out of the Wooden House", True, (255, 255, 255))
                text_title_rect = text_title.get_rect()
                text_title_rect.center = (menu_rect.width / 2, menu_rect.height / 2 - 250)
                self.menu_surface.blit(text_title, text_title_rect)
                play_button = pygame.Rect(self.window.get_width() / 2, self.window.get_height() / 2 + 100, 0,
                                             0).inflate(250, 90)
                self.menu_surface.fill((33, 33, 33) if not play_button.collidepoint(self.point) else (255, 255, 255),
                                 play_button)
                play_button_text = self.font.render("Play", True,
                                                       (255, 255, 255) if not play_button.collidepoint(
                                                           self.point) else (33, 33, 33))
                play_button_text_rect = play_button_text.get_rect()
                play_button_text_rect.center = (self.window.get_width() / 2, self.window.get_height() / 2 + 100)
                self.menu_surface.blit(play_button_text, play_button_text_rect)
                # play_button_rect = play_button.get_rect()
                # play_button_rect.center = (self.window.get_width() / 2, self.window.get_height() / 2 + 100)
                # self.menu_surface.blit(play_button, play_button_rect)
                self.window.blit(self.menu_surface, (0, 0))

                if play_button.collidepoint(self.point) and pygame.mouse.get_pressed()[0]:
                    self.in_menu = False
            else:
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
        f.write(f"Player made it into Wave {self.wave.number}\n")
        f.close()

        self.inventory = Inventory(self)
        self.player = Player(self, self.space, (self.player_start_cord["x"], self.player_start_cord["y"]))

        self.enemies = []
        # BasicEnemy(self, self.space, 40, (300, 300)), BasicEnemy(self, self.space, 40, (500, 300)),
        # RangeEnemy(self, self.space, 25, (750, 500))
        self.spawners = [Spawn(self, (400, 800)), Spawn(self, (2500, 250)), Spawn(self, (2800, 2800)), Spawn(self, (1200, 2800)), Spawn(self, (3000, 1500))]
        self.structures = [Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH / 2, -self.TILE_SIZE / 2),
                                (self.TILE_SIZE * self.MAP_TILES_LENGTH, self.TILE_SIZE)),
                           Wall(self, self.space, (-self.TILE_SIZE / 2, self.TILE_SIZE * self.MAP_TILES_LENGTH / 2),
                                (self.TILE_SIZE, self.TILE_SIZE * self.MAP_TILES_LENGTH)),
                           Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH + self.TILE_SIZE / 2,
                                                   self.TILE_SIZE * self.MAP_TILES_LENGTH / 2),
                                (self.TILE_SIZE, self.TILE_SIZE * self.MAP_TILES_LENGTH)),
                           Wall(self, self.space, (self.TILE_SIZE * self.MAP_TILES_LENGTH / 2,
                                                   self.TILE_SIZE * self.MAP_TILES_LENGTH + self.TILE_SIZE / 2),
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
                    structure = self.rotate_map_structure(self.MAP_STRUCTURES[index])
                    for j in range(len(structure)):
                        for g in range(len(structure[j])):
                            if i + j > self.MAP_TILES_LENGTH - 1 or k + g > self.MAP_TILES_LENGTH - 1:
                                continue
                            symbol = structure[j][g]
                            self.map[i + j][k + g] = symbol
                            if symbol == 1:
                                self.structures.append(
                                    Wall(self, self.space, ((i + j) * self.TILE_SIZE + self.TILE_SIZE / 2,
                                                            (k + g) * self.TILE_SIZE + self.TILE_SIZE / 2),
                                         (self.TILE_SIZE, self.TILE_SIZE)))
        self.ground_items = [Knife(self, (self.player_start_cord["x"] + 100, self.player_start_cord["y"])),
                             BuyStation(self, (1800, 2500), PistolItem(), 45, True, False),
                             BuyStation(self, (700, 200), ShotgunItem(), 100, True, False),
                             BuyStation(self, (400, 1800), AmmoBox(self, (0, 0), "medium", 10), 15, False, True),
                             BuyStation(self, (2100, 400), AmmoBox(self, (0, 0), "light", 3), 15, False, True),
                             BuyStation(self, (1100, 1400), Medkit(self, (0, 0)), 15, False, True)]
        self.projectiles = []
        self.coins = []

        self.wave = Wave(self, 1)

        self.closest_item = None
        self.is_paused = False
        self.graph = Graph(self)

    def get_position_by_player(self, pos):
        return self.player_start_cord["x"] - self.camera["x"] + pos[0], self.player_start_cord["y"] - self.camera["y"] + \
               pos[1]

    def rotate_map_structure(self, structure):
        middle_index = (len(structure) - 1) // 2
        new_structure = []
        for i in range(len(structure)):
            new_structure.append([])
            for k in range(len(structure[i])):
                new_structure[i].append(0)
        random_side = random.randrange(4)
        for i in range(len(structure)):
            for k in range(len(structure[i])):
                if structure[i][k] == 1:
                    if random_side == 0:
                        new_structure[i][k] = 1
                    elif random_side == 1:
                        new_structure[middle_index - k + middle_index][i] = 1
                    elif random_side == 2:
                        new_structure[k][middle_index - i + middle_index] = 1
                    elif random_side == 3:
                        new_structure[middle_index - k + middle_index][middle_index - i + middle_index] = 1
        return new_structure

    def enemy_projectile_hit(self, arbiter, space, data):
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
        if bullet is None or bullet.bullet_owner != "enemy":
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
        if enemy_object is None:
            return False
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


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def put(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def get(self):
        return heapq.heappop(self._queue)[-1]

    def empty(self):
        return not self._queue


class Node:
    def __init__(self, x, y):
        self.nodes = []
        self.x = x
        self.y = y


class Graph:
    def __init__(self, game):
        self.map = []
        self.max_length = game.MAP_TILES_LENGTH
        for i in range(len(game.map)):
            self.map.append([])
            for k in range(len(game.map[i])):
                self.map[i].append(Node(i, k))
        for i in range(len(game.map)):
            for k in range(len(game.map[i])):
                if self.check_index_range(k - 1) and game.map[i][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i][k - 1], 1))
                if self.check_index_range(k + 1) and game.map[i][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i][k + 1], 1))
                if self.check_index_range(i - 1) and game.map[i - 1][k] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k], 1))
                if self.check_index_range(i + 1) and game.map[i + 1][k] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k], 1))
                if self.check_index_range(k - 1) and self.check_index_range(i - 1) and game.map[i][k - 1] == 0 and game.map[i - 1][k] == 0 and game.map[i - 1][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k - 1], math.sqrt(2)))
                if self.check_index_range(k + 1) and self.check_index_range(i - 1) and game.map[i][k + 1] == 0 and game.map[i - 1][k] == 0 and game.map[i - 1][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i - 1][k + 1], math.sqrt(2)))
                if self.check_index_range(k + 1) and self.check_index_range(i + 1) and game.map[i][k + 1] == 0 and game.map[i + 1][k] == 0 and game.map[i + 1][k + 1] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k + 1], math.sqrt(2)))
                if self.check_index_range(k - 1) and self.check_index_range(i + 1) and game.map[i][k - 1] == 0 and game.map[i + 1][k] == 0 and game.map[i + 1][k - 1] == 0:
                    self.map[i][k].nodes.append((self.map[i + 1][k - 1], math.sqrt(2)))

    def check_index_range(self, index):
        return 0 <= index < self.max_length

    def neighbors(self, node):
        # new_neighbours = []
        # for item, _ in node.nodes:
        #     new_neighbours.append(item)
        # return new_neighbours
        return node.nodes

    def A_star(self, start, goal):
        # Create a priority queue for frontier nodes
        frontier = PriorityQueue()
        frontier.put(start, 0)
        # Create a dictionary to store the cost of each node
        cost_so_far = {start: 0}
        # Create a dictionary to store the came_from value for each node
        came_from = {start: None}

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next_node, cost in self.neighbors(current):
                # new_cost = cost_so_far[current] + graph.cost(current, next_node)
                new_cost = cost_so_far[current] + cost
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + math.sqrt(
                        (goal.x - next_node.x) ** 2 + (goal.y - next_node.y) ** 2)  # heuristic(goal, next_node)
                    frontier.put(next_node, priority)
                    came_from[next_node] = current

        # return came_from, cost_so_far
        return came_from

if __name__ == "__main__":
    game = Game(1000, 1000, 60)
    game.run()
