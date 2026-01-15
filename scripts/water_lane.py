import os
import pygame
from log import Log

class WaterLane:
    def __init__(self, y_pos, moving_right, speed, log_count):
        self.y_pos = y_pos
        self.height = 64
        self.speed_x = speed if moving_right else -speed
        # self.water_color = (0, 119, 190)

        script_dir = os.path.dirname(__file__)
        water_path = os.path.join(script_dir, '..', 'assets', 'Water.png')
        self.water_image = pygame.image.load(water_path).convert_alpha()

        self.logs = []
        
        spacing = 1280 // log_count
        for i in range(log_count):
            x = i * spacing
            log = Log(x, y_pos + 8)
            self.logs.append(log)
    
    def update(self):
        for log in self.logs:
            log.update(self.speed_x, 1280)
    
    def draw(self, screen):
        tile_width = self.water_image.get_width()
        for x in range(0, 1280, tile_width):
            screen.blit(self.water_image, (x, self.y_pos))
        
        for log in self.logs:
            log.draw(screen)

    def get_log_at_position(self, player_rect):
        for log in self.logs:
            if player_rect.colliderect(log.rect):
                return log
        return None