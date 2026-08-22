"""Per-article evidence for Treatise Arts. 730-750 (Part IV, Ch XVI: Observations).

SCOPE (INSTRUMENTUM, Wave 6, 2026-08-21): qualifies the genuine
post-D-24/D-17 implementations of Ch XVI articles 730-750 in

* ``maxwell.signal_processing.telegraphy``            -> Arts. 730-735
* ``maxwell.electromagnetism.measurements.galvanometers_extended``
                                                      -> Arts. 736-739,
                                                         741-744, 746-749

RESIDUAL WAVE-7 GAPS — CLOSED 2026-08-22: Arts. 740, 745, 750 formerly
had no genuine implementation (their old attributions — the 2.2 RC
rise-time rule, the 0.35/t_r bandwidth product, the 1/(2 t_r) signaling
thumb rule — were 20th-century heuristics falsely ascribed to those
articles; defect D-24 reclassified them ``standard_math`` with no
article numbers, see ``docs/reports/D24_ADJUDICATION_2026-08-21.md``).
Wave 7 (INSTRUMENTUM) recovered the genuine Treatise content of
740/745/750 from the 3rd-edition OCR and implemented it in
``maxwell.signal_processing.observation_methods``; the qualifying tests
live in ``tests/test_articles_ch16_wave7_740_745_750.py`` (deliberately
NOT marked here, to keep this bundle scoped to 730-749 implementations
of Wave 6).

INDEPENDENT ORACLES (never copied from the modules under test):
  * ``_biot_savart_axis_stat`` — direct vector quadrature of the
    explicit-c Gaussian Biot-Savart law ``dB = (I/c) dl x r / |r|^3``
    around filamentary loops (I in statamperes, B in gauss).  A genuine
    numerical integration, not the closed forms the modules implement.
  * ``_csqrt_polar`` — hand-rolled polar-form complex square root for the
    propagation constant gamma = sqrt((R+iwL)(G+iwC)); an algorithmic
    path independent of numpy's branch implementation.
  * ``_time_avg_power`` — composite-Simpson time average of v(t)*i(t)
    over one period for the wattmeter.
  * Hand-derived analytic limits: lossless line beta = w sqrt(LC);
    low-loss attenuation alpha ~ (R/2) sqrt(C/L) with error bound
    O((R/wL)^2); dipole-limit torque of a small coil at the centre of a
    large coil; Helmholtz flatness d^2B/dz^2 = 0 at the midpoint.
  * ``_bisect`` — independent bisection of the dynamometer torque
    balance.

UNIT CONVENTION: ``galvanometers_extended`` is explicit-c Gaussian
(D-16 class): coil currents read as statamperes, fields gauss, with
``CONST.C`` carried explicitly.  The quadrature oracle uses the SAME
convention so the numeric pin is convention-exact.  Telegraph-line math
is convention-free (R, L, C, G per unit length).

TOLERANCE CLASSES (Stage 4 §2.5): TIGHT 1e-10, STANDARD 1e-8,
NUMERIC 1e-6; coarser tolerances carry an explicit provenance (e.g.
finite-size dipole corrections).
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from maxwell.config.constants import CONST
from maxwell.electromagnetism.measurements.galvanometers_extended import (
    Electrodynamometer,
    HelmholtzGalvanometer,
    SineGalvanometer,
    TangentGalvanometer,
    electrodynamometer,
    wattmeter,
)
from maxwell.signal_processing.telegraphy import (
    TelegraphLine,
    calc_propagation_constant,
    calc_signal_delay,
    calc_signal_velocity,
)

TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6


# ---------------------------------------------------------------------------
# Independent oracles
# ---------------------------------------------------------------------------


def _biot_savart_axis_stat(
    current_stat: float,
    radius: float,
    z_eval: float,
    z_plane: float = 0.0,
    n_turns: int = 1,
    npts: int = 4000,
) -> float:
    """On-axis B (gauss) of one circular loop by direct quadrature.

    Provenance: explicit-c Gaussian Biot-Savart law
    ``dB = (I/c) dl x r / |r|^3`` integrated around a filamentary loop
    of the given radius lying in the plane z = z_plane, evaluated at the
    on-axis point (0, 0, z_eval).  Current is in statamperes.  The
    trapezoid rule on this smooth periodic integrand converges
    exponentially; 4000 points give << 1e-12 relative error here.
    Independent of every closed form in the modules under test.
    """
    a = radius
    phi = np.linspace(0.0, 2.0 * np.pi, npts, endpoint=False)
    dphi = 2.0 * np.pi / npts
    cos_p = np.cos(phi)
    sin_p = np.sin(phi)
    # displacement source -> field point
    rx = -a * cos_p
    ry = -a * sin_p
    rz = z_eval - z_plane
    r3 = (rx * rx + ry * ry + rz * rz) ** 1.5
    # dl = a dphi (-sin phi, cos phi, 0); (dl x r)_z = a^2 dphi
    cz = a * a * dphi * np.ones_like(phi)
    bz = (current_stat / CONST.C) * np.sum(cz / r3)
    return n_turns * bz


def _csqrt_polar(z: complex) -> complex:
    """Complex square root via polar form (hand-derived identity).

    Provenance: for z = r e^{i phi} with phi = atan2(Im z, Re z),
    sqrt(z) = sqrt(r) e^{i phi/2}.  Independent algorithmic path from
    numpy's csqrt; catches branch/sign errors in gamma computations.
    """
    r = abs(z)
    phi = math.atan2(z.imag, z.real)
    return math.sqrt(r) * complex(math.cos(phi / 2.0), math.sin(phi / 2.0))


def _gamma_oracle(R: float, L: float, C: float, G: float, omega: float) -> complex:
    """Propagation constant gamma by the polar-form complex square root."""
    return _csqrt_polar(complex(R, omega * L) * complex(G, omega * C))


def _time_avg_power(v_peak: float, i_peak: float, phase_rad: float, npts: int = 4097) -> float:
    """One-period time average of v(t) i(t) by composite Simpson.

    Provenance: v = Vp cos(wt), i = Ip cos(wt - phi);
    <v i> = (Vp Ip / 2) cos phi = Vrms Irms cos phi.  The quadrature is
    the oracle; the identity is what the module must reproduce.
    """
    t = np.linspace(0.0, 2.0 * np.pi, npts)
    vi = v_peak * np.cos(t) * i_peak * np.cos(t - phase_rad)
    # composite Simpson (npts odd -> even number of panels)
    h = 2.0 * np.pi / (npts - 1)
    y = vi
    return (h / 3.0) * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-2:2].sum()) / (
        2.0 * np.pi
    )


def _bisect(f, lo: float, hi: float, iterations: int = 120) -> float:
    """Independent bisection root of f on [lo, hi] (f(lo) < 0 < f(hi))."""
    flo = f(lo)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (flo < 0) == (fm < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Telegraph line relations — Arts. 730-735 (telegraphy.TelegraphLine)
# ---------------------------------------------------------------------------

_LINE = dict(R=0.01, L=10.0, C=1e-10, G=1e-12)
_OMEGA = 2.0 * math.pi * 1e6


@pytest.mark.article(730)
def test_art_730_signal_velocity():
    """Art. 730 — signal velocity v = 1/sqrt(LC).

    Provenance/oracle: on a lossless line the phase constant is
    beta = w sqrt(LC) (hand-derived from the wave equation), so the
    phase velocity w/beta equals 1/sqrt(LC); checked at three (L, C)
    pairs.  Plus the hand-derived scaling law v(L, C/4) = 2 v(L, C).
    Tolerance: TIGHT (pure identities).
    """
    for L, C in ((10.0, 1e-10), (2.5, 4e-11), (40.0, 2.5e-11)):
        line = TelegraphLine(R=0.0, L=L, C=C, G=0.0)
        beta_oracle = _OMEGA * math.sqrt(L * C)  # hand-derived lossless beta
        v_oracle = _OMEGA / beta_oracle
        v = line.signal_velocity()
        assert math.isclose(v, v_oracle, rel_tol=TIGHT), (
            f"Art. 730: v={v} vs oracle {v_oracle}"
        )
    v1 = TelegraphLine(R=0.0, L=10.0, C=1e-10, G=0.0).signal_velocity()
    v2 = TelegraphLine(R=0.0, L=10.0, C=0.25e-10, G=0.0).signal_velocity()
    assert math.isclose(v2 / v1, 2.0, rel_tol=TIGHT), "Art. 730: scaling v ~ 1/sqrt(C)"
    # module-level function agrees
    assert math.isclose(calc_signal_velocity(10.0, 1e-10), v1, rel_tol=TIGHT)


@pytest.mark.article(731)
def test_art_731_characteristic_impedance():
    """Art. 731 — characteristic impedance Z0 = sqrt(L/C).

    Provenance/oracle: hand-derived identity Z0 = v * L with
    v = 1/sqrt(LC) (independent route to the same quantity), plus the
    scaling law Z0(4L, C) = 2 Z0(L, C).  Tolerance: TIGHT.
    """
    L, C = 10.0, 1e-10
    line = TelegraphLine(R=0.0, L=L, C=C, G=0.0)
    z0_oracle = (1.0 / math.sqrt(L * C)) * L  # v * L, hand-derived
    assert math.isclose(line.characteristic_impedance(), z0_oracle, rel_tol=TIGHT)
    z0_a = TelegraphLine(R=0.0, L=L, C=C, G=0.0).characteristic_impedance()
    z0_b = TelegraphLine(R=0.0, L=4.0 * L, C=C, G=0.0).characteristic_impedance()
    assert math.isclose(z0_b / z0_a, 2.0, rel_tol=TIGHT), "Art. 731: Z0 ~ sqrt(L)"


@pytest.mark.article(732)
def test_art_732_attenuation_constant():
    """Art. 732 — attenuation constant alpha = Re sqrt((R+iwL)(G+iwC)).

    Provenance/oracle: (a) polar-form complex square root
    (``_gamma_oracle``), an independent algorithmic path; (b) the
    hand-derived low-loss asymptotic alpha ~ (R/2) sqrt(C/L) +
    (G/2) sqrt(L/C) with next-order correction O((R/wL)^2) ~ 2.5e-9
    for these parameters, asserted at the 1e-6 bound.

    Tolerance note: alpha/beta ~ 8.8e-10 here, so Re(gamma) is limited
    by cancellation to ~eps*|gamma|/alpha ~ 1.3e-7 relative in ANY
    algorithm; the independent-oracle assert therefore uses 1e-6.
    """
    line = TelegraphLine(**_LINE)
    gamma_o = _gamma_oracle(_LINE["R"], _LINE["L"], _LINE["C"], _LINE["G"], _OMEGA)
    alpha = line.attenuation_constant(_OMEGA)
    assert math.isclose(alpha, gamma_o.real, rel_tol=NUMERIC), (
        f"Art. 732: alpha={alpha} vs polar-csqrt oracle {gamma_o.real}"
    )
    # module-level propagation constant agrees with the same oracle
    gamma_mod = calc_propagation_constant(
        _LINE["R"], _LINE["L"], _LINE["C"], _LINE["G"], _OMEGA
    )
    assert abs(gamma_mod - gamma_o) < TIGHT * abs(gamma_o)
    # low-loss asymptotic (hand-derived), R/(wL) = 1.59e-4 -> bound 1e-6
    alpha_asym = (_LINE["R"] / 2.0) * math.sqrt(_LINE["C"] / _LINE["L"]) + (
        _LINE["G"] / 2.0
    ) * math.sqrt(_LINE["L"] / _LINE["C"])
    assert math.isclose(alpha, alpha_asym, rel_tol=NUMERIC), (
        f"Art. 732: alpha={alpha} vs low-loss asymptotic {alpha_asym}"
    )


@pytest.mark.article(733)
def test_art_733_phase_constant():
    """Art. 733 — phase constant beta = Im sqrt((R+iwL)(G+iwC)).

    Provenance/oracle: polar-form csqrt oracle for the lossy line; and
    the exact hand-derived lossless limit beta = w sqrt(LC) with
    R = G = 0.  Tolerance: TIGHT / STANDARD.
    """
    line = TelegraphLine(**_LINE)
    gamma_o = _gamma_oracle(_LINE["R"], _LINE["L"], _LINE["C"], _LINE["G"], _OMEGA)
    assert math.isclose(line.phase_constant(_OMEGA), gamma_o.imag, rel_tol=TIGHT)
    lossless = TelegraphLine(R=0.0, L=_LINE["L"], C=_LINE["C"], G=0.0)
    beta_oracle = _OMEGA * math.sqrt(_LINE["L"] * _LINE["C"])
    assert math.isclose(lossless.phase_constant(_OMEGA), beta_oracle, rel_tol=STANDARD)


@pytest.mark.article(734)
def test_art_734_signal_delay():
    """Art. 734 — delay per unit length tau = sqrt(LC) = 1/v.

    Provenance/oracle: hand-derived identity tau = 1/v checked against
    the Art. 730 velocity (both methods), and direct evaluation of
    length * sqrt(LC) for the module-level delay function.  TIGHT.
    """
    L, C = 10.0, 1e-10
    line = TelegraphLine(R=0.0, L=L, C=C, G=0.0)
    tau_oracle = 1.0 / line.signal_velocity()
    assert math.isclose(line.delay_per_length(), tau_oracle, rel_tol=TIGHT)
    length = 3.0e5  # 3 km
    delay = calc_signal_delay(L, C, length)
    assert math.isclose(delay, length * math.sqrt(L * C), rel_tol=TIGHT)
    # consistency: delay * velocity = length (hand-derived identity)
    assert math.isclose(delay * line.signal_velocity(), length, rel_tol=TIGHT)


@pytest.mark.article(735)
def test_art_735_voltage_at_distance():
    """Art. 735 — forward wave V(x) = V0 exp(-gamma x).

    Provenance/oracle: with gamma from the polar-csqrt oracle, the
    hand-derived magnitude/phase decomposition |V(x)| = V0 e^{-alpha x},
    arg V(x) = -beta x.  Tolerance: TIGHT.
    """
    line = TelegraphLine(**_LINE)
    gamma_o = _gamma_oracle(_LINE["R"], _LINE["L"], _LINE["C"], _LINE["G"], _OMEGA)
    V0, x = 5.0, 0.01  # abvolts, cm
    V = line.voltage_at_distance(V0, x, _OMEGA)
    assert math.isclose(abs(V), V0 * math.exp(-gamma_o.real * x), rel_tol=TIGHT)
    assert math.isclose(np.angle(V), -gamma_o.imag * x, rel_tol=TIGHT)
    assert math.isclose(abs(line.voltage_at_distance(V0, 0.0, _OMEGA)), V0, rel_tol=TIGHT)


# ---------------------------------------------------------------------------
# Tangent galvanometer — Arts. 736-738
# ---------------------------------------------------------------------------

_TG = dict(coil_radius=15.0, num_turns=10, earth_field=0.25)


def _tg_target_current(ratio_bh: float) -> float:
    """Hand-derived current (statamperes) giving B_coil/H = ratio_bh.

    Provenance: B_coil = (2 pi n I)/(c r) = ratio * H
    =>  I = ratio * H * c * r / (2 pi n).
    """
    return (
        ratio_bh * _TG["earth_field"] * CONST.C * _TG["coil_radius"]
        / (2.0 * math.pi * _TG["num_turns"])
    )


@pytest.mark.article(736)
def test_art_736_tangent_current_from_deflection():
    """Art. 736 — I = K tan(theta), K = c r H/(2 pi n).

    Provenance/oracle: the coil field for a chosen current is computed
    by independent Biot-Savart quadrature; needle equilibrium (hand
    derived) gives tan(theta) = B_quadrature/H; the instrument must
    recover the input current from that deflection.  NUMERIC tolerance
    for the quadrature (actually << 1e-12 here).
    """
    I0 = _tg_target_current(0.5)  # B/H = 0.5
    bq = _biot_savart_axis_stat(I0, _TG["coil_radius"], 0.0, n_turns=_TG["num_turns"])
    theta_deg = math.degrees(math.atan2(bq, _TG["earth_field"]))
    tg = TangentGalvanometer(**_TG)
    assert math.isclose(tg.current_from_deflection(theta_deg), I0, rel_tol=NUMERIC), (
        f"Art. 736: recovered {tg.current_from_deflection(theta_deg)} vs oracle {I0}"
    )
    # galvanometer constant: I(45 deg) = K = c r H/(2 pi n) (hand-derived)
    k_oracle = (
        CONST.C * _TG["coil_radius"] * _TG["earth_field"] / (2.0 * math.pi * _TG["num_turns"])
    )
    assert math.isclose(tg.current_from_deflection(45.0), k_oracle, rel_tol=TIGHT)


@pytest.mark.article(737)
def test_art_737_tangent_deflection_from_current():
    """Art. 737 — inverse reading theta = arctan(I/K).

    Provenance/oracle: same quadrature-derived equilibrium as Art. 736;
    deflection_from_current(I0) must return the quadrature equilibrium
    angle.  Also round-trip consistency I -> theta -> I.  NUMERIC.
    """
    I0 = _tg_target_current(0.5)
    bq = _biot_savart_axis_stat(I0, _TG["coil_radius"], 0.0, n_turns=_TG["num_turns"])
    theta_oracle = math.degrees(math.atan2(bq, _TG["earth_field"]))
    tg = TangentGalvanometer(**_TG)
    assert math.isclose(tg.deflection_from_current(I0), theta_oracle, rel_tol=NUMERIC)
    assert math.isclose(
        tg.current_from_deflection(tg.deflection_from_current(I0)), I0, rel_tol=STANDARD
    )


@pytest.mark.article(738)
def test_art_738_coil_field_at_center():
    """Art. 738 — coil centre field B = (2 pi n I)/(c r).

    Provenance/oracle: independent Biot-Savart quadrature at two
    geometries; the closed form must match the quadrature.  NUMERIC
    (quadrature error << 1e-12).
    """
    I0 = 0.5  # statamperes
    for radius, turns in ((15.0, 10), (7.5, 3)):
        bq = _biot_savart_axis_stat(I0, radius, 0.0, n_turns=turns)
        tg = TangentGalvanometer(coil_radius=radius, num_turns=turns)
        assert math.isclose(tg.coil_field_at_center(I0), bq, rel_tol=NUMERIC), (
            f"Art. 738: r={radius}, n={turns}: {tg.coil_field_at_center(I0)} vs {bq}"
        )


# ---------------------------------------------------------------------------
# Sine galvanometer — Art. 739
# ---------------------------------------------------------------------------


@pytest.mark.article(739)
def test_art_739_sine_galvanometer():
    """Art. 739 — I = K sin(theta); coil rotated to follow the needle.

    Provenance/oracle: quadrature coil field with B/H = 0.5 gives the
    hand-derived equilibrium sin(theta) = B/H, i.e. theta = 30 deg; the
    instrument must recover I0 from 30 deg.  Range limit of the sine
    law: I = K deflects exactly 90 deg.  NUMERIC / TIGHT.
    """
    sg_params = dict(coil_radius=12.0, num_turns=8, earth_field=0.2)
    ratio = 0.5
    I0 = ratio * sg_params["earth_field"] * CONST.C * sg_params["coil_radius"] / (
        2.0 * math.pi * sg_params["num_turns"]
    )
    bq = _biot_savart_axis_stat(I0, sg_params["coil_radius"], 0.0, n_turns=sg_params["num_turns"])
    theta_oracle = math.degrees(math.asin(bq / sg_params["earth_field"]))
    sg = SineGalvanometer(**sg_params)
    assert math.isclose(theta_oracle, 30.0, abs_tol=1e-9)  # quadrature sanity
    assert math.isclose(sg.current_from_deflection(theta_oracle), I0, rel_tol=NUMERIC)
    # range limit: sin(theta) = 1 at I = K (hand-derived)
    k = sg.galvanometer_constant
    assert math.isclose(sg.deflection_from_current(k), 90.0, abs_tol=1e-9)
    # round trip at a second operating point
    assert math.isclose(
        sg.current_from_deflection(sg.deflection_from_current(0.6 * k)),
        0.6 * k,
        rel_tol=STANDARD,
    )


# ---------------------------------------------------------------------------
# Helmholtz galvanometer — Arts. 741-743
# ---------------------------------------------------------------------------

_HZ = dict(coil_radius=10.0, num_turns_per_coil=50)


@pytest.mark.article(741)
def test_art_741_helmholtz_field_and_uniformity():
    """Art. 741 — Helmholtz pair: midpoint field and its flatness.

    Provenance/oracle: (a) midpoint field by two independent loop
    quadratures (coils at z = +/- r/2); (b) the Helmholtz condition
    d^2B/dz^2 = 0 at the midpoint (hand-derived: the on-axis curvature
    of one loop vanishes at axial offset r/2), asserted as a normalized
    second difference |D_pair| < 5e-4 at delta = r/10, against the
    single-loop curvature D_single ~ -3 (delta/r)^2 ~ -3e-2 which must
    be at least 30x larger.  Pre-checked exact values: D_pair = -2.28e-4,
    D_single = -2.963e-2.  NUMERIC.
    """
    r = _HZ["coil_radius"]
    n = _HZ["num_turns_per_coil"]
    I0 = 0.5  # statamperes
    b_oracle = _biot_savart_axis_stat(I0, r, 0.0, z_plane=+r / 2.0, n_turns=n) + (
        _biot_savart_axis_stat(I0, r, 0.0, z_plane=-r / 2.0, n_turns=n)
    )
    hz = HelmholtzGalvanometer(**_HZ)
    assert math.isclose(hz.field_at_center(I0), b_oracle, rel_tol=NUMERIC), (
        f"Art. 741: {hz.field_at_center(I0)} vs quadrature {b_oracle} "
        "(regression guard for the repaired 32pi/(5 sqrt5) prefactor)"
    )
    # uniformity: normalized second differences at delta = r/10
    delta = r / 10.0

    def b_pair(z):
        return _biot_savart_axis_stat(I0, r, z, z_plane=+r / 2.0, n_turns=n) + (
            _biot_savart_axis_stat(I0, r, z, z_plane=-r / 2.0, n_turns=n)
        )

    def b_single(z):
        return _biot_savart_axis_stat(I0, r, z, z_plane=0.0, n_turns=n)

    b0p, b0s = b_pair(0.0), b_single(0.0)
    d_pair = (b_pair(delta) - 2.0 * b0p + b_pair(-delta)) / b0p
    d_single = (b_single(delta) - 2.0 * b0s + b_single(-delta)) / b0s
    assert abs(d_pair) < 5e-4, f"Art. 741: pair not flat, D={d_pair}"
    assert -3.1e-2 < d_single < -2.8e-2, f"Art. 741: single curvature {d_single}"
    assert abs(d_pair) < abs(d_single) / 30.0


@pytest.mark.article(742)
def test_art_742_helmholtz_factor():
    """Art. 742 — Helmholtz factor 16/(5 sqrt(5)) ~ 1.4311.

    Provenance/oracle: ratio of quadratures (pair midpoint field /
    single-coil own-centre field).  The special case (separation = r)
    must equal the closed form 16/(5 sqrt(5)) — hand-derived from
    2 (4/5)^{3/2} — and the general-separation branch is pinned at
    d = 2r where the oracle ratio is 2/2^{3/2} = 1/sqrt(2).  NUMERIC.
    """
    r = _HZ["coil_radius"]
    n = _HZ["num_turns_per_coil"]
    I0 = 0.5
    b_pair = _biot_savart_axis_stat(I0, r, 0.0, z_plane=+r / 2.0, n_turns=n) + (
        _biot_savart_axis_stat(I0, r, 0.0, z_plane=-r / 2.0, n_turns=n)
    )
    b_single = _biot_savart_axis_stat(I0, r, 0.0, z_plane=0.0, n_turns=n)
    ratio_oracle = b_pair / b_single
    hz = HelmholtzGalvanometer(**_HZ)
    assert math.isclose(hz.helmholtz_factor, ratio_oracle, rel_tol=NUMERIC)
    assert math.isclose(hz.helmholtz_factor, 16.0 / (5.0 * math.sqrt(5.0)), rel_tol=TIGHT)
    # general branch at d = 2r: each coil seen from distance r
    b_2r = 2.0 * _biot_savart_axis_stat(I0, r, 0.0, z_plane=r, n_turns=n)
    hz2 = HelmholtzGalvanometer(coil_radius=r, num_turns_per_coil=n, coil_separation=2.0 * r)
    assert math.isclose(hz2.helmholtz_factor, b_2r / b_single, rel_tol=NUMERIC)
    assert math.isclose(hz2.helmholtz_factor, 1.0 / math.sqrt(2.0), rel_tol=TIGHT)


@pytest.mark.article(743)
def test_art_743_helmholtz_current_from_deflection():
    """Art. 743 — tangent reading with the Helmholtz constant.

    Provenance/oracle: the equilibrium current is I = B H^{-1}-driven:
    for the quadrature midpoint field B_q, tan(theta) = B_q/H and the
    instrument must recover the current that produced B_q.  NUMERIC.
    """
    r = _HZ["coil_radius"]
    n = _HZ["num_turns_per_coil"]
    H = 0.25
    I0 = 0.5
    bq = _biot_savart_axis_stat(I0, r, 0.0, z_plane=+r / 2.0, n_turns=n) + (
        _biot_savart_axis_stat(I0, r, 0.0, z_plane=-r / 2.0, n_turns=n)
    )
    theta_deg = math.degrees(math.atan2(bq, H))
    hz = HelmholtzGalvanometer(coil_radius=r, num_turns_per_coil=n, earth_field=H)
    assert math.isclose(hz.current_from_deflection(theta_deg), I0, rel_tol=NUMERIC)
    # K_helm = K_single / factor (hand-derived from the field ratio)
    k_single = CONST.C * r * H / (2.0 * math.pi * n)
    assert math.isclose(
        hz.galvanometer_constant,
        k_single / (16.0 / (5.0 * math.sqrt(5.0))),
        rel_tol=TIGHT,
    )


# ---------------------------------------------------------------------------
# Wattmeter — Arts. 744, 746
# ---------------------------------------------------------------------------


@pytest.mark.article(744)
def test_art_744_wattmeter_true_power():
    """Art. 744 — electrodynamometer wattmeter reads true power.

    Provenance/oracle: composite-Simpson time average of v(t) i(t) over
    one period, v = Vp cos(wt), i = Ip cos(wt - phi), with
    Vrms = 100, Irms = 5, phi = 60 deg (hand-derived P = 250).  NUMERIC.
    """
    vrms, irms, phi = 100.0, 5.0, math.pi / 3.0
    p_oracle = _time_avg_power(math.sqrt(2.0) * vrms, math.sqrt(2.0) * irms, phi)
    assert math.isclose(p_oracle, 250.0, rel_tol=NUMERIC)  # quadrature sanity
    res = wattmeter(voltage=vrms, current=irms, power_factor=math.cos(phi))
    assert math.isclose(res["power"], p_oracle, rel_tol=NUMERIC), (
        f"Art. 744: power {res['power']} vs quadrature {p_oracle}"
    )
    assert math.isclose(res["apparent_power"], vrms * irms, rel_tol=TIGHT)
    # pf = 1 limit: all power real
    res1 = wattmeter(voltage=vrms, current=irms, power_factor=1.0)
    assert math.isclose(res1["power"], vrms * irms, rel_tol=TIGHT)
    assert res1["reactive_power"] < 1e-12


@pytest.mark.article(746)
def test_art_746_wattmeter_reactive_and_phase():
    """Art. 746 — reactive power and phase angle.

    Provenance/oracle: the hand-derived 3-4-5 power triangle at
    pf = 0.6 (S = 500, P = 300, Q = 400), and the special-angle facts
    cos(60 deg) = 1/2, cos(30 deg) = sqrt(3)/2 for the phase readout.
    TIGHT.
    """
    res = wattmeter(voltage=100.0, current=5.0, power_factor=0.6)
    assert math.isclose(res["power"], 300.0, rel_tol=TIGHT)
    assert math.isclose(res["apparent_power"], 500.0, rel_tol=TIGHT)
    assert math.isclose(res["reactive_power"], 400.0, rel_tol=TIGHT)  # 3-4-5
    # deflection follows power through the wattmeter constant (hand arithmetic)
    res_k = wattmeter(voltage=100.0, current=5.0, power_factor=0.6, wattmeter_constant=2.5)
    assert math.isclose(res_k["deflection"], 120.0, rel_tol=TIGHT)
    # special angles: pf = 0.5 -> 60 deg ; pf = sqrt(3)/2 -> 30 deg
    for pf, deg in ((0.5, 60.0), (math.sqrt(3.0) / 2.0, 30.0)):
        assert math.isclose(
            math.cos(math.radians(wattmeter(1.0, 1.0, power_factor=pf)["phase_angle"])),
            pf,
            abs_tol=1e-12,
        )
        assert math.isclose(
            wattmeter(1.0, 1.0, power_factor=pf)["phase_angle"], deg, abs_tol=1e-9
        )


# ---------------------------------------------------------------------------
# Electrodynamometer — Arts. 747-749
# ---------------------------------------------------------------------------


def _dipole_gradient(a: float, b: float, n1: int, n2: int) -> float:
    """Hand-derived dipole-limit torque coefficient (explicit-c Gaussian).

    Provenance: a small coil (radius b, n2 turns) at the centre of a
    large coil (radius a, n1 turns), axes at angle theta.  The large
    coil's centre field is B1 = 2 pi n1 I1/(c a); the small coil's
    moment is m2 = pi b^2 n2 I2/c; the torque T = m2 x B1 has magnitude
    T = [2 pi^2 n1 n2 b^2/(c^2 a)] I1 I2 sin(theta).  Finite-size
    corrections are O((b/a)^2): from the flux expansion the relative
    correction to dM/dtheta is <= ~1.1 (b/a)^2 (worst case at small
    theta), i.e. <= 4.4e-4 for b/a = 0.02.
    """
    return 2.0 * math.pi**2 * n1 * n2 * b * b / (CONST.C * CONST.C * a)


@pytest.mark.article(747)
def test_art_747_electrodynamometer_torque():
    """Art. 747 — torque T = I1 I2 (dM/dtheta), dipole-limit oracle.

    Provenance/oracle: the hand-derived dipole-limit torque of a small
    coil inside a large coil (``_dipole_gradient``), checked at four
    angles with b/a = 0.02 so the finite-size correction (<= 4.4e-4)
    sits well inside the 1e-3 tolerance.
    """
    a, b, n1, n2 = 10.0, 0.2, 100, 50
    g_oracle = _dipole_gradient(a, b, n1, n2)
    ed = Electrodynamometer(mutual_inductance_gradient=g_oracle, spring_constant=1.0)
    I1, I2 = 0.3, 0.7
    for theta in (math.pi / 6.0, math.pi / 4.0, math.pi / 3.0, math.pi / 2.0):
        t_oracle = I1 * I2 * g_oracle * math.sin(theta)
        assert math.isclose(ed.torque(I1, I2, theta), t_oracle, rel_tol=1e-3), (
            f"Art. 747: theta={theta}: {ed.torque(I1, I2, theta)} vs {t_oracle}"
        )
    # module-level analysis reports the same max torque (theta = 90 deg)
    res = electrodynamometer(I1, I2, mutual_inductance_gradient=g_oracle, spring_constant=1.0)
    assert math.isclose(res["max_torque"], I1 * I2 * g_oracle, rel_tol=1e-3)


@pytest.mark.article(748)
def test_art_748_equilibrium_deflection():
    """Art. 748 — equilibrium theta = I1 I2 (dM/dtheta)/k.

    Provenance/oracle: constant-gradient model (M linear in theta over
    the working range, the wattmeter arrangement); the balance
    k theta = I1 I2 g is re-solved by independent bisection of
    f(theta) = k theta - I1 I2 g.  TIGHT against the bisection root.
    """
    g, k = 1e-6, 1.0
    I1, I2 = 2.0, 1.5
    ed = Electrodynamometer(mutual_inductance_gradient=g, spring_constant=k)
    theta_oracle = _bisect(lambda th: k * th - I1 * I2 * g, 0.0, 1.0)
    assert math.isclose(theta_oracle, I1 * I2 * g / k, rel_tol=1e-9)  # bisection sanity
    assert math.isclose(ed.equilibrium_deflection(I1, I2), theta_oracle, rel_tol=TIGHT)
    res = electrodynamometer(I1, I2, mutual_inductance_gradient=g, spring_constant=k)
    assert math.isclose(res["equilibrium_deflection_rad"], theta_oracle, rel_tol=TIGHT)
    # restoring-constant scaling: theta(k=2) = theta(k=1)/2 (hand-derived)
    ed2 = Electrodynamometer(mutual_inductance_gradient=g, spring_constant=2.0 * k)
    assert math.isclose(
        ed2.equilibrium_deflection(I1, I2), ed.equilibrium_deflection(I1, I2) / 2.0,
        rel_tol=TIGHT,
    )


@pytest.mark.article(749)
def test_art_749_series_square_law_and_product_invariance():
    """Art. 749 — series (Weber) mode: theta ~ I^2; theta ~ I1*I2.

    Provenance/oracle: independent bisection of the torque balance at
    two current pairs with equal product (2.0, 1.5) and (3.0, 1.0) —
    the deflections must coincide — and at I and 2I in series mode,
    where the deflection ratio must be exactly 4 (hand-derived square
    law).  TIGHT.
    """
    g, k = 1e-6, 1.0
    ed = Electrodynamometer(mutual_inductance_gradient=g, spring_constant=k)
    # product invariance: both pairs have I1*I2 = 3.0
    th_a = _bisect(lambda th: k * th - 2.0 * 1.5 * g, 0.0, 1.0)
    th_b = _bisect(lambda th: k * th - 3.0 * 1.0 * g, 0.0, 1.0)
    assert math.isclose(ed.equilibrium_deflection(2.0, 1.5), th_a, rel_tol=TIGHT)
    assert math.isclose(ed.equilibrium_deflection(3.0, 1.0), th_b, rel_tol=TIGHT)
    assert math.isclose(th_a, th_b, rel_tol=TIGHT)
    # series-mode square law: theta(2I, 2I) / theta(I, I) = 4
    I = 1.0
    th1 = ed.equilibrium_deflection(I, I)
    th2 = ed.equilibrium_deflection(2.0 * I, 2.0 * I)
    th2_oracle = _bisect(lambda th: k * th - (2.0 * I) * (2.0 * I) * g, 0.0, 1.0)
    assert math.isclose(th2, th2_oracle, rel_tol=TIGHT)
    assert math.isclose(th2 / th1, 4.0, rel_tol=TIGHT)
