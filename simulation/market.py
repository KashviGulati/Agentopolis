class Market:

    def __init__(self):

        self.food_price = 5
        self.transactions = 0


    def buy_food(self, agent):

        if agent.money >= self.food_price:

            agent.money -= self.food_price
            agent.food += 3

            self.transactions += 1
            return True

        return False


    def update_price(self):

        # demand based pricing
        if self.transactions > 30:
            self.food_price += 1

        elif self.transactions < 10:
            self.food_price -= 1

        # keep price within bounds
        self.food_price = max(3, min(self.food_price, 20))

        # reset demand counter
        self.transactions = 0