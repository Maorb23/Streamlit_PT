# birthday_problem/model.py

import numpy as np

def simulate_non_uniform_birthdays(n_students, birthday_probs, n_simulations=5000):
    cumulative_probs = np.cumsum(birthday_probs)
    shared_count = 0

    for _ in range(n_simulations):
        birthdays = np.searchsorted(cumulative_probs, np.random.rand(n_students))
        if len(birthdays) != len(set(birthdays)):
            shared_count += 1

    return shared_count / n_simulations

def generate_birthday_distribution(perturbation):
    monthly_birth_rates = {
        'January': 0.079, 'February': 0.076, 'March': 0.081, 'April': 0.08,
        'May': 0.083, 'June': 0.081, 'July': 0.087, 'August': 0.089,
        'September': 0.09, 'October': 0.087, 'November': 0.083, 'December': 0.085
    }
    days_in_month = {
        'January': 31, 'February': 28, 'March': 31, 'April': 30,
        'May': 31, 'June': 30, 'July': 31, 'August': 31,
        'September': 30, 'October': 31, 'November': 30, 'December': 31
    }

    birthday_probs = []
    for month, rate in monthly_birth_rates.items():
        daily_rate = rate / days_in_month[month] * np.random.normal(1, perturbation)
        birthday_probs.extend([daily_rate] * days_in_month[month])

    birthday_probs = np.array(birthday_probs)
    return birthday_probs / birthday_probs.sum()
