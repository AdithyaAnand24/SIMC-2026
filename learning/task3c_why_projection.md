# Task 3c — why we project onto directions

A plain-English companion to section 3c ("Computing the Eigenspectrum"). The whole part hinges
on one move: **projecting each measurement onto a direction and looking at the spread of the
results.** This note explains why that move is the heart of PCA.

## The objects in play

After cleaning and mean-centering, the data is the matrix $\widetilde{\mathbb{X}}$ of size
$\widetilde N \times M$ — one row $\vec{\tilde x}_i \in \mathbb{R}^M$ per sample (here $M = 3041$
frequencies). The **covariance matrix** is

$$
\mathbb{C} = \frac{1}{\widetilde N}\,\widetilde{\mathbb{X}}^\top\widetilde{\mathbb{X}}
\qquad (M \times M,\ \text{symmetric, PSD}).
$$

We never look at the 3041 raw numbers of a sample directly. Instead we ask a simpler question
over and over: *along this one direction, how much does the data vary?*

## What "projecting" actually means

Pick a direction — a unit vector $\vec w \in \mathbb{R}^M$. Projecting a measurement onto it is just
a dot product:

$$
z_i = \vec{\tilde x}_i \cdot \vec w.
$$

This collapses a 3041-dimensional point down to **one number**: its coordinate along $\vec w$.
Think of it as the shadow the data point casts on the $\vec w$-axis. Do this for all
$\widetilde N$ samples and you get a 1-D cloud of shadows $z_1, \dots, z_{\widetilde N}$.

## Why we care about the spread of those shadows

Because the data is mean-centered, the shadows average to zero, so their **variance** is

$$
\operatorname{Var}(z) = \frac{1}{\widetilde N}\sum_{i=1}^{\widetilde N} z_i^2 = \vec w^\top \mathbb{C}\, \vec w.
$$

This is the key identity. It says: *the variance of the data along direction $\vec w$ is exactly
$\vec w^\top\mathbb{C}\vec w$.* A direction with **large** variance is one along which samples spread out
and look different from each other — that is where the *information* lives. A direction with
**tiny** variance is one along which every sample looks the same — it tells you nothing about how
the samples differ. So projecting is how we *measure the usefulness of a direction*.

## Why eigenvectors are the directions we project onto

Now ask the natural question: **which direction has the most variance?** Maximize
$\vec w^\top\mathbb{C}\vec w$ over all unit vectors $\vec w$. This is the Rayleigh quotient from Question 2,
and its answer is the **top eigenvector** $\vec\nu_1$ of $\mathbb{C}$, with maximum value $\lambda_1$.

More generally, plug an eigenvector $\vec w = \vec\nu_k$ into the identity:

$$
\vec\nu_k^\top \mathbb{C}\, \vec\nu_k = \vec\nu_k^\top(\lambda_k\vec\nu_k) = \lambda_k.
$$

**Each eigenvalue is literally the variance of the data along its eigenvector.** That is why we
project onto eigenvectors specifically, and not arbitrary directions:

- The eigenvectors are mutually perpendicular, so each captures a *separate, non-overlapping* slice
  of variation.
- Ranking them by eigenvalue $\lambda_1 \ge \lambda_2 \ge \dots$ ranks the directions from "most
  informative" to "least."
- The total variance (the trace of $\mathbb{C}$) splits cleanly into these pieces:
  $\sum_k \lambda_k = \operatorname{tr}(\mathbb{C})$ — the sanity check in 3c.

Diagonalising $\mathbb{C}$ is therefore nothing but *finding the best directions to project onto*.

## Why this is the whole point of the question

In raw form, a sample is 3041 numbers and you cannot see any structure. PCA says: almost all the
meaningful variation is concentrated along a **few** eigenvector directions (the preamble's central
claim). Projecting onto those few directions replaces 3041 coordinates with a handful that retain
nearly all the variance — and *then* clusters become visible (that is 3e and 3f).

This is exactly why the specific 3c tasks are what they are:

| Task | What it really measures |
|---|---|
| ratio $\lambda_1/\lambda_2$ | how strongly the single top direction dominates |
| eigenvalue spectrum (lin + log) | how variance is distributed across directions |
| the **elbow** $k^\star$ | how many directions are "signal" before the noise tail |
| meaning of a large ratio | a few directions explain the data → strong low-dimensional structure |

## Connection to Questions 1 and 2

- **Q1:** the eigenvector with the largest eigenvalue was the long-time fate of the Markov system.
  Here the eigenvector with the largest eigenvalue is the direction of greatest variation. Same
  principle — *the dominant eigenvector is what matters* — applied to data instead of dynamics.
- **Q2:** maximising $\vec w^\top\mathbb{C}\vec w$ is the Rayleigh quotient, and the Power Method is the
  iterative recipe that finds the maximising $\vec w = \vec\nu_1$ without a full eigendecomposition.

## One-line takeaway

We project because **the variance of the projections measures how informative a direction is**, and
the eigenvectors of $\mathbb{C}$ are precisely the directions that carry the most variance — with each
eigenvalue being that variance. PCA is just choosing the few best directions to project onto.
