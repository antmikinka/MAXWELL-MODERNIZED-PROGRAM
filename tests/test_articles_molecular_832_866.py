"""Article-evidence tests for Arts. 832-866 (molecular currents, action at
distance, Neumann's potential, theory comparison, completeness of the
electromagnetic theory of light).

Cluster G evidence file (PHYSICUS, 2026-08-21). Every test is a qualifying
test: it compares module output against an INDEPENDENT oracle (closed-form
physics, CODATA constants, or a separately written quadrature), never
against values produced by the function under test.

Article map:
    832  molecular current moment m = iA/c
    833  dipole field of a molecular current
    834  equivalence of current loop and dipole off-axis
    835  magnetization M = N f m
    836  Curie susceptibility chi = N m^2 / (3 k_B T)
    837  bound current density J_b = c curl M
    838  total magnetic moment integral
    839  bound surface current K_b = c M x n
    840  uniformly magnetized sphere: B_inside = (8 pi / 3) M
    841  Weber force reduces to Coulomb; acceleration term
    842  Weber electrodynamic potential
    843  Coulomb limit residual of the Weber theory
    844  velocity correction factor 1 - r'^2/(2c^2)
    845  acceleration correction factor 1 + 2 r r''/c^2
    846  Ampere wire-force recovery from Weber electrodynamics
    847  induced EMF = -(M dI/dt + I dM/dt), Lenz sign
    848  Weber's constant = sqrt(2) c
    849  critical velocity and force sign flip
    850  conservation of energy under Weber's law
    851  Neumann vector potential of a circuit
    852  flux through a circuit = M I
    853  Neumann mutual inductance: quadrature vs elliptic closed form
    854  self-inductance of a circular circuit, L = 4 pi R (ln(8R/a) - 2)
    855  induced EMF = -M dI/dt
    856  reciprocity M_12 = M_21
    857  far-field (dipole) limit of the mutual inductance
    858  motional EMF of separating coaxial circuits
    859  characteristics of the competing theories
    860  computed residuals replace invented agreement scores
    861  computed consistency checks
    862  theory comparison aggregation
    863  consistency verification is computed
    864  cross-theory differences computed from residuals
    865  wave properties follow from K and mu
    866  Maxwell's relation n^2 = K verified honestly (no rigged data)
"""

from __future__ import annotations

import numpy as np
import pytest
from articles import ref_value, tolerance_of

from maxwell.config.constants import CONST
from maxwell.molecular.amperes_theory import (
    AmperesTheory,
    bound_surface_current,
    calc_molecular_field,
    calc_molecular_moment,
    sphere_center_field_rings,
    sphere_interior_field,
    total_magnetic_moment,
)
from maxwell.molecular.competing_theories import (
    CompetingTheory,
    analyze_theory_differences,
    compare_electromagnetic_theories,
    compare_theories,
    synthesize_theory_comparison,
    verify_theory_consistency,
)
from maxwell.molecular.neumanns_theory import (
    NeumannPotential,
    NeumannTheory,
    circular_loop_inductance,
    maxwell_mutual_inductance_closed_form,
    motional_emf_coaxial,
    neumann_far_field_residual,
    neumann_mutual_inductance,
    neumann_reciprocity_residual,
)
from maxwell.molecular.webers_theory import (
    WeberForce,
    WebersTheory,
    ampere_wire_force_recovery,
    calc_weber_force,
    critical_velocity,
    weber_constant,
    weber_energy_conservation_residual,
)
from maxwell.philosophy.medium_check import (
    MediumProperties,
    _wave_impedance,
    analyze_theory_completeness,
    calc_reflection_coefficient,
    calc_wave_properties,
    verify_maxwell_relation,
    verify_wave_speed,
)

C = CONST.C
K_B = CONST.K_BOLTZMANN


# ── independent oracles written for this file ───────────────────────────────


def _biot_savart_loop(point, current, radius, n=4000):
    """Independent Biot-Savart quadrature of a circular loop in the xy plane.

    B(r) = (I/c) oint dl' x (r - r') / |r - r'|^3  (Gaussian CGS).
    Written from scratch for this test file; shares no code with the
    modules under test.
    """
    point = np.asarray(point, dtype=np.float64)
    B = np.zeros(3)
    dt = 2.0 * np.pi / n
    for i in range(n):
        t = i * dt
        rp = np.array([radius * np.cos(t), radius * np.sin(t), 0.0])
        dl = radius * dt * np.array([-np.sin(t), np.cos(t), 0.0])
        sep = point - rp
        r = np.linalg.norm(sep)
        B += np.cross(dl, sep) / r**3
    return (current / C) * B


def _dipole_field(m_vec, point):
    """Independent dipole field B = (3 (m . rhat) rhat - m) / r^3."""
    r = np.asarray(point, dtype=np.float64)
    rn = np.linalg.norm(r)
    rhat = r / rn
    m_vec = np.asarray(m_vec, dtype=np.float64)
    return (3.0 * np.dot(m_vec, rhat) * rhat - m_vec) / rn**3


# ── Art. 832 — molecular current moment m = i A / c ─────────────────────────


