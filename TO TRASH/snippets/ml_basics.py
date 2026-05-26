"""SIMC 2026 -- Reference Snippets: ML Basics and Monte Carlo

Machine-learning primitives and Monte Carlo simulation tools.

Organisation
============

ML basics
---------
KMeans           -- partition M points into K clusters via Lloyd's algorithm;
                    returns labels, centroids, and inertia.
PCA              -- project an (M, N) matrix onto its leading r principal
                    components; returns scores, component vectors, and the
                    explained-variance ratios.
k-Nearest Neighbours -- brute-force Euclidean search returning the k closest
                    training points and their distances for each query.
Anomaly detection -- Isolation Forest scores each point with an anomaly score
                    derived from expected isolation depth; flagged outliers are
                    returned alongside the raw scores.

Monte Carlo
-----------
monte_carlo_simulate -- run a user-supplied scalar experiment R times, using a
                    shared NumPy random Generator for reproducibility; returns
                    the full result vector plus mean, std, and a 95% empirical
                    confidence interval.

Mathematical background
=======================

KMeans inertia
--------------
Lloyd's algorithm minimises the within-cluster sum of squared distances:

    W = sum_{i=1}^{M} || x_i - c_{k(i)} ||_2^2

where c_{k(i)} is the centroid of the cluster that point i was assigned to.
Lower W means tighter clusters; W is guaranteed to decrease or stay the same
on each iteration.

PCA via SVD
-----------
PCA finds the orthonormal directions v_1, ..., v_r that maximise the variance
of the projected data.  The r-th direction solves:

    max_{||v||=1, v perp v_1..v_{r-1}} Var(X v)

and can be computed as the top-r right singular vectors of the centred data
matrix X_c = X - mean(X, axis=0).  The explained variance ratio for PC k is

    rho_k = lambda_k / sum_j lambda_j

where lambda_k = sigma_k^2 / (M - 1) is the sample variance along PC k.

Monte Carlo estimation
----------------------
The Monte Carlo estimator of E[f(X)] is the sample average of R independent
realisations:

    mu_hat_R = (1/R) sum_{r=1}^{R} f(X_r).

By the law of large numbers mu_hat_R -> E[f(X)] almost surely.  The standard
error scales as sigma_f / sqrt(R), so halving the error requires four times
as many repetitions.
"""

from __future__ import annotations

from typing import Callable, NamedTuple

import numpy as np
from sklearn.cluster import KMeans as _SKLearnKMeans
from sklearn.decomposition import PCA as _SKLearnPCA
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import NearestNeighbors


# =============================================================================
# KMeans
# =============================================================================

class KMeansResult(NamedTuple):
    """Output of a KMeans fit."""
    labels:    np.ndarray   # shape (M,) -- integer cluster assignments 0..K-1
    centroids: np.ndarray   # shape (K, N) -- cluster centres
    inertia:   float        # within-cluster sum of squared distances (W)


def fit_kmeans(
    data: np.ndarray,
    n_clusters: int,
    *,
    n_init: int = 10,
    random_state: int = 0,
) -> KMeansResult:
    """Fit KMeans and return cluster labels, centroids, and inertia.

    KMeans partitions M points into K non-overlapping clusters by alternating
    between two steps until the assignments no longer change:

        1. Assignment step -- each point is assigned to its nearest centroid
           under the Euclidean metric.
        2. Update step -- each centroid is recomputed as the arithmetic mean
           of its currently assigned points.

    The algorithm is run ``n_init`` times from different random starts;
    scikit-learn uses the k-means++ seeding heuristic which places the initial
    centroids with probability proportional to their squared distance from
    already-chosen centroids, dramatically reducing the probability of
    converging to a poor local minimum.  The run with the lowest inertia W is
    retained.

    Parameters
    ----------
    data : ndarray of shape (M, N)
        The M data points in N-dimensional feature space.  Features should be
        on comparable scales; standardise with ``z_score`` from
        ``statistical_tools.py`` if they are not.
    n_clusters : int
        Number of clusters K.  Must satisfy 1 <= K <= M.
    n_init : int, optional
        Number of random initialisations; default 10.
    random_state : int, optional
        Seed for reproducible results; default 0.

    Returns
    -------
    result : KMeansResult
        Named tuple with:
        - ``labels`` -- shape (M,) integer cluster assignments.
        - ``centroids`` -- shape (K, N) cluster centres.
        - ``inertia`` -- within-cluster sum of squared distances W.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> data = np.vstack([rng.normal([0,0], 0.3, (50,2)),
    ...                   rng.normal([5,5], 0.3, (50,2))])
    >>> km = fit_kmeans(data, n_clusters=2)
    >>> len(np.unique(km.labels))
    2
    """
    km = _SKLearnKMeans(n_clusters=n_clusters, n_init=n_init, random_state=random_state)
    km.fit(data)
    return KMeansResult(
        labels=km.labels_,
        centroids=km.cluster_centers_,
        inertia=float(km.inertia_),
    )


