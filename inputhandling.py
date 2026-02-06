import pygame


pygame.init()


class Input_Handling:
    def get_input_tap(self):
        return pygame.key.get_just_pressed()

    def get_input_hold(self):
        return pygame.key.get_pressed()
