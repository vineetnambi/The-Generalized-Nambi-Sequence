# The Generalized Nambi Sequence: Cyclic Orbits of $d$-Digit Numbers in Arbitrary Bases

This repository contains the Python implementation of the **Generalized Nambi Sequence**—denoted the $(b, d)$**-Nambi Sequence**—for any numerical base $b \ge 3$ and any digit length $d \ge 2$, along with its divisor-modulus ($m \mid (b - 1)$), zero-inclusive ($m = b$), and Left-Shift mirror extensions.

Originally formulated for two-digit Base-10 numbers ($(10, 2)$) as a physical, generative mechanism for the modulo $9$ Fibonacci orbit structure cataloged in **OEIS A015134**, this generalized framework extends digital root concatenation to $d$-step Fibonacci ($d$-bonacci) recurrences across a closed $(b - 1)^d$-state universe.

## Mathematical Overview

For a fixed base $b \ge 3$ (with canonical modulus $m = b - 1$) and digit length $d \ge 2$, the sequence operates on $d$-digit Base-$b$ integers whose digits are strictly drawn from $\{1, 2, \dots, b - 1\}$. Excluding the digit `0` preserves a closed, reversible modular system. *(In the canonical regime, Binary,* $b = 2$*, is the sole degenerate exception, collapsing to a single state modulo* $1$*.)*

At each step, the Base-$b$ digital root of the sum of all $d$ digits becomes the new leading digit, while the first $d - 1$ digits shift one position to the right.

### Universal Bidirectional Generator Formulas

Because every Base-$b$ integer is congruent modulo $b - 1$ to the sum of its Base-$b$ digits, both the forward ($N_{\text{next}}$) and backward ($N_{\text{prev}}$) transitions can be computed directly from $N$ without tracking the underlying additive sequence:

* **Forward Function (**$N_{\text{next}}$**):**

  $$
  N_{\text{next}} = b^{d-1} \cdot \Big(1 + \big((N - 1) \bmod (b - 1)\big)\Big) + \left\lfloor \frac{N}{b} \right\rfloor
  $$

* **Backward Function (**$N_{\text{prev}}$**):**

  $$
  N_{\text{prev}} = b \cdot \left(N \bmod b^{d-1}\right) + \left(\left(\left\lfloor \frac{N}{b^{d-1}} \right\rfloor - \big((N \bmod b^{d-1}) \bmod (b - 1)\big) + (b - 2)\right) \bmod (b - 1)\right) + 1
  $$

### Shift Orientation Duality (Right-Shift vs. Left-Shift)

The concatenation rule admits two dual orientations depending on where the newly generated root is inserted:

* **Right-Shift (MSB-Insertion) Nambi Sequence (**$T_R$**):** Inserts the new digital root at the most significant position ($b^{d-1}$) and drops the units digit via $\lfloor N / b \rfloor$ (e.g., `11 -> 21 -> 32 -> 53`).
* **Left-Shift (LSB-Insertion) Nambi Sequence (**$T_L$**):** Inserts the new digital root at the least significant position ($b^0$) and drops the leading digit via $N \bmod b^{d-1}$ (e.g., `11 -> 12 -> 23 -> 35`).

#### Unified Parameterized Formulas ($\delta \in \{0, 1\}$)

Let $\delta = 0$ select Right-Shift ($T_R$) and $\delta = 1$ select Left-Shift ($T_L$). For any divisor modulus $m \mid (b - 1)$:

* **Unified Forward Function:**

  $$
  N_{\text{next}}^{(\delta)} = b^{(1-\delta)(d-1)} \cdot \Big(1 + \big((N - 1) \bmod m\big)\Big) + (1 - \delta)\left\lfloor \frac{N}{b} \right\rfloor + \delta \cdot b \left(N \bmod b^{d-1}\right)
  $$

* **Unified Backward Function:** Letting $(q_0, r_0) = (\lfloor N / b^{d-1} \rfloor,\; N \bmod b^{d-1})$ and $(q_1, r_1) = (N \bmod b,\; \lfloor N / b \rfloor)$:

  $$
  N_{\text{prev}}^{(\delta)} = b^{\delta(d-1)} \cdot \Big(\big((q_\delta - r_\delta - 1) \bmod m\big) + 1\Big) + b^{1-\delta} \cdot r_\delta
  $$

