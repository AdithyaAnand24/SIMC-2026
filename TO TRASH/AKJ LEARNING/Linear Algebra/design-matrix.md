---
tags:
  - simc
---

# Design matrix

> [!abstract] In one line
> The design matrix is your data spreadsheet expressed as a single matrix $X$: each row is one sample (a vector of measurements), each column is one feature.

## The idea

Imagine your lab results loaded into a spreadsheet:

| Sample | Wavenumber 1 | Wavenumber 2 | … | Wavenumber 1000 |
|--------|-------------|-------------|---|----------------|
| Mix 1  | 0.42        | 0.87        | … | 0.11           |
| Mix 2  | 0.39        | 0.91        | … | 0.14           |
| …      | …           | …           | … | …              |
| Mix 50 | 0.55        | 0.76        | … | 0.09           |

That spreadsheet *is* the design matrix $X$. There's nothing new here — you're just giving the spreadsheet a name and treating it as a matrix so you can do math on the whole thing at once.

In Python (NumPy) terms:

```python
X = np.zeros((n, p))
# X[i, j] = absorbance of sample i at wavenumber j
# n = number of samples     (rows)
# p = number of wavenumbers (columns)
```

**Key reading:** Row $i$ of $X$ is the full spectrum of sample $i$ — a vector in $p$-dimensional space. The design matrix stacks all $n$ of those sample-vectors.

## The math

$$X = \begin{pmatrix} — \mathbf{x}_1^\top — \\ — \mathbf{x}_2^\top — \\ \vdots \\ — \mathbf{x}_n^\top — \end{pmatrix}$$

- $X$ — the design matrix, size $n \times p$
- $n$ — number of samples (rows)
- $p$ — number of features / wavenumbers (columns)
- $\mathbf{x}_i$ — the spectrum (vector) of sample $i$; it has $p$ entries
- $\top$ — the "transpose" symbol; it just means the column-vector $\mathbf{x}_i$ is laid on its side to become a row — don't worry about this yet

The entry $X_{ij}$ (row $i$, column $j$) is the absorbance of sample $i$ at wavenumber $j$.

> [!warning] Common confusion
> It's rows = samples, columns = features — NOT the other way around. Many beginners swap these. A helpful check: the number of rows $n$ is usually small (50 samples), the number of columns $p$ is large (1000 wavenumbers), so if your matrix is tall and skinny something is wrong.

> [!note] The $p \gg n$ problem
> For IR spectra you might have $n = 50$ samples but $p = 1000$ wavenumbers. Your data matrix has **more columns than rows**. This is the core difficulty: you have 1000 features but only 50 examples to learn from. Classical statistics breaks down here — you cannot even invert the necessary matrices. This mismatch is exactly why PCA (dimensionality reduction) is essential before any further analysis.

## Why this matters for PCA on IR spectra

PCA operates directly on $X$. The first step is to **mean-center** $X$ (subtract the average spectrum). Then PCA finds the directions in $p$-dimensional space along which the rows of $X$ vary the most. Those directions become the principal components. Understanding that $X$ is an $n \times p$ matrix — with each row a sample in $\mathbb{R}^p$ — makes every subsequent PCA step concrete.

## Builds on
- [[matrix]]
- [[vector]]
- [[what-is-a-dimension]]

## Leads to
- [[covariance-matrix]]
- [[principal-component-analysis]]
