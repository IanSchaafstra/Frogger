import pygame
import random
from car import Car

class CarLane:
    def __init__(self, y: int, driving_rightwards: bool):
        self.y: int = y
        self.driving_rightwards: bool = driving_rightwards
        self.cars: list[Car] = []
        self.time_until_next_car: float = 0.0

    def update(self, dt: float):
        # update cars
        for car in self.cars:
            car.update(dt)

        # remove offscreen cars
        if len(self.cars) > 0:
            first_car = self.cars[0]
            if first_car.hitbox.right < 0 or first_car.hitbox.left > 1280:
                self.cars.remove(first_car)

        # add new cars
        self.time_until_next_car -= dt
        if self.time_until_next_car <= 0:
            if self.driving_rightwards:
                self.cars.append(Car(-128, self.y, True))
            else:
                self.cars.append(Car(1280, self.y, False))
            self.time_until_next_car += random.randint(1000, 4000) / 1000

    def draw(self, surface: pygame.Surface):
        for car in self.cars:
            car.draw(surface)