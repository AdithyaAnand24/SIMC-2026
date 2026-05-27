# codereadme.md — how the code works (and the few hard bits)

The notebook **`src/SIMC2026_submission.ipynb`** is written in a deliberately
simple style: plain `for` loops, descriptive variable names, one step at a time,
lots of comments. Anyone on the team should be able to read any cell top to
bottom and explain it.

This file covers two things:
- **Part A — the unavoidable library calls.** A handful of steps *cannot* be
  written as simple loops (they would be impossible to write by hand or would
  take hours to run). We kept those as one-line library calls and explain each
  here.
- **Part B — a plain-English glossary** of the everyday numpy we *did* keep, so
  nobody is ever staring at a line they don't understand.
- **Part C — the style** we used (what we replaced and why), so if we add parts
  3f / 3g / 3h later they match.

---

## How to run it

1. Open `src/SIMC2026_submission.ipynb` (Jupyter, VS Code, or Colab).
2. **Run from the repository root** so the paths work
   (`data/input/mystery_matrix1.npy` must be reachable as written).
3. "Run All", top to bottom. It needs only **numpy** and **matplotlib**.
4. It prints results and saves plots into `data/output/`.

### Expected numbers (use these to check a good run)

| Where | Should print |
|---|---|
| 1f | `c1 = 1.0  c2 = 0.5`; biggest difference ≈ 1e-16 |
| 1h | residue `p1(inf) = 0.001038` |
| 3a(i) | `T = 40` empty vials |
| 3a(ii) | 36 outliers, rows 924–959; cleaned matrix `(924, 3401)` |
| 3a(ii) | clusters `WITH = 26`, `WITHOUT = 25` (removing the 36 drops exactly one) |
| 3b | largest-variance feature `j* = 910` (variance ≈ 0.0199) |
| 3c | `lambda1/lambda2 = 3.533`; elbow `k* = 8`; 8 components ≈ 55.5%; 95% at k=667 |
| 3d | best match `row #193`, `cos = 0.918` |
| 3e | `distinct clusters = 25` |

If you get these, the run is correct.

---

## Part A — the unavoidable library calls (complexity we could NOT remove)

These four stay as library calls. Everything *around* them is plain loops.

### A1. `np.linalg.eigh(C)` — eigenvalues and eigenvectors

**Where:** Task 3c (`w, V = np.linalg.eigh(C)`) and inside the `pca_scores`
helper in 3a(ii) (`np.linalg.eigh(gram)`).

**What it does:** takes a square symmetric matrix and returns its *eigenvalues*
(how much variance lies along each principal direction) and *eigenvectors* (the
principal directions themselves). This is the mathematical heart of PCA.

**Why we can't write it by hand:** finding eigenvalues means solving a degree-`n`
polynomial. For our covariance matrix that is **degree 3401** — there is no
formula, only iterative numerical algorithms (QR iteration etc.) that are
hundreds of lines of very delicate floating-point code. Writing a correct,
stable version ourselves is not realistic. `eigh` is the standard, battle-tested
tool (it calls the LAPACK library). The `h` means "Hermitian/symmetric" — it is
the right one for a covariance matrix and returns the eigenvalues **smallest
first** (that is why we reverse them).

### A2. The matrix-multiply operator `@`

**Where:**
- `C = (X_centered.T @ X_centered) / N_tilde` — build the covariance matrix.
- `gram = Xc @ Xc.T` — the Gram matrix inside `pca_scores`.
- `Z = X_centered @ eigvecs[:, :4]` — project samples onto the top 4 directions.
- `M @ P_num[step]` and `row @ vector` — matrix-times-vector and dot products.

**What it does:** `A @ B` is ordinary matrix multiplication (row-times-column
sums).

**Why we kept it instead of looping:** the covariance line
`X_centered.T @ X_centered` multiplies a `3401×924` matrix by a `924×3401`
matrix. Done by hand that is **3401 × 3401 × 924 ≈ 10,000,000,000**
multiply-add operations. In a plain Python triple loop that would run for many
minutes to hours; with `@` it finishes in a fraction of a second. `@` is also
short and readable ("matrix multiply"), so looping it would make the code *both*
slower *and* harder to read. We left every `@` in place.

