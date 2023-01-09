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
    space.gravity = (0, 500)
    space.damping = 0.5

    player = Player(space, (400, 400))

    enemies = [BasicEnemy(space, 40)]
    structures = [Wall(space, (400, 775), (800, 50), color=(105, 86, 73, 100))]

    inputs = {
        "A": False,
        "D": False
    }

    def __init__(self, width, height, fps):
        assert(type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)
        self.fps = fps

    def draw(self):
        self.window.fill("royalblue")
        self.space.debug_draw(self.draw_options)
        pygame.display.update()

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.inputs["D"] = False
                    if event.key == pygame.K_a:
                        self.inputs["A"] = False

            self.player.move_player(self.inputs)
            self.draw()
            self.space.step(self.dt)
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game(800, 800, 60)
    game.run()