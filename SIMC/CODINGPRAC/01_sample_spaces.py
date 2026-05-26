"""
SIMC Probability — Exercise 01: Sample Spaces, Events, Axioms

Goal: Simulate a fair die roll 10,000 times and empirically verify P(even) = 0.5.

Concepts you should hit while writing this:
- Sample space S = {1, 2, 3, 4, 5, 6}
- Event E (the "even outcomes" subset of S)
- Probability axiom: P(E) = |E| / |S| for equally likely outcomes
- Frequentist interpretation: empirical frequency converges to probability as n -> inf

DO NOT USE AI FOR THE IMPLEMENTATION. Code it yourself.
If you get stuck, write a doubt in Workflow/doubts-SIMC.md, not a prompt.

Companion note: SIMC/Probability/sample-spaces-events-axioms.md
"""

import numpy as np
import matplotlib.pyplot as plt



def simulate_die_rolls(n: int) -> np.ndarray:
    """Return an array of n fair die rolls (integers 1-6).

    Hint: np.random.randint or np.random.default_rng().integers
    """

    arr = np.random.randint(1, 7, size=n)
    return arr


def probability_of_event(rolls: np.ndarray, event_fn) -> float:
    """Empirical probability of an event, given an array of outcomes
    and a function `event_fn(outcome) -> bool` that returns True if
    the outcome belongs to the event.

    Hint: boolean masking + .mean()
    """
    arr = event_fn(rolls)
    p = arr.mean()
    return p

def is_even(x: int) -> bool:
    
    return x % 2 == 0



if __name__ == "__main__":

    N_ROLLS = 10
    rolls1 = simulate_die_rolls(N_ROLLS)
    p_even = probability_of_event(rolls1, is_even)
    print(f"Empirical P(even) over {N_ROLLS:,} rolls = {p_even:.4f}")
    print(f"Theoretical P(even) = 0.5")
    print(f"Absolute error = {abs(p_even - 0.5):.4f}")


    # Stretch: vary N from 10 to 100_000 (log-spaced) and plot

    

    #DONE 

    # |empirical - 0.5| vs N to visualize the law of large numbers.
    N_values = np.logspace(1, 5, num=20, dtype=int)
    errors = np.array([])

    for N in N_values:
        rolls = simulate_die_rolls(N)
        p_even = probability_of_event(rolls, is_even)
        error = abs(p_even - 0.5)
        errors = np.append(errors, error)

    print(N_values)
    print(errors)
    

    fig , ax = plt.subplots()
    ax.plot(N_values, errors , marker='o')
    ax.set_xscale('log')
    ax.set_xlabel('Number of Rolls (log scale)')
    ax.set_ylabel('Absolute Error')
    ax.set_title('Convergence of Empirical P(even) to 0.5')
    ax.grid(True)
    plt.show()
