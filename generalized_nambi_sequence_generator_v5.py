"""
The Generalized Nambi Sequence Generator (v5 - Dual Shift Orientation)
----------------------------------------------------------------------
Supports three modular regimes and both shift orientations for any numerical
base b (2 <= b <= 36) and any digit length d >= 2:

  Modular Regimes:
    1. Canonical Mode (m = b - 1)      : Digital root concatenation (digits 1..b-1).
                                         Uses closed-form N_next and N_prev.
    2. Divisor-Modulus Mode (m | b - 1): Preserves the exact closed-form N_next shortcut;
                                         separates transient orphan tails (digits > m)
                                         from the m^d closed-loop core.
    3. Zero-Inclusive Mode (m = b)     : Uses units digit of digit sum mod b (digits 0..b-1).
                                         Maps all b^d states into pure closed loops and
                                         unlocks non-trivial Binary (Base 2) dynamics.

  Shift Orientations (delta in {0, 1}):
    - Right-Shift / MSB-Insertion (delta = 0, T_R): New root enters the most significant
      digit (b^(d-1)) and existing digits shift right.
    - Left-Shift  / LSB-Insertion (delta = 1, T_L): New root enters the least significant
      digit (b^0) and existing digits shift left.
    - Both orientations are topologically conjugate via digit reversal: T_L = R o T_R o R.

v5 Improvements:
  - Adds interactive Right-Shift (T_R) / Left-Shift (T_L) / Side-by-Side Mirror
    Comparison mode.
  - Implements the unified delta-parameterized N_next and N_prev generators.
  - Preserves the 1-bit-per-state bytearray bitset mapper (~125 KB per 1,000,000 states)
    and streaming orbit export to disk.

Reference:
  "The Generalized Nambi Sequence: Cyclic Orbits of d-Digit Numbers in Arbitrary Bases"
"""

import math
import traceback

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base(n: int, b: int, width: int = 0) -> str:
    """Convert a non-negative integer n to its string representation in base b."""
    if n == 0:
        s = "0"
    else:
        chars = []
        val = n
        while val > 0:
            val, rem = divmod(val, b)
            chars.append(DIGITS[rem])
        s = "".join(reversed(chars))
    return s.zfill(width) if width else s


def from_base(s: str, b: int) -> int:
    """Convert a base-b string representation to an integer."""
    return int(s, b)


def reverse_digits(n: int, d: int, b: int) -> int:
    """Reverse the d base-b digits of n (the involution operator R)."""
    rev = 0
    val = n
    for _ in range(d):
        val, rem = divmod(val, b)
        rev = rev * b + rem
    return rev


def divisors_of(n: int) -> list[int]:
    """Return all positive divisors of n >= 1 in ascending order."""
    divs = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    return sorted(divs)


def digit_sum_base(n: int, d: int, b: int) -> int:
    """Return the sum of the d base-b digits of n."""
    total = 0
    val = n
    for _ in range(d):
        total += val % b
        val //= b
    return total


def _new_root_digit(n: int, d: int, b: int, m: int | None, zero_inclusive: bool) -> int:
    """Compute the newly inserted root digit s for term n."""
    if zero_inclusive:
        return digit_sum_base(n, d, b) % b

    if m is None:
        m = b - 1

    if b == 2 or m == 1:
        return 1

    if (b - 1) % m == 0:
        # Exact closed-form algebraic shortcut holds iff m | (b - 1)
        return 1 + ((n - 1) % m)

    return 1 + ((digit_sum_base(n, d, b) - 1) % m)


