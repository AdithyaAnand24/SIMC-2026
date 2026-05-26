---
tags:
  - simc
---

# Matrix

> [!abstract] In one line
> A matrix is a rectangular grid of numbers — a NumPy 2-D array (a list of lists) — and you can read it three ways: a table of data, a stack of vectors, or a machine that transforms vectors.

## The idea

In Python (NumPy):

```python
import numpy as np
A = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
])
# A.shape == (2, 3)  →  2 rows, 3 columns
```

That is a matrix. Nothing more exotic than a 2-D array.

**Three lenses — same object, different uses:**

1. **A table of data.** Rows are observations, columns are variables. Exactly like a spreadsheet.

2. **A stack of vectors.** Each row `A[i]` is a row-vector. Each column is a column-vector. You can think of the matrix as either "rows stacked on top of each other" or "columns placed side by side."

3. **A transformation machine.** Feed a vector in, get a (possibly different) vector out. This is the key lens for understanding eigenvectors and PCA. The matrix rotates, stretches, or squishes the input vector to produce the output.

## The math

A matrix with $m$ rows and $n$ columns is called an $m \times n$ matrix (read "m by n"):

$$A = \begin{pmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{pmatrix}$$

- $A$ — the matrix (uppercase bold or just uppercase = convention)
- $a_{ij}$ — the entry in row $i$, column $j$ (row index first, always)
- $m$ — number of rows
- $n$ — number of columns

**Python translation:** `A[i-1, j-1]` in NumPy is $a_{ij}$ in math (Python is 0-indexed; math is 1-indexed).

**Special cases:**
- $m = n$: a **square matrix** — same number of rows and columns
- $m = 1$: a single row — equivalent to a row-vector
- $n = 1$: a single column — equivalent to a column-vector

> [!warning] Common confusion
> "$m \times n$" means **rows × columns** — rows come first. It's easy to flip. When someone says "a $3 \times 5$ matrix," they mean 3 rows and 5 columns, like a NumPy array of shape `(3, 5)`.

> [!example] Reading the indices
> $a_{23}$ means row 2, column 3 — the entry `A[1, 2]` in NumPy (0-indexed).

## Why this matters for PCA on IR spectra

Your entire IR dataset is stored as one matrix: rows = samples, columns = wavenumber readings. The covariance matrix (a square matrix derived from the data) is the object PCA actually decomposes. The transformation-machine view of matrices explains why multiplying a matrix by a vector changes the vector's direction — which is exactly what eigenvectors capture.

## Builds on
- [[vector]]

## Leads to
- [[design-matrix]]
- [[matrix-vector-multiplication]]
- [[covariance-matrix]]
