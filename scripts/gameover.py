import pygame
import sys
import os

from player import Player


class GameOver:
    def __init__(self):
        if os.name == "nt":
            self.path = os.path.join("assets", "Gameover.png")
        elif os.name == "posix":
            try:
                self.path = os.path.join("..", "assets", "Gameover.png")
            except FileNotFoundError:
                try:
                    self.path = os.path.join("assets", "Gameover.png")
                except FileNotFoundError:
                    print("File Gameover.png could not be loaded. Exiting.")
                    sys.exit()
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

        self.game_over = False

    def set_game_over(self):
        self.game_over = True

    def draw(self, screen: pygame.Surface):
        if self.game_over:
            screen.blit(self.image, self.rect)
