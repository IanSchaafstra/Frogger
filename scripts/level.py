import pygame
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

        self.car_lane = CarLane(400, True)
    

    def update(self, dt):
        # Hier zou je enemies/platform logic updaten
        self.car_lane.update(dt)
        pass

    def draw(self, screen):
        screen.fill(self.background_color)

        # Start/Finish zones
        pygame.draw.rect(screen, self.startfinish_color, self.finish_zone) 
        pygame.draw.rect(screen, self.startfinish_color, self.start_zone)  

        # Platforms
        for plat in self.platforms:
            pygame.draw.rect(screen, self.platform_color, plat)
    
    def player_finished(self):
        # check if player is on finish zone
        if self.player.rect.colliderect(self.finish_zone):
            return True
        return False
    
    # def player_on_start(self):
    #     # check if player is on start zone
    #     if self.player.rect.colliderect(self.start_zone):
    #         return True
    #     return False
    
    # def reset_player(self):
    #     # reset player to start 
    #     self.player.pos.update(self.screen_width / 2 - 32, self.screen_height - 64)
    #     self.player.rect.topleft = (self.player.pos.x, self.player.pos.y)

        #car lane
        self.car_lane.draw(screen)
