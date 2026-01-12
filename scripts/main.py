import pygame
import sys
from player import Player
from level import Level
from score import Score


pygame.init()
FPS = 60
SCREENX = 1280
SCREENY = 960
SCREEN_RES = pygame.Vector2(SCREENX, SCREENY)  # Screen resolution
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()

player = Player(
    pygame.Vector2(SCREENX / 2 - 32, SCREENY - 64)
)  # location is defined in a not-so-neat manner, subject to change. Player starts out in the bottom-middle of the screen.


level = Level(player, SCREEN_RES)

score = Score(player)


def main():
    dt = 0.0  # delta time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        level.update(dt)
        player.update()
        score.update(dt)

        if level.player_finished():
            print("FINISH bereikt!")
            level.reset_player()

        # if level.player_on_start():
        #     print("Speler op start")

        level.draw(screen)
        player.draw(screen)
        score.draw(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000  # delta time


if __name__ == "__main__":
    main()
