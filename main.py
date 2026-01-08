import pygame
import sys


pygame.init()
FPS = 60
SCREENX = 1280
SCREENY = 960
SCREEN_RES = pygame.Vector2(SCREENX, SCREENY)  # Screen resolution
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()


def main():
    dt = 0.0  # delta time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("grey")

        pygame.display.update()

        clock.tick(FPS)

        dt = clock.tick(FPS)  # delta time


if __name__ == "__main__":
    main()
