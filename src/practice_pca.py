"""SIMC 2026 -- Practice: PCA from scratch + power method + synthetic IR demo.

Run from the repo root:

    python src/practice_pca.py

Outputs (PNG plots + a short text log) go to data/output/practice/.

Four parts:
    A. 2-D toy data: verify the worked example from doc/CHEATSHEET.md.
    B. High-dimensional synthetic data with known rank: read the scree plot.
    C. Synthetic IR mixtures: SNV preprocessing, PCA, recover components.
    D. Noise sweep: watch the noise floor rise while signal eigenvalues stay put.

Everything uses only numpy + matplotlib so you can read the math through the code.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUT = Path("data") / "output" / "practice"


# =============================================================================
# Utilities -- the four primitives you'll re-derive over and over
# =============================================================================

def center(X: np.ndarray) -> np.ndarray:
    return X - X.mean(axis=0)


def covariance(Xc: np.ndarray) -> np.ndarray:
    M = Xc.shape[0]
    return (Xc.T @ Xc) / (M - 1)


def eig_sorted(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Eigendecompose a symmetric matrix; return (lam_desc, V_desc)."""
    lam, V = np.linalg.eigh(C)            # ascending
    order = np.argsort(lam)[::-1]
    return lam[order], V[:, order]


def power_method(
    C: np.ndarray,
    n_iter: int = 500,
    tol: float = 1e-10,
    seed: int = 0,
) -> tuple[float, np.ndarray, int]:
    """Return (lam_top, v_top, iterations_used) via the power iteration."""
    rng = np.random.default_rng(seed)
    N = C.shape[0]
    v = rng.standard_normal(N)
    v /= np.linalg.norm(v)
    lam_prev = 0.0
    for k in range(1, n_iter + 1):
        w = C @ v
        v = w / np.linalg.norm(w)
        lam = float(v @ (C @ v))
        if abs(lam - lam_prev) < tol:
            return lam, v, k
        lam_prev = lam
    return lam, v, n_iter


def snv(X: np.ndarray) -> np.ndarray:
    """Standard normal variate: row-wise mean/std normalisation. IR preprocessing."""
    mu = X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, keepdims=True)
    sd = np.where(sd == 0, 1.0, sd)
    return (X - mu) / sd


# =============================================================================
# Part A -- 2-D toy data: verify the cheat-sheet worked example
# =============================================================================

def part_a() -> None:
    print("\n=== Part A: 2-D toy data, manual PCA + power method ===")
    Xc = np.array([
        [ 2.0,  2.0],
        [-2.0, -2.0],
        [ 1.0, -1.0],
        [-1.0,  1.0],
    ])
    assert np.allclose(Xc.mean(axis=0), 0.0), "data should already be centered"

    C = covariance(Xc)
    print(f"  C =\n{C.round(4)}")
    print(f"  trace(C)  = {C.trace():.4f}    (expected 20/3 = 6.6667)")
    print(f"  det(C)    = {np.linalg.det(C):.4f}    (expected 64/9 = 7.1111)")

    lam, V = eig_sorted(C)
    print(f"  eigenvalues (desc)       = {lam.round(4)}    (expected [16/3, 4/3] = [5.3333, 1.3333])")
    print(f"  explained variance ratio = {(lam / lam.sum()).round(4)}    (expected [0.80, 0.20])")
    print(f"  PC1 = {V[:, 0].round(4)}    (expected (1, 1)/sqrt(2) ~= (0.7071, 0.7071), sign may flip)")
    print(f"  PC2 = {V[:, 1].round(4)}    (expected (1,-1)/sqrt(2))")

    # Power method on the same matrix
    lam_pm, v_pm, iters = power_method(C, seed=0)
    print(f"  power method:  lam_top = {lam_pm:.4f}, iters = {iters}")
    print(f"  |v_pm . PC1|         = {abs(v_pm @ V[:, 0]):.6f}   (should be ~1.0; sign ambiguous)")

    # Visualise
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(Xc[:, 0], Xc[:, 1], s=80, c="black", zorder=3)
    for k, color in zip(range(2), ["tab:blue", "tab:orange"]):
        v_arrow = V[:, k] * np.sqrt(lam[k]) * 1.6
        ax.annotate(
            "", xy=v_arrow, xytext=-v_arrow,
            arrowprops=dict(arrowstyle="->", color=color, lw=2),
        )
        ax.text(*(v_arrow * 1.1), f"PC{k+1}  (λ={lam[k]:.2f})",
                color=color, fontsize=11, ha="center")
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)
    ax.set_aspect("equal")
    ax.set_title("Part A: PCA of 4-point toy data")
    ax.set_xlabel("feature 1")
    ax.set_ylabel("feature 2")
    fig.tight_layout()
    fig.savefig(OUT / "A_toy_2d.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'A_toy_2d.png'}")


