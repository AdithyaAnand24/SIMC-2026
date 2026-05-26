---
tags:
  - simc
---

# Vector norm and distance

> [!abstract] In one line
> The norm is the length of a vector (Pythagoras generalized to any number of dimensions); distance between two points is the norm of the vector connecting them.

## The idea

In 2D you know Pythagoras: a point at $(3, 4)$ is $\sqrt{3^2 + 4^2} = 5$ units from the origin. The **norm** is exactly that idea, stretched to $n$ dimensions.

Think of a vector as an array. The norm is:

```
length = 0
for i in range(n):
    length += x[i] ** 2
length = length ** 0.5
```

**Distance** between two samples (two arrays) is the norm of their difference — how far apart they sit in $n$-dimensional space.

A **unit vector** is a vector whose norm equals exactly 1 — like rescaling any arrow so it points the same way but has length 1. You divide every entry by the original length.

## The math

**Norm** (written $\|\mathbf{x}\|$ or $\|\mathbf{x}\|_2$):

$$\|\mathbf{x}\| = \sqrt{\mathbf{x} \cdot \mathbf{x}} = \sqrt{\sum_{i=1}^{n} x_i^2}$$

where $x_i$ is the $i$-th entry of vector $\mathbf{x}$.

> [!note] Norm via dot product
> $\|\mathbf{x}\|^2 = \mathbf{x} \cdot \mathbf{x}$ — the dot product of a vector with itself equals its squared length.

**Distance** between vectors $\mathbf{a}$ and $\mathbf{b}$:

$$d(\mathbf{a}, \mathbf{b}) = \|\mathbf{a} - \mathbf{b}\| = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}$$

**Unit vector** (normalizing $\mathbf{x}$ to length 1):

$$\hat{\mathbf{x}} = \frac{\mathbf{x}}{\|\mathbf{x}\|}$$

so $\|\hat{\mathbf{x}}\| = 1$ always. The hat ($\hat{\phantom{x}}$) signals "unit vector."

> [!warning] Common confusion
> Normalizing a vector does NOT make its entries sum to 1 (that would be a probability vector). Normalizing makes its *Euclidean length* equal 1. The entries can be any real numbers as long as their squares sum to 1.

> [!example] Quick check
> $\mathbf{x} = [3, 4]$. $\|\mathbf{x}\| = \sqrt{9+16} = 5$. Unit vector: $\hat{\mathbf{x}} = [3/5,\ 4/5] = [0.6,\ 0.8]$. Check: $0.6^2 + 0.8^2 = 0.36 + 0.64 = 1$. ✓

## Why this matters for PCA on IR spectra

The power method (the algorithm that finds eigenvectors) renormalizes its working vector to unit length at every step — without that, entries explode or shrink to zero and the algorithm breaks. Distances between IR samples also drive the "curse of dimensionality" analysis: with 1000 wavelength channels, all pairwise distances start to look the same, making raw IR data hard to cluster until PCA compresses it.

## Builds on
- [[vector]]
- [[dot-product]]

## Leads to
- [[power-method]]
- [[distance-concentration-high-dimensions]]
