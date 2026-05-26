---
tags:
  - simc
---

# NumPy Basics

## What it is

NumPy is Python's array library — the foundation of nearly every scientific Python tool you'll touch (pandas, scipy, scikit-learn, PyTorch, JAX all sit on top of it). If you do anything numerical in Python that isn't trivial, you're using NumPy directly or indirectly.

The core object is the ==ndarray== (N-dimensional array): a ==homogeneous-type, contiguous-memory, fixed-shape== block of numbers. "Homogeneous" means every element is the same type (all `float64`, all `int32`, etc.) — unlike a Python list, which can mix ints, strings, dicts, and other lists. "Contiguous" means the data sits in one flat slab of memory, not scattered around the heap with pointer-chasing. That layout is what makes ndarrays fast.

The killer feature is ==vectorization==: operations apply to the whole array at once, without explicit loops. `arr * 2` doubles every element. `arr1 + arr2` adds them pairwise. This is both faster (the loop runs in C, not Python) AND more readable than the equivalent for-loop or list comprehension.

```python
# Python list: needs a comprehension
doubled = [x * 2 for x in my_list]

# NumPy: just multiply
doubled = arr * 2
```

## Why ndarrays beat Python lists

| Property | Python `list` | NumPy `ndarray` |
|---|---|---|
| Element type | Mixed (anything) | Homogeneous (one dtype) |
| Memory layout | Scattered (list of pointers) | Contiguous flat block |
| Speed (1M elements) | Slow (Python loop) | ~50-100x faster (C loop) |
| Math on whole array | `[x * 2 for x in xs]` | `arr * 2` |
| Element-wise add | `[a + b for a, b in zip(xs, ys)]` | `xs + ys` |
| Memory per int | ~28 bytes (Python object) | 8 bytes (`int64`) |
| Resizable | Yes (`.append()`) | No (fixed shape) |

> [!info] When to use which
> Use Python lists for small, mixed-type, frequently-resized data. Use ndarrays for anything numerical, large, or where you'll do math on every element.

## Java analogy

An ndarray is like a Java `double[]` or `int[][]` — fixed type, fixed shape, stored as a contiguous block — BUT with operator overloading. Java arrays force you to write the loop yourself; NumPy hides it.

```java
// Java: explicit loop required
double[] arr = new double[1000];
for (int i = 0; i < arr.length; i++) {
    arr[i] = arr[i] * 2;
}
```

```python
# NumPy: no loop visible
arr = arr * 2
```

Same operation, same O(n) cost — but NumPy's loop runs in compiled C, not interpreted Python, so it's typically 50-100x faster than the equivalent Python `for` loop. The Java loop is fast too (JIT-compiled), but it's still verbose.

## Creating arrays

```python
import numpy as np

np.array([1, 2, 3])           # from a Python list
np.array([[1, 2], [3, 4]])    # 2D from a nested list

np.zeros(5)                   # 1D: array([0., 0., 0., 0., 0.])
np.zeros((3, 4))              # 2D: 3 rows, 4 columns of zeros
np.ones(5)                    # array of ones
np.full((2, 3), 7)            # 2x3 array filled with 7

np.arange(0, 10, 2)           # like range: array([0, 2, 4, 6, 8])
np.linspace(0, 1, 5)          # 5 evenly-spaced points: [0., 0.25, 0.5, 0.75, 1.]

np.empty((3, 3))              # uninitialized — fast but contents are garbage
```

> [!tip] `arange` vs `linspace`
> `np.arange(start, stop, step)` is `stop`-EXCLUSIVE and you specify the step. `np.linspace(start, stop, num)` is `stop`-INCLUSIVE and you specify how many points. Use `linspace` when you want a known number of samples; use `arange` when you want a known step.

## Inspecting arrays

Every ndarray carries metadata:

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

arr.shape    # (2, 3) — tuple of dimensions
arr.ndim     # 2 — number of dimensions
arr.size     # 6 — total elements
arr.dtype    # dtype('int64') — element type
```

> [!warning] Shape is a tuple — mind the trailing comma
> A 1D array of length 5 has shape `(5,)` — note the comma. `(5)` in Python is just the integer 5 in parens; `(5,)` is a 1-tuple. This trips people up when constructing arrays: `np.zeros(5)` and `np.zeros((5,))` both work, but `np.zeros((3, 4))` requires the tuple form because shapes with multiple dimensions must be tuples.

## Indexing and slicing

Just like Python lists, with extensions for multi-D:

```python
arr = np.array([10, 20, 30, 40, 50])

