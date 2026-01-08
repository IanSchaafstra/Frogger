import pygame

class Level:
    def __init__(self, player=None, screen_size=(1280, 960)):
        self.player = player
        self.screen_width, self.screen_height = screen_size

        self.background_color = (135, 206, 235)  # sky blue
        self.startfinish_color = (0, 255, 0)     # green
        self.platform_color = (100, 100, 100)    # grey

        # Platforms als lijst van pygame.Rect
        self.platforms = []
        # Voeg één testplatform in het midden
        self.platforms.append(pygame.Rect(0, 400, self.screen_width, 50))

    def update(self):
        # Hier zou je enemies/platform logic updaten
        pass

    def draw(self, screen):
        # Achtergrond
        screen.fill(self.background_color)

        # Start/Finish zones
        finish_height = 50
        start_height = 50
        pygame.draw.rect(screen, self.startfinish_color, (0, 0, self.screen_width, finish_height))  # boven
        pygame.draw.rect(screen, self.startfinish_color, (0, self.screen_height - start_height, self.screen_width, start_height))  # onder

        # Platforms
        for plat in self.platforms:
            pygame.draw.rect(screen, self.platform_color, plat)