#### Digit-Reversal Conjugacy ($T_L = R \circ T_R \circ R$)

Let $R$ be the $d$-digit reversal operator ($R(a_1 a_2 \dots a_d) = a_d \dots a_2 a_1$). Because digit addition is commutative, $R \circ T_R = T_L \circ R$ holds for every base $b \ge 3$ and digit length $d \ge 2$ (as well as $b \ge 2$ in the zero-inclusive $m = b$ mode). Consequently, both orientations share:

* **Identical Orbit Partitions:** Same number of orbits and exact same cycle lengths.
* **Identical Repunit Loop Sums:** Every mirrored orbit pair sums to the exact same value (e.g., `1,287` for `11`; `19,980` for `111`; `346,632` for `1111`).
* **Identical Palindrome Milestones:** Starting from any palindromic seed, both shifts hit the same repdigit milestones on identical steps (e.g., `1111 -> 7777 -> 4444 -> 1111` at 26-step intervals in the 78-step $(10, 4)$ loop).

### Core Theorems

1. **Generalized Repunit Summation Theorem:** For any closed loop of period $k$ in the $(b, d)$-Nambi Sequence, the sum $L_{b, d}$ of all terms in the loop equals the Base-$b$ $d$-digit repunit multiplied by the sum of its single-digit roots:

   $$
   L_{b, d} = \left(\frac{b^d - 1}{b - 1}\right) \sum_{i=1}^{k} R_i
   $$

   For $(10, 2)$, the multiplier is `11` (yielding `1287` for the standard 24-step orbits). For $(10, 3)$, it is `111`; for $(8, 2)$, it is `9` ($11_8$).

2. **Singularity Characterization:** A state is a 1-step fixed point ($N_{\text{next}} = N$) if and only if all $d$ digits equal a common digit $x \in \{1, \dots, b - 1\}$ satisfying $(d - 1)x \equiv 0 \pmod{b - 1}$. The exact number of 1-step singularities in any $(b, d)$-universe is:

   $$
   \gcd(d - 1,\; b - 1)
   $$

### Modulus Selection and the $m \mid (b - 1)$ Condition

The canonical modulus $m = b - 1$ is the unique choice in Base $b$ that simultaneously uses the entire non-zero digit set $\{1, \dots, b - 1\}$, prevents transient orphan states, and supports the closed-form $N_{\text{next}}$ shortcut.

In general, a Base-$b$ integer $N$ is congruent modulo $m$ to the sum of its digits if and only if $b \equiv 1 \pmod{m}$, which holds precisely when $m \mid (b - 1)$:

| Modulus Regime | Closed-Form $N_{\text{next}}$? | Repunit Sum Theorem? | Orphan States? | Structural Behavior |
| ----- | ----- | ----- | ----- | ----- |
| **Canonical (**$m = b - 1$**)** | Yes | Yes | None | Full $(b - 1)^d$ closed, reversible universe. |
| **Divisor (**$m \mid (b - 1),\; m < b - 1$**)** | Yes | Yes | Yes | Contracts to an $m^d$-state core (e.g., $m = 3$ in Base 10; $m = 3, 5$ in Base 16). Digits $> m$ form transient entry tails. |
| **Non-Divisor (**$m < b - 1,\; m \nmid (b - 1)$**)** | No | Yes | Yes | Digits must be extracted before summing. Core orbits are isomorphic to the $(m + 1, d)$-Nambi Sequence (e.g., $\bmod 8$ in Base 10 mirrors Base 9). |
| **Full-Base (**$m = b$**, zero-inclusive)** | No | Yes | None | Partitions all $b^d$ states over $\{0, \dots, b - 1\}$ into pure loops, but $N \bmod b$ isolates only the units digit. |

### Verified Cross-Base Orbit Partitions (Canonical $m = b - 1$)

