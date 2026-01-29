import pygame
import os
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class NextLevel:
    def __init__(self):
        script_dir = os.path.dirname(__file__)

        self.font_path = os.path.join(script_dir, "..", "assets", "fontPixel.ttf")
        self.font = pygame.Font(self.font_path)

        self.curtain_mark = SCREEN_HEIGHT
        self.transition = False
        self.timer = 0.0
        self.n_level = 0
        self.text = self.font.render(
            f"Level {self.n_level}", antialias=False, color="white"
        )
        self.draw_pos = pygame.Vector2(
            SCREEN_WIDTH // 2 + self.text.width // 2, SCREEN_HEIGHT // 3
        )

    def set_transition(self):
        self.transition = True

    def update(self, dt: float):
        if self.transition:
            if self.curtain_mark > 0:
                self.curtain_mark -= 50 * dt
            elif self.timer < 1:
                self.timer += dt
            else:
                self.transition = False
                self.timer = 0.0
        self.text = self.font.render(
            f"Level {self.n_level}", antialias=False, color="white"
        )
        self.curtain_rect = pygame.Rect(
            0, SCREEN_HEIGHT, SCREEN_WIDTH, self.curtain_mark
        )

    def draw(self, screen: pygame.Surface):
        if self.transition:
            pygame.draw.rect(screen, "black", self.curtain_rect)
            screen.blit(self.text, self.draw_pos)

    def increase_level(self):
        self.n_level += 1

    def get_transition(self) -> bool:
        return self.transition
