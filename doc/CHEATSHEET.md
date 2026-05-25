# SIMC 2026 — High-D / PCA / IR Cheat Sheet

Keep this open during the challenge. Everything you should not have to re-derive.

---

## 0. Conventions

- `X` is shape `(M, N)`: **M samples (rows)** × **N features (columns)**. Sklearn convention.
- "Centered" = column-mean subtracted.
- λ = eigenvalue, V = matrix of eigenvectors (as columns), Σ = covariance matrix.

---

## 1. Variance, covariance, correlation

For samples `x_1,…,x_M`:

```
mean       x̄ = (1/M) Σ x_i
variance   Var(x) = (1/(M-1)) Σ (x_i − x̄)²          ← Bessel: divide by M-1
std dev    s = √Var
covariance Cov(x, y) = (1/(M-1)) Σ (x_i − x̄)(y_i − ȳ)
correl.    ρ(x, y) = Cov(x, y) / (s_x · s_y)         ← ∈ [−1, 1]
z-score    z_i = (x_i − x̄) / s
```

---

## 2. Covariance matrix

For **centered** `X_c`:

```
C = (1 / (M − 1)) · X_cᵀ X_c         shape (N, N), symmetric, PSD
```

- `C[i,i]` = Var(feature i).
- `C[i,j]` = Cov(feature i, feature j).
- **Diagonal C** ⇔ features are linearly uncorrelated. PCA's goal: find a basis where C becomes diagonal.
- `trace(C) = Σ C[i,i] = Σ λ_k` = total variance, **invariant under rotation**.

---

## 3. Worked numeric example (memorize the mechanics)

Centered data, M=4, N=2:

```
X_c = [[ 2,  2],
       [-2, -2],
       [ 1, -1],
       [-1,  1]]
```

Column means are zero (verify). Compute `X_cᵀ X_c`:

```
[[2·2+(-2)·(-2)+1·1+(-1)·(-1),    2·2+(-2)·(-2)+1·(-1)+(-1)·1],
 [...same by symmetry...,           2·2+(-2)·(-2)+(-1)·(-1)+1·1]]
= [[10, 6],
   [ 6,10]]
```

Divide by M−1 = 3:

```
C = (1/3) · [[10, 6],
              [ 6,10]]
trace(C) = 20/3 ≈ 6.667
det(C)   = (100 − 36)/9 = 64/9
```

Characteristic equation: `λ² − trace·λ + det = 0`:

```
λ² − (20/3)λ + 64/9 = 0
Δ = (20/3)² − 4·(64/9) = 400/9 − 256/9 = 144/9
√Δ = 12/3 = 4
λ₁ = (20/3 + 4)/2 = 32/6 = 16/3 ≈ 5.333
λ₂ = (20/3 − 4)/2 =  8/6 =  4/3 ≈ 1.333
```

Eigenvectors: for `[[a,b],[b,a]]` they are `(1, 1)/√2` and `(1, −1)/√2`. Sanity-check: `[[10,6],[6,10]] @ [1,1] = [16,16] = 16·[1,1]` ✓.

Explained variance ratios:

```
evr₁ = (16/3) / (20/3) = 0.80
evr₂ = ( 4/3) / (20/3) = 0.20
```

So PC1 captures 80% of variance, PC2 captures 20%. PC1 lies along `(1,1)/√2` — the diagonal — which is exactly where the spread is largest. **This is what an eigenspectrum reading looks like in 2-D.**

---

## 4. Eigendecomposition meaning

`C = V Λ Vᵀ`, with Λ diagonal of eigenvalues.

- Columns of V = orthonormal **principal axes** in feature space.
- `λ_k` = **variance** of data projected onto axis k.
- `Σ λ_k = trace(C)` = total variance.
- Sign of `V[:,k]` is ambiguous (flip it and nothing changes).

---

## 5. PCA in code

**From-scratch (correct, slow on huge N):**
```python
Xc      = X - X.mean(axis=0)
C       = (Xc.T @ Xc) / (X.shape[0] - 1)
lam, V  = np.linalg.eigh(C)                # ASCENDING order!
lam, V  = lam[::-1], V[:, ::-1]             # → descending
scores  = Xc @ V[:, :r]                     # (M, r)
evr     = lam / lam.sum()
```