arr[0]        # 10
arr[-1]       # 50 (last)
arr[1:4]      # array([20, 30, 40])
arr[:3]       # array([10, 20, 30])
arr[::2]      # array([10, 30, 50]) — every other
arr[::-1]     # array([50, 40, 30, 20, 10]) — reversed

# 2D
mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
mat[1, 2]     # 6 — row 1, col 2 (preferred)
mat[1][2]     # 6 — also works but slower (creates intermediate row)
mat[1, :]     # array([4, 5, 6]) — full row 1
mat[:, 2]     # array([3, 6, 9]) — full column 2
mat[0:2, 1:]  # 2x2 submatrix
```

> [!warning] Slices return VIEWS, not copies
> ==Modifying a slice modifies the original array.== This is a major difference from Python lists (which return copies on slice). If you need an independent copy, call `.copy()` explicitly.
> ```python
> arr = np.array([1, 2, 3, 4, 5])
> sub = arr[1:4]
> sub[0] = 999
> print(arr)  # array([  1, 999,   3,   4,   5]) — original mutated!
> ```

## Boolean masking (THE killer pattern)

This is the move you'll reach for constantly in simulations.

Element-wise comparison creates a ==boolean array== — same shape as the input, `True` where the condition holds:

```python
arr = np.array([1, 5, 3, 8, 2, 9])
arr > 4              # array([False,  True, False,  True, False,  True])
arr == 5             # array([False,  True, False, False, False, False])
arr % 2 == 0         # array([False, False, False,  True,  True, False])
```

Use boolean arrays to ==filter==:

```python
arr[arr > 4]         # array([5, 8, 9]) — only elements > 4
```

Or to ==count / compute fractions==:

```python
(arr > 4).sum()      # 3 — number of True values
(arr > 4).mean()     # 0.5 — fraction of True values
```

> [!tip] Boolean mean = empirical probability
> ==`(condition).mean()` returns the fraction of `True` values in a boolean array.== This is THE pattern for empirical probability — turn a condition into a boolean array, take the mean, and you have $\hat{P}$ for that event. If $X_i$ are i.i.d. samples and you want $\hat{P}(X > t)$:
> $$\hat{P}(X > t) = \frac{1}{n}\sum_{i=1}^{n} \mathbb{1}[X_i > t] = \texttt{(samples > t).mean()}$$

Example — fraction of uniform floats above 0.5:

```python
rng = np.random.default_rng(seed=0)
samples = rng.random(size=100_000)   # 100k floats in [0, 1)
print((samples > 0.5).mean())        # ≈ 0.5
```

## Element-wise operations (vectorization)

All standard arithmetic operators apply element-wise:

```python
arr + 10        # adds 10 to every element
arr - 1         # subtracts 1
arr * 2         # doubles
arr / 4         # divides (always returns floats)
arr // 2        # floor division (integer division)
arr ** 2        # squares
arr % 3         # modulo

arr1 + arr2     # element-wise (requires compatible shapes)
arr1 * arr2     # element-wise multiplication (NOT matrix multiplication — that's @)
```

NumPy math functions apply element-wise too:

```python
np.sqrt(arr)
np.exp(arr)
np.log(arr)
np.sin(arr)
np.abs(arr)
np.round(arr, decimals=2)
```

Comparisons return boolean arrays (see above): `arr > 5`, `arr == 0`, `arr1 < arr2`.

## Reductions

Reductions collapse an array to a single value (or a smaller array along an axis):

```python
arr.sum()        # total
arr.mean()       # average
arr.std()        # standard deviation
arr.var()        # variance
arr.min()        # smallest
arr.max()        # largest
arr.argmin()     # INDEX of smallest
arr.argmax()     # INDEX of largest

# For boolean arrays:
bools.any()      # True if any element is True
bools.all()      # True if all elements are True
```

Per-axis reductions on 2D arrays:

```python
mat = np.array([[1, 2, 3], [4, 5, 6]])

