"""SIMC 2026 -- Reference Snippets: Statistical Tools

Core statistical routines: descriptive summaries, z-score normalisation,
confidence intervals for the mean, and normal-distribution fitting.  Every
function operates on a NumPy array and returns either a scalar, an ndarray,
or a NamedTuple so that fields can be accessed by name rather than by position.

Mathematical background
=======================

Descriptive statistics
-----------------------
Given a sample x = (x_1, ..., x_N) the canonical summaries are:

    sample mean         x_bar = (1/N) sum_i x_i
    sample std          s     = sqrt( (1/(N-1)) sum_i (x_i - x_bar)^2 )

The N-1 denominator (Bessel's correction) gives the unbiased estimator of the
population variance; use ``ddof=0`` for the MLE / population estimator.

Z-score normalisation
---------------------
The z-score standardises each observation relative to the sample mean and
standard deviation:

    z_i = (x_i - x_bar) / s

After transformation the sample has mean 0 and standard deviation 1 (not
exactly unit-normal in distribution -- that requires the population parameters
-- but the moments are exact for the sample).

Confidence interval for the mean
----------------------------------
For an unknown population variance the exact t-interval is

    CI = x_bar +/- t_{alpha/2, N-1} * s / sqrt(N)

where t_{alpha/2, N-1} is the upper alpha/2 quantile of the t-distribution
with N-1 degrees of freedom.  For N >= 30 this is numerically close to the
z-interval (t -> z as N -> inf), but the t-interval is exact for normally
distributed data at any sample size.

Normal distribution fitting
----------------------------
The method-of-moments / MLE estimators for the Gaussian family are:

    mu_hat    = x_bar          (sample mean)
    sigma_hat = s              (sample std, ddof=1)

After fitting, a Kolmogorov--Smirnov (KS) test against Normal(mu_hat, sigma_hat)
is performed.  A large p-value (> 0.05) is consistent with normality; a small
p-value suggests the data are non-Gaussian.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from scipy import stats


# =============================================================================
# Descriptive statistics
# =============================================================================

class DescriptiveStats(NamedTuple):
    """Descriptive summary of a 1-D sample."""
    mean:   float
    std:    float
    minimum: float
    maximum: float
    median: float
    n:      int


def describe(sample: np.ndarray) -> DescriptiveStats:
    """Compute mean, standard deviation, range, median, and count of a sample.

    The standard deviation uses the unbiased (Bessel-corrected) divisor N-1.
    Non-finite values in ``sample`` are included in the computation and will
    propagate to the output; filter them with ``sample[np.isfinite(sample)]``
    beforehand if that is undesirable.

    Parameters
    ----------
    sample : ndarray of any shape
        The observations.  Multi-dimensional arrays are flattened to 1-D
        before computing any statistic.

    Returns
    -------
    stats : DescriptiveStats
        Named tuple with fields ``mean``, ``std``, ``minimum``, ``maximum``,
        ``median``, and ``n`` (sample size after flattening).

    Examples
    --------
    >>> desc = describe(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    >>> desc.mean
    3.0
    >>> desc.std
    1.5811388300841898
    """
    x = sample.ravel().astype(np.float64)
    return DescriptiveStats(
        mean=float(x.mean()),
        std=float(x.std(ddof=1)),
        minimum=float(x.min()),
        maximum=float(x.max()),
        median=float(np.median(x)),
        n=int(x.size),
    )


# =============================================================================
# Z-score
# =============================================================================

def z_score(sample: np.ndarray, *, ddof: int = 1) -> np.ndarray:
    """Standardise a sample to zero mean and unit standard deviation.

    Each observation is transformed by

        z_i = (x_i - mean(x)) / std(x, ddof=ddof).

    With ``ddof=1`` (default) the denominator is the unbiased sample standard
    deviation; with ``ddof=0`` it is the population (MLE) estimator, which is
    appropriate when ``sample`` is the entire population.

    If the standard deviation is zero (constant input), the function raises a
    ``ValueError`` rather than silently returning ``nan`` or ``inf``, because
    a constant sample carries no information that can be meaningfully
    standardised.

    Parameters
    ----------
    sample : ndarray of shape (N,) or any shape
        Observations to standardise.  Multi-dimensional arrays are flattened
        to 1-D; the returned array has shape ``(sample.size,)``.
    ddof : int, optional
        Delta degrees of freedom for the standard deviation; default 1.

    Returns
    -------
    z : ndarray of shape (sample.size,), dtype float64
        The standardised sample with mean 0 and standard deviation 1.

    Raises
    ------
    ValueError
        If the computed standard deviation is zero.

    Examples
    --------
    >>> z = z_score(np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]))
    >>> z.mean()   # doctest: +ELLIPSIS
    0.0
    >>> z.std(ddof=1)
    1.0
    """
    x = sample.ravel().astype(np.float64)
    mu = x.mean()
    sigma = x.std(ddof=ddof)
    if sigma == 0.0:
        raise ValueError(
            "z_score: sample standard deviation is zero -- cannot standardise a constant sample."
        )
    return (x - mu) / sigma


# =============================================================================
# Confidence interval for the mean
# =============================================================================

class ConfidenceInterval(NamedTuple):
    """Two-sided confidence interval for the population mean."""
    lower:            float
    upper:            float
    centre:           float   # sample mean = point estimate
    confidence_level: float
    n:                int


def confidence_interval_mean(
    sample: np.ndarray,
    *,
    confidence: float = 0.95,
) -> ConfidenceInterval:
    """Compute the two-sided t-interval for the population mean.

    Uses the Student-t distribution with N-1 degrees of freedom.  This is
    the exact interval when the population is normally distributed and the
    variance is unknown.  For N >= 30 the difference from the z-interval
    (which assumes known variance) is negligible.

    The half-width of the interval is

        h = t_{alpha/2, N-1} * s / sqrt(N),

    where alpha = 1 - confidence, s is the sample standard deviation (ddof=1),
    and t_{alpha/2, N-1} is the upper alpha/2 quantile of t(N-1).

    Parameters
    ----------
    sample : ndarray of shape (N,)
        The 1-D observations.  Flattened to 1-D if multi-dimensional.
    confidence : float, optional
        Coverage probability in (0, 1); default 0.95 for a 95 percent
        two-sided interval.

    Returns
    -------
    ci : ConfidenceInterval
        Named tuple with ``lower``, ``upper``, ``centre`` (sample mean),
        ``confidence_level``, and ``n``.

    Raises
    ------
    ValueError
        If the sample has fewer than 2 observations (degrees of freedom = 0).

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> ci = confidence_interval_mean(rng.normal(0, 1, 100))
    >>> ci.lower < 0 < ci.upper   # zero should be inside the 95% CI
    True
    """
    x = sample.ravel().astype(np.float64)
    n = x.size
    if n < 2:
        raise ValueError(
            "confidence_interval_mean: need at least 2 observations (got {n})."
        )
    mean = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    # scipy.stats.t.interval returns (lower, upper) centred on `loc` with
    # standard error `scale` for the given coverage level.
    lower, upper = stats.t.interval(confidence, df=n - 1, loc=mean, scale=se)
    return ConfidenceInterval(
        lower=float(lower),
        upper=float(upper),
        centre=float(mean),
        confidence_level=confidence,
        n=n,
    )


# =============================================================================
# Normal distribution fitting
# =============================================================================

class NormalFit(NamedTuple):
    """Parameters and goodness-of-fit for a fitted normal distribution."""
    mu:           float   # estimated mean
    sigma:        float   # estimated standard deviation (ddof=1)
    ks_statistic: float   # Kolmogorov--Smirnov test statistic D_N
    ks_p_value:   float   # asymptotic p-value for H_0: data ~ Normal(mu, sigma)


def fit_normal(sample: np.ndarray) -> NormalFit:
    """Fit a normal distribution to a sample by the method of moments.

    The method-of-moments estimators are:

        mu_hat    = sample mean
        sigma_hat = sample standard deviation (ddof=1)

    These coincide with the MLEs for the Gaussian family (up to the ddof=1
    vs ddof=0 distinction in sigma; the difference is O(1/N) and negligible
    for N >> 1).

    A one-sample Kolmogorov--Smirnov test is performed against the fitted
    Normal(mu_hat, sigma_hat).  The KS statistic D_N = max_x |F_N(x) - F(x)|
    measures the largest discrepancy between the empirical CDF F_N and the
    fitted Gaussian CDF F.  A large p-value is consistent with normality; a
    small p-value (< 0.05) suggests the data deviate significantly from the
    fitted Gaussian.

    Note: the KS p-value uses asymptotic tables and can be anti-conservative
    when the parameters are estimated from the data rather than specified a
    priori.  For rigorous testing prefer the Lilliefors correction or a
    bootstrap.

    Parameters
    ----------
    sample : ndarray of shape (N,)
        The 1-D observations.

    Returns
    -------
    fit : NormalFit
        Named tuple with ``mu``, ``sigma``, ``ks_statistic``, and
        ``ks_p_value``.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> fit = fit_normal(rng.normal(3.0, 1.5, 500))
    >>> abs(fit.mu - 3.0) < 0.2
    True
    >>> fit.ks_p_value > 0.05   # should not reject H_0
    True
    """
    x = sample.ravel().astype(np.float64)
    mu = float(x.mean())
    sigma = float(x.std(ddof=1))
    ks_stat, ks_p = stats.kstest(x, "norm", args=(mu, sigma))
    return NormalFit(
        mu=mu,
        sigma=sigma,
        ks_statistic=float(ks_stat),
        ks_p_value=float(ks_p),
    )


# =============================================================================
# Driver
# =============================================================================

def main() -> None:
    """Run each statistical function on a synthetic normally-distributed sample."""
    rng = np.random.default_rng(seed=7)
    sample = rng.normal(loc=5.0, scale=2.0, size=500)

    # -------------------------------------------------------------------------
    # 1. Descriptive statistics
    # -------------------------------------------------------------------------
    desc = describe(sample)
    print("Descriptive statistics")
    print(f"  n      = {desc.n}")
    print(f"  mean   = {desc.mean:.4f}  (expected 5.0)")
    print(f"  std    = {desc.std:.4f}   (expected 2.0)")
    print(f"  min    = {desc.minimum:.4f}")
    print(f"  median = {desc.median:.4f}")
    print(f"  max    = {desc.maximum:.4f}")

    # -------------------------------------------------------------------------
    # 2. Z-score
    # -------------------------------------------------------------------------
    z = z_score(sample)
    print(f"\nZ-score")
    print(f"  post-transform mean  = {z.mean():.2e}  (expected ~0)")
    print(f"  post-transform std   = {z.std(ddof=1):.6f}  (expected 1.0)")

    # -------------------------------------------------------------------------
    # 3. Confidence interval for the mean
    # -------------------------------------------------------------------------
    ci_95 = confidence_interval_mean(sample, confidence=0.95)
    ci_99 = confidence_interval_mean(sample, confidence=0.99)
    print(f"\nConfidence intervals for the mean")
    print(f"  95% CI: [{ci_95.lower:.4f}, {ci_95.upper:.4f}]  (centre {ci_95.centre:.4f})")
    print(f"  99% CI: [{ci_99.lower:.4f}, {ci_99.upper:.4f}]  (centre {ci_99.centre:.4f})")

    # -------------------------------------------------------------------------
    # 4. Normal distribution fitting
    # -------------------------------------------------------------------------
    fit = fit_normal(sample)
    print(f"\nNormal fit")
    print(f"  mu_hat    = {fit.mu:.4f}  (true 5.0)")
    print(f"  sigma_hat = {fit.sigma:.4f}  (true 2.0)")
    print(f"  KS stat   = {fit.ks_statistic:.4f}")
    print(f"  KS p-val  = {fit.ks_p_value:.4f}  ({'consistent with normality' if fit.ks_p_value > 0.05 else 'reject normality at 5%'})")


if __name__ == "__main__":
    main()
