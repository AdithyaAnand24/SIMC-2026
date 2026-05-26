---
tags:
  - simc
---

# Diagonal covariance matrix

> [!abstract] In one line
> A diagonal covariance matrix means every feature is uncorrelated with every other — and rotating to principal component axes is exactly the operation that turns the covariance matrix diagonal.

## The idea

Start with the [[covariance-matrix]] in the original feature space. It has lots of off-diagonal entries — those non-zero covariances represent redundant information (features moving together).

Now imagine rotating your entire data cloud to a new set of axes. You want to find the *special* rotation where, in the new coordinate system, no feature correlates with any other. In that system the covariance matrix would look like this:

$$\begin{pmatrix} \lambda_1 & 0 & 0 & \cdots \\ 0 & \lambda_2 & 0 & \cdots \\ 0 & 0 & \lambda_3 & \cdots \\ \vdots & & & \ddots \end{pmatrix}$$

All off-diagonals are zero. Every new axis varies independently. The diagonal entries $\lambda_1, \lambda_2, \ldots$ are just the variances along each new axis.

**This is PCA's whole trick:** find the rotation that diagonalizes $C$. The new axes are the **principal components**; the diagonal entries of the diagonalized matrix are the **eigenvalues** of $C$, each equal to the variance captured by its principal component. The rotation itself is encoded in the **eigenvectors** of $C$ (see [[eigenvectors-of-the-covariance-matrix]]).

## The math

Let $C$ be the $p \times p$ covariance matrix. The eigendecomposition of $C$ gives:

$$C = V \Lambda V^\top$$

where:
- $V$ — $p \times p$ matrix whose columns are the eigenvectors of $C$ (the principal component directions)
- $\Lambda$ — diagonal matrix with eigenvalues $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_p \geq 0$ on the diagonal
- $V^\top$ — transpose of $V$

**The diagonal form:** When you transform the data into the PC coordinate system, the covariance matrix of the transformed data is exactly $\Lambda$:

$$\Lambda = V^\top C V$$

Each $\lambda_k$ is the **variance** of the data projected onto principal component $k$.

**No off-diagonal terms** means:
$$\mathrm{Cov}(\text{PC}_i, \text{PC}_j) = 0 \quad \text{for } i \neq j$$

The principal components are mutually uncorrelated by construction.

> [!note] Eigenvalues = variance explained
> The fraction of total variance captured by PC $k$ is:
> $$\frac{\lambda_k}{\sum_{j=1}^{p} \lambda_j}$$
> A scree plot graphs these fractions in descending order. The "elbow" tells you how many PCs to keep. This is the [[eigenspectrum]].

> [!warning] Common confusion
> Diagonal does NOT mean the features are independent in the probabilistic sense — only uncorrelated (linear independence). For Gaussian data, uncorrelated does imply independent. For IR spectra (roughly Gaussian after centering), this distinction is usually safe to ignore.

> [!tip] Why this is powerful
> Original IR data: 1000 correlated channels, most variance packed into a few correlated clusters of wavenumbers. After PCA rotation: the same information lives in ~5–20 uncorrelated principal components, most of the remaining 980+ components are noise. You just compressed a 1000-dimensional problem into a 20-dimensional one without losing the signal.

## Why this matters for PCA on IR spectra

IR spectra have massive redundancy — adjacent wavenumber channels are highly correlated (they measure overlapping parts of the same molecular vibration). The off-diagonal entries of $C$ encode this redundancy. PCA diagonalizes $C$, stripping out all the redundancy and leaving you with a small set of uncorrelated "super-features" (principal components) that each capture an independent axis of chemical variation across your sample set. The eigenvalues rank those axes by importance.

## Builds on

- [[covariance-matrix]]

## Leads to

- [[principal-component-analysis]]
