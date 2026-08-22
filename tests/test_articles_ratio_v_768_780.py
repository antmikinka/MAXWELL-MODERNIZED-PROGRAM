"""Qualifying article tests for Treatise Arts. 768-780 (ratio of ESU to EMU units).

Part IV Chapter XIX: the experimental determination that the ratio of
electrostatic to electromagnetic units is a velocity, of the order of the
speed of light.  Evidence bundle for the LAST200 Stage 4 §3.4 Cluster D
acceptance criteria:

* dimensional check: every reduction carries ``[v] = L T^-1`` (cm/s),
  hand-derived in-test from the two defining force laws (never by
  re-deriving the code under test);
* Maxwell-parameter golden anchor: all methods recover
  ``v = 3.107 x 10^10 cm/s`` (EMPIRICAL tolerance class, rel_tol = 5e-2;
  provenance: Treatise Arts. 775-778 report v ~ 3.1 x 10^10 cm/s; the
  anchor value is the Weber-Kohlrausch (1856) result quoted in the
  chapter, cf. the Stage 4 §2.5 reference-store entry
  ``art768_weber_kohlrausch_v``);
* monotonicity/sensitivity sanity: the Art. 777 rapid-action correction
  never amplifies (Stage 3 defect D-03 regression ally — the canonical
  failing-before/passing-after guard lives in ``test_defects_s1.py``);
* condenser series/parallel identities in both unit systems, related by
  ``v^2``;
* independent oracles: hand-derived dimensional algebra, hand-computed
  golden readings, and ``core.units.dimensions.convert_esu_to_emu`` as a
  second, independently-coded conversion route.

Numeric-value convention (Maxwell, Arts. 768-770): for one and the same
physical quantity with readings ``n_esu``, ``n_emu``,
``n_esu / n_emu = v**p`` with p = +1 (charge, current), -1 (potential),
+2 (capacitance), -2 (resistance, inductance).

Tolerance classes follow docs/LAST200_STAGE4_TESTING_STRATEGY.md §2.5.
Golden values are inlined with provenance comments (the central
``tests/articles/reference_values.json`` store does not exist yet — same
deviation as ``test_defects_s1.py``).
"""

from __future__ import annotations

import math

import pytest

from maxwell.config.constants import CONST
from maxwell.core.units.dimensions import convert_esu_to_emu
from maxwell.experiments.ratio_v.combined import (
    apply_rapid_action_correction,
    combine_coil_condenser,
    compare_capacity_inductance,
    method_condenser_wippe,
    method_intermittent_current,
    method_maxwell_combined,
    rapid_action_charge_fraction,
)
from maxwell.experiments.ratio_v.condensers import (
    CondenserMeasurement,
    capacity_parallel,
    capacity_series,
    convert_capacity,
    method_jenkin,
    method_thomson_electrometer,
    method_weber_kohlrausch,
    sphere_capacity_esu,
)
from maxwell.experiments.ratio_v.theory import (
    UNIT_RATIO_POWERS,
    UnitRatioExperiment,
    calc_convection_current,
    compare_resistance_systems,
    derive_unit_ratio_dimension,
    historical_v_anchor,
    motivate_ratio_investigation,
    prove_ratio_is_velocity,
    v_from_convection_field,
)

from articles import ref_value, tolerance_of

# ── Constants and tolerance classes (Stage 4 §2.5) ──────────────────────

C_LIGHT = CONST.C  # 2.99792458e10 cm/s, the single source of truth

#: Historical anchor for v.  Provenance: Treatise Arts. 775-778 reported
#: value ~ 3.1 x 10^10 cm/s; 3.107 x 10^10 cm/s is the Weber-Kohlrausch
#: (1856) result quoted in the chapter (EMPIRICAL tolerance class).
#: Pinned in the reference store (art 768, weber_kohlrausch_v).
V_HIST = ref_value(768, "weber_kohlrausch_v")
TIGHT = 1e-10  # pure identities, closed-form algebra
STANDARD = 1e-8  # analytic formulas at exact points
NUMERIC = 1e-6  # quadrature/transcendentals
EMPIRICAL = 5e-2  # historical anchors

# ── Hand-derived dimensional oracle (independent of the code under test) ─
#
# Doubled (M, L, T) exponent vectors, derived here from the two defining
# force laws: ESU from Coulomb F = q1 q2 / r^2 ([q^2] = [F][L]^2 =
# M L^3 T^-2), EMU from Ampere's element force ([I^2] = [F][L]^2/[L]^2 =
# M L T^-2).  All other quantities follow mechanically.
_DIM = {
    "velocity": (0, 2, -2),
    "length": (0, 2, 0),
    "time": (0, 0, 2),
    "frequency": (0, 0, -2),
    "charge_esu": (1, 3, -2),
    "charge_emu": (1, 1, 0),
    "current_esu": (1, 3, -4),
    "current_emu": (1, 1, -2),
    "potential_esu": (1, 1, -2),
    "potential_emu": (1, 3, -4),
    "resistance_esu": (0, -2, 2),  # s/cm
    "resistance_emu": (0, 2, -2),  # cm/s
    "capacitance_esu": (0, 2, 0),  # cm
    "capacitance_emu": (0, -2, 4),  # s^2/cm
    "inductance_esu": (0, -2, 4),  # s^2/cm
    "inductance_emu": (0, 2, 0),  # cm
    "angular_velocity": (0, 0, -2),
}