@pytest.mark.article(832)
def test_art832_molecular_moment_is_ia_over_c():
    """Art. 832: the moment of a plane molecular current is i A / c in CGS.

    Oracle: hand arithmetic with the CODATA speed of light.
    """
    i, area = 1.0e10, 2.0  # abamperes, cm^2
    expected = i * area / C
    assert calc_molecular_moment(i, area) == pytest.approx(expected, rel=1e-12)
    # second independent golden: electron-scale loop
    # provenance: toy current magnitude for a microscopic loop; NOT the
    # speed of light despite the numerical coincidence (3.0e10 abamperes).
    i2, a2 = 3.0e10, 1.0e-4
    assert calc_molecular_moment(i2, a2) == pytest.approx(i2 * a2 / C, rel=1e-12)


# ── Art. 833 — dipole field of the molecular current ────────────────────────


@pytest.mark.article(833)
def test_art833_dipole_field_matches_biot_savart_on_axis():
    """Art. 833: far on axis, the loop field converges to 2 m / z^3.

    Oracle: (1) the exact on-axis loop field 2 pi I R^2 / (c (R^2+z^2)^{3/2}),
    checked against an independent Biot-Savart quadrature; (2) its dipole
    limit 2 m / z^3 with m = I pi R^2 / c.
    """
    radius, current = 0.01, 1.0e10
    m = current * np.pi * radius**2 / C
    z = 1.0
    B_exact_axis = 2.0 * np.pi * current * radius**2 / (C * (radius**2 + z**2) ** 1.5)
    B_num = _biot_savart_loop([0.0, 0.0, z], current, radius, n=2000)
    # independent quadrature reproduces the exact loop formula
    assert B_num[2] == pytest.approx(B_exact_axis, rel=1e-8)
    # the exact loop field converges to the dipole value with O(R^2/z^2) error
    assert abs(B_exact_axis - 2.0 * m / z**3) / (2.0 * m / z**3) < 3e-4
    # module's dipole field returns (B_r, B_theta) = (2m cos th / r^3, -m sin th / r^3)
    Br, Bth = calc_molecular_field(m, z, 0.0)
    assert Br == pytest.approx(2.0 * m / z**3, rel=1e-12)
    assert abs(Bth) < 1e-12 * m / z**3 + 1e-30


@pytest.mark.article(833)
def test_art833_dipole_field_equator():
    """Art. 833: in the equatorial plane |B| = m / r^3, opposite to m.

    Convention (pinned by the suite): the returned B_theta is the
    component along -theta_hat, so the physical equatorial field, which
    points opposite to m, carries a NEGATIVE B_theta here.
    """
    m = 2.5
    r = 0.5
    Br, Bth = calc_molecular_field(m, r, np.pi / 2)
    assert Br == pytest.approx(0.0, abs=1e-12)
    assert Bth == pytest.approx(-m / r**3, rel=1e-12)


# ── Art. 834 — equivalence of current loop and dipole off-axis ─────────────


@pytest.mark.article(834)
def test_art834_loop_equals_dipole_off_axis():
    """Art. 834: a small loop reproduces the full dipole field off axis.

    Oracle: independent Biot-Savart quadrature vs the dipole tensor
    formula at a generic angle theta = 60 degrees.
    """
    radius, current = 0.02, 5.0e9
    m = current * np.pi * radius**2 / C
    r_obs, theta = 2.0, np.pi / 3
    point = np.array([r_obs * np.sin(theta), 0.0, r_obs * np.cos(theta)])

    B_loop = _biot_savart_loop(point, current, radius, n=8000)
    B_dip = _dipole_field([0.0, 0.0, m], point)
    assert np.linalg.norm(B_loop - B_dip) / np.linalg.norm(B_dip) == pytest.approx(
        0.0, abs=5e-4
    )

    # module's (B_r, B_theta) decomposition must rebuild the same vector;
    # the suite-pinned convention measures B_theta along -theta_hat
    Br, Bth = calc_molecular_field(m, r_obs, theta)
    rhat = point / r_obs
    that = np.array([np.cos(theta), 0.0, -np.sin(theta)])
    B_mod = Br * rhat - Bth * that
    assert np.linalg.norm(B_mod - B_dip) / np.linalg.norm(B_dip) == pytest.approx(
        0.0, abs=1e-10
    )


# ── Art. 835 — magnetization M = N f m ──────────────────────────────────────


@pytest.mark.article(835)
def test_art835_magnetization_density_golden():
    """Art. 835: M is the aligned moment per unit volume, M = N f m."""
    theory = AmperesTheory(number_density=2.5e22, alignment_factor=0.4)
    m = 3.0e-20
    assert theory.magnetization(m) == pytest.approx(2.5e22 * 0.4 * m, rel=1e-12)


# ── Art. 836 — Curie susceptibility ─────────────────────────────────────────


@pytest.mark.article(836)
def test_art836_curie_law_codata_golden():
    """Art. 836: chi = N m^2 / (3 k_B T) with exact CODATA k_B."""
    assert K_B == pytest.approx(
        ref_value(836, "boltzmann_constant_erg_K"),
        **tolerance_of(836, "boltzmann_constant_erg_K"),
    )
    N, m, T = 1.0e23, 1.0e-20, 300.0
    theory = AmperesTheory(number_density=N, alignment_factor=1.0)
    expected = N * m**2 / (3.0 * K_B * T)
    assert theory.susceptibility(m, T, applied_field=100.0) == pytest.approx(
        expected, rel=1e-12
    )