# =============================================================================
# PCA
# =============================================================================

class PCAResult(NamedTuple):
    """Output of a PCA projection."""
    scores:                   np.ndarray  # shape (M, r) -- projected coordinates
    components:               np.ndarray  # shape (r, N) -- principal axes (row vectors)
    explained_variance_ratio: np.ndarray  # shape (r,) -- fraction of variance per PC


def fit_pca(data: np.ndarray, n_components: int) -> PCAResult:
    """Project data onto its leading r principal components.

    The first principal component PC1 is the unit vector that maximises the
    variance of the projected data.  PC2 is orthogonal to PC1 and maximises
    the remaining variance; and so on.  The projection is computed via the
    SVD of the column-centred data matrix, which is numerically stable for
    tall matrices (M >> N).

    The ``scores`` array has shape (M, r): row i is the r-dimensional
    representation of observation i.  The ``components`` array has shape
    (r, N): row k is the k-th principal axis expressed in the original
    feature basis; it has unit Euclidean norm.

    Parameters
    ----------
    data : ndarray of shape (M, N)
        Observation matrix; rows are samples, columns are features.  Column
        centering is applied automatically inside scikit-learn.
    n_components : int
        Number of principal components r to retain; must satisfy
        1 <= r <= min(M, N).

    Returns
    -------
    result : PCAResult
        Named tuple with ``scores`` (M, r), ``components`` (r, N), and
        ``explained_variance_ratio`` (r,) summing to at most 1.

    Examples
    --------
    >>> pca = fit_pca(np.eye(4), n_components=2)
    >>> pca.scores.shape
    (4, 2)
    >>> pca.explained_variance_ratio.sum() <= 1.0
    True
    """
    pca = _SKLearnPCA(n_components=n_components)
    scores = pca.fit_transform(data)
    return PCAResult(
        scores=scores,
        components=pca.components_,
        explained_variance_ratio=pca.explained_variance_ratio_,
    )


# =============================================================================
# k-Nearest Neighbours
# =============================================================================

class KNNResult(NamedTuple):
    """Output of a k-nearest-neighbour search."""
    distances: np.ndarray   # shape (Q, k) -- Euclidean distances, sorted ascending
    indices:   np.ndarray   # shape (Q, k) -- row indices into the training set


def knn_search(
    train: np.ndarray,
    queries: np.ndarray,
    k: int,
    *,
    algorithm: str = "auto",
) -> KNNResult:
    """Find the k nearest training points for each query point.

    Uses the Euclidean (L2) metric.  The ``"auto"`` algorithm selector chooses
    between brute force, KD-tree, and ball tree based on the number of samples
    and features.  For N > 20 features KD-tree and ball tree degrade toward
    brute force due to the curse of dimensionality; brute force is fastest
    for N > ~20 on modern hardware.

    The query points need not belong to the training set -- this function is
    therefore useful for both self-searches (e.g. computing each point's
    k-th-neighbour distance for outlier scoring) and cross-searches (e.g.
    propagating labels from a labelled corpus to an unlabelled query set by
    majority vote).

    Parameters
    ----------
    train : ndarray of shape (M, N)
        The corpus of reference points.
    queries : ndarray of shape (Q, N)
        Points for which neighbours are sought.
    k : int
        Number of neighbours to return per query; must satisfy 1 <= k <= M.
    algorithm : str, optional
        One of ``"auto"``, ``"brute"``, ``"kd_tree"``, ``"ball_tree"``;
        default ``"auto"``.

    Returns
    -------
    result : KNNResult
        Named tuple with:
        - ``distances`` -- shape (Q, k), sorted in ascending order.
        - ``indices``   -- shape (Q, k), corresponding row indices into ``train``.

    Examples
    --------
    >>> train = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    >>> result = knn_search(train, np.array([[0.1, 0.1]]), k=2)
    >>> result.indices[0]   # two closest points to (0.1, 0.1)
    array([0, 1])
    """
    nn = NearestNeighbors(n_neighbors=k, algorithm=algorithm)
    nn.fit(train)
    distances, indices = nn.kneighbors(queries)
    return KNNResult(distances=distances, indices=indices)


# =============================================================================
# Anomaly detection (Isolation Forest)
# =============================================================================

