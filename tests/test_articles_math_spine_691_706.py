"""Qualifying article-evidence tests for the Cluster-A math spine (2026-08-21).

Scope (MATHEMATICA uplift, Stage 4 G3 evidence for LAST200):
  * Arts. 691-693  geometric mean distance        (maxwell/math/geometry/gmd.py)
  * Arts. 696-705  complete elliptic integrals   (maxwell/math/elliptic_integrals.py)
  * Arts. 670-679  circular-coil field machinery (maxwell/.../circular_coils.py,
                   whose elliptic core was replaced by the rigorous AGM evaluator)
  * Art.  675      citation-metadata regression guard for the Part I / Part IV
                   decorator split in maxwell/math/spherical_harmonics.py

Every reference value comes from an INDEPENDENT oracle — never by re-deriving
the code under test:
  O1  Hardcoded golden values with DLMF provenance; K(1/2) is additionally
      reproduced from the Gamma-function closed form Gamma(1/4)^2/(4 sqrt(pi)).
  O2  scipy.special.ellipk/ellipe (Carlson symmetric forms — a different
      algorithm from the AGM used by the code under test).
  O3  Legendre relation  E K' + E' K - K K' = pi/2.
  O4  Descending Landen identity  K(k) = (1 + k1) K(k1),  k1 = (1-k')/(1+k').
  O5  Direct Biot-Savart quadrature of the current loop.
  O6  Exact on-axis / dipole-asymptotic formulas from the definition of the
      magnetic moment of a circular current.
  O7  GMD overlap (lens) reduction of the defining double-area integral to one
      quadrature, valid for COINCIDENT sections (d = 0):
      ln R = (A1 A2)^-1 int lens(t) 2 pi ln(t) t dt.
  O8  Tensor Gauss-Legendre quadrature of the rectangle self-GMD (overlap-area
      reduction), golden 0.4470491559 for the unit square.
  O9  Full pairwise brute-force mean for coaxial rings.
  O10 Direct tensor Gauss-Legendre quadrature (polar nodes, weights r dr dth)
      of the defining 4-D double-area integral for OVERLAPPING circular
      sections, cross-validated by resolution doubling.
  O11 Exact harmonicity theorem: the mutual GMD of two NON-overlapping filled
      disks equals the centre distance d EXACTLY (mean-value property of the
      harmonic log kernel; every correction term vanishes identically).

Deviations recorded for the gate pack (Stage 4 §4.1):
  * No ``tests/articles/reference_values.json`` exists yet; goldens are inlined
    with provenance comments instead.
  * Articles 694, 695, 706 are NOT marked here: no code touched by this uplift
    claims them (they are covered by other clusters).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

# ── DLMF-provenance golden values ────────────────────────────────────────────
# Harvested into the central reference store (tests/articles/
# reference_values.json, Stage-4 C3); provenance recorded there per entry
# (DLMF 19.2; Gamma-oracle; converged tensor Gauss-Legendre oracle O8).
from articles import ref_value, tolerance_of  # noqa: E402
from scipy.integrate import quad
from scipy.special import ellipe, ellipj, ellipk, gamma

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import (
    calc_coaxial_coil_pair,
    calc_coil_off_axis,
    calc_coil_on_axis,
    calc_double_coil_field,
)
from maxwell.math.elliptic_integrals import (
    EllipticIntegral,
    analyze_elliptic_integrals,
    calc_complete_elliptic_e_parameter,
    calc_complete_elliptic_integral_first_kind,
    calc_complete_elliptic_integral_second_kind,
    calc_complete_elliptic_k_parameter,
    verify_elliptic_integrals,
)
from maxwell.math.geometry.gmd import (
    calc_gmd_coaxial_circles,
    calc_gmd_parallel_wires,
    calc_inductance_from_gmd,
    calc_self_gmd_circle,
    calc_self_gmd_rectangle,
)

K_HALF_GOLDEN = ref_value(696, "K_parameter_half")
E_HALF_GOLDEN = ref_value(697, "E_parameter_half")
K_NEG1_GOLDEN = ref_value(696, "K_parameter_neg1")
E_NEG1_GOLDEN = ref_value(697, "E_parameter_neg1")
SQUARE_GMD_GOLDEN = ref_value(692, "square_self_gmd")


# ═══════════════════════════════════════════════════════════════════════════
# A. Complete elliptic integrals, parameter convention (Arts. 696-705)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(696)
@pytest.mark.article(697)
def test_K_E_golden_values_tight():
    """Art. 696/697 — golden K(m)/E(m) at TIGHT tolerance (DLMF provenance).

    Oracles: (a) hardcoded DLMF values, (b) the Gamma-function closed form
    K(1/2) = Gamma(1/4)^2/(4 sqrt(pi)) — a derivation channel completely
    independent of both the AGM under test and scipy's Carlson forms.
    """
    # exact endpoints
    assert calc_complete_elliptic_k_parameter(0.0) == pytest.approx(
        math.pi / 2, rel=1e-14
    )
    assert calc_complete_elliptic_e_parameter(0.0) == pytest.approx(
        math.pi / 2, rel=1e-14
    )
    assert calc_complete_elliptic_e_parameter(1.0) == pytest.approx(1.0, abs=1e-15)
    # interior goldens
    assert calc_complete_elliptic_k_parameter(0.5) == pytest.approx(
        K_HALF_GOLDEN, rel=1e-14
    )
    assert calc_complete_elliptic_e_parameter(0.5) == pytest.approx(
        E_HALF_GOLDEN, rel=1e-14
    )
    # Gamma-oracle for K(1/2): independent of AGM and of scipy
    k_gamma = gamma(0.25) ** 2 / (4.0 * math.sqrt(math.pi))
    assert k_gamma == pytest.approx(K_HALF_GOLDEN, rel=1e-15)
    assert calc_complete_elliptic_k_parameter(0.5) == pytest.approx(k_gamma, rel=1e-14)
    # negative parameter (imaginary modulus)
    assert calc_complete_elliptic_k_parameter(-1.0) == pytest.approx(
        K_NEG1_GOLDEN, rel=1e-14
    )
    assert calc_complete_elliptic_e_parameter(-1.0) == pytest.approx(
        E_NEG1_GOLDEN, rel=1e-14
    )


@pytest.mark.article(696)
@pytest.mark.article(697)
def test_K_E_cross_check_carlson_grid():
    """Art. 696/697 — AGM values vs scipy Carlson forms on a wide grid.

    scipy.special.ellipk/ellipe use Carlson symmetric forms, an algorithm
    independent of the AGM; agreement at 1e-12 relative across m in
    [-50, 1 - 1e-12] (log-spaced near m = 1 and over negative m) validates
    the full-domain hardening, including the imaginary-modulus branch.
    """
    m_grid = np.concatenate(
        [
            np.linspace(-50.0, -0.5, 25),
            np.linspace(0.0, 0.99, 40),
            1.0 - np.logspace(-2, -12, 11),  # approach the singularity
        ]
    )
    worst_k = worst_e = 0.0
    for m in m_grid:
        dk = abs(calc_complete_elliptic_k_parameter(m) - ellipk(m)) / ellipk(m)
        de = abs(calc_complete_elliptic_e_parameter(m) - ellipe(m)) / ellipe(m)
        worst_k = max(worst_k, dk)
        worst_e = max(worst_e, de)
    assert worst_k < 1e-12
    assert worst_e < 1e-12


@pytest.mark.article(702)
def test_negative_parameter_imaginary_modulus_transform():
    """Art. 702 — imaginary-modulus (negative-parameter) transformation.

    DLMF §19.7: for m < 0, with m1 = m/(m-1) in (0, 1),
        K(m) = K(m1) / sqrt(1 - m),    E(m) = sqrt(1 - m) * E(m1).
    Checked as self-consistency of the hardened evaluator, plus the
    large-negative asymptotics E(m)/sqrt(1-m) -> 1 and K(m) -> 0+ (it
    decays like ln(4 sqrt(-m))/sqrt(-m)).
    """
    for m in [-0.5, -1.0, -4.0, -25.0]:
        m1 = m / (m - 1.0)
        s = math.sqrt(1.0 - m)
        assert calc_complete_elliptic_k_parameter(m) == pytest.approx(
            calc_complete_elliptic_k_parameter(m1) / s, rel=1e-13
        )
        assert calc_complete_elliptic_e_parameter(m) == pytest.approx(
            s * calc_complete_elliptic_e_parameter(m1), rel=1e-13
        )
    # asymptotics
    m_big = -1e12
    E_big = calc_complete_elliptic_e_parameter(m_big)
    assert E_big / math.sqrt(1.0 - m_big) == pytest.approx(1.0, rel=1e-6)
    K_big = calc_complete_elliptic_k_parameter(m_big)
    # K(m) ~ ln(4 sqrt(-m)) / sqrt(-m)  (leading logarithmic term)
    assert K_big == pytest.approx(
        math.log(4.0 * math.sqrt(-m_big)) / math.sqrt(-m_big), rel=1e-3
    )


@pytest.mark.article(700)
def test_landen_identity_full_loop():
    """Art. 700 — descending Landen transformation as an exact identity.

    k1 = (1 - k')/(1 + k'), k' = sqrt(1 - k^2);  K(k) = (1 + k1) K(k1).
    Verified with the hardened evaluator for several moduli, and iterated
    to the fixed point: after enough Landen steps K -> pi/2, and the
    accumulated prefactor must reproduce K(k) to machine precision.
    """
    for k in [0.2, 0.5, 0.8, 0.99]:
        kp = math.sqrt(1.0 - k * k)
        k1 = (1.0 - kp) / (1.0 + kp)
        K_k = calc_complete_elliptic_integral_first_kind(k)
        K_k1 = calc_complete_elliptic_integral_first_kind(k1)
        assert K_k == pytest.approx((1.0 + k1) * K_k1, rel=1e-13)
        # iterate to the AGM fixed point
        kx, pref = k, 1.0
        for _ in range(12):
            kxp = math.sqrt(1.0 - kx * kx)
            k_next = (1.0 - kxp) / (1.0 + kxp)
            pref *= 1.0 + k_next
            kx = k_next
            if kx < 1e-15:
                break
        assert pref * (math.pi / 2.0) == pytest.approx(K_k, rel=1e-12)
    # the dataclass helper returns a consistent (k1, K(k1)) pair
    ei = EllipticIntegral(modulus=0.5)
    k1, K1 = ei.landen_transformation()
    assert k1 < 0.5 and k1 > 0
    assert K1 == pytest.approx(
        calc_complete_elliptic_integral_first_kind(k1), rel=1e-12
    )


@pytest.mark.article(696)
@pytest.mark.article(697)
def test_legendre_relation():
    """Art. 696/697 — Legendre relation E K' + E' K - K K' = pi/2.

    A global identity tying the four complete integrals together; holds
    for every k in (0, 1).  Strong end-to-end check of the evaluator.
    """
    for k in [0.1, 0.3, 0.5, 0.7, 0.9, 0.999]:
        kp = math.sqrt(1.0 - k * k)
        K = calc_complete_elliptic_integral_first_kind(k)
        E = calc_complete_elliptic_integral_second_kind(k)
        Kp = calc_complete_elliptic_integral_first_kind(kp)
        Ep = calc_complete_elliptic_integral_second_kind(kp)
        lhs = E * Kp + Ep * K - K * Kp
        assert lhs == pytest.approx(math.pi / 2, rel=1e-13)


@pytest.mark.article(701)
@pytest.mark.article(702)
def test_complementary_modulus_and_parameter_convention():
    """Arts. 701/702 — complementary modulus and the m = k^2 convention.

    k' = sqrt(1 - k^2); the parameter-convention API must agree with the
    modulus-convention API at m = k^2, and accept negative m where the
    modulus is imaginary.
    """
    ei = EllipticIntegral(modulus=0.6)
    assert ei.complementary_modulus() == pytest.approx(0.8, rel=1e-14)
    assert EllipticIntegral(modulus=0.5).parameter() == pytest.approx(0.25, rel=1e-14)
    for k in [0.0, 0.3, 0.7, 0.999999]:
        assert calc_complete_elliptic_k_parameter(k**2) == pytest.approx(
            calc_complete_elliptic_integral_first_kind(k), rel=1e-14
        )
        assert calc_complete_elliptic_e_parameter(k**2) == pytest.approx(
            calc_complete_elliptic_integral_second_kind(k), rel=1e-14
        )
    with pytest.raises(ValueError):
        calc_complete_elliptic_k_parameter(1.5)  # real K undefined for m > 1


@pytest.mark.article(698)
def test_third_kind_reduces_to_first_kind():
    """Art. 698 — Pi(n=0; phi, k) = F(phi, k) (complete: Pi = K).

    Loose tolerance: the module evaluates incomplete integrals by
    trapezoidal quadrature, so this is an O(1e-4) structural check.
    """
    ei = EllipticIntegral(modulus=0.5)
    pi_zero = ei.third_kind(amplitude=np.pi / 2, characteristic=0.0)
    K = ei.first_kind(np.pi / 2)
    assert pi_zero == pytest.approx(K, rel=1e-3)


@pytest.mark.article(699)
def test_jacobian_identities():
    """Art. 699 — Jacobi function identities sn^2 + cn^2 = 1, dn^2 + k^2 sn^2 = 1."""
    ei = EllipticIntegral(modulus=0.6)
    for u in [0.0, 0.5, 1.0, 2.3]:
        sn, cn, dn = ei.jacobian_functions(u)
        assert sn**2 + cn**2 == pytest.approx(1.0, abs=1e-14)
        assert dn**2 + 0.6**2 * sn**2 == pytest.approx(1.0, abs=1e-14)
    # independent cross-check against scipy's ellipj (parameter m = k^2 = 0.36)
    sn, cn, dn, _ph = ellipj(1.0, 0.36)
    sn_e, cn_e, dn_e = EllipticIntegral(modulus=0.6).jacobian_functions(1.0)
    assert (sn_e, cn_e, dn_e) == pytest.approx((sn, cn, dn), rel=1e-13)


@pytest.mark.article(703)
@pytest.mark.article(704)
@pytest.mark.article(705)
def test_verify_and_analyze_elliptic_relations():
    """Arts. 703-705 — the module's own relation checks pass end-to-end.

    verify_elliptic_integrals exercises K/E values, the Legendre relation
    and the Jacobi identities; analyze_elliptic_integrals sweeps moduli.
    """
    res = verify_elliptic_integrals(modulus=0.5)
    assert res["verified"] is True
    assert res["legendre_error"] < 1e-10
    ana = analyze_elliptic_integrals(modulus_range=(0.0, 0.9, 5))
    Ks = list(ana["K_values"])
    assert all(Ks[i] < Ks[i + 1] for i in range(len(Ks) - 1))  # K increasing
    Es = list(ana["E_values"])
    assert all(Es[i] > Es[i + 1] for i in range(len(Es) - 1))  # E decreasing


# ═══════════════════════════════════════════════════════════════════════════
# B. Circular-coil field machinery (Arts. 670-679)
# ═══════════════════════════════════════════════════════════════════════════


def _biot_savart_loop_B(
    current: float, a: float, rho: float, z: float, npts: int = 8192
) -> tuple[float, float]:
    """Independent oracle: direct Biot-Savart quadrature of the loop.

    B(r) = (I/c) oint dl x (r - r') / |r - r'|^3 in Gaussian CGS,
    evaluated on the symmetry plane phi = 0.
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


@pytest.mark.article(670)
@pytest.mark.article(671)
@pytest.mark.article(672)
def test_on_axis_formula_center_and_dipole():
    """Arts. 670-672 — on-axis field B = 2 pi n I a^2 / (c (a^2+z^2)^{3/2}).

    Oracles: the formula itself evaluated independently; the center value
    2 pi I/(c a); the far-field dipole law B -> 2 pi I a^2/(c z^3) with the
    exact first correction (1 + (a/z)^2)^{-3/2}.
    """
    c = CONST.C
    I, a, n = 1.0, 10.0, 3
    for z in [0.0, 2.5, 10.0, 33.3]:
        expected = 2.0 * math.pi * n * I * a**2 / (c * (a**2 + z**2) ** 1.5)
        assert calc_coil_on_axis(I, a, z, n) == pytest.approx(expected, rel=1e-14)
    # center field
    assert calc_coil_on_axis(I, a, 0.0) == pytest.approx(
        2.0 * math.pi * I / (c * a), rel=1e-14
    )
    # far-field dipole with exact geometric correction
    z_far = 100.0 * a
    B_far = calc_coil_on_axis(I, a, z_far)
    dipole = 2.0 * math.pi * I * a**2 / (c * z_far**3)
    assert B_far == pytest.approx(dipole * (1.0 + (a / z_far) ** 2) ** -1.5, rel=1e-12)
    assert B_far == pytest.approx(dipole, rel=2e-4)  # leading dipole term


@pytest.mark.article(673)
@pytest.mark.article(674)
@pytest.mark.article(675)
def test_off_axis_matches_biot_savart_oracle():
    """Arts. 673-675 — off-axis elliptic formula vs Biot-Savart quadrature.

    Points stay a comfortable distance from the wire (the field diverges
    on the winding itself, where BOTH the closed form and the quadrature
    legitimately lose precision).
    """
    a = 10.0
    for rho, z in [(5.0, 2.5), (0.5, 3.0), (15.0, 4.0), (2.0, 20.0), (8.0, 1.0)]:
        B = calc_coil_off_axis(1.0, a, np.array([rho, 0.0, z]))
        B_rho_ref, B_z_ref = _biot_savart_loop_B(1.0, a, rho, z)
        assert B[2] == pytest.approx(B_z_ref, rel=1e-6)
        assert B[0] == pytest.approx(B_rho_ref, rel=1e-6)
        assert B[1] == pytest.approx(0.0, abs=1e-30)  # symmetry plane


@pytest.mark.article(673)
def test_off_axis_reduces_to_on_axis_continuously():
    """Art. 673 — the off-axis expression tends EXACTLY to the on-axis one.

    Limit rho -> 0 of the elliptic formula: K(0) = E(0) = pi/2 gives
    B_z -> 2 pi I a^2/(c (a^2+z^2)^{3/2}).  This is the continuity check
    that the pre-fix implementation failed (its alpha^2 prefactor left a
    spurious factor 1/sqrt(a^2+z^2)).
    """
    a = 10.0
    for z in [0.0, 2.5, 7.7, 15.0]:
        on = calc_coil_on_axis(1.0, a, z)
        off = calc_coil_off_axis(1.0, a, np.array([1e-9, 0.0, z]))[2]
        assert off == pytest.approx(on, rel=1e-8)


@pytest.mark.article(674)
@pytest.mark.article(675)
def test_off_axis_far_field_dipole_pattern():
    """Arts. 674/675 — far-field is the exact dipole pattern of moment
    mu = pi I a^2 / c:  axial B = 2 mu/r^3, equatorial B = -mu/r^3.

    Tolerance 2e-3 accommodates the O((a/r)^2) = 4e-4 quadrupole tail.
    """
    c = CONST.C
    I, a = 1.0, 1.0
    mu = math.pi * I * a**2 / c
    r = 50.0 * a
    B_axis = calc_coil_off_axis(I, a, np.array([0.0, 0.0, r]))
    assert B_axis[2] == pytest.approx(2.0 * mu / r**3, rel=2e-3)
    B_eq = calc_coil_off_axis(I, a, np.array([r, 0.0, 0.0]))
    assert B_eq[2] == pytest.approx(-mu / r**3, rel=2e-3)
    assert B_eq[0] == pytest.approx(0.0, abs=abs(mu / r**3) * 1e-6)


@pytest.mark.article(676)
@pytest.mark.article(677)
def test_helmholtz_superposition_and_uniformity():
    """Arts. 676/677 — Helmholtz pair: exact superposition at the centre
    and second-order axial uniformity (the d^2 B/dz^2 term vanishes at
    separation = radius, leaving O((z/a)^4) variation).
    """
    I, a = 1.0, 10.0
    B_center = calc_double_coil_field(I, a, np.array([0.0, 0.0, 0.0]))
    expected = 2.0 * calc_coil_on_axis(I, a, a / 2.0)
    assert B_center[2] == pytest.approx(expected, rel=1e-12)
    assert B_center[0] == pytest.approx(0.0, abs=1e-30)
    # axial uniformity: O((z/a)^4) — at z = 0.05 a expect ~1e-6 variation
    B_off = calc_double_coil_field(I, a, np.array([0.0, 0.0, 0.05 * a]))
    assert B_off[2] / B_center[2] == pytest.approx(1.0, abs=1e-5)


@pytest.mark.article(678)
@pytest.mark.article(679)
def test_coaxial_pair_antisymmetry():
    """Arts. 678/679 — equal coaxial coils with OPPOSITE currents.

    By symmetry the axial field cancels exactly on the mid-plane while
    the radial parts add: B_total(rho) = 2 * B_rho(single coil seen from
    z = +sep/2).
    """
    I, a, sep, rho = 1.0, 10.0, 6.0, 3.0
    B = calc_coaxial_coil_pair(
        I,
        a,
        a,
        np.array([rho, 0.0, 0.0]),
        sep,
        current1_dir=1,
        current2_dir=-1,
    )
    B_single = calc_coil_off_axis(I, a, np.array([rho, 0.0, sep / 2.0]))
    assert B[2] == pytest.approx(0.0, abs=1e-18)  # exact antisymmetry
    assert B[0] == pytest.approx(2.0 * B_single[0], rel=1e-12)


# ═══════════════════════════════════════════════════════════════════════════
# C. Geometric mean distance (Arts. 691-693)
# ═══════════════════════════════════════════════════════════════════════════


def _lens_overlap(a1: float, a2: float, t: float) -> float:
    """Overlap area of two disks (radii a1, a2) at centre distance t."""
    if t >= a1 + a2:
        return 0.0
    if t <= abs(a1 - a2):
        return math.pi * min(a1, a2) ** 2
    term1 = a1**2 * math.acos((t**2 + a1**2 - a2**2) / (2.0 * t * a1))
    term2 = a2**2 * math.acos((t**2 + a2**2 - a1**2) / (2.0 * t * a2))
    k = math.sqrt(
        max(
            (-t + a1 + a2) * (t + a1 - a2) * (t - a1 + a2) * (t + a1 + a2),
            0.0,
        )
    )
    return term1 + term2 - 0.5 * k


def _gmd_disk_oracle(a1: float, a2: float, d: float) -> float:
    """Independent GMD oracle for two filled circular sections (d = 0 only).

    For COINCIDENT centre positions the defining double-area integral
    reduces EXACTLY by the overlap (convolution) trick to ONE quadrature:

        ln R = (A1 A2)^-1 int_0^{a1+a2} lens(t) * 2 pi ln(t) t dt,

    because the difference vector r2 - r1 then ranges isotropically with
    density proportional to the lens overlap at separation t.  (For
    d > 0 the same one-dimensional ansatz is NOT exact; overlapping
    sections at d > 0 are instead checked against the direct tensor
    Gauss-Legendre oracle _gmd_tensor_gl_oracle, and disjoint sections
    against the exact harmonicity theorem GMD = d.)
    """
    assert d == 0.0, "lens reduction is exact only for coincident sections"
    A1A2 = (math.pi * a1**2) * (math.pi * a2**2)
    val, _ = quad(
        lambda t: _lens_overlap(a1, a2, t) * 2.0 * math.pi * math.log(t) * t,
        0.0,
        a1 + a2,
        limit=300,
    )
    return math.exp(val / A1A2)


def _gmd_tensor_gl_oracle(
    a1: float, a2: float, d: float, nr: int, ntheta: int
) -> float:
    """Independent oracle: tensor Gauss-Legendre on the defining integral.

    ln GMD = (A1 A2)^-1 int_{D1} int_{D2} ln|r1 - r2| dA1 dA2 evaluated
    in polar coordinates on each disk with exact area weights r dr dth.
    A completely different algorithm and reduction from the code under
    test; convergence is monitored by doubling the node counts.
    """
    x, w = np.polynomial.legendre.leggauss(nr)
    t, v = np.polynomial.legendre.leggauss(ntheta)
    r1 = 0.5 * a1 * (x + 1.0)
    wr1 = r1 * (0.5 * a1 * w)  # r dr on [0, a1]
    r2 = 0.5 * a2 * (x + 1.0)
    wr2 = r2 * (0.5 * a2 * w)
    th = math.pi * (t + 1.0)  # [0, 2 pi]
    wth = math.pi * v
    p1 = np.stack(
        [r1[:, None] * np.cos(th)[None, :], r1[:, None] * np.sin(th)[None, :]],
        axis=-1,
    ).reshape(-1, 2)
    w1 = (wr1[:, None] * wth[None, :]).reshape(-1)
    p2 = np.stack(
        [d + r2[:, None] * np.cos(th)[None, :], r2[:, None] * np.sin(th)[None, :]],
        axis=-1,
    ).reshape(-1, 2)
    w2 = (wr2[:, None] * wth[None, :]).reshape(-1)
    A1A2 = (math.pi * a1**2) * (math.pi * a2**2)
    assert abs(w1.sum() - math.pi * a1**2) < 1e-9
    assert abs(w2.sum() - math.pi * a2**2) < 1e-9
    total, step = 0.0, 400
    for i in range(0, len(p1), step):
        dp = p1[i : i + step, None, :] - p2[None, :, :]
        total += float(
            np.sum(
                w1[i : i + step, None] * w2[None, :] * np.log(np.sqrt((dp**2).sum(-1)))
            )
        )
    return math.exp(total / A1A2)


@pytest.mark.article(691)
def test_self_gmd_circle_exact():
    """Art. 691 — self-GMD of a circular section is EXACTLY a e^{-1/4}.

    Oracle: the overlap-integral reduction of the defining quadruple
    integral (see _gmd_disk_oracle).  Also pins the golden coefficient
    0.7788007830714049 = e^{-1/4}.
    """
    for a in [0.5, 1.0, 3.7]:
        oracle = _gmd_disk_oracle(a, a, 0.0)
        assert calc_self_gmd_circle(a) == pytest.approx(oracle, rel=1e-8)
    assert calc_self_gmd_circle(1.0) == pytest.approx(math.exp(-0.25), rel=1e-15)
    assert math.exp(-0.25) == pytest.approx(
        ref_value(691, "self_gmd_circle_coefficient"),
        **tolerance_of(691, "self_gmd_circle_coefficient"),
    )


@pytest.mark.article(692)
def test_self_gmd_rectangle_square_and_thin_strip():
    """Art. 692 — rectangle self-GMD 0.44705 (w+h)/2 (Kennelly).

    (i) Unit square vs the Gauss-Legendre golden SQUARE_GMD_GOLDEN
    (overlap-area reduction, tensor GL n=500, converged to 1e-9): the
    formula is exact to ~2e-6 relative.  (ii) Thin-strip limit: as
    h -> 0 the true GMD tends to the segment value w e^{-3/2} =
    0.223130... w; Kennelly reproduces it to ~2e-3.  A regression to the
    pre-fix formula 0.44705 (w+h) — twice too large — would fail both
    checks immediately.
    """
    assert calc_self_gmd_rectangle(1.0, 1.0) == pytest.approx(
        SQUARE_GMD_GOLDEN, **tolerance_of(692, "square_self_gmd")
    )
    thin = calc_self_gmd_rectangle(1.0, 1e-9)
    assert thin == pytest.approx(
        ref_value(692, "thin_strip_segment_coefficient"),
        **tolerance_of(692, "thin_strip_segment_coefficient"),
    )
    # regression guard: the old (factor-2) value is far away
    assert thin < 0.25


@pytest.mark.article(693)
def test_gmd_parallel_wires_disjoint_sections_exact():
    """Art. 693 — mutual GMD of two NON-overlapping circular sections is
    EXACTLY the centre distance (oracle O11).

    Proof pinned by the test: ln|r1 - r2| is harmonic in r2 away from r1,
    so for r1 outside disk 2 the disk mean-value theorem gives the inner
    average ln|r1 - c2|; that function is harmonic in r1 over disk 1
    whenever c2 is outside it, so the outer average is ln d.  EVERY
    correction term vanishes identically — the pre-2026-08-21 formula
    d (1 - (a1^2+a2^2)/(4 d^2)) had a spurious O((a/d)^2) term (not even
    the RMS-distance expansion, whose sign is +).  Also pins continuity
    at contact, d = a1 + a2.
    """
    a1, a2 = 0.1, 0.15
    for d in [0.3, 1.0, 10.0, 1000.0]:
        code = calc_gmd_parallel_wires(
            np.array([0.0, 0.0, 0.0]), np.array([d, 0.0, 0.0]), a1, a2
        )
        assert code == pytest.approx(d, rel=1e-15)  # exact, no correction
    # regression guard: the old spurious correction sat ~8e-3 away at d=1
    assert (
        abs(
            calc_gmd_parallel_wires(
                np.array([0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), a1, a2
            )
            - 1.0
        )
        < 1e-12
    )
    # continuity at contact
    touch = calc_gmd_parallel_wires(
        np.array([0.0, 0.0, 0.0]), np.array([a1 + a2, 0.0, 0.0]), a1, a2
    )
    assert touch == pytest.approx(a1 + a2, rel=1e-12)


@pytest.mark.article(693)
def test_gmd_parallel_wires_overlap_vs_tensor_quadrature():
    """Art. 693 — overlap branch vs the direct tensor Gauss-Legendre
    oracle O10 (independent algorithm and reduction).

    The oracle's own convergence is asserted first (two resolutions must
    agree), guarding against trusting a single discretization.  The
    concentric equal-disk limit must reproduce the self-GMD a e^{-1/4}.
    """
    cases = [(1.0, 1.0, 1.0), (2.0, 0.5, 1.0), (1.0, 1.0, 0.5)]
    for a1, a2, d in cases:
        code = calc_gmd_parallel_wires(
            np.array([0.0, 0.0, 0.0]), np.array([d, 0.0, 0.0]), a1, a2
        )
        gl_lo = _gmd_tensor_gl_oracle(a1, a2, d, 28, 56)
        gl_hi = _gmd_tensor_gl_oracle(a1, a2, d, 36, 72)
        assert gl_lo == pytest.approx(gl_hi, rel=2e-4)  # oracle converged
        assert code == pytest.approx(gl_hi, rel=1e-4)
    # concentric equal disks -> exact self-GMD limit
    g0 = calc_gmd_parallel_wires(np.zeros(3), np.zeros(3), 1.0, 1.0)
    assert g0 == pytest.approx(math.exp(-0.25), rel=1e-9)


@pytest.mark.article(692)
@pytest.mark.article(693)
def test_gmd_coaxial_rings_closed_form():
    """Arts. 692/693 — GMD of two coaxial circular filaments.

    Exact closed form from int ln(A - B cos t) dt = 2 pi ln((A+sqrt(A^2-B^2))/2):
    GMD^2 = (A + sqrt(A^2 - B^2))/2, A = a1^2 + a2^2 + d^2, B = 2 a1 a2.
    Oracles: (i) full pairwise brute-force mean over both loops (chunked);
    (ii) coincident equal loops give GMD = a exactly (self-GMD of a
    circular filament); (iii) far-field GMD = d (1 + (a1^2+a2^2)/(2 d^2)).
    """
    # (i) brute force, well-separated loops
    a1, a2, d = 10.0, 5.0, 3.0
    n = 2000
    theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    ln_mean = 0.0
    for chunk in range(0, n, 400):
        th1 = theta[chunk : chunk + 400]
        dt = th1[:, None] - theta[None, :]
        r2 = a1**2 + a2**2 - 2.0 * a1 * a2 * np.cos(dt) + d**2
        ln_mean += np.sum(np.log(r2))
    brute = math.exp(0.5 * ln_mean / (n * n))
    assert calc_gmd_coaxial_circles(a1, a2, d) == pytest.approx(brute, rel=1e-9)
    # (ii) coincident equal loops
    assert calc_gmd_coaxial_circles(3.0, 3.0, 0.0) == pytest.approx(3.0, rel=1e-14)
    # (iii) far field — rings sit FARTHER apart than d on average
    far = calc_gmd_coaxial_circles(1.0, 1.0, 50.0)
    assert far == pytest.approx(50.0 * (1.0 + 2.0 / (2.0 * 50.0**2)), rel=1e-6)
    assert far > 50.0


@pytest.mark.article(693)
def test_inductance_gmd_correction_self_consistent():
    """Art. 693 — finite-wire inductance correction from the self-GMD.

    With GMD = a e^{-1/4} the correction 4 pi R ln(a/GMD) collapses to
    exactly pi R; L_corrected = L_filament - pi R (per turn).
    """
    R, a_wire = 10.0, 0.1
    L_fil = 4.0 * math.pi * R * (math.log(8.0 * R / a_wire) - 2.0)
    L = calc_inductance_from_gmd(L_fil, a_wire, R)
    assert L == pytest.approx(L_fil - math.pi * R, rel=1e-12)


# ═══════════════════════════════════════════════════════════════════════════
# D. Citation-metadata regression guard (spherical harmonics split)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(675)
def test_spherical_harmonics_citation_split_keeps_part4_winning():
    """Art. 675 — Part I / Part IV decorator split regression guard.

    The 2026-08-21 metadata fix split 15 mixed decorators into stacked
    (part=1 below, part=4 above — the topmost decorator wins).  This test
    pins the outcome: every formerly mixed function still presents a
    Part IV citation containing ONLY Part IV articles (675-695); no Part I
    article (128-146) may leak into the winning citation.
    """
    from maxwell.math.spherical_harmonics import (
        LegendrePolynomial,
        SphericalHarmonic,
        calc_associated_legendre,
        calc_legendre_polynomial,
        calc_multipole_expansion,
        calc_spherical_harmonic,
        verify_spherical_harmonics,
    )
    from maxwell.meta.citation import get_citation

    lp = LegendrePolynomial(degree=2)
    sh = SphericalHarmonic(l=1, m=0)
    targets = {
        "LegendrePolynomial.evaluate": (lp.evaluate, {675}),
        "SphericalHarmonic.evaluate": (sh.evaluate, {685}),
        "calc_legendre_polynomial": (calc_legendre_polynomial, {675, 676}),
        "calc_associated_legendre": (calc_associated_legendre, {689}),
        "calc_spherical_harmonic": (calc_spherical_harmonic, {685}),
        "calc_multipole_expansion": (calc_multipole_expansion, {690, 691, 692}),
    }
    for name, (func, expected_arts) in targets.items():
        cit = get_citation(func)
        assert cit is not None, f"{name} lost its citation in the split"
        assert cit.part == 4, f"{name}: Part IV citation must win, got part={cit.part}"
        assert (
            set(cit.articles) == expected_arts
        ), f"{name}: expected Part IV arts {expected_arts}, got {cit.articles}"
        assert not any(
            128 <= a <= 146 for a in cit.articles
        ), f"{name}: Part I article leaked into the Part IV citation"
    cit_v = get_citation(verify_spherical_harmonics)
    assert cit_v.part == 4
    assert all(675 <= a <= 695 for a in cit_v.articles)
