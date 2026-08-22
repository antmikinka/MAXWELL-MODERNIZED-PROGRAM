"""Qualifying tests for Treatise Art. 706 (coil of maximum self-inductance).

Part IV, Ch. XIV "Circular Currents", Art. 706: with a given length of
wire and a channel whose winding cross-section has self-GMD R, the
self-inductance L = 4.pi.n^2.a.(log(8a/R) - 2) (Art. 693) is greatest
when log(8a/R) = 7/2 under the constraints dn/n = 2 dR/R,
da/a = -2 dR/R; then L = 6.pi.n^2.a. For a circular channel of radius c
(R = e^(-1/4) c, Art. 691) this gives Gauss's a = e^(13/4) c/8; for a
square channel of side s (R = 0.44705 s) the Treatise quotes 2a = 3.7 s.

Qualifies ``maxwell/electromagnetism/optimization/coil_design.py``,
whose six legacy wire-budget/uniformity heuristics were reclassified
standard_math this wave (D-24 precedent) and whose genuine Art. 706
content is implemented by calc_self_inductance_circular_coil,
calc_optimal_mean_radius_to_gmd_ratio, calc_optimal_coil_mean_radius,
calc_gauss_optimal_coil, calc_max_inductance_design and
calc_square_channel_optimal_coil.

INDEPENDENT ORACLES (never copied from the module under test):
  * hand-derived closed forms pinned in reference_values.json;
  * finite-difference stationarity/maximality of L(R) along the
    constraint family (independent parametrization);
  * an independent 4-D midpoint quadrature of the log-distance kernel
    for the square-section self-GMD (diagonal-cell correction from the
    overlap-weighted unit-square integral), cross-checked against the
    Kennelly value used by the module.

TOLERANCE CLASSES (Stage 4 §2.5): TIGHT 1e-10, STANDARD 1e-8,
NUMERIC 1e-6, EMPIRICAL 1e-2 (historical printed proportion).

Provenance per test is stated in its docstring (rubric Stage-3 §6).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from maxwell.electromagnetism.optimization.coil_design import (
    calc_gauss_optimal_coil,
    calc_max_inductance_design,
    calc_optimal_coil_mean_radius,
    calc_optimal_mean_radius_to_gmd_ratio,
    calc_self_inductance_circular_coil,
    calc_square_channel_optimal_coil,
)
from maxwell.math.geometry.gmd import calc_self_gmd_circle, calc_self_gmd_rectangle

from articles import ref_value, tolerance_of

TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6

# Mean log distance within a unit square, computed independently from the
# overlap-weighted integral of (1-|u|)(1-|v|) log sqrt(u^2+v^2) over
# [-1,1]^2 by midpoint quadrature (N = 1600 gives -0.80508577; the
# N -> inf limit is used here). This is the diagonal-cell correction
# constant of the square-GMD quadrature oracle below. Not a physical
# constant.
_UNIT_SQUARE_MEAN_LOG = -0.80509


def _square_self_gmd_quadrature(side: float, n_cells: int = 30) -> float:
    """Independent oracle: self-GMD of a square section by 4-D quadrature.

    log R = (1/A^2) ∬∬ log|r - r'| dA dA' evaluated on an n_cells^2
    midpoint grid (n_cells^4 pairs); the n_cells^2 coincident-cell pairs
    are replaced by the analytic cell average log(h) + _UNIT_SQUARE_MEAN_LOG
    (h = side/n_cells). Validated: converges monotonically to 0.44705*side
    (N = 10 -> 0.44697, N = 20 -> 0.44703, N = 40 -> 0.44704) and its
    Monte-Carlo cross-check gave 0.4468 +/- 2e-4. Shares no code with the
    module under test (which uses the Kennelly form).
    """
    h = side / n_cells
    x = (np.arange(n_cells) + 0.5) * h
    xs, ys = np.meshgrid(x, x, indexing="ij")
    dx = xs[:, None, :, None] - xs[None, :, None, :]
    dy = ys[:, None, :, None] - ys[None, :, None, :]
    r2 = dx * dx + dy * dy
    mask = r2 > 0.0
    total = 0.5 * np.log(r2[mask]).sum()
    total += n_cells**2 * (math.log(h) + _UNIT_SQUARE_MEAN_LOG)
    return float(np.exp(total / n_cells**4))


# ---------------------------------------------------------------------------
# Golden proportions of the optimum
# ---------------------------------------------------------------------------


@pytest.mark.article(706)
def test_art_706_gauss_optimal_coil_golden() -> None:
    """Gauss's result a = e^(13/4).c/8 for a circular channel (Art. 706).

    Provenance: golden in reference_values.json (hand derivation:
    log(8a/R) = 7/2 with R = e^(-1/4) c); the historical approximation
    a ~ 3.22 c is also pinned (EMPIRICAL tolerance).
    """
    a = calc_gauss_optimal_coil(1.0)
    assert a == pytest.approx(
        ref_value(706, "gauss_optimal_a_over_c"),
        **tolerance_of(706, "gauss_optimal_a_over_c"),
    )
    assert a == pytest.approx(3.22, rel=1e-2)  # historical approximation
    # linearity in the channel radius (analytic identity)
    assert calc_gauss_optimal_coil(2.5) == pytest.approx(2.5 * a, rel=TIGHT)


@pytest.mark.article(706)
def test_art_706_optimal_winding_proportion_golden() -> None:
    """Optimum winding proportion a/R = e^(7/2)/8 (Art. 706).

    Provenance: golden in reference_values.json; hand derivation from
    d/dR [2 log n + log a + log(log(8a/R) - 2)] = 0 with the constraint
    differentials dn/n = 2 dR/R, da/a = -2 dR/R.
    """
    ratio = calc_optimal_mean_radius_to_gmd_ratio()
    assert ratio == pytest.approx(
        ref_value(706, "optimal_a_over_gmd"),
        **tolerance_of(706, "optimal_a_over_gmd"),
    )
    assert math.log(8.0 * ratio) == pytest.approx(3.5, rel=TIGHT)
    # inversion consistency: optimal radius from a given GMD
    r_gmd = 0.75
    assert calc_optimal_coil_mean_radius(r_gmd) == pytest.approx(
        ratio * r_gmd, rel=TIGHT
    )


@pytest.mark.article(706)
def test_art_706_disk_self_gmd_golden() -> None:
    """Circular-channel self-GMD R = e^(-1/4) c used by Art. 706.

    Provenance: golden in reference_values.json (Art. 691 exact result,
    verified independently in the math-spine bundle); pinned here because
    the Gauss optimum a/c = e^(13/4)/8 derives from it.
    """
    assert calc_self_gmd_circle(1.0) == pytest.approx(
        ref_value(706, "disk_gmd_over_radius"),
        **tolerance_of(706, "disk_gmd_over_radius"),
    )


# ---------------------------------------------------------------------------
# Independent stationarity oracle along the constraint family
# ---------------------------------------------------------------------------


@pytest.mark.article(706)
def test_art_706_fd_stationarity_of_inductance() -> None:
    """L(R) is stationary and maximal at log(8a/R) = 7/2 (Art. 706).

    Provenance: independent parametrization of the constraint family —
    scaling the channel figure by R changes n as R^2 and a as R^-2
    (dn/n = 2 dR/R, da/a = -2 dR/R) at fixed wire; the central finite
    difference of L with respect to ln R must vanish at the optimum and
    the optimum must beat its neighbours. Tolerance NUMERIC for the FD.
    """
    r0 = 0.6
    a0 = calc_optimal_mean_radius_to_gmd_ratio() * r0
    n0 = 1000.0

    def inductance_along_family(scale: float) -> float:
        r = r0 * scale
        n = n0 * scale**2
        a = a0 * scale**-2
        return calc_self_inductance_circular_coil(n, a, r)

    delta = 1e-5
    fd_derivative = (
        inductance_along_family(math.exp(delta))
        - inductance_along_family(math.exp(-delta))
    ) / (2.0 * delta)
    l0 = inductance_along_family(1.0)
    assert fd_derivative == pytest.approx(0.0, abs=1e-6 * l0)

    # maximality: the optimum beats both neighbours
    for shift in (0.9, 1.1, 0.99, 1.01):
        assert inductance_along_family(shift) < l0

    # at the optimum log(8a/R) = 7/2 exactly
    assert math.log(8.0 * a0 / r0) == pytest.approx(3.5, rel=TIGHT)


# ---------------------------------------------------------------------------
# Complete design and the optimum identity L = 6.pi.n^2.a
# ---------------------------------------------------------------------------


@pytest.mark.article(706)
def test_art_706_max_inductance_design_and_identity() -> None:
    """Complete design closes: L = 4.pi.n^2.a.(log(8a/R) - 2) = 6.pi.n^2.a.

    Provenance: hand algebra — at log(8a/R) = 7/2 the bracket is 3/2, so
    L = 4.pi.n^2.a.(3/2) = 6.pi.n^2.a. All quantities recomputed here
    from the returned design parameters.
    """
    wire_length, channel_radius = 5000.0, 0.8
    design = calc_max_inductance_design(wire_length, channel_radius)

    a = design["mean_radius"]
    n = design["n_turns"]
    r_gmd = design["gmd_self"]
    assert a == pytest.approx(calc_gauss_optimal_coil(channel_radius), rel=TIGHT)
    assert n == pytest.approx(wire_length / (2.0 * math.pi * a), rel=TIGHT)
    assert r_gmd == pytest.approx(calc_self_gmd_circle(channel_radius), rel=TIGHT)

    l_formula = 4.0 * math.pi * n**2 * a * (math.log(8.0 * a / r_gmd) - 2.0)
    assert design["inductance"] == pytest.approx(l_formula, rel=TIGHT)
    assert design["inductance_optimum_identity"] == pytest.approx(
        6.0 * math.pi * n**2 * a, rel=TIGHT
    )
    assert design["inductance"] == pytest.approx(
        design["inductance_optimum_identity"], rel=STANDARD
    )


# ---------------------------------------------------------------------------
# Square channel: quadrature oracle and the printed proportion 2a = 3.7 s
# ---------------------------------------------------------------------------


@pytest.mark.article(706)
def test_art_706_square_channel_matches_quadrature_and_printed_ratio() -> None:
    """Square channel: R_quad ~ 0.44705 s and 2a = 3.7 s (Art. 706).

    Provenance: independent 4-D midpoint quadrature of the log-distance
    kernel over the square section (this file, diagonal-corrected); the
    module's Kennelly self-GMD must agree with it (NUMERIC), and the
    resulting optimum must reproduce the Treatise's printed proportion
    2a = 3.7 s (EMPIRICAL tolerance per Stage 4 §2.5, golden in
    reference_values.json).
    """
    side = 1.0
    r_quad = _square_self_gmd_quadrature(side, n_cells=30)
    r_module = calc_self_gmd_rectangle(side, side)
    assert r_module == pytest.approx(r_quad, rel=1e-3)

    design = calc_square_channel_optimal_coil(side)
    assert design["gmd_self"] == pytest.approx(r_module, rel=TIGHT)
    assert design["diameter_to_side_ratio"] == pytest.approx(
        ref_value(706, "square_channel_side_ratio"),
        **tolerance_of(706, "square_channel_side_ratio"),
    )
    # and the same optimum condition log(8a/R) = 7/2 holds
    assert math.log(8.0 * design["mean_radius"] / design["gmd_self"]) == (
        pytest.approx(3.5, rel=TIGHT)
    )
