"""maxwell.electromagnetism.coil_comparison.coil_comparison — Arts. 752-757.

One article-specific computation per article of Part IV, Ch XVII
"Comparison of Coils" (Treatise 3rd edition, Vol. II, printed
pp. 392-398).  Every formula below is transcribed from the 3rd-edition
text of the chapter and carries the article and equation number it
reproduces.

Article map (as printed):
    752  Electrical measurement sometimes more accurate than direct
         measurement; the standard coil and its directly-measured G1
    753  Determination of G1 (constant of the galvanometer coil) by
         differential null against the standard coil
    754  Determination of g1 (magnetic moment of a small coil per unit
         current) by the on-axis null method
    755  Comparison of the coefficients of mutual induction of two pairs
         of coils (the electric balance for induction)
    756  Comparison of a coefficient of self-induction with a
         coefficient of mutual induction (Wheatstone-bridge methods)
    757  Comparison of the coefficients of self-induction of two coils

Unit convention: pure CGS-EMU.  G1 in gauss per abampere, g1 in cm^2,
M and L in centimetres, resistance in abohms.  No factor of c appears;
see the package docstring.
"""

from __future__ import annotations

import math

import numpy as np

from maxwell.math.elliptic_integrals import (
    calc_complete_elliptic_e_parameter,
    calc_complete_elliptic_k_parameter,
)
from maxwell.meta.citation import maxwell_cite


# ── Art. 752 — the standard coil; electrical vs direct measurement ─────────


@maxwell_cite(
    752,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="G1 of the standard coil from its measured dimensions",
)
def calc_standard_coil_g1(
    radius: float,
    n_turns: float,
    section_depth: float = 0.0,
    section_breadth: float = 0.0,
) -> float:
    """
    Magnetic force at the centre of the standard coil per unit current.

    Art. 752: the constants of a working (small, many-winding) coil
    cannot be found by direct measurement of its hidden windings, so
    they are determined electrically against a STANDARD coil whose
    constants follow from actual measurement of its form.  The standard
    coil is therefore made of considerable size, wound in a channel of
    rectangular section whose dimensions are small compared with its
    radius.

    For N turns of negligible section at radius A, the EMU centre field
    per unit current is

        G1 = 2 pi N / A .                                     (thin ring)

    For a channel of radial depth d and axial breadth b, uniformly
    filled with N turns, integrating the exact on-axis loop field
    2 pi a^2 / (a^2 + z^2)^{3/2} over the section gives the closed form

        G1 = (2 pi N / d) [ asinh((A + d/2)/(b/2))
                            - asinh((A - d/2)/(b/2)) ] ,      (b > 0)

    reducing to (2 pi N / d) ln((A + d/2)/(A - d/2)) for b = 0 and to
    2 pi N / A as d, b -> 0.  The section correction is small of order
    (d/A)^2 + (b/A)^2, which is why the article requires the section
    to be small compared with the radius.

    Args:
        radius: Mean radius A of the standard coil (cm).
        n_turns: Total number of windings N.
        section_depth: Radial depth d of the winding channel (cm).
        section_breadth: Axial breadth b of the winding channel (cm).

    Returns:
        G1, the field at the centre per unit current (gauss per
        abampere; EMU, no factor of c).

    Reference:
        Part IV, Art. 752: standard coil determined by measurement;
        Art. 700: definition of G1.
    """
    if radius <= 0.0 or n_turns <= 0.0:
        raise ValueError("radius and n_turns must be positive")
    if section_depth < 0.0 or section_breadth < 0.0:
        raise ValueError("section dimensions must be non-negative")
    if section_depth >= 2.0 * radius:
        raise ValueError("section_depth must be smaller than the diameter")

    if section_depth == 0.0:
        return 2.0 * math.pi * n_turns / radius

    a_outer = radius + section_depth / 2.0
    a_inner = radius - section_depth / 2.0
    if section_breadth > 0.0:
        half_b = section_breadth / 2.0
        bracket = math.asinh(a_outer / half_b) - math.asinh(a_inner / half_b)
    else:
        bracket = math.log(a_outer / a_inner)
    return 2.0 * math.pi * n_turns / section_depth * bracket


