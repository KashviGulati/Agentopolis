import random


class DecisionModel:

    def choose_action(self, agent):

        # Work score increases if agent is poor
        work_score = max(0, 10 - agent.money) * agent.work_ethic

        # Food score increases if agent is hungry
        food_score = max(0, 10 - agent.food)

        # Exploration influenced by personality
        explore_score = random.randint(1, 5) * agent.exploration_bias

        scores = {
            "work": work_score,
            "buy_food": food_score,
            "explore": explore_score
        }

        # choose highest score
        action = max(scores, key=scores.get)

        return action