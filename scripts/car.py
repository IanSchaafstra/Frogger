import pygame
from pygame import Rect, Color

class Car:
    def __init__(self, x: int, y: int, direction: int):
        
        self.hitbox = Rect(x, y, 64, 64)
        #direction 1 for right  -1 for left
        self.direction = direction

    def update(self, dt: float):
        self.hitbox.x += 0.2 * self.direction * dt

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, Color(255, 0, 0), self.hitbox)