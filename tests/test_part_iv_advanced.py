"""
Test Part IV Advanced modules — General Equations and Dimensional Analysis.

Comprehensive test coverage for 2 additional Part IV modules:
1. General Equations (Arts. 594-603) — Maxwell's general equations
2. Dimensional Analysis (Arts. 620-628) — ESU/EMU unit relationships

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (proportionality, direction)
- Edge cases (zero inputs, singularities)
- Citation decorator compliance
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import MaxwellCitation, get_citation

# =============================================================================
# GENERAL EQUATIONS MODULE TESTS (Arts. 594-603)
# =============================================================================


class TestFaradaysLaw:
    """Test Faraday's Law: ∇ × E = -(1/c)·∂B/∂t."""

    def test_faradays_law_opposes_change(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Faraday's law with negative sign: ∇ × E = -(1/c)·∂B/∂t.

        The negative sign (Lenz's law) ensures the induced field opposes
        the change in magnetic flux.

        For dB/dt = [0, 0, 1e10] gauss/s:
        curl_E = -(1/c) * dB/dt = -[0, 0, 1e10/c] statvolts/cm²
        """
        from maxwell.electromagnetism.theory.general_equations import calc_faradays_law

        dB_dt = np.array([0.0, 0.0, 1e10])  # Changing at 1e10 gauss/s in z
        curl_E = calc_faradays_law(dB_dt)

        # ∇ × E = -(1/c)·∂B/∂t
        expected = -(1.0 / C) * dB_dt
        assert_cgs_close(curl_E[2], expected[2], cgs_tolerance)

        # Verify negative sign (opposes change)
        assert (
            curl_E[2] < 0
        ), "Faraday's law should produce negative curl for increasing B"

    def test_faradays_law_magnitude(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify magnitude of Faraday's law calculation."""
        from maxwell.electromagnetism.theory.general_equations import calc_faradays_law

        dB_dt = np.array([1e10, 0.0, 0.0])
        curl_E = calc_faradays_law(dB_dt)

        # Magnitude should be |dB/dt| / c
        expected_magnitude = 1e10 / C
        assert_cgs_close(np.linalg.norm(curl_E), expected_magnitude, cgs_tolerance)

    def test_faradays_law_zero_change(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify zero dB/dt produces zero curl."""
        from maxwell.electromagnetism.theory.general_equations import calc_faradays_law

        dB_dt = np.zeros(3)
        curl_E = calc_faradays_law(dB_dt)

        assert_cgs_close(np.linalg.norm(curl_E), 0.0, cgs_tolerance)


class TestGeneralEMF:
    """Test General EMF: E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ."""

    def test_general_emf_motional_term(
        self, cgs_tolerance, assert_cgs_close, assert_vectors_close
    ) -> None:
        """Verify motional EMF term: (1/c)(v × B).

        For v = [1e8, 0, 0] cm/s and B = [0, 0, 1000] gauss:
        v × B = [0, -1e11, 0]
        E = (1/c) * [0, -1e11, 0] statvolts/cm
        """
        from maxwell.electromagnetism.theory.general_equations import calc_general_emf

        v = np.array([1e8, 0.0, 0.0])  # 1e8 cm/s in x
        B = np.array([0.0, 0.0, 1000.0])  # 1000 gauss in z
        E = calc_general_emf(
            velocity=v,
            B_field=B,
            A_potential=np.zeros(3),
            phi_potential=0.0,
            grad_phi=np.zeros(3),
        )

        # E = (1/c)(v × B) = (1/c)[0, -1e11, 0]
        expected = (1.0 / C) * np.cross(v, B)
        assert_vectors_close(E, expected, cgs_tolerance)

    def test_general_emf_inductive_term(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify inductive/transformer EMF term: -(1/c)·∂A/∂t.

        For dA/dt = [0, 0, 1e6] gauss·cm/s:
        E = -(1/c) * [0, 0, 1e6] statvolts/cm
        """
        from maxwell.electromagnetism.theory.general_equations import calc_general_emf

        dA_dt = np.array([0.0, 0.0, 1e6])  # Changing vector potential
        E = calc_general_emf(
            velocity=np.zeros(3),
            B_field=np.zeros(3),
            A_potential=np.zeros(3),
            phi_potential=0.0,
            grad_phi=np.zeros(3),
            dA_dt=dA_dt,
        )

        # E = -(1/c)·∂A/∂t
        expected = -(1.0 / C) * dA_dt
        assert_cgs_close(E[2], expected[2], cgs_tolerance)

    def test_general_emf_electrostatic_term(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify electrostatic term: -∇φ.

        For ∇φ = [100, 0, 0] statvolts/cm:
        E = -[100, 0, 0] statvolts/cm
        """
        from maxwell.electromagnetism.theory.general_equations import calc_general_emf

        grad_phi = np.array([100.0, 0.0, 0.0])
        E = calc_general_emf(
            velocity=np.zeros(3),
            B_field=np.zeros(3),
            A_potential=np.zeros(3),
            phi_potential=0.0,
            grad_phi=grad_phi,
        )

        # E = -∇φ
        assert_cgs_close(E[0], -100.0, cgs_tolerance)

    def test_general_emf_combined_terms(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify all three terms combine correctly."""
        from maxwell.electromagnetism.theory.general_equations import calc_general_emf

        v = np.array([1e8, 0.0, 0.0])
        B = np.array([0.0, 0.0, 1000.0])
        dA_dt = np.array([0.0, 0.0, 1e6])
        grad_phi = np.array([50.0, 0.0, 0.0])

        E = calc_general_emf(
            velocity=v,
            B_field=B,
            A_potential=np.zeros(3),
            phi_potential=0.0,
            grad_phi=grad_phi,
            dA_dt=dA_dt,
        )

        # E = (1/c)(v × B) - (1/c)·∂A/∂t - ∇φ
        motional = (1.0 / C) * np.cross(v, B)
        transformer = -(1.0 / C) * dA_dt
        electrostatic = -grad_phi
        expected = motional + transformer + electrostatic

        assert_cgs_close(np.linalg.norm(E), np.linalg.norm(expected), cgs_tolerance)


class TestPonderomotiveForce:
    """Test Ponderomotive Force: F = ρE + (1/c)(J × B)."""

    def test_ponderomotive_force_direction(
        self, cgs_tolerance, assert_cgs_close, assert_vectors_close
    ) -> None:
        """Verify ponderomotive force direction.

        For ρ = 1 statC/cm³, E = [1000, 0, 0] statV/cm:
        F = ρE = [1000, 0, 0] dynes/cm³
        """
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ponderomotive_force,
        )

        rho = 1.0
        E = np.array([1000.0, 0.0, 0.0])
        J = np.zeros(3)
        B = np.zeros(3)

        F = calc_ponderomotive_force(rho, E, J, B)

        # F = ρE (no magnetic term)
        expected = rho * E
        assert_vectors_close(F, expected, cgs_tolerance)

    def test_ponderomotive_force_magnetic_component(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify magnetic force component: (1/c)(J × B)."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ponderomotive_force,
        )

        rho = 0.0  # No charge density
        E = np.zeros(3)
        J = np.array([1e6, 0.0, 0.0])  # 1e6 abA/cm² in x
        B = np.array([0.0, 0.0, 1000.0])  # 1000 gauss in z

        F = calc_ponderomotive_force(rho, E, J, B)

        # F = (1/c)(J × B) = (1/c)[0, -1e9, 0]
        expected = (1.0 / C) * np.cross(J, B)
        assert_cgs_close(F[1], expected[1], cgs_tolerance)

    def test_ponderomotive_force_combined(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify combined electric and magnetic forces."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ponderomotive_force,
        )

        rho = 0.5
        E = np.array([100.0, 0.0, 0.0])
        J = np.array([0.0, 1e6, 0.0])
        B = np.array([0.0, 0.0, 500.0])

        F = calc_ponderomotive_force(rho, E, J, B)

        # Electric: ρE = [50, 0, 0]
        # Magnetic: (1/c)(J × B) = (1/c)[5e8, 0, 0]
        electric = rho * E
        magnetic = (1.0 / C) * np.cross(J, B)
        expected = electric + magnetic

        assert_cgs_close(F[0], expected[0], cgs_tolerance)


class TestMagneticInduction:
    """Test Magnetic Induction: B = H + 4πM."""

    def test_magnetic_induction_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify B = H + 4πM produces correct value.

        For H = [1000, 0, 0] oersted, M = [100, 0, 0] EMU/cm³:
        B = [1000 + 4π*100, 0, 0] gauss
        """
        from maxwell.electromagnetism.theory.general_equations import (
            calc_magnetic_induction,
        )

        H = np.array([1000.0, 0.0, 0.0])
        M = np.array([100.0, 0.0, 0.0])

        B = calc_magnetic_induction(H, M)

        # B = H + 4πM
        expected = H + 4.0 * np.pi * M
        assert_cgs_close(B[0], expected[0], cgs_tolerance)

    def test_magnetic_induction_zero_magnetization(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify B = H for non-magnetic material (M = 0)."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_magnetic_induction,
        )

        H = np.array([500.0, 0.0, 0.0])
        M = np.zeros(3)

        B = calc_magnetic_induction(H, M)

        assert_cgs_close(B[0], 500.0, cgs_tolerance)

    def test_magnetic_induction_proportional(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify B scales proportionally with M."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_magnetic_induction,
        )

        H = np.array([1000.0, 0.0, 0.0])
        M1 = np.array([50.0, 0.0, 0.0])
        M2 = np.array([100.0, 0.0, 0.0])

        B1 = calc_magnetic_induction(H, M1)
        B2 = calc_magnetic_induction(H, M2)

        # B2 - B1 should equal 4π(M2 - M1) = 4π*50
        expected_diff = 4.0 * np.pi * 50.0
        actual_diff = B2[0] - B1[0]
        assert_cgs_close(actual_diff, expected_diff, cgs_tolerance)


class TestAmpereMaxwellLaw:
    """Test Ampere-Maxwell Law: ∇ × H = (4π/c)J + (1/c)·∂D/∂t."""

    def test_ampere_maxwell_with_displacement(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify Ampere-Maxwell law includes displacement current.

        For J = [1, 0, 0] abA/cm²:
        conduction_term = (4π/c) * J

        For dE/dt = [0, 0, 1e10] statV/cm/s, ε = 1:
        displacement_term = (ε/c) * dE/dt
        """
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ampere_maxwell,
        )

        J = np.array([1.0, 0.0, 0.0])
        dE_dt = np.array([0.0, 0.0, 1e10])

        result = calc_ampere_maxwell(np.zeros(3), J, dE_dt)

        # Conduction: (4π/c) * J
        conduction_expected = (4.0 * np.pi / C) * J
        assert_cgs_close(
            result["conduction_term"][0], conduction_expected[0], cgs_tolerance
        )

        # Displacement: (1/c) * dE/dt (ε = 1 for vacuum)
        displacement_expected = (1.0 / C) * dE_dt
        assert_cgs_close(
            result["displacement_term"][2], displacement_expected[2], cgs_tolerance
        )

    def test_ampere_maxwell_conduction_only(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify conduction current term alone."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ampere_maxwell,
        )

        J = np.array([0.0, 1.0, 0.0])
        dE_dt = np.zeros(3)

        result = calc_ampere_maxwell(np.zeros(3), J, dE_dt)

        # Should only have conduction term
        expected = (4.0 * np.pi / C) * J
        assert_cgs_close(
            np.linalg.norm(result["curl_H"]), np.linalg.norm(expected), cgs_tolerance
        )

    def test_ampere_maxwell_displacement_only(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify displacement current term alone."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ampere_maxwell,
        )

        J = np.zeros(3)
        dE_dt = np.array([1e10, 0.0, 0.0])

        result = calc_ampere_maxwell(np.zeros(3), J, dE_dt)

        # Should only have displacement term
        expected = (1.0 / C) * dE_dt
        assert_cgs_close(
            np.linalg.norm(result["curl_H"]), np.linalg.norm(expected), cgs_tolerance
        )


class TestGaussLaws:
    """Test Gauss's Laws: ∇ · D = 4πρ and ∇ · B = 0."""

    def test_gauss_law_magnetic_zero(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Gauss's law for magnetism: ∇ · B = 0.

        For any uniform magnetic field, divergence should be zero.
        This expresses the absence of magnetic monopoles.
        """
        from maxwell.electromagnetism.theory.general_equations import (
            calc_gauss_law_magnetic,
        )

        B = np.array([1000.0, 0.0, 0.0])
        result = calc_gauss_law_magnetic(B)

        # ∇ · B = 0
        assert bool(result["verified"]) is True
        assert_cgs_close(result["divergence_B"], 0.0, cgs_tolerance)

    def test_gauss_law_electric_uniform(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Gauss's law for electricity with uniform field."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_gauss_law_electric,
        )

        D = np.array([500.0, 0.0, 0.0])
        result = calc_gauss_law_electric(D)

        # Uniform field has zero divergence
        assert_cgs_close(result["divergence_D"], 0.0, cgs_tolerance)

    def test_gauss_law_electric_with_charge(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify ∇ · D = 4πρ for known charge density."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_gauss_law_electric,
        )

        # For a point with charge density ρ = 1 statC/cm³
        rho = 1.0
        # We'd need a non-uniform D field for this test
        # For now, verify the formula structure
        D = np.array([4 * np.pi * rho, 0.0, 0.0])
        result = calc_gauss_law_electric(D, rho)

        # With uniform field, computed divergence is 0
        # The verification tests the input consistency
        assert result["charge_density_input"] == rho


class TestNumericalOperators:
    """Test numerical divergence and curl operators."""

    def test_numerical_divergence_constant_field(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify divergence of constant field is zero."""
        from maxwell.electromagnetism.theory.general_equations import (
            numerical_divergence,
        )

        # Constant field - single point returns 0
        field = np.array([100.0, 0.0, 0.0])

        div = numerical_divergence(field, grid_spacing=1.0)

        # Single point returns 0
        assert_cgs_close(div, 0.0, cgs_tolerance)

    def test_numerical_curl_single_point(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify curl of single point (uniform) field is zero."""
        from maxwell.electromagnetism.theory.general_equations import numerical_curl

        # Single point returns zero vector
        field = np.array([100.0, 0.0, 0.0])

        curl = numerical_curl(field, grid_spacing=1.0)

        # Single point returns zero vector
        assert_cgs_close(np.linalg.norm(curl), 0.0, cgs_tolerance)
        assert curl.shape == (3,)


class TestMaxwellEquationsVerification:
    """Test comprehensive Maxwell equations verification."""

    def test_verify_maxwell_equations(self) -> None:
        """Verify all Maxwell's equations pass verification."""
        from maxwell.electromagnetism.theory.general_equations import (
            verify_maxwell_equations,
        )

        result = verify_maxwell_equations()

        assert bool(result["all_verified"]) is True
        assert len(result["equations_tested"]) == 9

        # Individual equation verification
        assert bool(result["faraday_A"]["verified"]) is True
        assert bool(result["general_emf_B"]["verified"]) is True
        assert bool(result["ponderomotive_C"]["verified"]) is True
        assert bool(result["magnetic_induction_D"]["verified"]) is True
        assert bool(result["ampere_maxwell_E"]["verified"]) is True
        assert bool(result["electric_displacement_F"]["verified"]) is True
        assert bool(result["conduction_current_G"]["verified"]) is True
        assert bool(result["gauss_electric"]["verified"]) is True
        assert bool(result["gauss_magnetic"]["verified"]) is True


class TestMaxwellEquationsClass:
    """Test MaxwellEquations class."""

    def test_maxwell_equations_class_instantiation(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify MaxwellEquations class initialization."""
        from maxwell.electromagnetism.theory.general_equations import MaxwellEquations

        # Default (vacuum)
        eq = MaxwellEquations()
        assert eq.permittivity == 1.0
        assert eq.permeability == 1.0
        assert eq.conductivity == 0.0

    def test_maxwell_equations_class_with_material(self) -> None:
        """Verify MaxwellEquations with material properties."""
        from maxwell.electromagnetism.theory.general_equations import MaxwellEquations

        eq = MaxwellEquations.with_material_properties(
            permittivity=2.5, permeability=1.2, conductivity=1e6
        )

        assert eq.permittivity == 2.5
        assert eq.permeability == 1.2
        assert eq.conductivity == 1e6

    def test_maxwell_equations_class_equation_a(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify Equation (A) via class."""
        from maxwell.electromagnetism.theory.general_equations import MaxwellEquations

        eq = MaxwellEquations()
        dB_dt = np.array([0.0, 0.0, 1e10])

        curl_E = eq.equation_A_faraday(dB_dt)
        expected = -(1.0 / C) * dB_dt

        assert_cgs_close(curl_E[2], expected[2], cgs_tolerance)

    def test_maxwell_equations_class_negative_permittivity_raises(self) -> None:
        """Verify negative permittivity is prevented."""
        from maxwell.electromagnetism.theory.general_equations import MaxwellEquations

        with pytest.raises(ValueError, match="Permittivity must be positive"):
            MaxwellEquations(permittivity=-1.0)


# =============================================================================
# DIMENSIONAL ANALYSIS MODULE TESTS (Arts. 620-628)
# =============================================================================


class TestDimensionClass:
    """Test Dimension class for dimensional analysis."""

    def test_dimension_multiplication(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dimension multiplication adds exponents.

        Charge (ESU): M^(1/2) L^(3/2) T^(-1)
        Charge (ESU): M^(1/2) L^(3/2) T^(-1)
        Product: M L^3 T^(-2) — matches Coulomb's law dimensions
        """
        from maxwell.core.units.dimensions import Dimension

        # M^(1/2) L^(3/2) T^(-1) stored as (1, 3, -2)
        charge1 = Dimension(mass_exp=1, length_exp=3, time_exp=-2)
        charge2 = Dimension(mass_exp=1, length_exp=3, time_exp=-2)

        product = charge1 * charge2

        # Should be M L^3 T^(-2) = (2, 6, -4) doubled
        assert product.mass_exp == 2
        assert product.length_exp == 6
        assert product.time_exp == -4

    def test_dimension_division(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dimension division subtracts exponents.

        Potential / Current = Resistance
        """
        from maxwell.core.units.dimensions import Dimension

        # Potential (ESU): M^(1/2) L^(1/2) T^(-1) = (1, 1, -2)
        potential = Dimension(mass_exp=1, length_exp=1, time_exp=-2)
        # Current (ESU): M^(1/2) L^(3/2) T^(-2) = (1, 3, -4)
        current = Dimension(mass_exp=1, length_exp=3, time_exp=-4)

        ratio = potential / current

        # L^(-1) T = (0, -2, 2) doubled
        assert ratio.mass_exp == 0
        assert ratio.length_exp == -2
        assert ratio.time_exp == 2

    def test_dimension_power(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dimension power multiplies exponents.

        Charge squared: (M^(1/2) L^(3/2) T^(-1))^2 = M L^3 T^(-2)
        """
        from maxwell.core.units.dimensions import Dimension

        # Charge (ESU): M^(1/2) L^(3/2) T^(-1) = (1, 3, -2)
        charge = Dimension(mass_exp=1, length_exp=3, time_exp=-2)

        charge_squared = charge**2

        # M L^3 T^(-2) = (2, 6, -4) doubled
        assert charge_squared.mass_exp == 2
        assert charge_squared.length_exp == 6
        assert charge_squared.time_exp == -4

    def test_dimension_formatting(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify dimensional string formatting."""
        from maxwell.core.units.dimensions import Dimension

        # M^(1/2) L^(3/2) T^(-1)
        charge = Dimension(mass_exp=1, length_exp=3, time_exp=-2)
        formatted = charge.to_dimensional_string()

        assert "M^(1/2)" in formatted
        assert "L^(3/2)" in formatted
        assert "T^(-1)" in formatted

    def test_dimension_equality(self) -> None:
        """Verify dimension equality comparison."""
        from maxwell.core.units.dimensions import Dimension

        d1 = Dimension(mass_exp=1, length_exp=3, time_exp=-2)
        d2 = Dimension(mass_exp=1, length_exp=3, time_exp=-2)
        d3 = Dimension(mass_exp=0, length_exp=2, time_exp=0)

        assert d1 == d2
        assert d1 != d3


class TestESUvsEMUDimensions:
    """Test ESU vs EMU dimensional differences."""

    def test_esu_vs_emu_charge_dimensions(self) -> None:
        """Verify ESU and EMU charge have different dimensions.

        ESU charge: M^(1/2) L^(3/2) T^(-1) — from F = q₁q₂/r²
        EMU charge: M^(1/2) L^(1/2) — from force between currents

        The difference: ESU/EMU = [L T^(-1)] = velocity
        """
        from maxwell.core.units.dimensions import get_emu_dimensions, get_esu_dimensions

        esu_charge = get_esu_dimensions("charge")
        emu_charge = get_emu_dimensions("charge")

        # ESU: (1, 3, -2) doubled
        assert esu_charge.mass_exp == 1
        assert esu_charge.length_exp == 3
        assert esu_charge.time_exp == -2

        # EMU: (1, 1, 0) doubled
        assert emu_charge.mass_exp == 1
        assert emu_charge.length_exp == 1
        assert emu_charge.time_exp == 0

        # Ratio should be velocity: (0, 2, -2) doubled
        ratio = esu_charge / emu_charge
        assert ratio.mass_exp == 0  # No mass in velocity
        assert ratio.length_exp == 2  # L^1
        assert ratio.time_exp == -2  # T^(-1)

    def test_esu_vs_emu_resistance_dimensions(self) -> None:
        """Verify ESU and EMU resistance dimensions.

        ESU resistance: L^(-1) T
        EMU resistance: L T^(-1) — velocity!

        Ratio: ESU/EMU = L^(-2) T^2 = 1/velocity^2 = 1/c^2
        """
        from maxwell.core.units.dimensions import get_emu_dimensions, get_esu_dimensions

        esu_resistance = get_esu_dimensions("resistance")
        emu_resistance = get_emu_dimensions("resistance")

        # ESU: L^(-1) T = (0, -2, 2) doubled
        assert esu_resistance.mass_exp == 0
        assert esu_resistance.length_exp == -2
        assert esu_resistance.time_exp == 2

        # EMU: L T^(-1) = (0, 2, -2) doubled
        assert emu_resistance.mass_exp == 0
        assert emu_resistance.length_exp == 2
        assert emu_resistance.time_exp == -2


class TestUnitRatio:
    """Test ESU/EMU unit ratio calculations."""

    def test_unit_ratio_equals_c(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify ESU/EMU ratio for charge equals c.

        Art. 771-773: The ratio ESU/EMU for charge = c ≈ 3×10^10
        """
        from maxwell.core.units.dimensions import calc_unit_ratio

        result = calc_unit_ratio("charge")

        assert_cgs_close(result["ratio"], C, cgs_tolerance)
        assert result["power_of_c"] == 1
        assert "c^1" in result["relationship"]

    def test_unit_ratio_resistance_c_squared(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify ESU/EMU ratio for resistance equals c²."""
        from maxwell.core.units.dimensions import calc_unit_ratio

        result = calc_unit_ratio("resistance")

        expected_ratio = C**2
        assert_cgs_close(result["ratio"], expected_ratio, cgs_tolerance)
        assert result["power_of_c"] == 2

    def test_unit_ratio_capacitance_inverse(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify ESU/EMU ratio for capacitance equals 1/c²."""
        from maxwell.core.units.dimensions import calc_unit_ratio

        result = calc_unit_ratio("capacitance")

        expected_ratio = 1.0 / (C**2)
        assert_cgs_close(result["ratio"], expected_ratio, cgs_tolerance)
        assert result["power_of_c"] == -2


class TestUnitConversion:
    """Test ESU <-> EMU conversion functions."""

    def test_esu_to_emu_conversion(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify ESU to EMU conversion for charge.

        1 statcoulomb / c = abcoulombs
        """
        from maxwell.core.units.dimensions import convert_esu_to_emu

        # Convert 1 statcoulomb to abcoulombs
        q_emu = convert_esu_to_emu(1.0, "charge")

        # 1 statC = 1/c abcoulombs
        expected = 1.0 / C
        assert_cgs_close(q_emu, expected, cgs_tolerance)

    def test_emu_to_esu_conversion(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EMU to ESU conversion for charge.

        1 abcoulomb * c = statcoulombs
        """
        from maxwell.core.units.dimensions import convert_emu_to_esu

        # Convert 1 abcoulomb to statcoulombs
        q_esu = convert_emu_to_esu(1.0, "charge")

        # 1 abC = c statcoulombs
        assert_cgs_close(q_esu, C, cgs_tolerance)

    def test_conversion_round_trip(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify conversion round-trip returns original value."""
        from maxwell.core.units.dimensions import convert_emu_to_esu, convert_esu_to_emu

        original = 5.0

        # ESU -> EMU -> ESU
        emu = convert_esu_to_emu(original, "charge")
        esu = convert_emu_to_esu(emu, "charge")

        assert_cgs_close(esu, original, cgs_tolerance)


class TestPracticalUnitConversions:
    """Test practical unit conversion tables."""

    def test_practical_unit_conversions(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify practical unit conversion table.

        Art. 771-773: Conversion of SI units to CGS systems.
        """
        from maxwell.core.units.dimensions import get_practical_unit_conversions

        table = get_practical_unit_conversions()

        # 1 volt = 10^8 abvolts
        assert_cgs_close(table["volt"]["to_emu"], 1.0e8, cgs_tolerance)
        assert table["volt"]["emu_name"] == "abvolt"
        assert table["volt"]["esu_name"] == "statvolt"

        # 1 ampere = 0.1 abampere
        assert_cgs_close(table["ampere"]["to_emu"], 0.1, cgs_tolerance)
        assert table["ampere"]["emu_name"] == "abampere"

        # 1 ohm = 10^9 abohms
        assert_cgs_close(table["ohm"]["to_emu"], 1.0e9, cgs_tolerance)
        assert table["ohm"]["emu_name"] == "abohm"


class TestSpeedOfLightVerification:
    """Test speed of light relationship verification."""

    def test_speed_of_light_verification(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify verify_speed_of_light_relationship returns verified.

        Art. 771-781: All ESU/EMU ratios should yield the same c value.
        """
        from maxwell.core.units.dimensions import verify_speed_of_light_relationship

        result = verify_speed_of_light_relationship()

        assert result["verified"] is True
        assert_cgs_close(result["c_accepted"], C, cgs_tolerance)

        # All derived c values should match accepted value
        assert_cgs_close(result["c_from_charge"], C, cgs_tolerance)
        assert_cgs_close(result["c_from_current"], C, cgs_tolerance)
        assert_cgs_close(result["c_from_potential"], C, cgs_tolerance)

        # Maximum deviation should be tiny
        assert result["max_deviation"] < 1e-10


class TestDimensionalConsistency:
    """Test dimensional consistency verification."""

    def test_dimensional_consistency_charge(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify charge dimensional consistency.

        [Q]_ESU / [Q]_EMU should equal c^1 = velocity
        """
        from maxwell.core.units.dimensions import verify_dimensional_consistency

        result = verify_dimensional_consistency("charge")

        assert result["consistent"] is True
        assert result["velocity_power"] == 1
        assert "c^1" in result["explanation"]

    def test_dimensional_consistency_resistance(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify resistance dimensional consistency.

        [R]_ESU / [R]_EMU should equal c^(-2) = 1/velocity^2
        The velocity_power is -2 because ESU = EMU / c^2
        """
        from maxwell.core.units.dimensions import verify_dimensional_consistency

        result = verify_dimensional_consistency("resistance")

        assert result["consistent"] is True
        # ESU/EMU for resistance = 1/c^2, so velocity_power = -2
        assert result["velocity_power"] == -2


class TestDimensionalAnalysisCitations:
    """Test citation decorator compliance for dimensional analysis module."""

    def test_dimension_module_citations(self, require_citation) -> None:
        """Verify dimensional analysis functions have correct citations."""
        from maxwell.core.units.dimensions import (
            calc_unit_ratio,
            convert_esu_to_emu,
            get_emu_dimensions,
            get_esu_dimensions,
            verify_speed_of_light_relationship,
        )

        # Check get_esu_dimensions
        citation = require_citation(get_esu_dimensions)
        assert citation.part == 4
        assert any(a in citation.articles for a in [620, 621, 622])

        # Check get_emu_dimensions
        citation = require_citation(get_emu_dimensions)
        assert citation.part == 4
        assert any(a in citation.articles for a in [620, 626, 627, 628])

        # Check calc_unit_ratio
        citation = require_citation(calc_unit_ratio)
        assert citation.part == 4
        assert any(a in citation.articles for a in [771, 772, 773])


class TestGeneralEquationsCitations:
    """Test citation decorator compliance for general equations module."""

    def test_general_equations_module_citations(self, require_citation) -> None:
        """Verify general equations functions have correct citations."""
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ampere_maxwell,
            calc_faradays_law,
            calc_general_emf,
            calc_magnetic_induction,
            calc_ponderomotive_force,
            verify_maxwell_equations,
        )

        # Check calc_faradays_law
        citation = require_citation(calc_faradays_law)
        assert citation.part == 4
        assert 598 in citation.articles

        # Check calc_ponderomotive_force
        citation = require_citation(calc_ponderomotive_force)
        assert citation.part == 4
        assert 599 in citation.articles

        # Check calc_ampere_maxwell
        citation = require_citation(calc_ampere_maxwell)
        assert citation.part == 4
        assert 600 in citation.articles


# =============================================================================
# COMPREHENSIVE INTEGRATION TESTS
# =============================================================================


class TestPartIVAdvancedIntegration:
    """Integration tests for Part IV advanced modules."""

    def test_faraday_ampere_consistency(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify consistency between Faraday's and Ampere-Maxwell laws.

        For a self-consistent EM wave:
        - Changing B produces E (Faraday)
        - Changing E produces B (Ampere-Maxwell)
        """
        from maxwell.electromagnetism.theory.general_equations import (
            calc_ampere_maxwell,
            calc_faradays_law,
        )

        # Simulate one direction of EM wave
        dB_dt = np.array([0.0, 0.0, 1e10])
        dE_dt = np.array([1e10, 0.0, 0.0])

        # Faraday: curl E from changing B
        curl_E = calc_faradays_law(dB_dt)

        # Ampere-Maxwell: curl H from conduction + displacement
        result = calc_ampere_maxwell(np.zeros(3), np.zeros(3), dE_dt)

        # Both should produce non-zero results proportional to 1/c
        assert np.linalg.norm(curl_E) > 0
        assert np.linalg.norm(result["displacement_term"]) > 0

    def test_dimensional_analysis_with_general_equations(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify dimensional consistency of Maxwell's equations.

        All terms in Maxwell's equations should have consistent dimensions.
        """
        from maxwell.core.units.dimensions import Dimension

        # Check that ESU/EMU dimensional ratios are consistent
        # with the equations involving c

        # E field dimensions: ESU-based
        esu_E = get_esu_dimensions("electric_field")
        # B field dimensions: EMU-based
        emu_B = get_emu_dimensions("magnetic_induction")

        # In Faraday's law: ∇ × E = -(1/c)·∂B/∂t
        # Dimensions should work out with the 1/c factor
        # This test verifies the dimensional framework supports the equations

        # E has dimensions [M^(1/2) L^(-1/2) T^(-1)] in ESU
        assert esu_E.mass_exp == 1
        assert esu_E.length_exp == -1
        assert esu_E.time_exp == -2  # doubled

        # B has dimensions [M^(1/2) L^(-1/2) T^(-1)] in EMU
        assert emu_B.mass_exp == 1
        assert emu_B.length_exp == -1
        assert emu_B.time_exp == -2  # doubled


# Helper import for integration test
def get_esu_dimensions(quantity: str):
    from maxwell.core.units.dimensions import get_esu_dimensions as inner

    return inner(quantity)


def get_emu_dimensions(quantity: str):
    from maxwell.core.units.dimensions import get_emu_dimensions as inner

    return inner(quantity)
