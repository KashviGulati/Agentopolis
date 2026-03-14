import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
import plotly.express as px

from simulation.simulation_engine import Simulation


st.title("Agentopolis Economic Simulation")

steps = st.slider("Simulation Steps", 50, 500, 200)

if st.button("Run Simulation"):

    sim = Simulation(num_agents=200)
    sim.run(steps)

    df = pd.DataFrame({
        "Step": list(range(len(sim.population_history))),
        "Population": sim.population_history,
        "Food Price": sim.price_history
    })

    st.subheader("Population Over Time")
    fig1 = px.line(df, x="Step", y="Population")
    st.plotly_chart(fig1)

    st.subheader("Food Price Over Time")
    fig2 = px.line(df, x="Step", y="Food Price")
    st.plotly_chart(fig2)