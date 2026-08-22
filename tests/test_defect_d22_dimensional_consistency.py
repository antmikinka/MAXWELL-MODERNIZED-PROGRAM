"""D-22 regression: dimensional consistency of the vortex-medium energies.

Stage-3 register defect D-22 (S2) flagged ``vortex_engine/kinetic_energy.py``
(commit fce0348, lines 38, 69, 95-104) for dimensional heuristics decorated
``maxwell_original``:

* a perturbation energy ``0.5 |delta|^2`` carrying no density or stiffness
  (dimensionless, not an energy density);
* a "coupling energy" ``(J . axis) * H`` with the units of
  current-density x field, not an energy density;
* a plane-wave term mixing factors 0.25 and /2 against its own comment.

Disposition (Wave 7, PHYSICUS): the module was re-derived from the Treatise
itself -- Arts. 824-826 eqs. (2), (3), (5), (9) are now implemented verbatim
(category A ``maxwell_original``, no extension content left to reclassify
under the D-08 boundary).  This file supplies the dimensional-consistency
regression test demanded by the register: each energy term's dimensional
exponents (M, L, T) are MEASURED by rescaling the inputs and compared with
the hand-derived energy-density signature (1, -1, -2).  The sensitivity
twin shows the pre-fix heuristic class measures (0, 0, 0) and therefore
FAILS this check, i.e. the test is red on the old behavior class.

Composite-dimension convention: in the coupling terms the constants C*H
(Art. 824) and C*J (Art. 825) carry whatever dimensions make the term an
energy density; the rescalings below assign those dimensions explicitly, so
the check tests the whole term, not an arbitrary split between C and its
partner.

All asserts are numeric with stated tolerances (REQ-T rubric; lint R10);
the expected exponents are goldens in ``tests/articles/reference_values.json``
(arts. 824, 825, 826) with provenance.

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_defect_d22_dimensional_consistency.py -q
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from articles import ref_value, tolerance_of
from maxwell.vortex_engine.kinetic_energy import (
    calc_disturbed_vortex_energy,
    calc_plane_wave_vortex_energy,
    express_vortex_current_velocity,
)

ENERGY_DENSITY_EXPONENTS = (1.0, -1.0, -2.0)  # [M L^-1 T^-2], hand-derived


def _exponent(reference: float, rescaled: float, k: float) -> float:
    """Measured scaling exponent: log(rescaled/reference)/log(k)."""
    return math.log(rescaled / reference) / math.log(k)


@pytest.mark.regression("D-22")
@pytest.mark.article(826)
def test_d22_plane_wave_energy_density_has_energy_density_dimensions():
    """Art. 826 eq. (9): T = (1/2) rho |v|^2 + C gamma (xi'' eta-dot -
    eta'' xi-dot) must scale as an energy density.  Rescaling mass
    quantities by k_M, lengths by k_L, times by k_T (rho -> k_M k_L^-3,
    v -> k_L k_T^-1, curvature -> k_L^-1, composite C*gamma ->
    k_M k_L^-1 k_T^-1) must multiply T by k_M^1 k_L^-1 k_T^-2 -- both
    terms carry the same dimensions, so the sign of T is invariant and
    the exponents are well-defined.
    """
    rho, C, gamma = 1.3, 0.6, 0.9
    v = np.array([0.7, -1.1, 0.2])
    curvature = np.array([-0.4, 0.9, 0.1])
    k_m, k_l, k_t = 2.0, 3.0, 5.0

    T0 = calc_plane_wave_vortex_energy(rho, C, gamma, v, curvature)
    assert T0 > 0.0  # translational term dominates: log-safe

    exponent_mass = _exponent(
        T0, calc_plane_wave_vortex_energy(k_m * rho, k_m * C, gamma, v, curvature), k_m
    )
    exponent_length = _exponent(
        T0,
        calc_plane_wave_vortex_energy(
            k_l**-3 * rho, C / k_l, gamma, k_l * v, curvature / k_l
        ),
        k_l,
    )
    exponent_time = _exponent(
        T0, calc_plane_wave_vortex_energy(rho, C / k_t, gamma, v / k_t, curvature), k_t
    )

    assert exponent_mass == pytest.approx(
        ref_value(826, "energy_density_dimension_mass_exponent"),
        **tolerance_of(826, "energy_density_dimension_mass_exponent"),
    )
    assert exponent_length == pytest.approx(
        ref_value(826, "energy_density_dimension_length_exponent"),
        **tolerance_of(826, "energy_density_dimension_length_exponent"),
    )
    assert exponent_time == pytest.approx(
        ref_value(826, "energy_density_dimension_time_exponent"),
        **tolerance_of(826, "energy_density_dimension_time_exponent"),
    )


@pytest.mark.regression("D-22")
@pytest.mark.article(824)
def test_d22_art824_coupling_term_has_energy_density_dimensions():
    """Art. 824 eq. (3): 2 C (alpha omega_1 + beta omega_2 + gamma
    omega_3).  omega carries T^-1 and the composite C*H carries
    M L^-1 T^-1, so rescaling C by k_M (mass), C by k_L^-1 (length),
    and (C, omega) by k_T^-1 (time) must multiply the term by
    k_M^1 k_L^-1 k_T^-2 -- NOT the current-density-times-field units of
    the pre-fix heuristic.
    """
    H = np.array([0.2, -0.5, 0.8])
    omega = np.array([0.3, 0.6, 0.4])  # H.omega = +0.08 > 0: log-safe
    C = 1.4
    k_m, k_l, k_t = 2.0, 3.0, 5.0

    E0 = calc_disturbed_vortex_energy(H, omega, C)
    assert E0 > 0.0
    assert E0 == pytest.approx(2.0 * C * 0.08, rel=1e-12)  # hand arithmetic

    exponent_mass = _exponent(E0, calc_disturbed_vortex_energy(H, omega, k_m * C), k_m)
    exponent_length = _exponent(
        E0, calc_disturbed_vortex_energy(H, omega, C / k_l), k_l
    )
    exponent_time = _exponent(
        E0, calc_disturbed_vortex_energy(H, omega / k_t, C / k_t), k_t
    )

    assert exponent_mass == pytest.approx(
        ref_value(824, "coupling_energy_dimension_mass_exponent"),
        **tolerance_of(824, "coupling_energy_dimension_mass_exponent"),
    )
    assert exponent_length == pytest.approx(
        ref_value(824, "coupling_energy_dimension_length_exponent"),
        **tolerance_of(824, "coupling_energy_dimension_length_exponent"),
    )
    assert exponent_time == pytest.approx(
        ref_value(824, "coupling_energy_dimension_time_exponent"),
        **tolerance_of(824, "coupling_energy_dimension_time_exponent"),
    )


@pytest.mark.regression("D-22")
@pytest.mark.article(825)
def test_d22_art825_current_velocity_term_has_energy_density_dimensions():
    """Art. 825 eq. (5): 4 pi C (xi-dot u + eta-dot v + zeta-dot w).
    v carries L T^-1 and the composite C*J carries M L^-2 T^-1, so the
    rescalings v -> k_L v / k_T and C -> C / (k_M^-1 k_L^2 k_T) must
    multiply the term by k_M^1 k_L^-1 k_T^-2.
    """
    v = np.array([1.0, 2.0, 0.0])
    J = np.array([4.0, 5.0, 6.0])  # v.J = 14 > 0: log-safe
    C = 0.3
    k_m, k_l, k_t = 2.0, 3.0, 5.0

    E0 = express_vortex_current_velocity(v, J, C)
    assert E0 > 0.0
    assert E0 == pytest.approx(4.0 * math.pi * C * 14.0, rel=1e-12)  # hand

    exponent_mass = _exponent(E0, express_vortex_current_velocity(v, J, k_m * C), k_m)
    exponent_length = _exponent(
        E0, express_vortex_current_velocity(k_l * v, J, C / k_l**2), k_l
    )
    exponent_time = _exponent(
        E0, express_vortex_current_velocity(v / k_t, J, C / k_t), k_t
    )

    assert exponent_mass == pytest.approx(
        ref_value(825, "current_velocity_dimension_mass_exponent"),
        **tolerance_of(825, "current_velocity_dimension_mass_exponent"),
    )
    assert exponent_length == pytest.approx(
        ref_value(825, "current_velocity_dimension_length_exponent"),
        **tolerance_of(825, "current_velocity_dimension_length_exponent"),
    )
    assert exponent_time == pytest.approx(
        ref_value(825, "current_velocity_dimension_time_exponent"),
        **tolerance_of(825, "current_velocity_dimension_time_exponent"),
    )


@pytest.mark.regression("D-22")
def test_d22_sensitivity_twin_old_heuristic_class_fails_the_check():
    """Sensitivity twin (red-on-old-behavior): the pre-fix perturbation
    heuristic ``0.5 |delta|^2`` carried no density or stiffness, so it is
    dimensionless -- its measured exponents are (0, 0, 0), nowhere near
    the energy-density signature (1, -1, -2).  Any regression to the
    D-22 defect class therefore fails the dimensional asserts above.
    """

    def old_perturbation_energy(delta, density, velocity, time_scale):
        # Inline reconstruction of the pre-D-22 heuristic: it ignores the
        # density/velocity/time arguments entirely (that is the defect).
        return 0.5 * float(np.dot(delta, delta))

    delta = np.array([0.7, -1.1, 0.2])
    k = 3.0
    base = old_perturbation_energy(delta, 1.3, 2.0, 5.0)
    exponent_mass = _exponent(
        base, old_perturbation_energy(delta, k * 1.3, 2.0, 5.0), k
    )
    exponent_length = _exponent(
        base, old_perturbation_energy(k * delta, 1.3, 2.0, 5.0), k
    )
    exponent_time = _exponent(
        base, old_perturbation_energy(delta, 1.3, k * 2.0, k * 5.0), k
    )

    for measured, required in zip(
        (exponent_mass, exponent_length, exponent_time), ENERGY_DENSITY_EXPONENTS
    ):
        assert abs(measured - required) > 0.5, (
            "the dimensionless heuristic unexpectedly passed the "
            "energy-density dimensional check"
        )


@pytest.mark.regression("D-22")
@pytest.mark.article(826)
def test_d22_circular_ray_energy_phase_independent_identity():
    """Art. 826 eq. (9) identity (hand-derived): substituting the
    circular ray xi = r cos(nt - qz), eta = r sin(nt - qz) into eq. (9)
    gives T = (1/2) rho r^2 n^2 - C gamma r^2 q^2 n at EVERY phase
    nt - qz (the cos/sin cross terms cancel exactly), the Art. 828
    eq. (15) value.  Verified here at a generic phase, independent of
    the z = t = 0 pin in the magneto-optics suite.
    """
    rho, C, gamma = 1.2, 0.55, 0.35
    r, n, q = 1.7, 4.0, 2.3
    theta = 0.8  # generic phase nt - qz

    velocity = np.array(
        [-r * n * math.sin(theta), r * n * math.cos(theta), 0.0]
    )
    curvature = np.array(
        [-r * q * q * math.cos(theta), -r * q * q * math.sin(theta), 0.0]
    )

    T = calc_plane_wave_vortex_energy(rho, C, gamma, velocity, curvature)
    assert T == pytest.approx(
        0.5 * rho * r**2 * n**2 - C * gamma * r**2 * q**2 * n, rel=1e-12
    )
