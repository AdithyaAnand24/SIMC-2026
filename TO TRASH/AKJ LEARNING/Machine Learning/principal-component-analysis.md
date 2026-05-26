---
tags:
  - simc
---

# Principal Component Analysis (PCA)

> [!abstract] In one line
> PCA finds the few directions your data actually spreads along, rotates onto them, and throws away the rest — turning a 1000-number IR sample into a handful of meaningful numbers while keeping almost all the information.

## The idea

Imagine you're tracking a room full of people and every person carries 1000 sensors. Most of those sensors are picking up the same underlying story — temperature, humidity, movement — because reality has far fewer "degrees of freedom" than sensors. PCA asks: **what are the real axes of variation?**

Think of it as finding the best camera angles. If a cloud of data points looks like a flattened pancake floating in 3D space, there's one direction the pancake is thin in (barely any spread → throw it away) and two directions it's wide in (lots of spread → keep them). PCA finds those wide directions automatically, then re-describes every point using only them.

The key insight: **variance = information**. The directions where your data varies the most are the directions that actually distinguish one sample from another. The directions with near-zero variance are noise or redundancy.

This is the **linear** way to find the [[manifold-hypothesis|low-dimensional manifold]] your data lives on. If the manifold is curved, you need nonlinear methods. If it's (approximately) flat — which IR spectra often are — PCA nails it.

## The math: full pipeline

### Step 1 — Center the data

Subtract the mean spectrum from every sample. See [[mean-and-centering]].

$$\tilde{\mathbf{x}}_i = \mathbf{x}_i - \bar{\mathbf{x}}$$

Without centering, the first PC would just point at the mean, not the interesting variation.

### Step 2 — Build the covariance matrix

From your centered $n \times p$ [[design-matrix]] $\tilde{X}$, compute the $p \times p$ [[covariance-matrix]]:

$$C = \frac{1}{n-1}\tilde{X}^\top \tilde{X}$$

Entry $C_{ij}$ = how much wavelength $i$ and wavelength $j$ move together across samples. The diagonal entries are the [[variance]] of each individual wavelength.

### Step 3 — Find the eigenvectors and eigenvalues of $C$

This is the computational heart. See [[eigenvectors-of-the-covariance-matrix]].

$$C\mathbf{v}_k = \lambda_k \mathbf{v}_k$$

- $\mathbf{v}_k$ is the $k$-th **principal component** (a direction in the original $p$-dimensional space, a vector of length $p$)
- $\lambda_k$ is the corresponding **eigenvalue** = the amount of variance captured in that direction

The eigenvectors of the covariance matrix are always **orthogonal** (perpendicular to each other) and can be chosen to be unit length. They form a new coordinate system.

For ALL components: full eigendecomposition (e.g. `numpy.linalg.eig`).
For just the TOP few: [[power-method]] — faster when $p$ is large (like 1000 wavelengths).

### Step 4 — Rank by eigenvalue

Sort eigenvectors so $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p$.

**Critical fact:** in this new coordinate system (the PC basis), the covariance matrix is exactly diagonal. Off-diagonal terms vanish — the PCs are uncorrelated by construction. See [[diagonal-covariance-matrix]].

$$C_{\text{PC basis}} = \begin{pmatrix} \lambda_1 & 0 & \cdots \\ 0 & \lambda_2 & \cdots \\ \vdots & & \ddots \end{pmatrix}$$

### Step 5 — Project and reduce

Pick the top $k$ components. [[vector-projection|Project]] every sample onto them. This gives each sample a new, short description. See [[dimensionality-reduction]] for the full projection math.

## Key vocabulary

| Term | Plain English | Math |
|---|---|---|
| **Loadings** | The PC directions themselves — which wavelengths "load onto" this component | Eigenvectors $\mathbf{v}_1, \mathbf{v}_2, \dots$ |
| **Scores** | A sample's coordinates in PC space — its new short description | $z_{ik} = \tilde{\mathbf{x}}_i \cdot \mathbf{v}_k$ |
| **Explained variance** | How much of total data spread each PC captures | $\lambda_k / \sum_j \lambda_j$ |

Scores are what you run statistics on. Loadings are what you interpret (which wavelengths drive each PC).

> [!warning] Common confusion
> PCA doesn't "throw away data points" — it keeps ALL samples. It throws away **dimensions** (directions). Each sample still gets described, just with $k$ numbers instead of $p$.

> [!tip] The rotation picture
> PCA is literally a rotation of your coordinate axes so the new axes align with the directions of maximum variance. No data is distorted — it's a rigid rotation, not a stretch.

> [!example] Toy IR example
> You have 50 spectra, each with 1000 wavelength intensities. After PCA you find the first 3 PCs explain 95% of variance. Now each spectrum is just 3 numbers (its scores). You've gone from a $50 \times 1000$ matrix to a $50 \times 3$ matrix — same 50 samples, just 3 features instead of 1000.

## Why this matters for PCA on IR spectra

IR spectra have ~1000 wavelength channels but most variation comes from a handful of chemical factors (concentration of compound A, temperature, baseline drift, etc.). PCA extracts these underlying chemical signals as PCs. The loadings show WHICH wavelengths define each chemical factor; the scores show HOW MUCH of each factor each sample contains. This is why PCA is the standard first move in chemometrics.

## Builds on
- [[covariance-matrix]]
- [[eigenvectors-of-the-covariance-matrix]]
- [[power-method]]
- [[diagonal-covariance-matrix]]
- [[manifold-hypothesis]]
- [[mean-and-centering]]
- [[vector-projection]]
- [[design-matrix]]
- [[variance]]

## Leads to
- [[eigenspectrum]]
- [[dimensionality-reduction]]
- [[pca-on-ir-spectra]]
