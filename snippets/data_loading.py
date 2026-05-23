"""SIMC 2026 -- Reference Snippets: Data Loading

Functions for loading common scientific data formats (CSV, NPZ, TXT, JSON)
into NumPy arrays and Python data structures.  Each loader follows the same
pattern: accept a filesystem path, validate the file, load the payload, and
return it in a predictable type so callers never have to inspect raw bytes.

Formats covered
===============

CSV  -- delimiter-separated tabular data; returns a NumPy float64 array plus
        a header list so column names travel with the matrix.
NPZ  -- NumPy's native compressed archive; returns the raw NpzFile so all
        named arrays are accessible by key without loading everything at once.
TXT  -- whitespace-delimited plain text produced by ``np.savetxt``; returns a
        NumPy float64 array suitable for direct computation.
JSON -- arbitrary nested data from a JSON file; returns a Python dict / list
        so that structured records (e.g. SIMC summary files) can be read back
        verbatim.

Usage example
=============

    data, headers = load_csv("data/input/scores.csv")
    archive       = load_npz("data/input/sample.npz")
    X             = archive["sample_larger"]
    matrix        = load_txt("data/input/matrix.txt")
    summary       = load_json("data/output/task8/task8_summary.json")
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


# =============================================================================
# CSV
# =============================================================================

def load_csv(
    path: str | Path,
    *,
    delimiter: str = ",",
    has_header: bool = True,
) -> tuple[np.ndarray, list[str]]:
    """Load a delimiter-separated value file into a NumPy float64 array.

    The loader reads the optional header row separately so that column names
    are returned alongside the data matrix.  All remaining rows are cast to
    ``float64``; cells that are empty or cannot be parsed (e.g. ``"N/A"``,
    ``""``) become ``np.nan`` so downstream functions receive a clean float
    array rather than raising at load time.

    Parameters
    ----------
    path : str or Path
        Path to the CSV (or TSV) file.
    delimiter : str, optional
        Field separator; default ``","``; use ``"\\t"`` for tab-separated files.
    has_header : bool, optional
        If ``True`` (default) the first row is treated as column names and
        returned in ``headers``; if ``False`` an empty list is returned and
        every row is parsed as numeric data.

    Returns
    -------
    data : ndarray of shape (M, N), dtype float64
        The numeric payload; rows are observations, columns are variables.
        Cells that cannot be cast to float are replaced with ``np.nan``.
    headers : list of str
        Column names extracted from the first row, or ``[]`` when
        ``has_header=False``.

    Notes
    -----
    For very large files (> 10^6 rows) prefer ``np.genfromtxt`` with
    ``dtype=float`` directly, which streams the file without building an
    intermediate list of lists.

    Examples
    --------
    >>> data, headers = load_csv("scores.csv")
    >>> data.shape
    (200, 5)
    >>> headers
    ['student_id', 'q1', 'q2', 'q3', 'q4']
    """
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter=delimiter)
        rows = list(reader)

    if has_header and rows:
        headers: list[str] = rows[0]
        data_rows = rows[1:]
    else:
        headers = []
        data_rows = rows

    def _to_float(cell: str) -> float:
        stripped = cell.strip()
        if stripped == "":
            return np.nan
        try:
            return float(stripped)
        except ValueError:
            return np.nan

    data = np.array(
        [[_to_float(cell) for cell in row] for row in data_rows],
        dtype=np.float64,
    )
    return data, headers


# =============================================================================
# NPZ
# =============================================================================

def load_npz(path: str | Path) -> np.lib.npyio.NpzFile:
    """Load a NumPy compressed archive (.npz) and return the NpzFile handle.

    An NpzFile object is a lazy dict-like container: individual arrays are
    only decompressed and loaded into memory when accessed by key.  Callers
    should inspect ``loaded.files`` to discover the available arrays, then
    index by name::

        archive = load_npz("sample.npz")
        print(archive.files)           # ['sample_small', 'sample_larger']
        X = archive["sample_larger"]   # decompressed only here

    The returned object must be closed (or used as a context manager) to
    release the underlying ZIP file handle.  For one-off scripts it is safe
    to leave it open until the process exits; for server-side code, use::

        with load_npz("sample.npz") as archive:
            X = archive["sample_larger"]

    Parameters
    ----------
    path : str or Path
        Path to the ``.npz`` archive.  NumPy appends ``".npz"`` automatically
        if the extension is missing.

    Returns
    -------
    archive : NpzFile
        Lazy archive handle; access arrays with ``archive["name"]`` and list
        available keys with ``archive.files``.
    """
    return np.load(Path(path))


# =============================================================================
# TXT
# =============================================================================

def load_txt(path: str | Path, *, comments: str = "#") -> np.ndarray:
    """Load a plain-text numeric file written by ``np.savetxt`` into an array.

    ``np.loadtxt`` expects one row of whitespace-delimited floats per line.
    Lines beginning with the ``comments`` character (default ``"#"``) are
    silently skipped, which preserves compatibility with files that embed
    metadata via ``np.savetxt(..., header="alpha beta gamma")``.

    The result is always at least two-dimensional: a file with a single data
    row returns shape ``(1, N)`` rather than ``(N,)`` to avoid surprise when
    callers assume matrix semantics.

    Parameters
    ----------
    path : str or Path
        Path to the whitespace-delimited text file.
    comments : str, optional
        Character(s) that introduce comment / header lines; default ``"#"``.

    Returns
    -------
    data : ndarray of shape (M, N), dtype float64
        Numeric matrix; single-row files are reshaped to ``(1, N)``.

    Examples
    --------
    >>> matrix = load_txt("data/input/matrix.txt")
    >>> matrix.shape
    (50, 10)
    """
    data = np.loadtxt(Path(path), comments=comments, dtype=np.float64)
    if data.ndim == 1:
        # A single-row file produces a 1-D array; restore the row dimension so
        # callers can always assume shape (M, N) without an extra branch.
        data = data[np.newaxis, :]
    return data


# =============================================================================
# JSON
# =============================================================================

def load_json(path: str | Path) -> Any:
    """Load a JSON file and return the parsed Python object.

    JSON is the canonical output format for SIMC structured summaries (e.g.
    ``task8_summary.json``).  This loader returns whatever Python type the
    top-level JSON value maps to: a ``dict`` for JSON objects, a ``list`` for
    JSON arrays, or a scalar for bare primitives.  Callers can therefore
    round-trip any summary produced by ``json.dump`` without loss.

    The file is read with UTF-8 encoding, which is the JSON RFC-8259 default
    and matches the encoding used throughout the SIMC pipeline.

    Parameters
    ----------
    path : str or Path
        Path to the ``.json`` file.

    Returns
    -------
    payload : dict or list or scalar
        The parsed JSON value; concrete type depends on the file content.

    Examples
    --------
    >>> summary = load_json("data/output/task8/task8_summary.json")
    >>> summary["students"]
    10000
    >>> summary["null_similarity"]["expected_value"]
    2.556724
    """
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


# =============================================================================
# Driver
# =============================================================================

def main() -> None:
    """Demonstrate each loader with a small synthetic dataset.

    The driver writes temporary files to a system temp directory, loads them
    back with the loaders above, prints brief diagnostics for each, and
    removes the temporary files on exit.
    """
    import os
    import tempfile

    rng = np.random.default_rng(seed=0)
    data_orig = rng.standard_normal((5, 3))

    # -------------------------------------------------------------------------
    # 1. CSV round-trip
    # -------------------------------------------------------------------------
    with tempfile.NamedTemporaryFile(
        suffix=".csv", mode="w", delete=False, newline="", encoding="utf-8"
    ) as fh:
        csv_path = fh.name
        writer = csv.writer(fh)
        writer.writerow(["alpha", "beta", "gamma"])
        writer.writerows(data_orig.tolist())

    data_csv, headers = load_csv(csv_path)
    print("CSV -- headers:", headers)
    print("CSV -- shape  :", data_csv.shape)
    print("CSV -- row 0  :", data_csv[0].round(4))
    os.unlink(csv_path)

    # -------------------------------------------------------------------------
    # 2. NPZ round-trip
    # -------------------------------------------------------------------------
    with tempfile.NamedTemporaryFile(suffix=".npz", delete=False) as fh:
        npz_path = fh.name
    np.savez_compressed(npz_path, matrix=data_orig, labels=np.arange(5))
    archive = load_npz(npz_path)
    print("\nNPZ -- keys  :", archive.files)
    print("NPZ -- shape :", archive["matrix"].shape)
    archive.close()
    os.unlink(npz_path)

    # -------------------------------------------------------------------------
    # 3. TXT round-trip
    # -------------------------------------------------------------------------
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as fh:
        txt_path = fh.name
    np.savetxt(txt_path, data_orig, header="alpha beta gamma")
    data_txt = load_txt(txt_path)
    print("\nTXT -- shape :", data_txt.shape)
    print("TXT -- row 0 :", data_txt[0].round(4))
    os.unlink(txt_path)

    # -------------------------------------------------------------------------
    # 4. JSON round-trip
    # -------------------------------------------------------------------------
    payload_out = {
        "n_rows": int(data_orig.shape[0]),
        "n_cols": int(data_orig.shape[1]),
        "grand_mean": float(data_orig.mean()),
    }
    with tempfile.NamedTemporaryFile(
        suffix=".json", mode="w", delete=False, encoding="utf-8"
    ) as fh:
        json_path = fh.name
        json.dump(payload_out, fh, indent=2)

    payload_in = load_json(json_path)
    print("\nJSON -- payload:", payload_in)
    os.unlink(json_path)


if __name__ == "__main__":
    main()