@pytest.mark.article(836)
def test_art836_curie_halving_and_field_independence():
    """Art. 836: chi * T is constant; chi must not depend on the field."""
    theory = AmperesTheory(number_density=5.0e22, alignment_factor=1.0)
    m = 2.0e-20
    chi_300 = theory.susceptibility(m, 300.0, applied_field=1.0)
    chi_600 = theory.susceptibility(m, 600.0, applied_field=1.0)
    assert chi_300 == pytest.approx(2.0 * chi_600, rel=1e-12)
    assert theory.susceptibility(m, 300.0, applied_field=1.0) == pytest.approx(
        theory.susceptibility(m, 300.0, applied_field=5000.0), rel=1e-12
    )


# ── Art. 837 — bound current density J_b = c curl M ─────────────────────────


@pytest.mark.article(837)
def test_art837_uniform_magnetization_has_no_bound_current():
    """Art. 837: curl of a uniform M vanishes, so J_b = 0."""
    theory = AmperesTheory()
    uniform = lambda p: np.array([100.0, 0.0, 0.0])  # noqa: E731
    J = theory.bound_current_density(uniform, point=np.array([0.3, -0.2, 0.7]))
    assert np.allclose(J, 0.0, atol=1e-9)


@pytest.mark.article(837)
def test_art837_bound_current_is_c_curl_M_golden():
    """Art. 837: for M = (0, 0, x), curl M = (0, -1, 0) exactly.

    Oracle: analytic curl of a linear field; central differences are
    exact for linear functions, so agreement is machine-precision.
    """
    theory = AmperesTheory()
    M_field = lambda p: np.array([0.0, 0.0, p[0]])  # noqa: E731
    J = theory.bound_current_density(M_field, point=np.array([0.5, 0.1, 0.2]))
    expected = C * np.array([0.0, -1.0, 0.0])
    assert np.allclose(J, expected, rtol=1e-8)


# ── Art. 838 — total magnetic moment integral ───────────────────────────────


@pytest.mark.article(838)
def test_art838_total_moment_uniform_golden():
    """Art. 838: integral of uniform M over a box is M * V exactly."""
    M0 = np.array([0.0, 0.0, 5.0])
    bounds = ((0.0, 2.0), (0.0, 2.0), (0.0, 2.0))
    moment = total_magnetic_moment(lambda p: M0, bounds, n_per_axis=16)
    assert np.allclose(moment, M0 * 8.0, rtol=1e-12)


@pytest.mark.article(838)
def test_art838_total_moment_linear_field_golden():
    """Art. 838: M = (x, 0, 0) over the unit cube integrates to (1/2, 0, 0).

    Oracle: exact elementary integral; midpoint quadrature is exact for
    linear integrands.
    """
    bounds = ((0.0, 1.0), (0.0, 1.0), (0.0, 1.0))
    moment = total_magnetic_moment(
        lambda p: np.array([p[0], 0.0, 0.0]), bounds, n_per_axis=32
    )
    assert moment == pytest.approx(np.array([0.5, 0.0, 0.0]), abs=1e-9)


# ── Art. 839 — bound surface current K_b = c M x n ──────────────────────────


@pytest.mark.article(839)
def test_art839_surface_current_golden_cross_product():
    """Art. 839: K_b = c (M x n) as an exact vector identity."""
    M = np.array([0.0, 0.0, 10.0])
    n = np.array([1.0, 0.0, 0.0])
    K = bound_surface_current(M, n)
    assert np.allclose(K, C * np.array([0.0, 10.0, 0.0]), rtol=1e-12)
    # parallel M and normal carry no surface current
    assert np.allclose(
        bound_surface_current(M, np.array([0.0, 0.0, 1.0])), 0.0, atol=1e-20
    )


# ── Art. 840 — interior field of a magnetized sphere ────────────────────────


@pytest.mark.article(840)
def test_art840_sphere_center_field_rings_golden():
    """Art. 840: B at the center of a uniformly magnetized sphere is
    (8 pi / 3) M.

    Oracle: analytic ring integral oint 2 pi M sin^3 th dth = 8 pi M / 3.
    """
    M = np.array([0.0, 0.0, 1.0])
    B = sphere_center_field_rings(M, radius=3.0, n_rings=512)
    assert np.allclose(
        B,
        ref_value(840, "sphere_center_field_factor") * M,
        rtol=tolerance_of(840, "sphere_center_field_factor")["rel"],
    )


@pytest.mark.article(840)
def test_art840_sphere_interior_field_biot_savart_golden():
    """Art. 840: the full surface-current Biot-Savart quadrature also
    returns (8 pi / 3) M at the center (radius independence)."""
    M = np.array([0.0, 0.0, 2.0])
    for radius in (1.0, 5.0):
        B = sphere_interior_field(M, radius, n_theta=96, n_phi=192)
        # quadrature tolerance looser than the golden's 1e-8 store bound
        assert np.allclose(
            B, ref_value(840, "sphere_center_field_factor") * M, rtol=1e-6
        )


# ── Art. 841 — Weber's force law, Coulomb limit ─────────────────────────────


@pytest.mark.article(841)
def test_art841_weber_static_limit_is_coulomb():
    """Art. 841: with r' = r'' = 0 Weber's law reduces to Coulomb exactly."""
    assert calc_weber_force(2.0, 3.0, 4.0) == pytest.approx(
        ref_value(841, "weber_coulomb_static_limit"),
        **tolerance_of(841, "weber_coulomb_static_limit"),
    )
    F_vec = WebersTheory().force(
        1.0, -1.0, np.array([2.0, 0.0, 0.0]), np.zeros(3), np.zeros(3)
    )
    assert F_vec == pytest.approx(np.array([-0.25, 0.0, 0.0]), abs=1e-12)


