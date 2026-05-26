---
tags:
  - simc
---

# Beer–Lambert Law

> [!abstract] In one line
> Absorbance is directly proportional to concentration and path length — and because this relationship is linear, the spectrum of any mixture is just the sum of its components' spectra, which is exactly why PCA works perfectly on IR data.

## The idea

Imagine a beam of light passing through a glass cuvette filled with a colored solution. The more molecules of absorbing stuff are in the path, the more light gets stopped. If you double the concentration, twice as many molecules intercept the beam, and you get double the absorbance. Same logic if you double the path length: twice as long a journey through the solution, twice as many encounters with absorbing molecules.

This is the Beer–Lambert law: a clean, linear relationship between absorbance and "how much stuff is there."

## The math / mechanism

$$A = \varepsilon \, c \, \ell$$

Symbol definitions:

| Symbol | Name | Units |
|---|---|---|
| $A$ | Absorbance (dimensionless; $A = \log_{10}(I_0/I)$) | — |
| $\varepsilon$ | Molar absorptivity (intrinsic property of the substance at one wavenumber) | L mol⁻¹ cm⁻¹ |
| $c$ | Molar concentration of the absorbing species | mol L⁻¹ |
| $\ell$ | Path length of the cuvette | cm |

Note: $\varepsilon$ depends on the wavenumber $\tilde{\nu}$ — it is different at every point in the spectrum. The full spectrum $\boldsymbol{\varepsilon}(\tilde{\nu})$ is the **pure-component spectrum** of the substance.

**The crucial consequence — mixtures add:**

If a sample contains $k$ chemical components with concentrations $c_1, c_2, \ldots, c_k$ and pure-component spectra $\boldsymbol{\varepsilon}_1, \boldsymbol{\varepsilon}_2, \ldots, \boldsymbol{\varepsilon}_k$, then the measured spectrum of the mixture at wavenumber $\tilde{\nu}$ is:

$$A(\tilde{\nu}) = \ell \sum_{j=1}^{k} \varepsilon_j(\tilde{\nu}) \, c_j$$

In vector form (stacking all $p$ wavenumber channels):

$$\mathbf{a} = \ell \sum_{j=1}^{k} c_j \, \boldsymbol{\varepsilon}_j$$

The measured spectrum is a **linear combination** of the pure-component spectra, with the concentrations as coefficients.

> [!note] What this means geometrically
> All possible mixture spectra from $k$ pure components live on a $k$-dimensional **linear subspace** of $\mathbb{R}^p$. No matter how many samples you collect, they are all confined to this flat, low-dimensional slice of the 1000-dimensional space. This is a real-data example of the [[manifold-hypothesis]].

**Law breakdown:**

The Beer–Lambert law is linear only in the regime $A \lesssim 1$. At high concentrations:
- Molecular interactions change $\varepsilon$
- Stray light in the instrument becomes significant
- The linear model breaks down and spectra no longer add cleanly

> [!warning] Common confusion
> Beer–Lambert requires **one** pure component at a time to define $\varepsilon$. For a mixture, linearity only holds when the individual components do not chemically react with each other (no new species formed). If components react, the mixture spectrum is NOT a simple sum.

## Why this matters for PCA on IR spectra

Because absorbance is linear in concentration, the $n$ spectra in your dataset all lie on (or near) a $k$-dimensional subspace, where $k$ is the number of distinct chemical components. PCA finds the principal axes of variance — which, for this data, are exactly the directions spanning that subspace. The number of large eigenvalues in the [[eigenspectrum]] directly tells you $k$. A linear method (PCA) recovers a linear structure perfectly; this is not a coincidence.

## Builds on
- [[ir-spectroscopy]]

## Leads to
- [[pca-on-ir-spectra]]