@maxwell_cite(
    752,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Computed advantage of electrical comparison over direct measurement",
)
def calc_comparison_advantage(
    radius: float,
    radius_error: float,
    turns_error: float = 0.0,
    ratio_error: float = 1.0e-4,
) -> dict[str, float | bool]:
    """
    Computed comparison: electrical determination vs direct measurement.

    Art. 752: "It is better therefore to determine the electrical
    constants of the coil by direct electrical comparison with a
    standard coil whose constants are known."  The article's claim is
    made quantitative here.  For a thin coil G1 = 2 pi N / A, so the
    relative error of the DIRECT (geometric) determination is

        (dG1/G1)_direct = sqrt( (dA/A)^2 + (dN/N)^2 ) ,

    while the ELECTRICAL comparison against the standard (Art. 753,
    eq. (5)) transfers the standard's constant through a measured
    resistance ratio, whose relative error ``ratio_error`` is the only
    new uncertainty introduced for the working coil.  The verdict is
    computed from the two numbers, not asserted.

    Args:
        radius: Coil radius A (cm).
        radius_error: Absolute uncertainty dA of the radius (cm).
        turns_error: Absolute uncertainty dN of the turn count.
        ratio_error: Relative uncertainty of the resistance ratio used
            in the electrical comparison (dimensionless).

    Returns:
        Dictionary with the two computed relative uncertainties, the
        advantage factor direct/comparison, and the computed verdict
        ``electrical_superior``.

    Reference:
        Part IV, Art. 752: accuracy of electrical comparison.
    """
    if radius <= 0.0:
        raise ValueError("radius must be positive")
    if radius_error < 0.0 or turns_error < 0.0 or ratio_error < 0.0:
        raise ValueError("uncertainties must be non-negative")

    direct = math.hypot(radius_error / radius, turns_error)
    comparison = ratio_error
    advantage = direct / comparison if comparison > 0.0 else math.inf

    return {
        "direct_relative_error": direct,
        "comparison_relative_error": comparison,
        "advantage_factor": advantage,
        "electrical_superior": bool(direct > comparison),
    }


# ── Art. 753 — determination of G1 ─────────────────────────────────────────


@maxwell_cite(
    753,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Determine the coil constant G1' by null deflexion against the standard",
)
def determine_g1_by_null(
    g1_standard: float,
    gamma: float,
    gamma_prime: float,
) -> float:
    """
    Determine G1' of the galvanometer coil by the null method.

    Art. 753, eq. (2): the galvanometer coil is placed inside the
    standard coil, centres coincident, planes parallel to the earth's
    force, making a differential galvanometer.  If the opposing
    currents gamma (standard) and gamma' (galvanometer coil) produce no
    deflexion,

        G1' = (gamma / gamma') G1 .                            (2)

    Args:
        g1_standard: Constant G1 of the standard coil (gauss per
            abampere).
        gamma: Current in the standard coil (abamperes).
        gamma_prime: Current in the galvanometer coil (abamperes).

    Returns:
        G1' of the galvanometer coil (gauss per abampere).

    Reference:
        Part IV, Art. 753: determination of G1, eq. (2).
    """
    if gamma_prime == 0.0:
        raise ValueError("gamma_prime must be non-zero")
    return (gamma / gamma_prime) * g1_standard


