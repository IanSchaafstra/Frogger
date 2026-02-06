from gamemode import GameMode

from player import Player
from score import Score
from gameover import GameOver
from highscore import HighScore
from level import Level
from next_level import NextLevel
from lives_counter import LivesCounter


from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
import pygame


class Classic(GameMode):
    def __init__(self, name: str, screen: pygame.Surface):
        super().__init__(name, screen)
        self.player = Player(
            pygame.Vector2(SCREEN_WIDTH / 2 - TILE_SIZE / 2, SCREEN_HEIGHT - TILE_SIZE)
        )
        self.highscore = HighScore()
        self.score = Score(self.player, self.highscore)
        self.gameover = GameOver(self.player, self.highscore)
        self.next_level = NextLevel()
        self.level = Level(self.player, self.gameover, self.highscore, self.next_level)
        self.lives_counter = LivesCounter(self.player)

        self.gameobjects = [
            self.level,
            self.score,
            self.lives_counter,
            self.player,
            self.next_level,
            self.gameover,
        ]

    def update(self, dt: float, input_tap, input_hold):
        return super().update(dt, input_tap, input_hold)

    def draw(self, screen: pygame.Surface):
        return super().draw(self.screen)
