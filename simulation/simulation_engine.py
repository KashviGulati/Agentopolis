from simulation.environment import Environment
from simulation.agent import Agent
from simulation.market import Market


class Simulation:

    def __init__(self, num_agents=100):

        self.environment = Environment()
        self.market = Market()

        self.agents = []

        for i in range(num_agents):
            self.agents.append(Agent(i, self.environment.size))

    def step(self):

        for agent in self.agents:

            if not agent.alive:
                continue

            # movement
            agent.move(self.environment.size)

            pos = agent.position()

            # WORK if near workplace
            if self.environment.near_work_location(pos):
                agent.money += 5

            # BUY FOOD if hungry
            if agent.food < 3:
                self.market.buy_food(agent)

            # CONSUME FOOD
            agent.consume_food()

    def run(self, steps=100):

        for step in range(steps):

            self.step()

            alive_agents = sum(agent.alive for agent in self.agents)

            print(f"Step {step} | Alive agents: {alive_agents}")