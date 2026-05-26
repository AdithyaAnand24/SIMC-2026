---
tags:
  - simc
---

# Choosing Histogram Bins

> [!abstract] Prerequisites
> [[matplotlib-basics]] — assumes you know `ax.hist()`.
> [[numpy-basics]] — uses `np.arange`.

## What `bins` does

`bins=N` (integer) divides your data's range into $N$ equal-width buckets and counts samples in each. The choice controls how much you **smooth** vs how much **detail** you see.

| Too few bins | Just right | Too many bins |
|---|---|---|
| Oversmoothed | Shape clear, noise low | Noisy, jagged |
| Loses structure | Tells the story | Tells no story |

## The two regimes

### 1. Continuous data → use a rule of thumb

For floats (heights, temperatures, normal samples, etc.), pick by formula or let matplotlib decide:

| Rule | Formula | When |
|---|---|---|
| **Sqrt** | $k = \sqrt{N}$ | Simple, works OK most of the time |
| **Sturges** | $k = \log_2(N) + 1$ | Small N, near-normal data |
| **Freedman-Diaconis** | $\text{width} = 2 \cdot \text{IQR} / N^{1/3}$ | Robust to outliers; what `bins='auto'` uses |

Or just delegate:

```python
ax.hist(samples, bins='auto')   # matplotlib chooses for you (uses FD)
```

For 10,000 continuous samples, `'auto'` usually picks ~50 bins.

### 2. Discrete data → snap bins to integer edges

==This is the case that trips everyone up.==

If your data is integer-valued (counts, dice rolls, streak lengths), `bins=10` will divide the *range* into 10 equal-width bins. If the range is 0-20, bin edges land at 0, 2, 4, ..., 20 — so two integer values cram into each bar. You lose information and the histogram looks chunky.

The fix: place bin edges at the **half-integers** so each integer value gets its own bin, centered on it:

```python
ax.hist(streak_lengths, bins=np.arange(0.5, 20.5, 1), edgecolor='black')
```

Produces edges `[0.5, 1.5, 2.5, ..., 19.5]`. Each integer from 1 to 19 gets a clean bar.

> [!tip] General formula for integer data
> ```python
> bins=np.arange(data.min() - 0.5, data.max() + 1.5, 1)
> ```
> Snaps the bins exactly to integer values regardless of your data range.

## Worked example

```python
import numpy as np
import matplotlib.pyplot as plt

# Discrete: number of heads in 20 coin flips, repeated 10,000 times
counts = np.random.binomial(20, 0.5, size=10_000)

fig, axs = plt.subplots(1, 3, figsize=(15, 4))

# Bad: bins=10 on integer data — chunky, off-axis
axs[0].hist(counts, bins=10, edgecolor='black')
axs[0].set_title('bins=10 (BAD for integer data)')

# Better: bins='auto' — still doesn't align to integers
axs[1].hist(counts, bins='auto', edgecolor='black')
axs[1].set_title("bins='auto' (better, but still off)")

# Best: integer edges
axs[2].hist(counts, bins=np.arange(-0.5, 21.5, 1), edgecolor='black')
axs[2].set_title('integer edges (BEST)')

plt.show()
```

The third subplot will show a clean bell curve centered on 10 (Binomial(20, 0.5) has mean 10). The first two will look chunky and misaligned.

## Pragmatic algorithm

1. **Check your data type:**
   - Integer / discrete → explicit integer bin edges (`np.arange(min-0.5, max+1.5, 1)`)
   - Continuous → start with `bins='auto'`, eyeball result, tweak if needed
2. **Eyeball the result.** Oversmoothed? → more bins. Noisy? → fewer bins.
3. **Sanity check:** each bin should have at least ~10 samples. If not, too many bins.

## Common mistakes

> [!warning] Using `bins=N` on integer data without thinking
> The default integer behavior gives equal-width bins across the data range — which usually doesn't align to your integer values. Always use explicit integer edges for discrete data.

> [!warning] Picking a "round" number like `bins=10` reflexively
> Round numbers feel safe but are usually wrong for your specific data. Either let `bins='auto'` decide or pick edges deliberately.

> [!warning] Forgetting `edgecolor='black'`
> Without edge colors, adjacent bars blur into one another and you can't tell where one bar ends. Always add `edgecolor='black'` (or another contrasting color) for histograms.

> [!warning] Comparing two histograms with different bin counts
> If you're overlaying or side-by-siding two histograms, use the **same** bin edges for both — otherwise you can't visually compare bar heights.

## Why this matters for SIMC

Histograms are the workhorse plot for showing distributions in SIMC reports. Bad bin choice makes the distribution look misleading — judges will see noise or oversmoothing and dock you. Spending 30 seconds picking the right bins is the difference between a clear plot and a confusing one.

## Sources

- [Matplotlib `hist` docs](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html)
- [NumPy histogram bin algorithms](https://numpy.org/doc/stable/reference/generated/numpy.histogram_bin_edges.html)
