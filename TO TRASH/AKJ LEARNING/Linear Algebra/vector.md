---
tags:
  - simc
---

# Vector

> [!abstract] In one line
> A vector is an ordered list of numbers — a Python list, or in practice a NumPy array — and geometrically it's an arrow pointing from the origin to a specific spot in space.

## The idea

In Python you'd write:

```python
import numpy as np
x = np.array([2.0, 5.0, 1.0])   # a NumPy array — what you'll use all competition
# a plain list [2.0, 5.0, 1.0] works too, but NumPy gives you the math for free
```

That's a vector. The order matters: position 0 is `2.0`, position 1 is `5.0`, position 2 is `1.0`. Swap them and you get a different vector.

Geometrically, picture each number as a coordinate — the first along the x-axis, the second along the y-axis, and so on. The vector is an arrow that starts at the origin (all zeros) and ends at that specific point. The arrow has a **direction** (which way it points) and a **magnitude** (how long it is).

One row of a data table is a vector. If you measure the height, weight, and temperature of a patient, that one patient is the vector `{height, weight, temperature}`.

## The math

A vector with $p$ entries is written:

$$\mathbf{x} = (x_1,\ x_2,\ \dots,\ x_p)$$

- $\mathbf{x}$ — the whole vector (bold lowercase = convention for vectors)
- $x_i$ — the $i$-th entry (also called a **component** or **element**), $i$ goes from $1$ to $p$
- $p$ — the number of entries, called the **dimension** of the vector

**Column vector vs. row vector:** By default in math, a vector is written as a tall column:

$$\mathbf{x} = \begin{pmatrix} x_1 \\ x_2 \\ \vdots \\ x_p \end{pmatrix}$$

A **row vector** is the same list written horizontally: $(x_1, x_2, \dots, x_p)$. The difference only matters when you combine vectors with matrices — for now, think of them as the same thing.

> [!warning] Common confusion
> A vector is **ordered** — `{2, 5, 1}` and `{5, 1, 2}` are different vectors pointing to different places, just like `arr[0]` and `arr[1]` are different slots.

## Why this matters for PCA on IR spectra

In IR spectroscopy, the instrument measures the absorbance of a sample at hundreds of different wavelengths (wavenumbers). Those absorbance readings for one sample form a single vector. All the machinery of PCA — distances, directions, compression — is defined on these vectors, so understanding what a vector is unlocks everything else.

## Builds on
- nothing — start here

## Leads to
- [[what-is-a-dimension]]
- [[matrix]]
- [[dot-product]]
- [[vector-norm-and-distance]]
