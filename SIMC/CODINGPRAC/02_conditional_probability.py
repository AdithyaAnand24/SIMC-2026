"""
SIMC Probability — Exercise 02: Conditional Probability

Goal: Simulate drawing 2 cards (without replacement) from a standard 52-card deck.
Empirically verify:
    P(2nd card is an ace | 1st card is an ace) = 3 / 51

Concepts you should hit while writing this:
- Conditional probability: P(A | B) = P(A and B) / P(B)
- Sampling without replacement (state changes the sample space)
- Restriction: condition by FILTERING simulated trials (only count trials
  where the condition holds), then compute frequency of A within those.

DO NOT USE AI FOR THE IMPLEMENTATION. Code it yourself.

Companion note: SIMC/Probability/conditional-probability.md
"""

import numpy as np

N_TRIALS = 10000

# A deck: 52 cards. Aces are cards 0..3 (or pick any 4 indices — doesn't matter).
DECK_SIZE = 52
ACES = {0, 1, 2, 3}


def draw_two_cards(rng: np.random.Generator) -> tuple[int, int]:
    """Draw 2 distinct cards from a 52-card deck without replacement.

    Hint: rng.choice with replace=False, size=2
    """
    cards = np.arange(0, DECK_SIZE)
    draws = rng.choice(cards , replace=False , size=2)
    return tuple(draws)


def is_ace(card: int) -> bool:
    return card in ACES


def simulate(n_trials: int) -> float:
    """Run n_trials and return empirical P(2nd is ace | 1st is ace).

    Strategy:
      1. Run all n_trials.
      2. Filter to trials where the 1st card is an ace.
      3. Among THOSE, compute fraction where the 2nd is also an ace.
    """

    count_1st_ace = 0
    count_both_aces = 0
    for i in range(n_trials):


        draw = draw_two_cards(rng)
        if is_ace(draw[0]):
            count_1st_ace += 1
            if is_ace(draw[1]):
                count_both_aces += 1
    return count_both_aces / count_1st_ace if count_1st_ace > 0 else 0

def simulatejoint(n_trials: int) -> float:
    
    trials = 0
    for i in range(n_trials):


        draw = draw_two_cards(rng)
        if is_ace(draw[0]):
            if is_ace(draw[1]):
                trials += 1
    return trials / n_trials

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    p_empirical = simulate(N_TRIALS)
    p_theoretical = 3 / 51

    p_empirical_joint = simulatejoint(N_TRIALS)
    p_theoretical_joint = (4/52) * (3/51)


    print(f"Empirical P(2nd ace | 1st ace) over {N_TRIALS:,} trials = {p_empirical:.4f}")
    print(f"Theoretical P(2nd ace | 1st ace) = 3/51 = {p_theoretical:.4f}")
    print(f"Absolute error = {abs(p_empirical - p_theoretical):.4f}")

    print(f"Empirical P(2nd ace and 1st ace) over {N_TRIALS:,} trials = {p_empirical_joint:.4f}")
    print(f"Theoretical P(2nd ace and 1st ace) = (4/52) * (3/51) = {p_theoretical_joint:.4f}")

    # Stretch: Also compute P(2nd is ace) WITHOUT conditioning.
    # Is it the same? Different? Why?
