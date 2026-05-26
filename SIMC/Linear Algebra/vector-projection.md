---
tags:
  - simc
---

# Vector projection

> [!abstract] In one line
> Projecting a vector onto a direction gives its "shadow" on that line — one number that is the coordinate of the point along that axis.

## The idea

Shine a torch straight down onto a ruler lying flat. The shadow of a pencil on the ruler is the pencil's **projection** — it tells you how far along the ruler the pencil "really is" if you ignore the up-down part.

In math: you have a data point $\mathbf{x}$ (a list of $n$ measurements). You want to know how much of that point lies along some direction $\hat{\mathbf{u}}$ (a unit vector). The answer is one number — the **scalar projection**:

```
score = 0
for i in range(n):
    score += x[i] * u_hat[i]   # just a dot product
```

That single number `score` is the new coordinate of $\mathbf{x}$ on the axis defined by $\hat{\mathbf{u}}$.

This is exactly how PCA compresses data: each of the $m$ samples is projected onto the top $k$ principal directions, replacing $n$ original numbers per sample with just $k$ new numbers per sample.

## The math

Let $\hat{\mathbf{u}}$ be a **unit vector** (length 1) pointing in the direction you care about.

**Scalar projection** of $\mathbf{x}$ onto $\hat{\mathbf{u}}$:

$$\text{proj\_score} = \mathbf{x} \cdot \hat{\mathbf{u}} = \sum_{i=1}^{n} x_i \hat{u}_i$$

This is a single real number. It is the signed length of the shadow.

**Vector projection** (the shadow as an actual vector, pointing along $\hat{\mathbf{u}}$):

$$\text{proj}_{\hat{\mathbf{u}}}(\mathbf{x}) = (\mathbf{x} \cdot \hat{\mathbf{u}})\,\hat{\mathbf{u}}$$

You scale the unit direction by the scalar score to get back to a vector in the original space.

> [!note] Why $\hat{\mathbf{u}}$ must be a unit vector
> If $\hat{\mathbf{u}}$ is not normalized, the formula $\mathbf{x} \cdot \mathbf{u}$ gives a score inflated by $\|\mathbf{u}\|$. Dividing by the norm fixes this: $\text{score} = \mathbf{x} \cdot \mathbf{u} / \|\mathbf{u}\|$. In practice, always normalize first.

> [!warning] Common confusion
> The scalar projection gives a **number** (how far along). The vector projection gives a **vector** (the actual shadow point). They are different objects. PCA uses the scalar projection — one number per sample per component.

> [!example] In 2D
> $\mathbf{x} = [3, 4]$, axis $\hat{\mathbf{u}} = [1, 0]$ (the $x$-axis). Score $= 3 \cdot 1 + 4 \cdot 0 = 3$. That is the $x$-coordinate. Makes sense — projecting onto the $x$-axis just reads off the first entry.

## Why this matters for PCA on IR spectra

An IR spectrum has ~1000 wavelength intensities. After PCA finds, say, 3 principal directions, each spectrum's full 1000-number fingerprint is replaced by 3 scores — one dot product per principal component. Those 3 scores are the spectrum's coordinates in the compressed representation. Plotting samples by their first two scores reveals chemical clusters invisible in the original 1000-dimensional space.

## Builds on
- [[dot-product]]
- [[vector-norm-and-distance]]

## Leads to
- [[dimensionality-reduction]]
