# Tasks 3g & 3h — explained

A plain-English companion to the last two parts of Question 3. 3g asks you to *compare* the two
clustering routes you already built (covariance in 3e, Gram in 3f). 3h is the payoff: use
everything to answer "how many unique food samples were there really?"

---

## 3g) Comparing the Two Approaches [3 points]

### The two routes you are comparing

| | 3e — covariance space | 3f — Gram space |
|---|---|---|
| matrix | $\mathbb{C} = \tfrac{1}{\widetilde N}\widetilde{\mathbb{X}}^\top\widetilde{\mathbb{X}}$ | $\mathbb{G} = \tfrac{1}{\widetilde N}\widetilde{\mathbb{X}}\widetilde{\mathbb{X}}^\top$ |
| size | $M \times M$ (feature space, $M=3041$) | $\widetilde N \times \widetilde N$ (sample space) |
| eigenvectors live in | feature space (combinations of frequencies) | sample space (one component per sample) |
| a sample's coordinates | its projections $\vec{\tilde x}_i\cdot\vec\nu_k$ onto the top eigenvectors | read **directly** off the eigenvector components |

### Why the two give the *same* answer (the math connection)

This is exactly the result from **Question 2d**. If $\vec v$ is an eigenvector of $\mathbb{C}$ with
eigenvalue $\lambda$, then left-multiplying by $\widetilde{\mathbb{X}}$ shows $\widetilde{\mathbb{X}}\vec v$ is an
eigenvector of $\mathbb{G}$ with the **same** eigenvalue $\lambda$:

$$
\mathbb{C}\vec v = \lambda\vec v
\;\Longrightarrow\;
\mathbb{G}\,(\widetilde{\mathbb{X}}\vec v) = \tfrac{1}{\widetilde N}\widetilde{\mathbb{X}}\widetilde{\mathbb{X}}^\top\widetilde{\mathbb{X}}\vec v
= \widetilde{\mathbb{X}}\,(\mathbb{C}\vec v) = \lambda\,(\widetilde{\mathbb{X}}\vec v).
$$

So $\mathbb{C}$ and $\mathbb{G}$ share the same nonzero eigenvalues — they are **two views of one underlying
structure**. The coordinates a sample gets in 3e and the coordinates it gets in 3f are related by
exactly this $\widetilde{\mathbb{X}}\vec v$ map (up to a $1/\sigma$ rescaling and a possible sign flip).
That is why **you should find the same number of clusters both ways** — task (i). Any small
visual differences come only from numerics: the two matrices are built and diagonalised
differently, and one may have a friendlier condition number, so its eigenvectors are estimated more
cleanly.

### Task (ii) — what "belonging to a cluster" *means* in each space

This is the conceptual heart of 3g. Both routes cluster the same vials, but the **coordinates**
they use are different in kind:

**(a) Covariance space (3e).** A sample's coordinates are *how strongly it expresses each pattern
of variation*. Each eigenvector $\vec\nu_k$ is a direction in feature space — a particular weighted
combination of the 3041 frequencies, i.e. a spectral "shape." The coordinate $\vec{\tilde x}_i\cdot\vec\nu_k$
says how much of that shape sample $i$ contains. **Belonging to a cluster = having a similar
chemical fingerprint**: two vials are close because their spectra are built from the same mix of
spectral features.

**(b) Gram space (3f).** Here the coordinates come straight from sample-to-sample similarity. The
entry $G_{ij}$ is the dot-product similarity between vials $i$ and $j$; each row of $\mathbb{G}$ is one
vial's "similarity fingerprint" to every other vial. The eigenvectors are already
$\widetilde N$-dimensional, so each component *is* a sample's coordinate. **Belonging to a cluster =
being highly similar to the same group of vials**: proximity means "these vials look like each
other," measured directly, without ever naming a feature direction.

> **One-line contrast.** Covariance space asks *"which spectral patterns does this vial contain?"*;
> Gram space asks *"which other vials does this one resemble?"* Same clusters, because resembling
> the same vials and containing the same patterns are two descriptions of the same fact.

