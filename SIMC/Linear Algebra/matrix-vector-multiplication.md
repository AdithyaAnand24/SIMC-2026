---
tags:
  - simc
---

# Matrix × vector

> [!abstract] In one line
> Multiplying a matrix by a vector feeds the vector through a transformation machine — each entry of the output is one row's worth of a dot product, and geometrically the arrow gets rotated and/or stretched.

## The idea

Think of a matrix as a function:

```
input vector  →  [MATRIX]  →  output vector
```

The matrix does *something* to the input vector — it might rotate it, scale it, squish it, or flip it — and out comes a new vector. This is the "machine" reading of a matrix from the previous note.

**How the machine works mechanically:** Each row of the matrix "talks to" the input vector and produces one number for the output. Specifically, each output entry is the sum of element-wise products of one matrix row with the input vector. If you've seen the dot product, that's exactly what's happening — more on that in [[dot-product]].

## The math

Let $A$ be an $m \times n$ matrix and $\mathbf{x}$ be a vector of length $n$. The product $A\mathbf{x}$ is a vector of length $m$, where the $i$-th entry of the output is:

$$(A\mathbf{x})_i = \sum_{k=1}^{n} a_{ik}\, x_k = a_{i1}x_1 + a_{i2}x_2 + \cdots + a_{in}x_n$$

- $a_{ik}$ — entry in row $i$, column $k$ of $A$
- $x_k$ — the $k$-th entry of the input vector $\mathbf{x}$
- The output has $m$ entries (one per row of $A$)
- **Size rule:** the number of columns of $A$ must equal the length of $\mathbf{x}$

> [!example] Worked example — $2 \times 2$ times a $2$-vector
>
> $$A = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}, \quad \mathbf{x} = \begin{pmatrix} 4 \\ 5 \end{pmatrix}$$
>
> **Row 1 of output:** multiply row 1 of $A$ element-wise with $\mathbf{x}$, then sum:
> $$3 \cdot 4 + 1 \cdot 5 = 12 + 5 = 17$$
>
> **Row 2 of output:** multiply row 2 of $A$ element-wise with $\mathbf{x}$, then sum:
> $$0 \cdot 4 + 2 \cdot 5 = 0 + 10 = 10$$
>
> $$A\mathbf{x} = \begin{pmatrix} 17 \\ 10 \end{pmatrix}$$
>
> In Python (NumPy):
> ```python
> import numpy as np
> A = np.array([[3, 1], [0, 2]])
> x = np.array([4, 5])
>
> out = A @ x          # the @ operator IS matrix-vector multiplication
> # out -> array([17, 10])
>
> # the same thing spelled out as the loop above, so you see what @ hides:
> out = np.zeros(2)
> for i in range(2):
>     for k in range(2):
>         out[i] += A[i, k] * x[k]
> ```

**Geometric view:** The input vector $\mathbf{x}$ is an arrow at a certain angle and length. After multiplying by $A$, the output arrow $A\mathbf{x}$ generally points in a different direction and has a different length. The matrix *moved* the arrow.

> [!warning] Common confusion
> The column count of $A$ must equal the row count (length) of $\mathbf{x}$ — otherwise the operation is undefined. An $m \times n$ matrix eats an $n$-vector and produces an $m$-vector. If the sizes don't match, NumPy throws a shape error (`ValueError: matmul ... not aligned`).

> [!tip] Special case: eigenvectors
> For most input vectors, $A\mathbf{x}$ points in a completely different direction from $\mathbf{x}$. But there exist special vectors — called **eigenvectors** — where $A\mathbf{x}$ points in *exactly the same direction* as $\mathbf{x}$ (just scaled longer or shorter). Finding those special directions is what PCA does.

## Why this matters for PCA on IR spectra

Matrix-vector multiplication is the engine of almost every operation in PCA. The covariance matrix $C$ acts as a machine: when you feed it a direction vector $\mathbf{v}$, the output $C\mathbf{v}$ tells you how that direction is "amplified" by the data's variance structure. The eigenvectors of $C$ are the input directions where the output is just a scaled copy — those are the principal components.

## Builds on
- [[matrix]]
- [[vector]]
- [[dot-product]]

## Leads to
- [[eigenvectors-and-eigenvalues]]
- [[power-method]]
