import random


class Environment:

    def __init__(self, size=30):

        self.size = size

        # city grid
        self.grid = [["empty" for _ in range(size)] for _ in range(size)]

        self.work_locations = []
        self.market_locations = []
        self.housing_locations = []

        self.generate_city()

    def generate_city(self):

        # workplaces
        for _ in range(6):

            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            self.grid[x][y] = "work"
            self.work_locations.append((x, y))

        # markets
        for _ in range(4):

            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            self.grid[x][y] = "market"
            self.market_locations.append((x, y))

        # housing
        for _ in range(10):

            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            self.grid[x][y] = "housing"
            self.housing_locations.append((x, y))

    def near_work_location(self, pos):

        x, y = pos

        for wx, wy in self.work_locations:
            if abs(wx - x) <= 1 and abs(wy - y) <= 1:
                return True

        return False

    def near_market(self, pos):

        x, y = pos

        for mx, my in self.market_locations:
            if abs(mx - x) <= 1 and abs(my - y) <= 1:
                return True

        return False

    def nearest_workplace(self, pos):

        x, y = pos

        return min(
            self.work_locations,
            key=lambda w: abs(w[0] - x) + abs(w[1] - y)
        )

    def nearest_market(self, pos):

        x, y = pos

        return min(
            self.market_locations,
            key=lambda m: abs(m[0] - x) + abs(m[1] - y)
        )