| System $(b, d)$ | Mod $(b - 1)$ | Total States $(b - 1)^d$ | Singularities | Orbit Partition (`length x count`) |
| ----- | ----- | ----- | ----- | ----- |
| **Base 2 (Binary), any** $d$ | 1 | 1 | 1 | `1 x 1` (degenerate collapse) |
| **Base 3 (Ternary),** $d = 2$ | 2 | 4 | 1 | `1 x 1`, `3 x 1` |
| **Base 3 (Ternary),** $d = 3$ | 2 | 8 | 2 | `1 x 2`, `2 x 1`, `4 x 1` |
| **Base 8 (Octal),** $d = 2$ | 7 | 49 | 1 | `1 x 1`, `16 x 3` |
| **Base 8 (Octal),** $d = 3$ | 7 | 343 | 1 | `1 x 1`, `6 x 1`, `48 x 7` |
| **Base 10 (Decimal),** $d = 2$ | 9 | 81 | 1 | `1 x 1`, `8 x 1`, `24 x 3` |
| **Base 10 (Decimal),** $d = 3$ | 9 | 729 | 1 | `1 x 1`, `13 x 2`, `39 x 18` |
| **Base 16 (Hex),** $d = 2$ | 15 | 225 | 1 | `1 x 1`, `4 x 1`, `8 x 5`, `20 x 1`, `40 x 4` |

## The Zero-Inclusive Variant ($m = b$) and Binary LFSR Dynamics

Replacing the Base-$b$ digital root ($\bmod (b - 1)$ over $\{1, \dots, b - 1\}$) with the units digit of the digit sum ($\bmod b$ over $\{0, \dots, b - 1\}$) creates a parallel, zero-orphan system across all $b^d$ states:

* **Explicit Transition Rules:** Digits $a_1, \dots, a_d$ are summed explicitly:

  $$
  N_{\text{next}} = b^{d-1} \cdot \left(\left(\sum_{i=1}^{d} a_i\right) \bmod b\right) + \left\lfloor \frac{N}{b} \right\rfloor
  $$

* **Binary (**$b = 2$**) Unlocked:** Modulo $2$ addition reduces to bitwise **XOR**, turning the sequence into a $d$-bit Linear Feedback Shift Register (LFSR) with all-ones feedback taps ($a_{\text{new}} = a_1 \oplus a_2 \oplus \dots \oplus a_d$).
* **Singularity Law & Summation Invariant:** The number of 1-step fixed points becomes $\gcd(d - 1, b)$ (e.g., `000` and `555` in Base 10 for $d = 3$), and the Generalized Repunit Summation Theorem holds identically.

### Verified Zero-Inclusive ($m = b$) Orbit Partitions

| System $(b, d)$ | Total States ($b^d$) | Singularities ($\gcd(d - 1, b)$) | Orbit Partition (`length x count`) |
| ----- | ----- | ----- | ----- |
| **Base 2 (Binary),** $d = 2$ | 4 | 1 (`00`) | `1 x 1`, `3 x 1` |
| **Base 2 (Binary),** $d = 3$ | 8 | 2 (`000`, `111`) | `1 x 2`, `2 x 1`, `4 x 1` |
| **Base 2 (Binary),** $d = 4$ | 16 | 1 (`0000`) | `1 x 1`, `5 x 3` |
| **Base 3 (Ternary),** $d = 2$ | 9 | 1 (`00`) | `1 x 1`, `8 x 1` |
| **Base 8 (Octal),** $d = 2$ | 64 | 1 (`00`) | `1 x 1`, `3 x 1`, `6 x 2`, `12 x 4` |
| **Base 8 (Octal),** $d = 3$ | 512 | 2 (`000`, `444`) | `1 x 2`, `2 x 1`, `4 x 3`, `8 x 14`, `16 x 24` |
| **Base 10 (Decimal),** $d = 2$ | 100 | 1 (`00`) | `1 x 1`, `3 x 1`, `4 x 1`, `12 x 1`, `20 x 1`, `60 x 1` |
| **Base 10 (Decimal),** $d = 3$ | 1,000 | 2 (`000`, `555`) | `1 x 2`, `2 x 1`, `4 x 1`, `31 x 8`, `62 x 4`, `124 x 4` |
| **Base 16 (Hex),** $d = 2$ | 256 | 1 (`00`) | `1 x 1`, `3 x 1`, `6 x 2`, `12 x 4`, `24 x 8` |

## OEIS Connections

Extending the Nambi Sequence to arbitrary bases $b$ and digit widths $d$ provides a direct mechanical model for multiple entries in the On-Line Encyclopedia of Integer Sequences:

