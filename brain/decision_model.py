import random


class DecisionModel:

    def choose_action(self, agent):

        # work motivation increases when poor
        work_score = max(0, 20 - agent.money) * agent.work_ethic

        # food urgency increases when hungry
        food_score = max(0, 12 - agent.food) * agent.food_priority

        # exploration personality
        explore_score = random.randint(1, 5) * agent.exploration_bias

        scores = {
            "work": work_score,
            "buy_food": food_score,
            "explore": explore_score
        }

        return max(scores, key=scores.get)