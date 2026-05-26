# Task 3f — why eigenvector *components* are the sample coordinates

A plain-English companion to the Gram-space step. In 3e you got a sample's coordinates by
*projecting* it onto feature-space directions. In 3f the coordinates fall out **directly** as the
components of the eigenvectors — no projection step. This note explains why that is not a
coincidence but the whole point of the Gram matrix.

## The setup

The Gram matrix is built from sample-to-sample similarities:

$$
\mathbb{G} = \tfrac{1}{\widetilde N}\,\widetilde{\mathbb{X}}\,\widetilde{\mathbb{X}}^\top,
\qquad
G_{ij} = \tfrac{1}{\widetilde N}\,\langle \vec{\tilde x}_i,\ \vec{\tilde x}_j\rangle .
$$

It is $\widetilde N \times \widetilde N$: **one row and one column per sample**, not per feature. Entry
$G_{ij}$ is the dot-product similarity between vials $i$ and $j$.

## The key step: the eigen-decomposition *is* a coordinate factorisation

$\mathbb{G}$ is symmetric and positive semi-definite, so it decomposes into its eigenvectors $\vec u_k$
(with eigenvalues $\lambda_k \ge 0$):

$$
\mathbb{G} = \sum_k \lambda_k\, \vec u_k\,\vec u_k^\top
\qquad\Longrightarrow\qquad
G_{ij} = \sum_k \lambda_k\, (u_k)_i\,(u_k)_j .
$$

Now **define** a coordinate vector for sample $i$ by reading the $i$-th component out of each
eigenvector and scaling by $\sqrt{\lambda_k}$:

$$
\vec y_i = \Big(\sqrt{\lambda_1}\,(u_1)_i,\ \ \sqrt{\lambda_2}\,(u_2)_i,\ \ \dots\Big).
$$

Then the inner product of two of these coordinate vectors is

$$
\langle \vec y_i, \vec y_j\rangle
= \sum_k \big(\sqrt{\lambda_k}(u_k)_i\big)\big(\sqrt{\lambda_k}(u_k)_j\big)
= \sum_k \lambda_k (u_k)_i (u_k)_j
= G_{ij}
$$

**exactly.** So the $\vec y_i$ are genuine coordinates whose dot products reproduce the original
similarities. And by construction:

> **The $i$-th component of eigenvector $\vec u_k$ (scaled by $\sqrt{\lambda_k}$) is the $k$-th
> coordinate of sample $i$.**

That is the answer to "why are the components the coordinates." The decomposition
$\mathbb{G} = \sum_k \lambda_k \vec u_k\vec u_k^\top$ is literally a factorisation of *similarity* into
*coordinates × coordinates*; reading it back gives you the coordinates for free.

Two ways to read the eigenvectors:

| Read… | …and you get |
|---|---|
| **down** one eigenvector $\vec u_k$ (all $\widetilde N$ components) | coordinate $k$ of *every* sample |
| **across** eigenvectors at a fixed index $i$ | the full coordinate vector $\vec y_i$ of sample $i$ |

Each eigenvector has $\widetilde N$ entries — one per sample — so its components are *already indexed by
sample*. There is nothing left to project onto.

## Why this matches the covariance route (3e)

Take the SVD $\widetilde{\mathbb{X}} = \mathbb{U}\Sigma\mathbb{V}^\top$. The two matrices from 3e and 3f are
just the two products you can form:

$$
\underbrace{\widetilde{\mathbb{X}}^\top\widetilde{\mathbb{X}} = \mathbb{V}\Sigma^2\mathbb{V}^\top}_{\text{covariance } \mathbb{C}\ (M\times M)}
\qquad\qquad
\underbrace{\widetilde{\mathbb{X}}\,\widetilde{\mathbb{X}}^\top = \mathbb{U}\Sigma^2\mathbb{U}^\top}_{\text{Gram } \mathbb{G}\ (\widetilde N\times\widetilde N)}
$$

So the Gram eigenvectors are the columns of $\mathbb{U}$. The PCA scores — the coordinates 3e computes
by projecting — are

$$
\widetilde{\mathbb{X}}\,\mathbb{V} = \mathbb{U}\Sigma,
$$

and column $k$ of $\mathbb{U}\Sigma$ is exactly $\sigma_k\,\vec u_k$, i.e. the eigenvector $\vec u_k$ scaled by a
singular value. **Same coordinates, two routes:**

- **3e (covariance):** find the feature-space directions $\vec\nu_k$ first, then *project* each sample
  onto them.
- **3f (Gram):** the scaled eigenvector components *are already* those projected coordinates — you
  skip the directions in feature space entirely.

This is the same $\widetilde{\mathbb{X}}\vec v$ duality from 2d, just read in the other direction. It is
also why the Gram route still works when you only have similarities or distances and never form
explicit feature vectors at all (classical MDS, kernel PCA): the embedding of the points drops out
of the eigenvectors directly.

## One-line takeaway

Eigen-decomposing $\mathbb{G}$ factors sample-to-sample similarity into coordinates times coordinates,
so component $i$ of eigenvector $\vec u_k$ (times $\sqrt{\lambda_k}$) **is** sample $i$'s coordinate
along axis $k$ — the same coordinate 3e gets by projecting, obtained here without any projection.
