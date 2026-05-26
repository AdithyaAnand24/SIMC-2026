---
tags:
  - simc
---

# IR Spectroscopy

> [!abstract] In one line
> Shine infrared light through a molecule; it absorbs specific frequencies where bonds vibrate — the absorption pattern is a unique chemical fingerprint recorded as a spectrum.

## The idea

Molecular bonds (C–H, O–H, C=O, …) are not rigid sticks — they stretch and bend like tiny springs. Each bond vibrates at a natural frequency determined by the masses of the atoms and the stiffness of the bond. Infrared light carries exactly the right energy scale to match these vibrational frequencies. When IR light hits a sample, the bonds that match the incoming frequency absorb that energy; everything else passes through.

The instrument sweeps across frequencies and records **how much light was absorbed at each frequency**. The result is a spectrum: a graph of absorbance versus frequency. Think of it as the molecule's fingerprint — no two chemically distinct compounds have the same pattern.

## The math / mechanism

Frequency is reported as **wavenumber** $\tilde{\nu}$ (pronounced "nu-tilde"):

$$\tilde{\nu} = \frac{1}{\lambda}$$

Units: cm⁻¹. Higher wavenumber = higher frequency = higher energy vibration.

Typical IR range: $400$ to $4000\ \text{cm}^{-1}$.

**Two regions to know:**

| Region | Wavenumber range | What it tells you |
|---|---|---|
| Functional-group region | $1500$–$4000\ \text{cm}^{-1}$ | Specific bond types: O–H (~3300), C=O (~1715), N–H (~3300) |
| Fingerprint region | $400$–$1500\ \text{cm}^{-1}$ | Complex overlapping bends; unique to the whole molecule |

**The data-science bridge — this is the key insight:**

The instrument samples absorbance at $p \approx 1000$ discrete wavenumber points across the spectrum. So:

$$\text{one spectrum} = \begin{pmatrix} A_1 \\ A_2 \\ \vdots \\ A_p \end{pmatrix} \in \mathbb{R}^p$$

One spectrum is one [[vector]] of $p$ absorbance numbers — one point in $p$-dimensional space (see [[what-is-a-dimension]]).

Collect $n$ spectra (one per sample), stack them row by row:

$$\mathbf{X} = \begin{pmatrix} \text{spectrum}_1 \\ \text{spectrum}_2 \\ \vdots \\ \text{spectrum}_n \end{pmatrix} \in \mathbb{R}^{n \times p}$$

This is the [[design-matrix]]. All of chemometrics starts here.

> [!warning] Common confusion
> The fingerprint region ($400$–$1500$ cm⁻¹) is named for its diagnostic *uniqueness*, not because it's the most chemically interpretable region. The functional-group region is actually easier to read manually — the fingerprint region is where computational methods (like PCA) shine.

> [!tip] Why $p \approx 1000$ dimensions?
> Modern FTIR instruments routinely record $1000$–$4000$ wavenumber points per spectrum. Each point is one dimension. The data is high-dimensional by construction, which is exactly why PCA is so valuable here — see [[curse-of-dimensionality]].

## Why this matters for PCA on IR spectra

A spectrum is already a vector, and a dataset of spectra is already a matrix — there is no feature-engineering step. The $p$ wavenumber channels are the $p$ dimensions, and PCA will find the directions in that $p$-dimensional space that explain the most variance across your samples. Because chemically similar samples produce similar spectra, those directions correspond to real chemical structure.

## Builds on
- [[vector]]
- [[what-is-a-dimension]]

## Leads to
- [[beer-lambert-law]]
- [[pca-on-ir-spectra]]
