import numpy as np

class Environment:

    def __init__(self, size=20):
        self.size = size
        self.grid = np.zeros((size, size))

        self.food_locations = []
        self.work_locations = []

        self.generate_resources()

    def generate_resources(self):

        for _ in range(10):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)

            self.food_locations.append((x, y))

        for _ in range(5):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)

            self.work_locations.append((x, y))

    def is_food_location(self, pos):
        return pos in self.food_locations

    def is_work_location(self, pos):
        return pos in self.work_locations