@maxwell_cite(
    753,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Determine G1' through the shunt-divided currents, eqs. (3)-(5)",
)
def determine_g1_by_shunt(
    g1_standard: float,
    r1: float,
    r2: float,
) -> dict[str, float]:
    """
    Determine G1' when the current is divided by resistances.

    Art. 753, eqs. (3)-(5): the whole current gamma passes the standard
    coil, then divides so that gamma' flows through the galvanometer
    and resistance coils R1 while gamma - gamma' flows through R2.  By
    Art. 276,

        gamma' R1 = (gamma - gamma') R2 ,                       (3)
        gamma / gamma' = (R1 + R2) / R2 ,                       (4)
        G1' = (R1 + R2) / R2 * G1 .                             (5)

    Args:
        g1_standard: Constant G1 of the standard coil.
        r1: Resistance of the galvanometer branch R1 (abohm).
        r2: Resistance of the shunt branch R2 (abohm).

    Returns:
        Dictionary with ``current_ratio`` gamma/gamma' (eq. (4)) and
        ``g1_prime`` (eq. (5)).

    Reference:
        Part IV, Art. 753: determination of G1, eqs. (3)-(5).
    """
    if r1 < 0.0 or r2 <= 0.0:
        raise ValueError("R1 must be non-negative and R2 positive")
    current_ratio = (r1 + r2) / r2
    return {
        "current_ratio": current_ratio,
        "g1_prime": current_ratio * g1_standard,
    }


@maxwell_cite(
    753,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Residual of the deflexion equation H tan delta = G1' gamma' - G1 gamma",
)
def deflection_residual(
    h_field: float,
    delta: float,
    g1_standard: float,
    gamma: float,
    g1_prime: float,
    gamma_prime: float,
) -> float:
    """
    Residual of the Art. 753 deflexion equation.

    Art. 753, eq. (1): with opposing currents gamma (standard) and
    gamma' (galvanometer coil) producing a deflexion delta of the
    suspended magnet,

        H tan delta = G1' gamma' - G1 gamma ,                   (1)

    H the horizontal magnetic force of the earth.  This function
    returns the left-minus-right residual, which vanishes exactly when
    the constants and currents satisfy the equation.

    Args:
        h_field: Horizontal earth force H (gauss).
        delta: Observed deflexion (radians).
        g1_standard: G1 of the standard coil.
        gamma: Current in the standard coil (abamperes).
        g1_prime: G1' of the galvanometer coil.
        gamma_prime: Current in the galvanometer coil (abamperes).

    Returns:
        Residual H tan delta - (G1' gamma' - G1 gamma) (gauss-abampere).

    Reference:
        Part IV, Art. 753: determination of G1, eq. (1).
    """
    return h_field * math.tan(delta) - (g1_prime * gamma_prime - g1_standard * gamma)


# ── Art. 754 — determination of g1 ─────────────────────────────────────────


@maxwell_cite(
    754,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Axial field series G1 = 2 g1/r^3 + 3 g2/r^4 + 4 g3/r^5 + ...",
)
def axis_field_series(
    g_moments: float | list | tuple,
    r: float,
) -> float:
    """
    Field at distance r on the axis of a small coil, per unit current.

    Art. 754, eq. (6) (with the Art. 700 expansion): when the small
    coil is moved along the common axis of the standard coil, its
    action at the suspended magnet is

        G1(r) = 2 g1/r^3 + 3 g2/r^4 + 4 g3/r^5 + ...            (6)

    where g_n are the Art. 700 coefficients of the small coil (g1 its
    magnetic moment per unit current).  The term in g_n carries the
    factor (n + 1)/r^{n + 2}.

    Args:
        g_moments: The coefficients [g1, g2, g3, ...] (g1 in cm^2), or
            a bare scalar g1.
        r: Distance between the coil centres (cm), positive.

    Returns:
        Axial field per unit current (gauss per abampere).

    Reference:
        Part IV, Art. 754: determination of g1, eq. (6).
    """
    if r <= 0.0:
        raise ValueError("r must be positive")
    if isinstance(g_moments, (int, float)):
        g_moments = [g_moments]
    total = 0.0
    for index, g_n in enumerate(g_moments, start=1):
        total += (index + 1) * g_n / r ** (index + 2)
    return total


