---
tags:
  - simc
---

# Dot product

> [!abstract] In one line
> Multiply two vectors entry-by-entry, add everything up, get one number that measures how much the two vectors point the same way.

## The idea

Imagine two lists of numbers — say, intensity readings at $n$ wavelengths for two different samples. The dot product is the programmer's answer to "how similar are these lists?"

```
sum = 0
for i in range(n):
    sum += a[i] * b[i]
# sum IS the dot product
```

The result is a single number (a **scalar**), not a new vector. Think of it as a similarity score:
- Big positive → both lists "go up together"
- Near zero → the lists are unrelated (perpendicular)
- Negative → when one is large, the other tends to be small

## The math

$$\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i$$

where $\mathbf{a} = [a_1, a_2, \ldots, a_n]$ and $\mathbf{b} = [b_1, b_2, \ldots, b_n]$ are two vectors of the same length.

There is a second, geometric form:

$$\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\| \, \|\mathbf{b}\| \cos\theta$$

where $\|\mathbf{a}\|$ is the length (norm) of $\mathbf{a}$, $\|\mathbf{b}\|$ is the length of $\mathbf{b}$, and $\theta$ is the angle between them.

**Key fact about $\cos\theta$:**

| Angle $\theta$ | $\cos\theta$ | Meaning |
|---|---|---|
| $0°$ | $1$ | Same direction — maximum similarity |
| $90°$ | $0$ | Perpendicular — zero similarity |
| $180°$ | $-1$ | Opposite directions |

> [!warning] Common confusion
> The dot product is NOT a vector. It is always a single number. If your calculation ends with an arrow or a list, you made a mistake.

> [!tip] Perpendicular = dot product zero
> $\mathbf{a} \cdot \mathbf{b} = 0$ means the two vectors are **orthogonal** (perpendicular). This becomes the definition of "uncorrelated directions" in PCA — the principal components are chosen so that every pair has a zero dot product with each other.

## Why this matters for PCA on IR spectra

Every covariance calculation, every projection, every eigenvalue estimate is built on dot products. When PCA finds principal components, it enforces that each new axis is orthogonal (zero dot product) to all previous ones, so no information is repeated. The dot product is also the engine of [[vector-projection]]: to find a sample's coordinate on a new axis, you compute one dot product.

## Builds on
- [[vector]]

## Leads to
- [[covariance]]
- [[vector-projection]]
- [[rayleigh-quotient]]
- [[vector-norm-and-distance]]
