---
tags:
  - simc
---

# Surface-to-Volume Ratio in High Dimensions

> [!abstract] In one line
> In high dimensions a solid object is almost entirely surface — the interior essentially vanishes, so intuitions about "center" and "typical point" completely fail.

## The idea

Picture a peach. Most of it is flesh (interior); the skin is a thin layer you barely notice. Now imagine a 1000-D "peach." The skin has grown to swallow nearly the entire fruit. There is almost no flesh left. The object is all skin, no filling.

This sounds impossible, but it falls directly out of how volume scales with dimension.

Another way to see it: a unit cube in $d$ dimensions has side length 1, but an inscribed ball (touching the middle of each face) has radius $\tfrac{1}{2}$. As $d$ grows, the ball's volume shrinks to zero while the cube's stays 1. All the cube's "mass" ends up in the corners — i.e., at the surface — not near the center.

Consequence for data: if you sample points uniformly from a high-D ball, almost every point lands near the surface. There are essentially no "interior" points. Your intuition about what a "typical" or "average" data point looks like (sitting somewhere in the middle) is wrong.

## The math

Consider a $d$-dimensional ball of radius $R = 1$.

Define a thin shell of relative thickness $\varepsilon$ just inside the surface: the inner region has radius $1 - \varepsilon$.

The fraction of the total volume contained in the inner region is:

$$f_{\text{inner}} = \left(\frac{1-\varepsilon}{1}\right)^d = (1-\varepsilon)^d$$

The fraction in the **shell** (within $\varepsilon$ of the surface) is therefore:

$$f_{\text{shell}} = 1 - (1-\varepsilon)^d$$

> [!example] Concrete numbers
> Let $\varepsilon = 0.01$ (a 1% shell). Then:
> - $d = 2$: shell holds $\approx 2\%$ of volume. Most is interior. ✓ matches intuition.
> - $d = 100$: shell holds $1 - 0.99^{100} \approx 63\%$ of volume.
> - $d = 1000$: shell holds $1 - 0.99^{1000} \approx 99.996\%$ of volume.
>
> A 1% shell swallows essentially everything at 1000 dimensions.

As $d \to \infty$: $(1-\varepsilon)^d \to 0$ for any fixed $\varepsilon > 0$, so $f_{\text{shell}} \to 1$.

**Unit cube vs. inscribed ball:**
$$\frac{V_{\text{ball}}}{V_{\text{cube}}} = \frac{\pi^{d/2}}{\Gamma(d/2+1)} \cdot \frac{1}{2^d} \xrightarrow{d\to\infty} 0$$

The ball's volume fraction goes to zero; all the cube's volume is in its corners.

> [!warning] Common confusion
> The shell doesn't "shrink" — it stays at absolute thickness $\varepsilon R$. What changes is that the relative importance of the interior collapses. In a 1000-D space even a physically thick shell contains almost all the volume.

## Why this matters for PCA on IR spectra

If you tried to characterize the "center" of IR spectral space (e.g. the mean spectrum as a representative sample), it would be a nearly empty region — real spectra all crowd near the boundary. More practically, distance-based methods that assume data fills a region (like kernel density estimation) break silently. Reducing to the true low-D manifold via PCA places you in a space where centers and distances mean what you think they mean again.

## Builds on
- [[curse-of-dimensionality]]

## Leads to
- [[manifold-hypothesis]]
