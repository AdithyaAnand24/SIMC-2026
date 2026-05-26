# Task 2e — understanding the numerical verification

A plain-English companion to the hand calculation in `task1_guide.tex` (section 2e),
focused on the vector $\tfrac{1}{\sqrt2}(1,1)$ and why the two verification lines work.

## The setup

We apply the Power-Method / SVD recipe by hand to the rectangular matrix

$$
\mathbb{X} = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}
\qquad (N=3 \text{ rows},\ M=2 \text{ columns}).
$$

Because $M=2 < N=3$, we iterate on the smaller symmetric matrix $\mathbb{X}^\top\mathbb{X}$:

$$
\mathbb{X}^\top\mathbb{X} = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix},
\qquad \text{eigenvalues } \{3,\,1\},
\qquad \sigma_1 = \sqrt{3}.
$$

The three numbers we extract:

| Quantity | Value | What it is |
|---|---|---|
| $\sigma_1$ | $\sqrt{3}$ | largest singular value (the stretch factor) |
| $\vec v_1$ | $\tfrac{1}{\sqrt2}(1,1)$ | unit **right** singular vector (input direction) |
| $\vec u_1$ | $\tfrac{1}{\sqrt6}(1,1,2)$ | unit **left** singular vector (output direction) |

## Where $\tfrac{1}{\sqrt2}(1,1)$ comes from

Solving $(\mathbb{X}^\top\mathbb{X} - 3I)\vec v = \vec 0$ only gives a **direction**: "equal parts
of both components," i.e. the arrow pointing diagonally along $(1,1)$.

A singular vector must have length exactly 1 (that's the convention — singular vectors are
pure direction-markers with no size). The arrow $(1,1)$ is too long: by Pythagoras its length
is $\sqrt{1^2+1^2} = \sqrt2$. So we shrink it by dividing by $\sqrt2$:

$$
\vec v_1 = \frac{1}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix},
\qquad \lVert\vec v_1\rVert^2 = \tfrac12(1+1) = 1. \ \checkmark
$$

**The $\tfrac{1}{\sqrt2}$ is just a shrink factor that makes the arrow the right size — nothing more.**

## What the verification is actually checking

The SVD claims $\mathbb{X}$ has a special pair of directions glued together:

- an **input** direction $\vec v_1$ (our $\tfrac{1}{\sqrt2}(1,1)$), and
- an **output** direction $\vec u_1$.

The claim, in words:

> $\mathbb{X}$ takes the input arrow, **stretches it by $\sigma_1 = \sqrt3$**, and the result points
> exactly along the output arrow. Its transpose $\mathbb{X}^\top$ does the **reverse trip**: it takes
> the output arrow, stretches by the same $\sqrt3$, and lands back on the input arrow.

We computed $\sigma_1$, $\vec v_1$, $\vec u_1$ by one route; the verification plugs them back in
and confirms they obey this relationship.

### Check 1 — the forward trip: $\mathbb{X}\vec v_1 = \sigma_1\vec u_1$

$$
\mathbb{X}\vec v_1 = \frac{1}{\sqrt2}\begin{pmatrix}1\\1\\2\end{pmatrix},
\qquad
\sigma_1\vec u_1 = \sqrt3\cdot\frac{1}{\sqrt6}\begin{pmatrix}1\\1\\2\end{pmatrix}
= \frac{1}{\sqrt2}\begin{pmatrix}1\\1\\2\end{pmatrix}. \ \checkmark
$$

(using $\sqrt3/\sqrt6 = 1/\sqrt2$.)

### Check 2 — the reverse trip: $\mathbb{X}^\top\vec u_1 = \sigma_1\vec v_1$

Compute each side **independently**, then compare:

$$
\underbrace{\mathbb{X}^\top\vec u_1 = \frac{1}{\sqrt6}\begin{pmatrix}1+0+2\\0+1+2\end{pmatrix} = \frac{3}{\sqrt6}\begin{pmatrix}1\\1\end{pmatrix}}_{\text{arithmetic}}
\qquad
\underbrace{\sigma_1\vec v_1 = \sqrt3\cdot\frac{1}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix} = \frac{\sqrt3}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix}}_{\text{what the claim predicts}}
$$

## Why both sides are written as $\tfrac{3}{\sqrt6}$

The two results *look* different — "$\sqrt3$ over $\sqrt2$" versus "$3$ over $\sqrt6$" — but they are
the **same number in disguise**. Multiply the first top-and-bottom by $\sqrt3$:

$$
\frac{\sqrt3}{\sqrt2} = \frac{\sqrt3\cdot\sqrt3}{\sqrt2\cdot\sqrt3} = \frac{3}{\sqrt6}.
$$

The guide deliberately rewrites both sides in the identical $\tfrac{3}{\sqrt6}$ form so the match is
visible **at a glance**, instead of forcing the reader to simplify a surd in their head. Once both
sides read $\tfrac{3}{\sqrt6}(1,1)$, the equation is verified: the matrix really does behave the way
the SVD says.

## One-line takeaway

You found $\sigma_1, \vec v_1, \vec u_1$ by one route, then confirmed they satisfy the defining SVD
relationship by plugging them back in and watching **both sides land on the same vector**. The
$\tfrac{1}{\sqrt2}$ is only there to keep $\vec v_1$ unit length.
