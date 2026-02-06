from abc import ABC, abstractmethod
import pygame

from player import Player
from score import Score
from gameover import GameOver
from highscore import HighScore
from gameobject import GameObject


class GameMode(GameObject, ABC):
    @abstractmethod
    def __init__(self, name: str, screen: pygame.Surface):
        self.name = name
        self.screen = screen
        self.gameobjects = []

    @abstractmethod
    def update(self, dt: float, input_tap, input_hold):
        for item in self.gameobjects:
            item.update(dt, input_tap, input_hold)

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        for item in self.gameobjects:
            item.draw(screen)
