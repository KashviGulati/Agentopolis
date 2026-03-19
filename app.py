from flask import Flask, jsonify
from flask_cors import CORS
from simulation.simulation_engine import Simulation

engine = Simulation(num_agents=200)

app = Flask(__name__)
CORS(app)

sim = Simulation(num_agents=40)

@app.route("/step")
def step():

    engine.step()  # run one simulation step

    # filter alive agents
    alive_agents = [a for a in engine.agents if a.alive]

    return jsonify({
        "agents": [
            {
                "x": a.x,
                "y": a.y,
                "action": a.current_action
            } for a in alive_agents
        ],
        "price": engine.market.food_price,
        "alive": len(alive_agents),
        "wealth": [a.money for a in alive_agents]
    })

if __name__ == "__main__":
    app.run(debug=True)