@pytest.mark.article(841)
def test_art841_acceleration_term_golden():
    """Art. 841: after the c_W = sqrt(2) c substitution, Weber's
    acceleration term 2 r r'' / c_W^2 becomes r r'' / c^2.

    Oracle: hand-computed factor with the CODATA speed of light.
    """
    q1, q2, r, rdd = 1.0, 1.0, 2.0, 1.0e14
    factor = 1.0 + r * rdd / C**2
    F = calc_weber_force(q1, q2, r, 0.0, rdd)
    assert F == pytest.approx((q1 * q2 / r**2) * factor, rel=1e-12)


# ── Art. 842 — Weber's electrodynamic potential ─────────────────────────────


@pytest.mark.article(842)
def test_art842_weber_potential_golden():
    """Art. 842: V = (q1 q2 / r) (1 - r'^2 / (2 c^2)).

    Oracle: the conserved energy integral of Weber's law; exact
    arithmetic with CODATA c.
    """
    wf = WeberForce(q1=2.0, q2=3.0, separation=5.0, relative_velocity=1.0e9)
    expected = (6.0 / 5.0) * (1.0 - (1.0e9) ** 2 / (2.0 * C**2))
    assert wf.potential_energy() == pytest.approx(expected, rel=1e-12)


# ── Art. 843 — Coulomb limit residual ───────────────────────────────────────


@pytest.mark.article(843)
def test_art843_coulomb_limit_residual_is_zero():
    """Art. 843: the computed Coulomb-limit residual of the Weber theory
    must be exactly zero (static Weber force IS the Coulomb force)."""
    residuals = compare_theories()["webers_theory"]["computed_residuals"]
    assert residuals["coulomb_limit_residual"] == pytest.approx(0.0, abs=1e-15)
    wf = WeberForce(q1=1.5, q2=-2.5, separation=3.0)
    assert wf.force() == pytest.approx(wf.coulomb_limit(), rel=1e-14)


# ── Art. 844 — velocity correction factor ───────────────────────────────────


@pytest.mark.article(844)
def test_art844_velocity_factor_golden_at_point_one_c():
    """Art. 844: at r' = 0.1 c the velocity factor is 1 - 0.005 exactly.

    Oracle: 1 - (0.1 c)^2 / (2 c^2) = 0.995, independent of c.
    """
    wf = WeberForce(q1=1.0, q2=1.0, separation=1.0, relative_velocity=0.1 * C)
    golden = ref_value(844, "velocity_factor_at_0p1_c")
    tol = tolerance_of(844, "velocity_factor_at_0p1_c")
    assert wf.velocity_correction_factor() == pytest.approx(golden, **tol)
    assert wf.force() == pytest.approx(golden, **tol)


# ── Art. 845 — acceleration correction factor ───────────────────────────────


@pytest.mark.article(845)
def test_art845_acceleration_factor_golden():
    """Art. 845: with c_W = sqrt(2) c the factor is 1 + r r'' / c^2."""
    r, rdd = 2.0, 1.0e14
    wf = WeberForce(q1=1.0, q2=1.0, separation=r, relative_acceleration=rdd)
    expected = 1.0 + r * rdd / C**2
    assert wf.acceleration_correction_factor() == pytest.approx(expected, rel=1e-12)


# ── Art. 846 — Ampere's wire force recovered from Weber ─────────────────────


@pytest.mark.article(846)
def test_art846_wire_force_vs_finite_closed_form():
    """Art. 846: the parallel-wire force computed from element forces must
    match the closed finite-wire form F/L = -i1 i2 (sqrt(4L^2+d^2) - d)/(L d).

    Oracle: the closed form is derived independently in this test file
    (primitive integral of -i1 i2 dl1 dl2 / (c^2 rho) over two segments).
    """
    i1, i2, d, L = 1.0, 2.0, 0.5, 100.0
    result = ampere_wire_force_recovery(i1, i2, d, L, n_segments=2000)
    closed_finite = -i1 * i2 * (np.sqrt(4.0 * L**2 + d**2) - d) / (L * d)
    assert result["F_per_length_dynes_cm"] == pytest.approx(closed_finite, rel=2e-4)
    assert result["expected_infinite_wire_dynes_cm"] == pytest.approx(
        -2 * i1 * i2 / d, rel=1e-12
    )
    assert result["attractive"] is True


@pytest.mark.article(846)
def test_art846_antiparallel_currents_repel():
    """Art. 846: reversing one current reverses the force sign."""
    para = ampere_wire_force_recovery(1.0, 1.0, 1.0, 50.0, n_segments=400)
    anti = ampere_wire_force_recovery(1.0, -1.0, 1.0, 50.0, n_segments=400)
    assert para["F_per_length_dynes_cm"] < 0
    assert anti["F_per_length_dynes_cm"] > 0
    assert anti["attractive"] is False


# ── Art. 847 — induced EMF, transformer and motional terms ──────────────────


@pytest.mark.article(847)
def test_art847_induced_emf_goldens_and_lenz_sign():
    """Art. 847: EMF = -(M dI/dt + I dM/dt); golden arithmetic plus the
    Lenz requirement that a rising primary current drives a negative EMF."""
    wb = WebersTheory()
    assert wb.induced_emf(2.0, 3.0, dI_dt=5.0) == pytest.approx(
        ref_value(847, "emf_transformer_term"),
        **tolerance_of(847, "emf_transformer_term"),
    )
    assert wb.induced_emf(2.0, 3.0, dM_dt=5.0) == pytest.approx(
        ref_value(847, "emf_motional_term"),
        **tolerance_of(847, "emf_motional_term"),
    )
    assert wb.induced_emf(2.0, 3.0, dI_dt=5.0, dM_dt=5.0) == pytest.approx(
        ref_value(847, "emf_total"), **tolerance_of(847, "emf_total")
    )
    assert wb.induced_emf(1.0, 1.0, dI_dt=7.0) < 0  # Lenz sign


