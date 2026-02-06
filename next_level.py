import pygame
import os
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from gameobject import GameObject


class NextLevel(GameObject):
    def __init__(self):
        script_dir = os.path.dirname(__file__)

        self.font_path = os.path.join(script_dir, "assets", "fontPixel.ttf")
        self.font = pygame.Font(self.font_path, size=40)
        self.font

        self.curtain = SCREEN_HEIGHT  # NOTE: Just like in gameover.py, this controls the gradual covering of the screen. The higher the value, the lower the top of the black box is.
        self.transition = True
        self.timer = 0.0  # NOTE: this is used to extend the time the screen is black
        self.post_timer = 0.0  # NOTE: this is used to add some extra time to the transition while the level resets. Without this, you can see the level reset prematurely.
        self.n_level = 1
        self.text = self.font.render(
            f"Level {self.n_level}", antialias=False, color="white"
        )
        self.draw_pos = pygame.Vector2(
            SCREEN_WIDTH // 2 - self.text.width // 2, SCREEN_HEIGHT // 3
        )
        self.start_rect_block = pygame.Rect(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT
        )  # NOTE: This is used to make the screen completely black when the game launches. Otherwise, it would cover gradually like a regular transition.
        self.post_transition = False

    def update(self, dt: float, input_tap, input_hold):
        if self.transition:
            self.post_transition = False
            if self.curtain > 0:
                self.curtain -= 800 * dt
            elif self.timer < 0.5:
                self.timer += dt
                pass
            else:
                self.transition = False
                self.post_transition = True
                self.timer = 0.0

        if self.post_transition:
            self.post_timer += dt
            if self.post_timer < 0.3:
                pass
            else:
                self.post_transition = False
                self.post_timer = 0.0
                self.curtain = SCREEN_HEIGHT

            self.true_timer = self.timer
            self.timer += dt
        self.text = self.font.render(
            f"Level {self.n_level}", antialias=False, color="white"
        )
        self.curtain_rect = pygame.Rect(
            0, self.curtain, SCREEN_WIDTH, SCREEN_HEIGHT + 200
        )

    def draw(self, screen: pygame.Surface):
        if self.transition or self.post_transition:
            if self.n_level == 1:
                pygame.draw.rect(screen, "black", self.start_rect_block)
                screen.blit(self.text, self.draw_pos)
            else:
                pygame.draw.rect(screen, "black", self.curtain_rect)
                if self.curtain < SCREEN_HEIGHT / 3:
                    screen.blit(self.text, self.draw_pos)

    def set_transition(self):
        self.transition = True

    def increase_level(self):
        self.n_level += 1

    def reset_level(self):
        self.n_level = 1

    def get_level(self):
        return self.n_level

    def get_transition(self) -> bool:
        return self.transition
