import matplotlib.pyplot as plt
import numpy as np

# 1. Coin flip streaks — Flip 1,000 fair coins.
# Top row:    longest run of consecutive SAME-side | longest ALTERNATING run
# Bottom row: distribution of number of heads     | distribution of number of tails
# Repeat 10,000 times; histogram everything.

NumTrials = 10_000
NumFlips = 1_000

maxstreaksh = []
maxstreakst = []
maxstreaksalt = []
num_heads = []
num_tails = []

rng = np.random.default_rng(41)

for i in range(NumTrials):
    flips = rng.random(NumFlips) < 0.5

    # --- Longest consecutive-SAME streaks (heads and tails) ---
    streakh = 0
    streakt = 0
    maxstreakh = 0
    maxstreakt = 0

    for flip in flips:
        if flip:  # heads
            streakt = 0
            streakh += 1
            if streakh > maxstreakh:
                maxstreakh = streakh
        else:     # tails
            streakh = 0
            streakt += 1
            if streakt > maxstreakt:
                maxstreakt = streakt

    maxstreaksh.append(maxstreakh)
    maxstreakst.append(maxstreakt)

    # --- Longest ALTERNATING streak ---
    streakalt = 1
    maxstreakalt = 1
    for k in range(1, len(flips)):
        if flips[k] != flips[k - 1]:
            streakalt += 1
            if streakalt > maxstreakalt:
                maxstreakalt = streakalt
        else:
            streakalt = 1

    maxstreaksalt.append(maxstreakalt)

    # --- Number of heads / tails (one-shot per trial — boolean sums) ---
    h_count = int(flips.sum())                # True == 1
    num_heads.append(h_count)
    num_tails.append(NumFlips - h_count)


fig, axs = plt.subplots(2, 2, figsize=(13, 9))

# Top-left: longest consecutive-same streaks
axs[0, 0].hist(maxstreaksh, bins="auto", color='blue', alpha=0.5,
               label='Heads', edgecolor='black')
axs[0, 0].hist(maxstreakst, bins="auto", color='red', alpha=0.5,
               label='Tails', edgecolor='black')
axs[0, 0].set_xlabel('Longest consecutive-same streak')
axs[0, 0].set_ylabel('Frequency')
axs[0, 0].set_title('Longest run of same-side flips')
axs[0, 0].legend()

# Top-right: longest alternating streak
axs[0, 1].hist(maxstreaksalt, bins="auto", color='purple', alpha=0.6,
               label='Alternating (HTHT...)', edgecolor='black')
axs[0, 1].set_xlabel('Longest alternating streak')
axs[0, 1].set_ylabel('Frequency')
axs[0, 1].set_title('Longest alternating run')
axs[0, 1].legend()

# Bottom-left: number of heads per trial — symmetric bell around 500 (CLT)
# Bin width 2 keeps the histogram smooth (data spans ~430-570)
bins_count = np.arange(420.5, 580.5, 2)
axs[1, 0].hist(num_heads, bins='auto', color='blue', alpha=0.6, edgecolor='black')
axs[1, 0].axvline(500, color='black', linestyle='--', linewidth=1, label='Expected = 500')
axs[1, 0].set_xlabel('Number of heads in 1000 flips')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].set_title('Distribution of heads-count per trial')
axs[1, 0].legend()

# Bottom-right: number of tails per trial — mirror of heads-count by construction
axs[1, 1].hist(num_tails, bins='auto', color='red', alpha=0.6, edgecolor='black')
axs[1, 1].axvline(500, color='black', linestyle='--', linewidth=1, label='Expected = 500')
axs[1, 1].set_xlabel('Number of tails in 1000 flips')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].set_title('Distribution of tails-count per trial')
axs[1, 1].legend()

plt.tight_layout()
plt.show()

print(f"Mean longest heads-streak       = {np.mean(maxstreaksh):.2f}")
print(f"Mean longest tails-streak       = {np.mean(maxstreakst):.2f}")
print(f"Mean longest alternating-streak = {np.mean(maxstreaksalt):.2f}")
print(f"Theoretical longest run        ≈ log2(1000) ≈ {np.log2(1000):.2f}")
print()
print(f"Mean number of heads per trial = {np.mean(num_heads):.2f}   (expected 500)")
print(f"Std  number of heads per trial = {np.std(num_heads):.2f}    (expected sqrt(250) ≈ {np.sqrt(250):.2f})")
print(f"Mean number of tails per trial = {np.mean(num_tails):.2f}   (expected 500)")
