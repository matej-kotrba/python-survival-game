import pygame

import math

class Wave:
    def __init__(self, game, number):
        self.game = game
        self.number = number
        self.active = False
        self.wave_start_counter = self.game.fps * 10
        self.counter = 0

        self.overview_surface = pygame.surface.Surface((200, 60))
        self.rect = self.overview_surface.get_rect()

        self.font = pygame.font.Font(None, 22)

    def check_status(self):
        if self.counter >= self.wave_start_counter and len(self.game.enemies) <= 0:
            self.game.wave = Wave(self.game, self.number)
        elif not self.active and self.counter >= self.wave_start_counter:
            self.active = True
            self.counter += 1
        else:
            self.counter += 1


    def display_overview(self):
        self.overview_surface.fill((53, 53, 53))

        text = self.font.render(f"Wave {self.number}, status - {'ACTIVE' if self.active else math.floor(self.counter / 60)}", True, (255, 255, 255))

        text_rect = text.get_rect()

        self.overview_surface.blit(text, ((200 - text_rect.width) / 2, (60 - text_rect.height / 2) / 2))
        self.game.window.blit(self.overview_surface, (self.game.window.get_width() - self.rect.width,
                              self.game.window.get_height() - self.rect.height))

    def __del__(self):
        print(f"Wave {self.number} has been completed !")