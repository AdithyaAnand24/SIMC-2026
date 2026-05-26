"""
SIMC Probability — Exercise 03: Bayes' Theorem (the classic disease-test problem)

Setup (the canonical Bayes "gotcha" — get this in your bones):
    A disease affects 1% of a population.
    A test has:
      - Sensitivity (true positive rate)  = 99%   (P(test+ | disease) = 0.99)
      - Specificity (true negative rate) = 99%   (P(test- | healthy) = 0.99)
    You test positive. What is P(disease | test+)?

Intuition says ~99%. Bayes says ~50%. The simulation will prove it to you.

Goal: Simulate 1,000,000 people, compute the empirical P(disease | test+),
and verify it matches the Bayes calculation:
    P(D | T+) = P(T+ | D) * P(D) / P(T+)

Concepts you should hit while writing this:
- Prior, likelihood, posterior
- Total probability: P(T+) = P(T+|D)P(D) + P(T+|H)P(H)
- Why low base rate makes specificity matter more than sensitivity

DO NOT USE AI FOR THE IMPLEMENTATION. Code it yourself.

Companion note: SIMC/Probability/bayes-theorem.md
"""

import numpy as np

N_PEOPLE = 1_000_000
P_DISEASE = 0.01      # prior — base rate
SENSITIVITY = 0.99    # P(test+ | disease)
SPECIFICITY = 0.99    # P(test- | healthy) — so P(test+ | healthy) = 0.01


def simulate_population(n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Generate two boolean arrays of length n:
      - has_disease[i] = True if person i has the disease
      - tested_positive[i] = True if person i's test came back positive

    Hint: rng.random(n) < threshold for Bernoulli draws.
    Hint: tested_positive depends on has_disease.
    """

    has_disease = rng.random(n) < P_DISEASE
    tested_positive = np.zeros(n, dtype=bool)
    for i in range(n):
        if has_disease[i]:
            tested_positive[i] = rng.random() < SENSITIVITY
        else:
            tested_positive[i] = rng.random() < (1 - SPECIFICITY)

    return (has_disease, tested_positive)



def empirical_posterior(has_disease: np.ndarray, tested_positive: np.ndarray) -> float:
    """Compute P(disease | test+) from the simulated data."""

    positive = 0
    true_positives = 0
    for i in range(len(has_disease)):
        if tested_positive[i]:
            positive += 1
            if has_disease[i]:
                true_positives += 1

    return true_positives / positive
     

def bayes_posterior(prior: float, sensitivity: float, specificity: float) -> float:
    """Closed-form Bayes calculation of P(D | T+)."""
  
    prob = sensitivity * prior / (sensitivity * prior + (1 - specificity) * (1 - prior))
    return prob

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    has_disease, tested_positive = simulate_population(N_PEOPLE, rng)

    p_empirical = empirical_posterior(has_disease, tested_positive)
    p_bayes = bayes_posterior(P_DISEASE, SENSITIVITY, SPECIFICITY)

    print(f"Empirical P(D | T+) over {N_PEOPLE:,} people = {p_empirical:.4f}")
    print(f"Bayes-theorem    P(D | T+)                  = {p_bayes:.4f}")
    print(f"Absolute error = {abs(p_empirical - p_bayes):.4f}")

    # Stretch: vary the prior P(D) from 0.001 to 0.5 and plot P(D | T+).
    # When does the test become "useful"?

    # Stretch: vary specificity from 0.90 to 0.999 and plot.
    # Notice how much more sensitive the posterior is to specificity than to sensitivity
    # when the base rate is low. THIS is the Bayes lesson.
