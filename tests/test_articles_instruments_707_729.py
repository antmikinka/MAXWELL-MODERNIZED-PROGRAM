"""Per-article evidence for Treatise Arts. 707-729 (Part IV, Ch. XV).

Electromagnetic instruments: galvanometers, Helmholtz double coil,
sensitivity optimization, suspended coils, and electrodynamometers.

SCOPE: qualifies the T1->T2 uplift of ``maxwell/instruments/*``
(INSTRUMENTUM, WP-B1). Every article 707..729 carries at least one
``@pytest.mark.article`` qualifying test with a numeric assert.

INDEPENDENT ORACLES (never copied from the module under test):
  * ``_biot_savart_axis`` / ``_biot_savart_axis_stat`` — direct vector
    quadrature of the Biot-Savart law over a filamentary loop (and a
    Helmholtz pair), in the EMU (no c) and Gaussian (explicit CONST.C)
    forms respectively. Genuine numerical integration, not the closed
    forms the modules implement.
  * Hand-derived residuals/equilibria re-solved with an in-test Newton
    iteration (``_solve``) so the torque-balance roots are computed
    independently of the module's own bisection.

UNIT CONVENTION — two-convention layout after D-16 resolution (2026-08-22):
  * ``instruments.galvanometers`` follows the repo convention: Gaussian
    CGS with explicit c (CONST.C), currents in statamperes, fields in
    gauss. All galvanometer oracles/goldens below are statampere-based.
  * ``instruments.helmholtz``, ``instruments.dynamometers``,
    ``instruments.suspended_coil`` and ``optimization.sensitivity`` still
    carry the legacy EMU convention (abampere, no c); their oracles below
    remain EMU. They are not owned by this wave; the residual EMU pocket
    is documented in the Wave-7 report.
  Torques dyne.cm, forces dyne in both branches.

TOLERANCE CLASSES follow docs/LAST200_STAGE4_TESTING_STRATEGY.md §2.5:
  TIGHT 1e-10 (pure identities), STANDARD 1e-8 (closed-form physics),
  NUMERIC 1e-6 (quadrature/FD), EMPIRICAL 1e-2 (lab anchors — none here).

D-16 NOTE: the direct galvanometers-vs-circular_coils agreement for the
same physical coil is pinned here (``test_art_716_gaussian_agreement``)
and in the dedicated ``tests/test_d16_c_convention_consistency.py``.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import calc_coil_on_axis
from maxwell.instruments.dynamometers import (
    JouleCurrentWeigher,
    TorsionDynamometer,
    WeberDynamometer,
    calc_solenoid_suction,
    measure_current_from_torsion,
)
from maxwell.instruments.galvanometers import (
    FourCoilGalvanometer,
    SineGalvanometer,
    SingleCoilGalvanometer,
    StandardGalvanometer,
    TangentGalvanometer,
    ThreeCoilGalvanometer,
    UniformWireGalvanometer,
    apply_gaugain_suspension,
    calc_field_at_center,
    calc_galvanometer_response,
    calc_uniform_wire_sensitivity,
    design_sensitive_galvanometer,
    design_standard_coil,
    gaugain_offset,
)
from maxwell.instruments.helmholtz import HelmholtzCoil
from maxwell.instruments.optimization.sensitivity import (
    apply_sensitivity_wire_law,
    optimize_galvanometer_sensitivity,
    optimize_galvanometer_wire,
    sensitivity_figure_of_merit,
)
from maxwell.instruments.suspended_coil import (
    SuspendedCoil,
    ThomsonCombinedInstrument,
    ThomsonSensitiveCoil,
    calc_uniform_normal_force,
    determine_magnetic_force,
)

# Tolerance classes (Stage 4 §2.5)
TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6


# ---------------------------------------------------------------------------
# Independent oracles
# ---------------------------------------------------------------------------


def _biot_savart_axis(
    current: float,
    radius: float,
    z_eval: float,
    z_plane: float = 0.0,
    npts: int = 4000,
) -> float:
    """On-axis B of one circular loop by direct EMU Biot-Savart quadrature.

    Integrates dB = I dl x r / |r|^3 (no factor of c; abampere -> gauss)
    around a filamentary loop of the given radius lying in the plane
    z = z_plane, evaluated at the on-axis point (0, 0, z_eval).
    Independent of every closed form in the modules under test.
    """
    a = radius
    phi = np.linspace(0.0, 2.0 * np.pi, npts, endpoint=False)
    dphi = 2.0 * np.pi / npts
    cos_p = np.cos(phi)
    sin_p = np.sin(phi)
    # source point on the loop and tangent line element dl
    sx = a * cos_p
    sy = a * sin_p
    sz = np.full_like(phi, z_plane)
    dlx = -a * sin_p * dphi
    dly = a * cos_p * dphi
    dlz = np.zeros_like(phi)
    # displacement source -> field point
    rx = -sx
    ry = -sy
    rz = z_eval - sz
    r3 = (rx * rx + ry * ry + rz * rz) ** 1.5
    # cross product dl x r
    cx = dly * rz - dlz * ry
    cy = dlz * rx - dlx * rz
    cz = dlx * ry - dly * rx
    # by symmetry only the z component survives on axis, but sum all for safety
    bz = current * np.sum(cz / r3)
    return bz


def _biot_savart_axis_stat(
    current_stat: float,
    radius: float,
    z_eval: float,
    z_plane: float = 0.0,
    npts: int = 4000,
) -> float:
    """On-axis B of one circular loop by Gaussian Biot-Savart quadrature.

    Same direct line integral as ``_biot_savart_axis`` but with the
    Gaussian law dB = (I/c) dl x r / |r|^3 (explicit CONST.C; current in
    statamperes). This is the oracle for all galvanometer tests, whose
    module under test carries the same explicit-c convention (D-16).
    """
    return _biot_savart_axis(current_stat, radius, z_eval, z_plane, npts) / CONST.C


def _helmholtz_axis_oracle(
    current: float, radius: float, n_turns: int, z_eval: float, spacing: float
) -> float:
    """Helmholtz-pair on-axis field from two loop quadratures (EMU module)."""
    return n_turns * (
        _biot_savart_axis(current, radius, z_eval, z_plane=+spacing / 2.0)
        + _biot_savart_axis(current, radius, z_eval, z_plane=-spacing / 2.0)
    )


def _solve(f, df, x0: float, iterations: int = 60) -> float:
    """Independent Newton root of f, used to re-solve torque balances."""
    x = x0
    for _ in range(iterations):
        x = x - f(x) / df(x)
    return x


# ---------------------------------------------------------------------------
# Arts. 707-708: standard galvanometer and its construction
# ---------------------------------------------------------------------------


@pytest.mark.article(707)
def test_art_707_coil_constant_golden_and_limit() -> None:
    """G = 2.pi.n/(c.R) (Art. 707): golden value and the n->double identity.

    Hand-derived: a 100-turn coil of mean radius 10 cm has
    G = 2.pi.100/(c.10) gauss per statampere (golden stored in
    reference_values.json, computed as 20.pi/CONST.C). Doubling turns
    doubles G (linearity).
    """
    coil = StandardGalvanometer(
        n_turns=100, mean_radius=10.0, wire_radius=0.05, coil_depth=0.5
    )
    assert coil.coil_constant == pytest.approx(
        ref_value(707, "coil_constant_100t_r10"),
        **tolerance_of(707, "coil_constant_100t_r10"),
    )
    # linearity in n (analytic identity)
    coil2 = StandardGalvanometer(
        n_turns=200, mean_radius=10.0, wire_radius=0.05, coil_depth=0.5
    )
    assert coil2.coil_constant == pytest.approx(2.0 * coil.coil_constant, rel=TIGHT)
    # a -> infinity limit at fixed n: G -> 0 (field of a far ring vanishes)
    huge = StandardGalvanometer(
        n_turns=100, mean_radius=1e9, wire_radius=0.05, coil_depth=0.5
    )
    assert huge.coil_constant == pytest.approx(0.0, abs=1e-6)


@pytest.mark.article(707)
@pytest.mark.article(709)
def test_art_707_709_center_field_matches_biot_savart_oracle() -> None:
    """Field at the coil centre vs an independent Biot-Savart quadrature.

    Golden: for n=100, R=10, I=1 statampere the Gaussian centre field is
    B = 2.pi.n.I/(c.R) gauss; the numerical loop integral (Gaussian form,
    explicit CONST.C) must agree.
    """
    current, n_turns, radius = 1.0, 100, 10.0
    analytic = calc_field_at_center(current, n_turns, radius)
    # B = G*I at I = 1 statampere; same golden as the coil constant.
    assert analytic == pytest.approx(
        ref_value(707, "coil_constant_100t_r10"),
        **tolerance_of(707, "coil_constant_100t_r10"),
    )
    oracle = n_turns * _biot_savart_axis_stat(current, radius, 0.0)
    assert analytic == pytest.approx(oracle, rel=NUMERIC)


@pytest.mark.article(708)
def test_art_708_design_standard_coil_self_consistent() -> None:
    """Construction (Art. 708): designed coil reproduces the target G.

    The design fixes the radius to max_radius (uniformity rule) and then
    solves n = G.c.R/(2.pi) (Gaussian convention, D-16); the achieved
    constant must equal 2.pi.n/(c.R) and meet/exceed the target, with a
    physically positive winding depth.
    """
    target = 50.0
    design = design_standard_coil(
        target_constant=target, wire_radius=0.02, max_radius=8.0
    )
    assert design["mean_radius"] == pytest.approx(8.0, rel=TIGHT)
    n_from_geometry = target * CONST.C * 8.0 / (2.0 * math.pi)
    assert design["n_turns"] == pytest.approx(math.ceil(n_from_geometry), rel=TIGHT)
    # achieved constant reconstructs from geometry and covers the target
    g_achieved = 2.0 * math.pi * design["n_turns"] / (CONST.C * design["mean_radius"])
    assert design["coil_constant"] == pytest.approx(g_achieved, rel=TIGHT)
    assert g_achieved >= target
    assert design["coil_depth"] > 0.0


# ---------------------------------------------------------------------------
# Art. 709: torque balance with torsion (tangent law as the tau->0 limit)
# ---------------------------------------------------------------------------


@pytest.mark.article(709)
def test_art_709_tangent_law_zero_torsion() -> None:
    """theta = arctan(GI/H) when the suspension is torsion-free (Art. 709).

    Hand-derived tangent law; also the small-current limit theta -> GI/H.
    """
    g, h, m = 10.0, 0.2, 1.0
    current = 0.01
    theta = calc_galvanometer_response(
        current=current,
        coil_constant=g,
        horizontal_field=h,
        magnetic_moment=m,
        torsion_constant=0.0,
    )
    assert theta == pytest.approx(math.atan(g * current / h), rel=STANDARD)
    # small-current analytic limit theta -> GI/H
    tiny = calc_galvanometer_response(
        current=1e-9,
        coil_constant=g,
        horizontal_field=h,
        magnetic_moment=m,
        torsion_constant=0.0,
    )
    assert tiny == pytest.approx(g * 1e-9 / h, rel=NUMERIC)


@pytest.mark.article(709)
def test_art_709_torsion_balance_residual_and_independent_root() -> None:
    """Implicit balance mGI cos(t) = mH sin(t) + tau.t (Art. 709, D-15).

    The returned deflection must (a) drive the torque residual to zero and
    (b) agree with an independently Newton-solved root of the same
    balance equation. Regression guard for the D-15 dimensional defect
    (torsion added to a field without division by m).
    """
    g, h, m, tau, current = 12.0, 0.25, 2.0, 0.4, 0.02
    theta = calc_galvanometer_response(
        current=current,
        coil_constant=g,
        horizontal_field=h,
        magnetic_moment=m,
        torsion_constant=tau,
    )
    # (a) residual of the torque balance vanishes
    residual = m * g * current * math.cos(theta) - m * h * math.sin(theta) - tau * theta
    assert residual == pytest.approx(0.0, abs=1e-9)

    # (b) independent Newton solution of the same equation
    def f(t):
        return m * g * current * math.cos(t) - m * h * math.sin(t) - tau * t

    def df(t):
        return -m * g * current * math.sin(t) - m * h * math.cos(t) - tau

    theta_newton = _solve(f, df, x0=g * current / (h + tau / m))
    assert theta == pytest.approx(theta_newton, rel=STANDARD)

    # torsion opposes deflection: with torsion the angle is smaller
    theta_free = calc_galvanometer_response(
        current=current,
        coil_constant=g,
        horizontal_field=h,
        magnetic_moment=m,
        torsion_constant=0.0,
    )
    assert theta < theta_free


# ---------------------------------------------------------------------------
# Art. 710: tangent vs sine galvanometers (equivalence at theta -> 0)
# ---------------------------------------------------------------------------


@pytest.mark.article(710)
def test_art_710_tangent_sine_equivalence_at_zero() -> None:
    """Tangent and sine instruments agree to first order at theta = 0.

    Both read I = (H/G).theta + O(theta^3) for small deflection; their
    fractional difference must vanish as theta -> 0 (identity of the two
    laws at zero deflection), while at finite angle the tangent law reads
    higher (tan > sin).
    """
    g, h = 20.0, 0.18
    tg = TangentGalvanometer(coil_constant=g, horizontal_field=h)
    sg = SineGalvanometer(coil_constant=g, horizontal_field=h)

    for angle in (1e-4, 1e-3):
        i_tan = tg.current_from_deflection(angle)
        i_sin = sg.current_from_rotation(angle)
        # both -> (H/G).theta
        assert i_tan == pytest.approx(h / g * angle, rel=NUMERIC)
        assert i_sin == pytest.approx(h / g * angle, rel=NUMERIC)
        assert i_tan == pytest.approx(i_sin, rel=NUMERIC)

    # finite angle: tan(theta) > sin(theta)
    big = 0.5
    assert tg.current_from_deflection(big) > sg.current_from_rotation(big)
    # round-trip tangent law
    current = 0.01
    assert tg.current_from_deflection(
        tg.deflection_from_current(current)
    ) == pytest.approx(current, rel=TIGHT)


# ---------------------------------------------------------------------------
# Art. 711: single-coil galvanometer
# ---------------------------------------------------------------------------


@pytest.mark.article(711)
def test_art_711_single_coil_tangent_measurement() -> None:
    """Single-coil measurement equals (H/G) tan(theta) (Art. 711).

    Cross-checked against an independent TangentGalvanometer of the same
    geometry, and against the hand value for a concrete angle.
    """
    n, r, h = 50, 5.0, 0.2
    single = SingleCoilGalvanometer(n_turns=n, radius=r, horizontal_field=h)
    assert single.coil_constant == pytest.approx(
        2 * math.pi * n / (CONST.C * r), rel=TIGHT
    )
    theta = 0.3
    expected = h / single.coil_constant * math.tan(theta)
    assert single.measure_current(theta) == pytest.approx(expected, rel=TIGHT)
    tg = TangentGalvanometer(coil_constant=single.coil_constant, horizontal_field=h)
    assert single.measure_current(theta) == pytest.approx(
        tg.current_from_deflection(theta), rel=TIGHT
    )


# ---------------------------------------------------------------------------
# Art. 712: Gaugain's eccentric suspension
# ---------------------------------------------------------------------------


@pytest.mark.article(712)
def test_art_712_gaugain_offset_and_field_oracle() -> None:
    """Gaugain offset R/2 and the axial field there (Art. 712).

    The eccentric suspension point is half the radius; the field at that
    axial offset, checked against the independent Gaussian Biot-Savart
    quadrature, is B = (2.pi.n.I/(c.R)).(4/5)^(3/2).
    """
    radius, n, current = 10.0, 100, 1.0
    assert gaugain_offset(radius) == pytest.approx(radius / 2.0, rel=TIGHT)

    z = gaugain_offset(radius)
    analytic = apply_gaugain_suspension(radius, z, n, current)
    expected = (2.0 * math.pi * n * current / (CONST.C * radius)) * ref_value(
        712, "gaugain_field_factor"
    )
    assert analytic == pytest.approx(expected, rel=TIGHT)

    oracle = n * _biot_savart_axis_stat(current, radius, z)
    assert analytic == pytest.approx(oracle, rel=NUMERIC)

    # offset -> 0 recovers the centre field (continuity)
    assert apply_gaugain_suspension(radius, 0.0, n, current) == pytest.approx(
        calc_field_at_center(current, n, radius), rel=TIGHT
    )


# ---------------------------------------------------------------------------
# Art. 713: Helmholtz double coil
# ---------------------------------------------------------------------------


@pytest.mark.article(713)
def test_art_713_helmholtz_center_field_golden_and_oracle() -> None:
    """Helmholtz centre field B = 32.pi.n.I/(5.sqrt(5).a) (Art. 713).

    Golden EMU value (mu0 -> 4.pi): two coils each contribute
    2.pi.n.I.a^2/(a^2+(a/2)^2)^(3/2). Verified against the independent
    two-loop Biot-Savart quadrature.
    """
    radius, n, current = 10.0, 100, 1.0
    coil = HelmholtzCoil(radius=radius, n_turns=n, current=current)
    analytic = coil.field_at_center()
    # golden = 32.pi.n.I/(5.sqrt(5).a) for n = 100, I = 1, a = 10 cm
    golden = ref_value(713, "helmholtz_center_field")
    assert analytic == pytest.approx(
        golden, **tolerance_of(713, "helmholtz_center_field")
    )

    oracle = _helmholtz_axis_oracle(current, radius, n, 0.0, spacing=radius)
    assert analytic == pytest.approx(oracle, rel=NUMERIC)
    # on-axis profile at z=0 equals the centre value
    assert coil.field_on_axis(0.0) == pytest.approx(analytic, rel=TIGHT)


@pytest.mark.article(713)
def test_art_713_helmholtz_uniformity_condition_spacing_equals_radius() -> None:
    """Uniformity design point: d^2B/dz^2 |_{z=0} = 0 iff spacing = a.

    The axial second derivative (central finite difference of the module's
    own on-axis profile) must vanish at the Helmholtz spacing and be
    non-zero away from it; the error-budget design point is spacing = a.
    """
    radius, n, current = 10.0, 50, 1.0
    coil = HelmholtzCoil(radius=radius, n_turns=n, current=current)
    h = radius * 0.02

    def fd2(spacing: float, step: float) -> float:
        b_plus = coil.field_on_axis(+step, spacing=spacing)
        b_mid = coil.field_on_axis(0.0, spacing=spacing)
        b_minus = coil.field_on_axis(-step, spacing=spacing)
        return (b_plus - 2.0 * b_mid + b_minus) / step**2

    def second_derivative(spacing: float) -> float:
        # Richardson extrapolation: the central second difference has
        # truncation error (h^2/12).B''''(0) + O(h^4), so
        # (4.D(h/2) - D(h))/3 cancels the O(h^2) term (hand-derived).
        return (4.0 * fd2(spacing, 0.5 * h) - fd2(spacing, h)) / 3.0

    # at the Helmholtz spacing the second derivative vanishes
    assert second_derivative(radius) == pytest.approx(0.0, abs=1e-6)
    # away from it the field is curved (non-zero curvature)
    assert abs(second_derivative(0.5 * radius)) > 1e-2
    assert abs(second_derivative(2.0 * radius)) > 1e-2
    # the analytic optimum is exactly spacing = radius
    assert HelmholtzCoil.optimal_spacing(radius) == pytest.approx(radius, rel=TIGHT)


@pytest.mark.article(713)
def test_art_713_helmholtz_field_flatness_over_center_region() -> None:
    """Helmholtz flatness: fractional variation below 1.2e-4 for |z| < a/10.

    Stage-4 §3.2 anchor for Art. 713: the whole point of the spacing = a
    design is an extended uniform region around the centre. Provenance of
    the bound: at s = a the profile is B/B0 = 1 - 1.152 (z/a)^4 + O(z^6)
    (B''(0) = B'''(0) = 0; the quartic coefficient is
    (17280/15000) = 1.152 exactly, hand-derived), so the worst-case
    deviation over |z| <= a/10 is 1.152e-4 at the edge.
    """
    radius, n, current = 10.0, 50, 1.0
    coil = HelmholtzCoil(radius=radius, n_turns=n, current=current)
    b0 = coil.field_at_center()
    for z in np.linspace(0.0, radius / 10.0, 11):
        deviation = abs(coil.field_on_axis(float(z)) - b0) / b0
        assert deviation < 1.2e-4
    # the edge deviation follows the quartic law 1.152 (z/a)^4 closely
    edge = abs(coil.field_on_axis(radius / 10.0) - b0) / b0
    assert edge == pytest.approx(
        ref_value(713, "edge_quartic_deviation"),
        **tolerance_of(713, "edge_quartic_deviation"),
    )


@pytest.mark.article(713)
def test_art_713_helmholtz_far_field_dipole_limit() -> None:
    """Analytic limit z -> large: pair field decays as a dipole (Art. 713).

    Hand-derived far-field golden: each coil contributes
    2.pi.n.I.a^2/z^3 to leading order, so B.z^3 -> 4.pi.n.I.a^2. The
    O((a/z)^2) corrections cancel between the two symmetric coils
    (pair-sum of (1 +- a/2z)^-3 with the (1 - 3a^2/2d^2) Biot-Savart
    expansion), leaving O((a/z)^4) ~ 2e-5 here.
    """
    radius, n, current, z_far = 10.0, 50, 1.0, 500.0
    coil = HelmholtzCoil(radius=radius, n_turns=n, current=current)
    near = coil.field_on_axis(0.0)
    far = coil.field_on_axis(z_far)
    # monotone decay: far field is three orders of magnitude below centre
    assert far < near / 1000.0
    # dipole golden value (independent hand derivation)
    dipole_golden = ref_value(713, "far_field_dipole_z500")
    assert far == pytest.approx(
        dipole_golden, **tolerance_of(713, "far_field_dipole_z500")
    )


# ---------------------------------------------------------------------------
# Arts. 714-715: multi-coil galvanometers
# ---------------------------------------------------------------------------


@pytest.mark.article(714)
def test_art_714_four_coil_constant_is_sum_and_oracle() -> None:
    """Four-coil G = sum 2.pi.n_i/(c.R_i) (Art. 714), vs Biot-Savart oracle.

    The combined centre field (G.I) of the aiding coaxial pair must equal
    the independent Gaussian quadrature sum of the two rings.
    """
    inner_r, outer_r = 5.0, 10.0
    n_in, n_out = 40, 60
    h_field = 0.2
    four = FourCoilGalvanometer(
        inner_radius=inner_r,
        outer_radius=outer_r,
        n_turns_inner=n_in,
        n_turns_outer=n_out,
        horizontal_field=h_field,
    )
    g_expected = 2 * math.pi * (n_in / inner_r + n_out / outer_r) / CONST.C
    assert four.combined_coil_constant() == pytest.approx(g_expected, rel=TIGHT)

    current = 1.0
    field_module = four.combined_coil_constant() * current
    field_oracle = n_in * _biot_savart_axis_stat(
        current, inner_r, 0.0
    ) + n_out * _biot_savart_axis_stat(current, outer_r, 0.0)
    assert field_module == pytest.approx(field_oracle, rel=NUMERIC)

    # tangent-law measurement round trip
    theta = 0.25
    measured = four.measure_current(theta)
    assert measured == pytest.approx(h_field / g_expected * math.tan(theta), rel=TIGHT)


@pytest.mark.article(715)
def test_art_715_three_coil_constant_is_sum() -> None:
    """Three-coil G = sum 2.pi.n_i/(c.R_i) (Art. 715), with round trip."""
    radii = (4.0, 6.0, 8.0)
    turns = (30, 20, 10)
    h_field = 0.18
    three = ThreeCoilGalvanometer(radii=radii, n_turns=turns, horizontal_field=h_field)
    g_expected = sum(2 * math.pi * n / (CONST.C * r) for n, r in zip(turns, radii))
    assert three.combined_coil_constant() == pytest.approx(g_expected, rel=TIGHT)
    theta = 0.2
    assert three.measure_current(theta) == pytest.approx(
        h_field / g_expected * math.tan(theta), rel=TIGHT
    )


# ---------------------------------------------------------------------------
# Arts. 716-720: sensitivity optimization
# ---------------------------------------------------------------------------


@pytest.mark.article(716)
def test_art_716_wire_dimensions_match_prescribed_resistance() -> None:
    """Wire gauge for a prescribed coil resistance (Art. 716).

    With fixed volume V and resistivity rho, choosing
    L = sqrt(R.V/rho) makes rho.L/A exactly the prescribed resistance.
    """
    r_ext, rho, volume = 100.0, 1.6e-5, 5.0
    out = optimize_galvanometer_wire(
        external_resistance=r_ext,
        wire_resistivity=rho,
        available_volume=volume,
        coil_inner_radius=2.0,
        coil_outer_radius=6.0,
    )
    # hand-derived closure identities
    length = math.sqrt(r_ext * volume / rho)
    area = volume / length
    assert out["wire_length"] == pytest.approx(length, rel=TIGHT)
    assert out["wire_area"] == pytest.approx(area, rel=TIGHT)
    assert out["wire_radius"] == pytest.approx(math.sqrt(area / math.pi), rel=TIGHT)
    # the realized resistance equals the prescribed (external) resistance
    assert out["coil_resistance"] == pytest.approx(r_ext, rel=STANDARD)


@pytest.mark.article(717)
def test_art_717_sensitive_design_uses_full_wire_and_reports_merit() -> None:
    """Sensitive-galvanometer design (Art. 717) winds all the wire.

    The merit G/(R_coil+R_ext) and the resistance reconstruction must be
    self-consistent with the turn count at the given mean radius.
    """
    length, rho_l, r_ext, radius = 1000.0, 0.05, 40.0, 5.0
    out = design_sensitive_galvanometer(
        wire_length=length,
        wire_resistance=rho_l,
        target_resistance=r_ext,
        mean_radius=radius,
    )
    n_expected = int(length // (2.0 * math.pi * radius))
    assert out["n_turns"] == n_expected
    used = n_expected * 2.0 * math.pi * radius
    assert out["coil_resistance"] == pytest.approx(rho_l * used, rel=TIGHT)
    g_expected = 2.0 * math.pi * n_expected / (CONST.C * radius)
    assert out["galvanometer_constant"] == pytest.approx(g_expected, rel=TIGHT)
    assert out["sensitivity_merit"] == pytest.approx(
        g_expected / (rho_l * used + r_ext), rel=TIGHT
    )


@pytest.mark.article(718)
def test_art_718_greatest_sensibility_at_matched_resistance() -> None:
    """Theorem of greatest sensibility (Art. 718): optimum at R_coil = R_ext.

    The figure of merit g(R) = sqrt(R)/(R+R_ext) must be stationary and
    maximal exactly at R = R_ext (zero derivative, larger than neighbours),
    and the re-winding optimizer must land its coil resistance on R_ext.
    """
    r_ext = 50.0
    # stationarity of the merit at the matching point
    dmerit = (
        sensitivity_figure_of_merit(r_ext + 1e-6, r_ext)
        - sensitivity_figure_of_merit(r_ext - 1e-6, r_ext)
    ) / 2e-6
    assert dmerit == pytest.approx(0.0, abs=1e-4)
    assert sensitivity_figure_of_merit(r_ext, r_ext) > sensitivity_figure_of_merit(
        0.5 * r_ext, r_ext
    )
    assert sensitivity_figure_of_merit(r_ext, r_ext) > sensitivity_figure_of_merit(
        2.0 * r_ext, r_ext
    )

    # the optimizer drives the coil resistance to the external resistance
    out = optimize_galvanometer_sensitivity(
        wire_length=2000.0,
        wire_radius=0.05,
        wire_resistivity=1.6e-5,
        external_resistance=r_ext,
        coil_radius=5.0,
    )
    assert out["optimal_resistance"] == pytest.approx(r_ext, rel=STANDARD)
    assert out["sensitivity_gain"] >= 1.0 - NUMERIC


@pytest.mark.article(719)
def test_art_719_wire_thickness_grows_with_radius() -> None:
    """Law of wire thickness (Art. 719): section ∝ r^2, so y(r) ∝ r.

    The optimal wire radius must scale linearly with layer radius
    (cross-section proportional to the square of the distance from the
    axis), i.e. doubling the radius doubles the wire radius.
    """
    dims = {"inner_radius": 2.0, "outer_radius": 6.0, "depth": 1.0}
    r_ext, rho = 100.0, 1.6e-5
    y_at_r = apply_sensitivity_wire_law(3.0, r_ext, rho, dims)
    y_at_2r = apply_sensitivity_wire_law(6.0, r_ext, rho, dims)
    assert y_at_2r == pytest.approx(2.0 * y_at_r, rel=STANDARD)
    # monotone thickening outward (each outer layer uses thicker wire)
    radii = np.linspace(dims["inner_radius"], dims["outer_radius"], 9)
    ys = [apply_sensitivity_wire_law(float(r), r_ext, rho, dims) for r in radii]
    assert all(ys[i] < ys[i + 1] for i in range(len(ys) - 1))
    assert y_at_r > 0.0


@pytest.mark.article(720)
def test_art_720_uniform_wire_sensitivity_is_g_over_h() -> None:
    """Zero-deflection sensitivity d(theta)/dI = G/H (Art. 720).

    Checked both via the closed form (Gaussian convention: G carries the
    explicit CONST.C, sensitivity in rad/statampere) and as the numerical
    derivative of the tangent-law deflection at I = 0.
    """
    n, radius, h = 100, 10.0, 0.2
    sens = calc_uniform_wire_sensitivity(n, radius, h)
    assert sens == pytest.approx(2 * math.pi * n / (CONST.C * radius) / h, rel=TIGHT)

    coil = UniformWireGalvanometer(
        n_turns=n, radius=radius, wire_gauge=0.05, horizontal_field=h
    )
    assert coil.sensitivity() == pytest.approx(sens, rel=TIGHT)
    # numeric derivative of theta = arctan(GI/H) at I=0
    g = coil.coil_constant
    di = 1e-6
    dtheta_di = (math.atan(g * di / h) - math.atan(-g * di / h)) / (2 * di)
    assert dtheta_di == pytest.approx(sens, rel=NUMERIC)


# ---------------------------------------------------------------------------
# Arts. 721-724, 728: suspended-coil instruments
# ---------------------------------------------------------------------------


@pytest.mark.article(721)
def test_art_721_suspended_coil_moment_and_torque_balance() -> None:
    """Coil moment nIA and controlling/magnetic torque equilibrium (Art. 721).

    The equilibrium deflection solves k.theta = nIAH cos(theta); the
    residual must vanish and the small-current limit theta -> nIAH/k must
    hold (analytic limit theta -> 0).
    """
    n, area, k, h = 200, 4.0, 1.0, 0.15
    coil = SuspendedCoil(n_turns=n, area=area, torsion_constant=k, horizontal_field=h)
    current = 0.01
    assert coil.magnetic_moment(current) == pytest.approx(n * current * area, rel=TIGHT)

    theta = coil.equilibrium_deflection(current)
    residual = k * theta - n * current * area * h * math.cos(theta)
    assert residual == pytest.approx(0.0, abs=1e-10)
    # net torque zero at equilibrium
    assert coil.torque(current, theta) == pytest.approx(0.0, abs=1e-10)
    # small-angle limit theta -> nIAH/k (use a genuinely small deflection:
    # nIAH/k = 0.012 rad here so the cos(theta) correction is O(1e-4))
    i_small = 1e-4
    theta_small = coil.equilibrium_deflection(i_small)
    assert theta_small == pytest.approx(n * i_small * area * h / k, rel=1e-3)


@pytest.mark.article(722)
def test_art_722_thomson_sensitive_coil_sensitivity_and_round_trip() -> None:
    """Thomson sensitive coil: d(theta)/dI = nAH/k and exact inversion (Art. 722).

    measure_current must invert the equilibrium balance exactly:
    I = k.theta/(n.A.H.cos theta).
    """
    n, length, width, field, k = 300, 4.0, 1.0, 0.2, 0.5
    thomson = ThomsonSensitiveCoil(
        n_turns=n,
        coil_length=length,
        coil_width=width,
        field_strength=field,
        torsion_constant=k,
    )
    assert thomson.area == pytest.approx(length * width, rel=TIGHT)
    assert thomson.sensitivity() == pytest.approx(
        n * thomson.area * field / k, rel=TIGHT
    )
    # exact round trip through the (implicit) equilibrium
    current_true = 0.02
    mu = n * current_true * thomson.area
    theta = _solve(
        lambda t: k * t - mu * field * math.cos(t),
        lambda t: k + mu * field * math.sin(t),
        x0=mu * field / k,
    )
    assert thomson.measure_current(theta) == pytest.approx(current_true, rel=STANDARD)


@pytest.mark.article(723)
def test_art_723_determine_magnetic_force_from_deflection() -> None:
    """Suspended-coil determination of a field: H = k.theta/(nA.I) (Art. 723).

    Golden: a known current and deflection reconstruct the field; the
    closed loop (deflect in a known field, then recover the field) closes.
    """
    n, area, k = 100, 2.0, 1.0
    # small-deflection regime: nIAH/k = 0.03 rad, so the cos(theta)
    # correction in the exact equilibrium is O(theta^2/2) ~ 5e-4
    h_true, current = 0.3, 5e-4
    coil = SuspendedCoil(
        n_turns=n, area=area, torsion_constant=k, horizontal_field=h_true
    )
    theta = coil.equilibrium_deflection(current)
    # small-deflection reconstruction closes the loop
    h_recovered = determine_magnetic_force(theta, n * area, k, current)
    assert h_recovered == pytest.approx(h_true, rel=1e-3)
    # exact algebraic identity
    assert determine_magnetic_force(0.1, n * area, k, current) == pytest.approx(
        k * 0.1 / (n * area * current), rel=TIGHT
    )


@pytest.mark.article(724)
def test_art_724_combined_instrument_two_readings_agree() -> None:
    """Combined suspended-coil + galvanometer cross-read the same current (Art. 724).

    Feeding each sensor its own equilibrium deflection for a common current
    must make both readings reproduce that current.
    """
    g, h = 20.0, 0.2
    sens = 50.0  # rad / abampere for the suspended coil branch
    combo = ThomsonCombinedInstrument(
        galvanometer_constant=g, suspended_coil_sensitivity=sens, horizontal_field=h
    )
    current_true = 0.005
    theta_galv = math.atan(g * current_true / h)
    theta_coil = sens * current_true
    out = combo.measure_current_both_methods(theta_galv, theta_coil)
    assert out["from_galvanometer"] == pytest.approx(current_true, rel=STANDARD)
    assert out["from_suspended_coil"] == pytest.approx(current_true, rel=STANDARD)
    assert out["mean"] == pytest.approx(current_true, rel=STANDARD)


@pytest.mark.article(728)
def test_art_728_uniform_field_max_torque_matches_coil_torque() -> None:
    """Uniform in-plane field torque tau = nIAH (Art. 728).

    Must equal the magnetic part of the suspended-coil torque at theta = 0
    (where the field lies in the coil plane and the torque is maximal).
    """
    current, n, area, field = 0.02, 100, 3.0, 0.25
    assert calc_uniform_normal_force(current, n, area, field) == pytest.approx(
        n * current * area * field, rel=TIGHT
    )
    coil = SuspendedCoil(
        n_turns=n, area=area, torsion_constant=1.0, horizontal_field=field
    )
    assert coil.torque(current, 0.0) == pytest.approx(
        calc_uniform_normal_force(current, n, area, field), rel=TIGHT
    )


# ---------------------------------------------------------------------------
# Arts. 725-729: electrodynamometers
# ---------------------------------------------------------------------------


@pytest.mark.article(725)
def test_art_725_weber_dynamometer_square_law_and_equilibrium() -> None:
    """Weber dynamometer: tau = I^2 dM/dtheta, equilibrium I^2 M' = k.theta (Art. 725).

    The square law is verified computationally (torque ratio -> exponent 2)
    and the equilibrium/measure pair round-trips.
    """
    dm, k = 0.5, 2.0
    weber = WeberDynamometer(
        fixed_turns=100, moving_turns=50, mutual_coefficient=dm, torsion_constant=k
    )
    current = 0.3
    assert weber.torque(current) == pytest.approx(current**2 * dm, rel=TIGHT)
    # square law: doubling current quadruples torque
    assert weber.torque(2 * current) == pytest.approx(
        4 * weber.torque(current), rel=TIGHT
    )
    assert weber.verify_force_proportional_to_I_squared() is True

    theta = weber.equilibrium_deflection(current)
    assert theta == pytest.approx(current**2 * dm / k, rel=TIGHT)
    assert weber.measure_current(theta) == pytest.approx(current, rel=STANDARD)


@pytest.mark.article(726)
def test_art_726_joule_weigher_force_and_balancing_mass() -> None:
    """Joule current-weigher: F = I^2 dM/dx and m = F/g (Art. 726).

    Golden values with standard gravity 980.665 cm/s^2.
    """
    dmdx = 1.2
    weigher = JouleCurrentWeigher(
        fixed_coil_turns=100,
        moving_coil_turns=50,
        coil_separation=2.0,
        force_constant=dmdx,
    )
    current = 0.4
    force = weigher.force(current)
    assert force == pytest.approx(current**2 * dmdx, rel=TIGHT)
    assert weigher.measure_current(force) == pytest.approx(current, rel=STANDARD)
    assert weigher.balancing_mass(current) == pytest.approx(
        force / ref_value(726, "g_standard"), **tolerance_of(726, "g_standard")
    )


@pytest.mark.article(727)
def test_art_727_solenoid_suction_golden_and_work_identity() -> None:
    """Solenoid suction F = 4.pi.n1.n2.A.I^2 (Art. 727), with work identity.

    Golden numeric case; the work of full insertion F.L2 must equal the
    mutual energy M_total.I^2 of the fully-inserted position
    (M_total = 4.pi.n1.N2.A).
    """
    n1_tot, n2_tot, current = 1000, 100, 0.5
    l1, l2, area = 20.0, 5.0, 10.0
    force = calc_solenoid_suction(n1_tot, n2_tot, current, l1, l2, area)
    expected = 4.0 * math.pi * (n1_tot / l1) * (n2_tot / l2) * area * current**2
    assert force == pytest.approx(expected, rel=TIGHT)
    assert force == pytest.approx(
        ref_value(727, "solenoid_suction_golden"),
        **tolerance_of(727, "solenoid_suction_golden"),
    )

    # work identity: F.L2 == M_total.I^2, M_total = 4.pi.n1.N2.A
    m_total = 4.0 * math.pi * (n1_tot / l1) * n2_tot * area
    assert force * l2 == pytest.approx(m_total * current**2, rel=TIGHT)


@pytest.mark.article(729)
def test_art_729_torsion_dynamometer_angle_and_inversion() -> None:
    """Torsion dynamometer: theta = I^2 M'/k and its inversion (Art. 729).

    Cross-checked against the Weber dynamometer equilibrium at identical
    parameters (same physical torque balance).
    """
    dm, k = 0.8, 1.6
    torsion = TorsionDynamometer(
        fixed_turns=100, moving_turns=50, mutual_coefficient=dm, torsion_constant=k
    )
    current = 0.25
    theta = torsion.torsion_angle(current)
    assert theta == pytest.approx(current**2 * dm / k, rel=TIGHT)
    assert measure_current_from_torsion(theta, dm, k) == pytest.approx(
        current, rel=STANDARD
    )
    weber = WeberDynamometer(
        fixed_turns=100, moving_turns=50, mutual_coefficient=dm, torsion_constant=k
    )
    assert theta == pytest.approx(weber.equilibrium_deflection(current), rel=TIGHT)


# ---------------------------------------------------------------------------
# Cross-module c-convention guard (Stage-3 D-16, resolved 2026-08-22)
# ---------------------------------------------------------------------------


@pytest.mark.article(716)
def test_art_716_gaussian_agreement_galvanometers_vs_circular_coils() -> None:
    """Both modules now carry the same explicit-c Gaussian convention.

    After the D-16 resolution ``instruments.galvanometers`` and
    ``components.circular_coils`` both evaluate B = 2.pi.n.I/(c.R)
    (gauss, I in statamperes), so for the SAME physical coil they must
    agree numerically — no factor of c may remain between them. The
    former EMU form 2.pi.n.I/R is exactly CONST.C times larger, which is
    the discriminating check in tests/test_d16_c_convention_consistency.py.
    """
    current_stat, n, radius = 1.0, 100, 10.0
    galvanometer_field = calc_field_at_center(current_stat, n, radius)
    coil_field = calc_coil_on_axis(current_stat, radius, 0.0, n_turns=n)
    assert galvanometer_field == pytest.approx(coil_field, rel=TIGHT)
    # and the shared value is the Gaussian closed form 2.pi.n.I/(c.R)
    assert galvanometer_field == pytest.approx(
        2.0 * math.pi * n * current_stat / (CONST.C * radius), rel=TIGHT
    )
