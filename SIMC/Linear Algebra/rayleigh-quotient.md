---
tags:
  - simc
---

# Rayleigh quotient

> [!abstract] In one line
> Once you have an approximate eigenvector, the Rayleigh quotient is the formula that reads off its eigenvalue — it measures how much the matrix stretches that particular direction.

## The idea

The power method gives you a vector $\mathbf{b}$ that (hopefully) points along an eigenvector. But what is the corresponding eigenvalue? You need the stretch factor.

Here's the intuition: if $\mathbf{b}$ is truly an eigenvector, then $C\mathbf{b} = \lambda\mathbf{b}$. Both sides point the same way; the eigenvalue $\lambda$ is just the ratio of their lengths. The Rayleigh quotient computes that ratio cleanly using dot products.

Think of it this way: push $\mathbf{b}$ through the matrix $C$, then measure how much it grew (using a dot product instead of raw length, to handle the direction too).

## The math

For a square matrix $C$ and any non-zero vector $\mathbf{b}$, the **Rayleigh quotient** is:

$$R(\mathbf{b}) = \frac{\mathbf{b}^\top C\,\mathbf{b}}{\mathbf{b}^\top \mathbf{b}}$$

- $\mathbf{b}^\top C\,\mathbf{b}$ — numerator: first multiply $C\mathbf{b}$ (matrix-vector product), then dot with $\mathbf{b}$. Result is a scalar.
- $\mathbf{b}^\top \mathbf{b}$ — denominator: dot product of $\mathbf{b}$ with itself $= \|\mathbf{b}\|^2$. Also a scalar.
- $R(\mathbf{b})$ — a single number (the estimated eigenvalue).

**For a unit vector** $\hat{\mathbf{b}}$ (where $\|\hat{\mathbf{b}}\| = 1$):

$$R(\hat{\mathbf{b}}) = \hat{\mathbf{b}}^\top C\,\hat{\mathbf{b}}$$

The denominator collapses to 1 because $\hat{\mathbf{b}}^\top \hat{\mathbf{b}} = \|\hat{\mathbf{b}}\|^2 = 1$. This is the version used inside the power method loop, since the vector is renormalized at every step.

> [!example] What it means numerically
> After the power method converges to unit vector $\hat{\mathbf{b}}$, compute $C\hat{\mathbf{b}}$ and then take the dot product with $\hat{\mathbf{b}}$. If you get $0.87$, that means this principal component captures variance $0.87$ (in whatever units the covariance matrix uses). The eigenvalue IS the variance along that direction.

> [!note] Key property
> The Rayleigh quotient is **maximized** exactly when $\mathbf{b}$ points along the top eigenvector, and the maximum value equals the largest eigenvalue $\lambda_1$. This is why the power method's repeated multiplication keeps pushing $\mathbf{b}$ toward the top eigenvector — it is simultaneously maximizing the Rayleigh quotient.

> [!warning] Common confusion
> The Rayleigh quotient is NOT the same as the norm of $C\mathbf{b}$. It is a directional measure — it accounts for how much of the output $C\mathbf{b}$ still points along $\mathbf{b}$, not just how long the output is.

**In code (for unit vector `b`):**

```python
import numpy as np

# C is the covariance matrix, b is the current unit vector
Cb = C @ b                    # matrix-vector multiply
eigenvalue_estimate = b @ Cb  # dot product → scalar
```

This two-liner is what you run at the end of the power method to read off the eigenvalue.

## Why this matters for PCA on IR spectra

In PCA on IR spectra, the eigenvalue of each principal component equals the **variance** of the dataset along that direction. The Rayleigh quotient is how you compute it: once the power method finds a principal direction, apply the formula to get the eigenvalue, which tells you what fraction of total spectral variation is captured by that component. Dividing each eigenvalue by the sum of all eigenvalues gives the **explained variance ratio** — the standard way to decide how many components to keep.

## Builds on
- [[dot-product]]
- [[eigenvectors-and-eigenvalues]]

## Leads to
- [[power-method]]