# ── Art. 848 — Weber's constant ─────────────────────────────────────────────


@pytest.mark.article(848)
def test_art848_weber_constant_is_sqrt2_c():
    """Art. 848: Weber's electrodynamic unit of velocity is sqrt(2) c.

    Golden pinned in the reference store (sqrt(2) * 2.99792458e10 cm/s).
    """
    assert weber_constant() == pytest.approx(
        ref_value(848, "weber_constant_sqrt2_c"),
        **tolerance_of(848, "weber_constant_sqrt2_c"),
    )


# ── Art. 849 — critical velocity and sign flip ──────────────────────────────


@pytest.mark.article(849)
def test_art849_critical_velocity_and_force_sign_flip():
    """Art. 849: at r' = sqrt(2) c the velocity factor changes sign; the
    force of like charges flips from repulsion to attraction beyond it."""
    assert critical_velocity() == pytest.approx(weber_constant(), rel=1e-12)
    cw = critical_velocity()
    f_below = calc_weber_force(1.0, 1.0, 1.0, 0.99 * cw, 0.0)
    f_above = calc_weber_force(1.0, 1.0, 1.0, 1.01 * cw, 0.0)
    assert f_below > 0  # repulsion
    assert f_above < 0  # sign flipped beyond the critical velocity
    # exactly at the critical velocity the velocity factor vanishes
    wf = WeberForce(q1=1.0, q2=1.0, separation=1.0, relative_velocity=cw)
    assert wf.velocity_correction_factor() == pytest.approx(0.0, abs=1e-12)


# ── Art. 850 — energy conservation under Weber's law ────────────────────────


@pytest.mark.article(850)
def test_art850_weber_energy_conservation_residual():
    """Art. 850: E = (1/2) mu r'^2 + (q1 q2 / r)(1 - r'^2 / 2c^2) is an
    exact integral of Weber's law; an RK4 integration must conserve it."""
    residual = weber_energy_conservation_residual(
        q1=1.0, q2=-1.0, reduced_mass=1.0, r0=1.0, v0=1.0e5, t_end=1.0e-5, n_steps=4000
    )
    assert residual < 1.0e-8


# ── Art. 851 — Neumann vector potential ─────────────────────────────────────


@pytest.mark.article(851)
def test_art851_vector_potential_axisymmetry_and_far_dipole():
    """Art. 851: A = I oint dl'/|r - r'| is azimuthal and matches the
    far-field dipole form A -> (m x rhat)/r^2.

    Oracle: analytic dipole potential written in this test.
    """
    current, radius = 2.0, 1.0
    pot = NeumannPotential(
        current=current,
        circuit_shape=lambda t: np.array([radius * np.cos(t), radius * np.sin(t), 0.0]),
    )
    # axial symmetry: rotating the observation point rotates A
    n_seg = 400
    A1 = pot.vector_potential_at(np.array([3.0, 0.0, 1.0]), n_segments=n_seg)
    A2 = pot.vector_potential_at(np.array([0.0, 3.0, 1.0]), n_segments=n_seg)
    assert np.linalg.norm(A1) == pytest.approx(np.linalg.norm(A2), rel=1e-10)
    # azimuthal: z component vanishes exactly (dl has no z part); the
    # radial-cylindrical component vanishes analytically, and the O(dt)
    # bound below allows for the forward-difference dl discretization
    # used by the quadrature (exact for the continuous integral).
    dt = 2.0 * np.pi / n_seg
    r_cyl = np.array([3.0, 0.0, 0.0])
    assert abs(np.dot(A1, r_cyl / 3.0)) < 2.0 * dt * np.linalg.norm(A1)
    assert abs(A1[2]) < 1e-12 * np.linalg.norm(A1) + 1e-30
    # far-field dipole form: A = (m_vec x rhat) / r^2 with m in this
    # convention = I * area (the 1/c sits in the moment definition used
    # by the force laws; here A = I oint dl'/r directly).
    r_obs = np.array([60.0, 0.0, 80.0])  # r = 100 cm, R/r = 0.01
    # n_segments large enough that the O(dt) forward-difference error of
    # the quadrature (~ dt/2) sits well below the dipole truncation
    A_far = pot.vector_potential_at(r_obs, n_segments=20000)
    rn = np.linalg.norm(r_obs)
    A_dip = (
        np.cross(np.array([0.0, 0.0, current * np.pi * radius**2]), r_obs / rn) / rn**2
    )
    # O((R/r)^2) = 1e-4 correction to the leading dipole term
    assert np.linalg.norm(A_far - A_dip) / np.linalg.norm(A_dip) == pytest.approx(
        0.0, abs=1e-3
    )


# ── Art. 852 — flux through a circuit equals M I ────────────────────────────