class AnomalyResult(NamedTuple):
    """Output of the Isolation Forest anomaly detector."""
    scores:     np.ndarray   # shape (M,) -- anomaly score in [-1, 0]; lower = more anomalous
    is_anomaly: np.ndarray   # shape (M,) -- bool; True where the model predicts an outlier
    labels:     np.ndarray   # shape (M,) -- int; +1 inlier, -1 outlier


def detect_anomalies(
    data: np.ndarray,
    *,
    contamination: float = 0.05,
    random_state: int = 0,
) -> AnomalyResult:
    """Score each point with an Isolation Forest and flag the most anomalous.

    The Isolation Forest isolates observations by recursively partitioning
    the data with random axis-aligned splits.  Anomalies have fewer nearby
    points and are isolated in fewer splits on average; they therefore receive
    shorter average path lengths and lower anomaly scores.  The score is
    monotonically related to the negative of the expected isolation depth,
    normalised so that:

        score ~ -1   -->  typical outlier (very easy to isolate)
        score ~  0   -->  typical inlier  (hard to isolate)

    The ``contamination`` parameter sets the fraction of the training data
    that the decision boundary labels as anomalies.  It acts as the quantile
    threshold on the score distribution.  Set it to the expected prevalence
    of outliers if known; otherwise 0.05 (5 percent) is a conservative default.

    Parameters
    ----------
    data : ndarray of shape (M, N)
        The M observations in N-dimensional feature space.
    contamination : float, optional
        Expected outlier fraction in (0, 0.5); default 0.05.
    random_state : int, optional
        Seed for reproducibility; default 0.

    Returns
    -------
    result : AnomalyResult
        Named tuple with:
        - ``scores``     -- shape (M,), raw anomaly scores in [-1, 0].
        - ``is_anomaly`` -- shape (M,) bool, True for predicted outliers.
        - ``labels``     -- shape (M,) int, +1 = inlier, -1 = outlier.
    """
    iso = IsolationForest(contamination=contamination, random_state=random_state)
    iso.fit(data)
    labels = iso.predict(data)          # +1 = inlier, -1 = outlier
    scores = iso.score_samples(data)    # raw anomaly score in [-1, 0]
    return AnomalyResult(
        scores=scores,
        is_anomaly=(labels == -1),
        labels=labels,
    )


# =============================================================================
# Monte Carlo engine
# =============================================================================

class MonteCarloResult(NamedTuple):
    """Summary of a Monte Carlo simulation."""
    results:  np.ndarray   # shape (R,) -- all scalar outcomes
    mean:     float        # E[f(X)] estimate = (1/R) sum f(X_r)
    std:      float        # standard deviation of the outcomes (ddof=1)
    lower_ci: float        # 2.5th percentile of outcomes (95% empirical CI)
    upper_ci: float        # 97.5th percentile of outcomes


def monte_carlo_simulate(
    experiment: Callable[[np.random.Generator], float],
    n_repeats: int,
    *,
    seed: int = 0,
) -> MonteCarloResult:
    """Run a scalar experiment R times and summarise the distribution of outcomes.

    The Monte Carlo estimator approximates E[f(X)] by the sample mean of R
    independent realisations of the random variable f(X):

        mu_hat_R = (1/R) sum_{r=1}^{R} f(X_r)  -->  E[f(X)]  as R -> inf.

    The standard error of the estimate is sigma_f / sqrt(R), so increasing
    precision by a factor of 2 requires four times as many repetitions.  A
    rough rule of thumb: R = 10,000 gives two significant figures; R = 1,000,000
    gives three.

    The caller provides a Python callable ``experiment(rng) -> float`` that
    accepts a NumPy Generator and returns a single scalar outcome.  Ownership
    of the Generator stays with the engine so that successive calls draw from
    the same stream and each repeat is independent and reproducible.

    Parameters
    ----------
    experiment : callable (numpy.random.Generator) -> float
        A function accepting a NumPy Generator and returning a scalar outcome.
        The Generator must be the sole source of randomness inside the function
        so the engine can guarantee reproducibility.
    n_repeats : int
        Number of independent repetitions R.
    seed : int, optional
        Master seed for the random Generator; default 0.

    Returns
    -------
    result : MonteCarloResult
        Named tuple with:
        - ``results``  -- shape (R,), all raw outcomes.
        - ``mean``     -- Monte Carlo estimate of E[f(X)].
        - ``std``      -- sample standard deviation of the outcomes (ddof=1).
        - ``lower_ci`` -- 2.5th percentile (lower bound of 95% empirical CI).
        - ``upper_ci`` -- 97.5th percentile (upper bound of 95% empirical CI).

    Examples
    --------
    Estimate pi via the classical dart-board method (quarter-circle in the
    unit square):

    >>> def estimate_pi(rng):
    ...     xy = rng.random((10_000, 2))
    ...     return 4.0 * ((xy**2).sum(axis=1) <= 1.0).mean()
    >>> result = monte_carlo_simulate(estimate_pi, n_repeats=500, seed=0)
    >>> abs(result.mean - 3.14159) < 0.05
    True
    """
    rng = np.random.default_rng(seed)
    outcomes = np.array([experiment(rng) for _ in range(n_repeats)], dtype=float)
    return MonteCarloResult(
        results=outcomes,
        mean=float(outcomes.mean()),
        std=float(outcomes.std(ddof=1)),
        lower_ci=float(np.percentile(outcomes, 2.5)),
        upper_ci=float(np.percentile(outcomes, 97.5)),
    )


