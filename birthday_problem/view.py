# birthday_problem/view.py

import streamlit as st
from .model import simulate_non_uniform_birthdays, generate_birthday_distribution


def create_birthday_chart(birthday_probs):
    values = [
        {"day": int(day), "probability": float(probability)}
        for day, probability in zip(range(1, 366), birthday_probs)
    ]
    return {
        "data": {"values": values},
        "mark": {"type": "bar", "tooltip": True},
        "encoding": {
            "x": {
                "field": "day",
                "type": "quantitative",
                "title": "Day of the Year",
            },
            "y": {
                "field": "probability",
                "type": "quantitative",
                "title": "Probability",
            },
        },
        "height": 300,
        "title": "Non-Uniform Birthday Distribution",
    }


def birthday_problem_app():
    st.title("🎂 Birthday Problem Simulator")
    st.markdown("""
    ## **About the Birthday Problem**

    The Birthday Problem asks:  
    **What is the probability that at least two people in a group share the same birthday?**

    While it seems unlikely, the math is surprising:
    - In a group of just **23 people**, there's over a **50% chance** that two share a birthday.
    - In a group of **50 people**, the chance rises to **97%**.

    This simulation is based on **real U.S. birth date probabilities from 2019** with 0 perturbation. You can adjust the perturbation level to see how it affects the distribution of birthdates and the probability of shared birthdays.

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
        st.vega_lite_chart(
            create_birthday_chart(birthday_probs), use_container_width=True
        )
