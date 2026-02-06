import pygame
import sys
import os

from player import Player
from highscore import HighScore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOver:
    def __init__(self, player: Player, highscore: HighScore):
        curr_dir = os.path.dirname(__file__)
        self.assets_path = os.path.join(curr_dir, "assets")
        self.path_font = os.path.join(curr_dir, "assets", "fontPixel.ttf")
        self.font = pygame.Font(self.path_font, size=120)
        self.game_over_sound_path = os.path.join(
            curr_dir, "assets", "sounds", "GameOver.wav"
        )
        self.item_sound_path = os.path.join(self.assets_path, "GameOverItemAppear.wav")
        self.image_game_over = pygame.image.load(
            os.path.join(self.assets_path, "Gameover.png")
        )
        self.image_score = pygame.image.load(
            os.path.join(self.assets_path, "Score.png")
        )
        self.image_press_space = pygame.image.load(
            os.path.join(self.assets_path, "PressSpace.png")
        )
        self.image_press_a = pygame.image.load(
            os.path.join(self.assets_path, "PressA.png")
        )
        self.rect = self.image_game_over.get_rect()
        self.game_over = False
        self.curtain = 0
        self.curtainRect = pygame.Rect((0, 0), (SCREEN_WIDTH, 0))
        self.timer = 0
        self.player = player
        self.highscore = highscore
        self.n_points = self.player.get_score()

        self.game_over_sound = pygame.Sound(
            os.path.join(self.assets_path, "sounds", "GameOver.wav")
        )
        self.item_sound = pygame.Sound(
            os.path.join(self.assets_path, "sounds", "GameOverItemAppear.wav")
        )

        self.game_over_sound_played = False
        self.score_sound_played = False
        self.press_key_sound_played = False

    def set_game_over(self):
        self.game_over = True
        # self.game_over_sound.play()

    def reset(self):
        self.game_over = False
        self.curtain = 0
        self.timer = 0
        self.game_over_sound_played = False
        self.score_sound_played = False
        self.press_key_sound_played = False

    def update(self, dt: float):
        if self.game_over:
            if self.curtain < SCREEN_HEIGHT + 20:
                self.curtain += 1000 * dt

            self.timer += dt

    def draw(self, screen: pygame.Surface):
        self.n_points = self.player.get_score()
        score_surf = self.font.render(str(self.player.get_score()), False, "white")
        hiscore_surf = self.font.render(
            str(self.highscore.get_highscore()), False, "white"
        )
        if self.game_over:
            if self.curtain < SCREEN_HEIGHT + 20:
                self.curtainRect = pygame.Rect((0, 0), (SCREEN_WIDTH, self.curtain))
            pygame.draw.rect(screen, "black", self.curtainRect)
            if self.curtain > SCREEN_HEIGHT:
                if not self.game_over_sound_played:
                    self.item_sound.play()
                    self.game_over_sound_played = True
                screen.blit(self.image_game_over, self.rect)
                if self.timer > 1.5:
                    if not self.score_sound_played:
                        self.item_sound.play()
                        self.score_sound_played = True
                    screen.blit(self.image_score, self.image_score.get_rect())
                    screen.blit(score_surf, (680, 375))
                    screen.blit(hiscore_surf, (680, 525))
                if self.timer > 2 and int(self.timer) < self.timer - 0.4:
                    if not self.press_key_sound_played:
                        self.item_sound.play()
                        self.press_key_sound_played = True
                    screen.blit(
                        self.image_press_space, self.image_press_space.get_rect()
                    )
