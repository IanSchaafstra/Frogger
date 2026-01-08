import pygame


pygame.init()


class Player:
    def __init__(self, location: pygame.Vector2) -> None:
        self.pos = location
        self.sprite = pygame.image.load("../assets/Frog.png")
        self.rect = self.sprite.get_rect(topleft=self.pos)

    def update(self):
        keys = pygame.key.get_just_pressed()  # input handling happens within the update function for now. We could implement an input handling script later and pass it as a parameter.
        if keys[pygame.K_w]:
            for i in range(16):
                self.pos.y -= 4
                self.rect = pygame.Rect(self.pos.x, self.pos.y, 64, 64)
        if keys[pygame.K_s]:
            self.pos.y += 64
        if keys[pygame.K_a]:
            self.pos.x -= 64
        if keys[pygame.K_d]:
            self.pos.x += 64
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 64, 64)

    def draw(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "green", self.rect)
        screen.blit(self.sprite, self.pos)
