"""Wave-7 qualifying tests for Treatise Arts. 740, 745, 750 (Ch. XVI).

These three articles were residual gaps after the D-24 adjudication
(2026-08-21) removed fabricated signal-integrity attributions to exactly
these article numbers. This bundle qualifies the genuine implementations
in ``maxwell/signal_processing/observation_methods.py``, recovered from
the 3rd-edition OCR master
(VOLUME_2_PART_4_CHAPTERS/CHAPTER_XVI_ELECTROMAGNETIC_OBSERVATIONS.JSON):

  Art. 740 (p. 407): T = T1(1 + kappa c^2), kappa = 1/64; reduction of
      the observed mean vibration time to infinitely small arcs.
  Art. 745 (p. 411): phi = (theta0 + rho theta1)/(1 + rho), measurement
      by the first swing.
  Art. 750 (pp. 415-417): Weber's method of recoil, eqs. (18)-(30).

INDEPENDENT ORACLES (never copied from the module under test):
  * direct forward summation of T1(1 + kappa c_k^2) over the geometric
    amplitude series (Art. 740);
  * fixed-step RK4 integrations of the linear damped oscillator with
    event detection (turning points / zero crossings), pure python
    (Arts. 745, 750);
  * exact rational arithmetic via fractions.Fraction for the recoil
    identities (Art. 750).

TOLERANCE CLASSES (Stage 4 §2.5): TIGHT 1e-10 identities, STANDARD 1e-8
closed forms, NUMERIC 1e-6 quadrature/ODE; the rational pins use
rel 1e-13 since they compare against exact fractions converted to float.

Provenance per test is stated in its docstring (rubric Stage-3 §6).
"""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from maxwell.signal_processing.observation_methods import (
    KAPPA_MAGNETIC_NEEDLE,
    calc_elongation_ratio,
    calc_first_swing_deflection,
    calc_recoil_charge_product,
    calc_recoil_coefficient,
    calc_recoil_damping,
    calc_recoil_elongations,
    calc_small_arc_vibration_time,
    calc_vibration_time_at_amplitude,
)

from articles import ref_value, tolerance_of

TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6


# ---------------------------------------------------------------------------
# Independent RK4 oracle for the linear damped oscillator
# ---------------------------------------------------------------------------


def _rk4_damped(beta, omega0, theta0, v0, t_end, dt=1e-3, equilibrium=0.0):
    """Integrate th'' + 2*beta*th' + omega0^2*(th - equilibrium) = 0.

    Pure-python fixed-step RK4 (no scipy). Returns (t, theta, v) lists.
    Global error O(dt^4) ~ 1e-12 per unit time at dt = 1e-3, far below
    the NUMERIC tolerance used against it.
    """
    def deriv(t, y):
        th, v = y
        return (v, -2.0 * beta * v - omega0**2 * (th - equilibrium))

    t, y = 0.0, (theta0, v0)
    ts, ths, vs = [t], [y[0]], [y[1]]
    n_steps = int(round(t_end / dt))
    for _ in range(n_steps):
        k1 = deriv(t, y)
        k2 = deriv(t + 0.5 * dt, (y[0] + 0.5 * dt * k1[0], y[1] + 0.5 * dt * k1[1]))
        k3 = deriv(t + 0.5 * dt, (y[0] + 0.5 * dt * k2[0], y[1] + 0.5 * dt * k2[1]))
        k4 = deriv(t + dt, (y[0] + dt * k3[0], y[1] + dt * k3[1]))
        y = (
            y[0] + dt / 6.0 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
            y[1] + dt / 6.0 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]),
        )
        t += dt
        ts.append(t)
        ths.append(y[0])
        vs.append(y[1])
    return ts, ths, vs


# ---------------------------------------------------------------------------
# Art. 740 — time of vibration reduced to infinitely small arcs
# ---------------------------------------------------------------------------


