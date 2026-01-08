import pygame


pygame.init()


class Player:
    def __init__(self) -> None:
        self.pos = pygame.Vector2(0, 0)
        self.sprite = pygame.Rect(self.pos.x, self.pos.y, 64, 64)

    def update(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 64
