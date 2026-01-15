import pygame
from log import Log

class WaterLane:
    def __init__(self, y_pos, moving_right, speed, log_count):
        self.y_pos = y_pos
        self.height = 64
        self.speed_x = speed if moving_right else -speed
        self.water_color = (0, 119, 190)
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
        water_rect = pygame.Rect(0, self.y_pos, 1280, self.height)
        pygame.draw.rect(screen, self.water_color, water_rect)
        
        for log in self.logs:
            log.draw(screen)

    def get_log_at_position(self, player_rect):
        for log in self.logs:
            if player_rect.colliderect(log.rect):
                return log
        return None