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

    # smooth demand-based pricing
        if self.transactions > 20:
            self.food_price += 0.5

        elif self.transactions < 15:
            self.food_price -= 0.5

        print("Transactions:", self.transactions, "Price BEFORE:", self.food_price)
        # clamp values
        self.food_price = max(3, min(self.food_price, 20))

        # reset
        self.transactions = 0
        print("Price AFTER:", self.food_price)