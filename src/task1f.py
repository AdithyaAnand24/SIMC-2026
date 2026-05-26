"""SIMCC 2026 -- Task 1f: Numerical validation of parts (d) and (e).

This file is structured as two Colab cells, each delimited by a `# %%` marker
and a banner. Copy each cell into its own Colab cell and run them in order.

Cell 1 (Validation):  builds the Markov matrix, simulates the recursion,
                      computes the closed form from the eigenmode decomposition,
                      and asserts they agree to machine precision.
Cell 2 (Plotting):    produces the 2-panel figure for the report.  Depends on
                      `t`, `P_num`, `P_closed`, and `eps` defined in Cell 1.
"""

# =============================================================================
# %% Cell 1 -- Validation
# -----------------------------------------------------------------------------
# Task 1f -- Numerical validation of the closed-form expression from 1d,
# and of the asymptotic limit P(t) -> nu_1 from 1e.
#
# Strategy: simulate P(t) directly via the recursion, compute it independently
# from the eigenmode decomposition, and assert the two agree to machine
# precision.  If 1d is wrong, this cell will fail loudly.
# =============================================================================

import numpy as np

# --- Parameters --------------------------------------------------------------
eps = 0.1                                 # conversion rate per generation
p0  = np.array([0.5, 0.5])                # initial state (p2 = 1 - p1 by conservation)
T   = 100                                 # number of generations to simulate

# Markov matrix M; lower-triangular, column-stochastic.
M = np.array([[1 - eps, 0.0],
              [eps,     1.0]])

# --- Stage 1: direct simulation ---------------------------------------------
# P_num[t] is P(t) computed by iterating the recursion.  No analytical input.
P_num = np.zeros((T + 1, 2))
P_num[0] = p0
for t_step in range(T):
    P_num[t_step + 1] = M @ P_num[t_step]

# --- Stage 2: closed-form via eigenmode decomposition -----------------------
# Eigenvectors of M (derived by hand in 1b; lambda_1 = 1, lambda_2 = 1 - eps).
v1 = np.array([0,  1])                    # persistent mode  (lambda_1 = 1)
v2 = np.array([1, -1])                    # decaying mode    (lambda_2 = 1 - eps)

# Solve P(0) = c1*v1 + c2*v2 for the coefficients in the eigenbasis.
c1, c2 = np.linalg.solve(np.column_stack([v1, v2]), p0)
print(f"c1 = {c1},  c2 = {c2}")           # expect c1 = 1, c2 = 0.5

# Evaluate the closed form for all t at once via broadcasting.
# Shape: (T+1, 1) * (2,) broadcasts to (T+1, 2).
t = np.arange(T + 1)
P_closed = c1 * v1 + c2 * ((1 - eps) ** t)[:, None] * v2

# --- Stage 3: validation ----------------------------------------------------
# Both arrays should agree to machine precision; the assertion guards against
# anyone later breaking the math or the parameters.
max_err = np.max(np.abs(P_num - P_closed))
print(f"max |numeric - closed form| = {max_err:.2e}")
assert max_err < 1e-10, "closed form disagrees with simulation -- check 1d"

# Asymptotic check (validates 1e): P(T) should sit near [0, 1] = nu_1.
print(f"P(T={T}) = {P_num[-1]}   (should approach [0, 1])")


# =============================================================================
# %% Cell 2 -- Plotting
# -----------------------------------------------------------------------------
# Task 1f -- Visualisation of the validated trajectory.
#
# Two-panel figure for the report:
#   Panel A (linear): trajectories p_1(t), p_2(t) converging to (0, 1).
#                     Visual validation of 1e.
#   Panel B (log):    numeric p_1(t) overlaid on closed form (1/2)(1-eps)^t.
#                     A straight line on semilog-y proves the decay is
#                     geometric with rate (1 - eps); dots on the line prove
#                     1d's closed form is correct.
#
# Depends on: t, P_num, P_closed, eps   (defined in Cell 1)
# =============================================================================

import matplotlib.pyplot as plt

# Match the competition's serif typesetting.
plt.rcParams.update({"font.family": "serif", "font.size": 11})

fig, axes = plt.subplots(1, 2, figsize=(11, 4))

# --- Panel A: linear-scale trajectories -------------------------------------
# Dotted horizontal lines mark the asymptotic values, making the limit
# in 1e visible at a glance.
ax = axes[0]
ax.plot(t, P_num[:, 0], "o-", color="tab:blue",   ms=3, lw=1,
        label=r"$p_1(t)$ (type 1)")
ax.plot(t, P_num[:, 1], "o-", color="tab:orange", ms=3, lw=1,
        label=r"$p_2(t)$ (type 2)")
ax.axhline(0, color="tab:blue",   ls=":", lw=1, alpha=0.6)
ax.axhline(1, color="tab:orange", ls=":", lw=1, alpha=0.6)
ax.set_xlabel(r"generation $t$")
ax.set_ylabel("fractional population")
ax.set_title(rf"Population trajectories ($\epsilon = {eps}$)")
ax.set_ylim(-0.02, 1.05)
ax.legend(loc="center right")
ax.grid(alpha=0.3)

# --- Panel B: log-scale decay of p_1, numeric vs closed form ----------------
# theory_p1 is the closed form for component 1 only:
#   p_1(t) = c_2 * (1-eps)^t * v2[0]  =  (1/2)(1-eps)^t.
# On a log y-axis this is a perfect straight line; numeric dots lying on top
# of it constitute the validation of 1d.
theory_p1 = 0.5 * (1 - eps) ** t

ax = axes[1]
ax.semilogy(t, theory_p1,    "-",  color="black",    lw=1.2,
            label=r"theory: $\frac{1}{2}(1-\epsilon)^t$")
ax.semilogy(t, P_num[:, 0], "o",   color="tab:blue", ms=4,
            label=r"numeric $p_1(t)$")
ax.set_xlabel(r"generation $t$")
ax.set_ylabel(r"$p_1(t)$  (log scale)")
ax.set_title("Geometric decay of type-1: numeric vs closed form")
ax.legend()
ax.grid(which="both", alpha=0.3)

fig.tight_layout()
fig.savefig("task1f_trajectories.png", dpi=150, bbox_inches="tight")
plt.show()
