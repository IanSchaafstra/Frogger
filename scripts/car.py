import pygame
import os
from pygame import Rect, Color

class Car:
    def __init__(self, x: int, y: int, driving_rightwards: bool):
        if os.name == "posix":
            self.path = os.path.join("..", "assets", "Car.png")
        elif os.name == "nt":
            self.path = os.path.join("assets", "Car.png")
        else:
            print("Error with asset loading, please report")
            sys.exit()
        self.sprite = pygame.image.load(self.path)
        if driving_rightwards:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.hitbox = Rect(x, y, 128, 64)
        self.driving_rightwards = driving_rightwards

    def update(self, dt: float):
        movement = int(0.2 * dt)
        if not self.driving_rightwards:
            movement *= -1
        self.hitbox.x += movement

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.hitbox)