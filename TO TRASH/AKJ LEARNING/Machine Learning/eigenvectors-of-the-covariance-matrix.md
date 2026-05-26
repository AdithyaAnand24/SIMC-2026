---
tags:
  - simc
---

# Eigenvectors of the Covariance Matrix

> [!abstract] In one line
> When you find the eigenvectors of the covariance matrix, each one points along a direction the data actually spreads, and its eigenvalue tells you exactly how much spread there is in that direction.

## The idea

Imagine a cloud of data points plotted in 2D. The cloud isn't a perfect circle — it's an elongated ellipse tilted at some angle. There's a long axis (the direction the data spreads most) and a short axis (the direction it barely varies).

The eigenvectors of the [[covariance-matrix]] are exactly those axes. They are the skeleton of the data cloud.

Each eigenvector is a direction, and its paired eigenvalue $\lambda$ is a number that says: "the data, measured only along *this* direction, has variance $\lambda$."

- **Biggest eigenvalue → longest axis → most informative direction.** A point's position along this axis tells you the most about it.
- **Smallest eigenvalue → shortest axis → near-flat direction.** Almost nothing interesting happens here; it's mostly noise.
- All eigenvectors are **mutually perpendicular** (orthogonal), so the axes don't overlap or double-count.

Think of it like finding the natural coordinate system that the data itself prefers, instead of the arbitrary x/y/z axes the instrument recorded.

## The math

Let $\mathbf{C}$ be the $p \times p$ [[covariance-matrix]] of a centered dataset with $p$ features.

By the **Spectral Theorem**, because $\mathbf{C}$ is symmetric, it has a complete set of real, orthogonal eigenvectors $\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_p$ with real eigenvalues $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_p \geq 0$.

Each pair satisfies the defining equation (see [[eigenvectors-and-eigenvalues]]):
$$\mathbf{C}\,\mathbf{v}_i = \lambda_i\,\mathbf{v}_i$$

**Key identity — eigenvalue = variance along eigenvector:**

If you project every data point onto $\mathbf{v}_i$ (getting a scalar score per point), the [[variance]] of those scores is exactly $\lambda_i$.

$$\text{Var}(\text{scores along } \mathbf{v}_i) = \lambda_i$$

**Total variance is preserved:**
$$\sum_{i=1}^{p} \lambda_i = \text{trace}(\mathbf{C}) = \sum_{j=1}^{p} \text{Var}(x_j)$$

Nothing is lost; the variance is just redistributed into these new axes.

> [!warning] Common confusion
> The eigenvectors are directions (unit vectors), not data points. They live in feature space, not sample space. One eigenvector has $p$ components (one per wavenumber), not $n$ components (one per sample).

## Why this matters for PCA on IR spectra

An IR spectrum has ~1000 wavenumbers, giving a 1000-D covariance matrix with 1000 eigenvectors. But if the samples only vary due to a handful of chemical concentrations, almost all the variance is packed into the first few eigenvectors. Those are the axes worth keeping. The eigenvectors with tiny eigenvalues capture noise you can safely discard — this is the core logic of [[principal-component-analysis]] applied to IR data.

## Builds on
- [[eigenvectors-and-eigenvalues]]
- [[covariance-matrix]]
- [[variance]]

## Leads to
- [[principal-component-analysis]]
- [[eigenspectrum]]
