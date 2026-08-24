"""Qualifying G3 tests for Arts. 758, 760, 761, 763, 764 (Ch. XVIII).

Bundle B of the Wave-7 PHYSICUS share.  Arts. 759/762/767 already carry
qualifying tests in tests/test_lint_remediation_last200.py; this file
covers the remaining Ch. XVIII articles against oracles INDEPENDENT of
the code under test:

* Art. 758 recoil method: hand-arithmetic golden; measured dimensional
  exponents (+1, -1) establishing the CGS claim [R] = L T^-1; identity
  with the Art. 766 logarithmic decrement (theta1/theta2 = e^lambda).
* Art. 760 Lenz method: hand-arithmetic golden plus an independent
  Faraday oracle -- the induced EMF recovered by central finite
  differences of the analytic flux Phi(t) = N B A cos(omega t) of a
  rotating coil, never using the module's own product.
* Art. 761 rotating coil: hand-arithmetic golden, the same Faraday
  finite-difference oracle, and the known-series-resistance subtraction.
* Art. 763 temperature correction: hand-arithmetic goldens for copper
  and german silver plus the affine-law identities (constant slope
  alpha R0, midpoint linearity) derived independently by hand.
* Art. 764 coil inductance: hand-arithmetic golden for the new
  article-specific ``calc_solenoid_self_inductance`` plus an
  independent numerical oracle -- the EMU Neumann double integral over
  the current sheet of the solenoid, evaluated by scipy quadrature of
  the ring mutual-inductance angular integral (no elliptic-integral
  conventions, no module code), against which the long-solenoid formula
  must agree within its O(r/l) end-effect envelope.

All asserts are numeric with stated tolerances (REQ-T rubric; lint R10);
goldens live in ``tests/articles/reference_values.json`` with
provenance.

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_articles_absolute_resistance_758_764.py -q
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of
from scipy.integrate import quad

from maxwell.calibration.absolute_resistance import (
    AbsoluteResistance,
    StandardResistanceCoil,
    calc_absolute_resistance_lenz,
    calc_absolute_resistance_recoil,
    calc_absolute_resistance_rotating_coil,
    calc_recoil_damping_correction,
    calc_solenoid_self_inductance,
    calc_temperature_corrected_resistance,
)

TIGHT = 1e-12


# ── Art. 758 — recoil method ───────────────────────────────────────────────


@pytest.mark.article(758)
def test_art758_recoil_resistance_hand_golden():
    """Art. 758: R = (2M/T)(theta1/theta2) with M = 1000 cm, T = 2.0 s,
    theta1 = 0.1, theta2 = 0.08 gives 1000 * 1.25 = 1250 abohm.
    Golden: hand arithmetic (reference store art. 758).
    """
    R_free = calc_absolute_resistance_recoil(1000.0, 2.0, 0.1, 0.08)
    assert R_free == pytest.approx(
        ref_value(758, "recoil_resistance_hand_case"),
        **tolerance_of(758, "recoil_resistance_hand_case"),
    )
    R_method = AbsoluteResistance().recoil_method(1000.0, 2.0, 0.1, 0.08)
    assert R_method == pytest.approx(R_free, rel=TIGHT)


@pytest.mark.article(758)
def test_art758_recoil_velocity_dimension_exponents_measured():
    """Art. 758 dimensional claim [R] = L T^-1 (1 abohm = 1 cm/s): the
    exponents are MEASURED by rescaling the inputs, not asserted by
    comment.  M carries L^+1, T carries T^-1, and the deflection ratio
    is dimensionless (rescaling both deflections leaves R unchanged).
    """
    M, T, th1, th2 = 1000.0, 2.0, 0.1, 0.08
    R0 = calc_absolute_resistance_recoil(M, T, th1, th2)
    scale = 2.5

    R_len = calc_absolute_resistance_recoil(scale * M, T, th1, th2)
    R_time = calc_absolute_resistance_recoil(M, scale * T, th1, th2)
    exponent_length = math.log(R_len / R0) / math.log(scale)
    exponent_time = math.log(R_time / R0) / math.log(scale)

    assert exponent_length == pytest.approx(
        ref_value(758, "recoil_dimension_length_exponent"),
        **tolerance_of(758, "recoil_dimension_length_exponent"),
    )
    assert exponent_time == pytest.approx(
        ref_value(758, "recoil_dimension_time_exponent"),
        **tolerance_of(758, "recoil_dimension_time_exponent"),
    )
    # The deflection ratio is dimensionless: rescaling both deflections
    # by the same factor must leave R exactly fixed (exponent 0).
    R_ratio = calc_absolute_resistance_recoil(M, T, 1.7 * th1, 1.7 * th2)
    assert R_ratio / R0 == pytest.approx(1.0, rel=TIGHT)


@pytest.mark.article(758)
def test_art758_recoil_identity_with_art766_decrement():
    """Art. 758 cross-identity (hand-derived algebra): the deflection
    ratio entering the recoil formula is the exponential of the Art. 766
    logarithmic decrement, theta1/theta2 = e^lambda, so R must equal
    (2M/T) e^lambda with lambda computed by the independent Art. 766
    function calc_recoil_damping_correction.
    """
    M, T, th1, th2 = 1000.0, 2.0, 0.1, 0.08
    logarithmic_decrement, _ = calc_recoil_damping_correction(th1, th2)
    R = calc_absolute_resistance_recoil(M, T, th1, th2)
    assert R == pytest.approx(
        (2.0 * M / T) * math.exp(logarithmic_decrement), rel=TIGHT
    )


# ── Art. 760 — Lenz's law method R = EMF / I ───────────────────────────────


def _faraday_emf_peak_fd(n_turns, field, area, omega, h=1e-4):
    """Independent Faraday oracle: central finite differences of the
    analytic flux Phi(t) = N B A cos(omega t) of a coil rotating in a
    uniform field, evaluated at omega t = pi/2 where |dPhi/dt| peaks at
    N B A omega.  No module code participates in this derivation.
    """
    t_star = math.pi / (2.0 * omega)

    def flux(t):
        return n_turns * field * area * math.cos(omega * t)

    return -(flux(t_star + h) - flux(t_star - h)) / (2.0 * h)


@pytest.mark.article(760)
def test_art760_lenz_resistance_hand_golden():
    """Arts. 759-760: R = EMF/I = 1.0 abvolt / 0.1 abampere = 10 abohm.
    Golden: hand arithmetic (reference store art. 760).
    """
    R = calc_absolute_resistance_lenz(1.0, 0.1)
    assert R == pytest.approx(
        ref_value(760, "lenz_resistance_hand_case"),
        **tolerance_of(760, "lenz_resistance_hand_case"),
    )


@pytest.mark.article(760)
def test_art760_lenz_resistance_from_independent_faraday_emf():
    """Art. 760 with an independent EMF: the EMF is recovered by finite
    differences of the analytic rotating-coil flux (oracle above), and
    R = EMF/I must reproduce the hand value N B A omega / I.
    N = 120, B = 80 G, A = 15 cm^2, omega = 40 /s, I = 0.25 abampere.
    """
    N, B, A, omega, I = 120.0, 80.0, 15.0, 40.0, 0.25
    emf_exact = N * B * A * omega  # hand-derived peak EMF
    emf_fd = _faraday_emf_peak_fd(N, B, A, omega)
    # Sanity of the oracle itself: FD derivative vs the closed form.
    # provenance: central differences, error O((omega h)^2) ~ 1.6e-5.
    assert emf_fd == pytest.approx(emf_exact, rel=1e-4)

    R = calc_absolute_resistance_lenz(emf_fd, I)
    assert R == pytest.approx(emf_exact / I, rel=1e-4)


# ── Art. 761 — rotating coil (Lorenz) method ───────────────────────────────


@pytest.mark.article(761)
def test_art761_rotating_coil_resistance_hand_golden():
    """Art. 761: R = N B A omega / I with N = 200, B = 100 G,
    A = 25 cm^2, omega = 50 /s, I = 0.5 abampere gives
    200*100*25*50/0.5 = 5e7 abohm.  Golden: hand arithmetic.
    """
    R = calc_absolute_resistance_rotating_coil(200, 25.0, 50.0, 100.0, 0.5)
    assert R == pytest.approx(
        ref_value(761, "rotating_coil_resistance_hand_case"),
        **tolerance_of(761, "rotating_coil_resistance_hand_case"),
    )


@pytest.mark.article(761)
def test_art761_rotating_coil_matches_independent_faraday_oracle():
    """Art. 761 cross-oracle: the module's algebraic EMF N B A omega
    divided by I must equal the resistance obtained from the INDEPENDENT
    finite-difference Faraday EMF of the same rotating coil (no shared
    code path): tolerance covers the O((omega h)^2) FD error.
    """
    N, B, A, omega, I = 120.0, 80.0, 15.0, 40.0, 0.25
    R_module = calc_absolute_resistance_rotating_coil(int(N), A, omega, B, I)
    emf_fd = _faraday_emf_peak_fd(N, B, A, omega)
    assert R_module == pytest.approx(emf_fd / I, rel=1e-4)


@pytest.mark.article(761)
def test_art761_rotating_coil_known_series_subtraction():
    """Art. 761 class-method variant: the unknown resistance is the
    total EMF/I minus the known series resistance.  N = 100, B = 50 G,
    A = 10 cm^2, omega = 20 /s, I = 0.2 abampere, R_known = 3e6 abohm:
    (100*50*10*20)/0.2 - 3e6 = 5e6 - 3e6 = 2e6.  Golden: hand
    arithmetic.
    """
    R = AbsoluteResistance().rotating_coil_method(
        n_turns=100,
        coil_area=10.0,
        angular_velocity=20.0,
        magnetic_field=50.0,
        induced_current=0.2,
        circuit_resistance_known=3.0e6,
    )
    assert R == pytest.approx(2.0e6, rel=TIGHT)


# ── Art. 763 — temperature correction of the standard coils ────────────────


@pytest.mark.article(763)
def test_art763_copper_temperature_correction_hand_golden():
    """Art. 763: R(T) = R0 (1 + alpha (T - T0)) with R0 = 100 abohm,
    alpha = 0.004 /deg C (copper), T0 = 20 deg C, T = 30 deg C gives
    100 * 1.04 = 104.  Golden: hand arithmetic.
    """
    R = calc_temperature_corrected_resistance(100.0, 30.0, 0.004)
    assert R == pytest.approx(
        ref_value(763, "copper_resistance_30C"),
        **tolerance_of(763, "copper_resistance_30C"),
    )


@pytest.mark.article(763)
def test_art763_german_silver_coil_material_table_golden():
    """Art. 763 standard coil: german silver carries alpha = 0.0004 /deg
    C from the module's material table; R(45 deg C) for R0 = 1000 abohm
    is 1000 * (1 + 0.0004 * 25) = 1010.  Golden: hand arithmetic.
    """
    coil = StandardResistanceCoil(nominal_resistance=1000.0, material="german_silver")
    assert coil.temperature_coefficient == pytest.approx(0.0004, rel=TIGHT)
    R = coil.resistance_at_temperature(45.0)
    assert R == pytest.approx(
        ref_value(763, "german_silver_resistance_45C"),
        **tolerance_of(763, "german_silver_resistance_45C"),
    )


@pytest.mark.article(763)
def test_art763_affine_law_identities_hand_derived():
    """Art. 763 affine-law identities (hand-derived, characterize the
    linear temperature coefficient independently of the code's
    parameterization): the slope (R(T2) - R(T1))/(T2 - T1) equals
    alpha R0 exactly, and the midpoint value equals the mean of the
    endpoint values (affine midpoint linearity).
    """
    R0, alpha, T0 = 250.0, 0.0025, 20.0
    T_a, T_b = 12.0, 57.0
    R_a = calc_temperature_corrected_resistance(R0, T_a, alpha, T0)
    R_b = calc_temperature_corrected_resistance(R0, T_b, alpha, T0)

    slope = (R_b - R_a) / (T_b - T_a)
    assert slope == pytest.approx(alpha * R0, rel=TIGHT)

    T_mid = 0.5 * (T_a + T_b)
    R_mid = calc_temperature_corrected_resistance(R0, T_mid, alpha, T0)
    assert R_mid == pytest.approx(0.5 * (R_a + R_b), rel=TIGHT)


# ── Art. 764 — self-inductance of the standard coil ────────────────────────


def _ring_mutual_emu(radius: float, separation: float) -> float:
    """EMU Neumann mutual inductance of two coaxial circular rings.

    Independent oracle (no elliptic-integral conventions, no module
    code): M = (1) * oint oint (dl1 . dl2)/|r1 - r2| evaluated as

        M(d) = 2 pi r^2 Int_0^{2pi} cos(psi) /
               sqrt(2 r^2 (1 - cos psi) + d^2) d psi

    (the inner double integral collapses by translation symmetry in the
    angles).  Far-field sanity check: M -> 2 pi^2 r^4 / d^3, the dipole
    limit derived by hand from the on-axis ring field.
    """

    def integrand(psi):
        denom = math.sqrt(
            2.0 * radius * radius * (1.0 - math.cos(psi)) + separation * separation
        )
        return math.cos(psi) / denom

    # Integrand symmetric about psi = pi: integral over [0, 2 pi] is
    # twice the integral over [0, pi].
    value, _ = quad(integrand, 0.0, math.pi, limit=200)
    return 4.0 * math.pi * radius * radius * value


def _sheet_solenoid_inductance(n_turns: int, radius: float, length: float) -> float:
    """Current-sheet solenoid inductance by the Neumann double integral.

    L = n^2 Int_0^l Int_0^l M(|z1 - z2|) dz1 dz2
      = 2 n^2 Int_0^l (l - s) M(s) ds,   n = N/l,

    the standard surface-current limit of the filament sum; the
    logarithmic singularity of M(s) at s = 0 is integrable.
    """
    n_density = n_turns / length

    def integrand(s):
        return (length - s) * _ring_mutual_emu(radius, s)

    value, _ = quad(integrand, 0.0, length, limit=300)
    return 2.0 * n_density * n_density * value


@pytest.mark.article(764)
def test_art764_solenoid_inductance_hand_golden():
    """Art. 764: L = 4 pi^2 N^2 r^2 / l with N = 100, r = 10 cm,
    l = 20 cm gives 200000 pi^2 = 1973920.8802... cm (abhenry).
    Golden: hand arithmetic.  Guards raise on non-positive geometry.
    """
    L = calc_solenoid_self_inductance(100, 10.0, 20.0)
    assert L == pytest.approx(
        ref_value(764, "solenoid_inductance_hand_case"),
        **tolerance_of(764, "solenoid_inductance_hand_case"),
    )
    with pytest.raises(ValueError):
        calc_solenoid_self_inductance(0, 10.0, 20.0)
    with pytest.raises(ValueError):
        calc_solenoid_self_inductance(100, 0.0, 20.0)
    with pytest.raises(ValueError):
        calc_solenoid_self_inductance(100, 10.0, -20.0)


@pytest.mark.article(764)
def test_art764_oracle_self_check_ring_mutual_limits():
    """Oracle-for-the-oracle, two hand-derived limits of the Neumann
    ring integral: (a) far field M -> 2 pi^2 r^4 / (d^2 + r^2)^{3/2}
    (dipole flux through the second loop; the residual O((r/d)^2)
    flux-uniformity correction is ~6e-4 at d = 50 r); (b) near field
    M -> 4 pi r (ln(8r/d) - 2), the logarithmic self-limit of two
    coaxial circles.  Both were derived by hand, independent of the
    module and of any elliptic-integral convention.
    """
    r = 1.0
    # (a) far field, d = 50 r
    d_far = 50.0
    M_numeric_far = _ring_mutual_emu(r, d_far)
    M_dipole = 2.0 * math.pi**2 * r**4 / (d_far**2 + r**2) ** 1.5
    assert M_numeric_far == pytest.approx(M_dipole, rel=1e-3)

    # (b) near field, d = r/100
    d_near = 0.01
    M_numeric_near = _ring_mutual_emu(r, d_near)
    M_log = 4.0 * math.pi * r * (math.log(8.0 * r / d_near) - 2.0)
    assert M_numeric_near == pytest.approx(M_log, rel=1e-3)


@pytest.mark.article(764)
def test_art764_solenoid_inductance_neumann_sheet_oracle():
    """Art. 764 vs an INDEPENDENT numerical oracle: the Neumann
    current-sheet double integral (scipy quadrature of the ring mutual
    inductance, no module code, no elliptic conventions).  For the long
    solenoid (l/r = 100) the formula L = 4 pi^2 N^2 r^2 / l is the
    leading term; end effects (Nagaoka correction, order r/l) can only
    REDUCE the inductance, so the oracle ratio must lie below 1 and
    within the 2% envelope, and must converge monotonically to 1 as the
    aspect ratio grows.
    """
    n_turns = 100
    radius = 0.5
    length = 50.0  # l/r = 100
    L_formula = calc_solenoid_self_inductance(n_turns, radius, length)
    L_sheet = _sheet_solenoid_inductance(n_turns, radius, length)
    ratio = L_sheet / L_formula

    assert ratio < 1.0  # end effects reduce finite-solenoid inductance
    assert ratio == pytest.approx(1.0, abs=0.02)  # O(r/l) envelope

    # Monotone convergence to the long-solenoid formula.
    ratio_short = _sheet_solenoid_inductance(
        n_turns, radius, 12.5
    ) / calc_solenoid_self_inductance(
        n_turns, radius, 12.5
    )  # l/r = 25
    ratio_long = _sheet_solenoid_inductance(
        n_turns, radius, 100.0
    ) / calc_solenoid_self_inductance(
        n_turns, radius, 100.0
    )  # l/r = 200
    assert ratio_short < ratio < ratio_long < 1.0