# =============================================================================
# Driver
# =============================================================================

def main() -> None:
    """Demonstrate each function on synthetic data.

    Three well-separated Gaussian blobs are generated so that KMeans and PCA
    have non-trivial structure to discover.  Ten obvious outliers are appended
    for the anomaly detector.  The Monte Carlo section estimates pi via the
    dart-board method and demonstrates the 1/sqrt(R) convergence of the error.
    """
    rng = np.random.default_rng(seed=99)

    # Three Gaussian blobs in 2-D, 150 points each.
    data = np.vstack([
        rng.normal([0.0, 0.0], 0.5, size=(150, 2)),
        rng.normal([5.0, 0.0], 0.5, size=(150, 2)),
        rng.normal([2.5, 4.0], 0.5, size=(150, 2)),
    ])  # shape (450, 2)

    # -------------------------------------------------------------------------
    # 1. KMeans
    # -------------------------------------------------------------------------
    km = fit_kmeans(data, n_clusters=3)
    print("KMeans")
    print(f"  inertia              = {km.inertia:.2f}")
    print(f"  label distribution   = {np.bincount(km.labels)}")
    print(f"  centroid[0]          = {km.centroids[0].round(3)}")

    # -------------------------------------------------------------------------
    # 2. PCA
    # -------------------------------------------------------------------------
    pca = fit_pca(data, n_components=2)
    print("\nPCA")
    print(f"  explained var ratio  = {pca.explained_variance_ratio.round(4)}")
    print(f"  total variance explained = {pca.explained_variance_ratio.sum():.4f}")
    print(f"  PC1 direction        = {pca.components[0].round(4)}")

    # -------------------------------------------------------------------------
    # 3. k-Nearest Neighbours
    # -------------------------------------------------------------------------
    # Query the 5 nearest neighbours for two hand-picked query points.
    queries = np.array([[0.0, 0.0], [5.0, 0.0]])
    knn = knn_search(data, queries, k=5)
    print("\nk-Nearest Neighbours (k=5)")
    for q_idx, q in enumerate(queries):
        print(f"  query {q}: distances = {knn.distances[q_idx].round(3)}")

    # -------------------------------------------------------------------------
    # 4. Anomaly detection
    # -------------------------------------------------------------------------
    # Inject 10 points far from the main blobs.
    outliers = rng.uniform(-15, 15, size=(10, 2))
    data_with_outliers = np.vstack([data, outliers])
    anomaly = detect_anomalies(data_with_outliers, contamination=0.02)
    n_flagged = anomaly.is_anomaly.sum()
    injected_flagged = anomaly.is_anomaly[450:].sum()
    print("\nAnomaly detection (contamination=0.02)")
    print(f"  total flagged        = {n_flagged}")
    print(f"  injected outliers flagged = {injected_flagged} / 10")

    # -------------------------------------------------------------------------
    # 5. Monte Carlo -- estimate pi via the quarter-circle dart-board method
    # -------------------------------------------------------------------------
    # A dart landing uniformly in [0,1)^2 falls inside the quarter-circle of
    # radius 1 centred at the origin with probability pi/4. Averaging over N
    # darts and multiplying by 4 gives an estimate of pi.
    def estimate_pi(generator: np.random.Generator) -> float:
        n_darts = 10_000
        xy = generator.random((n_darts, 2))
        inside = (xy ** 2).sum(axis=1) <= 1.0
        return 4.0 * inside.mean()

    mc = monte_carlo_simulate(estimate_pi, n_repeats=300, seed=42)
    print("\nMonte Carlo -- pi estimate (300 repeats x 10,000 darts each)")
    print(f"  estimate             = {mc.mean:.5f}  (true pi = {np.pi:.5f})")
    print(f"  standard deviation   = {mc.std:.5f}")
    print(f"  95% empirical CI     = [{mc.lower_ci:.5f}, {mc.upper_ci:.5f}]")
    print(f"  error                = {abs(mc.mean - np.pi):.5f}")


if __name__ == "__main__":
    main()
