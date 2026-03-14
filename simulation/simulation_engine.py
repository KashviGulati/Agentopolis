from simulation.environment import Environment
from simulation.agent import Agent
from simulation.market import Market

import matplotlib.pyplot as plt
import time


class Simulation:

    def __init__(self, num_agents=100):

        self.environment = Environment()
        self.market = Market()
        self.population_history = []
        self.price_history = []
        self.wealth_history = []

        self.agents = []

        for i in range(num_agents):
            self.agents.append(Agent(i, self.environment.size))

        # setup visualization
        plt.ion()
        self.fig, self.ax = plt.subplots()


    def step(self):

        for agent in self.agents:

            if not agent.alive:
                continue

            action = agent.decide()

            pos = agent.position()

            if action == "work":

                if self.environment.near_work_location(pos):
                    agent.money += 5
                else:
                    target = self.environment.nearest_workplace(pos)
                    agent.move_toward(target, self.environment.size)
            elif action == "buy_food":

                traded = self.agent_trade(agent)

                if not traded:
                    success = self.market.buy_food(agent)

                    if not success:
                        agent.move(self.environment.size)

            elif action == "explore":

                agent.move(self.environment.size)

            agent.consume_food()


    def draw(self, step):

        self.ax.clear()

        xs = []
        ys = []
        colors = []

        for agent in self.agents:

            if not agent.alive:
                continue

            xs.append(agent.x)
            ys.append(agent.y)

            if agent.money > 80:
                colors.append("green")
            elif agent.money > 30:
                colors.append("yellow")
            else:
                colors.append("red")

        self.ax.scatter(xs, ys, c=colors)

        # plot workplaces
        wx = [x for x, y in self.environment.work_locations]
        wy = [y for x, y in self.environment.work_locations]

        self.ax.scatter(wx, wy, marker="s")

        self.ax.set_title(f"Step {step} | Food Price: {self.market.food_price}")
        self.ax.set_xlim(0, self.environment.size)
        self.ax.set_ylim(0, self.environment.size)

        plt.draw()
        plt.pause(0.01)


    def run(self, steps=100):

        for step in range(steps):

            self.step()
            self.market.update_price()
            self.draw(step)

            alive_agents = sum(agent.alive for agent in self.agents)

            wealth = [agent.money for agent in self.agents if agent.alive]
            self.wealth_history.append(wealth)
            
            self.population_history.append(alive_agents)
            self.price_history.append(self.market.food_price)

            print(f"Step {step} | Alive: {alive_agents} | Food Price: {self.market.food_price}")

            time.sleep(0.05)
    def agent_trade(self, buyer):

        for seller in self.agents:

            if seller is buyer:
                continue

            if not seller.alive:
                continue

            # seller must have extra food
            if seller.food > 6:

                # must be near each other
                if abs(seller.x - buyer.x) <= 1 and abs(seller.y - buyer.y) <= 1:

                    price = self.market.food_price

                    if buyer.money >= price:

                        buyer.money -= price
                        buyer.food += 2

                        seller.money += price
                        seller.food -= 2

                        return True

        return False