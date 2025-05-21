import streamlit as st
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import Band

from bokeh.models import Band, ColumnDataSource
from bokeh.plotting import figure

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
    win_rates = [stay_wins / n_simulations * 100, switch_wins / n_simulations * 100]
    colors = ["#df1a1a", "#108a22"]

    source = ColumnDataSource(data=dict(
        strategies=categories,
        win_rates=win_rates,
        fill_color=colors  # Add color here
    ))

    p = figure(x_range=categories, height=350, title="Win Rates by Strategy (%)",
               toolbar_location=None, tools="", sizing_mode="stretch_width")

    p.vbar(x='strategies', top='win_rates', width=0.5, source=source, fill_color='fill_color')

    p.y_range.start = 0
    p.y_range.end = 100
    p.yaxis.axis_label = "Win Rate (%)"
    p.xaxis.axis_label = "Strategy"
    p.title.align = "center"
    p.title.text_font_size = "16pt"

    return p


def create_monty_ci_plot(n_simulations, step=50, bootstrap_rounds=200):
    iterations = np.arange(step, n_simulations + 1, step)
    stay_rates = []
    switch_rates = []
    stay_ci = []
    switch_ci = []

    for n in iterations:
        wins = np.random.randint(0, 3, size=(bootstrap_rounds, n))
        choices = np.random.randint(0, 3, size=(bootstrap_rounds, n))

        stay_win_matrix = (wins == choices)
        switch_win_matrix = (wins != choices)

        stay_mean = stay_win_matrix.mean(axis=1)
        switch_mean = switch_win_matrix.mean(axis=1)

        stay_rates.append(stay_mean.mean() * 100)
        switch_rates.append(switch_mean.mean() * 100)
        stay_ci.append(np.percentile(stay_mean, [2.5, 97.5]) * 100)
        switch_ci.append(np.percentile(switch_mean, [2.5, 97.5]) * 100)

    # Unpack CIs
    stay_lower, stay_upper = zip(*stay_ci)
    switch_lower, switch_upper = zip(*switch_ci)

    # Create ColumnDataSources
    stay_src = ColumnDataSource(data=dict(
        x=iterations,
        y=stay_rates,
        lower=stay_lower,
        upper=stay_upper
    ))

    switch_src = ColumnDataSource(data=dict(
        x=iterations,
        y=switch_rates,
        lower=switch_lower,
        upper=switch_upper
    ))

    p = figure(
        title="Win Rate with Bootstrap CI over Iterations",
        x_axis_label="Number of Simulations",
        y_axis_label="Win Rate (%)",
        height=400,
        sizing_mode="stretch_width"
    )

    # Stay strategy line and CI band
    p.line('x', 'y', source=stay_src, color="#fb0c0c", legend_label="Stay", line_width=2)
    band1 = Band(base='x', lower='lower', upper='upper', source=stay_src,
                 level='underlay', fill_alpha=0.2, line_width=0, fill_color="#930909")
    p.add_layout(band1)

    # Switch strategy line and CI band
    p.line('x', 'y', source=switch_src, color="#03e707", legend_label="Switch", line_width=2)
    band2 = Band(base='x', lower='lower', upper='upper', source=switch_src,
                 level='underlay', fill_alpha=0.2, line_width=0, fill_color="#09df22")
    p.add_layout(band2)

    p.legend.location = "bottom_right"
    p.y_range.start = 0
    p.y_range.end = 100
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
    
    **EXTRA:** Check the "Explore More" option to explore the win rates distribution over iterations.           
    """)

    with st.form("monty_form"):
        n_simulations = st.slider("Number of Simulations", min_value=100, max_value=100_000, value=1000, step=100)
        explore_more = st.checkbox("📊 Explore More (CI over iterations)")
        submitted = st.form_submit_button("Run Simulation")

    if submitted:
        stay_wins, switch_wins = simulate_monty_hall(n_simulations)
        fig = create_monty_plot(stay_wins, switch_wins, n_simulations)
        st.bokeh_chart(fig, use_container_width=True)

        st.markdown(f"""
        - **Stay Strategy** win rate: `{stay_wins / n_simulations:.2%}`
        - **Switch Strategy** win rate: `{switch_wins / n_simulations:.2%}`
        """)

        if explore_more:
            ci_fig = create_monty_ci_plot(n_simulations)
            st.bokeh_chart(ci_fig, use_container_width=True)

