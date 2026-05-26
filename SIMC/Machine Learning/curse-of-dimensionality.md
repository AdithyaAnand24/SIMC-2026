---
tags:
  - simc
---

# Curse of Dimensionality

> [!abstract] In one line
> Your 2D and 3D intuition is wrong in high dimensions — space becomes so vast and so weird that naive data analysis quietly breaks.

## The idea

You know how a 2D map works: two numbers pin any location, "nearby" means something sensible, and you can cover a city with a modest grid of squares. Now imagine your data has 1000 numbers per point (like one IR spectrum per sample). The "space" those points live in has 1000 dimensions — and it behaves nothing like a city map.

Three specific disasters happen, each strange enough to deserve its own note:

1. **"All skin, no filling"** — objects in high dimensions have almost all their volume jammed into a thin shell at the surface. The center is essentially empty. → [[surface-to-volume-ratio-high-dimensions]]

2. **"Everything is equally far"** — distances pile up as you add axes, and eventually every pair of points is nearly the same large distance apart, making "nearest neighbour" meaningless. → [[distance-concentration-high-dimensions]]

3. **"You can never collect enough data"** — covering the space at any useful resolution requires exponentially many samples, far more than any real experiment can provide. → [[curse-of-sampling]]

Together they mean: if your data actually *lived* in all 1000 dimensions, you could never analyze it. Luckily, real data doesn't — see [[manifold-hypothesis]].

## The math

There's no single formula for the curse; it's a family of results. The unifying thread is that geometric quantities scale with $d$ (dimension) in explosive ways.

Dimension $d$ appears in exponents:
- Volume of a unit ball: $V_d = \dfrac{\pi^{d/2}}{\Gamma(d/2+1)} \to 0$ as $d \to \infty$
- Fraction of volume in shell of thickness $\varepsilon$: $1 - (1-\varepsilon)^d \to 1$
- Samples needed to cover grid with $k$ bins per axis: $k^d$

Each formula says the same thing in a different dialect: **dimension in the exponent = catastrophe.**

> [!warning] Common confusion
> High dimensionality doesn't mean "lots of data." It means lots of *features per data point* — e.g. 1000 wavenumbers measured per spectrum. You can have 10 spectra (samples) each with 1000 features. The curse is about the feature dimension $p$, not the sample count $n$.

## Why this matters for PCA on IR spectra

IR spectra live in ~1000-D space. If you tried to do any distance-based analysis directly (clustering, k-NN classification, density estimation), the curse would destroy the result — distances concentrate, the space is empty, and nothing generalises. This is exactly why we need [[principal-component-analysis]]: reduce from 1000 dimensions to ~5–20 meaningful ones before any further analysis.

## Builds on
- [[what-is-a-dimension]]

## Leads to
- [[surface-to-volume-ratio-high-dimensions]]
- [[distance-concentration-high-dimensions]]
- [[curse-of-sampling]]
- [[manifold-hypothesis]]
