import pygame
import pymunk
import pymunk.pygame_util
from classes.enemies.basic import BasicEnemy

pygame.init()

class Game:
    isRunning = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    window = None
    space = pymunk.Space()
    gravity = (0, 9.81)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    objects = [BasicEnemy(space, 50)]



    def __init__(self, width, height, fps):
        assert(type(width) == int and type(height) == int)
        self.window = pygame.display.set_mode((width, height))
        self.fps = fps

    def draw(self):
        self.window.fill("royalblue")
        pygame.display.update()

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                    break
            self.draw()
            self.space.step(self.dt)
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game(800,800, 60)
    game.run()