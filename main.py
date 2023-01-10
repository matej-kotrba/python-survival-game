import pygame
import pymunk
import pymunk.pygame_util
from classes.enemies.basic import BasicEnemy
from classes.structures.structures import Wall
from classes.player.player import Player

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

    player_start_cord = {
        "x": 400,
        "y": 400
    }

    camera = {
        "x": 0,
        "y": 0,
    }

    player = Player(space, (player_start_cord["x"], player_start_cord["y"]))

    enemies = [BasicEnemy(space, 40)]
    structures = [Wall(space, (400, 775), (800, 50), color=(105, 86, 73, 100))]

    inputs = {
        "A": False,
        "D": False,
        "W": False,
        "S": False
    }

    def __init__(self, width, height, fps):
        assert(type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.fps = fps

    def draw(self):
        self.window.fill("royalblue")
        self.space.debug_draw(self.draw_options)
        # pygame.display.update()
        for item in self.structures:
            self.window.blit(item, (item.body.position.x - self.camera["x"], item.body.position.y - self.camera["y"]))
        for item in self.enemies:
            self.window.blit(item, (item.body.position.x - self.camera["x"], item.body.position.y - self.camera["y"]))
        self.window.blit(self.player, (self.player.body.position.x - self.camera["x"],
                                       self.player.body.position.y - self.camera["y"]))
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


if __name__ == "__main__":
    game = Game(800, 800, 60)
    game.run()