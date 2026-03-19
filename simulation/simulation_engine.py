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

        # plt.ion()
        # self.fig, self.ax = plt.subplots()

    def step(self):

        for agent in self.agents:

            if not agent.alive:
                continue

            action = agent.decide(self.market)

            pos = agent.position()

            reward = 0

            # WORK
            if action == "work":

                if self.environment.near_work_location(pos):

                    agent.money += 5
                    reward += 2

                else:

                    target = self.environment.nearest_workplace(pos)
                    agent.move_toward(target, self.environment.size)

            # BUY FOOD
            elif action == "buy_food":

                traded = self.agent_trade(agent)

                if traded:

                    reward += 3

                else:

                    pos = agent.position()

                    if self.environment.near_market(pos):

                        success = self.market.buy_food(agent)

                        if success:
                            reward += 2
                        else:
                            agent.move(self.environment.size)

                    else:

                        target = self.environment.nearest_market(pos)
                        agent.move_toward(target, self.environment.size)

            # EXPLORE
            elif action == "explore":

                agent.move(self.environment.size)
                reward += 0.5

            # SURVIVAL
            agent.consume_food()

            if agent.alive:
                reward += 1
            else:
                reward -= 10

            if agent.alive:
                new_state = agent.rl.get_state(agent, self.market)
            else:
                new_state = None

            agent.rl.update(
                agent.last_state,
                agent.last_action,
                reward,
                new_state
            )

    def draw(self, step):

        self.ax.clear()

        size = self.environment.size

        # draw city tiles
        for x in range(size):
            for y in range(size):

                tile = self.environment.grid[x][y]

                if tile == "work":
                    color = "gray"

                elif tile == "market":
                    color = "blue"

                elif tile == "housing":
                    color = "purple"

                else:
                    color = "lightgreen"

                rect = plt.Rectangle((x, y), 1, 1, color=color, alpha=0.5)
                self.ax.add_patch(rect)

        # draw agents
        xs = []
        ys = []
        colors = []

        for agent in self.agents:

            if not agent.alive:
                continue

            xs.append(agent.x + 0.5)
            ys.append(agent.y + 0.5)

            if agent.money > 80:
                colors.append("gold")
            elif agent.money > 30:
                colors.append("orange")
            else:
                colors.append("red")

        self.ax.scatter(xs, ys, c=colors, s=40)

        self.ax.set_xlim(0, size)
        self.ax.set_ylim(0, size)

        self.ax.set_aspect("equal")

        self.ax.set_title(
            f"Agentopolis City | Step {step} | Food Price: {self.market.food_price}"
        )

        plt.draw()
        plt.pause(0.01)

    def run(self, steps=100):

        for step in range(steps):

            self.step()
            self.market.update_price()
            # self.draw(step)

            alive_agents = sum(agent.alive for agent in self.agents)

            wealth = [agent.money for agent in self.agents if agent.alive]

            self.wealth_history.append(wealth)
            self.population_history.append(alive_agents)
            self.price_history.append(self.market.food_price)

            print(
                f"Step {step} | Alive: {alive_agents} | Food Price: {self.market.food_price}"
            )

            time.sleep(0.05)

    def agent_trade(self, buyer):

        for seller in self.agents:

            if seller is buyer:
                continue

            if not seller.alive:
                continue

            if seller.food > 6:

                if abs(seller.x - buyer.x) <= 1 and abs(seller.y - buyer.y) <= 1:

                    price = self.market.food_price

                    if buyer.money >= price:

                        buyer.money -= price
                        buyer.food += 2

                        seller.money += price
                        seller.food -= 2

                        return True

        return False