@pytest.mark.article(740)
def test_art_740_vibration_time_amplitude_law() -> None:
    """T(c) = T1(1 + kappa c^2), kappa = 1/64 for the needle (Art. 740).

    Provenance: Treatise Vol. II 3rd ed., p. 407 ("the time of a
    vibration from rest to rest of amplitude c is in general of the form
    T = T1(1 + kappa c^2), where kappa ... for the ordinary pendulum is
    1/64"). Hand arithmetic: T1 = 2, c = 0.2 gives T = 2(1 + 0.04/64).
    The quadratic dependence is pinned by the 4x ratio of the excess at
    doubled amplitude.
    """
    t1, c = 2.0, 0.2
    expected = 2.0 * (1.0 + (1.0 / 64.0) * 0.04)
    assert calc_vibration_time_at_amplitude(t1, c) == pytest.approx(
        expected, rel=TIGHT
    )
    assert KAPPA_MAGNETIC_NEEDLE == pytest.approx(1.0 / 64.0, rel=TIGHT)
    # quadratic scaling of the excess over the small-arc time
    excess_c = calc_vibration_time_at_amplitude(t1, c) - t1
    excess_2c = calc_vibration_time_at_amplitude(t1, 2.0 * c) - t1
    assert excess_2c == pytest.approx(4.0 * excess_c, rel=TIGHT)


@pytest.mark.article(740)
def test_art_740_small_arc_time_golden_and_sum_oracle() -> None:
    """Exact inversion T1 = nT/(n + kappa S) vs a forward-sum oracle.

    Provenance: p. 407 gives nT = T1(n + kappa (c1^2 rho^2 - cn^2)/
    (rho^2 - 1)) and the approximate reduction; the module inverts the
    same relation exactly. Independent oracle: summing the per-swing
    times T1(1 + kappa c_k^2) over the geometric amplitudes
    c_k = c1 rho^-(k-1) must reproduce n*T. Golden stored in
    reference_values.json (case T = 2.0 s, n = 20, c1 = 1, rho = 1.03,
    kappa = 1/64), hand arithmetic.
    """
    t_mean, n, c1, rho, kappa = 2.0, 20, 1.0, 1.03, 1.0 / 64.0
    c_last = c1 * rho ** -(n - 1)

    t1 = calc_small_arc_vibration_time(t_mean, n, c1, c_last, kappa=kappa)
    assert t1 == pytest.approx(
        ref_value(740, "small_arc_time_T1"),
        **tolerance_of(740, "small_arc_time_T1"),
    )

    # independent forward oracle: direct summation of the series
    amplitudes = [c1 * rho ** -k for k in range(n)]
    total = sum(t1 * (1.0 + kappa * c**2) for c in amplitudes)
    assert total == pytest.approx(n * t_mean, rel=1e-12)

    # the elongation ratio helper reconstructs rho from first and last
    assert calc_elongation_ratio(c1, c_last, n) == pytest.approx(rho, rel=TIGHT)


@pytest.mark.article(740)
def test_art_740_limits_zero_kappa_and_undamped() -> None:
    """Analytic limits: kappa -> 0 gives T1 -> T; rho -> 1 collapses S.

    Provenance: with no amplitude correction the observed mean time IS
    the small-arc time; with no damping every swing has amplitude c1, so
    S -> n c1^2 and T1 -> nT/(n + kappa n c1^2). Both are analytic
    limits of the p. 407 relation, checked numerically here.
    """
    t_mean, n, c1 = 2.0, 20, 0.5
    # kappa -> 0: no correction
    t1 = calc_small_arc_vibration_time(
        t_mean, n, c1, c1 * 1.0000001 ** -(n - 1), kappa=1e-12
    )
    assert t1 == pytest.approx(t_mean, rel=1e-9)
    # rho -> 1 (undamped): S -> n c1^2
    rho_near = 1.0 + 1e-9
    c_last = c1 * rho_near ** -(n - 1)
    t1 = calc_small_arc_vibration_time(t_mean, n, c1, c_last)
    expected = n * t_mean / (n + KAPPA_MAGNETIC_NEEDLE * n * c1**2)
    assert t1 == pytest.approx(expected, rel=1e-5)


# ---------------------------------------------------------------------------
# Art. 745 — measurement by the first swing
# ---------------------------------------------------------------------------


