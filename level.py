import pygame
import sys
import os
from car_lane import CarLane
from water_lane import WaterLane
from player import Player
from gameover import GameOver
from highscore import HighScore
from next_level import NextLevel
from gameobject import GameObject
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class Level(GameObject):
    def __init__(
        self,
        player: Player,
        game_over: GameOver,
        highscore: HighScore,
        nextlevel: NextLevel,
    ):
        self.player = player
        self.gameover = game_over
        self.highscore = highscore
        self.nextlevel = nextlevel
        self.startfinish_color = (0, 255, 0)  # green
        self.platform_color = (100, 100, 100)  # grey

        # NOTE: textures
        script_dir = os.path.dirname(__file__)
        grass_image_path = os.path.join(script_dir, "assets", "Grass.png")
        self.grass_image = pygame.image.load(grass_image_path).convert_alpha()

        finish_image_path = os.path.join(script_dir, "assets", "Finish.png")
        self.finish_image = pygame.image.load(finish_image_path).convert_alpha()

        # NOTE: sounds
        self.splash_path = os.path.join(script_dir, "assets", "sounds", "Splash.wav")
        self.splash = pygame.Sound(self.splash_path)

        self.car_crash_path = os.path.join(
            script_dir, "assets", "sounds", "CarCrash.wav"
        )
        self.car_crash = pygame.Sound(self.car_crash_path)

        self.music_path = os.path.join(script_dir, "assets", "sounds", "FroggerBGM.wav")
        self.music = pygame.mixer.music.load(self.music_path)
        self.volume = pygame.mixer_music.get_volume()

        self.finish_zone = pygame.Rect(0, 0, SCREEN_WIDTH, 50)
        self.start_zone = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

        self.car_lanes: list[CarLane] = []
        self.water_lanes: list[WaterLane] = []

        self._on_start_last_frame = False
        self._on_finish_last_frame = False
        self.game_over = False
        self.dying = False
        self.dying_timer = 0.0
        self.transition = True
        self.first_transition = True

        self.dt = 0.0

        self.generate_level(self.player.get_score())

    def update(self, dt, input_tap, input_hold):
        self.dt = dt  # dt is now global

        old_transition = self.transition
        self.transition = self.nextlevel.get_transition()
        if old_transition != self.transition and old_transition:
            # NOTE: checks if the transition state (true or false) is diffirent from the one of the previous frame. If it is, it'll generate a new level.
            self.generate_level(self.player.get_score())
        self.player.set_freeze(self.transition)
        if self.dying:
            self.handle_dying_timer()  # NOTE: This decides which frame the death animation should display
            return
        if self.game_over:
            pygame.mixer_music.stop()
            self.nextlevel.reset_level()
            return
        elif self.transition:
            pygame.mixer_music.set_volume(0.2)
            return
        else:
            if self.first_transition:
                self.first_transition = False
                pygame.mixer_music.play(loops=-1)
            self.volume = pygame.mixer_music.get_volume()
            if self.volume < 1:
                self.volume += 0.05
            pygame.mixer_music.set_volume(self.volume)

            for car_lane in self.car_lanes:
                car_lane.update(dt)

            for water_lane in self.water_lanes:
                water_lane.update()

            self.check_water()
            self.check_collisions()

            on_start = self.player.rect.colliderect(self.start_zone)
            self._on_start_last_frame = on_start

            on_finish = self.player.rect.colliderect(self.finish_zone)
            if on_finish and not self._on_finish_last_frame:
                # NOTE: This handles moving from one level to the other
                self.nextlevel.set_transition()
                self.nextlevel.increase_level()
                self.player.reset_player()
            self._on_finish_last_frame = on_finish

    def draw(self, screen):
        # grass
        self.draw_grass(screen)

        # Start/Finish zones
        for x in range(0, SCREEN_WIDTH, self.finish_image.get_width()):
            screen.blit(self.finish_image, (x, 0))

        # Cars
        for car_lane in self.car_lanes:
            car_lane.draw(screen)

        # Water lanes
        for water_lane in self.water_lanes:
            water_lane.draw(screen)

    def handle_dying_timer(self):
        if self.dying_timer < 1:
            self.dying_timer += self.dt
        else:
            self.dying_timer = 0.0
            self.dying = False
            self.player.reset_player()

    def clear_lanes(self):
        self.car_lanes.clear()
        self.water_lanes.clear()

    def generate_level(self, score: int):
        self.clear_lanes()

        # increase car speed
        CarLane.speed = (
            200 + self.nextlevel.get_level() * 14
        )  # TODO: implement a proper speed increase system

        # load new lanes
        # every {lane_count_scaling} score add 1 water or car lane
        open_lanes = list(range(TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 3, TILE_SIZE))
        lane_count_scaling = 50
        level_difficulty = 200 + self.nextlevel.get_level() * 14 - lane_count_scaling

        # always fill third lane
        self.generate_lane(SCREEN_HEIGHT - TILE_SIZE * 3)

        # randomly fill other lanes
        while (
            level_difficulty > random.randint(0, lane_count_scaling)
            and len(open_lanes) >= 1
        ):
            next_lane = open_lanes[random.randint(0, len(open_lanes) - 1)]
            open_lanes.remove(next_lane)
            self.generate_lane(next_lane)
            level_difficulty -= lane_count_scaling

        # remove multi empty lanes
        previus_open_lane = 0
        for open_lane in open_lanes:
            if open_lane == previus_open_lane + TILE_SIZE:
                self.generate_lane(open_lane)
            else:
                previus_open_lane = open_lane

    def generate_lane(self, y: int):
        if random.randint(0, 1) == 0:
            self.car_lanes.append(
                CarLane(y, random.randint(0, 1) == 0, random.random() * 0.4 + 0.8)
            )
        else:
            self.water_lanes.append(
                WaterLane(
                    y,
                    random.randint(0, 1) == 0,
                    random.randint(2, 3),
                    random.randint(2, 4),
                )
            )

    def check_water(self):
        if self.game_over:
            return

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
            # print("Player drowned!")
            self.player_death()
            self.player.set_dying_type("splash")
            self.splash.play()

    def check_collisions(self):
        if self.game_over:
            return
        for car_lane in self.car_lanes:
            if (
                self.player.rect.collidelist([car.hitbox for car in car_lane.cars])
                != -1
            ):
                # hit car code
                # print("Player hit by car!")
                self.player_death()
                self.player.set_dying_type("crash")
                self.car_crash.play()

    def player_death(self):
        self.player.lose_live()
        if self.player.get_lives() <= 0:
            # print("game over")
            final_score = self.player.get_score()
            self.set_game_over(final_score)
            self.player.set_game_over()
            self.gameover.set_game_over()
        else:
            # print(f"lives left: {self.player.get_lives()}")
            self.dying = True

    def draw_grass(self, screen):
        for y in range(
            self.finish_image.get_height(), SCREEN_HEIGHT, self.grass_image.get_height()
        ):
            for x in range(0, SCREEN_WIDTH, self.grass_image.get_width()):
                screen.blit(self.grass_image, (x, y))

    def set_game_over(self, final_score):
        self.game_over = True
        if self.highscore:
            new_hs = self.highscore.update(final_score)
            # if new_hs:
            # print(f"New High Score: {final_score}!")

    def restart(self):
        self.game_over = False
        self.transition = True
        self.nextlevel.set_transition()
        self.nextlevel.reset_level()
        self.player.reset_after_game_over()
        self.gameover.reset()
        self._on_start_last_frame = False
        self._on_finish_last_frame = False
        self.generate_level(self.player.get_score())
        self.first_transition = True