**SVD variant (preferred when N >> M, e.g. IR spectra):**
```python
Xc            = X - X.mean(axis=0)
U, s, Vt      = np.linalg.svd(Xc, full_matrices=False)
lam           = s**2 / (M - 1)              # eigenvalues of C
V             = Vt.T                         # principal axes as columns
scores        = U[:, :r] * s[:r]             # = Xc @ V[:, :r]
```

**Sklearn (most concise, auto-centers):**
```python
from sklearn.decomposition import PCA
pca    = PCA(n_components=r).fit(X)
scores = pca.transform(X)
evr    = pca.explained_variance_ratio_
V      = pca.components_                     # (r, N)  — rows are PCs, NOT cols
```

> ⚠️ sklearn's `pca.components_` has PCs as **rows**; from-scratch `V` has them as **columns**. Don't mix conventions.

---

## 6. Power method (top eigenvector of C)

```
v ← random unit vector
for K iterations:
    w ← C @ v
    v ← w / ||w||
λ₁ ≈ vᵀ C v                  ← Rayleigh quotient
```

- Converges geometrically with rate `(λ₂/λ₁)ᵏ`. Fast when leading eigenvalue dominates (typical for low-rank signal).
- For **PC2**: deflate, then repeat: `C ← C − λ₁ · v₁ v₁ᵀ`.
- Use this when you want only the top few PCs of a giant matrix without paying for a full `eigh`.

---

## 7. Reading the eigenspectrum

- **Scree plot**: λ_k vs k. **Always use a log y-axis** — linear hides the tail.
- "**Elbow**" position ≈ intrinsic dimension d̂.
- **Cumulative explained variance**: smallest r with `cumsum(evr)[r] ≥ 0.95` is a standard cutoff.
- **Participation ratio** (a continuous "effective dim"):
  ```
  PR = (Σ λ_k)² / Σ λ_k²
  ```
- **Flat tail** at level σ² = isotropic noise floor.
- **Marčenko–Pastur edges** for pure noise (M samples, N features, σ² variance):
  ```
  λ ∈ [σ²(1 − √(N/M))², σ²(1 + √(N/M))²]
  ```
  A real signal must exceed the upper edge to be detectable.

For IR spectra of mixtures, # significant PCs ≈ # pure components.

---

## 8. Curse of dimensionality — the four facts

1. **Shell concentration**: in a unit N-ball, the fraction of volume within ε of the boundary is `1 − (1−ε)ᴺ → 1`. The inside is empty.
2. **Distance concentration**: for i.i.d. points, `(max d − min d) / min d → 0`. Nearest-neighbor becomes meaningless.
3. **Volume of unit N-ball**: `V_N = πᴺᐟ² / Γ(N/2 + 1) → 0` as N→∞ (peaks at N=5).
4. **Sample density**: to maintain density you need `~kᴺ` samples. Exponential.

**Implication**: raw Euclidean KNN on full-D IR spectra (N=1000+) is unreliable. Reduce first (PCA → 10–20 dims), then KNN.

---

## 9. Manifold hypothesis

Real high-D data concentrates near a d-dim manifold M ⊂ Rᴺ with d ≪ N.

- **Linear PCA** finds the best affine M (an r-plane through the mean).
- **Nonlinear**: Isomap (geodesics), UMAP (probabilistic graph), t-SNE (KL-div on neighborhood probs), diffusion maps.
- **Intrinsic-dim estimators**: PCA elbow, Levina–Bickel MLE, correlation dim, ID-via-kNN-distance ratios.
- For IR + Beer-Lambert: mixing is linear → manifold is flat → PCA is enough; intrinsic dim ≈ # of pure components.

---

## 10. IR spectroscopy preprocessing

Apply **in this order**:

