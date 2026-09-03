import streamlit as st
import numpy as np


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
    values = [
        {
            "strategy": "Stay",
            "win_rate": float(stay_wins / n_simulations * 100),
        },
        {
            "strategy": "Switch",
            "win_rate": float(switch_wins / n_simulations * 100),
        },
    ]
    return {
        "data": {"values": values},
        "mark": {"type": "bar", "tooltip": True},
        "encoding": {
            "x": {
                "field": "strategy",
                "type": "nominal",
                "title": "Strategy",
                "sort": ["Stay", "Switch"],
            },
            "y": {
                "field": "win_rate",
                "type": "quantitative",
                "title": "Win Rate (%)",
                "scale": {"domain": [0, 100]},
            },
            "color": {
                "field": "strategy",
                "type": "nominal",
                "scale": {
                    "domain": ["Stay", "Switch"],
                    "range": ["#df1a1a", "#108a22"],
                },
                "legend": None,
            },
        },
        "height": 350,
        "title": "Win Rates by Strategy (%)",
    }


def create_monty_ci_plot(n_simulations, step=50, bootstrap_rounds=200):
    iterations = np.arange(step, n_simulations + 1, step)
    stay_rates = []
    switch_rates = []
    stay_ci = []
    switch_ci = []

    for n in iterations:
        wins = np.random.randint(0, 3, size=(bootstrap_rounds, n))
        choices = np.random.randint(0, 3, size=(bootstrap_rounds, n))

        stay_win_matrix = wins == choices
        switch_win_matrix = wins != choices

        stay_mean = stay_win_matrix.mean(axis=1)
        switch_mean = switch_win_matrix.mean(axis=1)

        stay_rates.append(stay_mean.mean() * 100)
        switch_rates.append(switch_mean.mean() * 100)
        stay_ci.append(np.percentile(stay_mean, [2.5, 97.5]) * 100)
        switch_ci.append(np.percentile(switch_mean, [2.5, 97.5]) * 100)

    # Unpack CIs
    stay_lower, stay_upper = zip(*stay_ci)
    switch_lower, switch_upper = zip(*switch_ci)

    values = []
    for strategy, rates, lower, upper in (
        ("Stay", stay_rates, stay_lower, stay_upper),
        ("Switch", switch_rates, switch_lower, switch_upper),
    ):
        values.extend(
            {
                "iterations": int(iteration),
                "win_rate": float(rate),
                "lower": float(low),
                "upper": float(high),
                "strategy": strategy,
            }
            for iteration, rate, low, high in zip(iterations, rates, lower, upper)
        )

    color = {
        "field": "strategy",
        "type": "nominal",
        "scale": {
            "domain": ["Stay", "Switch"],
            "range": ["#df1a1a", "#108a22"],
        },
        "title": "Strategy",
    }
    return {
        "data": {"values": values},
        "layer": [
            {
                "mark": {"type": "area", "opacity": 0.2},
                "encoding": {
                    "x": {
                        "field": "iterations",
                        "type": "quantitative",
                        "title": "Number of Simulations",
                    },
                    "y": {
                        "field": "lower",
                        "type": "quantitative",
                        "title": "Win Rate (%)",
                        "scale": {"domain": [0, 100]},
                    },
                    "y2": {"field": "upper"},
                    "color": color,
                },
            },
            {
                "mark": {"type": "line", "strokeWidth": 2},
                "encoding": {
                    "x": {"field": "iterations", "type": "quantitative"},
                    "y": {"field": "win_rate", "type": "quantitative"},
                    "color": color,
                    "tooltip": [
                        {"field": "strategy", "type": "nominal"},
                        {"field": "iterations", "type": "quantitative"},
                        {
                            "field": "win_rate",
                            "type": "quantitative",
                            "format": ".2f",
                        },
                    ],
                },
            },
        ],
        "height": 400,
        "title": "Win Rate with Bootstrap CI over Iterations",
    }


def monty_hall_app():
    st.subheader("🚪 Monty Hall Problem Simulator")

    st.markdown("""
    The **Monty Hall problem** is a classic probability puzzle:  
    You're on a game show with 3 doors. Behind one is a prize.  
    You choose a door, then the host (who knows what's behind the doors) opens a different one to show a goat.  
    You now have the option to **stick** with your original choice or **switch**.

    What should you do?

    Use the slider below to run simulations and see which strategy works better.
    
    **EXTRA:** Check the "Explore More" option to explore the win rates distribution over iterations.           
    """)

    with st.form("monty_form"):
        n_simulations = st.slider("Number of Simulations", min_value=100, max_value=100_000, value=1000, step=100)
        explore_more = st.checkbox("📊 Explore More (CI over iterations)")
        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        stay_wins, switch_wins = simulate_monty_hall(n_simulations)
        fig = create_monty_plot(stay_wins, switch_wins, n_simulations)
        st.vega_lite_chart(fig, use_container_width=True)

        st.markdown(f"""
        - **Stay Strategy** win rate: `{stay_wins / n_simulations:.2%}`
        - **Switch Strategy** win rate: `{switch_wins / n_simulations:.2%}`
        """)

        if explore_more:
            ci_fig = create_monty_ci_plot(n_simulations)
            st.vega_lite_chart(ci_fig, use_container_width=True)
