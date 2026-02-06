from abc import ABC, abstractmethod
import pygame

from player import Player
from score import Score
from gameover import GameOver
from highscore import HighScore
from gameobject import GameObject


class GameMode(GameObject, ABC):
    @abstractmethod
    def __init__(
        self,
        name: str,
        player: Player,
        score: Score,
        gameover: GameOver,
        highscore: HighScore,
    ):
        self.name = name
        self.player = player
        self.score_class = Score
        self.gameover = gameover
        self.highscore = highscore
        self.gameobjects = [
            self.player,
            self.score_class,
            self.gameover,
            self.highscore,
        ]

    @abstractmethod
    def update(self, dt: float, input_tap, input_hold):
        for item in self.gameobjects:
            item.update(dt, input_tap, input_hold)

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        for item in self.gameobjects:
            item.draw(screen)
