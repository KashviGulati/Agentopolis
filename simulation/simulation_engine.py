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

        # Track RL action usage
        self.action_history = {
            "work": [],
            "buy_food": [],
            "explore": []
        }

        for i in range(num_agents):
            self.agents.append(Agent(i, self.environment.size))

        # Visualization
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def step(self):

        for agent in self.agents:

            if not agent.alive:
                continue

            # RL chooses action
            action = agent.decide(self.market)

            # track action
            self.action_history[action].append(1)

            pos = agent.position()

            reward = 0

            # ---------- WORK ----------
            if action == "work":

                if self.environment.near_work_location(pos):

                    agent.money += 5
                    reward += 2

                else:

                    target = self.environment.nearest_workplace(pos)
                    agent.move_toward(target, self.environment.size)

            # ---------- BUY FOOD ----------
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

            # ---------- EXPLORE ----------
            elif action == "explore":

                agent.move(self.environment.size)
                reward += 0.5

            # ---------- SURVIVAL ----------
            agent.consume_food()

            if agent.alive:
                reward += 1
            else:
                reward -= 10

            # ---------- RL UPDATE ----------
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

        # Agents
        self.ax.scatter(xs, ys, c=colors)

        # Workplaces
        wx = [x for x, y in self.environment.work_locations]
        wy = [y for x, y in self.environment.work_locations]

        self.ax.scatter(wx, wy, marker="s", color="black", s=120, label="Work")

        # Markets
        mx = [x for x, y in self.environment.market_locations]
        my = [y for x, y in self.environment.market_locations]

        self.ax.scatter(mx, my, marker="^", color="blue", s=140, label="Market")

        # Housing
        hx = [x for x, y in self.environment.housing_locations]
        hy = [y for x, y in self.environment.housing_locations]

        self.ax.scatter(hx, hy, marker="D", color="purple", s=120, label="Housing")

        self.ax.set_title(
            f"Agentopolis | Step {step} | Food Price: {self.market.food_price}"
        )

        self.ax.set_xlim(0, self.environment.size)
        self.ax.set_ylim(0, self.environment.size)

        self.ax.legend()
        self.ax.grid(True)

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

            print(
                f"Step {step} | Alive: {alive_agents} | Food Price: {self.market.food_price}"
            )

            time.sleep(0.05)

        # After simulation finishes
        self.plot_learning()

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

    def plot_learning(self):

        print("Plotting learning graph...")

        # Disable interactive mode so chart appears
        plt.ioff()

        actions = ["work", "buy_food", "explore"]

        counts = [
            len(self.action_history["work"]),
            len(self.action_history["buy_food"]),
            len(self.action_history["explore"])
        ]

        plt.figure()
        plt.bar(actions, counts)

        plt.title("Agent Action Preferences (Learning)")
        plt.xlabel("Action")
        plt.ylabel("Frequency")

        plt.show()