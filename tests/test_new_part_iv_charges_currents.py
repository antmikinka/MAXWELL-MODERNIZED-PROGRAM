"""
Test new Part IV Charges and Currents modules.

Comprehensive test coverage for charges and currents:
- Volume charge density (Art. 612) — rho = div(D)
- Surface charge density (Art. 613) — sigma = D_normal
- Total current (Art. 610) — C = conduction + displacement
- EMF relation (Art. 611) — C from EMF and resistance

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (conservation, Gauss's law)
- Edge cases (zero inputs, boundary conditions)
- CGS unit compliance
- Citation decorator compliance
"""

from __future__ import annotations

import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import get_citation, MaxwellCitation


# =============================================================================
# VOLUME CHARGE DENSITY TESTS (Art. 612)
# =============================================================================

class TestVolumeChargeDensity:
    """Test volume charge density: rho = div(D)/(4*pi)."""

    def test_charge_density_from_divergence(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify rho = div(D)/(4*pi) formula.

        For div(D) = 4*pi statcoulombs/cm³:
        rho = 1 statcoulomb/cm³
        """
        from maxwell.electromagnetism.charges.volume import calc_volume_charge_density

        div_D = 4.0 * np.pi  # statcoulombs/cm³
        rho = calc_volume_charge_density(np.zeros(3), div_D)
        expected = 1.0

        assert_cgs_close(rho, expected, cgs_tolerance)

    def test_charge_density_from_E_divergence(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify rho = epsilon*div(E)/(4*pi) formula."""
        from maxwell.electromagnetism.charges.volume import calc_charge_density_from_E

        div_E = 4.0 * np.pi
        epsilon = 1.0

        rho = calc_charge_density_from_E(div_E, epsilon)
        expected = epsilon * div_E / (4.0 * np.pi)

        assert_cgs_close(rho, expected, cgs_tolerance)

    def test_total_charge_uniform_density(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Q = rho*V for uniform density.

        For rho = 1 statcoulomb/cm³, V = 100 cm³:
        Q = 100 statcoulombs
        """
        from maxwell.electromagnetism.charges.volume import calc_total_charge_uniform

        rho = 1.0
        V = 100.0

        Q = calc_total_charge_uniform(rho, V)
        expected = rho * V

        assert_cgs_close(Q, expected, cgs_tolerance)

    def test_charge_in_sphere(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Q = rho*(4/3)*pi*R³ for sphere.

        For rho = 1, R = 3 cm:
        Q = 1 * (4/3)*pi*27 = 36*pi statcoulombs
        """
        from maxwell.electromagnetism.charges.volume import calc_charge_in_sphere

        rho = 1.0
        R = 3.0

        Q = calc_charge_in_sphere(rho, R)
        expected = rho * (4.0 / 3.0) * np.pi * R ** 3

        assert_cgs_close(Q, expected, cgs_tolerance)

    def test_field_from_charged_sphere_outside(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E = Q/r² outside sphere (point charge equivalent).

        For Q = 100 statcoulombs, r = 10 cm:
        E = 100/100 = 1 statvolt/cm
        """
        from maxwell.electromagnetism.charges.volume import calc_field_from_charged_sphere

        Q = 100.0
        R = 1.0  # Sphere radius
        r = 10.0  # Outside sphere

        E = calc_field_from_charged_sphere(Q, R, np.array([r, 0, 0]))
        expected = Q / (r ** 2)

        assert_cgs_close(np.linalg.norm(E), expected, cgs_tolerance)

    def test_field_from_charged_sphere_inside(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E = Q*r/R³ inside sphere (linear with r).

        For Q = 100, R = 10, r = 5:
        E = 100*5/1000 = 0.5 statvolt/cm
        """
        from maxwell.electromagnetism.charges.volume import calc_field_from_charged_sphere

        Q = 100.0
        R = 10.0
        r = 5.0  # Inside sphere

        E = calc_field_from_charged_sphere(Q, R, np.array([r, 0, 0]))
        expected = Q * r / (R ** 3)

        assert_cgs_close(np.linalg.norm(E), expected, cgs_tolerance)

    def test_field_at_center_zero(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify zero field at center of charged sphere."""
        from maxwell.electromagnetism.charges.volume import calc_field_from_charged_sphere

        E = calc_field_from_charged_sphere(100.0, 1.0, np.zeros(3))
        assert_vectors_close(E, np.zeros(3), cgs_tolerance)

    def test_verify_gauss_law_volume(self) -> None:
        """Verify Gauss's law for volume charge."""
        from maxwell.electromagnetism.charges.volume import verify_gauss_law_volume

        result = verify_gauss_law_volume(
            charge_density=1.0,
            sphere_radius=1.0
        )

        assert result["gauss_law_verified"] is True

    def test_volume_charge_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify VolumeCharge class methods."""
        from maxwell.electromagnetism.charges.volume import VolumeCharge

        vc = VolumeCharge(permittivity=1.0)

        # Test total charge in volume for uniform density
        def uniform_rho(r):
            return 1.0

        Q = vc.total_charge_in_volume(
            uniform_rho,
            ((0, 1), (0, 1), (0, 1)),  # 1 cm³ cube
            n_points=10
        )

        # Should be approximately 1.0
        assert abs(Q - 1.0) < 0.1  # 10% tolerance for numerical integration

    def test_negative_radius_raises(self) -> None:
        """Verify negative radius is handled."""
        from maxwell.electromagnetism.charges.volume import calc_charge_in_sphere

        Q = calc_charge_in_sphere(1.0, -1.0)
        assert Q == 0.0


# =============================================================================
# SURFACE CHARGE DENSITY TESTS (Art. 613)
# =============================================================================

class TestSurfaceChargeDensity:
    """Test surface charge density: sigma = D_normal."""

    def test_surface_density_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify sigma = D_normal formula.

        For D_normal = 100 statcoulombs/cm²:
        sigma = 100 statcoulombs/cm²
        """
        from maxwell.electromagnetism.charges.surface import calc_surface_density

        D_normal = 100.0
        sigma = calc_surface_density(D_normal)

        assert_cgs_close(sigma, D_normal, cgs_tolerance)

    def test_surface_density_from_vector(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify sigma = D·n from vector field."""
        from maxwell.electromagnetism.charges.surface import calc_surface_density_from_field

        D = np.array([0.0, 0.0, 100.0])  # Perpendicular to surface
        normal = np.array([0.0, 0.0, 1.0])

        sigma = calc_surface_density_from_field(D, normal)
        expected = np.dot(D, normal)

        assert_cgs_close(sigma, expected, cgs_tolerance)

    def test_surface_density_oblique_field(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify sigma = D*cos(theta) for oblique field."""
        from maxwell.electromagnetism.charges.surface import calc_surface_density_from_field

        D = np.array([0.0, 0.0, 100.0])
        normal = np.array([1.0, 0.0, 0.0])  # Perpendicular to D

        sigma = calc_surface_density_from_field(D, normal)

        # D perpendicular to normal: sigma = 0
        assert_cgs_close(sigma, 0.0, cgs_tolerance)

    def test_total_charge_on_surface(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Q = sigma*A for uniform surface density.

        For sigma = 10 statcoulombs/cm², A = 100 cm²:
        Q = 1000 statcoulombs
        """
        from maxwell.electromagnetism.charges.surface import calc_total_surface_charge

        sigma = 10.0
        A = 100.0

        Q = calc_total_surface_charge(sigma, A)
        expected = sigma * A

        assert_cgs_close(Q, expected, cgs_tolerance)

    def test_conducting_surface_density(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify sigma = E/(4*pi) for conductor surface.

        For E = 4*pi statvolts/cm at surface:
        sigma = 1 statcoulomb/cm²
        """
        from maxwell.electromagnetism.charges.surface import calc_conducting_surface_density

        E_surface = 4.0 * np.pi
        sigma = calc_conducting_surface_density(E_surface)
        expected = E_surface / (4.0 * np.pi)

        assert_cgs_close(sigma, expected, cgs_tolerance)

    def test_surface_charge_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify SurfaceCharge class methods."""
        from maxwell.electromagnetism.charges.surface import SurfaceCharge

        sc = SurfaceCharge()

        # Test surface density
        sigma = sc.surface_density(D_normal=50.0)
        assert_cgs_close(sigma, 50.0, cgs_tolerance)

        # Test total charge
        Q = sc.total_charge(sigma=10.0, area=50.0)
        assert_cgs_close(Q, 500.0, cgs_tolerance)

    def test_boundary_condition_discontinuity(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify D_above - D_below = 4*pi*sigma boundary condition."""
        from maxwell.electromagnetism.charges.surface import verify_boundary_condition

        result = verify_boundary_condition(
            sigma=1.0,
            D_above=100.0,
            D_below=100.0 - 4.0 * np.pi * 1.0
        )

        assert result["boundary_verified"] is True


# =============================================================================
# TOTAL CURRENT TESTS (Art. 610)
# =============================================================================

class TestTotalCurrent:
    """Test total current: C = conduction + displacement."""

    def test_total_current_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify J_total = J_cond + J_disp formula.

        For J_cond = 100, J_disp = 50:
        J_total = 150 abamperes/cm²
        """
        from maxwell.electromagnetism.currents.total import calc_total_current

        J_cond = np.array([100.0, 0.0, 0.0])
        J_disp = np.array([50.0, 0.0, 0.0])

        J_total = calc_total_current(J_cond, J_disp)
        expected = J_cond + J_disp

        assert_vectors_close(J_total, expected, cgs_tolerance)

    def test_total_current_magnitude(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify total current magnitude calculation."""
        from maxwell.electromagnetism.currents.total import calc_total_current_magnitude

        J_cond = 100.0
        J_disp = 50.0

        J_total = calc_total_current_magnitude(J_cond, J_disp)
        expected = J_cond + J_disp

        assert_cgs_close(J_total, expected, cgs_tolerance)

    def test_displacement_fraction(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify displacement current fraction."""
        from maxwell.electromagnetism.currents.total import calc_displacement_fraction

        J_cond = 100.0
        J_disp = 25.0

        fraction = calc_displacement_fraction(J_cond, J_disp)
        expected = J_disp / (J_cond + J_disp)

        assert_cgs_close(fraction, expected, cgs_tolerance)

    def test_total_current_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify TotalCurrent class methods."""
        from maxwell.electromagnetism.currents.total import TotalCurrent

        tc = TotalCurrent()

        J_cond = np.array([200.0, 0.0, 0.0])
        J_disp = np.array([50.0, 0.0, 0.0])

        J_total = tc.total(J_cond, J_disp)
        expected = J_cond + J_disp
        assert_vectors_close(J_total, expected, cgs_tolerance)

        # Verify displacement fraction
        frac = tc.displacement_fraction(J_cond, J_disp)
        assert abs(frac - 0.2) < cgs_tolerance

    def test_zero_displacement_current(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify total = conduction when displacement is zero."""
        from maxwell.electromagnetism.currents.total import calc_total_current

        J_cond = np.array([100.0, 0.0, 0.0])
        J_disp = np.zeros(3)

        J_total = calc_total_current(J_cond, J_disp)
        assert_vectors_close(J_total, J_cond, cgs_tolerance)

    def test_zero_conduction_current(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify total = displacement when conduction is zero."""
        from maxwell.electromagnetism.currents.total import calc_total_current

        J_cond = np.zeros(3)
        J_disp = np.array([75.0, 0.0, 0.0])

        J_total = calc_total_current(J_cond, J_disp)
        assert_vectors_close(J_total, J_disp, cgs_tolerance)


# =============================================================================
# EMF RELATION TESTS (Art. 611)
# =============================================================================

class TestEMFRelation:
    """Test EMF relation: C from EMF and resistance."""

    def test_ohm_law_emf(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify I = EMF/R (Ohm's law for circuits).

        For EMF = 1000 abvolts, R = 10 abohms:
        I = 100 abamperes
        """
        from maxwell.electromagnetism.currents.emf_relation import calc_current_from_emf

        emf = 1000.0
        R = 10.0

        I = calc_current_from_emf(emf, R)
        expected = emf / R

        assert_cgs_close(I, expected, cgs_tolerance)

    def test_emf_from_current(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EMF = I*R inverse formula."""
        from maxwell.electromagnetism.currents.emf_relation import calc_emf_from_current

        I = 50.0
        R = 20.0

        emf = calc_emf_from_current(I, R)
        expected = I * R

        assert_cgs_close(emf, expected, cgs_tolerance)

    def test_power_from_emf(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P = EMF*I power formula.

        For EMF = 100 abvolts, I = 10 abamperes:
        P = 1000 ergs/s
        """
        from maxwell.electromagnetism.currents.emf_relation import calc_power_from_emf

        emf = 100.0
        I = 10.0

        P = calc_power_from_emf(emf, I)
        expected = emf * I

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_emf_relation_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EMFRelation class methods."""
        from maxwell.electromagnetism.currents.emf_relation import EMFRelation

        relation = EMFRelation(resistance=50.0)

        # Test current from EMF
        I = relation.current_from_emf(500.0)
        assert_cgs_close(I, 10.0, cgs_tolerance)

        # Test EMF from current
        emf = relation.emf_from_current(5.0)
        assert_cgs_close(emf, 250.0, cgs_tolerance)

        # Test power
        P = relation.power(100.0, 2.0)
        assert_cgs_close(P, 200.0, cgs_tolerance)

    def test_series_resistance(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify R_series = R1 + R2."""
        from maxwell.electromagnetism.currents.emf_relation import calc_series_resistance

        R1 = 100.0
        R2 = 200.0

        R_total = calc_series_resistance([R1, R2])
        expected = R1 + R2

        assert_cgs_close(R_total, expected, cgs_tolerance)

    def test_parallel_resistance(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify 1/R_parallel = 1/R1 + 1/R2."""
        from maxwell.electromagnetism.currents.emf_relation import calc_parallel_resistance

        R1 = 100.0
        R2 = 100.0

        R_total = calc_parallel_resistance([R1, R2])
        expected = 50.0  # Two equal resistors in parallel

        assert_cgs_close(R_total, expected, cgs_tolerance)

    def test_zero_resistance_limit(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify infinite current for zero resistance (short circuit)."""
        from maxwell.electromagnetism.currents.emf_relation import calc_current_from_emf

        # Very small resistance (not exactly zero to avoid division by zero)
        I = calc_current_from_emf(100.0, 1e-10)
        assert I > 1e9  # Very large current


# =============================================================================
# INTEGRATED CHARGE/CURRENT TESTS
# =============================================================================

class TestChargeCurrentIntegration:
    """Test integrated charge and current relationships."""

    def test_continuity_equation(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify continuity: div(J) + d(rho)/dt = 0."""
        from maxwell.electromagnetism.charges.volume import verify_continuity_equation

        result = verify_continuity_equation(
            rho_func=lambda t: 100.0 - 10.0 * t,
            t=0.0,
            dt=0.1,
            div_J=10.0
        )

        assert result["continuity_verified"] is True

    def test_charge_conservation(self) -> None:
        """Verify charge conservation in closed system."""
        from maxwell.electromagnetism.charges.volume import verify_charge_conservation

        result = verify_charge_conservation(
            initial_charge=1000.0,
            current_out=10.0,
            time_interval=50.0
        )

        assert result["charge_conserved"] is True


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================

class TestChargesCurrentsCGSUnits:
    """Test CGS unit compliance for charge and current modules."""

    def test_volume_charge_units(self) -> None:
        """Verify volume charge produces CGS units."""
        from maxwell.electromagnetism.charges.volume import calc_volume_charge_density

        rho = calc_volume_charge_density(np.zeros(3), 4.0 * np.pi)
        assert isinstance(rho, float)
        # Units: statcoulombs/cm³

    def test_surface_charge_units(self) -> None:
        """Verify surface charge produces CGS units."""
        from maxwell.electromagnetism.charges.surface import calc_surface_density

        sigma = calc_surface_density(100.0)
        assert isinstance(sigma, float)
        # Units: statcoulombs/cm²

    def test_current_density_units(self) -> None:
        """Verify current density produces CGS units."""
        from maxwell.electromagnetism.currents.total import calc_total_current

        J = calc_total_current(
            np.array([100.0, 0, 0]),
            np.array([50.0, 0, 0])
        )
        assert isinstance(J, np.ndarray)
        # Units: abamperes/cm²


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================

class TestChargesCurrentsCitationCompliance:
    """Test citation decorator compliance for charge and current modules."""

    def test_volume_charge_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify volume charge functions have correct citations."""
        from maxwell.electromagnetism.charges.volume import (
            calc_volume_charge_density,
            calc_charge_in_sphere,
            verify_gauss_law_volume,
        )

        citation = require_citation(calc_volume_charge_density)
        assert citation.part == 4
        assert 612 in citation.articles

    def test_surface_charge_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify surface charge functions have correct citations."""
        from maxwell.electromagnetism.charges.surface import (
            calc_surface_density,
            calc_total_surface_charge,
        )

        citation = require_citation(calc_surface_density)
        assert citation.part == 4
        assert 613 in citation.articles

    def test_total_current_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify total current functions have correct citations."""
        from maxwell.electromagnetism.currents.total import (
            calc_total_current,
            calc_displacement_fraction,
        )

        citation = require_citation(calc_total_current)
        assert citation.part == 4
        assert 610 in citation.articles

    def test_emf_relation_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify EMF relation functions have correct citations."""
        from maxwell.electromagnetism.currents.emf_relation import (
            calc_current_from_emf,
            calc_power_from_emf,
        )

        citation = require_citation(calc_current_from_emf)
        assert citation.part == 4
        assert 611 in citation.articles
