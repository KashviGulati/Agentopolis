import sys
import os
import time
import requests
import streamlit as st
import pandas as pd
import numpy as np

# Allow imports (if needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ===============================
# GINI FUNCTION
# ===============================

def gini(values):
    values = np.array(values)

    if len(values) == 0:
        return 0

    values = np.sort(values)
    n = len(values)
    cumulative = np.cumsum(values)

    return (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n


# ===============================
# UI HEADER
# ===============================

st.set_page_config(layout="wide")
st.title("🏙️ Agentopolis Economic Simulation")

st.markdown("### 🔴 LIVE Simulation Running")


# ===============================
# DATA STORAGE
# ===============================

price_data = []
population_data = []
gini_data = []

placeholder = st.empty()


# ===============================
# START BUTTON
# ===============================

run = st.button("Start Live Simulation")


# ===============================
# LIVE LOOP
# ===============================

if run:

    while True:
        try:
            res = requests.get("http://127.0.0.1:5000/step")
            data = res.json()

            population = data["alive"]
            price = data["price"]
            wealth = data["wealth"]

            gini_val = gini(wealth)

            population_data.append(population)
            price_data.append(price)
            gini_data.append(gini_val)

            df = pd.DataFrame({
                "Population": population_data,
                "Price": price_data,
                "Gini": gini_data
            })

            with placeholder.container():

                # ===============================
                # METRICS
                # ===============================
                col1, col2, col3 = st.columns(3)

                col1.metric("👥 Population", population)
                col2.metric("💰 Food Price", price)
                col3.metric("⚖️ Gini Index", round(gini_val, 3))

                st.divider()

                # ===============================
                # STATUS / INSIGHT
                # ===============================
                if gini_val > 0.5:
                    st.error("⚠️ High inequality detected — economy unstable")
                elif gini_val > 0.3:
                    st.warning("⚠️ Moderate inequality — monitor system")
                else:
                    st.success("✅ Balanced economy")

                st.divider()

                # ===============================
                # CHARTS
                # ===============================
                st.subheader("📈 Population Dynamics")
                st.line_chart(df["Population"])

                st.subheader("💹 Market Behavior")
                st.line_chart(df["Price"])

                st.subheader("⚖️ Inequality Over Time")
                st.line_chart(df["Gini"])

                st.subheader("💰 Economic Distribution")
                st.bar_chart(wealth)

            time.sleep(1)

        except Exception as e:
            st.error(f"Error: {e}")
            break