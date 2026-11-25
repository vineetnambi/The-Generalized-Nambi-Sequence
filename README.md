# The Generalized Nambi Sequence: Cyclic Orbits of $d$-Digit Numbers in Arbitrary Bases

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24530328.svg)](https://doi.org/10.5281/zenodo.24530328)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0007--3200--3221-green.svg)](https://orcid.org/0009-0007-3200-3221)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/vineetnambi/The-Generalized-Nambi-Sequence)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Archival Links & Metadata

* **Author:** Vineet Nambi
* **ORCID:** [0009-0007-3200-3221](https://orcid.org/0009-0007-3200-3221)
* **Permanent Archive (Zenodo):** [doi:10.5281/zenodo.24530328](https://doi.org/10.5281/zenodo.24530328)
* **Zenodo Record:** [https://zenodo.org/records/24530328](https://zenodo.org/records/24530328)
* **GitHub Repository:** [https://github.com/vineetnambi/The-Generalized-Nambi-Sequence](https://github.com/vineetnambi/The-Generalized-Nambi-Sequence)
* **Foundational Two-Digit Paper:** [doi:10.5281/zenodo.19483055](https://doi.org/10.5281/zenodo.19483055)

---

## Overview

This repository contains the theory and reference Python implementation of the **Generalized Nambi Sequence**—denoted the $(b, d)$**-Nambi Sequence**—for any numerical base $b \ge 3$ and any digit length $d \ge 2$, along with its divisor-modulus ($m \mid (b - 1)$), zero-inclusive ($m = b$), and Left-Shift mirror extensions.

Originally formulated for two-digit Base-10 numbers ($(10, 2)$) as a physical, generative mechanism for the modulo $9$ Fibonacci orbit structure, this generalized framework extends digital root concatenation to $d$-step Fibonacci ($d$-bonacci) recurrences across a closed $(b - 1)^d$-state universe.

---

## Mathematical Foundations

For a fixed base $b \ge 3$ (with canonical modulus $m = b - 1$) and digit length $d \ge 2$, the sequence operates on $d$-digit Base-$b$ integers whose digits are strictly drawn from $\{1, 2, \dots, b - 1\}$. Excluding the digit `0` preserves a closed, reversible modular system. *(In the canonical regime, Binary,* $b = 2$*, is the sole degenerate exception, collapsing to a single state modulo* $1$*.)*

At each step, the Base-$b$ digital root of the sum of all $d$ digits becomes the new leading digit, while the first $d - 1$ digits shift one position to the right.

### Universal Bidirectional Generator Formulas

Because every Base-$b$ integer is congruent modulo $b - 1$ to the sum of its Base-$b$ digits, both the forward ($N_{\text{next}}$) and backward ($N_{\text{prev}}$) transitions can be computed directly from $N$ without tracking the underlying additive sequence:

* **Forward Function ($N_{\text{next}}$):**
  $$N_{\text{next}} = b^{d-1} \cdot \Big(1 + \big((N - 1) \bmod (b - 1)\big)\Big) + \left\lfloor \frac{N}{b} \right\rfloor$$

* **Backward Function ($N_{\text{prev}}$):**
  $$N_{\text{prev}} = b \cdot \left(N \bmod b^{d-1}\right) + \left(\left(\left\lfloor \frac{N}{b^{d-1}} \right\rfloor - \big((N \bmod b^{d-1}) \bmod (b - 1)\big) + (b - 2)\right) \bmod (b - 1)\right) + 1$$

---

### Linear Dynamical Formulation and Companion Matrices

The sequence can be formally modeled as an autonomous linear dynamical system over the finite commutative ring $\mathbb{Z}_m$:

$$\mathbf{v}_{n+1} \equiv \mathbf{C}_R \, \mathbf{v}_n \pmod{m}$$

where $\mathbf{C}_R \in \mathcal{M}_{d \times d}(\mathbb{Z}_m)$ is the recurrence companion matrix:

$$\mathbf{C}_R = \begin{pmatrix}
1 & 1 & 1 & \cdots & 1 & 1 \\
1 & 0 & 0 & \cdots & 0 & 0 \\
0 & 1 & 0 & \cdots & 0 & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & \cdots & 1 & 0
\end{pmatrix}$$

#### Key Linear Algebraic Theorems

1. **Invertibility in $\mathrm{GL}_d(\mathbb{Z}_m)$:** The characteristic polynomial is $p(\lambda) = \lambda^d - \sum_{j=0}^{d-1} \lambda^j$, yielding $\det(\mathbf{C}_R) = (-1)^{d-1} = \pm 1$. Because $\gcd(\pm 1, m) = 1$ for all $m \ge 2$, $\mathbf{C}_R \in \mathrm{GL}_d(\mathbb{Z}_m)$. This guarantees that every state belongs to a pure, reversible periodic cycle with zero transient tails.
2. **Singularity Law via Nullspace:** Fixed points satisfy $(\mathbf{C}_R - \mathbf{I}_d)\mathbf{v} \equiv \mathbf{0} \pmod m$. The rows force all digits to be identical ($x$), requiring $(d - 1)x \equiv 0 \pmod m$. The order of $\ker(\mathbf{C}_R - \mathbf{I}_d)$ is strictly $\gcd(d - 1, m)$.
3. **Similarity Under Exchange Matrix:** Letting $\mathbf{J}_d$ be the $d \times d$ anti-diagonal exchange matrix, $\mathbf{J}_d \mathbf{C}_R \mathbf{J}_d = \mathbf{C}_L$. Because $\mathbf{C}_L$ and $\mathbf{C}_R$ are similar matrices conjugate via $\mathbf{J}_d$, both shift directions share identical spectra, invariant factors, and cycle-length distributions.

---

### Shift Orientation Duality (Right-Shift vs. Left-Shift)

* **Right-Shift / MSB-Insertion ($T_R$):** Inserts the new digital root at the most significant position ($b^{d-1}$) and drops the units digit via $\lfloor N / b \rfloor$ (e.g., `11 -> 21 -> 32 -> 53`).
* **Left-Shift / LSB-Insertion ($T_L$):** Inserts the new digital root at the least significant position ($b^0$) and drops the leading digit via $N \bmod b^{d-1}$ (e.g., `11 -> 12 -> 23 -> 35`).

#### Unified Parameterized Formulas ($\delta \in \{0, 1\}$)

Let $\delta = 0$ select Right-Shift ($T_R$) and $\delta = 1$ select Left-Shift ($T_L$). For any divisor modulus $m \mid (b - 1)$:

* **Unified Forward Function:**
  $$N_{\text{next}}^{(\delta)} = b^{(1-\delta)(d-1)} \cdot \Big(1 + \big((N - 1) \bmod m\big)\Big) + (1 - \delta)\left\lfloor \frac{N}{b} \right\rfloor + \delta \cdot b \left(N \bmod b^{d-1}\right)$$

* **Unified Backward Function:** Letting $(q_0, r_0) = (\lfloor N / b^{d-1} \rfloor,\; N \bmod b^{d-1})$ and $(q_1, r_1) = (N \bmod b,\; \lfloor N / b \rfloor)$:
  $$N_{\text{prev}}^{(\delta)} = b^{\delta(d-1)} \cdot \Big(\big((q_\delta - r_\delta - 1) \bmod m\big) + 1\Big) + b^{1-\delta} \cdot r_\delta$$

* **Digit-Reversal Conjugacy:** Letting $R(a_1 a_2 \dots a_d) = a_d \dots a_2 a_1$, the two maps satisfy $T_L = R \circ T_R \circ R$. Consequently, both orientations preserve cycle lengths, repdigit milestones, and repunit loop sums.

---

### Core Theorems

1. **Generalized Repunit Summation Theorem:** For any closed loop of period $k$ in the $(b, d)$-Nambi Sequence, the sum $L_{b, d}$ of all terms in the loop equals the Base-$b$ $d$-digit repunit multiplied by the sum of its single-digit roots:
   $$L_{b, d} = \left(\frac{b^d - 1}{b - 1}\right) \sum_{i=1}^{k} R_i$$
   For $(10, 2)$, the multiplier is `11` (yielding `1287` for the standard 24-step orbits). For $(10, 3)$, it is `111`; for $(8, 2)$, it is `9` ($11_8$).

2. **Singularity Characterization:** The exact number of 1-step singularities in any $(b, d)$-universe is $\gcd(d - 1,\; b - 1)$.

---

### Modulus Selection and the $m \mid (b - 1)$ Condition

The canonical modulus $m = b - 1$ is the unique choice in Base $b$ that simultaneously uses the entire non-zero digit set $\{1, \dots, b - 1\}$, prevents transient orphan states, and supports the closed-form $N_{\text{next}}$ shortcut.

| Modulus Regime | Closed-Form $N_{\text{next}}$? | Repunit Sum Theorem? | Orphan States? | Structural Behavior |
| :--- | :---: | :---: | :---: | :--- |
| **Canonical ($m = b - 1$)** | **Yes** | **Yes** | **None** | Full $(b - 1)^d$ closed, reversible universe. |
| **Divisor ($m \mid (b - 1),\; m < b - 1$)** | **Yes** | **Yes** | Yes | Contracts to an $m^d$-state core. Digits $> m$ form transient entry tails. |
| **Non-Divisor ($m < b - 1,\; m \nmid (b - 1)$)** | No | **Yes** | Yes | Digits must be extracted before summing. Core orbits are isomorphic to $(m + 1, d)$. |
| **Full-Base ($m = b$, zero-inclusive)** | No | **Yes** | **None** | Partitions all $b^d$ states over $\{0, \dots, b - 1\}$ into pure loops; turns Binary into an LFSR. |

---

### Verified Cross-Base Orbit Partitions

#### Canonical Modulus ($m = b - 1$, Non-Zero Alphabet)

| System $(b, d)$ | Mod $(b - 1)$ | Total States $(b - 1)^d$ | Singularities | Orbit Partition (`length × count`) |
| :--- | :---: | :---: | :---: | :--- |
| **Base 2 (Binary), any $d$** | 1 | 1 | 1 | `1 × 1` (degenerate collapse) |
| **Base 3 (Ternary), $d = 2$** | 2 | 4 | 1 | `1 × 1`, `3 × 1` |
| **Base 3 (Ternary), $d = 3$** | 2 | 8 | 2 | `1 × 2`, `2 × 1`, `4 × 1` |
| **Base 8 (Octal), $d = 2$** | 7 | 49 | 1 | `1 × 1`, `16 × 3` |
| **Base 8 (Octal), $d = 3$** | 7 | 343 | 1 | `1 × 1`, `6 × 1`, `48 × 7` |
| **Base 10 (Decimal), $d = 2$** | 9 | 81 | 1 | `1 × 1`, `8 × 1`, `24 × 3` |
| **Base 10 (Decimal), $d = 3$** | 9 | 729 | 1 | `1 × 1`, `13 × 2`, `39 × 18` |
| **Base 16 (Hex), $d = 2$** | 15 | 225 | 1 | `1 × 1`, `4 × 1`, `8 × 5`, `20 × 1`, `40 × 4` |

#### Zero-Inclusive Modulus ($m = b$, Full $b^d$ Universe)

| System $(b, d)$ | Mod $b$ | Total States $b^d$ | Singularities $\gcd(d - 1, b)$ | Orbit Partition (`length × count`) |
| :--- | :---: | :---: | :---: | :--- |
| **Base 2 (Binary), $d = 2$** | 2 | 4 | 1 (`00`) | `1 × 1`, `3 × 1` |
| **Base 2 (Binary), $d = 3$** | 2 | 8 | 2 (`000`, `111`) | `1 × 2`, `2 × 1`, `4 × 1` |
| **Base 2 (Binary), $d = 4$** | 2 | 16 | 1 (`0000`) | `1 × 1`, `5 × 3` |
| **Base 3 (Ternary), $d = 2$** | 3 | 9 | 1 (`00`) | `1 × 1`, `8 × 1` |
| **Base 8 (Octal), $d = 2$** | 8 | 64 | 1 (`00`) | `1 × 1`, `3 × 1`, `6 × 2`, `12 × 4` |
| **Base 8 (Octal), $d = 3$** | 8 | 512 | 2 (`000`, `444`) | `1 × 2`, `2 × 1`, `4 × 3`, `8 × 14`, `16 × 24` |
| **Base 10 (Decimal), $d = 2$** | 10 | 100 | 1 (`00`) | `1 × 1`, `3 × 1`, `4 × 1`, `12 × 1`, `20 × 1`, `60 × 1` |
| **Base 10 (Decimal), $d = 3$** | 10 | 1,000 | 2 (`000`, `555`) | `1 × 2`, `2 × 1`, `4 × 1`, `31 × 8`, `62 × 4`, `124 × 4` |
| **Base 16 (Hex), $d = 2$** | 16 | 256 | 1 (`00`) | `1 × 1`, `3 × 1`, `6 × 2`, `12 × 4`, `24 × 8` |

---

## OEIS Connections

| Sequence | Title / Subject | Role in the $(b, d)$-Nambi System |
| :--- | :--- | :--- |
| [A001175](https://oeis.org/A001175) | Pisano periods: period of Fibonacci numbers $\bmod n$ | Primary orbit length for $d = 2$ in Base $b$ at $n = b - 1$ ($a(9) = 24$, $a(7) = 16$). |
| [A015134](https://oeis.org/A015134) | Number of different periods of Fibonacci-type sequences $\bmod n$ | Exact total number of orbits for $d = 2$ at $n = b - 1$ ($a(9) = 5$, $a(7) = 4$). |
| [A046738](https://oeis.org/A046738) | Tribonacci Pisano periods: period of A000073 $\bmod n$ | Primary orbit length for $d = 3$ at $n = b - 1$ ($a(9) = 39$, $a(7) = 48$). |
| [A046737](https://oeis.org/A046737) | Reduced period of Tribonacci numbers $\bmod n$ | Governs 13-step internal milestone symmetry ($111 \to 444 \to 777$). |
| [A106288](https://oeis.org/A106288) | Number of distinct orbit lengths of 3-step recursion $\bmod n$ | Orbit-length diversity in $d = 3$ universes (for $n = 9$: lengths 1, 13, 39). |
| [A000078](https://oeis.org/A000078) | Tetranacci numbers (4-step Fibonacci recurrence) | Governs $d = 4$ orbits; period modulo 9 is 78 (see also [A106295](https://oeis.org/A106295)). |

---

## Usage

### Prerequisites

* Python 3.10+ (standard library only; no external packages required).

### Running the Generator Script

```bash
python nambi_sequence_general_v5.py
```

The script interactively supports:
1. **Regime Selection:** Canonical ($m = b - 1$), Divisor ($m \mid (b - 1)$), or Zero-Inclusive ($m = b$).
2. **Orientation Selection:** Right-Shift ($T_R$), Left-Shift ($T_L$), or Side-by-Side Dual-Shift Comparison.
3. **Orbit Navigation:** Tracing forward ($N_{\text{next}}$) and backward ($N_{\text{prev}}$) from any valid seed.
4. **Universe Mapping:** High-speed 1-bit-per-state bitset mapping (~125 KB RAM per 1,000,000 states) with optional disk streaming.

---

## Citation

If you use this work, the code, or reference the Generalized Nambi Sequence in your research, please cite:

```bibtex
@misc{nambi2026generalized,
  author       = {Nambi, Vineet},
  title        = {The Generalized Nambi Sequence: Cyclic Orbits of d-Digit Numbers in Arbitrary Bases},
  year         = {2026},
  month        = may,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.24530328},
  url          = {https://doi.org/10.5281/zenodo.24530328},
  howpublished = {\url{https://github.com/vineetnambi/The-Generalized-Nambi-Sequence}}
}
```

### Related Works

* V. Nambi, *The Nambi Sequence: Cyclic Sequences of Two-Digit Numbers and Their Summation Invariants*, Zenodo, 2026. DOI: [10.5281/zenodo.19483055](https://doi.org/10.5281/zenodo.19483055).

---

## License

This project is open-source and distributed under the [MIT License](LICENSE).