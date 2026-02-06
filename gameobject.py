import pygame
from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def update(self, dt: float, input_tap, input_hold):
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
