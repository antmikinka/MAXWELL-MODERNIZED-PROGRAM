"""Article-evidence tests for Arts. 752-757 (Part IV, Ch XVII "Comparison
of Coils"), implemented by maxwell/electromagnetism/coil_comparison/.

CIRCUITUS evidence file (Wave 7, 2026-08-21).  Every test is a qualifying
test: it compares module output against an INDEPENDENT oracle — a
from-scratch Gauss-Legendre double quadrature of the Neumann integral, a
composite-Simpson section quadrature of the exact on-axis loop field, the
dipole/far-field limits of a circular circuit, or hand arithmetic of the
Wheatstone-bridge balance equations — never against values produced by the
function under test.

Article map:
    752  the standard coil: G1 from measured form; electrical comparison
         more accurate than direct measurement
    753  determination of G1' by differential null and by shunt division
    754  determination of g1 (small-coil moment) by the on-axis null
    755  comparison of two coefficients of mutual induction (electric
         balance); the standard pair directly calculable
    756  self-induction compared with mutual induction (bridge methods)
    757  comparison of two self-inductions (double bridge balance)
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of

from maxwell.electromagnetism.coil_comparison import (
    axis_field_series,
    calc_comparison_advantage,
    calc_g3_correction,
    calc_standard_coil_g1,
    compare_mutual_by_null,
    compare_self_inductions,
    deflection_residual,
    determine_g1_by_null,
    determine_g1_by_shunt,
    determine_small_coil_moment,
    full_null_residual,
    integral_induction_current,
    self_induction_from_mutual,
    self_induction_from_mutual_with_w,
    self_induction_ratio_from_bridge,
    standard_pair_mutual_inductance,
    steady_balance_residual,
)

# ── independent oracles written for this file ───────────────────────────────


def _neumann_double_integral(a: float, b: float, z: float, n: int = 256) -> float:
    """Independent Gauss-Legendre double quadrature of the Neumann integral.

    M = ∫∫ a b cos(phi - psi) / sqrt(a^2 + b^2 - 2ab cos(phi - psi) + z^2)
        dphi dpsi ,

    the EMU mutual induction of two coaxial circular filaments (no factor
    of c).  Written from scratch for this file; shares no code with the
    module under test.  The integrand is smooth for z > 0, so tensor
    Gauss-Legendre converges spectrally.
    """
    nodes, weights = np.polynomial.legendre.leggauss(n)
    phi = math.pi * (nodes + 1.0)  # map [-1, 1] -> [0, 2 pi]
    w_phi = math.pi * weights
    d_phi = phi[:, None] - phi[None, :]
    cos_d = np.cos(d_phi)
    integrand = a * b * cos_d / np.sqrt(a * a + b * b - 2.0 * a * b * cos_d + z * z)
    return float((w_phi[:, None] * integrand * w_phi[None, :]).sum())


def _section_g1_quadrature(
    radius: float, n_turns: float, depth: float, breadth: float, n: int = 2048
) -> float:
    """Independent composite-Simpson double quadrature of the exact
    on-axis loop field 2 pi a^2 / (a^2 + z^2)^{3/2} over the rectangular
    winding channel [A - d/2, A + d/2] x [-b/2, b/2], times N/(d b).

    No closed form is used anywhere in this oracle.
    """

    def simpson_weights(n_intervals: int) -> np.ndarray:
        w = np.ones(n_intervals + 1)
        w[1:-1:2] = 4.0
        w[2:-1:2] = 2.0
        return w / 3.0

    a_grid = np.linspace(radius - depth / 2.0, radius + depth / 2.0, n + 1)
    z_grid = np.linspace(-breadth / 2.0, breadth / 2.0, n + 1)
    w_a = simpson_weights(n)
    w_z = simpson_weights(n)
    field = (
        2.0
        * math.pi
        * a_grid[:, None] ** 2
        / (a_grid[:, None] ** 2 + z_grid[None, :] ** 2) ** 1.5
    )
    integral = (w_a[:, None] * field * w_z[None, :]).sum()
    return float(n_turns / (depth * breadth) * integral * (depth / n) * (breadth / n))


def _biot_savart_centre_field(radius: float, n: int = 4000) -> float:
    """Independent Biot-Savart line integral of a single circular loop at
    its own centre (EMU): B = oint dl / a^2 = 2 pi / a, evaluated as a
    trapezoidal quadrature of the full vector kernel rather than by
    quoting the answer."""
    total = 0.0
    dt = 2.0 * math.pi / n
    for i in range(n):
        t = (i + 0.5) * dt
        dl = radius * dt  # |dl| for a circle of radius a
        # distance from every source point to the centre is a; dl is
        # perpendicular to the radius vector, so |dl x r_hat| = dl
        total += dl / radius**2
    return total


def _exact_loop_axis_field(radius: float, r: float) -> float:
    """Exact on-axis field per unit current of a thin circular loop (EMU)."""
    return 2.0 * math.pi * radius**2 / (radius**2 + r**2) ** 1.5


# ── Art. 752 — the standard coil ────────────────────────────────────────────


@pytest.mark.article(752)
def test_752_standard_coil_g1_matches_independent_section_quadrature():
    """G1 of the standard coil (rectangular channel) vs a from-scratch
    double quadrature of the exact loop field over the section."""
    module_value = calc_standard_coil_g1(
        radius=10.0, n_turns=100.0, section_depth=1.0, section_breadth=0.5
    )
    oracle = _section_g1_quadrature(10.0, 100.0, 1.0, 0.5)
    assert module_value == pytest.approx(
        ref_value(752, "standard_coil_g1_rect_section"),
        **tolerance_of(752, "standard_coil_g1_rect_section"),
    )
    assert module_value == pytest.approx(oracle, rel=1e-9)


@pytest.mark.article(752)
def test_752_thin_ring_limit_matches_biot_savart_line_integral():
    """Thin-ring G1 = N * (2 pi / A) against an independent Biot-Savart
    line integral at the loop centre."""
    radius, turns = 10.0, 100.0
    module_value = calc_standard_coil_g1(radius=radius, n_turns=turns)
    oracle = turns * _biot_savart_centre_field(radius)
    assert module_value == pytest.approx(oracle, rel=1e-10)


@pytest.mark.article(752)
def test_752_comparison_advantage_computed_from_errors():
    """Art. 752's preference for electrical comparison, quantified:
    direct geometric error dA/A = 0.01 vs ratio error 1e-4."""
    result = calc_comparison_advantage(
        radius=10.0, radius_error=0.1, turns_error=0.0, ratio_error=1.0e-4
    )
    assert result["direct_relative_error"] == pytest.approx(0.01, rel=1e-13)
    assert result["advantage_factor"] == pytest.approx(
        ref_value(752, "comparison_advantage_factor"),
        **tolerance_of(752, "comparison_advantage_factor"),
    )
    assert result["electrical_superior"] is True


# ── Art. 753 — determination of G1 ─────────────────────────────────────────


@pytest.mark.article(753)
def test_753_null_determination_golden():
    """Eq. (2): G1' = (gamma/gamma') G1 = (3/4)*2.0 = 1.5."""
    assert determine_g1_by_null(2.0, 3.0, 4.0) == pytest.approx(
        ref_value(753, "g1_prime_by_null"), **tolerance_of(753, "g1_prime_by_null")
    )


@pytest.mark.article(753)
def test_753_shunt_determination_golden():
    """Eqs. (4)-(5): gamma/gamma' = (R1+R2)/R2 = 5, G1' = 5 * 2.0 = 10."""
    result = determine_g1_by_shunt(g1_standard=2.0, r1=400.0, r2=100.0)
    assert result["current_ratio"] == pytest.approx(5.0, rel=1e-13)
    assert result["g1_prime"] == pytest.approx(
        ref_value(753, "g1_prime_by_shunt"), **tolerance_of(753, "g1_prime_by_shunt")
    )


@pytest.mark.article(753)
def test_753_deflection_equation_residual():
    """Eq. (1): residual H tan delta - (G1' gamma' - G1 gamma) is the
    hand-computed -1.0 when unbalanced and 0 at an exact balance."""
    unbalanced = deflection_residual(
        h_field=0.2,
        delta=math.atan(0.5),
        g1_standard=1.0,
        gamma=0.4,
        g1_prime=1.5,
        gamma_prime=1.0,
    )
    assert unbalanced == pytest.approx(
        ref_value(753, "deflection_residual_unbalanced"),
        **tolerance_of(753, "deflection_residual_unbalanced"),
    )
    balanced = deflection_residual(
        h_field=0.18,
        delta=0.0,
        g1_standard=2.0,
        gamma=0.75,
        g1_prime=1.5,
        gamma_prime=1.0,
    )
    assert balanced == pytest.approx(0.0, abs=1e-15)


# ── Art. 754 — determination of g1 ─────────────────────────────────────────


@pytest.mark.article(754)
def test_754_axis_series_reproduces_exact_loop_field():
    """Eq. (6) with the Art. 700 moments of a thin loop (g1 = pi a^2,
    g3 = -(3/4) pi a^4, g5 = (5/8) pi a^6) against the EXACT on-axis
    loop field; agreement to the order of the first neglected term."""
    moments = [math.pi, 0.0, -0.75 * math.pi, 0.0, 0.625 * math.pi]
    series = axis_field_series(moments, 10.0)
    exact = _exact_loop_axis_field(1.0, 10.0)
    assert series == pytest.approx(exact, rel=1e-5)
    # leading term alone is the dipole field 2 g1 / r^3
    leading = axis_field_series(math.pi, 10.0)
    assert leading == pytest.approx(2.0 * math.pi / 10.0**3, rel=1e-14)


@pytest.mark.article(754)
def test_754_g3_of_thin_loop_golden():
    """g3 = -(1/8) pi a^2 (6 a^2) = -(3/4) pi for a = 1 cm; this value is
    the one that makes the eq. (6) series reproduce the exact loop field
    at order u^2 (checked in the previous test)."""
    assert calc_g3_correction(1.0) == pytest.approx(
        ref_value(754, "g3_thin_loop_a1"), **tolerance_of(754, "g3_thin_loop_a1")
    )


@pytest.mark.article(754)
def test_754_moment_inversion_is_exact_for_truncated_series():
    """Eq. (7) is the exact algebraic inverse of eq. (6) truncated at
    g3: feeding the truncated-series field back through the formula
    recovers g1 = pi to machine precision."""
    r = 5.0
    g3 = calc_g3_correction(1.0)
    g1_true = math.pi
    g1_field = 2.0 * g1_true / r**3 + 4.0 * g3 / r**5
    recovered = determine_small_coil_moment(g1_field, r, g3=g3)
    assert recovered == pytest.approx(
        ref_value(754, "small_coil_moment_recovered"),
        **tolerance_of(754, "small_coil_moment_recovered"),
    )


@pytest.mark.article(754)
def test_754_end_to_end_null_against_exact_loop_field():
    """Full on-axis null against the EXACT (all-orders) loop field.

    Standard coil A = 20 cm, N = 1 gives G1 = pi/10 at its centre; a
    unit-radius test loop has its exact field equal G1 at the closed-form
    distance r = sqrt(20^{2/3} - 1) (hand solution of
    2 pi/(1 + r^2)^{3/2} = pi/10).  The eq. (7) inversion with the g3
    correction must recover g1 = pi to within the known first neglected
    term, and must improve markedly on the uncorrected (1/2) G1 r^3.
    """
    g1_standard = math.pi / 10.0
    r_null = math.sqrt(20.0 ** (2.0 / 3.0) - 1.0)
    g3 = calc_g3_correction(1.0)
    corrected = determine_small_coil_moment(g1_standard, r_null, g3=g3)
    uncorrected = determine_small_coil_moment(g1_standard, r_null, g3=0.0)
    err_corrected = abs(corrected - math.pi) / math.pi
    err_uncorrected = abs(uncorrected - math.pi) / math.pi
    assert err_corrected < 0.05
    assert err_corrected < err_uncorrected / 4.0
    # sanity of the hand-derived null geometry against the exact field
    assert _exact_loop_axis_field(1.0, r_null) == pytest.approx(g1_standard, rel=1e-13)


# ── Art. 755 — comparison of coefficients of mutual induction ──────────────


@pytest.mark.article(755)
def test_755_standard_pair_matches_independent_neumann_quadrature():
    """Maxwell's elliptic formula (via the repo AGM) vs a from-scratch
    Gauss-Legendre double quadrature of the Neumann integral, for the
    equal-loop standard pair a = b = 10 cm, z = 10 cm."""
    module_value = standard_pair_mutual_inductance(10.0, 10.0, 10.0)
    oracle = _neumann_double_integral(10.0, 10.0, 10.0, n=256)
    assert module_value == pytest.approx(
        ref_value(755, "mutual_inductance_equal_loops"),
        **tolerance_of(755, "mutual_inductance_equal_loops"),
    )
    assert module_value == pytest.approx(oracle, rel=1e-9)


@pytest.mark.article(755)
def test_755_asymmetric_pair_and_reciprocity():
    """Asymmetric geometry against the independent Neumann quadrature,
    and reciprocity M12 = M21 (the Neumann integral is manifestly
    symmetric; the module must reproduce that)."""
    m_ab = standard_pair_mutual_inductance(8.0, 12.0, 5.0)
    m_ba = standard_pair_mutual_inductance(12.0, 8.0, 5.0)
    oracle = _neumann_double_integral(8.0, 12.0, 5.0, n=256)
    assert m_ab == pytest.approx(
        ref_value(755, "mutual_inductance_asymmetric"),
        **tolerance_of(755, "mutual_inductance_asymmetric"),
    )
    assert m_ab == pytest.approx(oracle, rel=1e-9)
    assert m_ab == pytest.approx(m_ba, rel=1e-14)


@pytest.mark.article(755)
def test_755_far_field_dipole_asymptotic():
    """Large-separation limit: M -> 2 pi^2 a^2 b^2 / z^3 (flux of one
    loop's dipole field through the other), an independent leading-order
    oracle with O(z^-5) corrections."""
    z = 100.0
    module_value = standard_pair_mutual_inductance(1.0, 1.0, z)
    leading = 2.0 * math.pi**2 / z**3
    assert module_value == pytest.approx(leading, rel=1e-3)


@pytest.mark.article(755)
def test_755_integral_induction_current_golden_and_null():
    """Eq. (8): x - y = gamma (M2/S - M1/R)/(1 + K/R + K/S) = -30/23 for
    the golden set, and zero exactly at the balance M2/S = M1/R."""
    unbalanced = integral_induction_current(
        gamma=2.0, m1=150.0, m2=200.0, r=30.0, s=50.0, k_galvanometer=10.0
    )
    assert unbalanced == pytest.approx(
        ref_value(755, "integral_current_unbalanced"),
        **tolerance_of(755, "integral_current_unbalanced"),
    )
    balanced = integral_induction_current(
        gamma=2.0, m1=150.0, m2=250.0, r=30.0, s=50.0, k_galvanometer=10.0
    )
    assert balanced == pytest.approx(0.0, abs=1e-15)


@pytest.mark.article(755)
def test_755_null_ratio_and_full_null_condition():
    """M2 = M1 S/R = 62.5 at the null; the 3rd-edition footnote
    condition M2 L1 - M1 L2 = 0 holds (resp. fails) as computed."""
    assert compare_mutual_by_null(50.0, 4.0, 5.0) == pytest.approx(
        ref_value(755, "m2_at_null"), **tolerance_of(755, "m2_at_null")
    )
    # proportional self-inductions give an exact full null
    assert full_null_residual(m1=4.0, m2=6.0, l1=9.0, l2=13.5) == pytest.approx(
        0.0, abs=1e-15
    )
    # hand-computed non-proportional case: |6*9 - 4*4|/54 = 38/54 = 19/27
    assert full_null_residual(m1=4.0, m2=6.0, l1=9.0, l2=4.0) == pytest.approx(
        19.0 / 27.0, rel=1e-13
    )


# ── Art. 756 — self-induction compared with mutual induction ───────────────


@pytest.mark.article(756)
def test_756_self_induction_from_mutual_golden():
    """Eq. (13): L = -(1 + P/Q) M = (7/4)*14 = 24.5 cm, with M < 0 as the
    article requires (opposite currents)."""
    assert self_induction_from_mutual(3.0, 4.0, -14.0) == pytest.approx(
        ref_value(756, "self_induction_eq13"),
        **tolerance_of(756, "self_induction_eq13"),
    )
    with pytest.raises(ValueError):
        self_induction_from_mutual(3.0, 4.0, +14.0)


@pytest.mark.article(756)
def test_756_third_method_with_shunt_w_golden():
    """Eq. (15): L = -(1 + P/Q + (P+R)/W) M = 14 * 121/60."""
    assert self_induction_from_mutual_with_w(
        3.0, 4.0, 5.0, 30.0, -14.0
    ) == pytest.approx(
        ref_value(756, "self_induction_eq15"),
        **tolerance_of(756, "self_induction_eq15"),
    )


@pytest.mark.article(756)
def test_756_steady_balance_residual():
    """Eq. (14): scaled residual |P S' - Q R| / max(...) is 1/21 for the
    unbalanced golden set and 0 at exact balance."""
    assert steady_balance_residual(3.0, 7.0, 4.0, 5.0) == pytest.approx(
        ref_value(756, "steady_residual_unbalanced"),
        **tolerance_of(756, "steady_residual_unbalanced"),
    )
    assert steady_balance_residual(3.0, 20.0, 4.0, 15.0) == pytest.approx(
        0.0, abs=1e-15
    )


# ── Art. 757 — comparison of two self-inductions ───────────────────────────


@pytest.mark.article(757)
def test_757_double_balance_residuals_and_ratio():
    """Eqs. (17)-(18): PS = QR and L/P = N/R both vanish as residuals for
    the balanced bridge, and the ratio L/N = P/R = 1/2 follows."""
    result = compare_self_inductions(
        p=2.0, q=3.0, r=4.0, s=6.0, l_self=10.0, n_self=20.0
    )
    assert result["steady_residual"] == pytest.approx(0.0, abs=1e-15)
    assert result["transient_residual"] == pytest.approx(0.0, abs=1e-15)
    assert result["l_over_n"] == pytest.approx(
        ref_value(757, "self_induction_ratio_double_balance"),
        **tolerance_of(757, "self_induction_ratio_double_balance"),
    )
    assert result["balanced"] is True
    assert self_induction_ratio_from_bridge(2.0, 4.0) == pytest.approx(
        ref_value(757, "self_induction_ratio_double_balance"),
        **tolerance_of(757, "self_induction_ratio_double_balance"),
    )


@pytest.mark.article(757)
def test_757_off_balance_residuals_hand_computed():
    """Off-balance residuals against hand arithmetic: steady
    |2*6.1 - 12|/12 = 1/60; transient |10/2 - 21/4|/(21/4) = 1/21."""
    result = compare_self_inductions(
        p=2.0, q=3.0, r=4.0, s=6.1, l_self=10.0, n_self=21.0
    )
    assert result["steady_residual"] == pytest.approx(1.0 / 60.0, rel=1e-13)
    assert result["transient_residual"] == pytest.approx(1.0 / 21.0, rel=1e-13)
    assert result["balanced"] is False
