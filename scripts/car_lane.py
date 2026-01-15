import pygame
import random
from car import Car

class CarLane:
    speed = 200.0

    def __init__(self, y: int, driving_rightwards: bool, speed_multiplier: float = 1):
        self.y: int = y
        self.driving_rightwards: bool = driving_rightwards
        self.cars: list[Car] = []
        self.time_until_next_car: float = 0.0
        self.speed_multiplier = speed_multiplier

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
                self.cars.append(Car(-128, self.y, True, CarLane.speed * self.speed_multiplier))
            else:
                self.cars.append(Car(1280, self.y, False, CarLane.speed * self.speed_multiplier))
            self.time_until_next_car += random.randint(1000, 4000) / 1000

    def draw(self, surface: pygame.Surface):
        for car in self.cars:
            car.draw(surface)