@maxwell_cite(
    754,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Third coefficient g3 = -(1/8) pi a^2 (6 a^2 + 3 xi^2 - 2 eta^2)",
)
def calc_g3_correction(
    radius: float,
    xi: float = 0.0,
    eta: float = 0.0,
) -> float:
    """
    Third coefficient g3 of a small coil's axial expansion.

    Art. 754 (value quoted from Art. 700): for a small coil of mean
    radius a whose windings have cross-section coordinates xi and eta
    relative to the mean circle,

        g3 = -(1/8) pi a^2 (6 a^2 + 3 xi^2 - 2 eta^2) .

    For a thin flat coil (xi = eta = 0) this is g3 = -(3/4) pi a^4,
    which reproduces the order a^4/r^5 term of the exact on-axis loop
    field 2 pi a^2 / (a^2 + r^2)^{3/2}.

    Args:
        radius: Mean radius a of the small coil (cm).
        xi: Radial cross-section coordinate of the windings (cm).
        eta: Axial cross-section coordinate of the windings (cm).

    Returns:
        g3 (cm^4).

    Reference:
        Part IV, Art. 754: g3 correction, by Art. 700.
    """
    if radius <= 0.0:
        raise ValueError("radius must be positive")
    return -0.125 * math.pi * radius**2 * (6.0 * radius**2 + 3.0 * xi**2 - 2.0 * eta**2)


@maxwell_cite(
    754,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Determine g1 = (1/2) G1 r^3 - 2 g3/r^2 from the on-axis null",
)
def determine_small_coil_moment(
    g1_standard: float,
    r_null: float,
    g3: float = 0.0,
) -> float:
    """
    Determine g1, the magnetic moment of the small coil per unit
    current, from the on-axis null distance.

    Art. 754, eq. (7): the small coil is moved along the common axis
    until the same current, flowing in opposite directions through the
    two coils, no longer deflects the magnet.  With the even-order
    terms eliminated by observing on both sides of the standard coil
    (and g3 either eliminated by halving the standard's windings or
    computed from the coil's dimensions),

        g1 = (1/2) G1 r^3 - 2 g3 / r^2 .                        (7)

    Args:
        g1_standard: Constant G1 of the standard coil (gauss per
            abampere).
        r_null: Null distance r between the coil centres (cm).
        g3: Third coefficient of the small coil (cm^4), default 0.

    Returns:
        g1, magnetic moment per unit current (cm^2).

    Reference:
        Part IV, Art. 754: determination of g1, eq. (7).
    """
    if r_null <= 0.0:
        raise ValueError("r_null must be positive")
    return 0.5 * g1_standard * r_null**3 - 2.0 * g3 / r_null**2


# ── Art. 755 — comparison of coefficients of mutual induction ──────────────


@maxwell_cite(
    755,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Mutual induction of the standard pair by Maxwell's elliptic formula",
)
def standard_pair_mutual_inductance(
    radius1: float,
    radius2: float,
    separation: float,
) -> float:
    """
    Coefficient of induction of a pair of coaxial circular coils whose
    geometry is directly measurable — the "standard pair" of Art. 755.

    Art. 755 requires comparing an unknown coefficient with "a pair of
    coils arranged so that their coefficient may be obtained by direct
    measurement and calculation".  For two coaxial circular filaments
    of radii a, b at axial separation z that calculation is Maxwell's
    elliptic-integral formula (Arts. 703-704),

        M = 4 pi sqrt(a b) [ (2/k - k) K(k^2) - (2/k) E(k^2) ] ,
        k^2 = 4 a b / [ (a + b)^2 + z^2 ] ,

    evaluated with the Landen/AGM complete elliptic integrals of
    ``maxwell.math.elliptic_integrals`` (full double precision for
    k^2 < 1; pure EMU, M in centimetres, no factor of c).

    Args:
        radius1: Radius a of the first coil (cm).
        radius2: Radius b of the second coil (cm).
        separation: Axial separation z of the coil planes (cm).

    Returns:
        Mutual induction M (cm, EMU).

    Reference:
        Part IV, Art. 755: standard pair directly calculable;
        Arts. 703-704: the elliptic-integral formula.
    """
    if radius1 <= 0.0 or radius2 <= 0.0:
        raise ValueError("radii must be positive")
    if separation < 0.0:
        raise ValueError("separation must be non-negative")
    s_sq = (radius1 + radius2) ** 2 + separation**2
    k_sq = 4.0 * radius1 * radius2 / s_sq
    # k^2 = 1 only for coincident filaments (the Neumann-integral
    # self-induction divergence); clamp to keep K finite.
    k_sq = min(k_sq, 1.0 - 1.0e-15)
    k = math.sqrt(k_sq)
    big_k = calc_complete_elliptic_k_parameter(k_sq)
    big_e = calc_complete_elliptic_e_parameter(k_sq)
    return 4.0 * math.pi * math.sqrt(radius1 * radius2) * (
        (2.0 / k - k) * big_k - (2.0 / k) * big_e
    )


