import numpy as np
import random


class Environment:

    def __init__(self, size=20):
        self.size = size
        self.grid = np.zeros((size, size))

        self.food_locations = []
        self.work_locations = []

        self.generate_resources()

    def generate_resources(self):

        # generate food locations
        for _ in range(10):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.food_locations.append((x, y))

        # generate work locations
        for _ in range(5):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            self.work_locations.append((x, y))

    def is_food_location(self, pos):
        return pos in self.food_locations

    def is_work_location(self, pos):
        return pos in self.work_locations

    # NEW: agents can work near workplace
    def near_work_location(self, pos):

        x, y = pos

        for wx, wy in self.work_locations:

            if abs(wx - x) <= 1 and abs(wy - y) <= 1:
                return True

        return False
    def nearest_workplace(self, pos):

        x, y = pos

        nearest = None
        min_dist = float("inf")

        for wx, wy in self.work_locations:

            dist = abs(wx - x) + abs(wy - y)

            if dist < min_dist:
                min_dist = dist
                nearest = (wx, wy)

        return nearest