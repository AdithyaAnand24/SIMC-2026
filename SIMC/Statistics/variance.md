---
tags:
  - simc
---

# Variance

> [!abstract] In one line
> Variance is the average squared distance from the mean — it measures how spread out a single feature is, and PCA hunts for the directions in which variance is largest.

## The idea

You already know variance from probability. Here's the quick recap through a geometric lens: imagine plotting all $n$ values of one feature on a number line. The mean $\bar{x}$ is the center. Variance asks: *on average, how far are the points from that center?* It squares the distances before averaging so that points above and below the mean don't cancel each other out.

Think of variance as the "width" of a distribution. A narrow spike has low variance; a wide spread has high variance.

**The key bridge to PCA:** PCA is essentially a search algorithm. It asks, "If I project all my data onto some direction (a line through the origin), which direction gives the projected points the most spread?" That spread *is* variance. PCA finds the direction of **maximum variance** first, then the direction of maximum remaining variance, and so on. Variance is the exact quantity PCA is maximizing at every step.

## The math

For $n$ observations of a single centered feature (so $\bar{x} = 0$ after centering):

$$\mathrm{Var}(x) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

**Symbols:**
- $x_i$ — value of observation $i$
- $\bar{x}$ — mean of the feature
- $n - 1$ — Bessel's correction: dividing by $n-1$ instead of $n$ gives an unbiased estimate when you have a sample rather than the full population

If the data are already centered ($\bar{x} = 0$, which they are after running [[mean-and-centering]]):

$$\mathrm{Var}(x) = \frac{1}{n-1} \sum_{i=1}^{n} x_i^2$$

> [!note] Standard deviation
> $\mathrm{SD}(x) = \sqrt{\mathrm{Var}(x)}$. Variance is in squared units; standard deviation brings it back to original units. PCA works with variance directly.

> [!warning] Common confusion
> Variance is always non-negative (it's a sum of squares). A variance of zero means every observation is identical — that feature carries zero information and PCA would assign it zero importance.

> [!tip] Units matter for PCA
> If one feature is in kilometers and another is in millimeters, the kilometer feature will have artificially inflated variance just from the scale. Always check whether to **standardize** (divide each feature by its standard deviation after centering) before running PCA. For IR spectra where all channels share the same absorbance units, centering alone is usually enough.

## Why this matters for PCA on IR spectra

An IR spectrum has ~1000 absorbance channels. Some wavenumber regions vary a lot across samples (high variance — chemically informative); others barely move (low variance — noise or instrument baseline). PCA captures the high-variance directions first, automatically ranking the channels by how much they differ across your sample set. The first few principal components will pick up the biggest sources of chemical variation in the spectra.

## Builds on

- [[mean-and-centering]]

## Leads to

- [[covariance]]
- [[eigenvectors-of-the-covariance-matrix]]
