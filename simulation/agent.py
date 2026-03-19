import random
from brain.decision_model import DecisionModel
from brain.reinforcement_learning import QLearning

class Agent:

    def __init__(self, agent_id, grid_size):

        if random.random() < 0.5:
            self.x = random.choice([10, 20])
            self.y = random.randint(0, grid_size - 1)
        else:
            self.y = random.choice([10, 20])
            self.x = random.randint(0, grid_size - 1)

        self.agent_id = agent_id

        # --- resources ---
        self.money = 50
        self.food = 5
        self.energy = 10

        

        self.alive = True
        

        self.current_action = None
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

        self.rl = QLearning()
        self.last_state = None
        self.last_action = None

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

    def decide(self, market):

        state = self.rl.get_state(self, market)

        action = self.rl.choose_action(state)

        self.current_action = action   
        self.last_state = state
        self.last_action = action

        return action

    def consume_food(self):

        # probabilistic food consumption
        if random.random() < 0.4:
            self.food -= 1

        if self.food <= 0:
            self.alive = False