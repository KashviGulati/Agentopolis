import random
from brain.decision_model import DecisionModel


class Agent:

    def __init__(self, agent_id, grid_size):

        self.agent_id = agent_id

        # --- resources ---
        self.money = 50
        self.food = 5
        self.energy = 10

        # --- position ---
        self.x = random.randint(0, grid_size - 1)
        self.y = random.randint(0, grid_size - 1)

        self.alive = True

        # --- personality traits ---
        self.work_ethic = random.uniform(0.5, 1.5)
        self.risk_tolerance = random.uniform(0.5, 1.5)
        self.exploration_bias = random.uniform(0.5, 1.5)
        self.sociability = random.uniform(0.5, 1.5)
        self.food_priority = random.uniform(0.5, 1.5)

        # --- memory system ---
        self.memory = {
            "last_food_price": None,
            "successful_trades": 0
        }

        # --- decision system ---
        self.brain = DecisionModel()

    def move(self, grid_size):

        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        self.x = max(0, min(grid_size - 1, self.x + dx))
        self.y = max(0, min(grid_size - 1, self.y + dy))

    def move_toward(self, target, grid_size):

        tx, ty = target

        if tx > self.x:
            self.x += 1
        elif tx < self.x:
            self.x -= 1

        if ty > self.y:
            self.y += 1
        elif ty < self.y:
            self.y -= 1

        self.x = max(0, min(grid_size - 1, self.x))
        self.y = max(0, min(grid_size - 1, self.y))

    def position(self):
        return (self.x, self.y)

    def decide(self):
        return self.brain.choose_action(self)

    def consume_food(self):

        # probabilistic food consumption
        if random.random() < 0.4:
            self.food -= 1

        if self.food <= 0:
            self.alive = False