@maxwell_cite(
    755,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Integral induction current through the galvanometer, eq. (8)",
)
def integral_induction_current(
    gamma: float,
    m1: float,
    m2: float,
    r: float,
    s: float,
    k_galvanometer: float,
) -> float:
    """
    Integral induction current through the galvanometer at breaking the
    battery circuit.

    Art. 755, eq. (8): with the standard pair (A, a), induction
    coefficient M1, in the battery circuit together with the test pair
    (B, b), coefficient M2, and the galvanometer of resistance K bridging
    the junctions so that the resistances of the two paths are R and S,

        x - y = gamma ( M2/S - M1/R ) / ( 1 + K/R + K/S ) .     (8)

    Args:
        gamma: Battery-circuit current gamma (abamperes).
        m1: Induction coefficient M1 of the standard pair (cm).
        m2: Induction coefficient M2 of the test pair (cm).
        r: Resistance R of path P-A-Q (abohm).
        s: Resistance S of path Q-B-P (abohm).
        k_galvanometer: Galvanometer resistance K (abohm).

    Returns:
        Integral current x - y through the galvanometer (abampere).

    Reference:
        Part IV, Art. 755: comparison of induction coefficients, eq. (8).
    """
    if r <= 0.0 or s <= 0.0:
        raise ValueError("R and S must be positive")
    if k_galvanometer < 0.0:
        raise ValueError("K must be non-negative")
    return gamma * (m2 / s - m1 / r) / (1.0 + k_galvanometer / r + k_galvanometer / s)


@maxwell_cite(
    755,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Induction coefficient M2 at the null, M2 = M1 S/R",
)
def compare_mutual_by_null(
    m1_standard: float,
    r: float,
    s: float,
) -> float:
    """
    Determine M2 by adjusting R and S to no galvanometer current.

    Art. 755: adjusting the resistances R and S till there is no
    current through the galvanometer at making or breaking the battery
    circuit makes the numerator of eq. (8) vanish, M2/S = M1/R, so "the
    ratio of M2 to M1 may be determined by measuring that of S to R":

        M2 = M1 S / R .

    Args:
        m1_standard: Induction coefficient M1 of the standard pair (cm).
        r: Balanced resistance R (abohm).
        s: Balanced resistance S (abohm).

    Returns:
        Induction coefficient M2 of the test pair (cm).

    Reference:
        Part IV, Art. 755: null determination of the ratio M2/M1.
    """
    if r <= 0.0 or s <= 0.0:
        raise ValueError("R and S must be positive")
    return m1_standard * s / r


