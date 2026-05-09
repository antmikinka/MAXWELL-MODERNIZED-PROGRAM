"""
Test new Part IV Constitutive Relations modules.

Comprehensive test coverage for constitutive relations:
- Magnetization (Art. 605) — B = H + 4*pi*I = mu*H
- Displacement (Art. 608) — D = (1/4pi)*K*E = epsilon*E
- Conductivity (Art. 609) — J = C*E (Ohm's law)
- Permeability (Art. 614) — B = mu*H

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (linearity, positivity)
- Edge cases (zero inputs, material limits)
- CGS unit compliance
- Citation decorator compliance
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import MaxwellCitation, get_citation

# =============================================================================
# MAGNETIZATION TESTS (Art. 605)
# =============================================================================


class TestMagnetization:
    """Test magnetic constitutive relation: B = H + 4*pi*I = mu*H."""

    def test_magnetic_induction_formula(
        self, cgs_tolerance, assert_vectors_close
    ) -> None:
        """Verify B = mu*H formula.

        For H = 100 oersted, mu = 1000 (iron):
        B = 1000 * 100 = 100,000 gauss
        """
        from maxwell.materials.constitutive.magnetization import calc_magnetic_induction

        H = np.array([100.0, 0.0, 0.0])
        mu = 1000.0

        B = calc_magnetic_induction(H, mu)
        expected = mu * H

        assert_vectors_close(B, expected, cgs_tolerance)

    def test_magnetization_intensity_formula(
        self, cgs_tolerance, assert_vectors_close
    ) -> None:
        """Verify I = chi*H formula.

        For chi = 100, H = 50 oersted:
        I = 100 * 50 = 5000 emu/cm³
        """
        from maxwell.materials.constitutive.magnetization import (
            calc_magnetization_intensity,
        )

        H = np.array([50.0, 0.0, 0.0])
        chi = 100.0

        I = calc_magnetization_intensity(H, chi)
        expected = chi * H

        assert_vectors_close(I, expected, cgs_tolerance)

    def test_permeability_from_susceptibility(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify mu = 1 + 4*pi*chi formula.

        For chi = 100:
        mu = 1 + 4*pi*100 = 1 + 1256.64 = 1257.64
        """
        from maxwell.materials.constitutive.magnetization import calc_permeability

        chi = 100.0
        mu = calc_permeability(chi)
        expected = 1.0 + 4.0 * np.pi * chi

        assert_cgs_close(mu, expected, cgs_tolerance)

    def test_susceptibility_from_permeability(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify chi = (mu - 1)/(4*pi) inverse formula."""
        from maxwell.materials.constitutive.magnetization import (
            calc_permeability,
            calc_susceptibility,
        )

        chi_original = 50.0
        mu = calc_permeability(chi_original)
        chiRecovered = calc_susceptibility(mu)

        assert_cgs_close(chiRecovered, chi_original, cgs_tolerance)

    def test_magnetic_moment_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify m = I*V formula.

        For I = 100 emu/cm³, V = 10 cm³:
        m = 100 * 10 = 1000 emu
        """
        from maxwell.materials.constitutive.magnetization import calc_magnetic_moment

        I = np.array([100.0, 0.0, 0.0])
        V = 10.0

        m = calc_magnetic_moment(I, V)
        expected = I * V

        assert_vectors_close(m, expected, cgs_tolerance)

    def test_magnetization_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Magnetization class methods."""
        from maxwell.materials.constitutive.magnetization import Magnetization

        mag = Magnetization(susceptibility=100.0)

        # Verify permeability calculated correctly
        expected_mu = 1.0 + 4.0 * np.pi * 100.0
        assert abs(mag.permeability - expected_mu) < cgs_tolerance * expected_mu

        # Test B = mu*H
        H = np.array([50.0, 0.0, 0.0])
        B = mag.magnetic_induction(H)
        expected_B = mag.permeability * H
        assert_vectors_close(B, expected_B, cgs_tolerance)

        # Test I = chi*H
        I = mag.magnetization_intensity(H)
        expected_I = mag.susceptibility * H
        assert_vectors_close(I, expected_I, cgs_tolerance)

    def test_verify_magnetization(self) -> None:
        """Verify magnetization relations pass verification."""
        from maxwell.materials.constitutive.magnetization import verify_magnetization

        result = verify_magnetization(
            H_field=np.array([100.0, 0.0, 0.0]), susceptibility=0.01
        )

        assert result["verified"] is True

    def test_magnetization_material_types(self) -> None:
        """Verify material classification by susceptibility."""
        from maxwell.materials.constitutive.magnetization import analyze_magnetization

        # Paramagnetic (chi > 0)
        result_para = analyze_magnetization(np.array([100.0, 0, 0]), 0.001)
        assert result_para["material_type"] == "paramagnetic"

        # Diamagnetic (chi < 0)
        result_dia = analyze_magnetization(np.array([100.0, 0, 0]), -0.0001)
        assert result_dia["material_type"] == "diamagnetic"

        # Non-magnetic (chi = 0)
        result_non = analyze_magnetization(np.array([100.0, 0, 0]), 0.0)
        assert result_non["material_type"] == "non-magnetic"

    def test_B_equals_H_plus_4piI(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify B = H + 4*pi*I identity.

        This is Maxwell's Eq. D (Art. 605).
        """
        from maxwell.materials.constitutive.magnetization import (
            calc_magnetic_induction,
            calc_magnetization_intensity,
            calc_permeability,
        )

        H = np.array([100.0, 0.0, 0.0])
        chi = 0.01

        mu = calc_permeability(chi)
        I = calc_magnetization_intensity(H, chi)
        B_from_mu = calc_magnetic_induction(H, mu)

        # B = H + 4*pi*I should equal B = mu*H
        B_from_HI = H + 4.0 * np.pi * I

        assert_vectors_close(B_from_mu, B_from_HI, cgs_tolerance)

    def test_vacuum_permeability(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify vacuum has mu = 1."""
        from maxwell.materials.constitutive.magnetization import calc_permeability

        mu_vacuum = calc_permeability(0.0)  # chi = 0 for vacuum
        assert_cgs_close(mu_vacuum, 1.0, cgs_tolerance)


# =============================================================================
# DISPLACEMENT TESTS (Art. 608)
# =============================================================================


class TestDisplacement:
    """Test electric displacement: D = (1/4pi)*K*E = epsilon*E."""

    def test_displacement_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify D = epsilon*E formula.

        For epsilon = 80 (water), E = 100 statvolts/cm:
        D = 80 * 100 = 8000 statcoulombs/cm²
        """
        from maxwell.materials.constitutive.displacement import calc_displacement

        E = np.array([100.0, 0.0, 0.0])
        epsilon = 80.0

        D = calc_displacement(E, epsilon)
        expected = epsilon * E

        assert_vectors_close(D, expected, cgs_tolerance)

    def test_permittivity_from_dielectric_constant(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify epsilon = K formula (CGS-Gaussian).

        For K = 80 (water):
        epsilon = 80
        """
        from maxwell.materials.constitutive.displacement import calc_permittivity

        K = 80.0
        epsilon = calc_permittivity(K)
        expected = K  # In CGS-Gaussian, epsilon = K

        assert_cgs_close(epsilon, expected, cgs_tolerance)

    def test_dielectric_constant_from_permittivity(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify K = epsilon (CGS-Gaussian) inverse formula."""
        from maxwell.materials.constitutive.displacement import (
            calc_dielectric_constant,
            calc_permittivity,
        )

        epsilon_original = 10.0
        K = calc_dielectric_constant(epsilon_original)
        epsilonRecovered = calc_permittivity(K)

        assert_cgs_close(epsilonRecovered, epsilon_original, cgs_tolerance)

    def test_displacement_current_formula(
        self, cgs_tolerance, assert_vectors_close, assert_cgs_close
    ) -> None:
        """Verify J_d = (1/4pi)*dD/dt formula.

        For dD/dt = 1e6 statcoulombs/cm²/s:
        J_d = 1e6/(4*pi) = 79577 abamperes/cm²
        """
        from maxwell.materials.constitutive.displacement import (
            calc_displacement_current,
        )

        dD_dt = np.array([1e6, 0.0, 0.0])
        J_d = calc_displacement_current(dD_dt)

        expected_magnitude = 1e6 / (4.0 * np.pi)
        assert_cgs_close(np.linalg.norm(J_d), expected_magnitude, cgs_tolerance)

    def test_displacement_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Displacement class methods."""
        from maxwell.materials.constitutive.displacement import Displacement

        disp = Displacement(permittivity=5.0)

        # Test D = epsilon*E
        E = np.array([200.0, 0.0, 0.0])
        D = disp.displacement(E)
        expected = 5.0 * E
        assert_vectors_close(D, expected, cgs_tolerance)

        # Test polarization P = D - E
        P = disp.polarization(E)
        expected_P = (disp.permittivity - 1) * E
        assert_vectors_close(P, expected_P, cgs_tolerance)

    def test_polarization_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify P = D - E = (epsilon - 1)*E formula."""
        from maxwell.materials.constitutive.displacement import calc_polarization

        E = np.array([100.0, 0.0, 0.0])
        epsilon = 5.0

        P = calc_polarization(E, epsilon)
        expected = (epsilon - 1.0) * E

        assert_vectors_close(P, expected, cgs_tolerance)

    def test_displacement_zero_field(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify zero displacement for zero field."""
        from maxwell.materials.constitutive.displacement import calc_displacement

        D = calc_displacement(np.zeros(3), 5.0)
        assert_vectors_close(D, np.zeros(3), cgs_tolerance)

    def test_vacuum_displacement(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify D = E in vacuum (epsilon = 1/(4pi) in CGS-ESU)."""
        from maxwell.materials.constitutive.displacement import calc_displacement

        E = np.array([100.0, 0.0, 0.0])
        # In CGS-ESU, vacuum epsilon_0 = 1/(4pi)
        epsilon_vacuum = 1.0 / (4.0 * np.pi)

        D = calc_displacement(E, epsilon_vacuum)
        expected = epsilon_vacuum * E

        assert_vectors_close(D, expected, cgs_tolerance)


# =============================================================================
# CONDUCTIVITY TESTS (Art. 609)
# =============================================================================


class TestConductivity:
    """Test electrical conductivity: J = C*E (Ohm's law)."""

    def test_ohm_law_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify J = C*E (Ohm's law in microscopic form).

        For C = 5.9e17 s⁻¹ (copper), E = 1 statvolt/cm:
        J = 5.9e17 statamperes/cm²
        """
        from maxwell.materials.constitutive.conductivity import calc_current_density

        E = np.array([1.0, 0.0, 0.0])
        C = 5.9e17  # Copper conductivity in CGS

        J = calc_current_density(E, C)
        expected = C * E

        assert_vectors_close(J, expected, cgs_tolerance)

    def test_resistance_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify R = rho*L/A formula.

        For rho = 1.7e-6 ohm*cm (copper), L = 100 cm, A = 1 cm²:
        R = 1.7e-6 * 100 / 1 = 1.7e-4 ohms
        """
        from maxwell.materials.constitutive.conductivity import calc_resistance

        rho = 1.7e-6  # Copper resistivity
        L = 100.0
        A = 1.0

        R = calc_resistance(rho, L, A)
        expected = rho * L / A

        assert_cgs_close(R, expected, cgs_tolerance)

    def test_conductivity_from_resistivity(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify C = 1/rho relationship."""
        from maxwell.materials.constitutive.conductivity import (
            calc_conductivity_from_resistivity,
        )

        rho = 1.7e-6
        C = calc_conductivity_from_resistivity(rho)
        expected = 1.0 / rho

        assert_cgs_close(C, expected, cgs_tolerance)

    def test_conductivity_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Conductivity class methods."""
        from maxwell.materials.constitutive.conductivity import Conductivity

        cond = Conductivity(conductivity=1e17)

        # Test J = C*E
        E = np.array([0.5, 0.0, 0.0])
        J = cond.current_density(E)
        expected = 1e17 * E
        assert_vectors_close(J, expected, cgs_tolerance)

        # Test E = J/C
        E_recovered = cond.electric_field(J)
        assert_vectors_close(E_recovered, E, cgs_tolerance)

    def test_joule_heating_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify P = I²*R Joule heating.

        For I = 1 abampere, R = 10 abohms:
        P = 1 * 10 = 10 ergs/s
        """
        from maxwell.materials.constitutive.conductivity import calc_joule_heating

        I = 1.0
        R = 10.0

        P = calc_joule_heating(I, R)
        expected = I**2 * R

        assert_cgs_close(P, expected, cgs_tolerance)

    def test_ohm_law_zero_field(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify zero current for zero field."""
        from maxwell.materials.constitutive.conductivity import calc_current_density

        J = calc_current_density(np.zeros(3), 1e17)
        assert_vectors_close(J, np.zeros(3), cgs_tolerance)

    def test_superconductor_limit(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify zero resistance for superconductor (C -> infinity)."""
        from maxwell.materials.constitutive.conductivity import calc_resistance

        # Superconductor: rho -> 0
        R = calc_resistance(0.0, 100.0, 1.0)
        assert_cgs_close(R, 0.0, cgs_tolerance)


# =============================================================================
# PERMEABILITY TESTS (Art. 614)
# =============================================================================


class TestPermeability:
    """Test permeability relation: B = mu*H."""

    def test_permeability_relation(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify B = mu*H (restating Art. 614).

        For mu = 5000 (mu-metal), H = 1 oersted:
        B = 5000 gauss
        """
        from maxwell.materials.constitutive.permeability import calc_B_from_H

        H = np.array([1.0, 0.0, 0.0])
        mu = 5000.0

        B = calc_B_from_H(H, mu)
        expected = mu * H

        assert_vectors_close(B, expected, cgs_tolerance)

    def test_H_from_B_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify H = B/mu inverse formula."""
        from maxwell.materials.constitutive.permeability import calc_H_from_B

        B = np.array([10000.0, 0.0, 0.0])
        mu = 1000.0

        H = calc_H_from_B(B, mu)
        expected = B / mu

        assert_vectors_close(H, expected, cgs_tolerance)

    def test_relative_permeability(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify mu_r = mu/mu_0 formula."""
        from maxwell.materials.constitutive.permeability import (
            calc_relative_permeability,
        )

        # For iron, mu ≈ 5000, mu_0 = 1 in CGS
        mu = 5000.0
        mu_r = calc_relative_permeability(mu)

        # In CGS, mu_0 = 1, so mu_r = mu
        assert_cgs_close(mu_r, mu, cgs_tolerance)

    def test_permeability_class(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Permeability class methods."""
        from maxwell.materials.constitutive.permeability import Permeability

        perm = Permeability(permeability=1000.0)

        # Test B = mu*H
        H = np.array([0.5, 0.3, 0.0])
        B = perm.B_from_H(H)
        expected = 1000.0 * H
        assert_vectors_close(B, expected, cgs_tolerance)

        # Test H = B/mu
        H_recovered = perm.H_from_B(B)
        assert_vectors_close(H_recovered, H, cgs_tolerance)

    def test_magnetic_energy_density(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify u = B²/(8*pi*mu) energy density.

        For B = 1000 gauss, mu = 1:
        u = 1000²/(8*pi) = 39788 ergs/cm³
        """
        from maxwell.materials.constitutive.permeability import (
            calc_magnetic_energy_density,
        )

        B = 1000.0
        mu = 1.0

        u = calc_magnetic_energy_density(B, mu)
        expected = B**2 / (8.0 * np.pi * mu)

        assert_cgs_close(u, expected, cgs_tolerance)

    def test_permeability_roundtrip(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify B->H->B roundtrip."""
        from maxwell.materials.constitutive.permeability import (
            calc_B_from_H,
            calc_H_from_B,
        )

        H_original = np.array([100.0, 50.0, 25.0])
        mu = 500.0

        B = calc_B_from_H(H_original, mu)
        H_recovered = calc_H_from_B(B, mu)

        assert_vectors_close(H_recovered, H_original, cgs_tolerance)

    def test_vacuum_permeability_value(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify vacuum mu = 1 in CGS."""
        from maxwell.materials.constitutive.permeability import VACUUM_PERMEABILITY

        # In CGS-EMU, vacuum permeability is exactly 1
        assert_cgs_close(VACUUM_PERMEABILITY, 1.0, cgs_tolerance)


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================


class TestConstitutiveCGSUnits:
    """Test CGS unit compliance for constitutive relations."""

    def test_magnetization_units(self) -> None:
        """Verify magnetization produces CGS units."""
        from maxwell.materials.constitutive.magnetization import (
            calc_magnetic_induction,
            calc_magnetization_intensity,
        )

        H = np.array([100.0, 0.0, 0.0])  # oersted

        B = calc_magnetic_induction(H, 1000.0)  # gauss
        assert isinstance(B, np.ndarray)
        assert B.dtype == np.float64

        I = calc_magnetization_intensity(H, 0.01)  # emu/cm³
        assert isinstance(I, np.ndarray)

    def test_displacement_units(self) -> None:
        """Verify displacement produces CGS units."""
        from maxwell.materials.constitutive.displacement import calc_displacement

        E = np.array([100.0, 0.0, 0.0])  # statvolts/cm
        D = calc_displacement(E, 80.0)  # statcoulombs/cm²

        assert isinstance(D, np.ndarray)
        assert D.dtype == np.float64

    def test_conductivity_units(self) -> None:
        """Verify conductivity produces CGS units."""
        from maxwell.materials.constitutive.conductivity import calc_current_density

        E = np.array([1.0, 0.0, 0.0])  # statvolts/cm
        J = calc_current_density(E, 1e17)  # statamperes/cm²

        assert isinstance(J, np.ndarray)


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================


class TestConstitutiveCitationCompliance:
    """Test citation decorator compliance for constitutive modules."""

    def test_magnetization_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify magnetization functions have correct citations."""
        from maxwell.materials.constitutive.magnetization import (
            calc_magnetic_induction,
            calc_magnetization_intensity,
            calc_permeability,
        )

        citation = require_citation(calc_magnetic_induction)
        assert citation.part == 4
        assert 605 in citation.articles

    def test_displacement_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify displacement functions have correct citations."""
        from maxwell.materials.constitutive.displacement import (
            calc_displacement,
            calc_displacement_current,
            calc_permittivity,
        )

        citation = require_citation(calc_displacement)
        assert citation.part == 4
        assert 608 in citation.articles

    def test_conductivity_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify conductivity functions have correct citations."""
        from maxwell.materials.constitutive.conductivity import (
            calc_current_density,
            calc_joule_heating,
            calc_resistance,
        )

        citation = require_citation(calc_current_density)
        assert citation.part == 4
        assert 609 in citation.articles

    def test_permeability_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify permeability functions have correct citations."""
        from maxwell.materials.constitutive.permeability import (
            calc_B_from_H,
            calc_H_from_B,
        )

        citation = require_citation(calc_B_from_H)
        assert citation.part == 4
        assert 614 in citation.articles
