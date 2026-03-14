import random

class Agent:

    def __init__(self, agent_id, grid_size):

        self.agent_id = agent_id

        self.money = 50
        self.food = 5
        self.energy = 10

        self.x = random.randint(0, grid_size-1)
        self.y = random.randint(0, grid_size-1)

        self.alive = True

    def move(self, grid_size):

        dx = random.choice([-1,0,1])
        dy = random.choice([-1,0,1])

        self.x = max(0, min(grid_size-1, self.x + dx))
        self.y = max(0, min(grid_size-1, self.y + dy))

    def position(self):
        return (self.x, self.y)

    def consume_food(self):

        self.food -= 1

        if self.food <= 0:
            self.alive = False