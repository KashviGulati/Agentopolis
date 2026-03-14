class Market:

    def __init__(self):
        self.food_price = 5

    def buy_food(self, agent):

        if agent.money >= self.food_price:
            agent.money -= self.food_price
            agent.food += 3
            return True

        return False