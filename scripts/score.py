import pygame
import os
from player import Player

pygame.init()


class Score:
    def __init__(self, player: Player):
        self.player = player
        self._score = 0

        if os.name == "posix":
            self.path = os.path.join("..", "assets", "font.ttf")
        elif os.name == "nt":
            self.path = os.path.join("assets", "font.ttf")

        self.font = pygame.font.Font(self.path, size=50)

    def update(self, dt: float):
        # dt isn't used, but is added for compatibility with other classes that use an update function

        self._score = self.player.get_score()

        self.surface = self.font.render(str(self._score), antialias=True, color="black")

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (50, 50))
