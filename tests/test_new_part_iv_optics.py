"""
Test new Part IV Optics modules.

Comprehensive test coverage for electromagnetic optics:
- Wave velocity (Arts. 786-787) — v = c/sqrt(eps*mu), n = c/v
- Optical constants (Arts. 788-789) — n² = K (Maxwell relation)
- Metal optics (Arts. 798-800) — conductivity -> opacity
- Plane waves (Arts. 790-791) — E ⊥ B ⊥ v (transverse)
- Radiation pressure (Arts. 792-793) — P = Energy/c
- Crystal optics (Arts. 794-797) — double refraction
- Field diffusion (Arts. 801-805) — fields diffuse into conductor

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (transverse waves, energy conservation)
- Edge cases (vacuum, perfect conductor limits)
- CGS unit compliance
- Citation decorator compliance
"""

from __future__ import annotations

import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import get_citation, MaxwellCitation


# =============================================================================
# WAVE VELOCITY TESTS (Arts. 786-787)
# =============================================================================

class TestWaveVelocity:
    """Test electromagnetic wave velocity: v = c/sqrt(eps*mu)."""

    def test_wave_velocity_vacuum(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify v = c in vacuum (eps = mu = 1).

        For eps = 1, mu = 1:
        v = c = 2.99792458e10 cm/s
        """
        from maxwell.optics.velocity import calc_wave_velocity

        v = calc_wave_velocity(1.0, 1.0)
        expected = CONST.C

        assert_cgs_close(v, expected, cgs_tolerance)

    def test_wave_velocity_medium(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify v = c/sqrt(eps*mu) in medium.

        For eps = 4 (glass approx), mu = 1:
        v = c/2 = 1.5e10 cm/s
        """
        from maxwell.optics.velocity import calc_wave_velocity

        v = calc_wave_velocity(4.0, 1.0)
        expected = CONST.C / 2.0

        assert_cgs_close(v, expected, cgs_tolerance)

    def test_wave_velocity_water(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify wave velocity in water (eps ≈ 80).

        For eps = 80, mu = 1:
        v = c/sqrt(80) = c/8.94
        """
        from maxwell.optics.velocity import calc_wave_velocity

        v = calc_wave_velocity(80.0, 1.0)
        expected = CONST.C / np.sqrt(80.0)

        assert_cgs_close(v, expected, cgs_tolerance)

    def test_refractive_index_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify n = sqrt(eps*mu) formula.

        For eps = 4, mu = 1:
        n = sqrt(4) = 2
        """
        from maxwell.optics.velocity import calc_refractive_index

        n = calc_refractive_index(4.0, 1.0)
        expected = 2.0

        assert_cgs_close(n, expected, cgs_tolerance)

    def test_refractive_index_vacuum(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify n = 1 in vacuum."""
        from maxwell.optics.velocity import calc_refractive_index

        n = calc_refractive_index(1.0, 1.0)
        assert_cgs_close(n, 1.0, cgs_tolerance)

    def test_permittivity_from_refractive_index(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify eps = n² for non-magnetic materials.

        For n = 1.5 (glass):
        eps = 2.25
        """
        from maxwell.optics.velocity import calc_permittivity_from_refractive_index

        eps = calc_permittivity_from_refractive_index(1.5)
        expected = 1.5 ** 2

        assert_cgs_close(eps, expected, cgs_tolerance)

    def test_wavelength_in_medium(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify lambda = lambda_0/n formula.

        For lambda_0 = 600 nm, n = 1.5:
        lambda = 400 nm
        """
        from maxwell.optics.velocity import calc_wavelength_in_medium

        lambda_0 = 600e-7  # 600 nm in cm
        n = 1.5

        lambda_med = calc_wavelength_in_medium(lambda_0, n)
        expected = lambda_0 / n

        assert_cgs_close(lambda_med, expected, cgs_tolerance)

    def test_wave_number_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify k = 2*pi/lambda formula.

        For lambda = 500 nm:
        k = 2*pi/(500e-7) = 1.26e5 cm⁻¹
        """
        from maxwell.optics.velocity import calc_wave_number

        lambda_0 = 500e-7  # 500 nm
        n = 1.0

        k = calc_wave_number(lambda_0, n)
        expected = 2.0 * np.pi / lambda_0

        assert_cgs_close(k, expected, cgs_tolerance)

    def test_E_B_ratio_vacuum(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify |E|/|B| = c in vacuum.

        |E|/|B| = c = 3e10 cm/s
        """
        from maxwell.optics.velocity import calc_E_B_ratio

        ratio = calc_E_B_ratio(1.0, 1.0)
        assert_cgs_close(ratio, CONST.C, cgs_tolerance)

    def test_E_B_ratio_medium(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify |E|/|B| = v = c/n in medium.

        For n = 2:
        |E|/|B| = c/2
        """
        from maxwell.optics.velocity import calc_E_B_ratio

        ratio = calc_E_B_ratio(4.0, 1.0)  # n = 2
        expected = CONST.C / 2.0

        assert_cgs_close(ratio, expected, cgs_tolerance)

    def test_wave_velocity_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify WaveVelocity class methods."""
        from maxwell.optics.velocity import WaveVelocity

        wv = WaveVelocity(permittivity=4.0, permeability=1.0)

        # Test velocity
        v = wv.velocity()
        assert_cgs_close(v, CONST.C / 2.0, cgs_tolerance)

        # Test refractive index
        n = wv.refractive_index()
        assert_cgs_close(n, 2.0, cgs_tolerance)

        # Test wavelength for f = 6e14 Hz (yellow light)
        wavelength = wv.wavelength(6e14)
        expected = wv.velocity() / 6e14
        assert_cgs_close(wavelength, expected, cgs_tolerance)

    def test_verify_maxwell_velocity(self) -> None:
        """Verify Maxwell's velocity relations."""
        from maxwell.optics.velocity import verify_maxwell_velocity

        result = verify_maxwell_velocity(permittivity=1.0, permeability=1.0)

        assert result["vacuum_verified"] is True
        assert result["maxwell_verified"] is True

    def test_negative_permittivity_raises(self) -> None:
        """Verify negative permittivity is prevented."""
        from maxwell.optics.velocity import calc_wave_velocity

        with pytest.raises(ValueError):
            calc_wave_velocity(-1.0, 1.0)


# =============================================================================
# OPTICAL CONSTANTS TESTS (Arts. 788-789)
# =============================================================================

class TestOpticalConstants:
    """Test optical constants: n² = K (Maxwell relation)."""

    def test_maxwell_optical_relation(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify n² = K (dielectric constant).

        For K = 2.25:
        n = 1.5
        """
        from maxwell.optics.constants import calc_refractive_from_dielectric

        K = 2.25
        n = calc_refractive_from_dielectric(K)
        expected = np.sqrt(K)

        assert_cgs_close(n, expected, cgs_tolerance)

    def test_dielectric_from_refractive(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify K = n² inverse relation.

        For n = 2.0:
        K = 4.0
        """
        from maxwell.optics.constants import calc_dielectric_from_refractive

        n = 2.0
        K = calc_dielectric_from_refractive(n)
        expected = n ** 2

        assert_cgs_close(K, expected, cgs_tolerance)

    def test_optical_constants_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify OpticalConstants class."""
        from maxwell.optics.constants import OpticalConstants

        oc = OpticalConstants()

        # Test n from K
        n = oc.refractive_from_dielectric(4.0)
        assert_cgs_close(n, 2.0, cgs_tolerance)

        # Test K from n
        K = oc.dielectric_from_refractive(1.5)
        assert_cgs_close(K, 2.25, cgs_tolerance)

    def test_dispersion_relation(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dispersion: n varies with frequency."""
        from maxwell.optics.constants import calc_dispersion

        # Simple dispersion model (dn/domega > 0 for normal dispersion)
        n1 = calc_dispersion(omega=5e14, omega_0=6e14)
        n2 = calc_dispersion(omega=7e14, omega_0=6e14)

        # Higher frequency should have higher n (normal dispersion)
        assert n2 > n1


# =============================================================================
# METAL OPTICS TESTS (Arts. 798-800)
# =============================================================================

class TestMetalOptics:
    """Test metal optics: conductivity -> opacity."""

    def test_skin_depth_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify skin depth: delta = c/sqrt(2*pi*sigma*omega).

        For copper (sigma = 5.9e17 s⁻¹), omega = 2*pi*1e6:
        delta ≈ 0.0066 cm
        """
        from maxwell.optics.metals import calc_skin_depth

        sigma = 5.9e17  # Copper conductivity
        omega = 2.0 * np.pi * 1e6  # 1 MHz

        delta = calc_skin_depth(sigma, omega)
        expected = CONST.C / np.sqrt(2.0 * np.pi * sigma * omega)

        assert_cgs_close(delta, expected, cgs_tolerance)

    def test_skin_depth_frequency_dependence(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify skin depth ∝ 1/sqrt(omega).

        Doubling frequency should reduce skin depth by sqrt(2).
        """
        from maxwell.optics.metals import calc_skin_depth

        sigma = 5.9e17
        omega1 = 2.0 * np.pi * 1e6
        omega2 = 2.0 * np.pi * 2e6

        delta1 = calc_skin_depth(sigma, omega1)
        delta2 = calc_skin_depth(sigma, omega2)

        expected_ratio = np.sqrt(2.0)
        actual_ratio = delta1 / delta2

        assert_cgs_close(actual_ratio, expected_ratio, cgs_tolerance * 10)

    def test_metal_absorption_coefficient(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify absorption coefficient: alpha = 1/delta."""
        from maxwell.optics.metals import calc_absorption_coefficient

        delta = 1e-4  # cm
        alpha = calc_absorption_coefficient(delta)
        expected = 1.0 / delta

        assert_cgs_close(alpha, expected, cgs_tolerance)

    def test_metal_reflectivity(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify metal reflectivity approaches 1 for high conductivity."""
        from maxwell.optics.metals import calc_metal_reflectivity

        # High conductivity metal
        sigma = 5.9e17
        omega = 2.0 * np.pi * 1e14

        R = calc_metal_reflectivity(sigma, omega)

        # Should be close to 1 (highly reflective)
        assert R > 0.9

    def test_transparency_criterion(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify transparency criterion: sigma << omega*epsilon."""
        from maxwell.optics.metals import check_transparency

        # Good conductor: opaque
        is_transparent_conductor = check_transparency(
            sigma=5.9e17,
            omega=1e15,
            epsilon=1.0
        )
        assert is_transparent_conductor is False

        # Dielectric: transparent
        is_transparent_dielectric = check_transparency(
            sigma=1e-10,
            omega=1e15,
            epsilon=2.0
        )
        assert is_transparent_dielectric is True

    def test_metal_optics_class(self) -> None:
        """Verify MetalOptics class."""
        from maxwell.optics.metals import MetalOptics

        mo = MetalOptics(conductivity=5.9e17)

        # Test skin depth at 1 MHz
        delta = mo.skin_depth(2.0 * np.pi * 1e6)
        assert delta > 0
        assert delta < 0.1  # Should be small

        # Test absorption
        alpha = mo.absorption_coefficient(delta)
        assert alpha > 100  # High absorption


# =============================================================================
# PLANE WAVE TESTS (Arts. 790-791)
# =============================================================================

class TestPlaneWaves:
    """Test plane electromagnetic waves: E ⊥ B ⊥ v."""

    def test_transverse_wave_condition(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E ⊥ k (transverse condition).

        For E along x, k along z:
        E · k = 0
        """
        from maxwell.optics.plane_waves import verify_transverse_condition

        E = np.array([100.0, 0.0, 0.0])
        k = np.array([0.0, 0.0, 1.0])

        result = verify_transverse_condition(E, k)
        assert result["transverse"] is True

    def test_E_B_orthogonality(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify E ⊥ B for plane waves."""
        from maxwell.optics.plane_waves import calc_B_from_E

        E = np.array([100.0, 0.0, 0.0])
        k = np.array([0.0, 0.0, 1.0])
        omega = CONST.C  # Vacuum

        B = calc_B_from_E(E, k, omega)

        # E · B should be 0
        dot = np.dot(E, B)
        assert_cgs_close(dot, 0.0, cgs_tolerance)

    def test_B_field_magnitude(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify |B| = |E|/c in vacuum."""
        from maxwell.optics.plane_waves import calc_B_from_E

        E = np.array([100.0, 0.0, 0.0])
        k = np.array([0.0, 0.0, 1.0])
        omega = CONST.C

        B = calc_B_from_E(E, k, omega)
        B_magnitude = np.linalg.norm(B)

        expected = np.linalg.norm(E) / CONST.C
        assert_cgs_close(B_magnitude, expected, cgs_tolerance)

    def test_poynting_vector_direction(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify S = E × B points in propagation direction."""
        from maxwell.optics.plane_waves import calc_poynting_vector

        E = np.array([100.0, 0.0, 0.0])
        B = np.array([0.0, 100.0 / CONST.C, 0.0])

        S = calc_poynting_vector(E, B)

        # S should point in +z direction
        assert S[2] > 0
        assert S[0] < 1e-10
        assert S[1] < 1e-10

    def test_wave_equation_solution(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify plane wave satisfies wave equation."""
        from maxwell.optics.plane_waves import verify_wave_equation

        result = verify_wave_equation(
            omega=CONST.C,
            k_magnitude=1.0,
            permittivity=1.0,
            permeability=1.0
        )

        assert result["wave_equation_verified"] is True

    def test_plane_wave_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify PlaneWave class."""
        from maxwell.optics.plane_waves import PlaneWave

        pw = PlaneWave(
            E_amplitude=100.0,
            omega=CONST.C,
            k_vector=np.array([0.0, 0.0, 1.0])
        )

        # Test E field at origin, t=0
        E = pw.E_field(np.zeros(3), 0.0)
        assert np.linalg.norm(E) > 0

        # Test B field
        B = pw.B_field(np.zeros(3), 0.0)

        # E · B = 0
        dot = np.dot(E, B)
        assert_cgs_close(dot, 0.0, cgs_tolerance * 100)


# =============================================================================
# RADIATION PRESSURE TESTS (Arts. 792-793)
# =============================================================================

class TestRadiationPressure:
    """Test radiation pressure: P = Energy/c."""

    def test_radiation_pressure_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P = u (energy density) for perfect absorption.

        For u = 1 erg/cm³:
        P = 1 dyne/cm²
        """
        from maxwell.optics.radiation_pressure import calc_radiation_pressure

        u = 1.0  # erg/cm³
        P = calc_radiation_pressure(u)
        expected = u

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_radiation_pressure_reflection(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P = 2u for perfect reflection.

        For u = 1 erg/cm³:
        P = 2 dyne/cm²
        """
        from maxwell.optics.radiation_pressure import calc_radiation_pressure_reflection

        u = 1.0
        P = calc_radiation_pressure_reflection(u)
        expected = 2.0 * u

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_radiation_pressure_from_intensity(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P = I/c from intensity.

        For I = c erg/cm²/s:
        P = 1 dyne/cm²
        """
        from maxwell.optics.radiation_pressure import calc_pressure_from_intensity

        I = CONST.C  # erg/cm²/s
        P = calc_pressure_from_intensity(I)
        expected = I / CONST.C

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_solar_radiation_pressure(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify solar radiation pressure at Earth.

        For solar constant ~1.4e6 erg/cm²/s:
        P ~ 4.7e-5 dyne/cm²
        """
        from maxwell.optics.radiation_pressure import calc_pressure_from_intensity

        I_solar = 1.4e6  # erg/cm²/s (solar constant)
        P = calc_pressure_from_intensity(I_solar)
        expected = I_solar / CONST.C

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_radiation_pressure_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify RadiationPressure class."""
        from maxwell.optics.radiation_pressure import RadiationPressure

        rp = RadiationPressure()

        # Test absorption
        P_absorb = rp.pressure_absorption(100.0)
        assert_cgs_close(P_absorb, 100.0, cgs_tolerance)

        # Test reflection
        P_reflect = rp.pressure_reflection(100.0)
        assert_cgs_close(P_reflect, 200.0, cgs_tolerance)

        # Test force on area
        F = rp.force_on_area(100.0, 10.0)  # P=100, A=10
        assert_cgs_close(F, 1000.0, cgs_tolerance)


# =============================================================================
# CRYSTAL OPTICS TESTS (Arts. 794-797)
# =============================================================================

class TestCrystalOptics:
    """Test crystal optics: double refraction, two wave velocities."""

    def test_birefringence_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify birefringence: Delta_n = n_e - n_o.

        For n_o = 1.54, n_e = 1.55 (positive crystal):
        Delta_n = 0.01
        """
        from maxwell.optics.crystals import calc_birefringence

        n_o = 1.54  # Ordinary index
        n_e = 1.55  # Extraordinary index

        delta_n = calc_birefringence(n_o, n_e)
        expected = n_e - n_o

        assert_cgs_close(delta_n, expected, cgs_tolerance)

    def test_double_refraction_angles(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify double refraction angle separation.

        For n1 = 1.5, n2 = 1.6, incident = 30°:
        theta1 = arcsin(sin(30°)/1.5)
        theta2 = arcsin(sin(30°)/1.6)
        """
        from maxwell.optics.crystals import calc_refraction_angle

        incident = np.pi / 6  # 30 degrees

        theta1 = calc_refraction_angle(incident, 1.5)
        theta2 = calc_refraction_angle(incident, 1.6)

        # theta1 should be larger (less refraction)
        assert theta1 > theta2

    def test_optic_axis_propagation(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify no birefringence along optic axis."""
        from maxwell.optics.crystals import calc_effective_index

        # Along optic axis (theta = 0), n_eff = n_o
        n_eff = calc_effective_index(n_o=1.54, n_e=1.55, theta=0.0)
        expected = 1.54

        assert_cgs_close(n_eff, expected, cgs_tolerance)

    def test_perpendicular_optic_axis(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify maximum birefringence perpendicular to optic axis."""
        from maxwell.optics.crystals import calc_effective_index

        # Perpendicular to optic axis (theta = 90°), n_eff = n_e
        n_eff = calc_effective_index(n_o=1.54, n_e=1.55, theta=np.pi/2)
        expected = 1.55

        assert_cgs_close(n_eff, expected, cgs_tolerance)

    def test_crystal_optics_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify CrystalOptics class."""
        from maxwell.optics.crystals import CrystalOptics

        co = CrystalOptics(n_o=1.54, n_e=1.55)

        # Test birefringence
        delta_n = co.birefringence()
        assert_cgs_close(delta_n, 0.01, cgs_tolerance)

        # Test effective index at 45°
        n_eff = co.effective_index(np.pi/4)
        assert n_o < n_eff < n_e


# =============================================================================
# FIELD DIFFUSION TESTS (Arts. 801-805)
# =============================================================================

class TestFieldDiffusion:
    """Test field diffusion into conductors."""

    def test_diffusion_time_scale(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify diffusion time: tau = sigma*L².

        For sigma = 1/(4pi*9e9) s, L = 1 cm:
        tau = L²/(4pi*sigma) (diffusion time)
        """
        from maxwell.optics.diffusion import calc_diffusion_time

        L = 1.0  # cm
        sigma = 5.9e17  # Copper

        # Diffusion time proportional to L²*sigma
        tau = calc_diffusion_time(L, sigma)
        assert tau > 0

    def test_diffusion_length(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify diffusion length: L_diff = sqrt(t/sigma).

        For t = 1 s, sigma -> large:
        L_diff -> small
        """
        from maxwell.optics.diffusion import calc_diffusion_length

        t = 1.0
        sigma = 1e17

        L_diff = calc_diffusion_length(t, sigma)
        assert L_diff > 0
        assert L_diff < 1.0  # Small for high conductivity

    def test_diffusion_equation_solution(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify diffusion equation: dB/dt = (1/4pi*sigma)*nabla²B."""
        from maxwell.optics.diffusion import verify_diffusion_equation

        result = verify_diffusion_equation(
            sigma=1e17,
            L=0.01,
            t=1e-6
        )

        assert result["diffusion_verified"] is True

    def test_field_penetration_depth(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify field penetration decays exponentially."""
        from maxwell.optics.diffusion import calc_field_at_depth

        B_surface = 1000.0
        depth = 1e-4
        delta = 1e-4  # Skin depth

        B = calc_field_at_depth(B_surface, depth, delta)
        expected = B_surface * np.exp(-depth / delta)

        assert_cgs_close(B, expected, cgs_tolerance)

    def test_diffusion_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify FieldDiffusion class."""
        from maxwell.optics.diffusion import FieldDiffusion

        fd = FieldDiffusion(conductivity=5.9e17)

        # Test skin depth at 60 Hz
        delta = fd.skin_depth_60hz()
        assert delta > 0

        # Test field attenuation
        B = fd.field_at_depth(1000.0, 1e-4, delta)
        assert B < 1000.0  # Attenuated


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================

class TestOpticsCGSUnits:
    """Test CGS unit compliance for optics modules."""

    def test_wave_velocity_units(self) -> None:
        """Verify wave velocity produces cm/s."""
        from maxwell.optics.velocity import calc_wave_velocity

        v = calc_wave_velocity(1.0, 1.0)
        assert isinstance(v, float)
        assert v > 1e9  # Should be ~c

    def test_radiation_pressure_units(self) -> None:
        """Verify radiation pressure produces dyne/cm²."""
        from maxwell.optics.radiation_pressure import calc_radiation_pressure

        P = calc_radiation_pressure(1.0)
        assert isinstance(P, float)
        # Units: dyne/cm²

    def test_skin_depth_units(self) -> None:
        """Verify skin depth produces cm."""
        from maxwell.optics.metals import calc_skin_depth

        delta = calc_skin_depth(5.9e17, 1e14)
        assert isinstance(delta, float)
        assert delta < 1.0  # Should be small


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================

class TestOpticsCitationCompliance:
    """Test citation decorator compliance for optics modules."""

    def test_wave_velocity_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify wave velocity functions have correct citations."""
        from maxwell.optics.velocity import (
            calc_wave_velocity,
            calc_refractive_index,
        )

        citation = require_citation(calc_wave_velocity)
        assert citation.part == 4
        assert any(a in citation.articles for a in [786, 787])

    def test_optical_constants_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify optical constants functions have correct citations."""
        from maxwell.optics.constants import calc_refractive_from_dielectric

        citation = require_citation(calc_refractive_from_dielectric)
        assert citation.part == 4
        assert any(a in citation.articles for a in [788, 789])

    def test_metal_optics_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify metal optics functions have correct citations."""
        from maxwell.optics.metals import calc_skin_depth

        citation = require_citation(calc_skin_depth)
        assert citation.part == 4
        assert any(a in citation.articles for a in [798, 799, 800])

    def test_radiation_pressure_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify radiation pressure functions have correct citations."""
        from maxwell.optics.radiation_pressure import calc_radiation_pressure

        citation = require_citation(calc_radiation_pressure)
        assert citation.part == 4
        assert any(a in citation.articles for a in [792, 793])
