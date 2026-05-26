---
tags:
  - simc
---

# Distance Concentration in High Dimensions

> [!abstract] In one line
> In high dimensions all pairwise distances converge to nearly the same value, so "nearest neighbour" becomes meaningless and noise drowns out every real signal.

## The idea

Imagine you're in a crowd and you want to find your closest friend. In a small room (2D), some people are clearly nearer than others — easy. Now stretch that room into 1000 dimensions. Distances pile up from every axis, and by the time you're done, every person is roughly the same enormous distance from you. Your "nearest friend" is barely closer than a stranger on the far side of the space. The concept of "near" has dissolved.

There are two separate mechanisms that cause this:

**Mechanism 1 — Distance grows with dimension.** Euclidean distance sums squared differences over all $p$ axes. Even if each individual axis contributes tiny random noise, those contributions accumulate. The noise itself pushes every point away from every other.

**Mechanism 2 — Relative contrast collapses.** Even if max and min distances both grow, the *ratio* of their difference to the minimum distance goes to zero. You lose the ability to distinguish "close" from "far."

> [!example] Analogy
> Imagine measuring how loud two songs are, adding one random instrument at a time. Each instrument adds a little noise to both songs. Eventually both songs are so dominated by random noise that you can't tell which was originally louder. The signal is drowned; only the noise remains.

## The math

**Distance accumulates like $\sqrt{p}$:**

If the difference in each coordinate between two points is a random variable with mean 0 and variance $\sigma^2$, the expected squared Euclidean distance is:

$$\mathbb{E}\left[\|\mathbf{x} - \mathbf{y}\|^2\right] = \sum_{j=1}^{p} \mathbb{E}[(x_j - y_j)^2] = p\sigma^2$$

So the expected distance scales as $\|\mathbf{x} - \mathbf{y}\| \sim \sigma\sqrt{p}$.

(See [[vector-norm-and-distance]] for the Euclidean norm definition.)

**Relative contrast → 0:**

Let $d_{\max}$ and $d_{\min}$ be the largest and smallest pairwise distances among $n$ points. A classic result (Beyer et al., 1999) shows:

$$\frac{d_{\max} - d_{\min}}{d_{\min}} \xrightarrow{p \to \infty} 0$$

All distances become indistinguishable.

**Noise has many directions to hide in:**

The real signal in IR data lives on a low-$k$ dimensional manifold inside $\mathbb{R}^p$. Random noise can shove a point in any of the $p$ directions. There are $p - k$ "noise directions" and only $k$ "signal directions." When $p \gg k$ (e.g., $p = 1000$, $k = 3$), almost all perturbations are pure noise. The signal-to-noise ratio effectively shrinks as $p$ grows.

> [!warning] Common confusion
> This doesn't mean all distances become *equal* in a strict sense — it means the *relative spread* of distances collapses. Nearest-neighbour algorithms still return *an* answer, but that answer is statistically meaningless because every point is approximately equidistant from the query point.

## Why this matters for PCA on IR spectra

IR spectra are ~1000-D vectors. Any classifier or clustering algorithm that relies on Euclidean distances (k-NN, k-means, Mahalanobis distance) will fail if applied directly to raw spectra: all spectra will appear nearly equidistant. PCA first projects onto the ~5–20 directions where real chemical variance lives, collapsing the $\approx 980$–995 noisy dimensions. In the reduced space, distances are meaningful again.

## Builds on
- [[curse-of-dimensionality]]
- [[vector-norm-and-distance]]

## Leads to
- [[manifold-hypothesis]]
