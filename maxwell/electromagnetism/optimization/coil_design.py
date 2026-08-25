"""maxwell.electromagnetism.optimization.coil_design — Coil of maximum self-inductance (Art. 706).

Genuine Treatise content (Part IV, Ch. XIV "Circular Currents", Art. 706):
with a given length of wire to be wound into a coil whose winding
cross-section has a given geometric mean distance R of itself, find the
form of the channel (mean radius a) for which the self-inductance is
greatest. With the self-inductance of a circular coil (Art. 693),

    L = 4.pi.n^2.a.(log(8a/R) - 2),

and the constraints of fixed wire and similar channel figures,
dn/n = 2 dR/R and da/a = -2 dR/R, the optimum satisfies

    log(8a/R) = 7/2,      i.e.   8a/R = e^(7/2),

and at the optimum L = 6.pi.n^2.a. For a circular channel of radius c
the self-GMD is R = e^(-1/4).c (Art. 691), giving Gauss's result
a = e^(13/4).c/8 ~= 3.2238 c; for a square channel of side s,
R = 0.44705 s and the Treatise quotes 2a = 3.7 s.

Legacy content: the six functions below (field-per-resistance
efficiency, single-coil/Helmholtz wire-budget optima, random-point
uniformity figure of merit) are modern coil-optimization heuristics.
They formerly carried a fabricated Art. 706 / chapter "Coil Design"
attribution; no chapter of that name exists in the Treatise and Art. 706
treats the coil of maximum self-inductance. Per the D-24 precedent
(re-decorate, do not delete working math) they are reclassified
``standard_math`` with no article numbers; their formulas are unchanged.

Unit convention: electromagnetic quantities in EMU for consistency with
``maxwell.math.geometry.gmd`` and the inductance machinery (inductance
in centimeters); no factor of c appears in L.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize_scalar

from maxwell.electromagnetism.components.circular_coils import (
    calc_coil_on_axis,
    calc_double_coil_field,
)
from maxwell.math.geometry.gmd import calc_self_gmd_circle, calc_self_gmd_rectangle
from maxwell.meta.citation import maxwell_cite

# ---------------------------------------------------------------------------
# Art. 706: coil of maximum self-inductance (genuine Treatise content)
# ---------------------------------------------------------------------------


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Self-inductance L = 4.pi.n^2.a.(log(8a/R) - 2) of a circular coil",
)
def calc_self_inductance_circular_coil(
    n_turns: float,
    mean_radius: float,
    gmd_self: float,
) -> float:
    """Self-inductance of a circular coil from its self-GMD (Art. 706).

    Maxwell's formula (Art. 693, applied throughout Art. 706): the
    self-inductance of a coil of n turns wound in a channel whose mean
    radius is a and whose winding cross-section has geometric mean
    distance R from itself is

        L = 4.pi.n^2.a.(log(8.a/R) - 2)

    (EMU: L in centimeters). All finite-thickness effects of the winding
    enter through R alone.

    Args:
        n_turns: Number of turns n.
        mean_radius: Mean radius of the coil a (cm).
        gmd_self: Self geometric mean distance R of the winding
            cross-section (cm); see ``maxwell.math.geometry.gmd``.

    Returns:
        Self-inductance L (cm, EMU).

    Raises:
        ValueError: for non-positive arguments.
    """
    if n_turns <= 0.0 or mean_radius <= 0.0 or gmd_self <= 0.0:
        raise ValueError("n_turns, mean_radius and gmd_self must be positive")
    return (
        4.0
        * np.pi
        * n_turns**2
        * mean_radius
        * (np.log(8.0 * mean_radius / gmd_self) - 2.0)
    )


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Optimum winding proportions log(8a/R) = 7/2 of Art. 706",
)
def calc_optimal_mean_radius_to_gmd_ratio() -> float:
    """Optimal ratio a/R for a coil of maximum self-inductance (Art. 706).

    With fixed wire and similar channel figures the variations obey
    dn/n = 2 dR/R and da/a = -2 dR/R; differentiating
    L = 4.pi.n^2.a.(log(8a/R) - 2) with respect to R then gives the
    stationarity condition log(8a/R) = 7/2, i.e.

        a/R = e^(7/2)/8.

    Returns:
        Optimal ratio a/R = e^(7/2)/8 (dimensionless, ~4.1394).
    """
    return np.exp(3.5) / 8.0


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Mean radius of the maximum-inductance coil for a given channel GMD",
)
def calc_optimal_coil_mean_radius(gmd_self: float) -> float:
    """Mean radius a of the maximum-inductance coil (Art. 706).

    Inverts the optimum log(8a/R) = 7/2 for a channel whose winding
    cross-section has self-GMD R:

        a = e^(7/2).R/8.

    At this radius the inductance reaches L = 6.pi.n^2.a.

    Args:
        gmd_self: Self-GMD R of the winding cross-section (cm).

    Returns:
        Optimal mean radius a (cm).

    Raises:
        ValueError: for non-positive gmd_self.
    """
    if gmd_self <= 0.0:
        raise ValueError("gmd_self must be positive")
    return calc_optimal_mean_radius_to_gmd_ratio() * gmd_self


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Gauss's result a = e^(13/4).c/8 for a circular channel",
)
def calc_gauss_optimal_coil(channel_radius: float) -> float:
    """Maximum-inductance coil on a circular channel (Art. 706, Gauss).

    For a circular channel of radius c the self-GMD of the cross-section
    is R = e^(-1/4).c (Art. 691), so the optimum mean radius is

        a = e^(7/2).e^(-1/4).c/8 = e^(13/4).c/8 ~= 3.2238 c.

    Args:
        channel_radius: Radius c of the circular channel (cm).

    Returns:
        Optimal mean radius a (cm).

    Raises:
        ValueError: for non-positive channel_radius.
    """
    if channel_radius <= 0.0:
        raise ValueError("channel_radius must be positive")
    return calc_optimal_coil_mean_radius(calc_self_gmd_circle(channel_radius))


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Complete maximum-inductance design for a given wire and channel",
)
def calc_max_inductance_design(
    wire_length: float,
    channel_radius: float,
) -> dict[str, float]:
    """Design the coil of greatest self-inductance (Art. 706).

    Winds the whole wire of length l at the optimal mean radius
    a = e^(13/4).c/8 on a circular channel of radius c, with
    n = l/(2.pi.a) turns; the achieved inductance equals the optimum
    identity L = 6.pi.n^2.a because log(8a/R) = 7/2 by construction.

    Args:
        wire_length: Total length of wire l (cm).
        channel_radius: Radius c of the circular channel (cm).

    Returns:
        Dict with mean_radius a, n_turns n, gmd_self R, inductance L
        and the optimum-identity value 6.pi.n^2.a (equal to L).

    Raises:
        ValueError: for non-positive inputs.
    """
    if wire_length <= 0.0:
        raise ValueError("wire_length must be positive")

    a = calc_gauss_optimal_coil(channel_radius)
    n_turns = wire_length / (2.0 * np.pi * a)
    r_gmd = calc_self_gmd_circle(channel_radius)
    inductance = calc_self_inductance_circular_coil(n_turns, a, r_gmd)
    return {
        "mean_radius": a,
        "n_turns": n_turns,
        "gmd_self": r_gmd,
        "inductance": inductance,
        "inductance_optimum_identity": 6.0 * np.pi * n_turns**2 * a,
    }


@maxwell_cite(
    706,
    part=4,
    chapter="Ch XIV: Circular Currents",
    theory_class="maxwell_original",
    description="Square channel optimum 2a = 3.7 s quoted by Maxwell",
)
def calc_square_channel_optimal_coil(side: float) -> dict[str, float]:
    """Maximum-inductance coil on a square channel (Art. 706).

    For a square winding cross-section of side s the self-GMD is
    R = 0.44705 s (``maxwell.math.geometry.gmd.calc_self_gmd_rectangle``),
    giving the optimum mean radius a = e^(7/2).R/8 and the Treatise's
    quoted proportion 2a = 3.7 s.

    Args:
        side: Side s of the square channel (cm).

    Returns:
        Dict with gmd_self R, mean_radius a and the diameter ratio 2a/s.

    Raises:
        ValueError: for non-positive side.
    """
    if side <= 0.0:
        raise ValueError("side must be positive")
    r_gmd = calc_self_gmd_rectangle(side, side)
    a = calc_optimal_coil_mean_radius(r_gmd)
    return {
        "gmd_self": r_gmd,
        "mean_radius": a,
        "diameter_to_side_ratio": 2.0 * a / side,
    }


# ---------------------------------------------------------------------------
# Legacy modern heuristics — reclassified standard_math (D-24 precedent,
# Wave 7 2026-08-22). Formerly attributed to a fabricated Art. 706 chapter
# "Coil Design"; no such chapter exists in the Treatise and the genuine
# Art. 706 content (coil of maximum self-inductance) is implemented above.
# Formulas unchanged; only the decoration is corrected.
# ---------------------------------------------------------------------------


# D-24-style reclassification: modern wire-budget field heuristic
# (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern field-per-resistance efficiency heuristic (post-Treatise)",
)
def calc_coil_efficiency(
    current: float,
    coil_radius: float,
    wire_length: float,
    wire_radius: float,
) -> dict[str, float]:
    """
    Calculate coil field efficiency.

    Modern heuristic (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent — the genuine Art. 706 content is
    :func:`calc_max_inductance_design`). For a given wire length and
    gauge, the efficiency is:

        eta = B_center / (I * sqrt(R))

    where R is the resistance proportional to wire_length / wire_area.

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        wire_length: Total wire length (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with efficiency parameters.
    """
    # Number of turns
    n = int(wire_length / (2 * np.pi * coil_radius))
    n = max(n, 1)

    # Center field
    B = calc_coil_on_axis(current, coil_radius, 0, n)

    # Wire cross-section area
    A_wire = np.pi * wire_radius**2

    # Resistance proportional (in arbitrary units)
    R_proportional = wire_length / A_wire

    # Efficiency
    efficiency = B / (current * np.sqrt(max(R_proportional, 1e-15)))

    return {
        "n_turns": n,
        "center_field": B,
        "wire_length": wire_length,
        "wire_cross_section": A_wire,
        "resistance_proportional": R_proportional,
        "efficiency": efficiency,
    }


# D-24-style reclassification: modern field-maximizing radius search
# (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern wire-budget optimal-radius search (post-Treatise)",
)
def calc_optimal_coil_radius(
    wire_length: float,
    wire_radius: float,
    target_position: float = 0.0,
) -> float:
    """
    Calculate optimal coil radius for maximum field at target position.

    Modern heuristic (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent). For a given wire length, the
    optimal radius balances the number of turns (favors small radius)
    against field strength per turn (favors large radius).

    Args:
        wire_length: Total wire length (cm).
        wire_radius: Wire radius (cm).
        target_position: Axial position for max field (cm).

    Returns:
        Optimal coil radius (cm).
    """

    def negative_field(a):
        if a < wire_radius * 2:
            return 1e30
        n = max(int(wire_length / (2 * np.pi * a)), 1)
        B = calc_coil_on_axis(1.0, a, target_position, n)
        return -B

    result = minimize_scalar(
        negative_field,
        bounds=(wire_radius * 2, wire_length / (2 * np.pi)),
        method="bounded",
    )
    return result.x


# D-24-style reclassification: modern Helmholtz wire-budget optimum
# (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern Helmholtz wire-budget optimum (post-Treatise)",
)
def calc_optimal_helmholtz(
    wire_length: float,
    wire_radius: float,
) -> dict[str, float]:
    """
    Calculate optimal Helmholtz coil configuration.

    Modern heuristic (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent). For a given wire length split
    equally between two coils, find the radius that maximizes uniform
    field at center.

    Args:
        wire_length: Total wire length for both coils (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with optimal configuration parameters.
    """
    wire_per_coil = wire_length / 2

    def negative_helmholtz_field(a):
        if a < wire_radius * 2:
            return 1e30
        n = max(int(wire_per_coil / (2 * np.pi * a)), 1)
        B = calc_double_coil_field(
            1.0, a, np.array([0, 0, 0]), coil_separation=a, n_turns=n
        )
        return -np.linalg.norm(B)

    result = minimize_scalar(
        negative_helmholtz_field,
        bounds=(wire_radius * 2, wire_per_coil / (2 * np.pi)),
        method="bounded",
    )

    optimal_radius = result.x
    n = max(int(wire_per_coil / (2 * np.pi * optimal_radius)), 1)
    B = calc_double_coil_field(
        1.0,
        optimal_radius,
        np.array([0, 0, 0]),
        coil_separation=optimal_radius,
        n_turns=n,
    )

    return {
        "optimal_radius": optimal_radius,
        "n_turns_per_coil": n,
        "separation": optimal_radius,
        "center_field_per_ampere": np.linalg.norm(B),
        "wire_per_coil": wire_per_coil,
    }


# D-24-style reclassification: modern random-sampling uniformity metric
# (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern random-sampling uniformity figure of merit (post-Treatise)",
)
def calc_uniformity_fom(
    coil_radius: float,
    n_turns: int = 1,
    coil_separation: float = None,
    evaluation_radius: float = None,
) -> dict[str, float]:
    """
    Calculate coil configuration uniformity figure of merit.

    Modern heuristic (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent). The uniformity is measured by the
    field variation over a spherical region of interest.

    Args:
        coil_radius: Coil radius (cm).
        n_turns: Turns per coil.
        coil_separation: Separation (cm, default = radius for Helmholtz).
        evaluation_radius: Radius of evaluation sphere (cm, default 0.1*coil_radius).

    Returns:
        Dictionary with uniformity figure of merit.
    """
    if coil_separation is None:
        coil_separation = coil_radius
    if evaluation_radius is None:
        evaluation_radius = 0.1 * coil_radius

    # Field at center
    B_center = calc_double_coil_field(
        1.0,
        coil_radius,
        np.array([0, 0, 0]),
        coil_separation=coil_separation,
        n_turns=n_turns,
    )
    B_center_mag = np.linalg.norm(B_center)

    # Field at various points within evaluation sphere
    n_points = 20
    max_variation = 0.0

    np.random.seed(42)
    for _ in range(n_points):
        # Random point within sphere
        r = evaluation_radius * np.random.uniform(0, 1)
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)

        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        B = calc_double_coil_field(
            1.0,
            coil_radius,
            np.array([x, y, z]),
            coil_separation=coil_separation,
            n_turns=n_turns,
        )
        B_mag = np.linalg.norm(B)
        variation = (
            abs(B_mag - B_center_mag) / B_center_mag if B_center_mag > 1e-15 else 0
        )
        max_variation = max(max_variation, variation)

    return {
        "coil_radius": coil_radius,
        "coil_separation": coil_separation,
        "evaluation_radius": evaluation_radius,
        "center_field_per_ampere": B_center_mag,
        "max_variation": max_variation,
        "uniformity_score": 1.0 - max_variation,
    }


# D-24-style reclassification: modern verification harness over the above
# heuristics (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern coil-design verification harness (post-Treatise)",
)
def verify_coil_design(
    wire_length: float = 100.0,
    wire_radius: float = 0.05,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify coil design optimization.

    Modern harness (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent). Verifies:
    1. Optimal radius produces higher field than arbitrary choices
    2. Helmholtz configuration has better uniformity than other separations

    Args:
        wire_length: Test wire length (cm).
        wire_radius: Test wire radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Optimal radius
    a_opt = calc_optimal_coil_radius(wire_length, wire_radius)
    n_opt = max(int(wire_length / (2 * np.pi * a_opt)), 1)
    B_opt = calc_coil_on_axis(1.0, a_opt, 0, n_opt)

    # Compare with arbitrary radii
    a_small = wire_radius * 10
    n_small = max(int(wire_length / (2 * np.pi * a_small)), 1)
    B_small = calc_coil_on_axis(1.0, a_small, 0, n_small)

    a_large = wire_length / (4 * np.pi)
    n_large = max(int(wire_length / (2 * np.pi * a_large)), 1)
    B_large = calc_coil_on_axis(1.0, a_large, 0, n_large)

    optimal_wins = B_opt >= B_small and B_opt >= B_large

    # Helmholtz uniformity vs other separations
    helmholtz_fom = calc_uniformity_fom(
        a_opt, n_opt, coil_separation=a_opt, evaluation_radius=0.1 * a_opt
    )
    tight_fom = calc_uniformity_fom(
        a_opt, n_opt, coil_separation=0.5 * a_opt, evaluation_radius=0.1 * a_opt
    )

    helmholtz_more_uniform = (
        helmholtz_fom["uniformity_score"] >= tight_fom["uniformity_score"]
    )

    return {
        "optimal_radius": a_opt,
        "B_optimal": B_opt,
        "B_small_radius": B_small,
        "B_large_radius": B_large,
        "optimal_wins": bool(optimal_wins),
        "helmholtz_uniformity": helmholtz_fom["uniformity_score"],
        "tight_uniformity": tight_fom["uniformity_score"],
        "helmholtz_more_uniform": bool(helmholtz_more_uniform),
        "verified": bool(optimal_wins and helmholtz_more_uniform),
    }


# D-24-style reclassification: modern analysis aggregate over the above
# heuristics (post-Treatise), no Treatise article number.
@maxwell_cite(
    part=4,
    chapter="",
    theory_class="standard_math",
    description="Modern coil-design analysis aggregate (post-Treatise)",
)
def analyze_coil_design(
    wire_length: float,
    wire_radius: float,
) -> dict[str, float | dict]:
    """
    Complete coil design optimization analysis.

    Modern aggregate (no Treatise article; former Art. 706 attribution
    removed per the D-24 precedent). Comprehensive analysis including:
    1. Optimal single coil
    2. Optimal Helmholtz pair
    3. Uniformity comparison
    4. Efficiency analysis

    Args:
        wire_length: Available wire length (cm).
        wire_radius: Wire radius (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    # Single coil optimization
    a_single = calc_optimal_coil_radius(wire_length, wire_radius)
    n_single = max(int(wire_length / (2 * np.pi * a_single)), 1)
    B_single = calc_coil_on_axis(1.0, a_single, 0, n_single)

    # Helmholtz optimization
    helmholtz = calc_optimal_helmholtz(wire_length, wire_radius)

    # Efficiency
    efficiency = calc_coil_efficiency(1.0, a_single, wire_length, wire_radius)

    return {
        "wire_length": wire_length,
        "wire_radius": wire_radius,
        "single_coil": {
            "radius": a_single,
            "n_turns": n_single,
            "center_field_per_ampere": B_single,
        },
        "helmholtz": helmholtz,
        "efficiency": efficiency,
    }
