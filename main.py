from simulation.simulation_engine import Simulation

def main():

    sim = Simulation(num_agents=200)

    sim.run(steps=100)


if __name__ == "__main__":
    main()