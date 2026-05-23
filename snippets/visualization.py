"""SIMC 2026 -- Reference Snippets: Visualization

Publication-ready plots for exploratory data analysis: heatmap, histogram,
scatter plot, Pearson correlation matrix, and clustering scatter plot.

Design principles
=================

Every function accepts a NumPy array as its primary data argument and a
``Path``-like output path.  Plots are saved as PNG at 150 dpi; the ``(fig,
ax)`` pair is also returned so the caller can apply additional formatting
(extra annotations, custom legends, axis rescaling) before calling
``fig.savefig`` again.  Nothing is printed to stdout and no figure windows are
opened, making these functions safe to call in headless server environments.

Titles and axis labels have sensible defaults that can be overridden via
keyword arguments.  Parent directories are created automatically if they do not
exist.

Dependencies
============

    numpy        -- array input
    matplotlib   -- all rendering
    scipy        -- not needed here; import only in the correlation helper if
                    the caller wants p-values alongside Pearson r

Quick-reference
===============

    plot_heatmap(matrix, path)                        2-D colour map
    plot_histogram(values, path)                      1-D frequency / density
    plot_scatter(x, y, path, labels=...)              2-D point cloud
    plot_correlation_matrix(data, path)               Pearson r grid
    plot_clustering(data, labels, path)               colour-coded clusters
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend; safe in headless environments
import matplotlib.pyplot as plt


# =============================================================================
# Heatmap
# =============================================================================

def plot_heatmap(
    matrix: np.ndarray,
    output_path: str | Path,
    *,
    title: str = "Heatmap",
    xlabel: str = "Column",
    ylabel: str = "Row",
    cmap: str = "viridis",
    annotate: bool = False,
) -> tuple[plt.Figure, plt.Axes]:
    """Render a 2-D NumPy array as a colour-mapped heatmap and save to disk.

    Each cell (i, j) is coloured by ``matrix[i, j]`` using the supplied
    colourmap.  A colourbar is appended to the right of the axes so the reader
    can decode the scale without inspecting the raw values.  Figure dimensions
    scale with the matrix aspect ratio (capped at 12 × 10 inches) so that
    neither very wide nor very tall matrices produce a squashed image.

    When ``annotate=True`` each cell is labelled with its value, formatted to
    two decimal places.  This is only readable for small matrices (N <= ~15);
    for larger matrices leave ``annotate=False`` (the default).

    Parameters
    ----------
    matrix : ndarray of shape (M, N)
        The 2-D data to visualise.  Non-finite values (``np.nan``,
        ``np.inf``) are rendered as white (masked) by matplotlib.
    output_path : str or Path
        Destination PNG file path.  Parent directories are created if absent.
    title : str, optional
        Axes title; default ``"Heatmap"``.
    xlabel, ylabel : str, optional
        Axis labels; defaults ``"Column"`` and ``"Row"``.
    cmap : str, optional
        Matplotlib colourmap name; default ``"viridis"``.  Use ``"RdBu_r"``
        for data that spans negative to positive values (e.g. correlations).
    annotate : bool, optional
        If ``True``, print each cell's numeric value inside the cell;
        default ``False``.

    Returns
    -------
    fig : Figure
    ax  : Axes
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    m, n = matrix.shape
    fig_w = min(2.0 + n * 0.5, 12.0)
    fig_h = min(2.0 + m * 0.5, 10.0)

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    im = ax.imshow(matrix.astype(float), aspect="auto", cmap=cmap)
    fig.colorbar(im, ax=ax, shrink=0.8)

    if annotate:
        for i in range(m):
            for j in range(n):
                ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=7)

    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return fig, ax


# =============================================================================
# Histogram
# =============================================================================

