import pygame
import sys
import os

from player import Player


class GameOver:
    def __init__(self):
        if os.name == "nt":
            self.path_game_over = os.path.join("assets", "Gameover.png")
            self.path_score = os.path.join("assets", "Score.png")
            self.path_press_space = os.path.join("assets", "PressSpace.png")
            self.path_press_a = os.path.join("assets", "PressA.png")
        elif os.name == "posix":
            try:
                self.path_game_over = os.path.join("..", "assets", "Gameover.png")
                self.path_score = os.path.join("..", "assets", "Score.png")
                self.path_press_space = os.path.join("..", "assets", "PressSpace.png")
                self.path_press_a = os.path.join("..", "assets", "PressA.png")
            except FileNotFoundError:
                try:
                    self.path_game_over = os.path.join("assets", "Gameover.png")
                    self.path_score = os.path.join("assets", "Score.png")
                    self.path_press_space = os.path.join("assets", "PressSpace.png")
                    self.path_press_a = os.path.join("assets", "PressA.png")
                except FileNotFoundError:
                    print("File Gameover.png could not be loaded. Exiting.")
                    sys.exit()
        self.image_game_over = pygame.image.load(self.path_game_over)
        self.image_score = pygame.image.load(self.path_score)
        self.image_press_space = pygame.image.load(self.path_press_space)
        self.image_press_a = pygame.image.load(self.path_press_a)
        self.rect = self.image_game_over.get_rect()
        self.game_over = False
        self.curtain = 0
        self.curtainRect = pygame.Rect((0, 0), (1280, 0))
        self.timer = 0

    def set_game_over(self):
        self.game_over = True

    def reset(self):
        self.game_over = False
        self.curtain = 0
        self.timer = 0

    def draw(self, screen: pygame.Surface):
        if self.game_over:
            if self.curtain < 970:
                self.curtainRect = pygame.Rect((0, 0), (1280, self.curtain))
                self.curtain += 10
            pygame.draw.rect(screen, "black", self.curtainRect)
            if self.curtain > 960:
                screen.blit(self.image_game_over, self.rect)
                self.timer += 1
                if self.timer > 10:
                    screen.blit(self.image_score, self.image_score.get_rect())
                if self.timer > 20 and (self.timer // 10) % 2 == 0:
                    screen.blit(
                        self.image_press_space, self.image_press_space.get_rect()
                    )
