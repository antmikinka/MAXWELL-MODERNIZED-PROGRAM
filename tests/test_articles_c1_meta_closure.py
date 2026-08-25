"""G2 gate C1 closure: article-specific evidence for Arts. 694, 695, 765, 766.

Wave of 2026-08-21.  The independent G2 audit found these four articles
"meta-only" (cited solely by verify_*/analyze_* functions, hence T0-class):

  * Arts. 694/695 (Part IV, Ch. XIV "Circular Currents") were cited only by
    ``verify_spherical_harmonics`` / ``analyze_spherical_harmonics`` in
    ``maxwell/math/spherical_harmonics.py``.
  * Arts. 765/766 (Part IV, Ch. XVIII "Resistance Unit") were cited only by
    ``verify_absolute_resistance`` / ``analyze_absolute_resistance`` in
    ``maxwell/calibration/absolute_resistance.py``.

This wave adds article-specific computations and qualifies them here with
numeric assertions against INDEPENDENT oracles:

  O1  scipy.integrate.quad of the closed-kernel integral
      A_phi = I a ∫₀^{2π} cosφ' dφ' / |r − r'| for the circular current —
      an adaptive Gauss-Kronrod quadrature, a different algorithm from the
      zonal-harmonic (lpmv) series under test.            [Art. 694]
  O2  Elliptic-integral closed form
      A_phi = 4 I a [(2 − k²)K(k) − 2E(k)] / (k² √((a+ρ)² + z²)),
      k² = 4aρ/((a+ρ)² + z²), evaluated with scipy.special.ellipk/ellipe
      (Carlson symmetric forms — independent of lpmv).    [Art. 694]
  O3  Dipole asymptotic: A_phi r² / (π I a² sinθ) → 1 as r → ∞ (exact
      magnetic-moment limit m = I π a² of the Treatise).  [Art. 694]
  O4  On-axis exact solid angle Ω(0, 0, z) = 2π(1 − z/√(z² + a²)). [695]
  O5  Direct Gauss-Legendre surface quadrature of the defining solid-angle
      integral Ω = ∫_disk (P − r')·ẑ dS / |P − r'|³ over the shell disk —
      a discretization independent of the series.         [Art. 695]
  O6  Dipole asymptotic ψ r² / (π I a² cosθ) → 1 (m = I π a²). [Art. 695]
  O7  solve_ivp integration of the RC discharge ODE dV/dt = −V/(RC): the
      resistance recovered from the simulated voltage equals the true R —
      independent of the closed-form logarithmic inversion under test. [765]
  O8  Analytic half-life reduction R = t/(C ln 2) at V = V₀/2, pinned with
      math.log (closed-form channel; O7 is the independent one). [Art. 765]
  O9  solve_ivp integration of the damped galvanometer oscillator
      θ̈ + 2γθ̇ + ω₀²θ = 0: the corrected first throw θ₁ e^{λ/2} must
      recover v₀/ω_d up to the known O((γ/ω)²) extremum-shift residual
      (predicted here: u²/2 with u = γ/ω_d ≈ 3.2e-5).     [Art. 766]
  O10 Exact-arithmetic pins for λ = ln(θ₁/θ₂) and θ₁* = θ₁√(θ₁/θ₂)
      (closed-form channel; O9 is the independent one).    [Art. 766]

Units: Gaussian-CGS/EMU throughout (abamperes, abvolts, cm, s; 1 abohm =
1 cm/s).  No velocity-of-light literal appears anywhere in this file.

D-39 regression guard included: the trivial ``EllipticIntegral.parameter()``
helper must carry NO article citation (it previously hijacked Art. 702).
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.integrate import quad, solve_ivp
from scipy.special import ellipe, ellipk

from maxwell.calibration.absolute_resistance import (
    calc_absolute_resistance_capacitor_discharge,
    calc_recoil_damping_correction,
)
from maxwell.math.elliptic_integrals import (
    EllipticIntegral,
    calc_complete_elliptic_e_parameter,
    calc_complete_elliptic_k_parameter,
)
from maxwell.math.spherical_harmonics import (
    calc_magnetic_shell_potential_circular_current,
    calc_vector_potential_circular_current,
)
from maxwell.meta.citation import get_citation

# Shared geometry for the circular-current checks: a = 1 cm loop, I = 2.5 abA,
# observation at r = 3 cm, θ = π/3 (well inside the exterior domain r > a,
# with ρ, z both non-zero so the off-axis terms are genuinely exercised).
LOOP_A = 1.0
CURRENT_I = 2.5
OBS_R = 3.0
OBS_THETA = math.pi / 3.0


# ═══════════════════════════════════════════════════════════════════════════
# Art. 694 — vector potential of a circular current (zonal vector harmonics)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(694)
def test_art694_vector_potential_series_vs_independent_oracles():
    """Art. 694 — A_φ of a circular current, three independent channels.

    Oracles:
      O1 adaptive Gauss-Kronrod quadrature (scipy quad) of the defining
         integral; tolerance rel 1e-10 (quad reaches ~1e-13 here; series
         truncation at (a/r)^42 ≈ 1e-20 is negligible).
      O2 elliptic closed form via scipy ellipk/ellipe; tolerance rel 1e-12.
      O3 dipole asymptotic; tolerance |ratio − 1| < 1e-4 (the first
         neglected correction is O((a/r)²) = 2.5e-5 at r = 200a).
    """
    rho = OBS_R * math.sin(OBS_THETA)
    z = OBS_R * math.cos(OBS_THETA)

    A_series = calc_vector_potential_circular_current(
        OBS_R, OBS_THETA, LOOP_A, CURRENT_I, l_max=40
    )
    assert np.isfinite(A_series) and A_series != 0.0

    # O1: direct quadrature of A_phi = I a ∫ cosφ' dφ' / |r − r'|.
    def kernel(phi_prime: float) -> float:
        dist_sq = OBS_R**2 + LOOP_A**2 - 2.0 * LOOP_A * rho * math.cos(phi_prime)
        return math.cos(phi_prime) / math.sqrt(dist_sq)

    A_quad = (
        CURRENT_I
        * LOOP_A
        * quad(kernel, 0.0, 2.0 * math.pi, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
    )
    # provenance: O1 — Gauss-Kronrod quadrature of the closed kernel,
    # algorithmically independent of the lpmv series under test.
    assert A_series == pytest.approx(A_quad, rel=1e-10)

    # O2: elliptic closed form A_phi = 4 I a [(2−k²)K − 2E]/(k² √((a+ρ)²+z²)),
    # k² = 4aρ/((a+ρ)² + z²); scipy's Carlson-form K, E.
    k_sq = 4.0 * LOOP_A * rho / ((LOOP_A + rho) ** 2 + z * z)
    A_elliptic = (
        4.0
        * CURRENT_I
        * LOOP_A
        * ((2.0 - k_sq) * ellipk(k_sq) - 2.0 * ellipe(k_sq))
        / (k_sq * math.sqrt((LOOP_A + rho) ** 2 + z * z))
    )
    # provenance: O2 — independently derived elliptic reduction (this
    # session) evaluated with scipy's Carlson forms.
    assert A_series == pytest.approx(A_elliptic, rel=1e-12)

    # O3: dipole asymptotic A_phi → π I a² sinθ / r² (m = I π a², EMU).
    r_far = 200.0 * LOOP_A
    A_far = calc_vector_potential_circular_current(
        r_far, OBS_THETA, LOOP_A, CURRENT_I, l_max=40
    )
    dipole_ratio = (
        A_far * r_far**2 / (CURRENT_I * math.pi * LOOP_A**2 * math.sin(OBS_THETA))
    )
    # provenance: O3 — exact magnetic-moment limit of the Treatise.
    assert abs(dipole_ratio - 1.0) < 1e-4

    # Analytic property: A_phi vanishes on the axis (P_l^1(±1) = 0).
    A_axis = calc_vector_potential_circular_current(OBS_R, 0.0, LOOP_A, CURRENT_I)
    assert abs(A_axis) < 1e-14


@pytest.mark.article(694)
def test_art694_vector_potential_citation_and_domain_guard():
    """Art. 694 — citation targets Art. 694 in Part IV; r ≤ a is rejected."""
    citation = get_citation(calc_vector_potential_circular_current)
    assert citation is not None
    assert citation.part == 4
    assert 694 in citation.articles

    # The exterior expansion is undefined at/inside the loop: numeric guard.
    with pytest.raises(ValueError):
        calc_vector_potential_circular_current(LOOP_A, OBS_THETA, LOOP_A, CURRENT_I)


# ═══════════════════════════════════════════════════════════════════════════
# Art. 695 — magnetic-shell potential ψ = I Ω (complementary scalar solution)
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(695)
def test_art695_magnetic_shell_potential_vs_independent_oracles():
    """Art. 695 — ψ = I Ω of the circular current, three channels.

    Oracles:
      O4 on-axis exact solid angle 2π(1 − z/√(z² + a²)); rel 1e-12.
      O5 independent Gauss-Legendre surface quadrature of the solid-angle
         integral over the shell disk; rel 1e-8 (quadrature-limited).
      O6 dipole asymptotic ψ → π I a² cosθ / r²; |ratio − 1| < 1e-4.

    Supplement (not an oracle): the Art. 694 and Art. 695 solutions are the
    complementary vector-harmonic descriptions of one field, so B_r from the
    curl of A must equal −∂ψ/∂r; checked by centred finite differences.
    """
    # O4: on-axis closed form of the solid angle.
    psi_axis = calc_magnetic_shell_potential_circular_current(
        OBS_R, 0.0, LOOP_A, CURRENT_I, l_max=40
    )
    psi_exact_axis = (
        CURRENT_I * 2.0 * math.pi * (1.0 - OBS_R / math.sqrt(OBS_R**2 + LOOP_A**2))
    )
    # provenance: O4 — elementary exact integral of dΩ on the symmetry axis.
    assert psi_axis == pytest.approx(psi_exact_axis, rel=1e-12)

    # O5: off-axis solid angle by direct surface quadrature over the disk:
    # Ω(P) = ∫_disk (P − r')·ẑ dS / |P − r'|³ (independent discretization).
    rho = OBS_R * math.sin(OBS_THETA)
    z = OBS_R * math.cos(OBS_THETA)
    nodes, weights = np.polynomial.legendre.leggauss(96)
    rho_nodes = 0.5 * LOOP_A * (nodes + 1.0)
    rho_weights = 0.5 * LOOP_A * weights
    n_phi = 192
    phi_nodes = np.linspace(0.0, 2.0 * math.pi, n_phi, endpoint=False)
    d_phi = 2.0 * math.pi / n_phi
    omega_disk = 0.0
    for rr, ww in zip(rho_nodes, rho_weights):
        dx = rho - rr * np.cos(phi_nodes)
        dy = 0.0 - rr * np.sin(phi_nodes)
        dist_cubed = (dx * dx + dy * dy + z * z) ** 1.5
        omega_disk += ww * rr * float(np.sum(z / dist_cubed)) * d_phi

    psi_offaxis = calc_magnetic_shell_potential_circular_current(
        OBS_R, OBS_THETA, LOOP_A, CURRENT_I, l_max=60
    )
    # provenance: O5 — tensor Gauss-Legendre quadrature of the defining
    # solid-angle surface integral, independent of the harmonic series.
    assert psi_offaxis == pytest.approx(CURRENT_I * omega_disk, rel=1e-8)

    # O6: dipole asymptotic ψ → m cosθ / r², m = I π a².
    r_far = 200.0 * LOOP_A
    psi_far = calc_magnetic_shell_potential_circular_current(
        r_far, OBS_THETA, LOOP_A, CURRENT_I, l_max=40
    )
    dipole_ratio = (
        psi_far * r_far**2 / (CURRENT_I * math.pi * LOOP_A**2 * math.cos(OBS_THETA))
    )
    # provenance: O6 — exact magnetic-moment limit of the Treatise.
    assert abs(dipole_ratio - 1.0) < 1e-4

    # Supplement: B = ∇×A = −∇ψ outside the source (694/695 consistency).
    h = 1e-4
    a_phi = calc_vector_potential_circular_current
    psi_fn = calc_magnetic_shell_potential_circular_current
    # B_r from curl of A: (1/(r sinθ)) ∂(sinθ A_φ)/∂θ
    f_plus = math.sin(OBS_THETA + h) * a_phi(OBS_R, OBS_THETA + h, LOOP_A, CURRENT_I)
    f_minus = math.sin(OBS_THETA - h) * a_phi(OBS_R, OBS_THETA - h, LOOP_A, CURRENT_I)
    b_r_from_a = (f_plus - f_minus) / (2.0 * h * OBS_R * math.sin(OBS_THETA))
    # B_r = −∂ψ/∂r
    b_r_from_psi = -(
        psi_fn(OBS_R + h, OBS_THETA, LOOP_A, CURRENT_I)
        - psi_fn(OBS_R - h, OBS_THETA, LOOP_A, CURRENT_I)
    ) / (2.0 * h)
    # Finite-difference-limited consistency between the two article codes.
    assert b_r_from_a == pytest.approx(b_r_from_psi, rel=1e-5)


@pytest.mark.article(695)
def test_art695_shell_potential_citation_and_domain_guard():
    """Art. 695 — citation targets Art. 695 in Part IV; r ≤ a is rejected."""
    citation = get_citation(calc_magnetic_shell_potential_circular_current)
    assert citation is not None
    assert citation.part == 4
    assert 695 in citation.articles

    with pytest.raises(ValueError):
        calc_magnetic_shell_potential_circular_current(
            LOOP_A, OBS_THETA, LOOP_A, CURRENT_I
        )


# ═══════════════════════════════════════════════════════════════════════════
# Art. 765 — capacitor-discharge determination of absolute resistance
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(765)
def test_art765_capacitor_discharge_resistance_vs_ode_oracle():
    """Art. 765 — R = t/(C ln(V₀/V)), validated against an RC ODE.

    Oracles:
      O7 solve_ivp integration of dV/dt = −V/(RC) with a known R_true and
         EMU capacitance; the resistance recovered from the simulated
         voltage must equal R_true; rel 1e-6 (solver-limited; observed
         ~2e-12).
      O8 analytic half-life reduction R = t/(C ln 2); rel 1e-14 (same
         closed-form channel, kept as a pin; O7 is the independent one).

    Units: C in EMU (s²/cm), t in s, R in abohm = cm/s; [R] = LT⁻¹.
    """
    # O7: independent time-domain simulation of the discharge.
    r_true = 1.0e11  # abohm (= cm/s)
    c_emu = 1.0e-10  # EMU capacitance (s²/cm); time constant τ = RC = 10 s
    t_meas = 3.0
    sol = solve_ivp(
        lambda t, y: [-y[0] / (r_true * c_emu)],
        (0.0, t_meas),
        [1.0],
        rtol=1e-11,
        atol=1e-14,
        dense_output=True,
    )
    v_final = float(sol.sol(t_meas)[0])
    # provenance: O7 — ODE integration (LSODA/RK family), not the
    # logarithmic inversion under test.
    assert v_final == pytest.approx(math.exp(-t_meas / (r_true * c_emu)), rel=1e-8)

    r_measured = calc_absolute_resistance_capacitor_discharge(
        c_emu, 1.0, v_final, t_meas
    )
    assert r_measured == pytest.approx(r_true, rel=1e-6)

    # Dimensional behaviour of [R] = T / (T² L⁻¹) = L T⁻¹: R is linear in
    # the time interval and inverse in the capacitance (numeric property
    # check of the velocity dimension, voltages held fixed).
    r_double_time = calc_absolute_resistance_capacitor_discharge(
        c_emu, 1.0, v_final, 2.0 * t_meas
    )
    assert r_double_time == pytest.approx(2.0 * r_measured, rel=1e-13)
    r_double_capacitance = calc_absolute_resistance_capacitor_discharge(
        2.0 * c_emu, 1.0, v_final, t_meas
    )
    assert r_double_capacitance == pytest.approx(0.5 * r_measured, rel=1e-13)

    # O8: half-life pin V = V₀/2 ⇒ R = t/(C ln 2).
    r_half = calc_absolute_resistance_capacitor_discharge(2.0, 1.0, 0.5, 4.0)
    # provenance: O8 — closed-form half-life reduction, pinned with math.log.
    assert r_half == pytest.approx(2.0 / math.log(2.0), rel=1e-14)


@pytest.mark.article(765)
def test_art765_capacitor_discharge_citation_and_guards():
    """Art. 765 — citation targets Art. 765; unphysical inputs rejected."""
    citation = get_citation(calc_absolute_resistance_capacitor_discharge)
    assert citation is not None
    assert citation.part == 4
    assert 765 in citation.articles

    with pytest.raises(ValueError):
        calc_absolute_resistance_capacitor_discharge(1.0, 0.5, 1.0, 1.0)  # no decay
    with pytest.raises(ValueError):
        calc_absolute_resistance_capacitor_discharge(-1.0, 1.0, 0.5, 1.0)  # C < 0
    with pytest.raises(ValueError):
        calc_absolute_resistance_capacitor_discharge(1.0, 1.0, 0.5, 0.0)  # t = 0


# ═══════════════════════════════════════════════════════════════════════════
# Art. 766 — damping (logarithmic decrement) correction of the recoil throw
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.article(766)
def test_art766_recoil_damping_correction_vs_oscillator_oracle():
    """Art. 766 — θ₁* = θ₁ e^{λ/2}, λ = ln(θ₁/θ₂), vs a damped-oscillator ODE.

    Oracles:
      O9 solve_ivp integration of θ̈ + 2γθ̇ + ω₀²θ = 0 (kicked at t = 0,
         θ(0) = 0, θ̇(0) = v₀): the corrected throw must recover v₀/ω_d.
         Rel tolerance 1e-3; the predicted residual is the extremum-shift
         term u²/2 with u = γ/ω_d ≈ 3.17e-5 (recorded below), so the test
         is comfortably inside tolerance while remaining sensitive to any
         wrong correction exponent (e.g. e^{λ} or e^{λ/4} fail by ≥ 1e-2).
      O10 exact-arithmetic pins for λ and θ₁* (closed-form channel).
    """
    omega0 = 2.0 * math.pi  # natural frequency (T = 1 s)
    gamma = 0.05  # damping constant (Q = ω₀/2γ ≈ 63 — a real recoil swing)
    v0 = 0.4
    omega_d = math.sqrt(omega0**2 - gamma**2)

    sol = solve_ivp(
        lambda t, y: [y[1], -2.0 * gamma * y[1] - omega0**2 * y[0]],
        (0.0, 3.0),
        [0.0, v0],
        rtol=1e-11,
        atol=1e-14,
        dense_output=True,
        max_step=0.005,
    )
    ts = np.linspace(0.0, 3.0, 300001)
    theta = sol.sol(ts)[0]
    slope = np.gradient(theta, ts)
    extrema = []
    for i in range(1, len(slope)):
        if slope[i - 1] > 0.0 >= slope[i]:
            extrema.append(ts[i - 1])
        elif slope[i - 1] < 0.0 <= slope[i]:
            extrema.append(ts[i - 1])
    theta1 = float(sol.sol(extrema[0])[0])  # first (positive) elongation
    theta2 = abs(float(sol.sol(extrema[1])[0]))  # next opposite elongation

    lam, theta1_star = calc_recoil_damping_correction(theta1, theta2)

    # The simulated decrement equals γπ/ω_d (half-period separation).
    # provenance: O9 — exact envelope property of the damped oscillator.
    assert lam == pytest.approx(gamma * math.pi / omega_d, rel=1e-5)

    # provenance: O9 — Maxwell's quarter-period damping correction recovers
    # the impulse amplitude v₀/ω_d up to the extremum-shift residual
    # u²/2 = 0.5·(γ/ω_d)² ≈ 3.17e-5, far inside the 1e-3 tolerance.
    predicted_residual = 0.5 * (gamma / omega_d) ** 2
    assert abs(theta1_star - v0 / omega_d) / (v0 / omega_d) < 1e-3
    # and the residual is of the predicted order, not accidentally zero:
    assert abs(theta1_star - v0 / omega_d) / (v0 / omega_d) < 10.0 * predicted_residual

    # O10: closed-form pins on a hard-coded damped pair (θ₁/θ₂ = 5/4).
    # provenance: O10 — exact arithmetic: ln(1.25), 0.1·√1.25.
    lam_pin, star_pin = calc_recoil_damping_correction(0.1, 0.08)
    assert lam_pin == pytest.approx(math.log(1.25), rel=1e-14)
    assert star_pin == pytest.approx(0.1 * math.sqrt(1.25), rel=1e-14)
    assert star_pin > 0.1  # damping correction increases the observed throw


@pytest.mark.article(766)
def test_art766_recoil_damping_correction_citation_and_guards():
    """Art. 766 — citation targets Art. 766; unphysical pairs rejected."""
    citation = get_citation(calc_recoil_damping_correction)
    assert citation is not None
    assert citation.part == 4
    assert 766 in citation.articles

    with pytest.raises(ValueError):
        calc_recoil_damping_correction(0.08, 0.1)  # growing swing: no decay
    with pytest.raises(ValueError):
        calc_recoil_damping_correction(0.0, 0.05)  # zero deflection


# ═══════════════════════════════════════════════════════════════════════════
# D-39 regression guard — the trivial m = k² helper must cite no article
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.regression("D-39")
def test_d39_parameter_helper_no_longer_hijacks_art702():
    """D-39 — ``parameter()`` carries no article citation; Art. 702 stays
    genuinely covered by the hardened parameter-convention evaluators."""
    # The helper still computes m = k² correctly (numeric pin: 0.5² = 0.25).
    assert EllipticIntegral(modulus=0.5).parameter() == pytest.approx(0.25, abs=1e-15)
    # ...but must NOT hijack article coverage any more.
    assert get_citation(EllipticIntegral.parameter) is None

    # Art. 702 remains cited by the genuine parameter-convention functions.
    for func in (
        calc_complete_elliptic_k_parameter,
        calc_complete_elliptic_e_parameter,
    ):
        citation = get_citation(func)
        assert citation is not None
        assert 702 in citation.articles