def plot_histogram(
    values: np.ndarray,
    output_path: str | Path,
    *,
    bins: int | str = "auto",
    title: str = "Histogram",
    xlabel: str = "Value",
    ylabel: str = "Frequency",
    density: bool = False,
    color: str = "#4C72B0",
) -> tuple[plt.Figure, plt.Axes]:
    """Plot a histogram of a 1-D sample and save to disk.

    The histogram uses NumPy's ``"auto"`` bin rule by default, which picks
    between the Sturges and Freedman--Diaconis estimators depending on sample
    size and spread.  Setting ``density=True`` normalises the y-axis to a
    probability density so the histogram integrates to 1 and can be overlaid
    with a fitted PDF (e.g. the output of ``fit_normal`` from
    ``statistical_tools.py``).

    Multi-dimensional inputs are silently flattened to 1-D before binning.

    Parameters
    ----------
    values : ndarray of shape (N,) or (M, N)
        The sample observations.  Non-finite values are included in the
        computation and will shift the bin range; remove them beforehand if
        undesirable.
    output_path : str or Path
        Destination PNG file path.
    bins : int or str, optional
        Number of equal-width bins or NumPy binning strategy (e.g.
        ``"auto"``, ``"fd"``, ``"sturges"``); default ``"auto"``.
    title, xlabel, ylabel : str, optional
        Axes labels; see defaults above.  ``ylabel`` is overridden to
        ``"Density"`` when ``density=True``.
    density : bool, optional
        Normalise to probability density; default ``False`` (raw counts).
    color : str, optional
        Bar fill colour; default ``"#4C72B0"`` (Seaborn blue).

    Returns
    -------
    fig : Figure
    ax  : Axes
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(
        values.ravel(),
        bins=bins,
        density=density,
        color=color,
        edgecolor="white",
        linewidth=0.5,
    )
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density" if density else ylabel)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return fig, ax


# =============================================================================
# Scatter plot
# =============================================================================

def plot_scatter(
    x: np.ndarray,
    y: np.ndarray,
    output_path: str | Path,
    *,
    labels: np.ndarray | None = None,
    title: str = "Scatter Plot",
    xlabel: str = "x",
    ylabel: str = "y",
    alpha: float = 0.7,
    point_size: float = 20.0,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot a 2-D scatter plot, optionally colouring points by a label array.

    When ``labels`` is supplied, each unique integer label receives a distinct
    colour from the ``"tab10"`` palette and appears in the legend.  When
    ``labels`` is ``None`` all points are rendered in a single default colour
    with no legend.

    The function does not perform any dimensionality reduction; the caller is
    responsible for projecting high-dimensional data to 2-D first (e.g. using
    PCA or t-SNE) before passing the first two dimensions as ``x`` and ``y``.

    Parameters
    ----------
    x, y : ndarray of shape (N,)
        Horizontal and vertical coordinates of the N points.
    output_path : str or Path
        Destination PNG file path.
    labels : ndarray of shape (N,) of int, optional
        Integer cluster / class assignment for each point; each unique value
        gets its own colour.  Negative labels (e.g. ``-1`` for noise in
        DBSCAN) are coloured grey.
    title, xlabel, ylabel : str, optional
        Axes labels.
    alpha : float, optional
        Point opacity in [0, 1]; default 0.7.
    point_size : float, optional
        Marker area in points²; default 20.

    Returns
    -------
    fig : Figure
    ax  : Axes
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmap = plt.get_cmap("tab10")

    fig, ax = plt.subplots(figsize=(6, 5))
    if labels is not None:
        for k in np.unique(labels):
            mask = labels == k
            color = "grey" if k < 0 else cmap(k % 10)
            label_str = "noise" if k < 0 else str(k)
            ax.scatter(
                x[mask], y[mask],
                color=color, label=label_str,
                alpha=alpha, s=point_size,
            )
        ax.legend(title="Label", markerscale=1.5, fontsize=8)
    else:
        ax.scatter(x, y, alpha=alpha, s=point_size)

    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return fig, ax


# =============================================================================
# Correlation matrix
# =============================================================================

def plot_correlation_matrix(
    data: np.ndarray,
    output_path: str | Path,
    *,
    column_names: list[str] | None = None,
    title: str = "Correlation Matrix",
    annotate: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """Compute and plot the Pearson correlation matrix of a data matrix.

    The correlation matrix R has R[i, j] = Pearson r between column i and
    column j.  Its diagonal is identically 1 and the matrix is symmetric.  A
    diverging ``"RdBu_r"`` colourmap centred on 0 is used so positive
    correlations (red) and negative correlations (blue) stand out against the
    white zero baseline.

    When ``annotate=True`` (default) each cell is labelled with its r value
    rounded to two decimal places.  For N > 20 variables this becomes crowded;
    pass ``annotate=False`` to suppress the text.

    Parameters
    ----------
    data : ndarray of shape (M, N) with N >= 2
        Observation matrix; rows are samples, columns are variables.
    output_path : str or Path
        Destination PNG file path.
    column_names : list of str, optional
        Variable names for tick labels; defaults to ``["0", "1", ...]``.
    title : str, optional
        Axes title.
    annotate : bool, optional
        Label each cell with its r value; default ``True``.

    Returns
    -------
    fig : Figure
    ax  : Axes
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # np.corrcoef computes the N × N Pearson correlation matrix when rowvar=False
    # (treat rows as observations, columns as variables).
    corr = np.corrcoef(data, rowvar=False)
    n = corr.shape[0]
    names = column_names if column_names is not None else [str(i) for i in range(n)]

    fig_side = max(4.0, n * 0.65 + 1.0)
    fig, ax = plt.subplots(figsize=(fig_side, fig_side * 0.9))
    im = ax.imshow(corr, vmin=-1.0, vmax=1.0, cmap="RdBu_r", aspect="auto")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")

    if annotate:
        for i in range(n):
            for j in range(n):
                text_color = "white" if abs(corr[i, j]) > 0.7 else "black"
                ax.text(
                    j, i, f"{corr[i, j]:.2f}",
                    ha="center", va="center", fontsize=8, color=text_color,
                )

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_title(title, fontsize=11)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return fig, ax


