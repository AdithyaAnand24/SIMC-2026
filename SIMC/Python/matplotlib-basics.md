---
tags:
  - simc
---

# Matplotlib Basics

## What it is

==Matplotlib is Python's default plotting library== — the foundation
everyone learns first, and the thing every other Python plotting tool
either wraps or competes with. It was originally modeled on MATLAB's
plotting interface (which is why so many functions are `plt.this()` and
`plt.that()` — you're calling them on an implicit "current figure"
sitting in global state somewhere).

It has ==two coexisting API styles==:

1. **State-machine style** (`plt.plot`, `plt.xlabel`, `plt.show`) —
   terse, MATLAB-flavored, hidden global state. Fine for quick one-off
   scripts; a mess for anything with multiple subplots.
2. **Object-oriented (OO) style** (`fig, ax = plt.subplots()`, then
   `ax.plot`, `ax.set_xlabel`) — explicit, scalable, the right default.

You'll see both in the wild. ==Write the OO style; learn to read the
state-machine style.==

Alternatives exist — **seaborn** (statistical plots, prettier defaults,
built on top of matplotlib) and **plotly** (interactive, web-native) —
but matplotlib is the bedrock. Pairs with [[numpy-basics]] constantly:
NumPy arrays in, matplotlib plots out.

## Install / import

```python
import matplotlib.pyplot as plt   # the standard alias — always pyplot as plt
import numpy as np                 # almost always paired with NumPy
```

The `plt` alias is universal convention. Stick with it even if it feels
weird — every tutorial, every Stack Overflow answer, every textbook
uses `plt`.

> [!info] No clean Java analog
> Matplotlib has no direct Java equivalent worth comparing to. Java's
> plotting libraries (JFreeChart, XChart) exist but are clunky and
> rarely used outside enterprise. That said, the **pattern** of
> `fig, ax = plt.subplots()` is similar in spirit to Swing:
> "create a JFrame, then add components to it." `fig` is the window,
> `ax` is the panel you draw on.

## The two API styles

### State-machine (older, terse)

```python
plt.plot([1, 2, 3], [4, 5, 6])
plt.xlabel("x")
plt.title("Look ma, no axes object")
plt.show()
```

Matplotlib keeps a "current figure" in hidden global state. Every
`plt.xxx` call mutates it. Concise for a single plot, but as soon as
you want two subplots or want to pass a figure between functions, the
hidden state becomes a debugging nightmare.