@maxwell_cite(
    755,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Full-null condition M2 L1 - M1 L2 = 0 of the 3rd-edition footnote",
)
def full_null_residual(
    m1: float,
    m2: float,
    l1: float,
    l2: float,
) -> float:
    """
    Relative residual of the complete-null condition.

    Art. 755, 3rd-edition footnote (Fleming's notes of Maxwell's last
    lecture, equation (8')): for there to be NO current at all in the
    galvanometer, transient as well as integral, one needs in addition
    to M2 R - M1 S = 0 the condition

        M2 L1 - M1 L2 = 0 ,

    L1, L2 being the self-inductions of coils A and B.  Returns the
    relative magnitude of the residual.

    Args:
        m1: Induction coefficient M1 (cm).
        m2: Induction coefficient M2 (cm).
        l1: Self-induction L1 of coil A (cm).
        l2: Self-induction L2 of coil B (cm).

    Returns:
        |M2 L1 - M1 L2| scaled by max(|M2 L1|, |M1 L2|, 1e-300)
        (dimensionless).

    Reference:
        Part IV, Art. 755 footnote: condition D = 0 of eq. (8').
    """
    lhs = m2 * l1
    rhs = m1 * l2
    scale = max(abs(lhs), abs(rhs), 1.0e-300)
    return abs(lhs - rhs) / scale


# ── Art. 756 — self-induction compared with mutual induction ───────────────


@maxwell_cite(
    756,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Self-induction L = -(1 + P/Q) M from the bridge null, eq. (13)",
)
def self_induction_from_mutual(
    p: float,
    q: float,
    m: float,
) -> float:
    """
    Determine a coil's self-induction by comparison with a mutual
    induction.

    Art. 756, eqs. (9)-(13): the coil of self-induction L sits in
    branch A-F (resistance P) of Wheatstone's bridge; a second coil in
    the battery lead has mutual induction M with it.  With no current,
    transient or permanent, through the galvanometer between F and H,

        P x = Q y ,                                             (11)
        L dx/dt + M (dx/dt + dy/dt) = 0 ,                       (12)
        L = -(1 + P/Q) M .                                      (13)

    Since L is always positive, M must be negative: the currents must
    flow in opposite directions through the coils placed in P and in
    the battery lead.

    Args:
        p: Bridge resistance P (abohm).
        q: Bridge resistance Q (abohm).
        m: Mutual induction M between the two coils (cm); must be
            negative.

    Returns:
        Self-induction L (cm, EMU).

    Reference:
        Part IV, Art. 756: comparison of self- with mutual induction,
        eqs. (9)-(13).
    """
    if p < 0.0 or q <= 0.0:
        raise ValueError("P must be non-negative and Q positive")
    if m >= 0.0:
        raise ValueError(
            "M must be negative (opposite currents); L = -(1 + P/Q) M > 0"
        )
    return -(1.0 + p / q) * m


@maxwell_cite(
    756,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Self-induction by the third method with the shunt W, eq. (15)",
)
def self_induction_from_mutual_with_w(
    p: float,
    q: float,
    r: float,
    w: float,
    m: float,
) -> float:
    """
    Third method of Art. 756: kill the residual transient with a
    conductor W between A and Z.

    Art. 756, eq. (15): when the transient due to self-induction is
    slightly in excess of that due to mutual induction, inserting a
    conductor of resistance W between A and Z (which does not disturb
    the no-permanent-current balance) gives, once the transient is
    removed by adjusting W alone,

        L = -(1 + P/Q + (P + R)/W) M .                          (15)

    Args:
        p: Bridge resistance P (abohm).
        q: Bridge resistance Q (abohm).
        r: Bridge resistance R (abohm).
        w: Adjusted resistance W (abohm).
        m: Mutual induction M (cm); must be negative.

    Returns:
        Self-induction L (cm, EMU).

    Reference:
        Part IV, Art. 756: third method, eq. (15).
    """
    if p < 0.0 or q <= 0.0 or r < 0.0 or w <= 0.0:
        raise ValueError("P, R non-negative; Q, W positive")
    if m >= 0.0:
        raise ValueError(
            "M must be negative (opposite currents); L = -(1 + P/Q + (P+R)/W) M > 0"
        )
    return -(1.0 + p / q + (p + r) / w) * m


