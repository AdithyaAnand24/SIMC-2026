---
tags:
  - simc
---

# Power method

> [!abstract] In one line
> A dead-simple repeat-until-settled algorithm: multiply by the matrix, renormalize, repeat — and the vector automatically swings to point along the strongest eigenvector.

## The idea

You need to find the eigenvector of the covariance matrix, but you don't know it. Here's the surprisingly simple trick:

1. Start with any random unit vector $\mathbf{b}$ (a random array, normalized to length 1).
2. Multiply it by the matrix $C$ (the covariance matrix).
3. The result is not a unit vector anymore — normalize it back to length 1.
4. Repeat steps 2–3 until the vector stops changing.

That's it. The vector converges to the eigenvector with the **largest** eigenvalue.

**Why does this work?** Any starting vector can be written as a mix of all the eigenvectors. Each time you multiply by $C$, every component gets scaled by its eigenvalue. The component along the biggest eigenvalue grows fastest — it dominates the others after enough multiplications. Normalizing keeps the numbers from exploding. Eventually, only the biggest-eigenvalue direction survives.

Think of it like compound interest: if you invest a mix of currencies but one currency has a 10% return and others have 1%, after 50 years almost everything is in the 10% currency regardless of how you started.

## The algorithm

**Pseudocode:**

```python
import numpy as np  # see [[numpy-basics]]

def power_method(C, num_iterations=1000):
    n = C.shape[0]
    b = np.random.randn(n)          # random starting vector
    b = b / np.linalg.norm(b)       # normalize to unit length

    for _ in range(num_iterations):
        b_new = C @ b               # matrix-vector multiply
        b = b_new / np.linalg.norm(b_new)   # renormalize

    return b   # converged to top eigenvector
```

`C @ b` is matrix-vector multiplication. `np.linalg.norm(b)` is $\|\mathbf{b}\|$.

**Convergence check** (optional but useful): if `b_new / norm(b_new)` barely changes between iterations, you're done. In practice, 100–500 iterations is usually plenty.

## Getting more than one eigenvector (deflation)

The power method as above gives only the top eigenvector. To get the 2nd, 3rd, … you use **deflation**:

1. Find eigenvector $\mathbf{v}_1$ with eigenvalue $\lambda_1$ (power method above).
2. "Remove" that direction from the matrix:
$$C_2 = C - \lambda_1 \mathbf{v}_1 \mathbf{v}_1^\top$$
3. Run power method on $C_2$ → gives $\mathbf{v}_2$ (the 2nd principal component).
4. Repeat for $C_3$, etc.

Each deflation peels off one direction. In practice, software packages (like `numpy.linalg.eigh`) do this internally — but understanding deflation is exactly what SIMC judges may ask you to explain.

> [!warning] Common confusion
> The power method finds the eigenvector with the *largest absolute eigenvalue* $|\lambda|$, not the largest positive one. For covariance matrices all eigenvalues are non-negative, so this is fine — but in general, watch out.

> [!tip] When to use this vs. full eigendecomposition
> An IR dataset might have 1000 wavelength channels, giving a $1000 \times 1000$ covariance matrix. Computing ALL 1000 eigenvectors is expensive. If you only need the top 5 principal components, running the power method 5 times (with deflation) is vastly faster. This is the practical reason PCA on large spectral data uses iterative methods.

## Why this matters for PCA on IR spectra

PCA requires finding the eigenvectors of the covariance matrix of the spectra. The power method is the conceptual engine behind every PCA solver. Understanding it means you can explain to judges exactly how the algorithm extracts chemical variation directions from 1000-channel IR data, step by step.

## Builds on
- [[matrix-vector-multiplication]]
- [[vector-norm-and-distance]]
- [[eigenvectors-and-eigenvalues]]

## Leads to
- [[rayleigh-quotient]]
- [[principal-component-analysis]]
