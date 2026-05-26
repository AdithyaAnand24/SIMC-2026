import matplotlib.pyplot as plt
import numpy as np
import random as random

# Setup: You're on a game show. Behind one of three doors is a car; behind the other two, goats. You pick a door (say door 1). The host (who knows where the car is) opens one of the other two doors that has a goat behind it. He then offers you the choice: stay with door 1, or switch to the remaining unopened door.

# Question: should you stay or switch? Most people's intuition says "doesn't matter, 50/50." It's not 50/50.

# What to simulate:

# 10,000 trials
# For each trial:
# Place car behind a random door (1, 2, or 3)
# Player picks a random door
# Host opens a goat door (one of the doors that isn't the player's pick AND isn't the car)
# Compute win probability for two strategies: "always stay" vs "always switch"
# Plot the two win rates as a bar chart

NumTrials = 10_000

switch_wins = 0
stay_wins = 0
for i in range(NumTrials):
    
    # initializing the doors
    door = np.zeros(3)
    r = random.randint(0, 2)
    door[r] = 1

    # player picks a random door
    player = random.randint(0, 2)
    
    # host opens a goat door
    for i in range(3):
        if door[i] == 0 and i != player:
            door[i] = -1
            break

    # if player no switch
    if door[player] == 1:
        stay_wins += 1
    else:
        switch_wins += 1

print(f"Switch wins: {switch_wins / NumTrials:.2%}")
print(f"Stay wins: {stay_wins / NumTrials:.2%}")

fig, ax = plt.subplots()
ax.bar(['Stay', 'Switch'], [stay_wins/NumTrials, switch_wins/NumTrials], color=['red', 'blue'])
ax.set_ylabel('Win rate')
ax.set_title('Monty Hall: Stay vs Switch (10,000 trials)')
ax.axhline(1/3, color='gray', linestyle='--', alpha=0.5)
ax.axhline(2/3, color='gray', linestyle='--', alpha=0.5)
plt.show()
