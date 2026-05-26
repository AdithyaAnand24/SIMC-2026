---
tags:
  - simc
---

# Eigenvectors and eigenvalues

> [!abstract] In one line
> Most vectors get rotated when you push them through a matrix; eigenvectors are the special directions that come out pointing the same way — just stretched or shrunk by a factor called the eigenvalue.

## The idea

Think of a matrix as a machine that takes a vector in, transforms it, and spits a (usually different) vector out. Feed it a random arrow: it rotates AND rescales the arrow. The output points somewhere new.

But for a few magic directions, the machine only rescales — no rotation at all. The arrow goes in, and a longer (or shorter, or flipped) version of the exact same arrow comes out. Those special arrows are **eigenvectors**. The stretch factor is the **eigenvalue**.

Analogy: imagine a rubber sheet being stretched horizontally. Most arrows drawn on the sheet rotate as the sheet deforms. But an arrow pointing purely left-right just gets longer — it's an eigenvector of the stretch, with eigenvalue = the stretch ratio.

## The math

For a square matrix $A$ (same number of rows and columns), a vector $\mathbf{v}$ is an eigenvector and $\lambda$ is its eigenvalue if:

$$A\mathbf{v} = \lambda\mathbf{v}$$

- $A$ — the matrix (the transformation machine)
- $\mathbf{v}$ — eigenvector: a non-zero vector, the special direction
- $\lambda$ — eigenvalue: a scalar (just a number), the stretch factor

The equation says: "applying $A$ to $\mathbf{v}$ gives back $\mathbf{v}$ scaled by $\lambda$."

> [!example] Tiny concrete example
> Let $A = \begin{bmatrix} 3 & 0 \\ 0 & 1 \end{bmatrix}$ (stretch $x$ by 3, leave $y$ alone).
>
> Try $\mathbf{v}_1 = [1, 0]$:
> $A\mathbf{v}_1 = [3 \cdot 1 + 0 \cdot 0,\ 0 \cdot 1 + 1 \cdot 0] = [3, 0] = 3 \cdot [1, 0]$
> → eigenvector with $\lambda = 3$.
>
> Try $\mathbf{v}_2 = [0, 1]$:
> $A\mathbf{v}_2 = [0, 1] = 1 \cdot [0, 1]$
> → eigenvector with $\lambda = 1$.
>
> A random vector like $[1, 1]$ gives $[3, 1]$ — different direction, not an eigenvector.

**Key properties:**
- A matrix can have multiple eigenvectors (one per "independent direction it preserves")
- Eigenvectors can be scaled by any constant and remain eigenvectors — so we always pick the unit-length version
- The eigenvalue can be positive (same direction), negative (flipped), or even zero (collapsed)

> [!warning] Common confusion
> Eigenvectors are directions, not specific arrows. $[1, 0]$ and $[5, 0]$ are the "same" eigenvector — they point the same way. We always normalize to the unit version $[1, 0]$.

## Why this matters for PCA on IR spectra

The covariance matrix of IR data has eigenvectors that are the **principal components** — the directions of maximum spread in the data. The corresponding eigenvalues tell you exactly how much variance each direction captures. Sorting eigenvalues largest-to-smallest ranks the principal components by importance. Dropping the small ones is how PCA compresses 1000 wavelengths down to 3 or 10 dimensions.

## Builds on
- [[matrix-vector-multiplication]]

## Leads to
- [[eigenvectors-of-the-covariance-matrix]]
- [[power-method]]
