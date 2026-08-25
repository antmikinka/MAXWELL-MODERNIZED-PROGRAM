"""Regression specs R1-R5 for the five Stage-3 S1 defects (D-01..D-05).

Implements docs/LAST200_STAGE4_TESTING_STRATEGY.md §4.1 (executable regression
specs) against docs/LAST200_STAGE3_QUALITY_REVIEW.md §3 (defect register).

STATUS: All five S1 defects (D-01..D-05) were FIXED on 2026-08-21 by the
implementer agents (PHYSICUS, CIRCUITUS, INSTRUMENTUM) and independently
certified by QUALITAS (see docs/reports/S1_CERTIFICATION_2026-08-21.md).
The tests were originally authored ``xfail(strict=True)`` so that the landing
fixes would XPASS into hard failures (failing-before / passing-after evidence
at gate G2). The xfail markers have now been removed: these tests are
PERMANENT GREEN REGRESSION GUARDS encoding the correct (fixed) physics. Any
future regression of a fixed defect will fail the suite immediately.

SCOPE GUARD: nothing under ``maxwell/`` is modified here — these tests only
encode expectations. The reference values are computed from independent,
first-principles oracles (Biot-Savart quadrature; elliptic-integral mutual
inductance), never by re-deriving the code under test.

Deviations from the Stage 4 §4.1 spec (all recorded for the gate pack):
  * The specs reference ``CONST.G_STANDARD``; no such attribute exists in
    maxwell/config/constants.py. Standard gravity and the other harvested
    goldens are now loaded from ``tests/articles/reference_values.json`` via
    ``ref_value``/``tolerance_of`` (Stage-4 C3, 2026-08-21).
  * R2: the spec's kinematic sub-check writes ``+(k_left-k_right)/2`` but the
    implementation defines ``rotation_per_length = (k_right-k_left)/2``; the
    D-04 fix (remove the factor 2 in ``calc_circular_velocity_split``) does not
    touch ``perform_kinematic_analysis``, so the sub-check follows the
    implementation convention to keep the regression flip-able.
  * R4: the curl-A cross-check is compared against an independent Biot-Savart
    oracle rather than ``calc_coil_off_axis`` (the latter is itself defective —
    Stage 3 D-14/D-29/D-30 — and would entangle this regression with a
    different defect).
  * R5: force compared in magnitude to be robust to the sign convention the fix
    adopts for ``dM/dx``.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of
from scipy.special import ellipe, ellipk

from maxwell.config.constants import CONST
from maxwell.electromagnetism.measurements.galvanometers_extended import (
    current_weigher,
)
from maxwell.electromagnetism.vis.circular_fields import _vector_potential_azimuthal
from maxwell.experiments.ratio_v.combined import apply_rapid_action_correction
from maxwell.magneto_optics.circular_polarization import (
    calc_circular_velocity_split,
    perform_kinematic_analysis,
)
from maxwell.optics.diffusion import calc_diffusion_length, calc_diffusion_time

# Standard gravity (cm/s^2). Stage 4 §4.1 references ``CONST.G_STANDARD`` but
# no such attribute exists in maxwell/config/constants.py; the value is pinned
# in the central reference store (art 726, g_standard) instead.
G_STANDARD = ref_value(726, "g_standard")


# ── Independent oracles (never re-derive the code under test) ─────────────


def _biot_savart_loop_B(
    current: float, a: float, rho: float, z: float, npts: int = 4096
) -> tuple[float, float]:
    """Independent B-field oracle for a circular current loop.

    Direct quadrature of the Biot-Savart law in Gaussian CGS
    (I in abamperes, B in gauss):

        B(r) = (I/c) oint dl x (r - r') / |r - r'|^3

    evaluated on the symmetry plane phi = 0 so that the field has only
    cylindrical components (B_rho, B_z). Validated against the exact on-axis
    result B_z = 2 pi I a^2 / (c (a^2 + z^2)^(3/2)) to machine precision.
    """
    c = CONST.C
    phi = np.linspace(0.0, 2.0 * np.pi, npts, endpoint=False)
    w = 2.0 * np.pi / npts
    cos_p = np.cos(phi)
    R2 = rho**2 + a**2 - 2.0 * a * rho * cos_p + z**2
    R3 = R2**1.5
    B_rho = (current * a * z / c) * np.sum(cos_p / R3) * w
    B_z = (current * a / c) * np.sum((a - rho * cos_p) / R3) * w
    return B_rho, B_z


def _coaxial_mutual_inductance_emu(a1: float, a2: float, d: float) -> float:
    """Mutual inductance (EMU, cm) of two coaxial circular loops.

    Standard elliptic-integral formula (Maxwell, Treatise Ch. XVI;
    EMU with mu_0 -> 4 pi so inductance has dimensions of length):

        M = 4 pi sqrt(a1 a2) [ (2/k - k) K(k^2) - (2/k) E(k^2) ]
        k^2 = 4 a1 a2 / ((a1 + a2)^2 + d^2)

    Cross-checked: far-field limit reproduces the dipole result
    M -> pi^2 a1^2 a2^2... (agrees with the SI formula converted to cm at
    the (a/d)^2 level).
    """
    k_sq = 4.0 * a1 * a2 / ((a1 + a2) ** 2 + d * d)
    k = math.sqrt(k_sq)
    K = ellipk(k_sq)
    E = ellipe(k_sq)
    return 4.0 * math.pi * math.sqrt(a1 * a2) * ((2.0 / k - k) * K - (2.0 / k) * E)


def _mutual_gradient_oracle(a1: float, a2: float, d: float, h: float = 1e-4) -> float:
    """dM/dd (EMU, dimensionless) by central difference of the elliptic M."""
    return (
        _coaxial_mutual_inductance_emu(a1, a2, d + h)
        - _coaxial_mutual_inductance_emu(a1, a2, d - h)
    ) / (2.0 * h)


# ── R1 — D-03 (Art. 777): rapid-action correction inverted ────────────────


@pytest.mark.article(777)
@pytest.mark.regression(defect="D-03")
def test_regression_D03_art777_correction_halves_v():
    """Treatise Art. 777 — Stage 3 defect D-03 (S1).

    ``apply_rapid_action_correction`` returns ``measured_v / charge_fraction``.
    An under-charged condenser makes the measured v too LARGE
    (v_meas = v_true / charge_fraction), so the correction must MULTIPLY by the
    charge fraction. Engineered case: charge_fraction = 1 - exp(-t_half/RC) = 0.5
    exactly (t_half/RC = ln 2), so the corrected velocity must HALVE (0.5); the
    current code returns 2.0, amplifying the error. Property check: the
    correction must never amplify for any charge_fraction < 1.
    """
    # engineer charge_fraction = 0.5 exactly: 1 - exp(-t_half/RC) = 0.5
    f, RC = 1.0, 1.0 / (2.0 * math.log(2.0))  # t_half/RC = ln 2
    corrected = apply_rapid_action_correction(1.0, f, RC)
    # pre-fix code returned 2.0; golden pinned in the reference store
    assert corrected == pytest.approx(
        ref_value(777, "rapid_action_halving"),
        **tolerance_of(777, "rapid_action_halving"),
    )
    # property: under-charging always makes measured v too LARGE; the
    # correction must shrink it (never amplify) for any charge_fraction < 1
    for f_i, rc_i in [(1.0, 0.1), (10.0, 0.5), (0.5, 2.0)]:
        assert apply_rapid_action_correction(1.0, f_i, rc_i) < 1.0


# ── R2 — D-04 (Art. 812): Delta-n factor of 2 ─────────────────────────────


@pytest.mark.article(812)
@pytest.mark.regression(defect="D-04")
def test_regression_D04_art812_delta_n_identity():
    """Treatise Art. 812 — Stage 3 defect D-04 (S1).

    From theta = (k_L - k_R) L / 2 = V B L one obtains
    Delta-n = V B lambda / pi — NO factor 2. The current code computes
    Delta-n = 2 V lambda B / pi, so the velocity split is 2x too large.
    The kinematic closed loop (rotation per length = half the wavenumber
    split) is asserted in the implementation's (k_right - k_left)/2 sign
    convention — see module docstring deviation note.
    """
    c = CONST.C
    V, B, lam, n = 0.1, 1000.0, 5.893e-5, 1.5  # Verdet, field, wavelength, index
    # theta = (k_L - k_R) L / 2 = V B L  =>  dn = V B lam / pi  (NO factor 2)
    expected_dn = ref_value(812, "delta_n_sodium_D")
    dv = calc_circular_velocity_split(n, B, V, lam)
    expected_dv = c * expected_dn / n**2
    assert dv == pytest.approx(expected_dv, rel=1e-12)  # pre-fix code was 2x off
    # closed loop: rotation per length = half the wavenumber difference
    ka = perform_kinematic_analysis(1.0, k_right=2.0e5 * 0.999, k_left=2.0e5 * 1.001)
    assert ka["rotation_per_length"] == pytest.approx(
        ref_value(812, "rotation_per_length_closed_loop"),
        **tolerance_of(812, "rotation_per_length_closed_loop"),
    )


# ── R3 — D-01 (Arts. 801-803): diffusion time missing 4 pi / c^2 ──────────


@pytest.mark.article(801)
@pytest.mark.article(802)
@pytest.mark.regression(defect="D-01")
def test_regression_D01_art801_diffusion_time_copper_and_roundtrip():
    """Treatise Arts. 801-803 — Stage 3 defect D-01 (S1).

    CGS magnetic diffusion: dB/dt = (c^2 / 4 pi sigma) nabla^2 B, hence the
    characteristic time is tau = 4 pi sigma L^2 / c^2. For a 1 cm copper slab
    (sigma = 5.35e17 s^-1 CGS) this is tau = 7.48 ms. The current code returns
    sigma L^2 = 5.35e17 — a diffusivity, not a time. The round-trip check
    (length(time(L)) = L) is self-consistent even in the defective code, so the
    copper-slab golden value is the discriminating assertion; the round trip
    additionally guards that time and length are fixed as a mutually derivable
    pair (tau = 4 pi sigma L^2 / c^2, L = sqrt(t c^2 / 4 pi sigma)).
    """
    # golden: tau = 4 pi sigma L^2 / c^2 for copper, L = 1 cm
    # provenance: Stage 4 §2.5 reference store key art801_tau_copper_1cm
    sigma_cu = 5.35e17  # s^-1, CGS conductivity of copper
    tau_expected = ref_value(801, "tau_copper_1cm")  # = 7.4804e-3 s
    assert calc_diffusion_time(1.0, sigma_cu) == pytest.approx(
        tau_expected, **tolerance_of(801, "tau_copper_1cm")
    )  # pre-fix code returned sigma*L^2 ~ 5.35e17
    # round trip: length(time(L)) must recover L (pair fixed together)
    L, sigma = 2.5, 1.0e16
    assert calc_diffusion_length(calc_diffusion_time(L, sigma), sigma) == pytest.approx(
        L, rel=1e-9
    )


# ── R4 — D-02 (Art. 702): A_phi prefactor / near-axis asymptotic ──────────


@pytest.mark.article(702)
@pytest.mark.regression(defect="D-02")
def test_regression_D02_art702_near_axis_psi_and_curl():
    """Treatise Art. 702 — Stage 3 defect D-02 (S1).

    The stream function psi = rho * A_phi of a circular current must scale as
    rho^2 near the axis (A_phi ∝ rho), i.e. slope 2 in log-log; the defective
    prefactor gives ~2.5. Additionally B = curl A (central differences of the
    azimuthal vector potential) must reproduce the true field; an independent
    Biot-Savart quadrature is used as the oracle because ``calc_coil_off_axis``
    is itself defective (Stage 3 D-14/D-29/D-30) and would entangle this
    regression with a different defect.
    """
    a = 10.0
    # (i) near-axis asymptotic: psi = rho * A_phi ∝ rho^2  (slope -> 2)
    rhos = np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2]) * a
    psi = np.array([r * _vector_potential_azimuthal(1.0, a, r, 0.0) for r in rhos])
    # log-log slope by closed-form OLS (identical to np.polyfit(..., 1)[0] but
    # without LAPACK/SVD — immune to the Stage 4 §7 plugin-resedding crash mode)
    x = np.log(rhos)
    y = np.log(psi)
    x0, y0 = x - x.mean(), y - y.mean()
    slope = float(np.dot(x0, y0) / np.dot(x0, x0))
    assert slope == pytest.approx(2.0, abs=0.05)  # pre-fix code gave ~2.5
    # (ii) B = curl A must match the independent Biot-Savart oracle at
    # (rho, z) = (0.5 a, 0.25 a). Axisymmetric curl in cylindrical coords:
    #   B_rho = -dA_phi/dz ,  B_z = (1/rho) d(rho A_phi)/d rho
    rho0, z0, h = 0.5 * a, 0.25 * a, 1e-3

    def A_phi(rho, z):
        return _vector_potential_azimuthal(1.0, a, rho, z)

    B_rho_curl = -(A_phi(rho0, z0 + h) - A_phi(rho0, z0 - h)) / (2.0 * h)
    B_z_curl = (
        ((rho0 + h) * A_phi(rho0 + h, z0) - (rho0 - h) * A_phi(rho0 - h, z0))
        / (2.0 * h)
        / rho0
    )
    B_rho_ref, B_z_ref = _biot_savart_loop_B(1.0, a, rho0, z0)
    # rel 1e-3 accommodates the finite-difference curl (spec: 1e-5 vs the
    # analytic oracle); today both components are ~1e3 off.
    assert B_rho_curl == pytest.approx(B_rho_ref, rel=1e-3)
    assert B_z_curl == pytest.approx(B_z_ref, rel=1e-3)


# ── R5 — D-05 (Arts. 751-754): current weigher fabricated geometry ────────


@pytest.mark.article(751)
@pytest.mark.regression(defect="D-05")
def test_regression_D05_art751_force_equals_I2_dMdx():
    """Treatise Arts. 751-754 — Stage 3 defect D-05 (S1).

    In EMU the force between the weigher's coils is F = I^2 dM/dx with NO
    factor of c^2, where dM/dx comes from the elliptic-integral mutual
    inductance of two coaxial loops. The current code invents a near-field
    factor r^2/(d^2 + r^2) and divides by c^2 while taking abamperes — it is
    ~1e23 too small. Oracle: dM/dx by central difference of
    M = 4 pi sqrt(a1 a2) [ (2/k - k) K - (2/k) E ] (scipy elliptic integrals).
    The force is compared in magnitude (robust to the sign convention the fix
    adopts for dM/dx); equivalent_mass = force / g_standard is self-consistent
    today and after the fix (consistency guard only).
    """
    a, d, I = 10.0, 1.0, 0.1  # cm, cm, abamperes
    dMdx = _mutual_gradient_oracle(a, a, d)  # EMU oracle
    res = current_weigher(I, a, 1, 1, d)
    assert abs(res["force"]) == pytest.approx(
        I * I * abs(dMdx), rel=2e-3
    )  # EMU: no c^2 — pre-fix code gave ~1e-23 dyn instead of ~1.24 dyn
    assert res["equivalent_mass"] == pytest.approx(res["force"] / G_STANDARD, rel=1e-12)