# =============================================================================
# Part B -- High-D synthetic data with KNOWN rank: read the scree
# =============================================================================

def part_b() -> None:
    print("\n=== Part B: high-D data with known rank, scree plot ===")
    rng = np.random.default_rng(0)
    M, N = 200, 500
    true_rank = 4

    # Build a rank-4 signal: M samples lie in a 4-d subspace of R^N.
    signal_std = np.array([5.0, 3.0, 1.5, 0.7])
    scores_true = rng.standard_normal((M, true_rank)) * signal_std
    # An orthonormal basis of the 4-d subspace, as a (N, 4) matrix.
    basis, _ = np.linalg.qr(rng.standard_normal((N, true_rank)))
    signal = scores_true @ basis.T                            # shape (M, N)
    noise = rng.standard_normal((M, N)) * 0.20
    X = signal + noise

    Xc = center(X)
    # SVD is the right tool when N > M.
    _, s, _ = np.linalg.svd(Xc, full_matrices=False)
    lam = s ** 2 / (M - 1)

    print(f"  top eigenvalues       = {lam[:8].round(4)}")
    print(f"  expected top 4 (variance of signal_std**2 = {signal_std**2}); rest = noise")
    print(f"  noise floor (median tail) = {np.median(lam[20:]):.4f}    (expected ~ 0.20**2 * N/M-ish)")
    cum = np.cumsum(lam) / lam.sum()
    targets = [0.90, 0.95, 0.99]
    cuts = [int(np.searchsorted(cum, t) + 1) for t in targets]
    print(f"  cumulative >= 90/95/99% reached at r = {cuts}")
    participation = (lam.sum() ** 2) / (lam ** 2).sum()
    print(f"  participation ratio   = {participation:.2f}    (continuous 'effective dim')")

    # Marčenko-Pastur upper edge for the noise bulk
    sigma2 = 0.20 ** 2
    mp_upper = sigma2 * (1 + np.sqrt(N / M)) ** 2
    print(f"  M-P upper edge (sigma^2*(1+sqrt(N/M))^2) = {mp_upper:.4f}")
    print(f"  -> signal eigenvalues above this edge are detectable")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(np.arange(1, 31), lam[:30], "o-")
    ax[0].set_title("Scree (linear) -- tail looks like 0")
    ax[0].set_xlabel("component k")
    ax[0].set_ylabel(r"$\lambda_k$")
    ax[1].semilogy(np.arange(1, 31), lam[:30], "o-")
    ax[1].axhline(np.median(lam[20:]), color="red", ls="--", label="noise floor")
    ax[1].axhline(mp_upper, color="purple", ls=":", label="M-P upper edge")
    ax[1].set_title("Scree (log) -- elbow at k=4")
    ax[1].set_xlabel("component k")
    ax[1].set_ylabel(r"$\lambda_k$ (log)")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "B_scree.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'B_scree.png'}")


# =============================================================================
# Part C -- Synthetic IR mixtures: SNV + PCA recovers pure components
# =============================================================================

def gaussian_peak(wavenumbers: np.ndarray, center_cm: float,
                  height: float, fwhm: float) -> np.ndarray:
    sigma = fwhm / 2.3548
    return height * np.exp(-0.5 * ((wavenumbers - center_cm) / sigma) ** 2)


