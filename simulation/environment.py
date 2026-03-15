import random


class Environment:

    def __init__(self, size=30):

        self.size = size

        # city zones
        self.work_locations = []
        self.market_locations = []
        self.housing_locations = []

        self.generate_city()

    def generate_city(self):

        # generate workplaces
        for _ in range(5):
            x = random.randint(2, self.size-3)
            y = random.randint(2, self.size-3)
            self.work_locations.append((x, y))

        # generate markets
        for _ in range(3):
            x = random.randint(2, self.size-3)
            y = random.randint(2, self.size-3)
            self.market_locations.append((x, y))

        # generate housing areas
        for _ in range(8):
            x = random.randint(2, self.size-3)
            y = random.randint(2, self.size-3)
            self.housing_locations.append((x, y))

    def near_work_location(self, pos):

        x, y = pos

        for wx, wy in self.work_locations:
            if abs(wx-x) <= 1 and abs(wy-y) <= 1:
                return True

        return False

    def near_market(self, pos):

        x, y = pos

        for mx, my in self.market_locations:
            if abs(mx-x) <= 1 and abs(my-y) <= 1:
                return True

        return False

    def nearest_workplace(self, pos):

        x, y = pos

        return min(
            self.work_locations,
            key=lambda w: abs(w[0]-x) + abs(w[1]-y)
        )

    def nearest_market(self, pos):

        x, y = pos

        return min(
            self.market_locations,
            key=lambda m: abs(m[0]-x) + abs(m[1]-y)
        )