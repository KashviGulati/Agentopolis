from flask import Flask, jsonify
from flask_cors import CORS
from simulation.simulation_engine import Simulation

app = Flask(__name__)
CORS(app)

sim = Simulation(num_agents=40)

@app.route("/step")
def step():
    sim.step()
    sim.market.update_price()

    agents_data = []

    for a in sim.agents:
        if a.alive:
            agents_data.append({
                "x": a.x,
                "y": a.y,
                "money": a.money,
                "food": a.food,
                "action": a.current_action
            })

    return jsonify({
        "agents": agents_data,
        "price": sim.market.food_price
    })

if __name__ == "__main__":
    app.run(debug=True)