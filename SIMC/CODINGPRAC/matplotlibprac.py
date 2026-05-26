import matplotlib.pyplot as plt
import numpy as np


xs = np.linspace(0, 2 * np.pi, 100)

fig, axs = plt.subplots(2, 1, figsize=(8, 5))   # 1 row, 2 columns
axs[0].plot(xs, np.sin(xs))
axs[0].set_title("sin(x)")
axs[1].plot(xs, np.cos(xs))
axs[1].set_title("cos(x)")
plt.tight_layout()   # auto-adjusts spacing so labels don't overlap
plt.show()
