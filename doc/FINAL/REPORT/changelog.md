# extras.md — change monitor for `SIMC2026_Preliminary_Q1_Q2.tex`

This file logs **every change** made when turning the handwritten notes into the
LaTeX preliminary report, and flags every **mistake**, **miss**, and **extra**.
Newest changes go at the top of the changelog. The tables below are the
standing record; keep them in sync with the coloured tags in the PDF.

**Source notes (sole basis for the math):**
- `notes/Note 26 May 2026.pdf` — Q1 parts a–b (rough)
- `notes/Note 26 May 2026 (2).pdf` — Q1 parts a–e, g (clean)
- `notes/task 2.pdf` — Q2 parts a–e

**Document built:** `SIMC2026_Preliminary_Q1_Q2.tex` (Q1 & Q2 only; Q3 to come).
**Tag legend (also rendered in the PDF):** 🟥 MISS · 🟧 CORRECTED · 🟦 EXTRA.

---

## 1. 🟧 MISTAKES found in the notes (corrected in the report)

| # | Location | What the notes had | What is correct | Why |
|---|----------|--------------------|-----------------|-----|
| M1 | **Q1(g)** time-varying ε | $\mathbf p(t)=1^{t}c_1+\bigl(1-\varepsilon(t)\bigr)^{t}c_2$ | $\mathbf p(t)=c_1\mathbf v_1+c_2\Bigl[\prod_{s=0}^{t-1}(1-\varepsilon_0e^{-s/t_0})\Bigr]\mathbf v_2$ | With a time-varying rate the matrices $\mathbf M(t)$ differ each step. They share the same eigenvectors (the eigenvectors don't depend on ε), so the $\mathbf v_2$ mode collects **one factor $(1-\varepsilon(s))$ per step** → a *product*, not the power $(1-\varepsilon(t))^t$. |
| M2 | **Q1(c)** linear combination | Used $c_1=1$ directly | $c_1=p_2(0)+\tfrac12$; equals 1 **only if** $p_2(0)=\tfrac12$ | The notes silently assumed the populations are normalised so $p_1(0)+p_2(0)=1$. Now stated explicitly; general form also given. |
| M3 | **Q2(d)(i)** PSD proof | $\mathbf w^\top(\mathbf X^\top\mathbf X)\mathbf w=\lVert \mathbf X^\top\mathbf w\rVert^2$ | $=\lVert \mathbf X\mathbf w\rVert^2$ | Typo: $(\mathbf X^\top\mathbf X)$ pairs with $\lVert\mathbf X\mathbf w\rVert^2$; $\lVert\mathbf X^\top\mathbf w\rVert^2$ belongs to the $\mathbf X\mathbf X^\top$ case. Result (PSD) unaffected. |
| M4 | **Q2(e)(i)** pseudocode label | "if $N\gg M$ compute $\mathbf X\mathbf X^\top$" | "if $N\ge M$ compute $\mathbf X^\top\mathbf X$" (the **smaller** matrix) | The notes' own stated reason ("the smaller matrix is cheaper") and their worked example (3×2 → used $\mathbf X^\top\mathbf X$, the 2×2) both contradict the label. Rule made consistent. |

---

## 2. 🟥 MISSES — parts of Q1/Q2 not yet attempted in the notes

| # | Part | Status | Placeholder in report |
|---|------|--------|------------------------|
| G1 | **Q1(f)** numerical validation of (d)/(e) | not started | Section 1(f): describes the check (iterate `M @ p`, compare to closed form, confirm limit `(0,1)`). **No numbers invented.** To implement in `src/task1.py`. |
| G2 | **Q1(h)** numerical validation of (g) | not started | Section 1(h): same approach with $\varepsilon(t)=\varepsilon_0 e^{-t/t_0}$; check the residual $c_2\Pi_\infty$. To implement in `src/task1.py`. |
| G3 | **Q2(c)(ii)** why vanishing gap is fundamental | marked "explanation" only | Written by me — see Extras E1. |
| G4 | **Q2(c)(iii)** finite-precision risks when $|\lambda_2/\lambda_1|\approx1$ | marked "explanation" only | Written by me — see Extras E2. |

> Q1(f), Q1(h) deliberately left as descriptive placeholders so the report
> contains **no fabricated numerical results**. Fill them once `task1.py` runs.

---

## 3. 🟦 EXTRAS — content added beyond the notes (please verify)

| # | Location | What I added | Risk |
|---|----------|--------------|------|
| E1 | **Q2(c)(ii)** | Full explanation: no "selection mechanism" when amplification factors are equal; oscillation vs degenerate-eigenspace cases. | Conceptual; standard. Low. |
| E2 | **Q2(c)(iii)** | Full explanation: iteration count $\sim 1/(1-\lvert\lambda_2/\lambda_1\rvert)$; $10^{-16}$ rounding competes with the $\lvert\lambda_2/\lambda_1\rvert^k$ signal; ordering ambiguity. | Conceptual; matches the challenge's grey-box note. Low. |
| E3 | **Q1(g)** | Qualitative consequence: the infinite product converges to a **positive** limit $\Pi_\infty$, so type-1 is **not** fully depleted (conversion "switches off"). | A genuine new claim. Mathematically sound (since $\sum\varepsilon(s)<\infty$). **Verify before using in Q&A.** |
| E4 | **Q1(a)** | Added the column-stochastic one-line argument ($\mathbf 1^\top\mathbf M=\mathbf 1^\top$) alongside the induction proof. | Reinforces, doesn't replace. Low. |
| E5 | **Q1(e)(ii)** | Made the limit explicit: $c_1\mathbf v_1=(0,\,p_1(0)+p_2(0))$ — all mass ends as type-2. | Follows directly from (a)+(c). Low. |

---

## 4. ✍️ ELABORATIONS — notes' steps expanded to full rigour (no new claims)

- **Q1(a):** notes said "by deduction"; expanded to an explicit induction on $S(t)=S(t+1)$.
- **Q1(b):** added the lower-triangular observation; wrote out both null-space solves in full.
- **Q1(d):** added the line $\mathbf M^t\mathbf v_i=\lambda_i^t\mathbf v_i$ justifying the scalar powers.
- **Q2(a):** restructured the notes' parallel/residual decomposition into a clean proof; made the requirement $a_1\ne0$ and $|\lambda_1|>|\lambda_2|$ explicit.
- **Q2(b):** wrote the weighted-average bound $\sum\omega_i\lambda_i^2/\sum\omega_i\le\lambda_2^2$ explicitly.
- **Q2(d)(ii):** added the $\mathbf X\mathbf v\ne\mathbf 0$ step (needed for the eigenvector to be valid) and the converse direction.
- **Q2(e)(ii):** added the second verification $\mathbf X^\top\mathbf u_1=\sigma_1\mathbf v_1$ in full (notes showed mainly the first).

---

## 5. 🛠️ STRUCTURE / FORMATTING decisions

- Based on `templates/SIMC2026_Preliminary_Detailed.tex` **preamble** (12pt Times via `mathptmx`, A4, 2 cm margins, `fancyhdr`). Trimmed the 24-section generic scaffold (literature, data provenance, sensitivity, etc.) — **not applicable** to two proof-only questions; will return for Q3.
- Vectors set as bold lowercase ($\mathbf v$), matrices bold uppercase ($\mathbf M,\mathbf X$). Challenge used blackboard $\mathbb{M},\mathbb{X}$; switched to bold for readability — purely cosmetic, flag here in case you want to match the prompt exactly.
- Added three review macros `\miss`, `\fix`, `\extra` that print coloured tags in the PDF, one per item above.
- Kept the preamble minimal per the "keep LaTeX simple for now" instruction.

---

## 6. 🟩 VERIFIED — notes that were checked and are correct as-is

- Q1(b) eigenpairs: $\lambda_1=1,\mathbf v_1=(0,1)$; $\lambda_2=1-\varepsilon,\mathbf v_2=(1,-1)$. ✔
- Q2(c)(i): $\mathbf X^k\mathbf x_0=(a,(-1)^k b)$, oscillates, no convergence. ✔
- Q2(e)(ii) worked example: $\mathbf X^\top\mathbf X=\begin{psmallmatrix}2&1\\1&2\end{psmallmatrix}$, $\lambda=1,3$; $\mathbf v_1=\tfrac1{\sqrt2}(1,1)$, $\sigma_1=\sqrt3$, $\mathbf u_1=\tfrac1{\sqrt6}(1,1,2)$. **Both** $\mathbf X\mathbf v_1=\sigma_1\mathbf u_1$ and $\mathbf X^\top\mathbf u_1=\sigma_1\mathbf v_1$ check out. ✔

---

## 7. Changelog (newest first)

### 2026-05-26 — compiled to PDF
- Compiled with **tectonic 0.16.9** (installed via `brew install tectonic` — no sudo, so MacTeX was not needed). Output: `report.pdf` (also `SIMC2026_Preliminary_Q1_Q2.pdf`), **7 pages**, exit 0.
- Build fix 1: defined missing macro `\yy` (`\mathbf{y}`) — used in the Q2(a) proof but not declared. Was the "Undefined control sequence" error.
- Build fix 2: replaced non-ASCII characters the Times/T1 font can't render — em-dash `—`→`---`, en-dash `–`→`--`, middle-dot `·`→`\textperiodcentered{}`. Cosmetic only; no content changed.

### 2026-05-26 — initial build
- Created `SIMC2026_Preliminary_Q1_Q2.tex` from the three notes PDFs.
- Wrote full proofs for Q1(a–e,g) and Q2(a–e).
- Logged 4 mistakes (M1–M4), 4 misses (G1–G4), 5 extras (E1–E5), 7 elaborations.
- Pending: compile to PDF once MacTeX finishes installing.