@pytest.mark.article(745)
def test_art_745_first_swing_golden() -> None:
    """phi = (theta0 + rho theta1)/(1 + rho) (Art. 745), rational golden.

    Provenance: Treatise Vol. II 3rd ed., p. 411. Golden theta0 = 6,
    theta1 = 5, rho = 6/5: phi = (6 + 6)/(11/5) = 60/11, exact rational
    arithmetic (fractions.Fraction) converted to float.
    """
    phi_frac = (Fraction(6) + Fraction(6, 5) * Fraction(5)) / (
        Fraction(1) + Fraction(6, 5)
    )
    assert phi_frac == Fraction(60, 11)
    phi = calc_first_swing_deflection(6.0, 5.0, 1.2)
    assert phi == pytest.approx(
        ref_value(745, "first_swing_golden"),
        **tolerance_of(745, "first_swing_golden"),
    )
    assert phi == pytest.approx(float(phi_frac), rel=1e-13)


@pytest.mark.article(745)
def test_art_745_damped_oscillator_rk4_oracle() -> None:
    """RK4 oracle: switching a steady current shifts the equilibrium.

    Provenance: independent integration of th'' + 2 beta th' +
    omega0^2 (th - phi) = 0 with the magnet at rest at the zero reading
    theta0 when the current is switched on (equilibrium jumps to phi).
    The turning points of the exact linear solution lie at t_k =
    k pi/omega1 with amplitudes decaying by exp(beta pi/omega1) per
    swing, so the first overshoot satisfies phi - theta0 =
    rho (theta1 - phi), rho = exp(beta pi/omega1) — the formula under
    test, verified here end-to-end numerically.
    """
    beta, omega0 = 0.05, 1.0
    omega1 = math.sqrt(omega0**2 - beta**2)
    phi_true, theta0 = 0.4, 0.05
    t_end = 20.0
    ts, ths, vs = _rk4_damped(
        beta, omega0, theta0, 0.0, t_end, equilibrium=phi_true
    )

    # first turning point: first sign change of the velocity after t = 0
    idx = next(i for i in range(1, len(vs)) if vs[i - 1] > 0.0 >= vs[i])
    # parabolic-vertex refinement of the peak from the three surrounding
    # grid values (equal spacing h): offset = h(y_a - y_c)/
    # (2(y_a + y_c - 2y_b)), value = y_b - (y_c - y_a)^2/
    # (8(y_a + y_c - 2y_b)) -- hand-derived quadratic interpolation.
    h = ts[idx] - ts[idx - 1]
    y_a, y_b, y_c = ths[idx - 1], ths[idx], ths[idx + 1]
    theta_first = y_b - (y_c - y_a) ** 2 / (8.0 * (y_a + y_c - 2.0 * y_b))

    rho_exact = math.exp(beta * math.pi / omega1)
    # (1) the observed decay ratio from the simulation matches the formula
    rho_obs = (phi_true - theta0) / (theta_first - phi_true)
    assert rho_obs == pytest.approx(rho_exact, rel=NUMERIC)
    # (2) Maxwell's correction recovers the true equilibrium phi
    phi_recovered = calc_first_swing_deflection(theta0, theta_first, rho_exact)
    assert phi_recovered == pytest.approx(phi_true, abs=5e-4)


@pytest.mark.article(745)
def test_art_745_undamped_limit_is_midpoint() -> None:
    """Undamped rule: permanent deflexion is half the extreme elongation.

    Provenance: p. 411, "If there is no resistance, the permanent
    deflexion phi is half the extreme elongation" — the rho -> 1 limit
    of the formula, with the zero reading as the other extreme.
    """
    theta0, theta1 = 0.0, 1.4
    assert calc_first_swing_deflection(theta0, theta1, 1.0) == pytest.approx(
        0.5 * (theta0 + theta1), rel=TIGHT
    )
    # with a non-zero zero reading the midpoint form still holds
    assert calc_first_swing_deflection(2.0, 3.0, 1.0) == pytest.approx(2.5, rel=TIGHT)


