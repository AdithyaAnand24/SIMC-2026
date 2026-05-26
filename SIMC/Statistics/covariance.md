---
tags:
  - simc
---

# Covariance

> [!abstract] In one line
> Covariance measures whether two features rise and fall together — it is the signed version of variance extended to pairs of features.

## The idea

[[variance]] told you how spread out *one* feature is. Covariance asks about *two* features: **do they move together?**

Picture a dataset of people. Height and weight tend to be positively correlated — tall people tend to be heavier. When height is above its mean, weight tends to be above its mean too. Their covariance is positive.

Now picture height and resting heart rate — no consistent relationship. Sometimes a tall person has a high heart rate, sometimes low. Those two features vary independently. Their covariance is near zero.

If feature A goes up whenever feature B goes down (and vice versa), they are negatively correlated. Covariance is negative.

**Intuition for the sign:**
- $(x_i - \bar{x})$ is positive when $x$ is above its mean, negative when below
- $(y_i - \bar{y})$ similarly
- Their product is positive when both deviate in the **same direction**, negative when they deviate in **opposite directions**
- Averaging those products over all observations gives you the covariance

## The math

For $n$ observations of two features $x$ and $y$:

$$\mathrm{Cov}(x, y) = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

**Symbols:**
- $x_i, y_i$ — values of the two features for observation $i$
- $\bar{x}, \bar{y}$ — means of each feature

**Special cases:**
- $\mathrm{Cov}(x, x) = \mathrm{Var}(x)$ — variance is just a feature's covariance with itself
- $\mathrm{Cov}(x, y) = \mathrm{Cov}(y, x)$ — covariance is symmetric

**Connection to the dot product:**

After centering (so $\bar{x} = \bar{y} = 0$), the formula becomes:

$$\mathrm{Cov}(x, y) = \frac{1}{n-1} \sum_{i=1}^{n} x_i y_i = \frac{1}{n-1} \, \mathbf{x} \cdot \mathbf{y}$$

where $\mathbf{x}$ and $\mathbf{y}$ are the centered column vectors. Covariance is proportional to the [[dot-product]] of the two centered columns. This geometric link is worth holding onto: the [[dot-product]] of two vectors is zero when they are **perpendicular**. So:

$$\mathrm{Cov}(x, y) = 0 \iff \text{uncorrelated} \iff \text{centered columns are perpendicular}$$

PCA finds a new set of axes where all the column pairs end up perpendicular — making all off-diagonal covariances zero.

> [!warning] Common confusion
> Covariance = 0 means **uncorrelated**, not independent. Independence is a stronger statement. Two features can have zero covariance but still have a non-linear relationship. For PCA this distinction rarely matters in practice, but don't confuse the two.

> [!note] Normalizing gives correlation
> The **Pearson correlation coefficient** is just covariance normalized by the product of standard deviations:
> $$r_{xy} = \frac{\mathrm{Cov}(x,y)}{\mathrm{SD}(x)\,\mathrm{SD}(y)} \in [-1, 1]$$
> Covariance has units (e.g., absorbance²); correlation is dimensionless. PCA uses covariance, not correlation (unless you standardize first).

## Why this matters for PCA on IR spectra

IR absorption bands are often correlated — nearby wavenumber channels absorb similarly because they reflect overlapping molecular vibrations from the same bond type. A high covariance between channels 1600 cm⁻¹ and 1620 cm⁻¹ tells PCA "these two channels carry redundant information; bundle them." PCA's job is to find new axes where all such cross-channel correlations disappear, giving you independent summary variables (principal components).

## Builds on

- [[variance]]
- [[mean-and-centering]]
- [[dot-product]]

## Leads to

- [[covariance-matrix]]
