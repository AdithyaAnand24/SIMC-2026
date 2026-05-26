# SIMCC 2026 — Concept Roadmap

A complete list of concepts needed for the challenge *"A Linear Algebra Guide to
the Strange Life of High-Dimensional Data"*, ordered from foundational to most
challenging. Each concept is tagged by where it is used (Q1 / Q2 / Q3).

---

## Tier 0 — Absolute foundations (everything builds on these)

- **Vectors** — a column of numbers; components, direction, and magnitude (norm) `‖v‖ = √(v·v)` *(Q1, Q2, Q3)*
- **Dot product / inner product** — `v·w`, and what it measures (similarity, projection) *(Q2, Q3)*
- **Matrices** — rectangular arrays; reading dimensions (N×M) *(all)*
- **Matrix–vector multiplication** — the `(a b; c d)(x;y)` rule *(Q1)*
- **Matrix–matrix multiplication** — `(AB)ᵢₖ = Σⱼ AᵢⱼBⱼₖ`; dimension compatibility (cols of A = rows of B) *(Q2, Q3)*
- **Transpose** — `(Aᵀ)ᵢⱼ = Aⱼᵢ`; how it flips dimensions *(Q2, Q3)*
- **Identity matrix** and **determinant** of a 2×2 (`ad − bc`) *(Q1)*
- **Linear combinations** — `c₁v₁ + c₂v₂` *(Q1)*

## Tier 1 — Eigentheory (the conceptual heart)

- **Eigenvectors & eigenvalues** — `Mv = λv`; "scaling without rotating" *(Q1, Q2, Q3)*
- **Characteristic equation** — solving `det(M − λI) = 0` *(Q1)*
- **Eigendecomposition / diagonalization** — expressing dynamics in the eigenbasis *(Q1, Q3)*
- **Orthonormal basis of eigenvectors** — `vᵢ·vⱼ = 0` for i≠j, `vᵢ·vᵢ = 1` *(Q2, Q3)*

## Tier 2 — Q1 specifics: Markov dynamics

- **Markov matrices & the Markov property** (state depends only on present) *(Q1)*
- **Conservation laws** (showing `p₁+p₂` is constant) *(Q1)*
- **Discrete-time evolution via eigenvectors** — `P(t) = c₁λ₁ᵗv₁ + c₂λ₂ᵗv₂` *(Q1)*
- **Long-time / asymptotic behavior** — dominant eigenvalue takes over (steady state) *(Q1)*
- **Time-varying parameters** — handling `ε(t) = ε₀e^(−t/t₀)`; products/sums of evolving matrices *(Q1g)*

## Tier 3 — Q2 specifics: iterative methods & SVD

- **The Power Method** — iterating `xₖ₊₁ = Xxₖ / ‖Xxₖ‖` to find the dominant eigenvector *(Q2)*
- **Proof of convergence** — expand `x₀` in the eigenbasis, show non-dominant terms decay *(Q2a)*
- **Convergence rate & the spectral gap** — residual shrinks by `|λ₂/λ₁|` per step *(Q2b)*
- **Failure when the spectral gap closes** (`|λ₁|=|λ₂|`) — non-convergence vs. mere slowness *(Q2c)*
- **Finite-precision / floating-point sensitivity** — rounding noise (~10⁻¹⁶) competing with signal *(Q2c)*
- **Symmetric matrices & the spectral theorem** — real eigenvalues, orthonormal eigenvectors *(Q2d)*
- **Positive semi-definite (PSD) matrices** — `wᵀAw ≥ 0` ⟹ non-negative eigenvalues *(Q2d)*
- **The two products `XᵀX` and `XXᵀ`** — building symmetric matrices from a rectangular one; proving they share nonzero eigenvalues *(Q2d, Q3)*
- **Singular values** `σᵢ = √λᵢ` *(Q2)*
- **Singular Value Decomposition (SVD)** — `X = UΣVᵀ`; left/right singular vectors *(Q2, Q3)*
- **Geometric picture of SVD** — rotate → stretch → rotate; unit sphere → ellipsoid *(Q2)*
- **Algorithm design / pseudocode** — writing language-agnostic Power-Method-for-SVD, choosing `XᵀX` vs `XXᵀ` by cost when N≪M *(Q2e)*

## Tier 4 — Q3 specifics: applied data analysis (PCA & clustering)

- **Design matrix** — samples (rows) × features (columns) *(Q3)*
- **Data cleaning** — detecting/removing corrupted rows (background-noise vials) and a second hidden error *(Q3a)*
- **Mean-centering** — subtracting per-feature means, and *why* (else the mean spectrum dominates) *(Q3b)*
- **Variance** — per-feature fluctuation; diagonal of the covariance matrix *(Q3b)*
- **Covariance matrix** `C = (1/Ñ)X̃ᵀX̃` — feature space *(Q3)*
- **Trace as total variance** (invariance under rotation) *(Q3b)*
- **Principal Component Analysis (PCA)** — eigendecomposition of C; eigenvalues = variance per direction *(Q3c)*
- **Eigenvalue spectrum interpretation** — signal vs. noise eigenvalues, the **elbow** `k⋆`, the `λ₁/λ₂` ratio *(Q3c)*
- **Projection onto eigenvectors** — `zᵢ = x̃ᵢ·νₖ`; dimensionality reduction to top-4 components *(Q3d, Q3e)*
- **Interpreting the leading eigenvector** in feature (frequency) space *(Q3d)*
- **Gram matrix** `G = (1/Ñ)X̃X̃ᵀ` — sample space; similarity fingerprints *(Q3f)*
- **Covariance ↔ Gram duality** — shared nonzero eigenvalues; `uᵢ = X̃vᵢ/σᵢ` *(Q3f, Q3g)*
- **Clustering & scatter-plot interpretation** — pairwise 2D projections, counting clusters *(Q3e, Q3f)*
- **Condition number & numerical conditioning** — why one of C/G gives cleaner eigenvectors *(Q3g)*

## Tier 5 — The hardest / synthesis (the "challenge" peak)

- **Connecting all three questions** — the *same* dominant-direction principle across Markov steady states, Power Method, and PCA
- **Q3h: the open-ended inference** — determining the true number of unique food samples (<100) from the spectral structure, reasoning about ~10 dominant molecules, rank, and clustering. This requires combining cleaning + PCA + clustering + scientific judgment with no formula to plug into.
- **Scientific interpretation / defense** — explaining *why* results hold (for the Q&A judges), not just computing them.

## Practical skills you'll also need (not "math concepts" but required)

- **NumPy**: loading `.npy`, `np.linalg.eigh` (vs `eig` — and why `eigh` for symmetric), matrix ops, broadcasting for mean-centering
- **Matplotlib**: line plots (variance, eigenvalue spectrum on linear + log scales, eigenvector components), scatter-plot grids with alpha/transparency
- **Jupyter notebook** workflow (the submission format)
- **Spectroscopy domain basics**: what infrared spectra represent, why molecules give "fingerprint" signatures

---

## Suggested learning order

Tier 0 → 1 → 2 (do Q1) → 3 (do Q2) → 4 (do Q3a–g) → 5 (Q3h synthesis).

Q1 and Q2 are self-contained and teach the theory; Q3 is where the bulk of the
points live (and the report should devote the most space to it, per the
instructions).