| OEIS Entry | Description | Role in the $(b, d)$-Nambi Sequence |
| ----- | ----- | ----- |
| [**A001175**](https://oeis.org/A001175) | Pisano periods: period of Fibonacci numbers mod $n$ | Primary orbit length for $d = 2$ at $n = b - 1$ ($a(9) = 24$, $a(7) = 16$, $a(15) = 40$). |
| [**A015134**](https://oeis.org/A015134) | Number of different periods of Fibonacci-type sequences mod $n$ | Exact total orbit count for $d = 2$ at $n = b - 1$ ($a(9) = 5$, $a(7) = 4$). |
| [**A046738**](https://oeis.org/A046738) | Period of Fibonacci 3-step sequence (A000073) mod $n$ | Primary orbit length for $d = 3$ at $n = b - 1$ ($a(9) = 39$, $a(7) = 48$, $a(2) = 4$). |
| [**A046737**](https://oeis.org/A046737) | Reduced period of A000073 mod $n$ | Internal milestone symmetry for $d = 3$ ($a(9) = 13$ gives `111 -> 444 -> 777 -> 111`). |
| [**A106288**](https://oeis.org/A106288) | Number of distinct orbit lengths of the 3-step recursion mod $n$ | Counts distinct cycle lengths in $(b, 3)$ (for $n = 9$, the 3 lengths are `1`, `13`, `39`). |
| [**A000078**](https://oeis.org/A000078) | Tetranacci numbers (4-step Fibonacci recurrence) | Underlying additive recurrence for $d = 4$. |
| [**A106295**](https://oeis.org/A106295) | Period of Lucas 4-step sequence mod $n$ (matches A000078 mod $n$ for $n < 563$) | Primary orbit length for $d = 4$ at $n = b - 1$ ($a(9) = 78$, $a(7) = 342$). |

## Usage

### Prerequisites

* Python 3.10+ (no external dependencies required).

### Running the Script

```
python nambi_sequence_general.py
```

The interactive menu lets you choose between three modular regimes:

1. **Canonical (**$m = b - 1$**):** Full non-zero digital root system for bases $3$ to $36$.
2. **Divisor Modulus (**$m \mid (b - 1)$**):** Preserves the closed-form $N_{\text{next}}$ shortcut and reports any transient orphan tails for seeds containing digits $> m$.
3. **Zero-Inclusive (**$m = b$**):** Full $b^d$ universe including `0` and unlocking Binary ($b = 2$) LFSR dynamics.

The script uses a compact bitset/bytearray universe mapper and stays open after completing a run so you can inspect the output or start another calculation.

### Example Output (Base 8, $d = 2$, Canonical Mode, Seed `11`)

```
==================================================================
 THE GENERALIZED NAMBI SEQUENCE | Base 8, 2-Digit
 Regime: Canonical (m = b - 1 = 7)
==================================================================
Initial Seed           : 11 (Base 8)
Next Term (N_next)     : 21 (Base 8)
Prev Term (N_prev)     : 17 (Base 8)
Closed Orbit Length    : 16 step(s)
Expected Singularities : gcd(d - 1, m) = gcd(1, 7) = 1
Loop Sum (Base 10)     : 576
Loop Sum (Base 8 )     : 1100
Repunit Check          : 9 * 64 = 576
Closed Orbit Path      : ['11', '21', '32', '53', '15', '61', '76', '67', '66', '56', '45', '24', '62', '16', '71', '17']
OEIS Connections       :
  - OEIS A001175 (Pisano period mod 7)
  - OEIS A015134 (Number of Fibonacci-type orbits mod 7)
==================================================================
```

## Academic References

* **Zenodo Archive:** Nambi, Vineet. (2026). *The Nambi Sequence: Cyclic Sequences of Two-Digit Numbers and Their Summation Invariants*. DOI: `10.5281/zenodo.19483055`
* **OEIS Foundation Inc. (2026):** Sequences A001175, A015134, A046738, A046737, A106288, A000078, and A106295. Published electronically at `https://oeis.org`
* **Wall (1960):** D. D. Wall, *Fibonacci series modulo* $m$, The American Mathematical Monthly, 67(6), 525–532.

## License

This project is open-source and available under the MIT License.