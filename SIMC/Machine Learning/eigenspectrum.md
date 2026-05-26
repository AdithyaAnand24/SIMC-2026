---
tags:
  - simc
---

# Eigenspectrum (scree plot)

> [!abstract] In one line
> Line up all the eigenvalues from biggest to smallest and look at how fast they fall off — that shape tells you how many directions actually matter, reading the data's intrinsic dimension directly from the graph.

## The idea

After PCA hands you a list of eigenvalues, you have a choice: keep all $p$ components (pointless — you haven't reduced anything) or keep some $k$ (the whole payoff). But how do you pick $k$?

The eigenspectrum answers this visually. Picture a bar chart where the first bar is the tallest, the second a bit shorter, and so on. If the bars drop off a cliff after position 3 and then flatline near zero for the remaining 997 — the data genuinely lives in 3 dimensions. The cliff tells you the intrinsic dimension.

This is the [[manifold-hypothesis]] made quantitative: if the eigenspectrum has a sharp elbow at $k$, the manifold is $k$-dimensional. The near-zero eigenvalues aren't extra information — they're noise.

The plot of $\lambda_i$ vs $i$ is called a **scree plot** (named after the rubble at the foot of a cliff — the flat tail IS the scree).

## The math

Let $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p \ge 0$ be the eigenvalues of the [[covariance-matrix]], sorted descending.

**Variance explained by component $i$:**

$$\text{VE}_i = \frac{\lambda_i}{\displaystyle\sum_{j=1}^{p} \lambda_j}$$

This is a fraction between 0 and 1 (multiply by 100 for percent). It answers: "what share of total data spread does PC $i$ capture?"

**Cumulative variance explained by the top $k$ components:**

$$\text{CVE}(k) = \frac{\displaystyle\sum_{i=1}^{k} \lambda_i}{\displaystyle\sum_{j=1}^{p} \lambda_j}$$

**Common thresholds used in practice:**
- Keep enough PCs so $\text{CVE}(k) \ge 0.95$ (95% of variance)
- Or find the "elbow" — the $k$ where $\lambda_{k+1}$ drops sharply relative to $\lambda_k$

> [!note] Why eigenvalues = variance
> Recall from [[eigenvectors-of-the-covariance-matrix]]: when you project the centered data onto eigenvector $\mathbf{v}_k$, the variance of those projected values (the scores) equals exactly $\lambda_k$. So the eigenvalue spectrum IS the variance spectrum. Bigger eigenvalue = more informative direction.

**The scree plot** is simply:

```python
import matplotlib.pyplot as plt  # [[matplotlib-basics]]
plt.plot(range(1, len(eigenvalues)+1), eigenvalues, 'o-')
plt.xlabel('Component index')
plt.ylabel('Eigenvalue (variance)')
plt.title('Scree plot')
```

Look for the "elbow" — the point where the curve bends from steep to flat. That's $k$.

> [!warning] Common confusion
> The elbow isn't always obvious. If the data truly has no low-dimensional structure, the eigenspectrum decays smoothly with no cliff. In that case PCA won't compress well — but this is rare for real spectroscopy data, which almost always has a sharp elbow (chemistry has far fewer degrees of freedom than wavelengths).

> [!example] IR spectra eigenspectrum
> A dataset of 200 IR spectra with 1000 wavelength channels might produce eigenvalues like: $\lambda_1 = 4200$, $\lambda_2 = 890$, $\lambda_3 = 210$, $\lambda_4 = 8$, $\lambda_5 = 7$, ..., $\lambda_{1000} \approx 0$. CVE(3) = $(4200+890+210)/(4200+890+210+\dots) \approx 0.97$. Keep 3 PCs. The cliff is between PC 3 and PC 4.

> [!tip] CVE curve is the companion plot
> Plot CVE(k) vs k alongside the scree plot. It's monotonically increasing from 0 to 1. The $k$ where it crosses 0.95 (or 0.99) is your answer if the elbow is ambiguous.

## Why this matters for PCA on IR spectra

For IR spectra, the eigenspectrum is diagnostic of the chemistry. A single dominant eigenvalue means one chemical factor (e.g. one compound's concentration) drives almost all variation. Two large eigenvalues might mean two compounds co-vary. The eigenspectrum also tells you whether your [[curse-of-dimensionality|dimensionality problem]] is actually solvable: if the first 3–5 PCs capture 95%+, you've confirmed the data truly lives on a low-dimensional manifold and downstream models will be reliable.

## Builds on
- [[eigenvectors-of-the-covariance-matrix]]
- [[principal-component-analysis]]
- [[covariance-matrix]]
- [[manifold-hypothesis]]

## Leads to
- [[dimensionality-reduction]]
