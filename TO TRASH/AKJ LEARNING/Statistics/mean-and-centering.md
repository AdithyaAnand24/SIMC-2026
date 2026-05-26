---
tags:
  - simc
---

# Mean and centering

> [!abstract] In one line
> Subtracting each feature's mean from every data point shifts the entire data cloud so its center lands exactly at the origin.

## The idea

You already know the mean: add everything up, divide by $n$. Centering is the next small step — it just moves the data.

Imagine a swarm of bees hovering somewhere in a room. "Centering" the swarm means you teleport the whole swarm so that its center of mass sits exactly at the room's center point. Every bee moves by the same offset; the *shape* of the swarm is unchanged. That's all centering does to a dataset.

Why bother? PCA only cares about **how the data spreads around its center** — it looks for the directions of maximum scatter. If the data cloud isn't centered at the origin, the math picks up a false "direction" toward wherever the cloud is floating. Centering removes that artifact before PCA starts.

## The math

For a dataset with $n$ observations and $p$ features, let $x_{ij}$ be the value of observation $i$ on feature $j$.

**Mean of feature $j$:**
$$\bar{x}_j = \frac{1}{n} \sum_{i=1}^{n} x_{ij}$$

**Centered value:**
$$\tilde{x}_{ij} = x_{ij} - \bar{x}_j$$

You compute one mean per feature (per column), then subtract it from every entry in that column. The result $\tilde{x}_{ij}$ is the *centered* version of the data.

After centering, every column has mean exactly 0:
$$\frac{1}{n}\sum_{i=1}^{n} \tilde{x}_{ij} = 0$$

> [!warning] Common confusion
> You subtract the **column** mean, not a single grand mean. Each feature gets its own mean removed. Subtracting one number from the whole dataset would only work if all features were on the same scale — which they almost never are.

> [!example] IR spectroscopy context
> An IR spectrum has ~1000 wavenumber channels (features). Centering subtracts the average absorbance at each wavenumber across all samples. This removes the "baseline offset" shared by all spectra, leaving only the variation that distinguishes one sample from another.

## Why this matters for PCA on IR spectra

PCA measures variance and covariance — both are defined relative to the mean. If you skip centering, PCA mixes up "where the data sits" with "how the data varies," and the first principal component ends up pointing toward the average spectrum rather than the direction of maximum variation between samples. Centering is not optional; it is step 1 of every PCA pipeline.

## Builds on

*(uses the probability mean you already know — no new prerequisites)*

## Leads to

- [[variance]]
- [[covariance]]
