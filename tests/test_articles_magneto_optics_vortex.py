"""Article-evidence tests for Arts. 806-831 (magneto-optics & vortex engine).

Covers Maxwell 1873, Part IV, Ch. XXI "Magnetic Action on Light":
  * magneto_optics/rotation.py             — Arts. 806-810
  * magneto_optics/circular_polarization.py — Arts. 811-817
  * magneto_optics/energy_analysis.py      — Arts. 818-821
  * vortex_engine/vortex_lattice.py        — Arts. 822-824, 831
  * vortex_engine/helmholtz_law.py         — Art. 823
  * vortex_engine/kinetic_energy.py        — Arts. 824-826
  * vortex_engine/equations_of_motion.py   — Arts. 827-828
  * vortex_engine/magnetic_rotation.py     — Arts. 829-830

Every oracle below is derived independently of the implementation
(Treatise equations, hand arithmetic, or quoted historical data with
provenance).  Tolerance classes:
  TIGHT     — exact algebraic identities (rel/abs 1e-10);
  STANDARD  — floating-point rearrangements (1e-8);
  NUMERIC   — sqrt/root comparisons (1e-6);
  EMPIRICAL — historical measurements (explicit provenance comments).
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from articles import ref_value, tolerance_of

from maxwell.config.constants import CONST
from maxwell.magneto_optics.circular_polarization import (
    CircularlyPolarizedRay,
    calc_circular_velocity_split,
    calc_magnetic_velocity_split,
    calc_natural_velocity_split,
    define_light_vector,
    derive_circular_kinematics,
    perform_kinematic_analysis,
)
from maxwell.magneto_optics.energy_analysis import (
    MagnetoOpticMedium,
    calc_propagation_quadratic,
    prove_real_rotation_required,
    quadratic_coupling_coefficient,
    summarize_magneto_optic_results,
)
from maxwell.magneto_optics.rotation import (
    VERDET_MINUTE_TO_RAD,
    FaradayRotator,
    VerdetTable,
    apply_verdet_negative_rotation,
    establish_rotation_laws,
    measure_rotation_by_analyser,
    model_natural_rotation,
    round_trip_rotation,
    verdet_to_rad,
)
from maxwell.vortex_engine.equations_of_motion import (
    VortexEquations,
    calc_vortex_circular_velocity,
)
from maxwell.vortex_engine.helmholtz_law import (
    apply_helmholtz_vortex_law,
    calc_vortex_stretching,
)
from maxwell.vortex_engine.kinetic_energy import (
    calc_disturbed_vortex_energy,
    calc_plane_wave_vortex_energy,
    calc_vortex_angular_velocity,
    express_vortex_current_velocity,
)
from maxwell.vortex_engine.magnetic_rotation import (
    VERDET_CS2_DATA,
    compare_verdet_data,
    derive_magnetic_rotation,
    rotation_coefficient,
    verdet_inverse_square_analysis,
)
from maxwell.vortex_engine.vortex_lattice import (
    MolecularVortex,
    VortexLattice,
    append_mechanical_theory_notes,
)

TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6

#: Golden angle: Verdet's absolute rotation of the ray E in bisulphide of
#: carbon, 25 deg 28 min (Maxwell 1873, Vol. II, p. 468, Art. 830 table
#: caption "Rotation of the ray E = 25 deg .28'").  EMPIRICAL provenance.
#: Pinned in the reference store (art 830, verdet_E_rotation_deg).
VERDET_E_ROTATION_RAD = math.radians(ref_value(830, "verdet_E_rotation_deg"))


# ── Art. 806 — measurement of rotation by the analyser ──────────────────────


@pytest.mark.article(806)
def test_art806_rotation_measured_by_analyser_difference():
    """Art. 806-807: the rotation is the angle through which the analyser
    must be turned to re-extinguish the ray; only the difference matters.

    Golden: Verdet's E-ray rotation 25 deg 28 min (provenance above).
    """
    assert measure_rotation_by_analyser(0.0, VERDET_E_ROTATION_RAD) == pytest.approx(
        VERDET_E_ROTATION_RAD, abs=TIGHT
    )
    # invariance under a common offset of both analyser readings
    offset = 0.7321
    assert measure_rotation_by_analyser(0.4 + offset, 1.15 + offset) == pytest.approx(
        0.75, abs=TIGHT
    )


# ── Art. 807 — Verdet's law theta = V B L ───────────────────────────────────


@pytest.mark.article(807)
def test_art807_theta_equals_VBL_and_inversion():
    """Art. 807-808: theta = V B L, with V carried in rad/(gauss cm).

    Golden (hand arithmetic): flint glass V = 0.020 min/(G cm)
    (VerdetTable default, EMPIRICAL), B = 1000 G, L = 10 cm gives
    theta = 0.020 * (pi/10800) * 1000 * 10 = pi/54 rad.
    """
    V_min = 0.020
    rotator = FaradayRotator(verdet_constant=verdet_to_rad(V_min), path_length=10.0)
    theta = rotator.rotation_angle(B_field=1000.0)
    assert theta == pytest.approx(math.pi / 54.0, rel=TIGHT)
    # unit-conversion constant is exact: 1 min = pi/10800 rad
    assert VERDET_MINUTE_TO_RAD == pytest.approx(math.pi / 10800.0, rel=TIGHT)
    # inversion B = theta / (V L) round-trips
    assert rotator.B_field_from_rotation(theta) == pytest.approx(1000.0, rel=TIGHT)


# ── Art. 808 — the three laws: path, resolved force, medium ─────────────────


@pytest.mark.article(808)
def test_art808_rotation_follows_resolved_part_of_force():
    """Art. 808: rotation proportional to (1) path length, (2) the resolved
    part of the magnetic force in the direction of the ray, (3) the medium
    coefficient; equals V x (increase of magnetic potential along the ray).
    """
    V = 3.0e-4  # rad/(G cm)
    B = np.array([0.0, 0.0, 1000.0])
    # ray along (0,3,4): cos(angle with B) = 4/5 -> resolved part = 800 G
    laws = establish_rotation_laws(V, B, np.array([0.0, 3.0, 4.0]), 5.0)
    assert laws["resolved_field"] == pytest.approx(800.0, rel=TIGHT)
    assert laws["potential_increase"] == pytest.approx(800.0 * 5.0, rel=TIGHT)
    assert laws["rotation_angle"] == pytest.approx(V * 800.0 * 5.0, rel=TIGHT)
    # transverse ray: zero resolved part -> zero rotation (law 2)
    laws_t = establish_rotation_laws(V, B, np.array([1.0, 0.0, 0.0]), 5.0)
    assert laws_t["rotation_angle"] == pytest.approx(0.0, abs=TIGHT)
    # law (1): doubling the path doubles the rotation
    laws_2L = establish_rotation_laws(V, B, np.array([0.0, 3.0, 4.0]), 10.0)
    assert laws_2L["rotation_angle"] == pytest.approx(
        2.0 * laws["rotation_angle"], rel=TIGHT
    )
    # consistency with FaradayRotator for a field-aligned ray
    rotator = FaradayRotator(verdet_constant=V, path_length=5.0)
    aligned = establish_rotation_laws(V, B, np.array([0.0, 0.0, 1.0]), 5.0)
    assert aligned["rotation_angle"] == pytest.approx(
        rotator.rotation_angle(1000.0), rel=TIGHT
    )


# ── Art. 809 — Verdet's sign rule and the Verdet table ─────────────────────


@pytest.mark.article(809)
def test_art809_ferromagnetic_rotation_is_negative_of_diamagnetic():
    """Art. 809: ferromagnetic media give the negative rotation (opposite
    to the current that would produce the field); diamagnetic the positive.
    """
    V, B, L = 2.0e-4, 500.0, 4.0
    dia = apply_verdet_negative_rotation(V, B, L, "diamagnetic")
    ferro = apply_verdet_negative_rotation(V, B, L, "ferromagnetic")
    assert dia == pytest.approx(V * B * L, rel=TIGHT)
    assert ferro == pytest.approx(-V * B * L, rel=TIGHT)
    assert ferro + dia == pytest.approx(0.0, abs=TIGHT)
    # the rule acts on the magnitude: a negative input still yields -|V|
    ferro_neg = apply_verdet_negative_rotation(-V, B, L, "ferromagnetic")
    assert ferro_neg == pytest.approx(ferro, rel=TIGHT)


@pytest.mark.article(809)
def test_art809_verdet_table_units_and_ratios():
    """Art. 809: Verdet table carries min/(gauss cm); radian accessor
    applies the exact factor pi/10800; ratios are unit-independent.
    """
    table = VerdetTable()
    # EMPIRICAL: classical table values (min/(G cm)) at the sodium D line
    assert table.get_verdet("water") == pytest.approx(0.0131, rel=TIGHT)
    assert table.get_verdet("carbon_disulfide") == pytest.approx(0.0424, rel=TIGHT)
    assert table.get_verdet_rad("water") == pytest.approx(
        0.0131 * math.pi / 10800.0, rel=TIGHT
    )
    ratio = table.compare_materials("carbon_disulfide", "water")
    assert ratio == pytest.approx(0.0424 / 0.0131, rel=TIGHT)
    # unit independence: the same ratio from the radian values
    ratio_rad = table.get_verdet_rad("carbon_disulfide") / table.get_verdet_rad("water")
    assert ratio_rad == pytest.approx(ratio, rel=TIGHT)


# ── Art. 810 — natural rotation, Biot's law, round trip ────────────────────


@pytest.mark.article(810)
def test_art810_biot_law_and_round_trip_reciprocity():
    """Art. 810: natural rotation obeys Biot's law theta ~ 1/lambda^2 and is
    exactly undone on reflection, whereas magnetic rotation doubles.
    """
    alpha, L, lam = 1.0e-9, 5.0, 5.0e-5
    theta = model_natural_rotation(alpha, L, lam)
    assert theta == pytest.approx(alpha * L / lam**2, rel=TIGHT)
    # Biot: doubling the wavelength quarters the rotation
    assert model_natural_rotation(alpha, L, 2.0 * lam) == pytest.approx(
        theta / 4.0, rel=TIGHT
    )
    # natural (reciprocal) round trip cancels; magnetic doubles
    assert round_trip_rotation(theta, magnetic=False) == pytest.approx(0.0, abs=TIGHT)
    assert round_trip_rotation(theta, magnetic=True) == pytest.approx(
        2.0 * theta, rel=TIGHT
    )
    # cross-check with the Faraday rotator
    rotator = FaradayRotator(verdet_constant=2.0e-4, path_length=10.0)
    theta_F = rotator.rotation_angle(1000.0)
    assert round_trip_rotation(theta_F, magnetic=True) == pytest.approx(
        2.0 * 2.0e-4 * 1000.0 * 10.0, rel=TIGHT
    )


# ── Art. 811 — rotation is half the phase difference ───────────────────────


@pytest.mark.article(811)
def test_art811_rotation_is_half_phase_difference():
    """Art. 811: the plane of polarization turns through HALF the phase
    difference accumulated by the two circular components.
    """
    omega, k_r, k_l = 1.0e15, 2.0e5 * 1.002, 2.0e5 * 0.998
    ka = perform_kinematic_analysis(omega, k_r, k_l)
    assert ka["phase_diff_per_length"] == pytest.approx(k_r - k_l, rel=TIGHT)
    assert ka["rotation_per_length"] == pytest.approx((k_r - k_l) / 2.0, rel=TIGHT)
    assert ka["v_right"] == pytest.approx(omega / k_r, rel=TIGHT)
    assert ka["v_left"] == pytest.approx(omega / k_l, rel=TIGHT)
    # over a path L the rotation is half the total phase difference
    L = 7.5
    assert ka["rotation_per_length"] * L == pytest.approx(
        (k_r - k_l) * L / 2.0, rel=TIGHT
    )


# ── Art. 812 — Delta n = V B lambda / pi (D-04: no factor 2) ────────────────


@pytest.mark.article(812)
@pytest.mark.article(811)
def test_art812_index_split_and_closed_loop_with_811():
    """Art. 812: from theta = V B L = (k_R - k_L) L / 2 one obtains
    Delta n = V B lambda / pi and Delta v = c Delta n / n^2.  Closed loop
    with Art. 811: rebuilding the wave numbers from n +- Delta n/2 must
    give rotation per length exactly V B.
    """
    n, B, V, lam = 1.5, 1000.0, 0.1, 5.893e-5
    dv = calc_circular_velocity_split(n, B, V, lam)
    assert dv == pytest.approx(CONST.C * V * B * lam / math.pi / n**2, rel=TIGHT)
    # closed loop: k = n omega / c, omega = 2 pi c / lambda
    delta_n = V * B * lam / math.pi
    omega = 2.0 * math.pi * CONST.C / lam
    k_r = (n + delta_n / 2.0) * omega / CONST.C
    k_l = (n - delta_n / 2.0) * omega / CONST.C
    ka = perform_kinematic_analysis(omega, k_r, k_l)
    assert ka["rotation_per_length"] == pytest.approx(V * B, rel=STANDARD)


# ── Art. 813 — the circular ray: tip of the vector traces a circle ─────────


@pytest.mark.article(813)
def test_art813_circular_ray_constant_magnitude_transverse():
    """Art. 813: the disturbance vector of a circularly polarized ray
    rotates at constant magnitude (its tip describes a circle), stays
    perpendicular to the ray, and a quarter period turns it by 90 deg.
    The left-handed ray is the mirror image diag(1,-1,1) of the right.
    """
    A, omega, k = 2.5, 1.0e15, 2.0e5
    right = CircularlyPolarizedRay(
        amplitude=np.array([A, 0.0, 0.0]),
        omega=omega,
        k=k,
        handedness="right",
        propagation_axis=np.array([0.0, 0.0, 1.0]),
    )
    left = CircularlyPolarizedRay(
        amplitude=np.array([A, 0.0, 0.0]),
        omega=omega,
        k=k,
        handedness="left",
        propagation_axis=np.array([0.0, 0.0, 1.0]),
    )
    zhat = np.array([0.0, 0.0, 1.0])
    for z, t in [(0.0, 0.0), (1.3e-4, 2.1e-15), (7.0e-5, 5.5e-16)]:
        E_r = right.electric_field(z, t)
        E_l = left.electric_field(z, t)
        # constant magnitude = radius of the circle
        assert np.linalg.norm(E_r) == pytest.approx(A, rel=STANDARD)
        assert np.linalg.norm(E_l) == pytest.approx(A, rel=STANDARD)
        # transverse to the ray
        assert float(np.dot(E_r, zhat)) == pytest.approx(0.0, abs=STANDARD)
        # mirror relation: left = diag(1, -1, 1) right
        assert E_l == pytest.approx(np.array([E_r[0], -E_r[1], E_r[2]]), abs=STANDARD)
    # a quarter period turns the vector through 90 deg
    E0 = right.electric_field(0.0, 0.0)
    E_quarter = right.electric_field(0.0, (2.0 * math.pi / omega) / 4.0)
    assert float(np.dot(E0, E_quarter)) == pytest.approx(0.0, abs=STANDARD)


# ── Art. 814 — natural velocity split ───────────────────────────────────────


@pytest.mark.article(814)
def test_art814_natural_split_delta_v_formula():
    """Art. 814: with rotation per length rho = (k_R - k_L)/2, the split is
    Delta v = 2 v^2 rho / omega about v_avg = c/n.
    """
    n, rho, lam = 1.55, 1.0e-3, 5.0e-5
    res = calc_natural_velocity_split(n, rho, lam)
    v_avg = CONST.C / n
    omega = 2.0 * math.pi * CONST.C / lam
    delta_v = 2.0 * v_avg**2 * rho / omega
    assert res["delta_v"] == pytest.approx(delta_v, rel=TIGHT)
    # float64 cancellation in (v_avg + d/2) - (v_avg - d/2): STANDARD class
    assert res["v_right"] - res["v_left"] == pytest.approx(delta_v, rel=STANDARD)
    assert (res["v_right"] + res["v_left"]) / 2.0 == pytest.approx(v_avg, rel=TIGHT)


# ── Art. 815 — magnetic split matches Art. 812 ─────────────────────────────


@pytest.mark.article(815)
@pytest.mark.article(812)
def test_art815_magnetic_split_consistent_with_art812():
    """Art. 815: Delta k = 2 V B gives Delta v = v^2 Delta k / omega, which
    must equal the Art. 812 result c V B lambda / (pi n^2).
    """
    n, B, V, lam = 1.7, 800.0, 4.0e-5, 4.861e-5
    res = calc_magnetic_velocity_split(n, B, V, lam)
    dv812 = calc_circular_velocity_split(n, B, V, lam)
    assert res["delta_v"] == pytest.approx(dv812, rel=STANDARD)
    assert res["delta_v"] == pytest.approx(
        CONST.C * V * B * lam / math.pi / n**2, rel=STANDARD
    )


# ── Art. 816 — the disturbance is a transverse vector ──────────────────────


@pytest.mark.article(816)
def test_art816_light_vector_is_transverse_projection():
    """Art. 816: the luminiferous disturbance is a vector perpendicular to
    the ray; the light vector is the disturbance with its longitudinal
    part removed.
    """
    ray = np.array([0.0, 0.0, 2.0])  # need not be unit
    d = np.array([1.0, 2.0, 3.0])
    lv = define_light_vector(d, ray)
    # hand oracle: remove the z component -> (1, 2, 0)
    assert lv == pytest.approx(np.array([1.0, 2.0, 0.0]), abs=TIGHT)
    # perpendicularity to machine precision for an oblique ray
    ray_ob = np.array([1.0, 1.0, 1.0])
    lv_ob = define_light_vector(d, ray_ob)
    assert float(np.dot(lv_ob, ray_ob)) == pytest.approx(0.0, abs=STANDARD)
    # a purely transverse disturbance passes through unchanged
    d_trans = np.array([1.0, -1.0, 0.0])
    assert define_light_vector(d_trans, ray) == pytest.approx(d_trans, abs=TIGHT)


# ── Art. 817 — equations of the circular ray ────────────────────────────────


@pytest.mark.article(817)
def test_art817_kinematics_equations_and_conventions():
    """Art. 817 eqs. (1)-(4): xi = r cos(nt - qz + a), eta = r sin(...),
    n tau = 2 pi, q lambda = 2 pi, velocity = n/q; handedness by the sign
    of q (q < 0 right-handed), propagation sense by the relative signs of
    n and q.
    """
    n, q, r, a, z, t = 6.0, -2.0, 1.5, 0.3, 0.7, 1.1
    kin = derive_circular_kinematics(n, q, r, phase=a, z=z, t=t)
    theta = n * t - q * z + a
    assert kin["theta"] == pytest.approx(theta, rel=TIGHT)
    assert kin["xi"] == pytest.approx(r * math.cos(theta), rel=TIGHT)
    assert kin["eta"] == pytest.approx(r * math.sin(theta), rel=TIGHT)
    # eq. (1): the tip lies on the circle of radius r
    assert kin["xi"] ** 2 + kin["eta"] ** 2 == pytest.approx(r**2, rel=TIGHT)
    assert kin["radius"] == pytest.approx(r, rel=TIGHT)
    # eqs. (3)-(4) and the velocity n/q
    assert kin["period"] * n == pytest.approx(2.0 * math.pi, rel=TIGHT)
    assert kin["wavelength"] * abs(q) == pytest.approx(2.0 * math.pi, rel=TIGHT)
    assert kin["velocity"] == pytest.approx(n / q, rel=TIGHT)
    # conventions: q < 0 right-handed; opposite signs -> negative z
    assert kin["handedness"] == "right"
    assert kin["propagation_direction"] == -1
    kin_left = derive_circular_kinematics(n, +abs(q), r)
    assert kin_left["handedness"] == "left"
    assert kin_left["propagation_direction"] == 1
    # degenerate inputs are rejected (period / velocity undefined)
    with pytest.raises(ValueError):
        derive_circular_kinematics(0.0, q, r)
    with pytest.raises(ValueError):
        derive_circular_kinematics(n, 0.0, r)


# ── Art. 818 — potential (electric) vs kinetic (magnetic) energy ───────────


@pytest.mark.article(818)
def test_art818_energy_labels_potential_electric_kinetic_magnetic():
    """Art. 818: potential energy depends on configuration (electric
    displacement), kinetic energy is quadratic in the velocities (magnetic
    disturbance).  Golden (hand arithmetic): eps = mu = 1, volume = 8 pi,
    unit amplitudes -> energies exactly 1.0.
    """
    medium = MagnetoOpticMedium(permittivity=1.0, permeability=1.0, verdet_constant=0.0)
    vol = 8.0 * math.pi
    E_case = medium.calc_medium_energy(np.array([1.0, 0.0, 0.0]), np.zeros(3), vol)
    assert E_case["electric_energy"] == pytest.approx(1.0, rel=TIGHT)
    assert E_case["potential_energy"] == pytest.approx(1.0, rel=TIGHT)
    assert E_case["magnetic_energy"] == pytest.approx(0.0, abs=TIGHT)
    assert E_case["kinetic_energy"] == pytest.approx(0.0, abs=TIGHT)
    assert E_case["total_energy"] == pytest.approx(1.0, rel=TIGHT)
    B_case = medium.calc_medium_energy(np.zeros(3), np.array([0.0, 1.0, 0.0]), vol)
    assert B_case["kinetic_energy"] == pytest.approx(1.0, rel=TIGHT)
    assert B_case["magnetic_energy"] == pytest.approx(1.0, rel=TIGHT)
    assert B_case["potential_energy"] == pytest.approx(0.0, abs=TIGHT)
    # ratio: potential/kinetic, inf when kinetic vanishes
    assert E_case["potential_to_kinetic_ratio"] == float("inf")
    mixed = medium.calc_medium_energy(
        np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), vol
    )
    assert mixed["potential_to_kinetic_ratio"] == pytest.approx(1.0, rel=TIGHT)


# ── Art. 819 — the propagation quadratic and equation (8) ──────────────────


@pytest.mark.article(819)
def test_art819_quadratic_roots_and_coupling_eq8():
    """Art. 819 eqs. (7)-(8): A n^2 + B n + C = 0 with
    A(n_1 + n_2) + B = 0.  Golden (hand arithmetic):
    2 n^2 - 4 n - 6 = 0 -> disc = 64, roots {3, -1}.
    """
    res = calc_propagation_quadratic(2.0, -4.0, -6.0)
    assert res["discriminant"] == pytest.approx(
        ref_value(819, "quadratic_discriminant"),
        **tolerance_of(819, "quadratic_discriminant"),
    )
    assert res["n1"] == pytest.approx(
        ref_value(819, "quadratic_root_large"),
        **tolerance_of(819, "quadratic_root_large"),
    )
    assert res["n2"] == pytest.approx(
        ref_value(819, "quadratic_root_small"),
        **tolerance_of(819, "quadratic_root_small"),
    )
    assert res["sum_roots"] == pytest.approx(
        ref_value(819, "quadratic_sum_roots"),
        **tolerance_of(819, "quadratic_sum_roots"),
    )
    assert res["product_roots"] == pytest.approx(
        ref_value(819, "quadratic_product_roots"),
        **tolerance_of(819, "quadratic_product_roots"),
    )
    # eq. (8): B = -A(n_1 + n_2) recovers the coupling coefficient
    B = quadratic_coupling_coefficient(2.0, res["n1"], res["n2"])
    assert B == pytest.approx(-4.0, rel=TIGHT)
    with pytest.raises(ValueError):
        calc_propagation_quadratic(0.0, 1.0, 1.0)


@pytest.mark.article(819)
def test_art819_medium_propagation_condition_and_split():
    """Art. 819: v_phase = c/sqrt(eps mu); in the magnetic force the two
    circular components split by Delta n = V B lambda / pi with
    Delta v = v^2 (2 V B)/omega, consistent with Arts. 812/815.
    """
    eps, mu, V = 4.0, 1.0, 5.0e-5
    medium = MagnetoOpticMedium(eps, mu, V)
    B, lam = 1000.0, 5.0e-5
    res = medium.derive_propagation_condition(magnetic_field=B, wavelength=lam)
    n = math.sqrt(eps * mu)
    assert res["refractive_index"] == pytest.approx(n, rel=TIGHT)
    assert res["v_phase"] == pytest.approx(CONST.C / n, rel=TIGHT)
    assert res["delta_n"] == pytest.approx(V * B * lam / math.pi, rel=TIGHT)
    omega = 2.0 * math.pi * CONST.C / lam
    dv = (CONST.C / n) ** 2 * (2.0 * V * B) / omega
    assert res["velocity_split"] == pytest.approx(dv, rel=TIGHT)
    # float64 cancellation in (v_avg + d/2) - (v_avg - d/2): STANDARD class
    assert res["v_right"] - res["v_left"] == pytest.approx(dv, rel=STANDARD)
    # no wavelength -> no split
    res0 = medium.derive_propagation_condition(magnetic_field=B)
    assert res0["delta_n"] == pytest.approx(0.0, abs=TIGHT)
    assert res0["v_right"] == pytest.approx(res0["v_phase"], rel=TIGHT)


# ── Art. 820 — a real rotation is required (D-06) ───────────────────────────


@pytest.mark.article(820)
def test_art820_round_trip_discriminant_detects_real_rotation():
    """Art. 820: the magnetic round trip is 2 theta while the reciprocal
    (natural) round trip is 0; a nonzero discriminant forces a real
    angular velocity in the medium (the B n term of the kinetic energy).
    """
    res = prove_real_rotation_required(0.1)
    assert res["faraday_round_trip"] == pytest.approx(0.2, rel=TIGHT)
    assert res["natural_round_trip"] == pytest.approx(0.0, abs=TIGHT)
    assert res["discriminant"] == pytest.approx(0.2, rel=TIGHT)
    assert res["requires_real_rotation"] is True
    # zero rotation: no discriminant, nothing to explain
    res0 = prove_real_rotation_required(0.0)
    assert res0["discriminant"] == pytest.approx(0.0, abs=TIGHT)
    assert res0["requires_real_rotation"] is False
    # property: discriminant = 2 theta for any theta
    for theta in [1e-6, -0.3, 2.7]:
        r = prove_real_rotation_required(theta)
        assert r["discriminant"] == pytest.approx(2.0 * theta, rel=TIGHT)


# ── Art. 821 — computed summary of the magneto-optic results (D-07) ────────


@pytest.mark.article(821)
def test_art821_summary_is_fully_derived_and_consistent():
    """Art. 821: every summary entry is derived from the inputs and matches
    the dedicated Arts. 812/815 machinery.
    """
    eps, mu, V, B, lam, L = 4.0, 1.0, 5.0e-5, 1000.0, 5.0e-5, 10.0
    summary = summarize_magneto_optic_results(eps, mu, V, B, lam, L)
    n = math.sqrt(eps * mu)
    assert summary["refractive_index"] == pytest.approx(n, rel=TIGHT)
    assert summary["v_phase"] == pytest.approx(CONST.C / n, rel=TIGHT)
    assert summary["delta_n"] == pytest.approx(V * B * lam / math.pi, rel=TIGHT)
    assert summary["rotation_per_length"] == pytest.approx(V * B, rel=TIGHT)
    assert summary["total_rotation"] == pytest.approx(V * B * L, rel=TIGHT)
    omega = 2.0 * math.pi * CONST.C / lam
    dv = (CONST.C / n) ** 2 * (2.0 * V * B) / omega
    assert summary["velocity_split"] == pytest.approx(dv, rel=TIGHT)
    assert summary["non_reciprocity_residual"] == pytest.approx(
        2.0 * V * B * L, rel=TIGHT
    )
    # cross-consistency with the Art. 815 split
    split = calc_magnetic_velocity_split(n, B, V, lam)
    assert summary["velocity_split"] == pytest.approx(split["delta_v"], rel=TIGHT)
    # every entry numeric (no prose results)
    for value in summary.values():
        assert isinstance(value, float)


# ── Art. 822 — mechanics of a molecular vortex ─────────────────────────────


@pytest.mark.article(822)
def test_art822_vortex_energy_momentum_and_gear_condition():
    """Art. 822: T = (pi/4) rho omega^2 r^4, L = (pi/2) rho r^4 omega,
    T = (1/2)|L| omega; the gear condition requires alternating rotation.

    Golden (hand arithmetic): rho=2, omega=3, r=1/2 ->
    T = (pi/4)*2*9*(1/16) = 0.28125 pi;  |L| = (pi/2)*2*(1/16)*3 = 0.1875 pi.
    """
    v = MolecularVortex(angular_velocity=3.0, density=2.0, radius=0.5)
    assert v.kinetic_energy() == pytest.approx(
        ref_value(822, "vortex_kinetic_energy_golden"),
        **tolerance_of(822, "vortex_kinetic_energy_golden"),
    )
    L = v.angular_momentum()
    assert float(np.linalg.norm(L)) == pytest.approx(
        ref_value(822, "vortex_angular_momentum_golden"),
        **tolerance_of(822, "vortex_angular_momentum_golden"),
    )
    assert v.kinetic_energy() == pytest.approx(
        0.5 * float(np.linalg.norm(L)) * 3.0, rel=TIGHT
    )
    # model magnetic quantity: (1/2) rho omega r^2, proportional to omega
    assert v.magnetic_field_equivalent() == pytest.approx(0.75, rel=TIGHT)
    v2 = MolecularVortex(angular_velocity=6.0, density=2.0, radius=0.5)
    assert v2.magnetic_field_equivalent() == pytest.approx(
        2.0 * v.magnetic_field_equivalent(), rel=TIGHT
    )
    # gear condition: alternating True, same sign False, zero not a gear,
    # fewer than two vortices undefined (ValueError)
    lattice = VortexLattice()
    for w in (1.0, -1.0, 1.0):
        lattice.add_vortex(MolecularVortex(w, 1.0, 1.0))
    assert lattice.verify_vortex_gear_condition() is True
    bad = VortexLattice()
    bad.add_vortex(MolecularVortex(1.0, 1.0, 1.0))
    bad.add_vortex(MolecularVortex(1.0, 1.0, 1.0))
    assert bad.verify_vortex_gear_condition() is False
    zero = VortexLattice()
    zero.add_vortex(MolecularVortex(1.0, 1.0, 1.0))
    zero.add_vortex(MolecularVortex(0.0, 1.0, 1.0))
    assert zero.verify_vortex_gear_condition() is False
    with pytest.raises(ValueError):
        VortexLattice().verify_vortex_gear_condition()


# ── Art. 823 — Helmholtz's law of vortex variation ─────────────────────────


@pytest.mark.article(823)
def test_art823_helmholtz_variation_and_strength_ratio():
    """Art. 823 eqs. (1)-(2): the angular velocity transforms by the
    deformation gradient I + J, and the strength varies as |P'Q'|/|PQ|,
    the stretch of the vortex axis.
    """
    omega = np.array([1.0, 2.0, 3.0])
    J = np.diag([0.5, 0.1, 0.2])
    omega_prime = apply_helmholtz_vortex_law(omega, J)
    assert omega_prime == pytest.approx(np.array([1.5, 2.2, 3.6]), rel=TIGHT)
    # no distortion -> unchanged
    assert apply_helmholtz_vortex_law(omega, np.zeros((3, 3))) == pytest.approx(
        omega, rel=TIGHT
    )
    # stretch factor of the z axis under J is 1.2
    stretch = calc_vortex_stretching(np.array([0.0, 0.0, 5.0]), J)
    assert stretch == pytest.approx(1.2, rel=TIGHT)
    # strength ratio s'/s equals the axis stretch for an axial vortex
    omega_axial = np.array([0.0, 0.0, 5.0])
    ratio = np.linalg.norm(apply_helmholtz_vortex_law(omega_axial, J)) / np.linalg.norm(
        omega_axial
    )
    assert ratio == pytest.approx(stretch, rel=TIGHT)
    # isotropic compression by 10% shrinks every axis by 0.9
    assert calc_vortex_stretching(
        np.array([1.0, 1.0, 0.0]), -0.1 * np.eye(3)
    ) == pytest.approx(0.9, rel=TIGHT)
    with pytest.raises(ValueError):
        calc_vortex_stretching(np.zeros(3), J)


# ── Arts. 824-825 — angular velocity of the element, coupling terms ────────


@pytest.mark.article(824)
def test_art824_angular_velocity_is_half_curl_and_coupling_term():
    """Art. 824 eqs. (2)-(3): omega = (1/2) curl v (rigid rotation
    recovers the rigid angular velocity), and the kinetic energy contains
    2 C (H . omega).
    """
    Omega = 7.0
    # rigid rotation v = Omega x r about z: gradient [[0,-O,0],[O,0,0],[0,0,0]]
    L = np.array([[0.0, -Omega, 0.0], [Omega, 0.0, 0.0], [0.0, 0.0, 0.0]])
    omega = calc_vortex_angular_velocity(L)
    assert omega == pytest.approx(np.array([0.0, 0.0, Omega]), rel=TIGHT)
    # irrotational strain carries no angular velocity
    assert calc_vortex_angular_velocity(np.diag([1.0, 2.0, 3.0])) == pytest.approx(
        np.zeros(3), abs=TIGHT
    )
    # eq. (3): 2 C (alpha omega_1 + beta omega_2 + gamma omega_3)
    H = np.array([0.0, 0.0, 0.4])
    w = np.array([0.0, 0.0, Omega])
    C = 1.5
    assert calc_disturbed_vortex_energy(H, w, C) == pytest.approx(
        2.0 * C * 0.4 * Omega, rel=TIGHT
    )


@pytest.mark.article(825)
def test_art825_coupling_in_terms_of_current_and_velocity():
    """Art. 825 eq. (5): 4 pi C (xi-dot u + eta-dot v + zeta-dot w).

    Golden (hand arithmetic): v=(1,2,3), J=(4,5,6) -> v.J = 32 -> 128 pi C.
    """
    v = np.array([1.0, 2.0, 3.0])
    J = np.array([4.0, 5.0, 6.0])
    C = 0.25
    assert express_vortex_current_velocity(v, J, C) == pytest.approx(
        4.0 * math.pi * C * 32.0, rel=TIGHT
    )


# ── Art. 826 — plane-wave kinetic energy, identity with Art. 828 ───────────


@pytest.mark.article(826)
@pytest.mark.article(828)
def test_art826_plane_wave_energy_reduces_to_art828_eq15():
    """Art. 826 eq. (9): T = (1/2) rho |v|^2 + C gamma (xi'' eta-dot -
    eta'' xi-dot).  Identity (hand-derived): substituting the circular ray
    xi = r cos(nt-qz), eta = r sin(nt-qz) at z=t=0 gives exactly the
    Art. 828 eq. (15) value (1/2) rho r^2 n^2 - C gamma r^2 q^2 n.
    """
    rho, C, gamma = 1.1, 0.7, 0.4
    # direct numerical case (hand arithmetic):
    # 0.5*2*(9+16) + 0.5*0.1*(7*4 - 11*3) = 25 + 0.05*(28-33) = 24.75
    T = calc_plane_wave_vortex_energy(
        2.0, 0.5, 0.1, np.array([3.0, 4.0, 0.0]), np.array([7.0, 11.0, 0.0])
    )
    assert T == pytest.approx(
        ref_value(826, "plane_wave_energy_hand_case"),
        **tolerance_of(826, "plane_wave_energy_hand_case"),
    )
    # identity with eq. (15) on the circular ray at z = t = 0
    r, n, q = 2.0, 5.0, 3.0
    velocity = np.array([0.0, r * n, 0.0])  # (xi-dot, eta-dot, 0)
    curvature = np.array([-r * q**2, 0.0, 0.0])  # (xi'', eta'', 0)
    T_wave = calc_plane_wave_vortex_energy(rho, C, gamma, velocity, curvature)
    assert T_wave == pytest.approx(
        0.5 * rho * r**2 * n**2 - C * gamma * r**2 * q**2 * n, rel=TIGHT
    )


# ── Arts. 827-828 — equations of motion and circular velocities ────────────


@pytest.mark.article(827)
def test_art827_equation_of_motion_residual_vanishes_at_roots():
    """Art. 827 eqs. (10)-(13): for the circular ray, the inertial
    coefficient rho n^2 - 2 C gamma q^2 n must balance the Cauchy elastic
    coefficient Q = A_0 q^2 - A_1 q^4; the residual vanishes exactly at
    the roots of Art. 828 eq. (18).
    """
    eq = VortexEquations(
        ether_density=1.0,
        elastic_constant=4.0,
        coupling_constant=0.5,
        magnetic_force=0.2,
        elastic_higher=0.0,
    )
    q = 0.3
    roots = eq.solve_plane_wave(q)
    Q = 4.0 * q**2  # A0 q^2 with A1 = 0
    assert roots["Q"] == pytest.approx(Q, rel=TIGHT)
    for n in (roots["n_plus"], roots["n_minus"]):
        res = eq.derive_vortex_equations_of_motion(n, q)
        assert res["residual"] == pytest.approx(0.0, abs=NUMERIC)
        assert res["force_inertial_coefficient"] == pytest.approx(
            res["force_elastic_coefficient"], rel=NUMERIC
        )
    # off-shell: residual is nonzero and equals inertial - elastic
    res_off = eq.derive_vortex_equations_of_motion(1.234, q)
    assert res_off["residual"] == pytest.approx(
        1.234**2 - 2.0 * 0.5 * 0.2 * q**2 * 1.234 - Q, rel=TIGHT
    )
    with pytest.raises(ValueError):
        VortexEquations(ether_density=0.0, elastic_constant=1.0).solve_plane_wave(q)


@pytest.mark.article(828)
def test_art828_circular_velocities_and_vieta_identities():
    """Art. 828: the two roots n+- of eq. (18) give the velocities n/q of
    the two circular components; Vieta: n+ + n- = 2 C gamma q^2 / rho and
    n+ n- = -Q/rho (the product is fixed by the elasticity alone).
    """
    q, rho, A0, C, gamma = 0.3, 1.0, 4.0, 0.5, 0.2
    res = calc_vortex_circular_velocity(q, rho, A0, C, gamma)
    Q = A0 * q**2
    assert res["v_plus"] == pytest.approx(res["n_plus"] / q, rel=TIGHT)
    assert res["v_minus"] == pytest.approx(res["n_minus"] / q, rel=TIGHT)
    assert res["velocity_split"] == pytest.approx(
        (res["n_plus"] - res["n_minus"]) / q, rel=TIGHT
    )
    assert res["n_plus"] + res["n_minus"] == pytest.approx(res["sum_roots"], rel=TIGHT)
    assert res["sum_roots"] == pytest.approx(2.0 * C * gamma * q**2 / rho, rel=TIGHT)
    assert res["n_plus"] * res["n_minus"] == pytest.approx(
        res["product_roots"], rel=STANDARD
    )
    assert res["product_roots"] == pytest.approx(-Q / rho, rel=TIGHT)
    # gamma = 0: no splitting, the two roots are opposite
    res0 = calc_vortex_circular_velocity(q, rho, A0, C, 0.0)
    assert res0["n_plus"] == pytest.approx(-res0["n_minus"], rel=TIGHT)
    assert res0["sum_roots"] == pytest.approx(0.0, abs=TIGHT)
    with pytest.raises(ValueError):
        calc_vortex_circular_velocity(0.0, rho, A0, C, gamma)


# ── Arts. 829-830 — rotation formula and Verdet's data ─────────────────────


@pytest.mark.article(829)
def test_art829_rotation_formula_eq26_and_denominator():
    """Art. 829 eqs. (25)-(26): theta = m c gamma (i^2/lambda^2)
    (i - lambda di/dlambda) with m = 4 pi^2 C / (v rho); the exact eq. (24)
    multiplies by 1/(1 - 2 pi C gamma i^2 / (v rho lambda)).
    """
    C, rho, L, gamma, i, lam = 1.0e-8, 1.0, 10.0, 1000.0, 1.63, 5.893e-5
    slope = -1.0e4
    m = 4.0 * math.pi**2 * C / (CONST.C * rho)
    assert rotation_coefficient(C, rho) == pytest.approx(m, rel=TIGHT)
    expected = m * L * gamma * (i**2 / lam**2) * (i - lam * slope)
    theta = derive_magnetic_rotation(C, rho, L, gamma, i, lam, dispersion_slope=slope)
    assert theta == pytest.approx(expected, rel=TIGHT)
    # no dispersion slope: the (i - lambda di/dlambda) factor is just i
    theta0 = derive_magnetic_rotation(C, rho, L, gamma, i, lam)
    assert theta0 == pytest.approx(m * L * gamma * i**3 / lam**2, rel=TIGHT)
    # denominator correction: ratio is 1/(1 - 2 pi C gamma i^2/(v rho lam))
    theta_corr = derive_magnetic_rotation(
        C, rho, L, gamma, i, lam, include_denominator_correction=True
    )
    denom = 1.0 - 2.0 * math.pi * C * gamma * i**2 / (CONST.C * rho * lam)
    assert theta_corr / theta0 == pytest.approx(1.0 / denom, rel=TIGHT)
    # gamma -> 0: the rotation vanishes (both forms)
    assert derive_magnetic_rotation(C, rho, L, 0.0, i, lam) == pytest.approx(
        0.0, abs=TIGHT
    )


@pytest.mark.article(830)
def test_art830_verdet_table_golden_and_laws():
    """Art. 830: Verdet's bisulphide-of-carbon table (Maxwell 1873, Vol. II,
    p. 468).  Golden: rotation of ray E is 25 deg 28 min (EMPIRICAL,
    historical measurement); the observed column is normalized to E=1000.
    """
    data = VERDET_CS2_DATA
    assert data["rotation_of_E"] == pytest.approx(
        ref_value(830, "verdet_E_rotation_deg"),
        **tolerance_of(830, "verdet_E_rotation_deg"),
    )
    assert data["observed_rotation"]["E"] == pytest.approx(1000.0, rel=TIGHT)
    # EMPIRICAL: Verdet's own observed values (p. 468), from the store
    for line in ("C", "D", "F", "G"):
        value = ref_value(830, f"verdet_observed_{line}")
        assert data["observed_rotation"][line] == pytest.approx(
            value, **tolerance_of(830, f"verdet_observed_{line}")
        )
    # formula (I) values of Art. 830 (which is Art. 829 eq. (26))
    for line, value in [("C", 589), ("D", 760), ("E", 1000), ("F", 1234), ("G", 1713)]:
        assert data["calculated_formula_1"][line] == pytest.approx(value, rel=TIGHT)
    # formula (I) tracks Verdet's observations to ~1% (Treatise: "the
    # agreement is somewhat close for bisulphide of carbon")
    for line in data["observed_rotation"]:
        comp = compare_verdet_data(
            data["calculated_formula_1"][line],
            data["observed_rotation"][line],
            tolerance=0.02,
        )
        assert comp["agrees"] is True
    # comparator verdict flips outside tolerance
    assert compare_verdet_data(1000.0, 1234.0, tolerance=0.1)["agrees"] is False


@pytest.mark.article(830)
def test_art830_inverse_square_laws_from_verdet_data():
    """Art. 830, Verdet's results: (1) rotations follow approximately the
    inverse square of the wave-length; (2) theta lambda^2 increases from
    the least refrangible (C) to the most refrangible (G) end.

    Independent LSQ oracle (normal equation of theta = k/lambda^2,
    implemented in the test, not re-used from the module).
    """
    data = VERDET_CS2_DATA
    lines = ["C", "D", "E", "F", "G"]
    lam = np.array([data["wavelengths_cm"][ln] for ln in lines])
    theta = np.array([data["observed_rotation"][ln] for ln in lines])
    res = verdet_inverse_square_analysis(lam, theta)
    # law (2): theta lambda^2 strictly increases C -> G (hand-verified:
    # 592*6.563^2 = 25499.2, 768*5.893^2 = 26670.7, 1000*5.270^2 = 27772.9,
    # 1234*4.861^2 = 29158.6, 1704*4.308^2 = 31624.3; units 1e-10 cm^2)
    assert res["monotonic_increase"] is True
    tls = res["theta_lambda_squared"]
    assert list(np.round(tls / 1e-10)) == [25499.0, 26671.0, 27773.0, 29159.0, 31624.0]
    # law (1): independent least-squares cross-check, k = sum(theta x)/sum(x^2)
    x = [1.0 / l**2 for l in lam]
    k_oracle = sum(t * xi for t, xi in zip(theta, x)) / sum(xi * xi for xi in x)
    assert res["best_fit_k"] == pytest.approx(k_oracle, rel=STANDARD)
    frac = [(k_oracle * xi - t) / t for t, xi in zip(theta, x)]
    rms_oracle = math.sqrt(sum(f * f for f in frac) / len(frac))
    assert res["rms_fractional_residual"] == pytest.approx(rms_oracle, rel=STANDARD)
    assert res["obeys_inverse_square_within_threshold"] is True
    assert rms_oracle < 0.15  # "approximately" the inverse-square law


# ── Art. 831 — computed state of the mechanical theory ─────────────────────


@pytest.mark.article(831)
def test_art831_mechanical_theory_summary_computed():
    """Art. 831 (Note): the mechanical state of the vortex medium is
    reported numerically.  Golden (hand arithmetic): with the elastic
    constant calibrated to rho c^2, the wave speed equals c exactly; a
    gear pair of opposite rotations carries zero net field and zero net
    angular momentum; each vortex contributes (pi/4) rho omega^2 r^4
    = 0.28125 pi to the kinetic energy.
    """
    rho, omega, r = 2.0, 3.0, 0.5
    lattice = VortexLattice()
    lattice.add_vortex(MolecularVortex(omega, rho, r))
    lattice.add_vortex(MolecularVortex(-omega, rho, r))
    elastic = rho * CONST.C**2
    notes = append_mechanical_theory_notes(lattice, elastic)
    assert notes["vortex_count"] == 2
    assert notes["wave_speed"] == pytest.approx(CONST.C, rel=NUMERIC)
    assert notes["wave_speed_over_light"] == pytest.approx(1.0, rel=NUMERIC)
    assert notes["mean_density"] == pytest.approx(rho, rel=TIGHT)
    # gear pair: everything directional cancels, energies add
    assert notes["net_magnetic_field"] == pytest.approx(np.zeros(3), abs=TIGHT)
    assert notes["total_angular_momentum"] == pytest.approx(np.zeros(3), abs=TIGHT)
    assert notes["total_kinetic_energy"] == pytest.approx(
        2.0 * ref_value(822, "vortex_kinetic_energy_golden"),
        **tolerance_of(822, "vortex_kinetic_energy_golden"),
    )
    assert notes["gear_condition_satisfied"] is True
    # empty lattice and single-vortex lattice are undefined states
    with pytest.raises(ValueError):
        append_mechanical_theory_notes(VortexLattice(), elastic)
    single = VortexLattice()
    single.add_vortex(MolecularVortex(omega, rho, r))
    with pytest.raises(ValueError):
        append_mechanical_theory_notes(single, elastic)