### A3. `np.load(DATA_PATH)`

**What it does:** reads the binary `.npy` file into an array.

**Why:** `.npy` is a special binary format; there is no sensible way to parse it
by hand. One line, done.

### A4. `np.linalg.solve(basis, p0)` — solve a tiny system

**Where:** Task 1f, to find `c1, c2` with `p0 = c1·v1 + c2·v2`.

**What it does:** solves the 2-equation, 2-unknown system for `c1` and `c2`.

**Why we kept it:** this one *is* small enough to do by hand (it's only 2×2),
but `np.linalg.solve` states the intent clearly in one line ("solve these
equations") and avoids a fiddly elimination by hand that could hide a bug. The
answer here is `c1 = 1.0, c2 = 0.5`.

---

## Part B — plain-numpy glossary (the shortcuts we DID keep)

These are simple enough to keep, but here is exactly what each one means.

- **`axis=0` vs `axis=1`.** Our data is rows = samples, columns = frequencies.
  - `axis=0` means "go **down** the columns" → one result **per frequency**.
    `S_clean.mean(axis=0)` = the average spectrum (one value per frequency).
  - `axis=1` means "go **across** the rows" → one result **per sample**.
    `rows.std(axis=1)` = how much each spectrum wiggles (one value per sample).
- **`.mean()`, `.var()`, `.sum()`, `.min()`, `.max()`** on an array compute the
  average / variance / total / smallest / largest. With no `axis` they use every
  number; with `axis=0` or `axis=1` they work per-column or per-row (see above).
- **`.T`** is the transpose: it flips rows and columns (a `924×3401` becomes
  `3401×924`).
- **Boolean masks.** `empty = norms < 3.0` makes an array of True/False, one per
  sample. `S[empty]` then selects exactly the rows where the mask is True. Read
  `S[empty]` as "the spectra that are empty". `int(empty.sum())` counts the
  Trues (True counts as 1).
- **`np.argmax(variances)`** returns the *index* of the largest value (here, the
  frequency with the most variance). It does **not** return the value itself.
- **`np.sort(norms)`** returns the norms sorted smallest-to-largest (a copy).
- **`np.median(x)`** is the middle value.
- **`np.histogram(x, bins=40)`** counts how many values fall in each of 40 equal
  buckets; we print it as a text bar chart to see the empty gap.
- **`np.abs`, `np.exp`** are element-by-element absolute value and `e^x`.
- **Subtracting a row from a matrix** — `X_centered = S_clean - average_spectrum`
  — subtracts the (length-3401) average spectrum from *every* row. numpy lining
  shapes up like this automatically is called *broadcasting*; here it just means
  "center every spectrum".
- **`np.clip` is NOT used** — we replaced it with an explicit loop that sets tiny
  negative eigenvalues (rounding error) to 0.

---

## Part C — the simple-coding style we used

For consistency, if we write parts **3f / 3g / 3h** later, follow the same rules.
Wherever the original code used a clever one-liner, we replaced it with a loop:

| Clever original | What we wrote instead |
|---|---|
| `np.linalg.norm(S, axis=1)` | a `for i` loop calling `np.linalg.norm(S[i])` on each row |
| `np.argsort(x)[::-1][:k]` | a loop that picks the top-k one at a time |
| `np.diff(sn)` + `np.argmax(...)` | a loop that checks each neighbour gap and keeps the widest |
| `np.argsort(w)[::-1]` (reverse) | build an index list with `range(len-1, -1, -1)` |
| `np.clip(x, 0, None)` | a loop that zeroes negatives |
| `np.cumsum` / `np.searchsorted` | a running-total loop / a scan loop |
| `((Z[:,None]-Z[None])**2).sum(-1)` (distance matrix) | nested loops computing each distance |
| one-line "leader clustering" | the same algorithm written out with named variables |
| `np.cumprod` + `np.concatenate` | a running-product loop |
| list comprehensions, `zip`, ternary `a if c else b` | explicit `for` loops and `if/else` |

**Rule of thumb:** if a line needs a comment longer than the line to explain,
turn it into a loop. The two exceptions are the four items in Part A — those stay
as library calls and are explained above.
