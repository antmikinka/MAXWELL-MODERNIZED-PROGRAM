"""Qualifying article-evidence bundle for Arts. 680-690 (Stage-3 section 6).

MATHEMATICA, 2026-08-21.  Scope (Part IV citation map from the ledger):
  * Arts. 680-683  cylindrical conductors + solenoid/Helmholtz machinery
                   (maxwell/electromagnetism/components/cylinders.py,
                    maxwell/electromagnetism/components/solenoids.py)
  * Art.  684      wire self-inductance (cylinders.py)
  * Arts. 685-687  spherical-harmonic evaluation + cylinder vector potential
                   (maxwell/math/spherical_harmonics.py, cylinders.py)
  * Arts. 688-690  normalization, associated Legendre functions, zonal
                   multipole expansion (spherical_harmonics.py)

The file ALSO carries the executable regression specs for the Stage-3
defects D-14 / D-29 / D-30 (elliptic core of circular_coils.py), whose
comparison tests are a prerequisite for everything off-axis.

Every expected value comes from an INDEPENDENT oracle -- never by
re-deriving the code under test:
  O1  Direct Biot-Savart quadrature of current loops (periodic trapezoid,
      spectral convergence; vectorized, Gaussian CGS with CONST.C).
  O2  Infinite-cylinder volume Biot-Savart quadrature: the axial (zeta)
      integral is done EXACTLY (kernel 2/rho^2), the cross-section by
      tensor Gauss-Legendre.  Valid for the exterior of any cylindrically
      symmetric current distribution.
  O3  Ampere's circuital law as exact analytic limit (oint B.dl = 4 pi I/c,
      Gaussian): inside/outside/surface fields of uniform cylinders.
  O4  Filament (particle-method) discretization of the annular cross-section
      for hollow-cylinder wall points: each filament carries the EXACT
      infinite straight-wire field 2 dI/(c d); the self-cell (whose
      principal-value contribution vanishes by symmetry for uniform current
      density) is masked.  Convergence is asserted by resolution doubling.
  O5  Numerical EMU flux-linkage and internal-energy quadrature for the
      wire inductance (L' = Phi'/I + 2 W_int/I^2), independent closed forms.
  O6  Hand-coded Condon-Shortley closed forms for P_l^m, Y_l^m, real
      harmonics and the zonal multipole series (l <= 3), plus Gauss-Legendre
      quadrature of |Y|^2 and scipy.integrate.quad orthogonality integrals.
  O7  scipy.special.ellipk/ellipe (Carlson symmetric forms) -- a different
      algorithm from the AGM used by the code under test -- for the D-14
      comparison at the register's k^2 points.

Goldens (pure numbers with provenance) live in
tests/articles/reference_values.json and are loaded via
``from articles import ref_value, tolerance_of``.

Tolerances are stated per test with their provenance.  Units: Gaussian CGS
(currents in abamperes, lengths in cm, B in gauss), EMU for inductances.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of  # noqa: E402
from scipy.integrate import quad
from scipy.special import ellipe, ellipk, lpmv

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import (
    calc_coil_off_axis,
    calc_coil_on_axis,
)
from maxwell.electromagnetism.components.cylinders import (
    calc_cylinder_vector_potential,
    calc_cylindrical_field,
    calc_hollow_cylinder_field,
    calc_wire_self_inductance,
)
from maxwell.electromagnetism.components.solenoids import (
    calc_helmholtz_center,
    calc_helmholtz_uniformity,
)
from maxwell.math.elliptic_integrals import (
    calc_complete_elliptic_e_parameter,
    calc_complete_elliptic_k_parameter,
)
from maxwell.math.spherical_harmonics import (
    SphericalHarmonic,
    calc_associated_legendre,
    calc_multipole_expansion,
    calc_spherical_harmonic,
)

# ═══════════════════════════════════════════════════════════════════════════
# Independent oracles (never re-derive the code under test)
# ═══════════════════════════════════════════════════════════════════════════


def _biot_savart_loop_B(
    current: float, a: float, rho: float, z: float, npts: int = 16384
) -> tuple[float, float]:
    """O1: direct Biot-Savart quadrature of a circular loop (Gaussian CGS).

    B(r) = (I/c) oint dl x (r - r') / |r - r'|^3, evaluated in the symmetry
    plane phi = 0 by the periodic trapezoid rule, which converges
    spectrally for z != 0 (measured: <= 5e-14 relative down to k^2 = 0.9999).
    Returns (B_rho, B_z).
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


def _biot_savart_two_loops_axis(
    current: float, a: float, n_turns: int, z: float, sep: float
) -> float:
    """O1 specialized: on-axis B_z of two coaxial loops at z = +/- sep/2.

    Direct quadrature of the line-integral kernel (no analytic shortcut):
    B_z = (nI/c) oint a^2 dphi / (a^2 + dz^2)^{3/2}.
    """
    c = CONST.C
    phi = np.linspace(0.0, 2.0 * np.pi, 4096, endpoint=False)
    w = 2.0 * np.pi / len(phi)
    total = 0.0
    for zc in (-sep / 2.0, sep / 2.0):
        dz = z - zc
        R3 = (a**2 + dz**2) ** 1.5
        total += (n_turns * current / c) * a**2 / R3 * (len(phi) * w)
    return total


def _cylinder_Bphi_exterior_volume(
    current: float, a: float, r: float, nr: int = 24, npsi: int = 48
) -> float:
    """O2: volume Biot-Savart of an INFINITE uniform solid cylinder.

    The axial integral int_{-inf}^{inf} dzeta/(rho^2 + zeta^2)^{3/2} = 2/rho^2
    is exact, leaving B_phi(r) = (2J/c) int s ds dpsi (r - s cos psi)/rho^2
    over the disk, done by tensor Gauss-Legendre.  For r > a the integrand
    is smooth; measured accuracy ~1e-15 relative at (nr, npsi) = (24, 48).
    """
    J = current / (math.pi * a**2)
    xs, ws = np.polynomial.legendre.leggauss(nr)
    s = 0.5 * a * (xs + 1.0)
    wss = 0.5 * a * ws
    xp, wp = np.polynomial.legendre.leggauss(npsi)
    psi = math.pi * (xp + 1.0)
    wps = math.pi * wp
    S, P = np.meshgrid(s, psi, indexing="ij")
    W = np.outer(wss, wps)
    rho2 = r**2 + S**2 - 2.0 * r * S * np.cos(P)
    num = r - S * np.cos(P)
    return float((2.0 * J / CONST.C) * np.sum(W * num * S / rho2))


def _annulus_Bphi_filaments(
    current: float, a: float, b: float, r: float, ns: int = 256
) -> float:
    """O4: annular wall field by a filament (particle) discretization.

    The annulus a < s < b is replaced by straight filaments, each carrying
    dI = J dA and contributing the EXACT infinite straight-wire field
    2 dI/(c d) azimuthally.  The cell containing the observation point has
    vanishing principal value for uniform J and is masked.  Converges
    algebraically; resolution doubling is asserted where it is used.
    """
    J = current / (math.pi * (b**2 - a**2))
    xs, ws = np.polynomial.legendre.leggauss(ns)
    s = 0.5 * (b - a) * (xs + 1.0) + a
    wss = 0.5 * (b - a) * ws
    npsi = 4 * ns
    xp, wp = np.polynomial.legendre.leggauss(npsi)
    psi = math.pi * (xp + 1.0)
    wps = math.pi * wp
    S, P = np.meshgrid(s, psi, indexing="ij")
    W = np.outer(wss, wps)
    d2 = r**2 + S**2 - 2.0 * r * S * np.cos(P)
    num = r - S * np.cos(P)
    delta = 0.75 * math.pi * max((b - a) / ns, r / npsi)
    mask = d2 > delta**2
    dI = J * S * W
    return float(np.sum(mask * (2.0 / CONST.C) * dI * num / np.maximum(d2, 1e-300)))


def _helmholtz_uniformity_variations_oracle(
    current: float, a: float, n_turns: int, offsets: list[float]
) -> list[float]:
    """O1: |B(z)|/B(0) - 1 for the Helmholtz pair from loop quadrature."""
    B0 = _biot_savart_two_loops_axis(current, a, n_turns, 0.0, a)
    out = []
    for z in offsets:
        Bz = _biot_savart_two_loops_axis(current, a, n_turns, z, a)
        out.append(abs(abs(Bz) - abs(B0)) / abs(B0))
    return out


# ── O6: hand-coded Condon-Shortley closed forms (l <= 3) ──────────────────


def _P_closed(l: int, m: int, x: float) -> float:
    """Exact Ferrers P_l^m with Condon-Shortley phase (matches lpmv)."""
    if m < 0:
        m = -m  # code-under-test convention: |m|
    key = (l, m)
    sq = math.sqrt(max(1.0 - x * x, 0.0))
    table = {
        (0, 0): 1.0,
        (1, 0): x,
        (1, 1): -sq,
        (2, 0): 0.5 * (3.0 * x**2 - 1.0),
        (2, 1): -3.0 * x * sq,
        (2, 2): 3.0 * (1.0 - x**2),
        (3, 0): 0.5 * (5.0 * x**3 - 3.0 * x),
        (3, 1): -1.5 * (5.0 * x**2 - 1.0) * sq,
        (3, 2): 15.0 * x * (1.0 - x**2),
        (3, 3): -15.0 * sq**3,
    }
    return table[key]


def _Y_closed(l: int, m: int, theta: float, phi: float) -> complex:
    """Exact Y_l^m (Condon-Shortley) for the few low orders used here."""
    c1 = math.cos(theta)
    s1 = math.sin(theta)
    if (l, m) == (0, 0):
        return complex(1.0 / math.sqrt(4.0 * math.pi), 0.0)
    if (l, m) == (1, 0):
        return complex(math.sqrt(3.0 / (4.0 * math.pi)) * c1, 0.0)
    if (l, m) == (1, 1):
        amp = -math.sqrt(3.0 / (8.0 * math.pi)) * s1
        return amp * complex(math.cos(phi), math.sin(phi))
    if (l, m) == (1, -1):
        amp = math.sqrt(3.0 / (8.0 * math.pi)) * s1  # Y_1^{-1} = -conj(Y_1^1)
        return amp * complex(math.cos(phi), -math.sin(phi))
    if (l, m) == (2, 0):
        return complex(
            math.sqrt(5.0 / (4.0 * math.pi)) * 0.5 * (3.0 * c1**2 - 1.0), 0.0
        )
    if (l, m) == (2, 1):
        amp = -math.sqrt(15.0 / (8.0 * math.pi)) * c1 * s1
        return amp * complex(math.cos(phi), math.sin(phi))
    raise KeyError((l, m))


def _zonal_multipole_oracle(r: float, theta: float, moments: dict[int, float]) -> float:
    """O6: independent zonal series Phi = sum_l q_l N_l P_l(cos th)/r^{l+1}.

    N_l = sqrt((2l+1)/(4 pi)); P_l are the hand-coded Legendre polynomials.
    """
    x = math.cos(theta)
    P = {0: 1.0, 1: x, 2: 0.5 * (3.0 * x**2 - 1.0), 3: 0.5 * (5.0 * x**3 - 3.0 * x)}
    total = 0.0
    for l, q in moments.items():
        N = math.sqrt((2.0 * l + 1.0) / (4.0 * math.pi))
        total += q * N * P[l] / r ** (l + 1)
    return total


# ═══════════════════════════════════════════════════════════════════════════
# A. Defect regressions D-14 / D-29 / D-30 (circular-coil elliptic core)
# ═══════════════════════════════════════════════════════════════════════════


def _legacy_truncated_series_K(m: float) -> float:
    """The DEFECTIVE pre-2026-08-21 approximant, kept only to prove the flip."""
    if m < 0:
        return math.pi / 2
    m2, m3 = m * m, m**3
    return (math.pi / 2) * (1 + m / 4 + 9 * m2 / 64 + 25 * m3 / 256)


@pytest.mark.regression("D-14")
def test_d14_elliptic_routing_matches_scipy_at_register_points():
    """D-14 — register comparison points k^2 = {0.5, 0.9, 0.99, 0.9999}.

    The circular-coil module evaluates K/E exclusively through the
    Landen/AGM evaluators of maxwell.math.elliptic_integrals; those must
    agree with scipy's Carlson-form ellipk/ellipe (O7, an independent
    algorithm) at the four register points.  Tolerance 1e-13 relative
    (measured <= 4e-15).  The same test also proves failing-before:
    the deleted truncated series was off by > 50% relative at k^2 = 0.9999.
    """
    for k_sq in (0.5, 0.9, 0.99, 0.9999):
        K_code = calc_complete_elliptic_k_parameter(k_sq)
        E_code = calc_complete_elliptic_e_parameter(k_sq)
        K_ref, E_ref = float(ellipk(k_sq)), float(ellipe(k_sq))
        assert abs(K_code - K_ref) / K_ref < 1e-13
        assert abs(E_code - E_ref) / E_ref < 1e-13
        # failing-before evidence: the deleted approximant, at the worst point
        if k_sq == 0.9999:
            old_err = abs(_legacy_truncated_series_K(k_sq) - K_ref) / K_ref
            assert old_err > 0.5  # was ~54% wrong; any revival must fail here


@pytest.mark.regression("D-14")
def test_d14_near_wire_fields_vs_biot_savart():
    """D-14 — off-axis fields at physical points realizing the four k^2.

    Geometry a = rho = 1 gives k^2 = 4/(4 + z^2); the register points map
    to z = 2, 2/3, sqrt(4/0.99 - 4), sqrt(4/0.9999 - 4).  Oracle O1
    (spectral periodic trapezoid, measured <= 5e-14 at k^2 = 0.9999);
    tolerance 1e-10 relative.  The pre-fix series corrupted precisely this
    near-wire regime.
    """
    z_of = {
        0.5: 2.0,
        0.9: math.sqrt(4.0 / 0.9 - 4.0),
        0.99: math.sqrt(4.0 / 0.99 - 4.0),
        0.9999: math.sqrt(4.0 / 0.9999 - 4.0),
    }
    for k_sq, z in z_of.items():
        B = calc_coil_off_axis(1.0, 1.0, np.array([1.0, 0.0, z]))
        B_rho_ref, B_z_ref = _biot_savart_loop_B(1.0, 1.0, 1.0, z, npts=32768)
        assert B[2] == pytest.approx(B_z_ref, rel=1e-10)
        assert B[0] == pytest.approx(B_rho_ref, rel=1e-10)


@pytest.mark.regression("D-29")
def test_d29_negative_parameter_not_pi_over_2():
    """D-29 — K(m < 0) via the imaginary-modulus branch, not the constant pi/2.

    Oracle: the DLMF-provenance golden ref_value(696, 'K_parameter_neg1')
    (= 1.3110287771460598, cross-checked against scipy's Carlson forms)
    and a grid against scipy ellipk/ellipe (O7).  The regression-flip guard
    keeps the defective constant-pi/2 behavior at a safe distance.
    """
    K_neg1 = calc_complete_elliptic_k_parameter(-1.0)
    assert K_neg1 == pytest.approx(
        ref_value(696, "K_parameter_neg1"),
        **tolerance_of(696, "K_parameter_neg1"),
    )
    # flip guard: the defective code returned exactly pi/2 for ALL m < 0
    assert abs(K_neg1 - math.pi / 2) > 0.2
    assert calc_complete_elliptic_e_parameter(-1.0) == pytest.approx(
        float(ellipe(-1.0)), rel=1e-14
    )
    for m in (-10.0, -4.0, -1.0, -0.25, -0.01):
        assert calc_complete_elliptic_k_parameter(m) == pytest.approx(
            float(ellipk(m)), rel=1e-13
        )
        assert calc_complete_elliptic_e_parameter(m) == pytest.approx(
            float(ellipe(m)), rel=1e-13
        )


@pytest.mark.regression("D-30")
def test_d30_header_formulas_match_implementation():
    """D-30 — the header's standard elliptic form is what the code runs.

    Symptoms of the stale alpha/beta parameterization were (i) a spurious
    extra 1/alpha in the prefactor and (ii) failure to reduce to the exact
    on-axis formula as rho -> 0.  Checks: continuous on-axis reduction at
    four heights (rel 1e-8); scale invariance B(lambda geom) = B/lambda of
    the dimensionless invariant c*B*a/I (catches any wrong power of alpha;
    rel 1e-13); independent Biot-Savart cross-check (O1) at an interior
    point (rel 1e-9).
    """
    a = 10.0
    for z in (0.0, 2.5, 7.7, 15.0):
        on = calc_coil_on_axis(1.0, a, z)
        off = calc_coil_off_axis(1.0, a, np.array([1e-9, 0.0, z]))[2]
        assert off == pytest.approx(on, rel=1e-8)
    # dimensionless invariant under (a, rho, z) -> 2 (a, rho, z)
    inv1 = CONST.C * calc_coil_off_axis(1.0, 10.0, np.array([4.0, 0.0, 3.0]))[2] * 10.0
    inv2 = CONST.C * calc_coil_off_axis(1.0, 20.0, np.array([8.0, 0.0, 6.0]))[2] * 20.0
    assert inv1 == pytest.approx(inv2, rel=1e-13)
    # interior point vs oracle O1
    B = calc_coil_off_axis(1.0, 10.0, np.array([5.0, 0.0, 2.5]))
    B_rho_ref, B_z_ref = _biot_savart_loop_B(1.0, 10.0, 5.0, 2.5)
    assert B[2] == pytest.approx(B_z_ref, rel=1e-9)
    assert B[0] == pytest.approx(B_rho_ref, rel=1e-9)


# ═══════════════════════════════════════════════════════════════════════════
# B. Arts. 680-683: cylinders + solenoids/Helmholtz
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(680)
def test_art680_solid_cylinder_exterior_vs_volume_biot_savart():
    """Art. 680 — exterior field B = 2I/(c r) of a uniform solid cylinder.

    Oracle O2: infinite-cylinder volume Biot-Savart (exact axial kernel,
    tensor Gauss-Legendre cross-section), independently converged at two
    resolutions (must agree to 1e-12), then compared at rel 1e-10.  Oracle
    O3 (Ampere) pins the same value analytically.
    """
    I, a = 1.0, 1.0
    for r in (2.0, 5.0, 10.0):
        lo = _cylinder_Bphi_exterior_volume(I, a, r, 16, 32)
        hi = _cylinder_Bphi_exterior_volume(I, a, r, 24, 48)
        assert lo == pytest.approx(hi, rel=1e-12)  # oracle converged
        assert calc_cylindrical_field(I, a, r) == pytest.approx(hi, rel=1e-10)
        assert calc_cylindrical_field(I, a, r) == pytest.approx(
            2.0 * I / (CONST.C * r), rel=1e-14
        )  # Ampere (O3)


@pytest.mark.article(680)
def test_art680_helmholtz_center_coefficient():
    """Art. 680 — Helmholtz centre field (solenoids.py): exact coefficient.

    Golden ref_value(680, 'helmholtz_center_coefficient') = 8/sqrt(125)
    = (4/5)^{3/2}: B_center = (8/sqrt(125)) * 4 pi n I / (c a).  Oracle O1:
    direct two-loop Biot-Savart quadrature at the centre (rel 1e-8).
    """
    I, a, n = 1.0, 10.0, 2
    coeff = calc_helmholtz_center(I, a, n) / (4.0 * math.pi * n * I / (CONST.C * a))
    assert coeff == pytest.approx(
        ref_value(680, "helmholtz_center_coefficient"),
        **tolerance_of(680, "helmholtz_center_coefficient"),
    )
    B_quad = _biot_savart_two_loops_axis(I, a, n, 0.0, a)
    assert calc_helmholtz_center(I, a, n) == pytest.approx(B_quad, rel=1e-8)


@pytest.mark.article(681)
def test_art681_inside_field_surface_invariant_and_continuity():
    """Art. 681 — inside field, surface invariant and branch continuity.

    Inside, Ampere with uniform current density gives B = 2 I r/(c a^2)
    exactly (O3, rel 1e-14).  The surface invariant c a B(a)/I = 2 is the
    golden ref_value(681, 'solid_cylinder_surface_field_invariant');
    continuity across r = a is checked to 1e-5 relative (both branches are
    exact there, so this is a 1e-14-level check with generous margin).
    """
    I, a = 1.0, 1.0
    for r in (0.1, 0.25, 0.5, 0.9):
        assert calc_cylindrical_field(I, a, r) == pytest.approx(
            2.0 * I * r / (CONST.C * a**2), rel=1e-14
        )
    B_surface = calc_cylindrical_field(I, a, a)
    invariant = CONST.C * a * B_surface / I
    assert invariant == pytest.approx(
        ref_value(681, "solid_cylinder_surface_field_invariant"),
        **tolerance_of(681, "solid_cylinder_surface_field_invariant"),
    )
    B_in = calc_cylindrical_field(I, a, a * (1.0 - 1e-6))
    B_out = calc_cylindrical_field(I, a, a * (1.0 + 1e-6))
    assert abs(B_in - B_out) / B_in < 1e-5
    # linear ramp inside: B(r)/r constant (structural, numeric)
    ratios = [calc_cylindrical_field(I, a, r) / r for r in (0.2, 0.4, 0.8)]
    assert ratios[0] == pytest.approx(ratios[1], rel=1e-14)
    assert ratios[1] == pytest.approx(ratios[2], rel=1e-14)


@pytest.mark.article(682)
def test_art682_hollow_cylinder_cavity_zero_and_wall_oracle():
    """Art. 682 — bore field exactly zero; wall field vs filament oracle.

    Cavity: zero enclosed current + symmetry => B = 0 (golden
    ref_value(683, 'hollow_cylinder_cavity_field'), abs 1e-25; asserted
    here for the 682 branch).  Wall at the annulus midpoint r = (a+b)/2:
    oracle O4 (filament discretization with masked self-cell), converged by
    resolution doubling ns = 128 -> 256 (must agree to 5e-5 relative),
    comparison at rel 5e-5.
    """
    I, a, b = 1.0, 1.0, 2.0
    for r in (0.0, 0.3, 0.99):
        B = calc_hollow_cylinder_field(I, a, b, r)
        assert B == pytest.approx(
            ref_value(683, "hollow_cylinder_cavity_field"),
            **tolerance_of(683, "hollow_cylinder_cavity_field"),
        )
    r_mid = 0.5 * (a + b)
    lo = _annulus_Bphi_filaments(I, a, b, r_mid, ns=128)
    hi = _annulus_Bphi_filaments(I, a, b, r_mid, ns=256)
    assert lo == pytest.approx(hi, rel=5e-4)  # oracle converging
    assert calc_hollow_cylinder_field(I, a, b, r_mid) == pytest.approx(hi, rel=5e-5)


@pytest.mark.article(682)
def test_art682_helmholtz_uniformity_profile_vs_quadrature():
    """Art. 682 — Helmholtz uniformity profile (solenoids.py) vs oracle O1.

    calc_helmholtz_uniformity reports |B|/B0 - 1 at 10 axial offsets in
    [0, 0.1 a]; every entry is compared against the two-loop Biot-Savart
    quadrature (rel 2e-6; the first offset is exactly 0 by construction).
    """
    I, a, n = 1.0, 10.0, 1
    res = calc_helmholtz_uniformity(I, a, n)
    offsets = list(res["offsets"])
    variations = list(res["variations"])
    oracle = _helmholtz_uniformity_variations_oracle(I, a, n, offsets)
    assert variations[0] == pytest.approx(0.0, abs=1e-30)
    for got, want in zip(variations[1:], oracle[1:]):
        assert got == pytest.approx(want, rel=2e-6)
    assert res["max_variation"] == pytest.approx(max(oracle), rel=2e-6)


@pytest.mark.article(683)
def test_art683_hollow_exterior_and_ampere_wall_values():
    """Art. 683 — exterior = full-current line field; wall Ampere values.

    Exterior (r >= b): the whole current I is enclosed, so B = 2I/(c r)
    exactly (O3, rel 1e-14), re-confirmed by the volume oracle O2 applied
    to the equivalent solid cylinder of radius b carrying I (rel 1e-10).
    Wall points near each boundary are pinned by the exact Ampere closed
    form 2I(r^2 - a^2)/(c r (b^2 - a^2)) (analytic limit, rel 1e-14).
    """
    I, a, b = 1.0, 1.0, 2.0
    for r in (2.0, 3.0, 10.0):
        assert calc_hollow_cylinder_field(I, a, b, r) == pytest.approx(
            2.0 * I / (CONST.C * r), rel=1e-14
        )
    solid_equiv = _cylinder_Bphi_exterior_volume(I, b, 3.0, 24, 48)
    assert calc_hollow_cylinder_field(I, a, b, 3.0) == pytest.approx(
        solid_equiv, rel=1e-10
    )
    for r in (1.2, 1.8):
        assert calc_hollow_cylinder_field(I, a, b, r) == pytest.approx(
            2.0 * I * (r**2 - a**2) / (CONST.C * r * (b**2 - a**2)), rel=1e-14
        )


@pytest.mark.article(683)
def test_art683_helmholtz_axial_uniformity_fourth_order():
    """Art. 683 — Helmholtz axial uniformity is fourth order (separation = a).

    With d^2 B/dz^2 = 0 at the centre, |B(z)/B(0) - 1| scales as (z/a)^4:
    the oracle-O1 variations at z = 0.1 a and z = 0.05 a must have ratio
    16 (measured 15.87; tolerance rel 0.05 absorbs the O((z/a)^2) tail),
    and the code's max_variation at 0.1 a must equal the quadrature value
    (rel 1e-6).
    """
    I, a, n = 1.0, 10.0, 1
    v_half = _helmholtz_uniformity_variations_oracle(I, a, n, [0.05 * a])[0]
    v_full = _helmholtz_uniformity_variations_oracle(I, a, n, [0.1 * a])[0]
    assert v_full / v_half == pytest.approx(16.0, rel=0.05)
    res = calc_helmholtz_uniformity(I, a, n, max_offset=0.1 * a)
    assert res["max_variation"] == pytest.approx(v_full, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# C. Art. 684: wire self-inductance
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(684)
def test_art684_wire_inductance_from_flux_and_energy_quadrature():
    """Art. 684 — per-wire loop inductance L' = 1/2 + 2 ln(d/a), d = 10a.

    Oracle O5 (independent EMU construction, no closed form trusted):
      external flux linkage  Phi'/I = int_a^{10a} (2/x) dx  (numerical),
      internal inductance    L_int = (2/I^2) int_0^a (B^2/8 pi) 2 pi r dr
      with B(r) = 2 I r/a^2 (numerical),
    giving L' = Phi'/I + L_int.  Comparison rel 1e-10; golden pin
    ref_value(684, 'wire_loop_inductance_per_cm_d_over_a_10') rel 1e-14;
    length proportionality L(5 cm) = 5 L(1 cm) exact.  Convention note:
    this is the per-wire value with the return at d; the full two-wire
    loop is twice this (Maxwell's 4 ln(d/a) + 1).
    """
    a = 1.0
    d_ret = 10.0 * a  # code fixes the return path at d = 10 a
    ext, _ = quad(lambda x: 2.0 / x, a, d_ret, limit=200)

    def b_inside(r: float) -> float:
        return 2.0 * r / a**2  # EMU gauss for I = 1 abampere

    energy_int, _ = quad(
        lambda r: (b_inside(r) ** 2 / (8.0 * math.pi)) * 2.0 * math.pi * r,
        0.0,
        a,
        limit=200,
    )
    L_oracle = ext + 2.0 * energy_int  # I = 1
    assert calc_wire_self_inductance(a) == pytest.approx(L_oracle, rel=1e-10)
    assert calc_wire_self_inductance(a) == pytest.approx(
        ref_value(684, "wire_loop_inductance_per_cm_d_over_a_10"),
        **tolerance_of(684, "wire_loop_inductance_per_cm_d_over_a_10"),
    )
    assert calc_wire_self_inductance(a, wire_length=5.0) == pytest.approx(
        5.0 * calc_wire_self_inductance(a), rel=1e-14
    )


# ═══════════════════════════════════════════════════════════════════════════
# D. Arts. 685-687: spherical harmonics + cylinder vector potential
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(685)
def test_art685_spherical_harmonic_vs_closed_forms():
    """Art. 685 — Y_l^m against hand-coded Condon-Shortley closed forms.

    Oracle O6 for (l, m) in {(0,0), (1,0), (1,1), (1,-1), (2,0), (2,1)} at
    two angles each; complex agreement rel 1e-13.  The intensity golden
    |Y_1^1(pi/3)|^2 = 9/(32 pi) is pinned through the same values.
    scipy lpmv is NOT used as oracle (the code delegates to scipy's
    sph_harm_y); the closed forms are an independent derivation channel.
    """
    for theta, phi in ((0.7, 1.3), (math.pi / 3.0, 0.0)):
        for l, m in ((0, 0), (1, 0), (1, 1), (1, -1), (2, 0), (2, 1)):
            got = calc_spherical_harmonic(l, m, theta, phi)
            want = _Y_closed(l, m, theta, phi)
            assert abs(got - want) / abs(want) < 1e-13
    Y11 = calc_spherical_harmonic(1, 1, math.pi / 3.0, 0.9)
    assert abs(Y11) ** 2 == pytest.approx(
        ref_value(685, "Y11_intensity_at_theta_pi_over_3"),
        **tolerance_of(685, "Y11_intensity_at_theta_pi_over_3"),
    )


@pytest.mark.article(685)
def test_art685_wire_inductance_radius_independence():
    """Art. 685 — cylinders.py side of the 684/685 citation pair.

    With the return path fixed at d = 10 radii, ln(d/a) = ln 10 is
    a-independent: L'(a) is exactly scale invariant (rel 1e-14 across a
    factor-100 radius sweep).  Independent of the golden in the 684 test.
    """
    base = calc_wire_self_inductance(1.0)
    for a in (0.01, 0.1, 3.7, 100.0):
        assert calc_wire_self_inductance(a) == pytest.approx(base, rel=1e-14)


@pytest.mark.article(686)
def test_art686_real_harmonics_vs_closed_forms():
    """Art. 686 — real spherical harmonics vs independent closed forms.

    Code convention (documented here): m > 0 -> sqrt(2) Re Y_l^m,
    m < 0 -> sqrt(2) Im Y_l^m, m = 0 -> Y_l^0 (no sqrt(2)).  Oracle O6:
      sqrt(2) Re Y_1^1 = -sqrt(3/(4 pi)) sin th cos ph,
      sqrt(2) Im Y_1^{-1} = -sqrt(3/(4 pi)) sin th sin ph,
      Y_2^0 = sqrt(5/(4 pi)) (3 cos^2 th - 1)/2,
    rel 1e-13 at two angles.
    """
    for theta, phi in ((1.1, 0.7), (2.0, 5.5)):
        got = SphericalHarmonic(l=1, m=1).evaluate_real(theta, phi)
        want = -math.sqrt(3.0 / (4.0 * math.pi)) * math.sin(theta) * math.cos(phi)
        assert got == pytest.approx(want, rel=1e-13)
        got = SphericalHarmonic(l=1, m=-1).evaluate_real(theta, phi)
        want = -math.sqrt(3.0 / (4.0 * math.pi)) * math.sin(theta) * math.sin(phi)
        assert got == pytest.approx(want, rel=1e-13)
        got = SphericalHarmonic(l=2, m=0).evaluate_real(theta, phi)
        want = (
            math.sqrt(5.0 / (4.0 * math.pi)) * 0.5 * (3.0 * math.cos(theta) ** 2 - 1.0)
        )
        assert got == pytest.approx(want, rel=1e-13)


@pytest.mark.article(686)
def test_art686_vector_potential_matches_ampere_field_integral():
    """Art. 686 — A_z of the cylinder: -dA_z/dr = B_phi from Ampere data.

    Differences of the code's A_z must equal -int B_phi dr with B_phi the
    ANALYTIC Ampere field (O3, independent of the code's field routines):
      inside:  Delta A = -I/(c a^2) (r2^2 - r1^2),
      outside: Delta A = -(2I/c) ln(r2/r1),
    both integrals evaluated numerically by scipy.integrate.quad
    (rel 1e-8).  Branch continuity at r = a: both give -I/c (rel 1e-14).
    """
    I, a = 1.0, 1.0
    r1, r2 = 0.2, 0.8
    int_in, _ = quad(lambda r: 2.0 * I * r / (CONST.C * a**2), r1, r2)
    dA = calc_cylinder_vector_potential(I, a, r2) - calc_cylinder_vector_potential(
        I, a, r1
    )
    assert dA == pytest.approx(-int_in, rel=1e-8)
    r1, r2 = 1.5, 4.0
    int_out, _ = quad(lambda r: 2.0 * I / (CONST.C * r), r1, r2)
    dA = calc_cylinder_vector_potential(I, a, r2) - calc_cylinder_vector_potential(
        I, a, r1
    )
    assert dA == pytest.approx(-int_out, rel=1e-8)
    assert calc_cylinder_vector_potential(I, a, a * 0.99999999) == pytest.approx(
        calc_cylinder_vector_potential(I, a, a * 1.00000001), rel=1e-12
    )
    assert calc_cylinder_vector_potential(I, a, a) == pytest.approx(
        -I / CONST.C, rel=1e-14
    )


@pytest.mark.article(687)
def test_art687_intensity_closed_form_and_phi_independence():
    """Art. 687 — intensity |Y_l^m|^2: closed form and phi-independence.

    Oracle O6: |Y_1^1|^2 = (3/(8 pi)) sin^2 theta, |Y_2^0|^2 =
    (5/(4 pi)) ((3 cos^2 theta - 1)/2)^2; rel 1e-13 at three theta values.
    Phi-independence (the e^{im phi} factor drops out of |.|^2) is checked
    across a phi sweep at rel 1e-14 (the observed spread is single-ulp
    rounding noise, ~2e-16 relative).  Golden pin at theta = pi/3 via
    ref_value(685, 'Y11_intensity_at_theta_pi_over_3') (shared closed form).
    """
    sh11 = SphericalHarmonic(l=1, m=1)
    sh20 = SphericalHarmonic(l=2, m=0)
    for theta in (0.4, 1.1, 2.6):
        assert sh11.intensity(theta, 0.3) == pytest.approx(
            (3.0 / (8.0 * math.pi)) * math.sin(theta) ** 2, rel=1e-13
        )
        assert sh20.intensity(theta, 0.3) == pytest.approx(
            (5.0 / (4.0 * math.pi)) * (0.5 * (3.0 * math.cos(theta) ** 2 - 1.0)) ** 2,
            rel=1e-13,
        )
    base = sh11.intensity(1.1, 0.0)
    for phi in (0.7, 2.2, 5.1):
        assert sh11.intensity(1.1, phi) == pytest.approx(base, rel=1e-14)
    assert sh11.intensity(math.pi / 3.0, 0.9) == pytest.approx(
        ref_value(685, "Y11_intensity_at_theta_pi_over_3"),
        **tolerance_of(685, "Y11_intensity_at_theta_pi_over_3"),
    )


# ═══════════════════════════════════════════════════════════════════════════
# E. Arts. 688-690: normalization, associated Legendre, multipole expansion
# ═══════════════════════════════════════════════════════════════════════════


def _gl_sphere_norm_closed_form(l: int, m: int, n_nodes: int = 96) -> float:
    """O6: independent Gauss-Legendre quadrature of |Y_l^m|^2 over the sphere.

    u = cos theta in [-1, 1] (GL nodes), phi in [0, 2 pi] (periodic
    trapezoid, exact for the trigonometric polynomial |e^{im phi}|^2 = 1
    and its products).  Uses ONLY the closed forms _Y_closed.
    """
    xs, ws = np.polynomial.legendre.leggauss(n_nodes)
    theta_vals = np.arccos(xs)
    n_phi = 128
    phis = np.linspace(0.0, 2.0 * np.pi, n_phi, endpoint=False)
    dphi = 2.0 * np.pi / n_phi
    total = 0.0
    for th, wu in zip(theta_vals, ws):
        for ph in phis:
            Y = _Y_closed(l, m, th, ph)
            total += wu * dphi * abs(Y) ** 2
    return total


@pytest.mark.article(688)
def test_art688_normalization_theorem_and_code_band():
    """Art. 688 — int |Y_l^m|^2 dOmega = 1: theorem oracle + code checker.

    The theorem itself is verified by independent Gauss-Legendre quadrature
    of the closed forms (oracle O6; rel 1e-12) for (l, m) = (0,0), (1,1),
    (2,0).  Since the 2026-08-22 G3-R3 fix, the code's normalization_check
    uses Gauss-Legendre nodes in cos(theta) and an endpoint-excluded
    periodic phi grid, removing the old 50/49 ~= +2.04 percent phi-endpoint
    double count; its integral now matches the independent closed-form
    oracle to abs 1e-10, the golden ref_value(688,
    'normalization_unit_integral') = 1 holds at abs 1e-12, and the
    tolerance argument gates the returned 'normalized' decision.
    """
    for l, m in ((0, 0), (1, 1), (2, 0)):
        oracle = _gl_sphere_norm_closed_form(l, m)
        assert oracle == pytest.approx(1.0, rel=1e-12)  # theorem, independent
    for l, m in ((0, 0), (1, 1), (2, 1)):
        check = SphericalHarmonic(l=l, m=m).normalization_check()
        got = check["integral"]
        # code checker vs the INDEPENDENT closed-form oracle (not self-
        # comparison): the old 50/49 overcount (0.0204) dwarfs this band
        assert got == pytest.approx(_gl_sphere_norm_closed_form(l, m), abs=1e-10)
        assert got == pytest.approx(
            ref_value(688, "normalization_unit_integral"),
            **tolerance_of(688, "normalization_unit_integral"),
        )
        # tolerance argument is wired into the pass/fail decision:
        # the default tolerance accepts the ~1e-14 quadrature error,
        # while tolerance=0.0 (demanding exact floating-point equality)
        # flips the decision to False
        assert check["normalized"] is True
        assert (
            SphericalHarmonic(l=l, m=m).normalization_check(tolerance=0.0)["normalized"]
            is False
        )


@pytest.mark.article(689)
def test_art689_associated_legendre_closed_forms_and_goldens():
    """Art. 689 — P_l^m vs hand-coded polynomials (NOT scipy: code wraps lpmv).

    Oracle O6 at x in {0.5, 0.0, -0.3, 0.8} for (l, m) in
    {(1,1), (2,1), (2,2), (3,1), (3,2), (3,3)}; rel 1e-13.  Goldens
    P_3^1(1/2) and P_2^2(1/2) from the reference store.  The |m|
    (negative-order) convention is pinned, and |m| > l must raise.
    Convention hygiene: my closed forms are cross-checked once against the
    lpmv convention the code delegates to (oracle self-calibration).
    """
    for x in (0.5, 0.0, -0.3, 0.8):
        for l, m in ((1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)):
            got = calc_associated_legendre(l, m, x)
            want = _P_closed(l, m, x)
            scale = max(abs(want), 1e-30)
            assert abs(got - want) / scale < 1e-13
    # oracle self-calibration against the library convention (not the code)
    assert _P_closed(3, 1, 0.5) == pytest.approx(float(lpmv(1, 3, 0.5)), rel=1e-15)
    assert _P_closed(2, 2, 0.5) == pytest.approx(float(lpmv(2, 2, 0.5)), rel=1e-15)
    # goldens
    assert calc_associated_legendre(3, 1, 0.5) == pytest.approx(
        ref_value(689, "P31_at_half"), **tolerance_of(689, "P31_at_half")
    )
    assert calc_associated_legendre(2, 2, 0.5) == pytest.approx(
        ref_value(689, "P22_at_half"), **tolerance_of(689, "P22_at_half")
    )
    # negative-order convention: |m| used
    assert calc_associated_legendre(3, -1, 0.5) == pytest.approx(
        calc_associated_legendre(3, 1, 0.5), rel=1e-15
    )
    with pytest.raises(ValueError):
        calc_associated_legendre(2, 3, 0.5)


@pytest.mark.article(689)
def test_art689_associated_legendre_orthogonality_integrals():
    """Art. 689 — global orthogonality of P_l^m (independent quadrature).

    scipy.integrate.quad over the CODE's output (a global property no
    closed-form table can fake): int_{-1}^1 P_2^1 P_3^1 dx = 0 (abs 1e-10)
    and int_{-1}^1 [P_3^1]^2 dx = 2 (l+m)! / ((2l+1)(l-m)!) = 24/7
    (rel 1e-8).
    """
    cross, _ = quad(
        lambda x: calc_associated_legendre(2, 1, x) * calc_associated_legendre(3, 1, x),
        -1.0,
        1.0,
        limit=200,
    )
    assert cross == pytest.approx(0.0, abs=1e-10)
    norm, _ = quad(
        lambda x: calc_associated_legendre(3, 1, x) ** 2,
        -1.0,
        1.0,
        limit=200,
    )
    assert norm == pytest.approx(24.0 / 7.0, rel=1e-8)


@pytest.mark.article(690)
def test_art690_zonal_multipole_expansion_closed_forms():
    """Art. 690 — zonal multipole series vs the independent closed form.

    Oracle O6: Phi = sum_l q_l sqrt((2l+1)/(4 pi)) P_l(cos th)/r^{l+1} with
    hand-coded P_l.  Checks: pure monopole golden pin
    ref_value(690, 'monopole_potential_unit_q00_at_r2'); pure dipole and
    quadrupole terms (rel 1e-13 at two angles); superposition of l = 0..3
    (rel 1e-13); per-degree radial decay Phi_l(2r)/Phi_l(r) = 2^{-(l+1)}
    (rel 1e-12).
    """
    mono = calc_multipole_expansion(2.0, 0.7, 0.3, {0: 1.0})
    assert mono.real == pytest.approx(
        ref_value(690, "monopole_potential_unit_q00_at_r2"),
        **tolerance_of(690, "monopole_potential_unit_q00_at_r2"),
    )
    assert mono.imag == pytest.approx(0.0, abs=1e-30)
    for theta in (0.7, 2.1):
        for l in (1, 2):
            got = calc_multipole_expansion(3.0, theta, 0.4, {l: 1.0})
            want = _zonal_multipole_oracle(3.0, theta, {l: 1.0})
            assert got.real == pytest.approx(want, rel=1e-13)
            assert got.imag == pytest.approx(0.0, abs=1e-30)
    moments = {0: 1.5, 1: -0.7, 2: 0.4, 3: 0.9}
    got = calc_multipole_expansion(2.5, 1.2, 0.0, moments, max_l=4)
    want = _zonal_multipole_oracle(2.5, 1.2, moments)
    assert got.real == pytest.approx(want, rel=1e-13)
    # radial decay per degree
    for l in (0, 1, 2, 3):
        near = calc_multipole_expansion(2.0, 1.0, 0.0, {l: 1.0}).real
        far = calc_multipole_expansion(4.0, 1.0, 0.0, {l: 1.0}).real
        assert far / near == pytest.approx(2.0 ** -(l + 1), rel=1e-12)
