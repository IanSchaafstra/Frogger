import sys

from classic import Classic
from inputhandling import Input_Handling

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

import pygame

pygame.init()


def main():
    SCREEN_RES = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)

    input_handling = Input_Handling()

    screen = pygame.display.set_mode(SCREEN_RES)

    clock = pygame.time.Clock()

    classic = Classic("classic", screen)

    gamemodes = [
        classic,
    ]

    curr_gamemode = classic

    dt = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("black")

        input_tap = input_handling.get_input_tap()
        input_hold = input_handling.get_input_hold()

        if curr_gamemode is not None:
            curr_gamemode.update(dt, input_tap, input_hold)
            curr_gamemode.draw(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000


if __name__ == "__main__":
    main()