# ---------------------------------------------------------------------------
# Art. 750 — Weber's method of recoil
# ---------------------------------------------------------------------------


@pytest.mark.article(750)
def test_art_750_elongation_chain_rational_goldens() -> None:
    """Eqs. (19)-(26) with rational data; eqs. (29)-(30) close exactly.

    Provenance: pp. 415-417. Rational case K = 1, Q0 = 1, Q = 7/4,
    exp(-lam) = 5/6 computed independently with fractions.Fraction:
    a = 1, b = -5/6, c = -(7/4 - 25/36) = -19/18, d = 95/108. The
    module must reproduce these, and the two measurement invariants
    (29) (d-b)/(a-c) = e^-lam and (30) KQ = ((a-b)e^-2lam + d-c)/
    (1 + e^-lam) must return 5/6 and 7/4 from a, b, c, d, lam alone.
    """
    r = Fraction(5, 6)
    k_coef, q0, q = Fraction(1), Fraction(1), Fraction(7, 4)
    a_f = k_coef * q0
    b_f = -a_f * r
    c_f = -k_coef * (q - q0 * r**2)
    d_f = -c_f * r
    # exact expectations (hand rational arithmetic, eqs. 19-26)
    assert (a_f, b_f, c_f, d_f) == (
        Fraction(1),
        Fraction(-5, 6),
        Fraction(-19, 18),
        Fraction(95, 108),
    )
    # the invariants hold in exact rational arithmetic before any float:
    # (29) (d-b)/(a-c) = r, (30) KQ = ((a-b)r^2 + d - c)/(1 + r) = 7/4
    assert (d_f - b_f) / (a_f - c_f) == r
    assert ((a_f - b_f) * r**2 + d_f - c_f) / (1 + r) == Fraction(7, 4)

    lam = math.log(6.0 / 5.0)
    out = calc_recoil_elongations(1.0, float(q), float(q0), lam)
    assert out["a"] == pytest.approx(float(a_f), rel=1e-13)
    assert out["b"] == pytest.approx(float(b_f), rel=1e-13)
    assert out["c"] == pytest.approx(float(c_f), rel=1e-13)
    assert out["d"] == pytest.approx(float(d_f), rel=1e-13)

    # invariant (29): damping from the four elongations
    ratio = math.exp(-calc_recoil_damping(out["a"], out["b"], out["c"], out["d"]))
    assert ratio == pytest.approx(
        ref_value(750, "recoil_damping_ratio"),
        **tolerance_of(750, "recoil_damping_ratio"),
    )
    # invariant (30): KQ from the four elongations and lam
    kq = calc_recoil_charge_product(out["a"], out["b"], out["c"], out["d"], lam)
    assert kq == pytest.approx(
        ref_value(750, "recoil_charge_product"),
        **tolerance_of(750, "recoil_charge_product"),
    )


@pytest.mark.article(750)
def test_art_750_recoil_coefficient_forms_and_limits() -> None:
    """Eq. (18) structure: undamped limit and the small-lam expansion.

    Provenance: p. 415 eqs. (14)/(17)/(18). Undamped (lam = 0) K must
    reduce to (G/H) pi/T1 = (G/H) omega1. For small lam the Treatise's
    approximate inversion (17), Q ~ (H/G)(T1/pi)(1 + lam/2) theta1,
    implies K ~ (G/H)(pi/T1)(1 - lam/2) to first order — checked at
    lam = 0.01.
    """
    g, h, t1 = 1.2, 0.3, 2.5
    k0 = calc_recoil_coefficient(g, h, t1, 0.0)
    assert k0 == pytest.approx(g / h * math.pi / t1, rel=TIGHT)

    lam = 0.01
    k_small = calc_recoil_coefficient(g, h, t1, lam)
    assert k_small / k0 == pytest.approx(1.0 - 0.5 * lam, abs=1e-4)

    # continuity at lam -> 0+
    assert calc_recoil_coefficient(g, h, t1, 1e-12) == pytest.approx(k0, rel=1e-9)


