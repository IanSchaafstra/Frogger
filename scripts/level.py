import pygame
import sys
from car_lane import CarLane
from water_lane import WaterLane
from player import Player
from gameover import GameOver


class Level:
    def __init__(self, player: Player, game_over: GameOver, screen_size=(1280, 960)):
        self.player = player
        self.gameover = game_over
        self.screen_width, self.screen_height = screen_size

        self.background_color = (0, 100, 0)  # Dark green
        self.startfinish_color = (0, 255, 0)  # green
        self.platform_color = (100, 100, 100)  # grey

        self.platforms = []
        self.platforms.append(pygame.Rect(0, 386, self.screen_width, 64))
        self.platforms.append(pygame.Rect(0, 448, self.screen_width, 64))

        self.finish_zone = pygame.Rect(0, 0, self.screen_width, 50)
        self.start_zone = pygame.Rect(0, self.screen_height - 50, self.screen_width, 50)

        self.car_lanes: list[CarLane] = [CarLane(384, True), CarLane(448, False)]
        self.water_lanes = [
            WaterLane(128, moving_right=True, speed=2, log_count=3),
            WaterLane(192, moving_right=False, speed=3, log_count=2),
            WaterLane(256, moving_right=True, speed=2, log_count=4),
        ]

        self._on_start_last_frame = False
        self._on_finish_last_frame = False
        self.game_over = False

    def update(self, dt):
        if self.game_over:
            return
        else:
            # Hier zou je enemies/platform logic updaten
            for car_lane in self.car_lanes:
                car_lane.update(dt)

            for water_lane in self.water_lanes:
                water_lane.update()

            self.check_water()
            self.check_collisions()

            on_start = self.player.rect.colliderect(self.start_zone)
            if on_start and not self._on_start_last_frame:
                print("Player on start zone")
            self._on_start_last_frame = on_start

            on_finish = self.player.rect.colliderect(self.finish_zone)
            if on_finish and not self._on_finish_last_frame:
                print("Finished!")
                self.player.reset_player()
            self._on_finish_last_frame = on_finish

    def check_water(self):
        on_water = False
        on_log = False

        for water_lane in self.water_lanes:
            if (
                self.player.rect.top < water_lane.y_pos + water_lane.height
                and self.player.rect.bottom > water_lane.y_pos
            ):
                on_water = True
                # print(f"Player in water lane at y={water_lane.y_pos}")  # DEBUG
                log = water_lane.get_log_at_position(self.player.rect)

                if log:
                    on_log = True
                    # print(f"Player on log!")  # DEBUG
                    self.player.move_with_log(water_lane.speed_x)
                    break

        # print(f"on_water: {on_water}, on_log: {on_log}")  # DEBUG
        if on_water and not on_log:
            print("Player drowned!")
            # self.player.reset_player()
            self.set_game_over()
            self.player.set_game_over()
            self.gameover.set_game_over()

    def check_collisions(self):
        for car_lane in self.car_lanes:
            if (
                self.player.rect.collidelist([car.hitbox for car in car_lane.cars])
                != -1
            ):
                # hit car code
                self.set_game_over()
                self.player.set_game_over()
                self.gameover.set_game_over()

    def draw(self, screen):
        screen.fill(self.background_color)

        # Start/Finish zones
        pygame.draw.rect(screen, self.startfinish_color, self.finish_zone)
        pygame.draw.rect(screen, self.startfinish_color, self.start_zone)

        # Platforms
        for plat in self.platforms:
            pygame.draw.rect(screen, self.platform_color, plat)

        # Cars
        for car_lane in self.car_lanes:
            car_lane.draw(screen)

            # Water lanes
            for water_lane in self.water_lanes:
                water_lane.draw(screen)
        # the reset_player function has been moved to player.py

        #    def reset_player(self):
        #        self.player.pos.update(self.screen_width // 2, self.screen_height - 100)
        #        self.player.rect.topleft = (
        #            self.player.pos.x,
        #            self.player.pos.y,
        # )  # this line is redundant. It doesn't seem to be causing issues, but it gives an error in my code editor.
        #

    def set_game_over(self):
        self.game_over = True
