import pygame
import os
import sys


pygame.init()


class Player:
    def __init__(self, location: pygame.Vector2) -> None:
        self.pos = location
        if os.name == "posix":
            self.path = os.path.join("..", "assets", "Frog.png")
        elif os.name == "nt":
            self.path = os.path.join("assets", "Frog.png")
        else:
            print("Error with asset loading, please report")
            sys.exit()
        # if os.name == "posix":
        #    self.sprite = pygame.image.load("../assets/Frog.png")
        # elif os.name == "nt":
        #    self.sprite = pygame.image.load("..\\assets\\Frog.png")
        self.sprite = pygame.image.load(self.path)
        self.rot_sprite = self.sprite
        self.rect = self.sprite.get_rect(topleft=self.pos)

        self._score = 0
        self._score_marker = self.pos.y

    def update(self):
        keys = pygame.key.get_just_pressed()  # input handling happens within the update function for now. We could implement an input handling script later and pass it as a parameter.
        if keys[pygame.K_w]:
            self.pos.y -= 64
            self.rot_sprite = pygame.transform.rotate(self.sprite, 0)
        if keys[pygame.K_s]:
            self.rot_sprite = pygame.transform.rotate(self.sprite, 180)
            self.pos.y += 64
            if self.pos.y > 960 - self.rect.width:
                self.pos.y -= 64
        if keys[pygame.K_a]:
            self.rot_sprite = pygame.transform.rotate(self.sprite, 90)
            self.pos.x -= 64
            if self.pos.x < 0:
                self.pos.x += 64
        if keys[pygame.K_d]:
            self.rot_sprite = pygame.transform.rotate(self.sprite, -90)
            self.pos.x += 64
            if self.pos.x > 1280 - self.rect.width:
                self.pos.x -= 64
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 64, 64)
        self.update_score()

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "green", self.rect)
        screen.blit(self.rot_sprite, self.pos)

    def get_score(self) -> int:
        return self._score

    def update_score(self):
        if self.pos.y < self._score_marker:
            self._score += 1
            self._score_marker = self.pos.y

    def reset_player(self):
        self.pos = pygame.Vector2(1280 // 2, 960 - 64)
        self._score_marker = self.pos.y