def n_next(
    n: int,
    d: int,
    b: int = 10,
    m: int | None = None,
    zero_inclusive: bool = False,
    delta: int = 0,
) -> int:
    """
    Compute the next term using the unified delta-parameterized generator:
      delta = 0 -> Right-Shift / MSB-Insertion (T_R)
      delta = 1 -> Left-Shift  / LSB-Insertion (T_L)
    """
    s = _new_root_digit(n, d, b, m, zero_inclusive)
    if delta == 0:
        return (b ** (d - 1)) * s + (n // b)
    return b * (n % (b ** (d - 1))) + s


def n_prev(
    n: int,
    d: int,
    b: int = 10,
    m: int | None = None,
    zero_inclusive: bool = False,
    delta: int = 0,
) -> int:
    """
    Compute the previous term (exact inverse on the closed-loop core) for
    delta = 0 (Right-Shift, T_R) or delta = 1 (Left-Shift, T_L).
    """
    power = b ** (d - 1)
    if delta == 0:
        q = n // power
        r = n % power
    else:
        q = n % b
        r = n // b

    if zero_inclusive:
        s_r = digit_sum_base(r, d - 1, b)
        recovered = (q - s_r) % b
    else:
        if m is None:
            m = b - 1
        if b == 2 or m == 1:
            recovered = 1
        elif (b - 1) % m == 0:
            recovered = ((q - (r % m) - 1) % m) + 1
        else:
            s_r = digit_sum_base(r, d - 1, b)
            recovered = ((q - s_r - 1) % m) + 1

    if delta == 0:
        return b * r + recovered
    return power * recovered + r


def trace_seed(
    seed: int,
    d: int,
    b: int = 10,
    m: int | None = None,
    zero_inclusive: bool = False,
    delta: int = 0,
) -> tuple[list[int], list[int]]:
    """
    Trace the trajectory from `seed` under shift orientation `delta`.
    Returns (transient_tail, closed_orbit).
    """
    seen_index: dict[int, int] = {}
    path: list[int] = []
    current = seed

    while current not in seen_index:
        seen_index[current] = len(path)
        path.append(current)
        current = n_next(current, d, b, m=m, zero_inclusive=zero_inclusive, delta=delta)

    cycle_start = seen_index[current]
    return path[:cycle_start], path[cycle_start:]


def _dense_idx_to_base_str(idx: int, d: int, m: int, zero_inclusive: bool) -> str:
    """Convert a dense state index (0..m^d - 1) directly to its d-digit base-b string."""
    offset = 0 if zero_inclusive else 1
    chars = [""] * d
    val = idx
    for pos in range(d - 1, -1, -1):
        val, rem = divmod(val, m)
        chars[pos] = DIGITS[rem + offset]
    return "".join(chars)


def map_entire_universe(
    d: int,
    b: int = 10,
    m: int | None = None,
    zero_inclusive: bool = False,
    delta: int = 0,
    export_path: str | None = None,
) -> dict[int, int]:
    """
    Map all m^d states in the closed-loop core using a 1-bit-per-state bytearray bitset.
    Memory footprint is (m^d) / 8 bytes (~125 KB per 1,000,000 states).
    Supports both delta = 0 (Right-Shift) and delta = 1 (Left-Shift).
    If `export_path` is provided, streams every orbit directly to disk.
    """
    if zero_inclusive:
        m_eff = b
        shift_offset = 0
    else:
        m_eff = (b - 1) if m is None else m
        shift_offset = d - 1

    total_states = m_eff ** d
    visited = bytearray((total_states + 7) >> 3)
    orbit_counts: dict[int, int] = {}
    power = m_eff ** (d - 1)

    out_file = open(export_path, "w", encoding="utf-8") if export_path else None
    orbit_id = 0

    try:
        if out_file:
            regime = "Zero-Inclusive" if zero_inclusive else f"Modulus m={m_eff}"
            shift_name = "Left-Shift (T_L)" if delta == 1 else "Right-Shift (T_R)"
            out_file.write(
                f"# Generalized Nambi Sequence Orbits | Base {b}, d={d}, {regime}, {shift_name}\n"
            )
            out_file.write(f"# Total Core States: {total_states}\n\n")

        for start_idx in range(total_states):
            if visited[start_idx >> 3] & (1 << (start_idx & 7)):
                continue

            curr = start_idx
            length = 0
            orbit_terms: list[str] | None = [] if out_file else None

            while not (visited[curr >> 3] & (1 << (curr & 7))):
                visited[curr >> 3] |= 1 << (curr & 7)
                if orbit_terms is not None:
                    orbit_terms.append(_dense_idx_to_base_str(curr, d, m_eff, zero_inclusive))
                length += 1

                # Compute next dense index in O(d) time with zero heap allocations
                if m_eff == 1:
                    curr = 0
                else:
                    s = shift_offset
                    tmp = curr
                    for _ in range(d):
                        s += tmp % m_eff
                        tmp //= m_eff
                    new_digit = s % m_eff
                    if delta == 0:
                        curr = power * new_digit + (curr // m_eff)
                    else:
                        curr = m_eff * (curr % power) + new_digit

            orbit_counts[length] = orbit_counts.get(length, 0) + 1
            if out_file and orbit_terms is not None:
                orbit_id += 1
                out_file.write(f"Orbit {orbit_id} (Length {length}): {' -> '.join(orbit_terms)}\n")
    finally:
        if out_file:
            out_file.close()

    return dict(sorted(orbit_counts.items()))


def get_oeis_notes(d: int, m: int) -> list[str]:
    """Return relevant OEIS sequence notes for the active (d, m) parameters."""
    notes = []
    if d == 2:
        notes.append(f"OEIS A001175 (Pisano period mod {m})")
        notes.append(f"OEIS A015134 (Number of Fibonacci-type orbits mod {m})")
    elif d == 3:
        notes.append(f"OEIS A046738 (Tribonacci period mod {m})")
        notes.append(f"OEIS A046737 (Tribonacci reduced period mod {m})")
        notes.append(f"OEIS A106288 (Tribonacci orbits mod {m})")
    elif d == 4:
        notes.append(f"OEIS A000078 (Tetranacci recurrence mod {m})")
    return notes


def get_valid_mode() -> str:
    """Prompt the user to choose the modular regime."""
    print("Select Modular Regime:")
    print("  1. Canonical (m = b - 1)       -- Full non-zero digital root system")
    print("  2. Divisor Modulus (m | b - 1) -- Preserves algebraic N_next shortcut")
    print("  3. Zero-Inclusive (m = b)      -- Full b^d universe (includes 0 & unlocks Base 2)")
    while True:
        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Error: Please enter 1, 2, or 3.\n")


def get_valid_shift_mode() -> str:
    """Prompt the user to choose the shift orientation."""
    print("\nSelect Shift Orientation:")
    print("  1. Right-Shift / MSB-Insertion (T_R, delta = 0) -- Original Nambi Sequence")
    print("  2. Left-Shift  / LSB-Insertion (T_L, delta = 1) -- Swapped Mirror Sequence")
    print("  3. Compare Both (T_R vs T_L)                    -- Verify Mirror Conjugacy")
    while True:
        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Error: Please enter 1, 2, or 3.\n")


def get_valid_base(min_base: int = 2) -> int:
    """Prompt the user for a valid base b."""
    while True:
        raw = input(f"Enter the numerical base b ({min_base} to 36, e.g., 10, 8, 16): ").strip()
        if not raw.isdigit() or not (min_base <= int(raw) <= 36):
            print(f"Error: Please enter an integer between {min_base} and 36.\n")
            continue
        return int(raw)


def get_valid_divisor_modulus(b: int) -> int:
    """Prompt the user for a divisor m of (b - 1)."""
    divs = [x for x in divisors_of(b - 1) if x >= 2]
    if not divs:
        return 1
    print(f"Valid non-trivial divisors of (b - 1) = {b - 1}: {divs}")
    while True:
        raw = input(f"Choose modulus m from {divs}: ").strip()
        if raw.isdigit() and int(raw) in divs:
            return int(raw)
        print(f"Error: m must divide {b - 1} to preserve the closed-form N_next shortcut.\n")


def get_valid_digit_count() -> int:
    """Prompt the user for a valid number of digits d >= 2."""
    while True:
        raw = input("Enter the number of digits d (d >= 2): ").strip()
        if not raw.isdigit() or int(raw) < 2:
            print("Error: Please enter an integer greater than or equal to 2.\n")
            continue
        return int(raw)


def get_valid_seed(d: int, b: int, zero_inclusive: bool) -> int:
    """Prompt the user for a valid d-digit seed in base b."""
    allowed = DIGITS[0:b] if zero_inclusive else DIGITS[1:b]
    while True:
        raw = input(
            f"Enter a {d}-digit seed in Base {b} (allowed digits: {allowed[0]}-{allowed[-1]}): "
        ).strip().upper()
        if len(raw) != d:
            print(f"Error: The seed must be exactly {d} digits long.\n")
            continue
        if not zero_inclusive and "0" in raw:
            print("Error: Non-zero mode prohibits the digit 0.\n")
            continue
        if any(ch not in allowed for ch in raw):
            print(f"Error: Invalid digit for Base {b}. Use only characters from '{allowed}'.\n")
            continue
        return from_base(raw, b)


def print_single_orbit_report(
    seed: int,
    d: int,
    b: int,
    m: int,
    zero_inclusive: bool,
    delta: int,
    mode_label: str,
) -> None:
    """Print detailed results for a single shift orientation."""
    tail, orbit = trace_seed(seed, d, b, m=m, zero_inclusive=zero_inclusive, delta=delta)
    loop_sum = sum(orbit)
    repunit = (b**d - 1) // (b - 1)
    root_sum = sum((x // (b ** (d - 1))) if delta == 0 else (x % b) for x in orbit)
    expected_singularities = math.gcd(d - 1, m)
    shift_label = "Right-Shift / MSB-Insertion (T_R, delta=0)" if delta == 0 else "Left-Shift / LSB-Insertion (T_L, delta=1)"

    print("\n" + "=" * 70)
    print(f" THE GENERALIZED NAMBI SEQUENCE | Base {b}, {d}-Digit")
    print(f" Regime: {mode_label}")
    print(f" Shift : {shift_label}")
    print("=" * 70)
    print(f"Initial Seed           : {to_base(seed, b, d)} (Base {b})")
    print(f"Next Term (N_next)     : {to_base(n_next(seed, d, b, m=m, zero_inclusive=zero_inclusive, delta=delta), b, d)}")
    if not tail:
        print(f"Prev Term (N_prev)     : {to_base(n_prev(seed, d, b, m=m, zero_inclusive=zero_inclusive, delta=delta), b, d)}")
    else:
        print(f"Transient Orphan Tail  : {[to_base(x, b, d) for x in tail]} ({len(tail)} step(s) to core)")
    print(f"Closed Orbit Length    : {len(orbit)} step(s)")
    print(f"Expected Singularities : gcd(d - 1, m) = gcd({d - 1}, {m}) = {expected_singularities}")
    print(f"Loop Sum (Base 10)     : {loop_sum}")
    if b != 10:
        print(f"Loop Sum (Base {b:<2d})     : {to_base(loop_sum, b)}")
    print(f"Repunit Check          : {repunit} * {root_sum} = {repunit * root_sum}")

    if len(orbit) <= 100:
        print(f"Closed Orbit Path      : {[to_base(x, b, d) for x in orbit]}")
    else:
        preview = [to_base(x, b, d) for x in orbit[:10]]
        print(f"Closed Orbit Path      : {preview} ... ({len(orbit):,} terms total)")

    oeis_notes = get_oeis_notes(d, m)
    if oeis_notes:
        print("OEIS Connections       :")
        for note in oeis_notes:
            print(f"  - {note}")
    print("=" * 70 + "\n")


def print_comparison_report(
    seed: int, d: int, b: int, m: int, zero_inclusive: bool, mode_label: str
) -> None:
    """Compare Right-Shift T_R(seed) against Left-Shift T_L(R(seed)) side by side."""
    rev_seed = reverse_digits(seed, d, b)
    tail_r, orb_r = trace_seed(seed, d, b, m=m, zero_inclusive=zero_inclusive, delta=0)
    tail_l, orb_l = trace_seed(rev_seed, d, b, m=m, zero_inclusive=zero_inclusive, delta=1)

    exact_mirror = (
        len(orb_r) == len(orb_l)
        and all(reverse_digits(x, d, b) == y for x, y in zip(orb_r, orb_l))
    )

    print("\n" + "=" * 70)
    print(f" SHIFT ORIENTATION DUALITY CHECK | Base {b}, {d}-Digit")
    print(f" Regime: {mode_label}")
    print("=" * 70)
    print(f"Right-Shift Seed (T_R) : {to_base(seed, b, d)}")
    print(f"Mirror Seed R(seed)    : {to_base(rev_seed, b, d)} (used for Left-Shift T_L)")
    print(f"T_R Orbit Length / Sum : {len(orb_r)} steps | Sum = {sum(orb_r)}")
    print(f"T_L Orbit Length / Sum : {len(orb_l)} steps | Sum = {sum(orb_l)}")
    print(f"Exact Digit-Reversal?  : {'YES (T_L = R o T_R o R verified)' if exact_mirror else 'NO'}")

    # Highlight repdigit milestones if present
    milestones = [
        (i + 1, to_base(x, b, d))
        for i, x in enumerate(orb_r)
        if len(set(to_base(x, b, d))) == 1
    ]
    if milestones:
        print(f"Repdigit Milestones    : {milestones}")

    limit = min(len(orb_r), 20)
    print(f"\nFirst {limit} Aligned Mirror Steps:")
    print(f"  {'Step':<6} {'Right-Shift (T_R)':<20} {'Left-Shift (T_L)':<20}")
    print(f"  {'-'*4:<6} {'-'*17:<20} {'-'*16:<20}")
    for i in range(limit):
        print(f"  {i + 1:<6} {to_base(orb_r[i], b, d):<20} {to_base(orb_l[i], b, d):<20}")
    if len(orb_r) > limit:
        print(f"  ... ({len(orb_r) - limit} more mirrored steps)")
    print("=" * 70 + "\n")


def run_session() -> None:
    mode = get_valid_mode()
    zero_inclusive = mode == "3"
    shift_choice = get_valid_shift_mode()
    b = get_valid_base(min_base=2 if zero_inclusive else 3)

    if zero_inclusive:
        m = b
        mode_label = f"Zero-Inclusive (m = b = {b})"
    elif mode == "2":
        m = get_valid_divisor_modulus(b)
        mode_label = f"Divisor Modulus (m = {m} | {b - 1})"
    else:
        m = b - 1
        mode_label = f"Canonical (m = b - 1 = {m})"

    d = get_valid_digit_count()
    seed = get_valid_seed(d, b, zero_inclusive)

    if shift_choice == "3":
        print_comparison_report(seed, d, b, m, zero_inclusive, mode_label)
        active_delta = 0
    else:
        active_delta = 0 if shift_choice == "1" else 1
        print_single_orbit_report(seed, d, b, m, zero_inclusive, active_delta, mode_label)

    core_states = m**d
    est_kb = max(1, (core_states + 7) // 8 // 1024)
    if core_states <= 5_000_000:
        shift_tag = "T_L" if active_delta == 1 else "T_R"
        choice = input(
            f"Map the entire core universe ({m}^{d} = {core_states:,} states, ~{est_kb:,} KB RAM) under {shift_tag}? (y/n): "
        ).strip().lower()
        if choice == "y":
            export_choice = input(
                "Stream all full orbit paths to a text file as well? (y/n): "
            ).strip().lower()
            export_path = None
            if export_choice == "y":
                export_path = f"nambi_orbits_b{b}_d{d}_m{m}_{shift_tag}.txt"
            print("Mapping universe... please wait.")
            summary = map_entire_universe(
                d, b, m=m, zero_inclusive=zero_inclusive, delta=active_delta, export_path=export_path
            )
            total_orbits = sum(summary.values())
            print(
                f"\nCore Universe Partition (Base {b}, d = {d}, m = {m}, {shift_tag} | {core_states:,} states, {total_orbits:,} orbits):"
            )
            for length, count in summary.items():
                print(f"  Length {length:6d} : {count:6d} orbit(s) ({length * count:,} states)")
            if export_path:
                print(f"\nSaved all {total_orbits:,} orbits to: {export_path}")
    else:
        print(
            f"Note: Core universe size ({core_states:,} states) exceeds the 5,000,000-state interactive limit."
        )


def main() -> None:
    try:
        while True:
            run_session()
            again = input("\nRun another calculation? (y/n): ").strip().lower()
            if again != "y":
                break
            print()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception:
        print("\nAn unexpected error occurred:")
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
