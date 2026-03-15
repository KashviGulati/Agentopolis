import random


class QLearning:

    def __init__(self):

        # Q-table: (state, action) → value
        self.q_table = {}

        self.learning_rate = 0.1
        self.discount = 0.9
        self.epsilon = 0.1   # exploration probability

        self.actions = ["work", "buy_food", "explore"]

    def get_state(self, agent, market):

        # simple discretized state

        food_state = "low_food" if agent.food < 4 else "ok_food"
        money_state = "poor" if agent.money < 20 else "rich"
        price_state = "high_price" if market.food_price > 6 else "low_price"

        return (food_state, money_state, price_state)

    def choose_action(self, state):

        # exploration
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        # exploitation
        q_values = [self.q_table.get((state, a), 0) for a in self.actions]

        max_q = max(q_values)
        best_actions = [
            a for a, q in zip(self.actions, q_values) if q == max_q
        ]

        return random.choice(best_actions)

    def update(self, state, action, reward, next_state):

        current_q = self.q_table.get((state, action), 0)

        future_q = max(
            [self.q_table.get((next_state, a), 0) for a in self.actions]
        )

        new_q = current_q + self.learning_rate * (
            reward + self.discount * future_q - current_q
        )

        self.q_table[(state, action)] = new_q