def _dim_mul(*dims):
    """Dimensional product: doubled exponents add."""
    out = [0, 0, 0]
    for d in dims:
        for i in range(3):
            out[i] += d[i]
    return tuple(out)


def _dim_div(a, b):
    """Dimensional quotient: doubled exponents subtract."""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dim_sqrt(d):
    """Dimensional square root: doubled exponents halve."""
    assert all(e % 2 == 0 for e in d), f"odd doubled exponents: {d}"
    return (d[0] // 2, d[1] // 2, d[2] // 2)


# ── Maxwell-era apparatus for the shared anchor (documented parameters) ──
#
# Orders of magnitude of the Chapter XIX laboratory practice: a Leyden
# battery of ~0.5 microfarad (5e5 cm of ESU capacitance), a battery of
# hundreds of Daniell cells (~600 V ~ 2 statvolt), a 1 megohm standard
# coil (1e15 abohm), a 0.1 henry coil (1e8 cm of EMU inductance), and
# hand-operated key/wippe at ~1 Hz.
_APP = {
    "C_esu": 5.0e5,  # cm
    "V_esu": 2.0,  # statvolt
    "R_emu": 1.0e15,  # abohm (1 megohm)
    "L_emu": 1.0e8,  # cm (0.1 H)
    "f": 1.0,  # Hz
}


# ── Art. 768 — statement and significance of the investigation ──────────


@pytest.mark.article(768)
def test_art_768_motivation_quantitative_anchor():
    """Art. 768: the motivation carries the quantitative historical anchor.

    The chapter's point is not prose but a number: the reported ratio is
    a velocity of ~3.1 x 10^10 cm/s.  The motivation dictionary must pin
    that value (EMPIRICAL class) together with its provenance, and the
    anchor must be self-consistent with ``historical_v_anchor`` and with
    the accepted speed of light to within the historical tolerance.
    """
    motivation = motivate_ratio_investigation()
    reported = motivation["reported_v_cm_s"]
    # hand-derived oracle: the stored anchor value itself (provenance above)
    assert reported == pytest.approx(V_HIST, rel=EMPIRICAL)
    assert motivation["reported_v_rel_tol"] == pytest.approx(EMPIRICAL, rel=TIGHT)
    # internal consistency: motivation and anchor agree exactly
    anchor = historical_v_anchor()
    assert reported == pytest.approx(anchor["v_cm_s"], rel=TIGHT)
    assert anchor["rel_tol"] == pytest.approx(EMPIRICAL, rel=TIGHT)
    # the reported value is a velocity of the order of light: within the
    # historical tolerance of the accepted c
    assert abs(reported - C_LIGHT) / C_LIGHT < EMPIRICAL


# ── Art. 769 — the ratio is dimensionally a velocity ────────────────────


@pytest.mark.article(769)
def test_art_769_dimensional_derivation_from_force_laws():
    """Art. 769: [Q_ESU]/[Q_EMU] is a power of velocity, derived (D-19).

    Independent oracle: the doubled exponent vectors are hand-derived in
    ``_DIM`` from Coulomb's and Ampere's force laws.  For every quantity
    the derivation must reproduce both the dimensional power (exponent
    vector) and the numeric power p of v in n_esu/n_emu = v^p.
    """
    # hand-derived expectation: ratio exponents and velocity power p
    expected = {
        "charge": (0, 1, -1),
        "current": (0, 1, -1),
        "potential": (0, -1, 1),
        "resistance": (0, -2, 2),
        "capacitance": (0, 2, -2),
        "inductance": (0, -2, 2),
    }
    for quantity, ratio_exp in expected.items():
        result = derive_unit_ratio_dimension(quantity)
        assert result["is_velocity_power"] is True
        got = result["ratio_exponents"]
        for g, e in zip(got, ratio_exp):
            assert g == pytest.approx(float(e), abs=1e-12)
        p = UNIT_RATIO_POWERS[quantity]
        assert result["velocity_power"] == pytest.approx(p, abs=1e-12)
        # derivation matches the numeric convention: the power derived
        # from the force laws equals the numeric power of v in
        # n_esu/n_emu = v^p (hand-derived consistency)
        assert math.isclose(result["velocity_power"], result["numeric_power"])
    # the proof entry point returns the derived result, never the measured
    # value (D-19 closure: no speed-of-light constant in the derivation)
    proof = prove_ratio_is_velocity("charge")
    assert proof["ratio_dimensions"] == "L T^-1"
    assert proof["is_velocity_power"] is True


@pytest.mark.sympy
@pytest.mark.article(769)
def test_art_769_sympy_symbolic_derivation():
    """Art. 769: symbolic check that [q_ESU]/[q_EMU] = L T^-1.

    Independent symbolic oracle built from the two force laws (Stage 4
    §3.4: 'symbolic dimensional derivation (SymPy)').  ESU: q^2 = F r^2
    (Coulomb).  EMU: I^2 dl^2 / r^2 = F (Ampere element force), so
    I^2 = F and q_EMU = I T.
    """
    import sympy as sp

    M, L, T = sp.symbols("M L T", positive=True)
    force = M * L * T**-2  # Newton: M L T^-2
    q_esu = sp.sqrt(force * L**2)  # Coulomb: q^2 = F r^2
    i_emu = sp.sqrt(force)  # Ampere: I^2 dl^2/r^2 = F with dl, r both lengths
    q_emu = i_emu * T  # charge = current x time
    ratio = sp.simplify(q_esu / q_emu)
    # hand-derived expectation: exactly L T^-1, mass cancels
    assert sp.simplify(ratio - L / T) == 0
    powers = sp.powsimp(ratio, combine="all").as_powers_dict()
    assert math.isclose(float(powers.get(L, 0)), 1.0, abs_tol=1e-12)
    assert math.isclose(float(powers.get(T, 0)), -1.0, abs_tol=1e-12)
    assert math.isclose(float(powers.get(M, 0)), 0.0, abs_tol=1e-12)


@pytest.mark.article(769)
def test_art_769_unit_ratio_experiment_all_quantities():
    """Art. 769: the p-aware framework recovers v from readings in either
    direction of the unit-size asymmetry.

    Readings are constructed by hand for each power p:
    n_esu = 2 v^p, n_emu = 2  =>  v = (n_esu/n_emu)^(1/p).  Charge is
    additionally cross-checked against the independently coded conversion
    in ``core.units.dimensions`` (D-20 route).
    """
    for quantity, p in UNIT_RATIO_POWERS.items():
        n_esu = 2.0 * C_LIGHT**p
        exp = UnitRatioExperiment(n_esu, 2.0, quantity, quantity_kind=quantity)
        assert exp.calculate_ratio() == pytest.approx(C_LIGHT, rel=STANDARD)
        assert exp.verify_equals_c() is True
    # independent oracle (separately coded module): one abcoulomb holds
    # c statcoulombs, i.e. converting 1 ESU charge to EMU divides by c
    one_abcoulomb_in_statcoulombs = 1.0 / convert_esu_to_emu(1.0, "charge")
    assert one_abcoulomb_in_statcoulombs == pytest.approx(C_LIGHT, rel=STANDARD)
    q_experiment = UnitRatioExperiment(
        one_abcoulomb_in_statcoulombs, 1.0, "one abcoulomb", quantity_kind="charge"
    )
    assert q_experiment.calculate_ratio() == pytest.approx(C_LIGHT, rel=STANDARD)


@pytest.mark.article(769)
def test_art_769_dimensional_check_v_cm_s():
    """Required anchor: [v] = cm/s for every Chapter XIX reduction.

    Each formula's dimensional vector is computed here from the
    hand-derived oracle ``_DIM`` (doubled exponents) and must equal the
    velocity vector (0, 2, -2) before halving where applicable.
    """
    velocity = _DIM["velocity"]
    reductions = {
        # Weber-Kohlrausch / WK family: sqrt(C_ESU / C_EMU)
        "weber_kohlrausch": _dim_sqrt(
            _dim_div(_DIM["capacitance_esu"], _DIM["capacitance_emu"])
        ),
        # Thomson: I_EMU R_EMU / V_ESU
        "thomson": _dim_div(
            _dim_mul(_DIM["current_emu"], _DIM["resistance_emu"]),
            _DIM["potential_esu"],
        ),
        # Jenkin / intermittent current: I_ESU / I_EMU
        "jenkin": _dim_div(_DIM["current_esu"], _DIM["current_emu"]),
        # wippe: sqrt(R_EMU C_ESU f)
        "wippe": _dim_sqrt(
            _dim_mul(
                _DIM["resistance_emu"], _DIM["capacitance_esu"], _DIM["frequency"]
            )
        ),
        # LC resonance: omega sqrt(L_EMU C_ESU)
        "lc_resonance": _dim_mul(
            _DIM["angular_velocity"],
            _dim_sqrt(_dim_mul(_DIM["inductance_emu"], _DIM["capacitance_esu"])),
        ),
        # coil + condenser: sqrt(L_EMU C_ESU) / T
        "coil_condenser": _dim_div(
            _dim_sqrt(_dim_mul(_DIM["inductance_emu"], _DIM["capacitance_esu"])),
            _DIM["time"],
        ),
        # resistance comparison: sqrt(R_EMU / R_ESU)
        "resistance": _dim_sqrt(
            _dim_div(_DIM["resistance_emu"], _DIM["resistance_esu"])
        ),
        # convection field inversion: q omega / (a H); [H] = M^1/2 L^-1/2 T^-1
        "convection": _dim_div(
            _dim_mul(_DIM["charge_esu"], _DIM["angular_velocity"]),
            _dim_mul(_DIM["length"], (1, -1, -2)),
        ),
    }
    for name, dim in reductions.items():
        assert dim == velocity, f"{name}: got {dim}, expected {velocity}"
        # numeric tie: the dimensional velocity power of each reduction is
        # exactly +1, i.e. one power of v (hand-derived p = 1)
        assert math.isclose(dim[1] / 2, 1.0, abs_tol=1e-12)
        assert math.isclose(dim[2] / 2, -1.0, abs_tol=1e-12)


# ── Art. 770 — convection current ───────────────────────────────────────


@pytest.mark.article(770)
def test_art_770_convection_current_geometry_and_field():
    """Art. 770: rotating charged ring — explicit geometry (D-20 closure).

    Hand-derived oracle: one revolution of period T = 2 pi / omega
    transports the whole charge, so I_ESU = q omega / (2 pi), the EMU
    current is smaller by the factor v (charge power p = +1), and the
    centre field of the ring is H = 2 pi I_EMU / a = q omega / (v a).
    The EMU current is cross-checked against the independently coded
    ``convert_esu_to_emu`` route.
    """
    q, a, omega = 10.0, 5.0, 100.0  # statcoulomb, cm, rad/s
    result = calc_convection_current(q, a, omega)
    period = 2.0 * math.pi / omega
    assert result["period_s"] == pytest.approx(period, rel=TIGHT)
    assert result["current_esu"] == pytest.approx(q / period, rel=TIGHT)
    expected_emu = q * omega / (2.0 * math.pi * C_LIGHT)
    assert result["current_emu"] == pytest.approx(expected_emu, rel=TIGHT)
    assert result["field_at_center"] == pytest.approx(
        q * omega / (C_LIGHT * a), rel=TIGHT
    )
    # independent conversion oracle (D-20): I_EMU = q_EMU / period with
    # q_EMU from the separately coded core conversion
    q_emu = convert_esu_to_emu(q, "charge")
    assert result["current_emu"] == pytest.approx(q_emu / period, rel=TIGHT)
    # inversion: measuring the field determines v
    v_recovered = v_from_convection_field(q, a, omega, result["field_at_center"])
    assert v_recovered == pytest.approx(C_LIGHT, rel=TIGHT)
    # sensitivity: half the field implies double the recovered velocity
    assert v_from_convection_field(
        q, a, omega, 0.5 * result["field_at_center"]
    ) == pytest.approx(2.0 * C_LIGHT, rel=TIGHT)


# ── Arts. 771-774 — condenser methods ───────────────────────────────────


@pytest.mark.article(771)
def test_art_771_weber_kohlrausch_reduction():
    """Art. 771: WK reduction v = sqrt(C_ESU/C_EMU), with the ESU value
    from geometry (isolated sphere C = K a) and hand-checked dimensions.
    """
    # geometric ESU capacitance: sphere of radius a has C = K a cm
    assert sphere_capacity_esu(10.0) == pytest.approx(10.0, rel=TIGHT)
    assert sphere_capacity_esu(10.0, 2.0) == pytest.approx(20.0, rel=TIGHT)
    c_esu = sphere_capacity_esu(10.0)
    c_emu = c_esu / C_LIGHT**2  # hand-derived: C_EMU = C_ESU / v^2
    v = method_weber_kohlrausch(c_esu, c_emu)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # dimensional oracle: L / (L^-1 T^2) = L^2 T^-2, sqrt -> velocity
    assert _dim_sqrt(_dim_div(_DIM["capacitance_esu"], _DIM["capacitance_emu"])) == (
        0,
        2,
        -2,
    )
    # dataclass route agrees with the function route
    meas = CondenserMeasurement(c_esu, c_emu, "weber_kohlrausch")
    assert meas.calculate_v() == pytest.approx(v, rel=TIGHT)
    assert meas.deviation_from_c() == pytest.approx(0.0, abs=1e-6)


@pytest.mark.article(771)
def test_art_771_series_parallel_identities_both_systems():
    """Art. 771: composition identities hold in both unit systems and
    commute with the v^2 conversion.

    Hand-derived oracle: C1 = 3, C2 = 6 (cm): parallel = 9, series = 2.
    """
    c1, c2 = 3.0, 6.0
    par_esu = capacity_parallel(c1, c2)
    ser_esu = capacity_series(c1, c2)
    assert par_esu == pytest.approx(9.0, rel=TIGHT)
    assert ser_esu == pytest.approx(2.0, rel=TIGHT)
    # convert the whole combination, or combine the converted parts: the
    # two routes must coincide (linear/rational maps commute with /v^2)
    for v in (C_LIGHT, V_HIST):
        e1 = convert_capacity(c1, "to_emu", v)
        e2 = convert_capacity(c2, "to_emu", v)
        assert capacity_parallel(e1, e2) == pytest.approx(
            convert_capacity(par_esu, "to_emu", v), rel=TIGHT
        )
        assert capacity_series(e1, e2) == pytest.approx(
            convert_capacity(ser_esu, "to_emu", v), rel=TIGHT
        )
        # the two systems are related by exactly v^2 for the combinations
        assert par_esu / capacity_parallel(e1, e2) == pytest.approx(v**2, rel=TIGHT)
        assert ser_esu / capacity_series(e1, e2) == pytest.approx(v**2, rel=TIGHT)
    # round trip: ESU -> EMU -> ESU at the historical anchor
    assert convert_capacity(
        convert_capacity(9.0, "to_emu", V_HIST), "to_esu", V_HIST
    ) == pytest.approx(9.0, rel=TIGHT)


@pytest.mark.article(772)
def test_art_772_thomson_emf_ratio():
    """Art. 772: Thomson's method v = I_EMU R_EMU / V_ESU.

    Hand-derived apparatus: V_ESU = 2 statvolt (~600 V electrometer
    reading), I = 0.5 abampere, R = 4 c abohm so that I R = c V_ESU in
    abvolts.  Dimensional oracle: (M^1/2 L^1/2 T^-1)(L T^-1) /
    (M^1/2 L^1/2 T^-1) = L T^-1.
    """
    v_esu, i_emu = 2.0, 0.5
    r_emu = C_LIGHT * v_esu / i_emu  # hand-derived balance reading
    v = method_thomson_electrometer(v_esu, i_emu, r_emu)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # dimensional oracle via doubled vectors
    assert _dim_div(
        _dim_mul(_DIM["current_emu"], _DIM["resistance_emu"]), _DIM["potential_esu"]
    ) == (0, 2, -2)
    # sensitivity: v is linear in the EMU emf (doubling R doubles v)
    assert method_thomson_electrometer(v_esu, i_emu, 2.0 * r_emu) == pytest.approx(
        2.0 * C_LIGHT, rel=STANDARD
    )


@pytest.mark.article(774)
def test_art_774_jenkin_intermittent_discharge():
    """Art. 774: Jenkin's method v = C_ESU V_ESU f / I_EMU.

    Hand-derived Maxwell-era apparatus: C = 1e6 cm (~1.1 microfarad),
    V = 2 statvolt (~600 V), f = 0.5 Hz, giving an average discharge
    current I_EMU = C V f / c ~ 3.34e-5 abampere (0.33 mA) — a
    galvanometer-scale current.
    """
    c_esu, v_esu, f = 1.0e6, 2.0, 0.5
    i_emu = c_esu * v_esu * f / C_LIGHT  # hand-derived reading
    v = method_jenkin(c_esu, v_esu, f, i_emu)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # the same physics implemented in combined.py must agree exactly
    assert method_intermittent_current(c_esu, v_esu, f, i_emu) == pytest.approx(
        v, rel=TIGHT
    )
    # dimensional oracle: ratio of currents -> one power of velocity
    assert _dim_div(_DIM["current_esu"], _DIM["current_emu"]) == (0, 2, -2)
    # sensitivity: v is linear in the frequency
    assert method_jenkin(c_esu, v_esu, 2.0 * f, i_emu) == pytest.approx(
        2.0 * C_LIGHT, rel=STANDARD
    )


# ── Arts. 773, 775-779 — combined methods ───────────────────────────────


@pytest.mark.article(773)
def test_art_773_maxwell_combined_cross_routes():
    """Art. 773: Maxwell's combined method — two routes agree, RC is a
    pure-time invariant.

    Hand-derived Maxwell-era apparatus: R = 1 megohm standard (1e15
    abohm), C = 5e5 cm (~0.56 microfarad Leyden battery).  Readings in
    the other system follow from the powers p = -2 (resistance) and
    p = +2 (capacitance).  The RC time constant is hand-computed:
    tau = R_EMU C_ESU / c^2 = 0.5563250280... s.
    """
    r_emu = 1.0e15
    c_esu = 5.0e5
    r_esu = r_emu / C_LIGHT**2  # hand-derived (p = -2)
    c_emu = c_esu / C_LIGHT**2  # hand-derived (p = +2)
    result = method_maxwell_combined(r_esu, r_emu, c_esu, c_emu)
    assert result["v_from_resistance"] == pytest.approx(C_LIGHT, rel=STANDARD)
    assert result["v_from_capacitance"] == pytest.approx(C_LIGHT, rel=STANDARD)
    assert result["mean_v"] == pytest.approx(C_LIGHT, rel=STANDARD)
    assert result["mean_v"] == pytest.approx(V_HIST, rel=EMPIRICAL)
    assert result["disagreement_pct"] == pytest.approx(0.0, abs=1e-12)
    # pure-time invariant: R_EMU C_EMU = R_ESU C_ESU, hand-computed value
    tau_hand = ref_value(773, "rc_time_constant")
    assert result["rc_time_constant_emu_s"] == pytest.approx(
        tau_hand, **tolerance_of(773, "rc_time_constant")
    )
    assert result["rc_time_constant_esu_s"] == pytest.approx(
        tau_hand, **tolerance_of(773, "rc_time_constant")
    )
    assert result["rc_invariance_rel_diff"] == pytest.approx(0.0, abs=1e-12)
    # direction guard (regression ally): the inverted resistance formula
    # sqrt(R_ESU/R_EMU) yields 1/c, off by a factor c^2 — the reduction
    # must sit on the correct branch
    wrong_direction = math.sqrt(r_esu / r_emu)
    assert wrong_direction == pytest.approx(1.0 / C_LIGHT, rel=TIGHT)
    assert result["v_from_resistance"] / wrong_direction == pytest.approx(
        C_LIGHT**2, rel=TIGHT
    )


@pytest.mark.article(773)
def test_art_773_cross_method_agreement():
    """Art. 773 programme: every Chapter XIX method applied to one
    self-consistent apparatus must return the same velocity.

    The readings are constructed by forward physics at the accepted c
    from independent base quantities (C_ESU, V_ESU, R_EMU, L_EMU, f);
    the assertion is method-vs-method agreement, independent of any
    historical anchor (anti-circularity: no method is compared against a
    value it helped to construct).
    """
    c_esu, v_esu, r_emu, l_emu, f = 5.0e5, 2.0, 1.0e15, 1.0e8, 1.0
    v_wk = method_weber_kohlrausch(c_esu, c_esu / C_LIGHT**2)
    v_th = method_thomson_electrometer(
        v_esu, 0.1, C_LIGHT * v_esu / 0.1
    )
    v_je = method_jenkin(c_esu, v_esu, f, c_esu * v_esu * f / C_LIGHT)
    v_ic = method_intermittent_current(c_esu, v_esu, f, c_esu * v_esu * f / C_LIGHT)
    v_wi = method_condenser_wippe(1.0, c_esu, C_LIGHT**2 / (c_esu * f), f)
    omega = C_LIGHT / math.sqrt(l_emu * c_esu)
    v_lc = compare_capacity_inductance(c_esu, l_emu, omega)
    period = 2.0 * math.pi * math.sqrt(l_emu * c_esu) / C_LIGHT
    v_cc = combine_coil_condenser(l_emu, c_esu, period)
    v_re = compare_resistance_systems(r_emu / C_LIGHT**2, r_emu)["calculated_v"]
    v_co = method_maxwell_combined(
        r_emu / C_LIGHT**2, r_emu, c_esu, c_esu / C_LIGHT**2
    )["mean_v"]
    values = [v_wk, v_th, v_je, v_ic, v_wi, v_lc, v_cc, v_re, v_co]
    for v in values:
        assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    # mutual agreement tighter than any method tolerance
    spread = (max(values) - min(values)) / C_LIGHT
    assert math.isclose(spread, 0.0, abs_tol=1e-9)


@pytest.mark.article(775)
def test_art_775_intermittent_current():
    """Art. 775: intermittent-current reduction with its own apparatus.

    Hand-derived: C = 5e5 cm, V = 2 statvolt, f = 1 Hz gives
    I_EMU = C V f / c ~ 3.34e-5 abampere; the charge per cycle is
    Q = C V = 1e6 statcoulomb.
    """
    c_esu, v_esu, f = 5.0e5, 2.0, 1.0
    charge_per_cycle = c_esu * v_esu  # hand-derived: 1e6 statcoulomb
    assert charge_per_cycle == pytest.approx(1.0e6, rel=TIGHT)
    i_emu = charge_per_cycle * f / C_LIGHT
    v = method_intermittent_current(c_esu, v_esu, f, i_emu)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # closure: recompute the current from the recovered v and the ESU
    # charge; it must reproduce the measured current
    assert charge_per_cycle * f / v == pytest.approx(i_emu, rel=TIGHT)


@pytest.mark.article(776)
def test_art_776_condenser_wippe_balance():
    """Art. 776: wippe balance v = sqrt(R C_ESU f / rho).

    Hand-derived apparatus: C = 1e6 cm, f = 10 Hz, rho = 1, balance
    resistance R = c^2/(C f) ~ 8.99e13 abohm (~90 kohm).  Dimensional
    oracle: (L T^-1)(L)(T^-1) = L^2 T^-2; square root -> velocity.  The
    legacy inverted form 1/sqrt(R C f) is dimensionless and wrong — the
    reduction must carry cm/s.
    """
    c_esu, f = 1.0e6, 10.0
    r_emu = C_LIGHT**2 / (c_esu * f)  # hand-derived balance resistance
    v = method_condenser_wippe(1.0, c_esu, r_emu, f)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # dimensional oracle: R_EMU C_ESU f is L^2 T^-2 (its square root cm/s)
    assert _dim_mul(_DIM["resistance_emu"], _DIM["capacitance_esu"], _DIM["frequency"]) == (
        0,
        4,
        -4,
    )
    # bridge-ratio convention: v ∝ rho^-1/2 at fixed R, C, f
    assert method_condenser_wippe(4.0, c_esu, r_emu, f) == pytest.approx(
        0.5 * C_LIGHT, rel=STANDARD
    )
    # square-root sensitivity in R: doubling R multiplies v by sqrt(2)
    assert method_condenser_wippe(1.0, c_esu, 2.0 * r_emu, f) == pytest.approx(
        math.sqrt(2.0) * C_LIGHT, rel=STANDARD
    )


@pytest.mark.article(777)
def test_art_777_rapid_action_correction_contract():
    """Art. 777: rapid-action correction never amplifies (D-03 ally).

    Hand-derived oracle: charge fraction = 1 - exp(-t_half/RC) with
    t_half = 1/(2f).  The corrected value is measured_v times that
    fraction, so it is never larger than the measurement; the engineered
    fraction = 0.5 case halves it exactly; in the slow limit the
    correction tends to the identity.
    """
    # charge fraction against a hand-evaluated exponential
    f, rc = 1.0, 0.3
    fraction_hand = 1.0 - math.exp(-0.5 / rc)  # t_half = 0.5 s
    assert rapid_action_charge_fraction(f, rc) == pytest.approx(
        fraction_hand, rel=NUMERIC
    )
    # engineered fraction = 0.5 exactly: t_half/RC = ln 2
    rc_half = 1.0 / (2.0 * math.log(2.0))
    assert apply_rapid_action_correction(1.0, 1.0, rc_half) == pytest.approx(
        0.5, rel=1e-12
    )
    # never amplifies: corrected strictly below measured for rapid action
    for f_i, rc_i in [(1.0, 0.1), (10.0, 0.5), (0.5, 2.0), (50.0, 1e-3)]:
        corrected = apply_rapid_action_correction(2.5e10, f_i, rc_i)
        assert corrected < 2.5e10
        assert corrected == pytest.approx(
            2.5e10 * (1.0 - math.exp(-1.0 / (2.0 * f_i * rc_i))), rel=NUMERIC
        )
    # monotone in rapidity: the action is "too rapid" when the switching
    # half-period is short compared with RC; a LARGER time constant
    # (slower circuit) undercharges more and shrinks the corrected v more
    v_slow_circuit = apply_rapid_action_correction(1.0, 1.0, 0.5)
    v_fast_circuit = apply_rapid_action_correction(1.0, 1.0, 0.05)
    assert v_slow_circuit < v_fast_circuit < 1.0
    # equivalently, faster switching (smaller half-period) shrinks more
    assert apply_rapid_action_correction(1.0, 10.0, 0.5) < apply_rapid_action_correction(
        1.0, 1.0, 0.5
    )
    # slow limit: charge fraction -> 1, correction -> identity
    assert apply_rapid_action_correction(1.0, 1e-6, 1.0) == pytest.approx(
        1.0, rel=1e-9
    )


@pytest.mark.article(778)
def test_art_778_lc_resonance_velocity():
    """Art. 778: capacity vs self-induction, v = omega sqrt(L_EMU C_ESU).

    Hand-derived apparatus: L = 1e8 cm (0.1 H), C = 1e5 cm (~0.11
    microfarad); omega = c / sqrt(L C) ~ 5.996e4 rad/s.  Dimensional
    oracle: sqrt(cm x cm) x s^-1 = cm/s.
    """
    l_emu, c_esu = 1.0e8, 1.0e5
    omega_hand = C_LIGHT / math.sqrt(l_emu * c_esu)
    v = compare_capacity_inductance(c_esu, l_emu, omega_hand)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # dimensional oracle: (L)(L) under the root, times T^-1
    assert _dim_mul(
        _DIM["angular_velocity"],
        _dim_sqrt(_dim_mul(_DIM["inductance_emu"], _DIM["capacitance_esu"])),
    ) == (0, 2, -2)
    # sensitivity: v is linear in omega
    assert compare_capacity_inductance(c_esu, l_emu, 2.0 * omega_hand) == pytest.approx(
        2.0 * C_LIGHT, rel=STANDARD
    )


@pytest.mark.article(779)
def test_art_779_coil_condenser_period():
    """Art. 779: coil + condenser, v = 2 pi sqrt(L_EMU C_ESU) / T.

    Hand-derived apparatus: L = 1e8 cm, C = 1e5 cm,
    T = 2 pi sqrt(L C)/c ~ 1.048e-4 s.  Cross-checked against the
    Art. 778 resonance route on the same apparatus (two independent
    reductions of one LC oscillator must agree).
    """
    l_emu, c_esu = 1.0e8, 1.0e5
    period_hand = 2.0 * math.pi * math.sqrt(l_emu * c_esu) / C_LIGHT
    v = combine_coil_condenser(l_emu, c_esu, period_hand)
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # independent-method agreement: period and angular frequency routes
    omega = 2.0 * math.pi / period_hand
    assert compare_capacity_inductance(c_esu, l_emu, omega) == pytest.approx(
        v, rel=TIGHT
    )
    # dimensional oracle: sqrt(L C) / T -> L T^-1
    assert _dim_div(
        _dim_sqrt(_dim_mul(_DIM["inductance_emu"], _DIM["capacitance_esu"])),
        _DIM["time"],
    ) == (0, 2, -2)


# ── Art. 780 — comparison of the two resistance systems ─────────────────


@pytest.mark.article(780)
def test_art_780_resistance_ratio_direction():
    """Art. 780: v = sqrt(R_EMU / R_ESU) — and not the inverted root.

    Hand-derived apparatus: the same 1 megohm coil reads R_EMU = 1e15
    abohm and R_ESU = 1e15/c^2 = 1.11265...e-6 statohm.  Dimensional
    oracle: (L T^-1)/(L^-1 T) = L^2 T^-2; square root -> velocity.  The
    inverted formula sqrt(R_ESU/R_EMU) = 1/c is off by c^2 and must not
    be returned (the pre-uplift code sat on that branch).
    """
    r_emu = 1.0e15  # abohm = 1 megohm
    r_esu = r_emu / C_LIGHT**2  # hand-derived statohm reading
    result = compare_resistance_systems(r_esu, r_emu)
    v = result["calculated_v"]
    assert v == pytest.approx(C_LIGHT, rel=STANDARD)
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # direction guard: the wrong root is 1/c, smaller than the right one
    # by exactly c^2
    wrong = math.sqrt(r_esu / r_emu)
    assert wrong == pytest.approx(1.0 / C_LIGHT, rel=TIGHT)
    assert v / wrong == pytest.approx(C_LIGHT**2, rel=TIGHT)
    # the p-aware framework agrees with the dedicated reduction
    exp = UnitRatioExperiment(r_esu, r_emu, "megohm coil", quantity_kind="resistance")
    assert exp.calculate_ratio() == pytest.approx(v, rel=TIGHT)
    # dimensional oracle
    assert _dim_sqrt(_dim_div(_DIM["resistance_emu"], _DIM["resistance_esu"])) == (
        0,
        2,
        -2,
    )


# ── Shared v-anchor: Maxwell-parameter golden test (whole chapter) ──────


def _anchor_readings() -> dict[str, float]:
    """Readings of the documented apparatus at the historical anchor.

    The base apparatus (_APP) is expressed at v = V_HIST using the
    power table: R_ESU = R_EMU/v^2, C_EMU = C_ESU/v^2, I = C V f / v,
    balance R = v^2/(C f), omega = v/sqrt(L C), T = 2 pi sqrt(L C)/v.
    """
    c_esu, v_esu, r_emu, l_emu, f = (
        _APP["C_esu"],
        _APP["V_esu"],
        _APP["R_emu"],
        _APP["L_emu"],
        _APP["f"],
    )
    va = V_HIST
    return {
        "R_esu": r_emu / va**2,
        "C_emu": c_esu / va**2,
        "I_discharge": c_esu * v_esu * f / va,
        "R_wippe": va**2 / (c_esu * f),
        "omega": va / math.sqrt(l_emu * c_esu),
        "period": 2.0 * math.pi * math.sqrt(l_emu * c_esu) / va,
        "R_thomson": va * v_esu / 0.1,
    }


def _anchor_cases():
    """Parametrization cases: (article, description, callable -> v)."""
    c_esu, v_esu, r_emu, l_emu, f = (
        _APP["C_esu"],
        _APP["V_esu"],
        _APP["R_emu"],
        _APP["L_emu"],
        _APP["f"],
    )
    rd = _anchor_readings()
    return [
        pytest.param(
            lambda: method_weber_kohlrausch(c_esu, rd["C_emu"]),
            marks=[pytest.mark.article(771)],
            id="art771-weber-kohlrausch",
        ),
        pytest.param(
            lambda: method_thomson_electrometer(v_esu, 0.1, rd["R_thomson"]),
            marks=[pytest.mark.article(772)],
            id="art772-thomson",
        ),
        pytest.param(
            lambda: method_maxwell_combined(
                rd["R_esu"], r_emu, c_esu, rd["C_emu"]
            )["mean_v"],
            marks=[pytest.mark.article(773)],
            id="art773-maxwell-combined",
        ),
        pytest.param(
            lambda: method_jenkin(c_esu, v_esu, f, rd["I_discharge"]),
            marks=[pytest.mark.article(774)],
            id="art774-jenkin",
        ),
        pytest.param(
            lambda: method_intermittent_current(c_esu, v_esu, f, rd["I_discharge"]),
            marks=[pytest.mark.article(775)],
            id="art775-intermittent-current",
        ),
        pytest.param(
            lambda: method_condenser_wippe(1.0, c_esu, rd["R_wippe"], f),
            marks=[pytest.mark.article(776)],
            id="art776-condenser-wippe",
        ),
        pytest.param(
            lambda: compare_capacity_inductance(c_esu, l_emu, rd["omega"]),
            marks=[pytest.mark.article(778)],
            id="art778-lc-resonance",
        ),
        pytest.param(
            lambda: combine_coil_condenser(l_emu, c_esu, rd["period"]),
            marks=[pytest.mark.article(779)],
            id="art779-coil-condenser",
        ),
        pytest.param(
            lambda: compare_resistance_systems(rd["R_esu"], r_emu)["calculated_v"],
            marks=[pytest.mark.article(780)],
            id="art780-resistance",
        ),
    ]


@pytest.mark.parametrize("reduction", _anchor_cases())
def test_ch19_v_anchor_maxwell_parameters(reduction):
    """The v-anchor (Stage 4 §3.4): every reduction of Chapter XIX, run
    on the documented Maxwell-era apparatus (_APP: 5e5 cm Leyden
    battery, 2 statvolt, 1 megohm, 0.1 H coil, 1 Hz key), recovers the
    reported value v = 3.107 x 10^10 cm/s within the EMPIRICAL class
    (rel_tol 5e-2).  Provenance: Treatise Arts. 775-778 report
    v ~ 3.1 x 10^10 cm/s; the anchor value is the Weber-Kohlrausch
    (1856) result quoted in the chapter.  The anchor itself is a
    velocity of the order of the accepted speed of light.
    """
    v = reduction()
    assert v == pytest.approx(V_HIST, rel=EMPIRICAL)
    # the historical anchor sits within 5% of the accepted c (hand check
    # on the anchor, independent of the code under test)
    assert abs(V_HIST - C_LIGHT) / C_LIGHT < EMPIRICAL
