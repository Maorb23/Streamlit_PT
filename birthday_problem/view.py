# birthday_problem/view.py

import streamlit as st
import numpy as np
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from .model import simulate_non_uniform_birthdays, generate_birthday_distribution

def create_bokeh_plot(birthday_probs):
    days = np.arange(1, 366)
    source = ColumnDataSource(data=dict(x=days, y=birthday_probs))
    p = figure(title="Non-Uniform Birthday Distribution", x_axis_label='Day of the Year', y_axis_label='Probability', height=300, sizing_mode='stretch_width')
    p.vbar(x='x', top='y', width=1, source=source)
    return p

def birthday_problem_app():
    st.title("🎂 Birthday Problem Simulator")
    st.markdown("""
    ## **About the Birthday Problem**

    The Birthday Problem asks:  
    **What is the probability that at least two people in a group share the same birthday?**

    While it seems unlikely, the math is surprising:
    - In a group of just **23 people**, there's over a **50% chance** that two share a birthday.
    - In a group of **50 people**, the chance rises to **97%**.

    This simulation Uses **realistic birth dates probabilities in the US from 2019** with 0 perturbation. You can adjust the perturbation level to see how it affects the distribution of birthdays and the probability of shared birthdays.

    Use the sliders below to explore your own scenarios!
    """)

    with st.form("birthday_sim_form"):
        n_students = st.slider("Number of Students", 2, 100, 23)
        perturbation = st.slider("Perturbation Level", 0.0, 0.5, 0.1)
        submit = st.form_submit_button("Run Simulation")

    if submit:
        birthday_probs = generate_birthday_distribution(perturbation)
        prob_shared = simulate_non_uniform_birthdays(n_students, birthday_probs)

        st.success(f"📊 Probability of shared birthday: **{prob_shared:.3f}**")
        st.bokeh_chart(create_bokeh_plot(birthday_probs), use_container_width=True)
