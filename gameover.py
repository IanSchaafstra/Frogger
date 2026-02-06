import pygame
import sys
import os

from player import Player
from highscore import HighScore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from gameobject import GameObject


class GameOver(GameObject):
    def __init__(self, player: Player, highscore: HighScore):
        curr_dir = os.path.dirname(__file__)

        # NOTE: Asset loading
        self.assets_path = os.path.join(curr_dir, "assets")
        self.font = pygame.Font(
            os.path.join(self.assets_path, "fontPixel.ttf"), size=120
        )
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
        )  # NOTE: unused, this is the same as Pressspace.png except it tells you to press A.

        self.rect = self.image_game_over.get_rect()
        self.game_over = False
        self.curtain = 0  # NOTE: this variable keeps track of the "curtain" that's drawn before the game over screen appears.
        self.curtainRect = pygame.Rect((0, 0), (SCREEN_WIDTH, 0))
        self.timer = 0
        self.player = player
        self.highscore = highscore
        self.n_points = self.player.get_score()

        self.game_over_sound = pygame.Sound(  # NOTE: currently unused.
            os.path.join(self.assets_path, "sounds", "GameOver.wav")
        )
        self.item_sound = pygame.Sound(
            os.path.join(self.assets_path, "sounds", "GameOverItemAppear.wav")
        )

        # NOTE: State management
        self.game_over_sound_played = False
        self.score_sound_played = False
        self.press_key_sound_played = False  # NOTE: These 3 variables keep track of whether a sound is already played during the game over screen. This is to prevent it from playing multiple times.

    def update(self, dt: float, input_tap, input_hold):
        if self.game_over:
            if (
                self.curtain < SCREEN_HEIGHT + 20
            ):  # NOTE: The + 20 is to accomodate for any inconsistencies introduced by implementing delta time.
                self.curtain += 1000 * dt

            self.timer += dt

        self.n_points = self.player.get_score()
        self.score_surf = self.font.render(str(self.player.get_score()), False, "white")
        self.hiscore_surf = self.font.render(
            str(self.highscore.get_highscore()), False, "white"
        )

    def draw(self, screen: pygame.Surface):
        self.game_over_drawing(screen)

    def reset(self):
        self.game_over = False
        self.curtain = 0
        self.timer = 0
        self.game_over_sound_played = False
        self.score_sound_played = False
        self.press_key_sound_played = False

    def set_game_over(self):
        self.game_over = True
        # self.game_over_sound.play()
        #

    def game_over_drawing(self, screen: pygame.Surface):
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
                    screen.blit(self.score_surf, (680, 375))
                    screen.blit(self.hiscore_surf, (680, 525))
                if self.timer > 2 and int(self.timer) < self.timer - 0.4:
                    if not self.press_key_sound_played:
                        self.item_sound.play()
                        self.press_key_sound_played = True
                    screen.blit(
                        self.image_press_space, self.image_press_space.get_rect()
                    )
