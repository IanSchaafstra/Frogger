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

    def update(self):
        keys = pygame.key.get_just_pressed()  # input handling happens within the update function for now. We could implement an input handling script later and pass it as a parameter.
        if keys[pygame.K_w]:
            self.pos.y -= 64
            self.rot_sprite = pygame.transform.rotate(self.sprite, 0)
        if keys[pygame.K_s]:
            self.pos.y += 64
            self.rot_sprite = pygame.transform.rotate(self.sprite, 180)
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

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "green", self.rect)
        screen.blit(self.rot_sprite, self.pos)