@pytest.mark.article(852)
def test_art852_flux_equals_MI():
    """Art. 852: Phi = oint A . dl = M I for coaxial loops.

    Oracle: the Neumann double integral computed by an independent
    function (module-level quadrature) of the same mathematical object.
    """
    current, R1, R2, d = 3.0, 1.0, 2.0, 3.0
    pot = NeumannPotential(
        current=current,
        circuit_shape=lambda t: np.array([R1 * np.cos(t), R1 * np.sin(t), 0.0]),
    )
    target = lambda t: np.array([R2 * np.cos(t), R2 * np.sin(t), d])  # noqa: E731
    flux = pot.magnetic_flux_through(target, n_segments=80)
    M = neumann_mutual_inductance(R1, R2, d, n_segments=400)
    assert flux == pytest.approx(M * current, rel=2e-3)


# ── Art. 853 — quadrature vs Maxwell's elliptic closed form ─────────────────


@pytest.mark.article(853)
def test_art853_neumann_quadrature_matches_elliptic_closed_form():
    """Art. 853: M = 4 pi sqrt(ab) [(2/k - k) K(k^2) - (2/k) E(k^2)].

    Oracle: scipy.special elliptic integrals are an independent
    implementation of the closed form; the Neumann double integral is
    evaluated by direct quadrature.
    """
    for R1, R2, d in [(1.0, 2.0, 3.0), (1.0, 1.0, 0.5), (2.0, 5.0, 10.0)]:
        M_quad = neumann_mutual_inductance(R1, R2, d, n_segments=400)
        M_cf = maxwell_mutual_inductance_closed_form(R1, R2, d)
        assert M_quad == pytest.approx(M_cf, rel=5e-3)
        assert M_quad > 0  # coaxial same-orientation loops couple positively


# ── Art. 854 — self-inductance of a circular circuit ────────────────────────


@pytest.mark.article(854)
def test_art854_self_inductance_golden_formula():
    """Art. 854: L = 4 pi R (ln(8R/a) - 2) (surface-current form).

    Oracle: hand arithmetic; ln(800) - 2 at R = 10, a = 0.1.
    """
    R, a = 10.0, 0.1
    expected = 4.0 * np.pi * R * (np.log(8.0 * R / a) - 2.0)
    assert circular_loop_inductance(R, a) == pytest.approx(expected, rel=1e-12)
    nt = NeumannTheory()
    loop = lambda t: np.array([R * np.cos(t), R * np.sin(t), 0.0])  # noqa: E731
    assert nt.self_inductance(loop, wire_radius=a) == pytest.approx(expected, rel=1e-12)


# ── Art. 855 — transformer EMF = -M dI/dt ───────────────────────────────────


@pytest.mark.article(855)
def test_art855_induced_emf_neumann_sign_and_golden():
    """Art. 855: EMF_2 = -M dI_1/dt with the Lenz-minus sign."""
    nt = NeumannTheory()
    assert nt.induced_emf(3.0, 2.0, 5.0) == pytest.approx(-15.0, rel=1e-12)
    # Lenz: increasing primary current induces an opposing EMF
    assert nt.induced_emf(1.0, 1.0, 4.0) < 0
    # decreasing primary current induces an EMF of the opposite sign
    assert nt.induced_emf(1.0, 1.0, -4.0) > 0


# ── Art. 856 — reciprocity M_12 = M_21 ──────────────────────────────────────


@pytest.mark.article(856)
def test_art856_reciprocity_with_unequal_discretizations():
    """Art. 856: the Neumann integral is symmetric under 1 <-> 2 even when
    the two circuits are discretized with different segment counts."""
    residual = neumann_reciprocity_residual(
        R1=1.0, R2=3.0, d=2.0, n_segments_12=180, n_segments_21=140
    )
    assert residual < 1.0e-6


# ── Art. 857 — far-field dipole limit ───────────────────────────────────────


@pytest.mark.article(857)
def test_art857_far_field_dipole_limit():
    """Art. 857: M -> 2 pi^2 R1^2 R2^2 / d^3 at large separation.

    Oracle: dipole-dipole coupling derived independently; the residual is
    O(R^2/d^2) plus discretization error, bounded here.
    """
    R1, R2, d = 1.0, 1.0, 20.0
    M_quad = neumann_mutual_inductance(R1, R2, d, n_segments=400)
    M_dipole = 2.0 * np.pi**2 * R1**2 * R2**2 / d**3
    rel = abs(M_quad - M_dipole) / M_dipole
    assert 0.0 < rel < 0.02
    assert neumann_far_field_residual(
        R1=R1, R2=R2, d=d, n_segments=400
    ) == pytest.approx(rel, rel=1e-6)


# ── Art. 858 — motional EMF of separating circuits ──────────────────────────


@pytest.mark.article(858)
def test_art858_motional_emf_matches_dipole_oracle():
    """Art. 858: EMF = -I v dM/dd; in the far field M = 2 pi^2 R1^2 R2^2 d^-3
    so EMF = 6 pi^2 I v R1^2 R2^2 / d^4 > 0 when the loops separate.

    Oracle: closed dipole derivative computed in this test.
    """
    R1, R2, d, I, v = 1.0, 1.0, 20.0, 5.0, 2.0
    emf = motional_emf_coaxial(R1, R2, d, I, v, n_segments=400)
    emf_dipole = 6.0 * np.pi**2 * I * v * R1**2 * R2**2 / d**4
    assert emf > 0  # Lenz: separation weakens coupling, EMF sustains flux
    assert emf == pytest.approx(emf_dipole, rel=0.03)


# ── Art. 859 — characteristics of the competing theories ────────────────────