---

## 3h) The forgetful taste tester [6 points]

This is the synthesis question. The story: 1000 vials, labels lost; **fewer than 100** unique
samples (each vial holds one sample); samples are fermented caffeinated drinks; the IR spectroscopy
was tuned to **ten** dominant molecules (water, ethanol, methanol, caffeine, propionic/formic/
lactic/acetic acid, glycerol, acetaldehyde).

### Task (i) — how many unique samples were there *actually*? [4 points]

**The core idea: one unique sample → one cluster.** Each of the unique recipes was poured into
several vials and measured repeatedly. Repeated measurements of the *same* sample differ only by
noise, so they land in a tight clump in PCA/Gram space. **The number of distinct clusters in your
scatter plots is the number of unique samples.** You read it off the 3e/3f projections, and 3g
gives you a free cross-check: the covariance and Gram routes should agree on the count.

**The trap to avoid — dimensionality is not the same as the number of samples.** There are two
different "counts" floating around in this problem, and they answer different questions:

| Count | What produces it | Roughly equals |
|---|---|---|
| **intrinsic dimension** = number of *signal* eigenvalues (the elbow $k^\star$ from 3c) | the **10 molecules** | $\approx 10$ |
| **number of clusters** = number of distinct clumps in the projections | the **unique recipes** | the answer to (i), $< 100$ |

Why the intrinsic dimension is set by the molecules: by the Beer–Lambert idea, every spectrum is a
**linear mixture of the ten pure-molecule spectra**. So the whole cleaned dataset lives (up to
noise) in a subspace of dimension about 10 — that is what the eigenspectrum elbow in 3c is telling
you. But within that ~10-dimensional subspace, the vials still group into however many *distinct
mixtures* (recipes) were actually poured. **Don't report "10" as the number of samples** — 10 is
the number of chemical building blocks, not the number of drinks.

**How to justify the count (what to actually show):**

1. Confirm the data is clean (3a removed the noise-only vials and the second error) and
   mean-centred (3b).
2. Use the eigenspectrum/elbow (3c) to argue the signal lives in $\sim$10 dimensions, consistent
   with the ten molecules — this validates the physics and tells you how many eigenvectors are worth
   projecting onto.
3. Project onto the top eigenvectors and **count the clusters** in the 3e scatter grid; repeat in
   Gram space (3f); show the two agree (3g). That agreed-upon cluster count is your answer, and it
   should come out below the stated bound of 100.

(The exact number is whatever your cleaned data shows — read it off your own cluster plots; this
note explains the reasoning, not a pre-computed figure.)

### Task (ii) — which earlier parts were useful? [2 points]

A short "audit trail" of how the whole competition feeds the answer:

- **3a — error removal:** counting clusters only works on clean data; corrupted/noise-only vials
  would masquerade as a spurious cluster.
- **3b — variance / mean-centring:** centring is what makes the covariance capture *differences
  between* samples rather than the shared average spectrum.
- **3c — eigenspectrum + elbow:** gives the intrinsic dimensionality ($\approx$10 molecules) and how
  many eigenvectors to keep before projecting.
- **3d — leading eigenvector:** confirms the dominant directions correspond to real molecular
  signatures, not artefacts.
- **3e / 3f — clustering two ways:** the actual cluster count = the number of unique samples.
- **3g — covariance vs Gram agreement:** an independent cross-check that the count is real and not a
  numerical artefact of one particular matrix.
- **Question 2 (Power Method / SVD):** the engine that extracts the dominant eigenvectors of these
  large matrices, and the 2d result that makes the covariance and Gram views interchangeable.
- **Question 1 (dominant eigenvector = what matters):** the founding principle that a few special
  directions capture a whole system's behaviour — here, a few directions capture which drink is
  which.

> **One-line takeaway for 3h.** The 10 molecules set the *dimension* of the data; the unique recipes
> set the *number of clusters*. Clean the data, confirm the ~10-D signal subspace, then count the
> clusters in the projections (cross-checked across covariance and Gram space) — that count, below
> 100, is the number of unique samples.