1. **Baseline correction** (asymmetric least squares "ALS", or rolling minimum) — removes drift.
2. (Optional) **Savitzky–Golay** smoothing, or 1st/2nd derivative spectrum (sharpens peaks, kills baselines).
3. **SNV** (standard normal variate) per spectrum:
   ```
   x_i ← (x_i − mean(x_i)) / std(x_i)
   ```
   Removes pathlength / scattering effects. Guard against `std == 0`.
4. **Column mean-center** across samples — this is the PCA centering.

> Do NOT z-score per column unless features are on wildly different physical scales. IR absorbances are already comparable.

---

## 11. Diagnostic IR bands (cm⁻¹)

| Band | Mode | Tells you |
|---|---|---|
| 3200–3600 | O–H, N–H stretch | alcohols, water, amines (broad) |
| 3000–3100 | =C–H, aromatic C–H | unsaturation, ring |
| 2850–3000 | aliphatic C–H | most organics |
| 2200–2260 | C≡N | nitriles |
| 2100–2260 | C≡C | alkynes |
| 1650–1750 | C=O | ester ~1735, ketone ~1715, amide ~1650 |
| 1600–1680 | C=C, aromatic ring | conjugation |
| 1500–1600 | N=O | nitro |
| < 1500 | "fingerprint" | molecular identity |

IR plots are conventionally drawn with **wavenumber decreasing left→right** (`ax.invert_xaxis()`).

---

## 12. Sanity checks (run after every step)

- `np.allclose(Xc.mean(axis=0), 0)`  ← centering worked
- `np.allclose(C, C.T)`               ← symmetric
- `(lam >= -1e-10).all()`             ← PSD
- `np.isclose(lam.sum(), C.trace())`  ← eigenvalues sum to trace
- `np.allclose(scores @ V[:, :r].T + X.mean(axis=0), X_reconstructed)`
- `np.isclose(evr.sum(), 1.0)` if r = N
- Eigenvector sign ambiguity: `V[:,k]` and `−V[:,k]` are both valid.

---

## 13. Common bugs

| Bug | Symptom | Fix |
|---|---|---|
| Forgot to center | PC1 points toward mean | Subtract `X.mean(axis=0)` |
| Divided by M not M−1 | Off by `M/(M−1)`; eigvecs OK | Use M−1 (Bessel) |
| Used `eig` not `eigh` | Unsorted, possibly complex | Always `eigh` for symmetric |
| Didn't flip eigh order | Top PC last instead of first | `lam[::-1], V[:, ::-1]` |
| Linear scree | Tail looks like zero | Use `semilogy` |
| SNV on flat row | NaN from /0 | Guard `std == 0` |
| KNN on raw high-D | Distances all ≈ equal | PCA first, then KNN |
| Mixed sklearn / from-scratch V | Off-by-transpose | sklearn = rows; from-scratch = cols |

---

## 14. Numerical sketch (memorize the shape)

For `X` shape `(M=200, N=500)` with **rank-3** signal + isotropic Gaussian noise σ:

- `λ₁, λ₂, λ₃` ≈ the three signal variances (large).
- `λ₄, …, λ_{min(M,N)}` ≈ σ² (the noise floor).
- Upper Marčenko–Pastur edge: `σ²·(1 + √(N/M))² ≈ σ²·(1+√2.5)² ≈ 6.6·σ²`.
- A signal eigenvalue must exceed this edge to be detectable.

If your scree plot shows a flat plateau at `≈ σ²` everywhere → no low-d structure, or your data is pure noise.

---

## 15. What to do in the first 10 minutes of the challenge

1. Load data; print shape, dtype, any NaNs.
2. Look at a few raw spectra (`plot_scatter` or just `plt.plot(X[:5].T)`).
3. Mean-center; check `Xc.mean(axis=0)` ≈ 0.
4. SVD: `U, s, Vt = np.linalg.svd(Xc, full_matrices=False)`.
5. Plot scree on log scale; spot the elbow.
6. Project to 2-D: `scores = U[:, :2] * s[:2]`. Scatter. Do you see clusters?
7. *Now* decide preprocessing (SNV? derivative?) and re-run.

Do not optimize before you've eyeballed the data.