mat.sum()              # 21 — sum of all elements
mat.sum(axis=0)        # array([5, 7, 9]) — sum down each column
mat.sum(axis=1)        # array([6, 15]) — sum across each row
```

> [!info] `axis=0` vs `axis=1` mnemonic
> `axis=0` is the axis that ==goes away== — `sum(axis=0)` collapses the row dimension, leaving one value per column. Same for `mean`, `max`, etc.

## Random numbers

The `np.random` module is what you'll use for simulations. ==Always use the modern `default_rng` API== — better statistical properties, reproducible with a seed, thread-safe.

```python
rng = np.random.default_rng(seed=42)   # create a generator (seed for reproducibility)

rng.integers(low, high, size=n)        # n random ints in [low, high) — high is EXCLUSIVE
rng.random(size=n)                      # n random floats in [0, 1)
rng.choice(a, size=n, replace=False)   # n choices from array a
rng.normal(loc=0, scale=1, size=n)     # n samples from Normal(mean=0, std=1)
rng.uniform(low=0, high=1, size=n)     # n samples from Uniform(low, high)
```

Example — flipping 1000 coins and counting heads:

```python
rng = np.random.default_rng(seed=1)
flips = rng.integers(0, 2, size=1000)   # 0 or 1, 1000 times
fraction_heads = (flips == 1).mean()
print(fraction_heads)                    # ≈ 0.5
```

> [!info] Old API vs new API
> You'll see `np.random.randint(low, high, size=n)` in older tutorials and Stack Overflow answers. It still works, but `rng = np.random.default_rng(seed); rng.integers(...)` is the modern preferred form. Use it from the start so seeding is reproducible.

> [!warning] `high` is EXCLUSIVE
> Both `rng.integers(1, 7)` and `np.random.randint(1, 7)` give values in `{1, 2, 3, 4, 5, 6}`, NOT 1..7. Classic off-by-one trap. To roll a 6-sided die, use `(1, 7)` — not `(1, 6)`.

## Common mistakes

> [!warning] Off-by-one with `integers` / `randint`
> The `high` argument is ==exclusive==. To sample from $\{1, 2, \ldots, k\}$, use `rng.integers(1, k+1, size=n)`.

> [!warning] Integer vs float division
> `arr / 2` always returns floats (even if both operands are ints). Use `arr // 2` for integer (floor) division. This bit me coming from Java where `int / int = int`.

> [!warning] Mutation vs reassignment
> `arr += 1` modifies in place; `arr = arr + 1` creates a new array and rebinds the name. The first is faster and memory-efficient, but if another variable also references the original array, it will see the change too. Be deliberate.

> [!warning] Shape mismatch on arithmetic
> `np.array([1, 2, 3]) + np.array([1, 2])` raises `ValueError`. ==Broadcasting== (separate note for later) handles SOME shape mismatches automatically — e.g., adding a scalar to an array, or adding a 1D array to each row of a 2D array — but not arbitrary ones. When in doubt, print `.shape` on both sides.

> [!warning] Slices are views, not copies
> (Repeating because it bites everyone.) `sub = arr[1:4]; sub[0] = 999` mutates `arr`. Use `arr[1:4].copy()` if you need independence.

> [!warning] `==` returns an array, not a bool
> `arr == 5` is a boolean array, not a single `True`/`False`. Don't use it directly in an `if`: `if arr == 5:` raises `ValueError`. Use `if (arr == 5).any():` or `if (arr == 5).all():` depending on intent.

> [!tip] Type annotations for NumPy functions
> When writing function signatures that take or return arrays, annotate as `np.ndarray` (not just `array`, which Python doesn't know about). For the full pattern — including how to be more specific with shape/dtype — see [[type-hints]].

## Why this matters for SIMC

NumPy is the floor for every modeling, simulation, and data-handling task in SIMC. Probability simulations (Monte Carlo dice/coin/card experiments), linear algebra (matrix ops in transition matrices, regression), statistical inference (vectorized aggregations across thousands of trials), and any ML model fitting — all of it runs on ndarrays. Get fluent here and every downstream topic (`scipy.stats`, `pandas`, `sklearn`) becomes incrementally easier rather than a fresh language to learn.

Your current exercise (`SIMC/CODINGPRAC/01_sample_spaces.py`) is the simplest possible application: sample → condition → mean. That same three-step pattern scales from die rolls to bootstrap confidence intervals to MCMC. Internalize it now.

## Sources

- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) — official tutorial, gentle pace
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) — faster tour for users with programming background
- [NumPy random sampling docs](https://numpy.org/doc/stable/reference/random/index.html) — full `default_rng` API reference