@maxwell_cite(
    756,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Steady-balance residual P S' - Q R, eq. (14)",
)
def steady_balance_residual(
    p: float,
    s_prime: float,
    q: float,
    r: float,
) -> float:
    """
    Residual of the no-permanent-current condition.

    Art. 756, eq. (14): the resistances are first adjusted so that

        P S' = Q R ,                                            (14)

    which is the condition that there be no permanent current through
    the galvanometer; the distance between the coils (or W) is then
    adjusted to kill the transient.  Returns the scaled residual of
    eq. (14).

    Args:
        p: Resistance P (abohm).
        s_prime: Resistance S' (abohm).
        q: Resistance Q (abohm).
        r: Resistance R (abohm).

    Returns:
        |P S' - Q R| / max(|P S'|, |Q R|, 1e-300) (dimensionless).

    Reference:
        Part IV, Art. 756: steady balance, eq. (14).
    """
    lhs = p * s_prime
    rhs = q * r
    scale = max(abs(lhs), abs(rhs), 1.0e-300)
    return abs(lhs - rhs) / scale


# ── Art. 757 — comparison of two self-inductions ───────────────────────────


@maxwell_cite(
    757,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Bridge residuals for comparing two self-inductions, eqs. (16)-(18)",
)
def compare_self_inductions(
    p: float,
    q: float,
    r: float,
    s: float,
    l_self: float,
    n_self: float,
) -> dict[str, float | bool]:
    """
    Compare the coefficients of self-induction of two coils in adjacent
    branches of Wheatstone's bridge.

    Art. 757, eqs. (16)-(18): with coils of self-induction L (in P) and
    N (in R) inserted in two adjacent branches, the condition of no
    galvanometer current is

        (P x + L dx/dt) S y = Q y (R x + N dx/dt) ,             (16)

        P S = Q R   for no permanent current ,                  (17)
        L / P = N / R   for no transient current .              (18)

    Both currents being got rid of by a proper adjustment of the
    resistances, the ratio of L to N is determined by comparison of the
    resistances.  This function returns both computed residuals and the
    verdict derived from them.

    Args:
        p, q, r, s: Bridge arm resistances P, Q, R, S (abohm).
        l_self: Self-induction L of the coil in P (cm).
        n_self: Self-induction N of the coil in R (cm).

    Returns:
        Dictionary with the scaled steady residual (eq. (17)), the
        scaled transient residual (eq. (18)), the computed ratio L/N,
        and ``balanced`` (both residuals below 1e-12).

    Reference:
        Part IV, Art. 757: comparison of self-inductions.
    """
    if min(p, q, r, s) <= 0.0:
        raise ValueError("all bridge arms must be positive")
    if l_self <= 0.0 or n_self <= 0.0:
        raise ValueError("self-inductions must be positive")
    steady = abs(p * s - q * r) / max(abs(q * r), 1.0e-300)
    transient = abs(l_self / p - n_self / r) / max(abs(n_self / r), 1.0e-300)
    return {
        "steady_residual": steady,
        "transient_residual": transient,
        "l_over_n": l_self / n_self,
        "balanced": bool(steady < 1.0e-12 and transient < 1.0e-12),
    }


@maxwell_cite(
    757,
    part=4,
    chapter="Ch XVII: Comparison of Coils",
    theory_class="maxwell_original",
    description="Self-induction ratio L/N = P/R at the double balance",
)
def self_induction_ratio_from_bridge(
    p: float,
    r: float,
) -> float:
    """
    Ratio of the two self-inductions at the double balance.

    Art. 757: when both the permanent and the transient currents have
    been got rid of, eqs. (17) and (18) hold together and

        L / N = P / R .

    Args:
        p: Resistance P of the arm carrying L (abohm).
        r: Resistance R of the arm carrying N (abohm).

    Returns:
        Ratio L/N (dimensionless).

    Reference:
        Part IV, Art. 757: ratio from the resistance comparison.
    """
    if p <= 0.0 or r <= 0.0:
        raise ValueError("P and R must be positive")
    return p / r