# =============================================================================
# Clustering plot
# =============================================================================

def plot_clustering(
    data: np.ndarray,
    labels: np.ndarray,
    output_path: str | Path,
    *,
    title: str = "Clustering Plot",
    xlabel: str = "Component 1",
    ylabel: str = "Component 2",
    show_centroids: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """Visualise cluster assignments in 2-D using the first two columns of data.

    Each cluster is rendered as a filled scatter layer.  When
    ``show_centroids=True`` (default) an ``"x"`` marker is placed at the
    column-mean of each cluster so the reader can see both the extent and the
    centre of each group.  This is useful for verifying KMeans results without
    having to import the centroids separately.

    If ``data`` has more than two columns only columns 0 and 1 are plotted.
    For high-dimensional data the caller should project to 2-D with PCA or
    t-SNE before calling this function.

    Parameters
    ----------
    data : ndarray of shape (M, D) with D >= 2
        Point coordinates; only columns 0 and 1 are used.
    labels : ndarray of shape (M,) of int
        Cluster label for each point.  Negative labels are coloured grey
        (convention used by DBSCAN for noise points).
    output_path : str or Path
        Destination PNG file path.
    title, xlabel, ylabel : str, optional
        Axes labels.
    show_centroids : bool, optional
        Overlay an ``"x"`` marker at each cluster centroid; default ``True``.

    Returns
    -------
    fig : Figure
    ax  : Axes
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    x, y = data[:, 0], data[:, 1]
    cmap = plt.get_cmap("tab10")
    unique_labels = np.unique(labels)

    fig, ax = plt.subplots(figsize=(6, 5))
    for k in unique_labels:
        mask = labels == k
        color = "grey" if k < 0 else cmap(k % 10)
        label_str = "noise" if k < 0 else f"Cluster {k}"
        ax.scatter(x[mask], y[mask], color=color, label=label_str, alpha=0.6, s=20)
        if show_centroids and k >= 0:
            cx, cy = x[mask].mean(), y[mask].mean()
            ax.scatter(
                cx, cy,
                color=color, marker="x", s=120, linewidths=2.5, zorder=5,
            )

    ax.legend(title="Cluster", markerscale=1.4, fontsize=8)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return fig, ax


# =============================================================================
# Driver
# =============================================================================

def main() -> None:
    """Generate all five plots from synthetic Gaussian data and save to disk.

    Output is written to ``data/output/snippets/`` relative to the current
    working directory.  Run from the repository root so that the path mirrors
    the convention used throughout the SIMC pipeline.
    """
    out = Path("data/output/snippets")
    out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed=42)

    # A 4-column data matrix: first two columns are correlated, last two are
    # independent noise.  This makes the correlation matrix non-trivial.
    base = rng.standard_normal((200, 2))
    noise = rng.standard_normal((200, 2)) * 0.3
    data = np.hstack([base, base[:, ::-1] * 0.8 + noise])

    # Binary labels for the scatter / clustering plots.
    labels = (rng.random(200) > 0.5).astype(int)

    # -------------------------------------------------------------------------
    # 1. Heatmap of the 4 × 4 Gram (X^T X) matrix -- a nice symmetric example.
    # -------------------------------------------------------------------------
    gram = data.T @ data / data.shape[0]
    plot_heatmap(
        gram, out / "heatmap.png",
        title="Gram Matrix (X\u1d40X / M)",
        xlabel="Feature", ylabel="Feature",
        cmap="magma", annotate=True,
    )

    # -------------------------------------------------------------------------
    # 2. Histogram of the first column.
    # -------------------------------------------------------------------------
    plot_histogram(
        data[:, 0], out / "histogram.png",
        title="Column 0 -- Marginal Distribution",
        xlabel="Value", density=True,
    )

    # -------------------------------------------------------------------------
    # 3. Scatter plot of the first two columns, coloured by binary label.
    # -------------------------------------------------------------------------
    plot_scatter(
        data[:, 0], data[:, 1], out / "scatter.png",
        labels=labels,
        title="Scatter: Column 0 vs Column 1",
        xlabel="Column 0", ylabel="Column 1",
    )

    # -------------------------------------------------------------------------
    # 4. Correlation matrix of all four columns.
    # -------------------------------------------------------------------------
    plot_correlation_matrix(
        data, out / "correlation_matrix.png",
        column_names=["A", "B", "C", "D"],
        title="Pearson Correlation Matrix",
    )

    # -------------------------------------------------------------------------
    # 5. Clustering plot using the same binary labels.
    # -------------------------------------------------------------------------
    plot_clustering(
        data, labels, out / "clustering.png",
        title="Clustering: Binary Labels",
    )

    print("All plots written to", out)


if __name__ == "__main__":
    main()