### Object-oriented (recommended)

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_xlabel("x")
ax.set_title("Explicit is better than implicit")
plt.show()
```

`fig` is the whole figure (the window/canvas); `ax` is the plotting
area (the actual axes with ticks and data). You call methods on `ax`
instead of going through `plt`. This scales cleanly: want a 2x2 grid?
`fig, axs = plt.subplots(2, 2)` and you get a 2D array of axes objects.

> [!tip] Default to the OO style
> ==Use `fig, ax = plt.subplots()` for everything==, even single
> plots. It's slightly more typing now but saves real pain later when
> you want subplots, custom DPI, multiple legends, or to hand a figure
> off to another function. Tutorials often use the state-machine style
> — learn to read it, but write the OO style yourself.

## The basic plot types

### Line plot

```python
fig, ax = plt.subplots()
xs = np.linspace(0, 2 * np.pi, 100)
ax.plot(xs, np.sin(xs), label="sin(x)")
ax.plot(xs, np.cos(xs), label="cos(x)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Sine and cosine")
ax.legend()
plt.show()
```

Call `ax.plot` multiple times to overlay lines on the same axes. The
`label=` kwarg is what `ax.legend()` reads.

### Scatter plot

```python
xs = np.random.normal(size=200)
ys = np.random.normal(size=200)
fig, ax = plt.subplots()
ax.scatter(xs, ys, alpha=0.5, s=10)   # alpha = transparency, s = marker size
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.show()
```

Useful kwargs: `alpha` (0 transparent, 1 opaque) for dense point clouds,
`s` for marker size, `c` for color (can be an array — color-by-value).

### Histogram

```python
samples = np.random.normal(loc=0, scale=1, size=10_000)  # 10k Normal samples
fig, ax = plt.subplots()
ax.hist(samples, bins=50, edgecolor="black")
ax.set_xlabel("value")
ax.set_ylabel("count")
ax.set_title("Histogram of 10,000 standard Normal samples")
plt.show()
```

`bins` controls how many buckets — too few hides structure, too many is
noisy. `edgecolor="black"` draws bar borders so adjacent bars are
visually distinct (the default makes them blur together).

### Bar plot

```python
categories = ["A", "B", "C", "D"]
heights = [3, 7, 2, 5]
fig, ax = plt.subplots()
ax.bar(categories, heights)
plt.show()
```

For ==already-bucketed categorical data==. Don't confuse with `hist`
(see common mistakes).

## Labels, title, legend, grid

```python
ax.set_xlabel("x label")
ax.set_ylabel("y label")
ax.set_title("Plot title")
ax.legend()                # only works if plot calls used label="..."
ax.grid(True, alpha=0.3)   # grid with light transparency
```

State-machine equivalents are `plt.xlabel`, `plt.ylabel`, `plt.title`,
`plt.legend`, `plt.grid` — same args, no `set_` prefix. Both work; pick
one style per plot.

## Log scales

```python
fig, ax = plt.subplots()
ax.plot(xs, ys)
ax.set_xscale("log")    # log x-axis
ax.set_yscale("log")    # log y-axis
# Or both at once with the convenience method:
ax.loglog(xs, ys)
```

Quick demo on synthetic $y = 1/x$ data:

```python
xs = np.logspace(0, 3, 50)   # 50 points from 10^0 to 10^3, log-spaced
ys = 1 / xs                  # y = 1/x → straight line slope -1 on log-log
fig, ax = plt.subplots()
ax.loglog(xs, ys, marker="o")
ax.set_xlabel("x (log scale)")
ax.set_ylabel("y (log scale)")
ax.set_title("y = 1/x on log-log axes")
ax.grid(True, which="both", alpha=0.3)  # "both" = major + minor gridlines
plt.show()
```

> [!example] Log-log straight line = power law
> If $y = c \cdot x^k$, then $\log y = \log c + k \log x$. On log-log
> axes, this is a ==straight line of slope $k$ and intercept $\log c$==.
> Spotting straight lines in log-log plots is THE way to detect power
> laws in data — which is why log-log is the go-to view for convergence
> rates, scaling laws, and anything $\propto N^{\alpha}$.

## Saving figures (DPI matters)

```python
fig.savefig("plot.png", dpi=150, bbox_inches="tight")
```

- `dpi=150` — decent for screens; use `300` for print/PDF.
- `bbox_inches="tight"` — trims excess whitespace around the figure.
- File extension picks the format: `.png`, `.pdf`, `.svg`, `.jpg`.

==For SIMC submissions, save as PDF or high-DPI PNG.== Vector formats
(`.pdf`, `.svg`) stay sharp at any zoom; raster (`.png`) is fine if you
use `dpi=300`.

## Multiple subplots

```python
fig, axs = plt.subplots(1, 2, figsize=(12, 5))   # 1 row, 2 columns
axs[0].plot(xs, np.sin(xs))
axs[0].set_title("sin(x)")
axs[1].plot(xs, np.cos(xs))
axs[1].set_title("cos(x)")
plt.tight_layout()   # auto-adjusts spacing so labels don't overlap
plt.show()
```

For a 2x2 grid: `fig, axs = plt.subplots(2, 2)`, then index as
`axs[0, 0]`, `axs[0, 1]`, `axs[1, 0]`, `axs[1, 1]` (2D NumPy indexing —
see [[numpy-basics]]).

`plt.tight_layout()` is almost always worth calling — it prevents
labels and titles from overlapping between subplots.

## Common mistakes

> [!warning] Forgetting `plt.show()` or `fig.savefig()`
> Without one of these, nothing happens — the figure exists in memory
> but never renders. In Jupyter notebooks, plots often render
> automatically at the end of a cell, but in standalone scripts you
> MUST call `plt.show()` (to display) or `fig.savefig()` (to write to
> disk). Silent no-output is the #1 beginner trap.

> [!warning] Mixing state-machine and OO styles
> Don't switch between `plt.xlabel()` and `ax.set_xlabel()` inside the
> same plot. Pick one. The state-machine calls act on whatever "current
> axes" matplotlib thinks is active, which may not be your `ax`.

> [!warning] `hist` vs `bar`
> `ax.hist(data)` is for ==binning continuous data into a histogram==
> (you give it raw values, it counts).
> `ax.bar(categories, heights)` is for ==already-bucketed categorical
> data== (you give it labels + heights). Using the wrong one gives
> baffling results — `hist` on category names will crash; `bar` on raw
> data won't bin anything.

> [!warning] `figsize` is in inches, not pixels
> `figsize=(8, 5)` means 8 inches wide, 5 inches tall. Total pixels =
> `figsize * dpi`. So `figsize=(8, 5)` at `dpi=150` is 1200x750 px.
> Confused students sometimes pass huge `figsize=(800, 500)` trying to
> get pixel dimensions — that produces an 800-inch-wide figure
> (matplotlib will refuse or grind your machine).

> [!warning] Default figure is too small for reports
> The default `figsize=(6.4, 4.8)` is tiny — fine for a notebook
> preview, cramped for a written report. ==Set `figsize=(8, 5)` or
> larger== for anything you're submitting.

> [!warning] Calling `plt.show()` clears the figure
> After `plt.show()` returns, the figure state is reset. If you want
> to both display and save, ==save first, then show==:
> `fig.savefig(...)` then `plt.show()`.

## Why this matters for SIMC

Every SIMC submission needs plots — judges expect them and your
argument is much weaker without visual evidence. Matplotlib is the
standard tool; nothing else is worth your time right now. The two-API
confusion is the #1 time-sink for beginners — ==pick the OO style and
stick with it== and you'll save hours of "wait, why isn't this label
showing up?" debugging. Log-log plots in particular are a SIMC judging
favorite: they're how you visually demonstrate convergence rates like
$|\text{error}| \sim 1/\sqrt{N}$ as straight lines, which is much more
convincing than just quoting a number.

## Sources

- [Matplotlib quickstart guide](https://matplotlib.org/stable/users/explain/quick_start.html)
- [Matplotlib pyplot tutorial](https://matplotlib.org/stable/tutorials/pyplot.html)
- [Matplotlib official tutorials index](https://matplotlib.org/stable/tutorials/index.html)
- [Axes API reference](https://matplotlib.org/stable/api/axes_api.html)