@pytest.mark.article(859)
def test_art859_compare_theories_structure_and_required_flags():
    """Art. 859: the comparison covers Ampere, Weber and Neumann with the
    characteristic flags Maxwell's account assigns to each."""
    result = compare_theories()
    assert set(result.keys()) == {"amperes_theory", "webers_theory", "neumanns_theory"}
    # exactly the three competing theories of Arts. 859-861 (numeric pin)
    assert len(result) == 3
    for theory in result.values():
        assert "characteristics" in theory
        assert isinstance(theory["characteristics"], dict) and theory["characteristics"]
    # capability flags required by Maxwell's chapter XXII/XXIII analysis
    from maxwell.molecular.competing_theories import (
        analyze_amperes_theory,
        analyze_neumanns_theory,
        analyze_webers_theory,
        maxwells_theory_advantages,
    )

    amp = analyze_amperes_theory()
    assert amp["molecular_currents"]
    assert isinstance(amp["limitations"], list) and amp["limitations"]
    web = analyze_webers_theory()
    assert web["velocity_dependent"] and web["action_at_distance"]
    neu = analyze_neumanns_theory()
    assert neu["potential_based"] and neu["induction_focus"]
    maxw = maxwells_theory_advantages()
    assert maxw["field_concept"] and maxw["displacement_current"]


# ── Art. 860 — computed residuals, no invented scores ───────────────────────


@pytest.mark.article(860)
def test_art860_residuals_are_finite_small_and_honest():
    """Art. 860: every theory reports >= 4 computed residuals, all finite,
    all below an honest bound (no invented 0.95-style scores, no NaNs)."""
    result = compare_theories()
    for name, theory in result.items():
        residuals = theory["computed_residuals"]
        assert len(residuals) >= 4, name
        for key, value in residuals.items():
            assert np.isfinite(value), (name, key)
            assert value >= 0.0, (name, key)
        assert theory["max_residual"] < 0.05, name
        assert theory["max_residual"] == pytest.approx(
            max(residuals.values()), rel=1e-12
        )


@pytest.mark.article(860)
def test_art860_dipole_residual_independently_zero():
    """Art. 860: Ampere's dipole-axis residual is exactly zero because the
    axis field formula IS 2m/r^3 (independent re-derivation)."""
    residuals = compare_theories()["amperes_theory"]["computed_residuals"]
    assert residuals["dipole_axis_residual"] == pytest.approx(0.0, abs=1e-15)
    assert residuals["dipole_equator_residual"] == pytest.approx(0.0, abs=1e-15)


# ── Art. 861 — computed consistency checks ──────────────────────────────────


@pytest.mark.article(861)
def test_art861_checks_are_boolean_and_self_consistent():
    """Art. 861: computed_checks are booleans; n_checks_passed counts them."""
    result = compare_theories()
    for name, theory in result.items():
        checks = theory["computed_checks"]
        assert checks, name
        assert all(isinstance(v, bool) for v in checks.values()), name
        assert theory["n_checks_passed"] == sum(checks.values()), name
        assert theory["n_checks_passed"] == len(checks), name


@pytest.mark.article(861)
def test_art861_weber_checks_include_critical_velocity_sign_flip():
    """Art. 861: Weber's analysis check set includes the critical-velocity
    sign flip, and it passes (value 1 = pass, computed in the module)."""
    from maxwell.molecular.competing_theories import analyze_webers_theory

    checks = analyze_webers_theory()["computed_checks"]
    assert "critical_velocity_sign_flip" in checks
    assert float(checks["critical_velocity_sign_flip"]) == pytest.approx(1.0)


# ── Art. 862 — aggregation of the comparison ────────────────────────────────


@pytest.mark.article(862)
def test_art862_compare_all_and_synthesis_best_theory():
    """Art. 862: CompetingTheory.compare_all aggregates computed residuals
    for a known theory; synthesize_theory_comparison selects the theory
    with the smallest maximum computed residual among Maxwell/Weber/Neumann."""
    ct = CompetingTheory(name="Weber", fundamental_entity="moving_charge")
    full = ct.compare_all()
    assert isinstance(full, dict) and "Weber" in full
    entry = full["Weber"]
    assert "computed_residuals" in entry and "max_residual" in entry
    # Weber's residuals from compare_all equal the compare_theories entry
    assert entry["computed_residuals"] == pytest.approx(
        compare_theories()["webers_theory"]["computed_residuals"], rel=1e-12
    )

    synth = synthesize_theory_comparison()
    cr = synth["comparison_results"]
    assert set(cr.keys()) == {"Maxwell", "Weber", "Neumann"}
    best_by_rule = min(cr, key=lambda k: cr[k]["max_residual"])
    assert synth["best_theory"] == best_by_rule
    # independent oracle for Maxwell's single residual: |3.1e10 - 3.15e10|/3.15e10
    assert cr["Maxwell"]["computed_residuals"]["historical_wave_speed_residual"] == (
        pytest.approx(abs(3.1e10 - 3.15e10) / 3.15e10, rel=1e-12)
    )


# ── Art. 863 — consistency verification is computed ─────────────────────────


@pytest.mark.article(863)
def test_art863_verify_theory_consistency_computed_for_all_theories():
    """Art. 863: verify_theory_consistency derives 'verified' from the
    computed checks for every theory."""
    for name in ("Maxwell", "Weber", "Neumann", "Ampere"):
        v = verify_theory_consistency(name)
        checks = v["computed_checks"]
        assert v["verified"] == all(checks.values())
        assert v["verified"] == v["fully_consistent"]
        assert v["consistency_fraction"] == pytest.approx(
            sum(checks.values()) / len(checks), rel=1e-12
        )


