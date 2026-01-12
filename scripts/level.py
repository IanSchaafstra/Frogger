import pygame
import sys
from car_lane import CarLane

class Level:
    def __init__(self, player=None, screen_size=(1280, 960)):
        self.player = player
        self.screen_width, self.screen_height = screen_size

        self.background_color = (135, 206, 235)  # sky blue
        self.startfinish_color = (0, 255, 0)     # green
        self.platform_color = (100, 100, 100)    # grey

        self.platforms = []
        self.platforms.append(pygame.Rect(0, 400, self.screen_width, 50))

        self.finish_zone = pygame.Rect(0, 0, self.screen_width, 50)
        self.start_zone = pygame.Rect(0, self.screen_height - 50, self.screen_width, 50)        

        self.car_lanes: list[CarLane] = [CarLane(384, True), CarLane(448, False)]
    
        self._on_start_last_frame = False
        self._on_finish_last_frame = False

    def update(self, dt):
        # Hier zou je enemies/platform logic updaten
        for car_lane in self.car_lanes:
            car_lane.update(dt)

        on_start = self.player.rect.colliderect(self.start_zone)
        if on_start and not self._on_start_last_frame:
            print("Player on start zone")
        self._on_start_last_frame = on_start

        on_finish = self.player.rect.colliderect(self.finish_zone)
        if on_finish and not self._on_finish_last_frame:
            print("Finished!")
            self.reset_player()
        self._on_finish_last_frame = on_finish
        self.check_collisions()

    def check_collisions(self):
        for car_lane in self.car_lanes:
            if self.player.rect.collidelist([car.hitbox for car in car_lane.cars]) != -1:
                # hit car code
                sys.exit()

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

    def reset_player(self):
        self.player.pos.update(self.screen_width // 2, self.screen_height - 100)
        self.player.rect.topleft = (self.player.pos.x, self.player.pos.y)