def part_c() -> None:
    print("\n=== Part C: synthetic IR mixtures, PCA recovers components ===")
    wn = np.linspace(400, 4000, 1024)

    # Three fictitious pure components with distinctive bands.
    pure_A = gaussian_peak(wn, 3300, 1.0, 200) + gaussian_peak(wn, 1650, 0.6,  60)
    pure_B = gaussian_peak(wn, 1720, 0.9,  40) + gaussian_peak(wn, 2900, 0.5,  80)
    pure_C = gaussian_peak(wn, 2250, 0.8,  50) + gaussian_peak(wn, 1450, 0.4,  70)
    pure = np.stack([pure_A, pure_B, pure_C], axis=0)        # (3, N_wn)

    # Build M=80 mixtures with random concentrations summing to 1 (Dirichlet).
    M = 80
    rng = np.random.default_rng(7)
    conc = rng.dirichlet([1.0, 1.0, 1.0], size=M)            # (M, 3)
    X = conc @ pure                                           # Beer-Lambert linearity
    X = X + rng.standard_normal(X.shape) * 0.01              # measurement noise

    # Preprocessing: SNV (per-row), then mean-center (per-column).
    X_snv = snv(X)
    Xc = center(X_snv)

    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    lam = s ** 2 / (M - 1)
    evr = lam / lam.sum()
    print(f"  top 6 explained variance ratios = {evr[:6].round(4)}")
    print(f"  -> first 3 dominate (3 pure components), the rest are noise")

    # 1) Pure spectra vs the leading 3 PCs.
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    for name, p, c in zip("ABC", pure, ["tab:blue", "tab:orange", "tab:green"]):
        ax[0].plot(wn, p, color=c, label=f"pure {name}")
    ax[0].set_title("Synthetic pure IR components")
    ax[0].set_ylabel("absorbance")
    ax[0].legend()
    ax[0].invert_xaxis()                                      # IR convention

    for k in range(3):
        ax[1].plot(wn, Vt[k], label=f"PC{k+1} (evr={evr[k]:.2%})")
    ax[1].set_title("Recovered principal axes (rows of $V^T$ after SNV)")
    ax[1].set_xlabel("wavenumber ($cm^{-1}$)")
    ax[1].set_ylabel("loading")
    ax[1].invert_xaxis()
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "C_ir_components.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'C_ir_components.png'}")

    # 2) 2-D score plot, coloured by dominant pure component.
    scores = U[:, :2] * s[:2]
    dominant = conc.argmax(axis=1)
    fig, ax = plt.subplots(figsize=(6, 5))
    for k, lab in enumerate("ABC"):
        m = dominant == k
        ax.scatter(scores[m, 0], scores[m, 1],
                   label=f"dom {lab}", alpha=0.75, s=40)
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)
    ax.set_xlabel("PC1 score")
    ax.set_ylabel("PC2 score")
    ax.set_title("Part C: mixture scores (PC1 vs PC2)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "C_ir_scores.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'C_ir_scores.png'}")

    # 3) Compare WITHOUT SNV: see how preprocessing matters.
    Xc_raw = center(X)
    _, s_raw, _ = np.linalg.svd(Xc_raw, full_matrices=False)
    lam_raw = s_raw ** 2 / (M - 1)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(np.arange(1, 11), lam[:10], "o-", label="SNV + center")
    ax.semilogy(np.arange(1, 11), lam_raw[:10], "s-", label="center only")
    ax.set_xlabel("component k")
    ax.set_ylabel(r"$\lambda_k$ (log)")
    ax.set_title("Part C: preprocessing changes the eigenspectrum")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "C_preprocessing_compare.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'C_preprocessing_compare.png'}")


# =============================================================================
# Part D -- Noise sweep: signal eigvals stay put, noise floor rises
# =============================================================================

def part_d() -> None:
    print("\n=== Part D: noise level vs eigenspectrum shape ===")
    rng = np.random.default_rng(1)
    M, N = 200, 500
    rank = 3
    basis, _ = np.linalg.qr(rng.standard_normal((N, rank)))
    signal_std = np.array([4.0, 2.0, 0.8])
    scores_true = rng.standard_normal((M, rank)) * signal_std
    signal = scores_true @ basis.T

    fig, ax = plt.subplots(figsize=(7, 5))
    for sigma, color in zip([0.05, 0.20, 0.50, 1.00],
                            ["tab:blue", "tab:orange", "tab:green", "tab:red"]):
        X = signal + rng.standard_normal(signal.shape) * sigma
        Xc = center(X)
        _, s, _ = np.linalg.svd(Xc, full_matrices=False)
        lam = s ** 2 / (M - 1)
        mp_upper = (sigma ** 2) * (1 + np.sqrt(N / M)) ** 2
        ax.semilogy(np.arange(1, 31), lam[:30], "o-",
                    color=color, label=fr"$\sigma$ = {sigma}")
        ax.axhline(mp_upper, color=color, ls=":", alpha=0.5)
        print(f"  sigma={sigma}: top-3 lam = {lam[:3].round(3)},  "
              f"M-P upper edge = {mp_upper:.3f}")

    ax.set_xlabel("component k")
    ax.set_ylabel(r"$\lambda_k$ (log)")
    ax.set_title("Part D: noise floor rises with $\\sigma$; signal eigvals stay put")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "D_noise_levels.png", dpi=150)
    plt.close(fig)
    print(f"  -> {OUT / 'D_noise_levels.png'}")
    print(f"  takeaway: a signal eigenvalue must exceed the M-P upper edge "
          f"sigma^2 * (1 + sqrt(N/M))^2 to be detectable")


# =============================================================================
# Driver
# =============================================================================

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    part_a()
    part_b()
    part_c()
    part_d()
    print(f"\nDone. All outputs in {OUT.resolve()}")


if __name__ == "__main__":
    main()
