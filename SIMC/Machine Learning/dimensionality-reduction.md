---
tags:
  - simc
---

# Dimensionality reduction

> [!abstract] In one line
> The actual payoff move — replace each sample's 1000 original numbers with just $k$ numbers (its coordinates along the top $k$ principal components), keeping the signal and discarding the noise directions.

## The idea

You've done all the work: centered the data, built the covariance matrix, found the eigenvectors, read the eigenspectrum, decided you need $k = 3$ components. Now what?

You take every spectrum (a vector of 1000 numbers) and re-express it in the new coordinate system defined by the top 3 PCs. Instead of saying "this spectrum has intensity 0.42 at wavelength 847 nm, 0.39 at 848 nm, ..., (997 more numbers)", you now say "this spectrum is at position $(z_1, z_2, z_3) = (2.1, -0.4, 0.9)$ in PC space."

That triple of numbers — the **scores** — is the complete, compressed description of the spectrum. And crucially: the directions you threw away (PCs 4 through 1000) were almost all noise. So you haven't just compressed — you've **denoised**.

Think of it like shadows: a 3D object casts a 2D shadow. If you choose the right light direction, the shadow captures the object's shape almost perfectly. PCA finds that optimal light direction.

## The math

### Building the projection matrix

Take the top $k$ eigenvectors $\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_k$ (each is a vector of length $p$, from [[eigenvectors-of-the-covariance-matrix]]).

Stack them as **columns** to form the **loading matrix** $W$:

$$W = \begin{pmatrix} | & | & & | \\ \mathbf{v}_1 & \mathbf{v}_2 & \cdots & \mathbf{v}_k \\ | & | & & | \end{pmatrix} \quad \text{shape: } p \times k$$

### Computing scores (the actual reduction)

For a centered sample $\mathbf{x} \in \mathbb{R}^p$ (already mean-subtracted, see [[mean-and-centering]]):

$$\mathbf{z} = W^\top \mathbf{x} \quad \in \mathbb{R}^k$$

Expanded:

$$z_i = \mathbf{v}_i \cdot \mathbf{x} = \sum_{j=1}^{p} v_{ij}\, x_j$$

Each score $z_i$ is the [[dot-product]] of the sample with the $i$-th PC direction — a [[vector-projection]] of the sample onto that axis. This is why the scores measure "how much of PC $i$ is in this sample."

For all $n$ samples at once (using the design matrix $\tilde{X}$, shape $n \times p$):

$$Z = \tilde{X} W \quad \in \mathbb{R}^{n \times k}$$

$Z$ is your compressed dataset: same $n$ samples, but $k$ features instead of $p$.

> [!note] Why $W^\top \mathbf{x}$ not $W\mathbf{x}$?
> $W$ is $p \times k$. Your sample $\mathbf{x}$ is $p \times 1$. You want a $k \times 1$ output. So you need $W^\top$ (which is $k \times p$) times $\mathbf{x}$ ($p \times 1$) = $k \times 1$. Each row of $W^\top$ is one eigenvector, dotted with $\mathbf{x}$.

### Approximate reconstruction (decompression)

You can go back to the original space (approximately):

$$\hat{\mathbf{x}} = W \mathbf{z} = W W^\top \mathbf{x}$$

If $k = p$, reconstruction is perfect (no info lost). If $k < p$, the reconstruction is the closest point to $\mathbf{x}$ in the $k$-dimensional PC subspace — it loses only the noise/redundancy directions.

**Reconstruction error** for a sample:

$$\|\mathbf{x} - \hat{\mathbf{x}}\|^2 = \sum_{i=k+1}^{p} z_i^2$$

The error equals the sum of squared scores along the discarded directions. For good PCA choices, these are tiny.

> [!warning] Common confusion
> $WW^\top$ is NOT the identity matrix (unless $k = p$). It's a projection matrix — applying it twice does the same thing as applying it once. Don't expect $\hat{\mathbf{x}} = \mathbf{x}$ when $k < p$.

> [!tip] Compression + denoising together
> Two things happen simultaneously when you keep only $k$ PCs:
> 1. **Compression**: $p$ numbers → $k$ numbers per sample.
> 2. **Denoising**: the discarded directions (small $\lambda$) capture noise and measurement error; throwing them away makes the compressed representation cleaner than the original.
> This is why PCA-preprocessed models often outperform models trained on raw data.

> [!example] Concrete numbers
> $p = 1000$ wavelengths, $k = 3$ PCs retained, $n = 200$ spectra.
> - Raw data matrix: $200 \times 1000 = 200{,}000$ numbers.
> - After reduction: $Z$ is $200 \times 3 = 600$ numbers.
> - Compression factor: 333×.
> - CVE: 97% (from the [[eigenspectrum]]).
> - Lost: 3% of variance, which was mostly detector noise.

### In code

```python
import numpy as np  # [[numpy-basics]]

# X: (n, p) raw data matrix
X_centered = X - X.mean(axis=0)          # center: [[mean-and-centering]]
C = X_centered.T @ X_centered / (n - 1)  # covariance: [[covariance-matrix]]
eigenvalues, eigenvectors = np.linalg.eigh(C)  # [[eigenvectors-of-the-covariance-matrix]]

# Sort descending
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

k = 3                          # pick from [[eigenspectrum]]
W = eigenvectors[:, :k]        # (p, k) loading matrix
Z = X_centered @ W             # (n, k) scores — DIMENSIONALITY REDUCED
X_reconstructed = Z @ W.T      # (n, p) approximate reconstruction
```

## Why this matters for PCA on IR spectra

Raw IR spectra fed into any model would drown it: 1000 correlated features, tiny training sets, [[curse-of-dimensionality]] in full force. After dimensionality reduction to $k = 3$–$10$ PCs, each spectrum becomes a short vector of uncorrelated, chemically interpretable scores. Classification models, regression (for concentration), and clustering all work dramatically better on $Z$ than on the raw $X$. This is the entire reason PCA is the default preprocessing step in chemometrics.

## Builds on
- [[principal-component-analysis]]
- [[vector-projection]]
- [[eigenspectrum]]
- [[eigenvectors-of-the-covariance-matrix]]
- [[covariance-matrix]]
- [[mean-and-centering]]
- [[dot-product]]
- [[curse-of-dimensionality]]

## Leads to
- [[pca-on-ir-spectra]]
