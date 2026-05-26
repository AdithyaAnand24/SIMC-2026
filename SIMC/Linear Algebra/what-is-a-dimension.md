---
tags:
  - simc
---

# What is a dimension

> [!abstract] In one line
> A dimension is just one slot in your vector — the number of dimensions equals the number of features, which equals the length of the array that describes one data point.

## The idea

Imagine giving someone directions to a spot:

- **1D:** "Go 3 metres forward." One number tells you everything. A number line.
- **2D:** "Go 3 east, 5 north." Two numbers. A flat map.
- **3D:** "Go 3 east, 5 north, 2 up." Three numbers. The real world.

The pattern: **dimension = how many numbers you need to pin down one point = the length of the vector.**

Now consider an IR spectrum. The instrument fires infrared light at a sample and measures how much is absorbed at, say, 1000 different wavenumbers. One sample produces 1000 readings:

```python
spectrum = np.zeros(1000)   # one sample = one vector of length 1000
```

That single sample is a **point in 1000-dimensional space**. You cannot draw it. Your brain cannot picture it. That is fine — mathematics works perfectly in any number of dimensions, even billions.

> [!note] "High-dimensional data"
> When people say a dataset is high-dimensional, they just mean each data point is described by a long vector — many features per sample. IR spectra are a classic example.

## The math

If a vector $\mathbf{x} = (x_1, x_2, \dots, x_p)$ has $p$ entries, we say it lives in **$p$-dimensional space**, written $\mathbb{R}^p$.

- $\mathbb{R}$ — the set of all real numbers
- $\mathbb{R}^p$ — the set of all ordered lists of $p$ real numbers
- $p$ — **dimensionality** (also called the number of features, variables, or columns)

For an IR spectrum measured at $p = 1000$ wavenumbers, each sample $\mathbf{x} \in \mathbb{R}^{1000}$. The symbol $\in$ just means "is a member of" — your array slot fits inside that space.

> [!warning] Common confusion
> "Dimension" in everyday speech often means physical dimension (length, width, height). In data science it means **the number of distinct coordinates needed to describe one observation**. A 1000-wavenumber IR spectrum lives in 1000 dimensions, even though physically it's just one little cuvette of liquid.

## Why this matters for PCA on IR spectra

PCA's entire job is **dimensionality reduction**: it takes your $p = 1000$ dimensional data and finds a much smaller number of directions (principal components) that still capture most of the information. Understanding that each sample is a point in a very high-dimensional space makes clear *why* you need PCA — plotting or analyzing 1000-dimensional clouds of points directly is impossible.

## Builds on
- [[vector]]

## Leads to
- [[design-matrix]]
- [[curse-of-dimensionality]]
