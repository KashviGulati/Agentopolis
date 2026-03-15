import random


class DecisionModel:

    def choose_action(self, agent):

        # --- work motivation ---
        work_score = max(0, 20 - agent.money) * agent.work_ethic

        # --- hunger motivation ---
        food_score = max(0, 10 - agent.food) * agent.food_priority

        # if price rising, buy earlier
        if agent.memory["last_food_price"] is not None:
            if agent.memory["last_food_price"] > 6:
                food_score *= 1.3

        # --- exploration ---
        explore_score = random.randint(1, 5) * agent.exploration_bias

        scores = {
            "work": work_score,
            "buy_food": food_score,
            "explore": explore_score
        }

        return max(scores, key=scores.get)