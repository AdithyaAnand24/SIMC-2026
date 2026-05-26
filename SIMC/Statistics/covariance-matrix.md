---
tags:
  - simc
---

# Covariance matrix

> [!abstract] In one line
> The covariance matrix is a single square grid that records the variance of every feature and the covariance between every pair — it is the complete description of how your data spreads, and it is what PCA factorizes.

## The idea

You have $p$ features. Each pair of features has a covariance. Instead of keeping $p^2$ separate numbers scattered around, you pack them all into one tidy square grid: the **covariance matrix** $C$.

Think of it like a mileage chart on a road map: rows and columns both label the same set of cities (features), and each cell holds the "distance" (covariance) between the row-city and the column-city. The diagonal cells are the city's distance to itself — which is its variance.

For IR spectra with 1000 wavenumber channels, $C$ is a $1000 \times 1000$ grid. That's one million entries, but only about half a million are unique (because $C_{ij} = C_{ji}$). PCA reduces all of that to a handful of eigenvectors — that's the payoff.

## The math

For a dataset with $p$ features, $C$ is a $p \times p$ matrix where:

$$C_{ij} = \mathrm{Cov}(\text{feature } i,\, \text{feature } j)$$

**Diagonal entries** ($i = j$): variances of each feature
$$C_{ii} = \mathrm{Var}(\text{feature } i)$$

**Off-diagonal entries** ($i \neq j$): covariances between pairs
$$C_{ij} = \mathrm{Cov}(\text{feature } i, \text{feature } j)$$

**Symmetry:** $C_{ij} = C_{ji}$, so $C = C^\top$ — the covariance matrix is always symmetric.

**Compact matrix formula:**

Let $X$ be the centered $n \times p$ [[design-matrix]] (rows = observations, columns = centered features). Then:

$$C = \frac{1}{n-1} X^\top X$$

This is a [[matrix-vector-multiplication]] between the transpose of $X$ and $X$ itself. Each entry $C_{ij}$ computes to $\frac{1}{n-1}\sum_k X_{ki} X_{kj}$, which is exactly $\mathrm{Cov}(\text{feature }i, \text{feature }j)$ on centered data. One matrix multiplication encodes all $p^2$ covariances at once.

> [!example] Tiny example (2 features)
> Features: wavenumber channel A, wavenumber channel B.
> $$C = \begin{pmatrix} \mathrm{Var}(A) & \mathrm{Cov}(A,B) \\ \mathrm{Cov}(B,A) & \mathrm{Var}(B) \end{pmatrix}$$
> If $\mathrm{Cov}(A,B) = 0$, the two channels are uncorrelated and the matrix is diagonal — the ideal post-PCA situation.

> [!warning] Common confusion
> The covariance matrix is $p \times p$ (features × features), **not** $n \times p$ (observations × features). It summarizes how features relate to each other across all observations. Confusing $X$ with $C$ is a frequent source of dimension errors.

> [!note] Always symmetric positive semi-definite
> Because $C = \frac{1}{n-1}X^\top X$, it is always symmetric and **positive semi-definite** — meaning all its eigenvalues are $\geq 0$. This is why PCA eigenvalues (= variances captured) are never negative.

## Why this matters for PCA on IR spectra

PCA works by finding the eigenvectors of the covariance matrix $C$. Those eigenvectors become the new axes (principal components); the corresponding eigenvalues tell you how much variance each axis captures. The entire PCA algorithm is: (1) center $X$, (2) compute $C = \frac{1}{n-1}X^\top X$, (3) decompose $C$ into eigenvectors. Every subsequent step flows from this matrix.

## Builds on

- [[covariance]]
- [[matrix]]
- [[design-matrix]]

## Leads to

- [[diagonal-covariance-matrix]]
- [[eigenvectors-of-the-covariance-matrix]]
- [[principal-component-analysis]]
