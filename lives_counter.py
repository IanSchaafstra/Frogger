import pygame
import os
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from gameobject import GameObject


class LivesCounter(GameObject):
    def __init__(self, player: Player):
        self.player = player

        curr_dir = os.path.dirname(__file__)

        self.sprite = pygame.image.load(os.path.join(curr_dir, "assets", "Frog.png"))

        self.sprite = pygame.transform.scale_by(self.sprite, 0.75)

    def update(self, dt: float, input_tap, input_hold):
        pass

    def draw(self, screen: pygame.Surface):
        x_pos = SCREEN_WIDTH - self.sprite.width
        lives_icons_offset = 8
        for i in range(self.player.get_lives()):
            screen.blit(self.sprite, (x_pos, 0))
            x_pos -= self.sprite.width + lives_icons_offset
