import pygame

class Log:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 192, 48)
        self.color = (139, 69, 19)
        
    def update(self, speed_x, screen_width):
        self.rect.x += speed_x
        
        # Wrap around screen
        if speed_x > 0:
            if self.rect.left > screen_width:
                self.rect.right = 0
        else:
            if self.rect.right < 0:
                self.rect.left = screen_width
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)