@pytest.mark.article(750)
def test_art_750_kicked_oscillator_ode_oracle() -> None:
    """Full recoil sequence from an independent kicked-oscillator RK4.

    Provenance: independent integration of the damped magnet
    th'' + 2 beta th' + omega0^2 th = 0, kicked at rest by Q0
    (velocity jump v0 = (G/H) omega0^2 Q0), then — when it returns
    through the equilibrium point moving negatively — given the second
    velocity change -v, v = (G/H) omega0^2 Q, exactly as described in
    pp. 415-416 (eqs. 20-25). The four simulated turning points a, b,
    c, d must satisfy the module's eq. (29)/(30) reconstructions with
    K from eq. (18).
    """
    g_over_h = 1.0
    omega0, beta = 1.0, 0.08
    omega1 = math.sqrt(omega0**2 - beta**2)
    t1 = math.pi / omega1
    lam = beta * math.pi / omega1
    q0, q = 1.0, 1.75

    k_formula = calc_recoil_coefficient(g_over_h, 1.0, t1, lam)

    # stage A: kick Q0 at rest at zero (eq. 20) and integrate the free
    # motion through a (eq. 19), the first return through zero (eq. 21),
    # b (eq. 22), and the SECOND return through zero (eq. 23), where the
    # protocol applies the current -Q.
    v0 = g_over_h * omega0**2 * q0
    ts, ths, vs = _rk4_damped(beta, omega0, 0.0, v0, 30.0)
    i_a = next(i for i in range(1, len(vs)) if vs[i - 1] > 0.0 >= vs[i])
    a_ode = ths[i_a]
    i_z1 = next(i for i in range(i_a, len(ths)) if ths[i - 1] > 0.0 >= ths[i])
    assert vs[i_z1] < 0.0  # first return, negative direction (eq. 21)
    i_b = next(i for i in range(i_z1, len(vs)) if vs[i - 1] < 0.0 <= vs[i])
    b_ode = ths[i_b]  # second elongation, negative (eq. 22)
    i_z2 = next(i for i in range(i_b, len(ths)) if ths[i - 1] < 0.0 <= ths[i])
    v_at_zero2 = vs[i_z2]
    assert v_at_zero2 > 0.0  # second return, eq. 23 (v2 = v0 e^{-2 lam})
    # eq. 21/23 velocity decay checks
    assert vs[i_z1] == pytest.approx(-v0 * math.exp(-lam), rel=1e-4)
    assert v_at_zero2 == pytest.approx(v0 * math.exp(-2.0 * lam), rel=1e-4)

    # stage B: velocity change -v at the zero point (eqs. 24-25), then
    # integrate to the negative elongation c and on to d (eq. 26).
    v_change = g_over_h * omega0**2 * q
    v_after = v_at_zero2 - v_change
    assert v_after < 0.0  # Q > Q0 e^{-2 lam}, motion reversed (p. 416)
    ts2, ths2, vs2 = _rk4_damped(beta, omega0, 0.0, v_after, 30.0)
    i_c = next(i for i in range(1, len(vs2)) if vs2[i - 1] < 0.0 <= vs2[i])
    c_ode = ths2[i_c]  # negative elongation (eq. 25)
    i_d_zero = next(i for i in range(i_c, len(ths2)) if ths2[i - 1] < 0.0 <= ths2[i])
    ts3, ths3, vs3 = _rk4_damped(beta, omega0, 0.0, vs2[i_d_zero], 30.0)
    i_d = next(i for i in range(1, len(vs3)) if vs3[i - 1] > 0.0 >= vs3[i])
    d_ode = ths3[i_d]

    # eq. (18): first elongation a = K Q0
    assert a_ode == pytest.approx(k_formula * q0, rel=1e-5)
    # eq. (29): damping invariant from the simulated elongations
    ratio = (d_ode - b_ode) / (a_ode - c_ode)
    assert ratio == pytest.approx(math.exp(-lam), rel=1e-4)
    # eq. (30): KQ reconstruction closes to K_formula * Q
    kq = calc_recoil_charge_product(a_ode, b_ode, c_ode, d_ode, lam)
    assert kq == pytest.approx(k_formula * q, rel=1e-3)
