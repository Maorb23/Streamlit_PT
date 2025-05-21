import streamlit as st
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

def simulate_monty_hall(n_simulations=1000):
    # Randomly assign winning doors
    winning_doors = np.random.randint(0, 3, size=n_simulations)
    initial_choices = np.random.randint(0, 3, size=n_simulations)

    # If you stay, you win if your first pick was the winning door
    stay_wins = (initial_choices == winning_doors).sum()

    # If you switch, you win if you did NOT initially pick the winning door
    switch_wins = n_simulations - stay_wins

    return stay_wins, switch_wins

def create_monty_plot(stay_wins, switch_wins, n_simulations):
    categories = ["Stay", "Switch"]
    counts = [stay_wins / n_simulations * 100, switch_wins / n_simulations * 100]

    source = ColumnDataSource(data=dict(strategies=categories, win_rates=counts))

    p = figure(x_range=categories, height=350, title="Win Rates by Strategy (%)",
               toolbar_location=None, tools="", sizing_mode="stretch_width")
    p.vbar(x='strategies', top='win_rates', width=0.5, source=source, color=["#a9a9a9", "#66c2a5"])

    p.y_range.start = 0
    p.y_range.end = 100
    p.yaxis.axis_label = "Win Rate (%)"
    p.xaxis.axis_label = "Strategy"
    p.title.align = "center"
    p.title.text_font_size = "16pt"

    return p

def monty_hall_app():
    st.subheader("🚪 Monty Hall Problem Simulator")

    st.markdown("""
    The **Monty Hall problem** is a classic probability puzzle:  
    You're on a game show with 3 doors. Behind one is a prize.  
    You choose a door, then the host (who knows what's behind the doors) opens a different one to show a goat.  
    You now have the option to **stick** with your original choice or **switch**.

    What should you do?

    Use the slider below to run simulations and see which strategy works better.
    """)

    with st.form("monty_form"):
        n_simulations = st.slider("Number of Simulations", min_value=100, max_value=100_000, value=1000, step=100)
        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        stay_wins, switch_wins = simulate_monty_hall(n_simulations)
        fig = create_monty_plot(stay_wins, switch_wins, n_simulations)

        st.bokeh_chart(fig, use_container_width=True)

        st.markdown(f"""
        - **Stay Strategy** win rate: `{stay_wins / n_simulations:.2%}`
        - **Switch Strategy** win rate: `{switch_wins / n_simulations:.2%}`
        """)