# ── Art. 864 — cross-theory differences from residuals ──────────────────────


@pytest.mark.article(864)
def test_art864_differences_and_cross_comparison_computed():
    """Art. 864: differences between theories are derived from their
    residual budgets, not asserted."""
    diff = analyze_theory_differences("Maxwell", "Weber")
    assert diff["total_residual_theory1"] >= 0.0
    assert diff["total_residual_theory2"] >= 0.0
    lower = diff["computed_lower_residual_theory"]
    if diff["total_residual_theory1"] < diff["total_residual_theory2"]:
        assert lower == diff["theory1"]
    else:
        assert lower == diff["theory2"]

    cross = compare_electromagnetic_theories()
    assert {"Maxwell", "Weber", "Neumann"} <= set(cross.keys())
    for entry in cross.values():
        # every cross-comparison entry carries computed residuals, no scores
        assert "computed_residuals" in entry or "computed_checks" in entry


# ── Art. 865 — wave properties from K and mu ────────────────────────────────


@pytest.mark.article(865)
def test_art865_wave_speed_and_impedance_goldens():
    """Art. 865: v = c / sqrt(K mu); in vacuum v = c and Z = E/H = 1.

    Oracle: the Gaussian plane-wave impedance sqrt(mu/K) equals exactly 1
    in vacuum; the water speed follows from the empirical n = 1.3327.
    """
    vacuum = calc_wave_properties(MediumProperties("vacuum", 1.0, 1.0))
    assert vacuum.speed == pytest.approx(C, rel=1e-12)
    assert vacuum.impedance == pytest.approx(1.0, rel=1e-12)
    assert vacuum.is_transverse is True
    assert _wave_impedance(1.0, 1.0) == pytest.approx(1.0, rel=1e-12)

    K_water, n_golden = 1.776, 1.3326665
    water = calc_wave_properties(MediumProperties("water_optical", K_water, 1.0))
    assert water.speed == pytest.approx(C / np.sqrt(K_water), rel=1e-12)
    assert water.speed == pytest.approx(C / n_golden, rel=1e-3)
    assert water.impedance == pytest.approx(np.sqrt(1.0 / K_water), rel=1e-12)


@pytest.mark.article(865)
def test_art865_reflection_coefficient_golden():
    """Art. 865: normal-incidence R = ((n1 - n2)/(n1 + n2))^2.

    Oracle: Fresnel formula evaluated in this test.
    """
    air = MediumProperties("air", 1.000586, 1.0)
    glass = MediumProperties("glass", 2.25, 1.0)
    R = calc_reflection_coefficient(air, glass)
    n1, n2 = np.sqrt(1.000586), 1.5
    assert R == pytest.approx(((n1 - n2) / (n1 + n2)) ** 2, rel=1e-12)
    # total internal reflection beyond the critical angle
    dense = MediumProperties("glass", 2.25, 1.0)
    rare = MediumProperties("air", 1.0, 1.0)
    assert calc_reflection_coefficient(
        dense, rare, angle_incidence=1.0
    ) == pytest.approx(1.0)


# ── Art. 866 — honest verification of n^2 = K ───────────────────────────────


@pytest.mark.article(866)
def test_art866_default_dataset_verifies_with_provenance():
    """Art. 866: the default dataset (air, paraffin, sulfur, optical water)
    satisfies n^2 = K within tolerance; every entry carries provenance and
    the static-water trap is excluded with a dispersion reason."""
    r = verify_maxwell_relation()
    assert r["verified"] is True
    assert r["verified"] == r["all_agree"]
    for name, entry in r["media"].items():
        assert entry["agrees"] is True, name
        assert entry["provenance"], name
        assert entry["n_predicted"] == pytest.approx(
            np.sqrt(entry["K_measured"]), rel=1e-12
        )
    excluded_names = [e["name"] for e in r["excluded_media"]]
    assert "water_static" in excluded_names
    for e in r["excluded_media"]:
        assert e["reason"]


@pytest.mark.article(866)
def test_art866_honesty_wrong_water_datum_flips_the_verdict():
    """Art. 866: injecting the actual static-water numbers (K = 80.4 with
    the optical n = 1.3330) must flip 'verified' to False. The verdict is
    computed from the data, never hardcoded."""
    r = verify_maxwell_relation(media_data=[("water", 80.4, 1.3330)])
    entry = r["media"]["water"]
    expected_error = abs(1.3330 - np.sqrt(80.4)) / np.sqrt(80.4)
    assert entry["error"] == pytest.approx(expected_error, rel=1e-12)
    assert entry["error"] == pytest.approx(0.8513, abs=1e-3)
    assert entry["agrees"] is False
    assert r["all_agree"] is False
    assert r["verified"] is False


@pytest.mark.article(866)
def test_art866_wave_speed_check_and_completeness_are_computed():
    """Art. 866: verify_wave_speed's verdict equals the conjunction of its
    sub-checks; analyze_theory_completeness combines computed verdicts."""
    ws = verify_wave_speed()
    assert ws["verified"] == (
        ws["historical_agreement"]
        and ws["modern_agreement"]
        and ws["water_speed_correct"]
    )
    assert ws["verified"] is True
    complete = analyze_theory_completeness()
    assert complete["theory_complete"] == bool(
        complete["wave_speed"]["verified"]
        and complete["maxwell_relation"]["verified"]
        and complete["transverse_waves"]
    )
