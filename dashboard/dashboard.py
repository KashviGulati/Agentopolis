import sys
import os

# Allow Streamlit to access project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from simulation.simulation_engine import Simulation


def gini(values):
    values = np.array(values)

    if len(values) == 0:
        return 0

    values = np.sort(values)
    n = len(values)

    cumulative = np.cumsum(values)

    gini_coeff = (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n

    return gini_coeff


st.title("Agentopolis Economic Simulation")
st.write("Simulating a multi-agent economic system with dynamic markets.")

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

    gini_values = [gini(w) for w in sim.wealth_history]

    df_gini = pd.DataFrame({
        "Step": list(range(len(gini_values))),
        "Gini": gini_values
    })

    st.subheader("Wealth Inequality (Gini Index)")
    fig3 = px.line(df_gini, x="Step", y="Gini")
    st.plotly_chart(fig3)