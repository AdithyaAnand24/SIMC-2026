---
tags:
  - simc
---

# Curse of Sampling

> [!abstract] In one line
> To sample a high-dimensional space at even crude resolution you need exponentially many points — far more than any experiment could ever collect.

## The idea

Suppose you want to cover a 1D line with evenly spaced measurements: 10 bins suffice to get a rough picture. Now cover a 2D square: you need $10 \times 10 = 100$ grid squares. A 3D cube: $10^3 = 1000$ cells. Each time you add one dimension you multiply the count by 10.

For 1000 dimensions: $10^{1000}$ sample points.

The estimated number of atoms in the observable universe is about $10^{80}$. You are short by $10^{920}$ atoms' worth of samples.

This means that for any real dataset — hundreds of IR spectra, thousands at best — your data is *infinitely* sparse compared to the space it nominally lives in. No matter how densely your samples seem packed, the vast majority of the 1000-D space has never been visited and never will be.

> [!example] Analogy
> You want to characterize the taste of every possible pizza by sampling one pizza for each combination of toppings. With 10 toppings and 3 options each (none / light / heavy), you already need $3^{10} = 59{,}049$ pizzas just to cover all combinations at the coarsest resolution. Add 10 more toppings and you need $3^{20} \approx 3.5$ billion. Real IR spectra have ~1000 "topping slots" (wavenumbers). The pizza shop burns down before you finish ordering.

## The math

Suppose you partition each of $p$ dimensions into $k$ equal bins. The number of grid cells you must populate with at least one sample to have a "complete" picture is:

$$N_{\text{required}} = k^p$$

For any fixed resolution $k > 1$, this grows exponentially in $p$.

Conversely, if you have only $n$ actual samples spread over $k^p$ cells, the fraction of cells that contain at least one sample is:

$$\text{coverage} \approx \frac{n}{k^p} \xrightarrow{p \to \infty} 0$$

Even if $n$ is large (say $10^6$), coverage collapses to zero for $p$ in the hundreds.

> [!example] Numbers
> $k = 10$ bins per axis, $n = 1{,}000$ samples.
> - $p = 3$: need $10^3 = 1{,}000$ cells. Coverage $\approx 100\%$. Dense!
> - $p = 6$: need $10^6$ cells. Coverage $= 0.1\%$.
> - $p = 10$: need $10^{10}$ cells. Coverage $= 0.00001\%$.
> - $p = 1000$: astronomically sparse.

**A related way to think about it — nearest-neighbour distance:**

For $n$ uniformly distributed points in a $p$-dimensional unit cube, the expected distance to the nearest neighbour scales as:

$$d_{\text{nn}} \sim n^{-1/p}$$

Even with $n = 10^6$ samples in $p = 1000$ dimensions, $d_{\text{nn}} \approx (10^6)^{-1/1000} = 10^{-6/1000} \approx 0.986$ — almost the maximum possible distance of 1. Every point's "nearest neighbour" is nearly as far as the farthest point.

> [!warning] Common confusion
> The curse of sampling isn't about "not collecting enough data in practice." Even in principle — with unlimited resources — you can never collect $10^{1000}$ spectra. The fundamental problem is combinatorial: the space is categorically unsamplable at any useful resolution.

## Why this matters for PCA on IR spectra

You will never have enough IR spectra to characterise 1000-D space directly. But you don't need to, because the samples don't fill 1000-D space — they cluster on a low-dimensional manifold (see [[manifold-hypothesis]]). PCA finds that manifold and projects onto it. Once you're in 5–20 dimensions rather than 1000, the sampling problem becomes tractable: a few hundred spectra can densely cover a 5-D space.

## Builds on
- [[curse-of-dimensionality]]

## Leads to
- [[manifold-hypothesis]]
