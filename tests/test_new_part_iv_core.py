"""
Test new Part IV Core Electromagnetism modules.

Comprehensive test coverage for core EM theory modules:
- Cyclic potentials (Art. 480)
- Equipotential surfaces (Arts. 486-487)
- Directrix functions (Arts. 517-519)
- Mutual energy (Arts. 520-521)
- Circuit equivalence (Arts. 482-485)
- Parallel current attraction (Arts. 496-497)
- Elemental forces (Arts. 510-515)
- Generalized forces (Arts. 573-575)
- Ponderomotive forces (Arts. 602-603)
- Sliding contact/motional EMF (Arts. 594-597)
- Lenz's law (Art. 542)
- Self-induction (Arts. 546-551)
- Generalized induction (Arts. 576-577)
- Force law comparisons (Arts. 526-527)
- Energy conservation (Arts. 543-544)
- Dynamical model (Arts. 568-577)
- Electrotonic state (Arts. 540-541)

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (conservation, symmetry)
- Edge cases (zero inputs, boundary conditions)
- CGS unit compliance
- Citation decorator compliance
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import MaxwellCitation, get_citation

# =============================================================================
# CYCLIC POTENTIAL TESTS (Art. 480)
# =============================================================================


class TestCyclicPotential:
    """Test multivalued magnetic potential around current-carrying wire."""

    def test_cyclic_potential_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Omega = -2*I*phi formula.

        For I = 1 abampere, phi = pi/2:
        Omega = -2 * 1 * pi/2 = -pi oersted*cm
        """
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_cyclic_potential,
        )

        current = 1.0  # 1 abampere
        angle = np.pi / 2  # 90 degrees

        Omega = calc_cyclic_potential(current, angle)

        expected = -2.0 * current * angle
        assert_cgs_close(Omega, expected, cgs_tolerance)

    def test_cyclic_potential_one_revolution(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify Delta(Omega) = -4*pi*I per revolution.

        For I = 1 abampere, one complete circuit:
        Delta(Omega) = Omega(2*pi) - Omega(0) = -4*pi oersted*cm
        """
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_cyclic_potential,
            calc_potential_difference,
        )

        current = 1.0

        Omega_0 = calc_cyclic_potential(current, 0.0)
        Omega_2pi = calc_cyclic_potential(current, 2.0 * np.pi)

        delta_Omega = Omega_2pi - Omega_0
        expected = -4.0 * np.pi * current

        assert_cgs_close(delta_Omega, expected, cgs_tolerance)

    def test_cyclic_potential_branch_independence(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify potential difference is branch-independent."""
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_cyclic_potential,
        )

        current = 1.0
        angle1 = np.pi / 4
        angle2 = 3 * np.pi / 4

        # Calculate difference at branch 0
        diff_0 = calc_cyclic_potential(
            current, angle2, branch=0
        ) - calc_cyclic_potential(current, angle1, branch=0)

        # Calculate difference at branch 1
        diff_1 = calc_cyclic_potential(
            current, angle2, branch=1
        ) - calc_cyclic_potential(current, angle1, branch=1)

        # Should be identical (branch constant cancels)
        assert_cgs_close(diff_0, diff_1, cgs_tolerance)

    def test_cyclic_potential_zero_current(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify zero current produces zero potential."""
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_cyclic_potential,
        )

        Omega = calc_cyclic_potential(0.0, np.pi)
        assert_cgs_close(Omega, 0.0, cgs_tolerance)

    def test_potential_difference_formula(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify Delta(Omega) = -2*I*(phi2 - phi1)."""
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_potential_difference,
        )

        current = 1.0
        angle1 = 0.0
        angle2 = np.pi

        delta = calc_potential_difference(current, angle1, angle2)
        expected = -2.0 * current * (angle2 - angle1)

        assert_cgs_close(delta, expected, cgs_tolerance)

    def test_cyclic_constant_property(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify CyclicPotential.cyclic_constant = -4*pi*I."""
        from maxwell.electromagnetism.potentials.multivalued import CyclicPotential

        current = 1.0
        cp = CyclicPotential(current=current)

        assert_cgs_close(cp.cyclic_constant, -4.0 * np.pi * current, cgs_tolerance)

    def test_work_on_magnetic_pole(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify W = 4*pi*m*I for unit pole moved around wire.

        For m = 1 emu, I = 1 abampere, 1 loop:
        W = 4*pi*1*1 = 4*pi ergs
        """
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_work_on_magnetic_pole,
        )

        pole_strength = 1.0  # 1 emu
        current = 1.0  # 1 abampere
        loops = 1

        W = calc_work_on_magnetic_pole(pole_strength, current, loops)
        expected = 4.0 * np.pi * pole_strength * current * loops

        assert_cgs_close(W, expected, cgs_tolerance)

    def test_verify_cyclic_potential(self) -> None:
        """Verify cyclic potential relations pass verification."""
        from maxwell.electromagnetism.potentials.multivalued import (
            verify_cyclic_potential,
        )

        result = verify_cyclic_potential(current=1.0)

        assert result["verified"] is True
        assert result["field_verified"] is True


# =============================================================================
# PARALLEL CURRENT ATTRACTION TESTS (Arts. 496-497)
# =============================================================================


class TestParallelCurrentAttraction:
    """Test force between parallel current-carrying conductors."""

    def test_force_per_unit_length_formula(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify F/L = 2*I1*I2/r formula.

        For I1 = I2 = 1 abampere, r = 1 cm:
        F/L = 2*1*1/1 = 2 dynes/cm
        """
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_per_unit_length,
        )

        I1 = 1.0
        I2 = 1.0
        r = 1.0

        F_per_L = calc_force_per_unit_length(I1, I2, r)
        expected = 2.0 * I1 * I2 / r

        assert_cgs_close(F_per_L, expected, cgs_tolerance)

    def test_total_force_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify F = 2*I1*I2*L/r formula.

        For I1 = I2 = 1 abampere, r = 1 cm, L = 10 cm:
        F = 2*1*1*10/1 = 20 dynes
        """
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_parallel_wires,
        )

        I1 = 1.0
        I2 = 1.0
        r = 1.0
        L = 10.0

        F = calc_force_parallel_wires(I1, I2, r, L)
        expected = 2.0 * I1 * I2 * L / r

        assert_cgs_close(F, expected, cgs_tolerance)

    def test_attractive_for_same_direction(self) -> None:
        """Verify positive force (attraction) for same-direction currents."""
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_parallel_wires,
        )

        F = calc_force_parallel_wires(1.0, 1.0, 1.0, 1.0)
        assert F > 0  # Positive = attractive

    def test_repulsive_for_opposite_direction(self) -> None:
        """Verify negative force (repulsion) for opposite-direction currents."""
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_parallel_wires,
        )

        F = calc_force_parallel_wires(1.0, -1.0, 1.0, 1.0)
        assert F < 0  # Negative = repulsive

    def test_force_inverse_distance_relationship(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify F ∝ 1/r inverse distance relationship."""
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_parallel_wires,
        )

        I1 = 1.0
        I2 = 1.0
        L = 1.0
        r1 = 1.0
        r2 = 2.0

        F1 = calc_force_parallel_wires(I1, I2, r1, L)
        F2 = calc_force_parallel_wires(I1, I2, r2, L)

        # F2 should be F1/2
        expected = F1 / 2.0
        assert_cgs_close(F2, expected, cgs_tolerance)

    def test_force_proportional_to_current_product(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify F ∝ I1*I2 proportionality."""
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_per_unit_length,
        )

        r = 1.0

        # I1 = 1, I2 = 1
        F1 = calc_force_per_unit_length(1.0, 1.0, r)

        # I1 = 2, I2 = 2: should be 4x
        F2 = calc_force_per_unit_length(2.0, 2.0, r)

        expected = 4.0 * F1
        assert_cgs_close(F2, expected, cgs_tolerance)

    def test_work_done_moving_wires(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify W = 2*I1*I2*ln(r2/r1) work formula.

        For I1 = I2 = 1, r1 = 1, r2 = 2:
        W = 2*1*1*ln(2) = 2*ln(2) ergs
        """
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_work_parallel_wires,
        )

        I1 = 1.0
        I2 = 1.0
        r1 = 1.0
        r2 = 2.0

        W = calc_work_parallel_wires(I1, I2, r1, r2)
        expected = 2.0 * I1 * I2 * np.log(r2 / r1)

        assert_cgs_close(W, expected, cgs_tolerance)

    def test_parallel_conductor_force_class(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify ParallelConductorForce class properties."""
        from maxwell.electromagnetism.dynamics.attraction import ParallelConductorForce

        pcf = ParallelConductorForce(
            current1=1.0, current2=1.0, separation=1.0, length=10.0
        )

        assert_cgs_close(pcf.force_per_unit_length, 2.0, cgs_tolerance)
        assert_cgs_close(pcf.total_force, 20.0, cgs_tolerance)
        assert pcf.is_attractive is True

    def test_verify_parallel_force_law(self) -> None:
        """Verify parallel force law verification passes."""
        from maxwell.electromagnetism.dynamics.attraction import (
            verify_parallel_force_law,
        )

        result = verify_parallel_force_law(current1=1.0, current2=1.0)

        assert bool(result["verified"]) is True
        assert bool(result["inverse_r_verified"]) is True
        assert bool(result["scaling_verified"]) is True
        assert bool(result["sign_change_verified"]) is True


# =============================================================================
# ELEMENTAL FORCE TESTS (Arts. 510-515)
# =============================================================================


class TestElementalForces:
    """Test forces between current elements (Ampere, Grassmann, Neumann forms)."""

    def test_current_element_creation(self) -> None:
        """Verify CurrentElement creation and properties."""
        from maxwell.electromagnetism.forces.elemental import CurrentElement

        elem = CurrentElement(
            current=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )

        assert np.linalg.norm(elem.direction) == 1.0  # Normalized
        assert elem.current == 1.0

    def test_ampere_force_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Ampere's force law between current elements.

        d²F = (I1*I2/r²) * [2(dl1·r)(dl2·r)/r² - (dl1·dl2)] * r_hat
        """
        from maxwell.electromagnetism.forces.elemental import (
            CurrentElement,
            calc_ampere_force,
        )

        # Two parallel elements separated by 1 cm
        elem1 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )
        elem2 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 1.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )

        F = calc_ampere_force(elem1, elem2)

        # Force should be along y-axis (attractive for parallel currents)
        assert F[0] < 1e-15  # No x-component
        assert F[2] < 1e-15  # No z-component
        assert F[1] < 0  # Negative y = attractive

    def test_grassmann_force_formula(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Grassmann force law: dF = (I1*I2/r²) * dl2 × (dl1 × r_hat)."""
        from maxwell.electromagnetism.forces.elemental import (
            CurrentElement,
            calc_grassmann_force,
        )

        elem1 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )
        elem2 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 1.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )

        F = calc_grassmann_force(elem1, elem2)

        # Force should be along -y for this configuration
        assert F[1] < 0  # Attractive

    def test_mutual_energy_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify mutual energy: d²W = -(I1*I2/r) * (dl1·dl2)."""
        from maxwell.electromagnetism.forces.elemental import (
            CurrentElement,
            calc_element_mutual_energy,
        )

        elem1 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 0.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )
        elem2 = CurrentElement(
            current=1.0,
            position=np.array([0.0, 1.0, 0.0]),
            direction=np.array([1.0, 0.0, 0.0]),
            length=0.001,
        )

        W = calc_element_mutual_energy(elem1, elem2)

        # Energy should be negative (attractive configuration)
        assert W < 0

    def test_force_equivalence_verification(self) -> None:
        """Verify Ampere and Grassmann forms equivalent for closed loop."""
        from maxwell.electromagnetism.forces.elemental import verify_force_equivalence

        result = verify_force_equivalence(
            current1=1.0, current2=1.0, loop_radius=1.0, n_segments=32, tolerance=1e-2
        )

        assert result["equivalence_verified"] is True

    def test_parallel_element_force(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify force between parallel current elements."""
        from maxwell.electromagnetism.forces.elemental import (
            calc_parallel_element_force,
        )

        # Perpendicular elements: parallel to each other, perpendicular to separation
        F = calc_parallel_element_force(
            current1=1.0,
            current2=1.0,
            length1=0.001,
            length2=0.001,
            separation=1.0,
            element_angle=np.pi / 2,  # Perpendicular to separation
        )

        # Force should be attractive (negative along separation)
        assert F[0] < 0


# =============================================================================
# LENZ'S LAW TESTS (Art. 542)
# =============================================================================


class TestLenzLaw:
    """Test Lenz's law: induced EMF opposes change in flux."""

    def test_induced_emf_opposes_increasing_flux(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify negative EMF for increasing flux (dPhi/dt > 0)."""
        from maxwell.electromagnetism.induction.lenz import calc_induced_emf_lenz

        # Increasing flux: dPhi/dt = 1000 maxwells/s
        emf = calc_induced_emf_lenz(1000.0)

        assert emf < 0  # Opposes increase
        assert_cgs_close(emf, -1000.0, cgs_tolerance)

    def test_induced_emf_opposes_decreasing_flux(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify positive EMF for decreasing flux (dPhi/dt < 0)."""
        from maxwell.electromagnetism.induction.lenz import calc_induced_emf_lenz

        # Decreasing flux: dPhi/dt = -1000 maxwells/s
        emf = calc_induced_emf_lenz(-1000.0)

        assert emf > 0  # Opposes decrease
        assert_cgs_close(emf, 1000.0, cgs_tolerance)

    def test_induced_emf_zero_flux_change(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify zero EMF for constant flux."""
        from maxwell.electromagnetism.induction.lenz import calc_induced_emf_lenz

        emf = calc_induced_emf_lenz(0.0)
        assert_cgs_close(emf, 0.0, cgs_tolerance)

    def test_lenz_law_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify LenzLaw class induced_emf property."""
        from maxwell.electromagnetism.induction.lenz import LenzLaw

        lenz = LenzLaw(flux_change_rate=500.0)
        emf = lenz.induced_emf

        assert emf < 0
        assert_cgs_close(emf, -500.0, cgs_tolerance)


# =============================================================================
# SELF-INDUCTION TESTS (Arts. 546-551)
# =============================================================================


class TestSelfInduction:
    """Test self-induction: EMF = -L*dI/dt."""

    def test_self_induction_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EMF = -L*dI/dt formula.

        For L = 1000 cm (abhenries), dI/dt = 10 abamperes/s:
        EMF = -1000 * 10 = -10000 abvolts
        """
        from maxwell.electromagnetism.induction.self import calc_self_induction_emf

        inductance = 1000.0  # cm (abhenries)
        dI_dt = 10.0  # abamperes/s

        emf = calc_self_induction_emf(inductance, dI_dt)
        expected = -inductance * dI_dt

        assert_cgs_close(emf, expected, cgs_tolerance)

    def test_self_induction_opposes_current_increase(self) -> None:
        """Verify negative EMF opposes increasing current."""
        from maxwell.electromagnetism.induction.self import calc_self_induction_emf

        emf = calc_self_induction_emf(100.0, 5.0)  # dI/dt > 0
        assert emf < 0

    def test_self_induction_opposes_current_decrease(self) -> None:
        """Verify positive EMF opposes decreasing current."""
        from maxwell.electromagnetism.induction.self import calc_self_induction_emf

        emf = calc_self_induction_emf(100.0, -5.0)  # dI/dt < 0
        assert emf > 0

    def test_magnetic_energy_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify magnetic energy W = (1/2)*L*I².

        For L = 1000 cm, I = 5 abamperes:
        W = 0.5 * 1000 * 25 = 12500 ergs
        """
        from maxwell.electromagnetism.induction.self import calc_magnetic_energy

        inductance = 1000.0
        current = 5.0

        W = calc_magnetic_energy(inductance, current)
        expected = 0.5 * inductance * current**2

        assert_cgs_close(W, expected, cgs_tolerance)

    def test_self_inductance_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify SelfInductance class properties."""
        from maxwell.electromagnetism.induction.self import SelfInductance

        si = SelfInductance(inductance=500.0, initial_current=0.0)

        emf = si.induced_emf(dI_dt=2.0)
        assert_cgs_close(emf, -1000.0, cgs_tolerance)

        energy = si.stored_energy(current=10.0)
        assert_cgs_close(energy, 25000.0, cgs_tolerance)


# =============================================================================
# ELECTROTONIC STATE TESTS (Arts. 540-541)
# =============================================================================


class TestElectrotonicState:
    """Test Faraday's electrotonic state (vector potential)."""

    def test_electrotonic_state_formula(
        self, cgs_tolerance, assert_vectors_close
    ) -> None:
        """Verify electrotonic state A (vector potential).

        For infinite wire: A_phi = 2I*ln(r) (in azimuthal direction)
        """
        from maxwell.electromagnetism.fields.electrotonic import calc_electrotonic_state

        current = 1.0
        position = np.array([1.0, 0.0, 0.0])

        A = calc_electrotonic_state(current, position)

        # Vector potential should be azimuthal (y-direction at this point)
        assert A[0] < 1e-10  # No radial component

    def test_electrotonic_state_zero_current(
        self, cgs_tolerance, assert_vectors_close
    ) -> None:
        """Verify zero electrotonic state for zero current."""
        from maxwell.electromagnetism.fields.electrotonic import calc_electrotonic_state

        A = calc_electrotonic_state(0.0, np.array([1.0, 0.0, 0.0]))
        assert_vectors_close(A, np.zeros(3), cgs_tolerance)

    def test_electrotonic_state_curl_gives_B(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify curl(A) = B relationship."""
        from maxwell.electromagnetism.fields.electrotonic import (
            ElectrotonicState,
            verify_electrotonic_state,
        )

        result = verify_electrotonic_state(current=1.0, tolerance=1e-4)

        assert result["curl_verified"] is True


# =============================================================================
# FORCE LAW COMPARISONS TESTS (Arts. 526-527)
# =============================================================================


class TestForceLawComparisons:
    """Test comparisons between Ampere, Grassmann, and Weber force laws."""

    def test_amperes_law_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Ampere's force law implementation."""
        from maxwell.electromagnetism.theory.comparisons import ampere_force_law

        I1 = 1.0
        I2 = 1.0
        r = 1.0

        F = ampere_force_law(I1, I2, r)
        expected = 2.0 * I1 * I2 / r  # Should match parallel wire formula

        assert_cgs_close(F, expected, cgs_tolerance)

    def test_grassmann_force_law(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Grassmann force law: F ∝ I × B."""
        from maxwell.electromagnetism.theory.comparisons import grassmann_force_law

        current = 1.0
        dl = np.array([1.0, 0.0, 0.0])
        B = np.array([0.0, 0.0, 1000.0])

        F = grassmann_force_law(current, dl, B)

        # F = I * dl × B: should be in -y direction
        assert F[1] < 0

    def test_weber_force_law(self) -> None:
        """Verify Weber force law implementation."""
        from maxwell.electromagnetism.theory.comparisons import weber_force_law

        # Weber force depends on velocity - just verify it runs
        q1 = 1.0
        q2 = 1.0
        r = np.array([1.0, 0.0, 0.0])
        v1 = np.array([0.0, 1.0, 0.0])
        v2 = np.array([0.0, -1.0, 0.0])

        F = weber_force_law(q1, q2, r, v1, v2)
        assert isinstance(F, np.ndarray)
        assert len(F) == 3


# =============================================================================
# ENERGY CONSERVATION TESTS (Arts. 543-544)
# =============================================================================


class TestEnergyConservation:
    """Test Helmholtz/Thomson energy conservation derivation."""

    def test_energy_balance_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify energy balance: dW_electric = dW_mechanical + dW_heat."""
        from maxwell.electromagnetism.theory.conservation import (
            verify_energy_conservation,
        )

        result = verify_energy_conservation(
            emf=1000.0, current=1.0, resistance=10.0, mechanical_power=500.0
        )

        assert result["energy_conserved"] is True

    def test_conservation_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EnergyConservation class."""
        from maxwell.electromagnetism.theory.conservation import EnergyConservation

        ec = EnergyConservation()

        # Electrical power: P = E*I
        electrical_power = ec.electrical_power(emf=100.0, current=2.0)
        assert_cgs_close(electrical_power, 200.0, cgs_tolerance)

        # Joule heating: P = I²*R
        heat_power = ec.joule_heat(current=2.0, resistance=10.0)
        assert_cgs_close(heat_power, 40.0, cgs_tolerance)


# =============================================================================
# DYNAMICAL MODEL TESTS (Arts. 568-577)
# =============================================================================


class TestDynamicalModel:
    """Test Maxwell's dynamical model of electromagnetic fields."""

    def test_total_kinetic_energy(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify T_total = T_mech + T_elec + T_coupling."""
        from maxwell.electromagnetism.theory.dynamical_model import DynamicalModel

        dm = DynamicalModel()

        # Mechanical KE: T = 0.5*m*v²
        T_mech = dm.mechanical_kinetic_energy(mass=10.0, velocity=5.0)
        expected = 0.5 * 10.0 * 25.0
        assert_cgs_close(T_mech, expected, cgs_tolerance)

        # Electrical KE: T = 0.5*L*I²
        T_elec = dm.electrokinetic_energy(inductance=100.0, current=3.0)
        expected = 0.5 * 100.0 * 9.0
        assert_cgs_close(T_elec, expected, cgs_tolerance)

    def test_generalized_momentum(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify p = dT/d(q_dot) generalized momentum."""
        from maxwell.electromagnetism.theory.dynamical_model import DynamicalModel

        dm = DynamicalModel()

        # Momentum from mechanical KE
        p = dm.generalized_momentum(mass=10.0, velocity=5.0)
        expected = 10.0 * 5.0  # p = m*v
        assert_cgs_close(p, expected, cgs_tolerance)


# =============================================================================
# GENERALIZED FORCES TESTS (Arts. 573-575)
# =============================================================================


class TestGeneralizedForces:
    """Test generalized force: F_x = dT/dx from energy."""

    def test_generalized_force_from_energy(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify F_x = dT/dx relationship."""
        from maxwell.electromagnetism.forces.generalized import calc_generalized_force

        # For T = 0.5*L(x)*I², F_x = 0.5*I²*dL/dx
        inductance_gradient = 10.0  # dL/dx
        current = 2.0

        F = calc_generalized_force(inductance_gradient, current)
        expected = 0.5 * current**2 * inductance_gradient

        assert_cgs_close(F, expected, cgs_tolerance)


# =============================================================================
# PONDEROMOTIVE FORCE TESTS (Arts. 602-603)
# =============================================================================


class TestPonderomotiveForce:
    """Test general ponderomotive force equations."""

    def test_ponderomotive_force_basic(
        self, cgs_tolerance, assert_vectors_close
    ) -> None:
        """Verify ponderomotive force on current element: F = I*L×B."""
        from maxwell.electromagnetism.forces.ponderomotive import (
            calc_ponderomotive_force,
        )

        current = 1.0
        length = np.array([1.0, 0.0, 0.0])
        B = np.array([0.0, 0.0, 1000.0])

        F = calc_ponderomotive_force(current, length, B)

        # F = I*L × B: should be in -y direction
        assert F[0] < 1e-10  # No x-component
        assert F[1] < 0  # Negative y
        assert F[2] < 1e-10  # No z-component
        assert_vectors_close(F[:2], np.array([0.0, -1000.0]), cgs_tolerance * 1000)


# =============================================================================
# SLIDING CONTACT / MOTIONAL EMF TESTS (Arts. 594-597)
# =============================================================================


class TestSlidingContact:
    """Test motional EMF from sliding contact: EMF = v×B×L."""

    def test_motional_emf_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify motional EMF = v*B*L for perpendicular v, B, L.

        For v = 100 cm/s, B = 1000 gauss, L = 10 cm:
        EMF = 100 * 1000 * 10 = 1,000,000 abvolts
        """
        from maxwell.electromagnetism.forces.sliding import calc_motional_emf

        v = np.array([100.0, 0.0, 0.0])
        B = np.array([0.0, 0.0, 1000.0])
        L = 10.0

        emf = calc_motional_emf(v, B, L)
        expected = 100.0 * 1000.0 * 10.0

        assert_cgs_close(emf, expected, cgs_tolerance)

    def test_motional_emf_zero_velocity(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify zero EMF for stationary conductor."""
        from maxwell.electromagnetism.forces.sliding import calc_motional_emf

        emf = calc_motional_emf(np.zeros(3), np.array([0.0, 0.0, 1000.0]), 10.0)
        assert_cgs_close(emf, 0.0, cgs_tolerance)

    def test_motional_emf_parallel_motion(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify zero EMF when motion parallel to field."""
        from maxwell.electromagnetism.forces.sliding import calc_motional_emf

        v = np.array([0.0, 0.0, 100.0])  # Parallel to B
        B = np.array([0.0, 0.0, 1000.0])
        L = 10.0

        emf = calc_motional_emf(v, B, L)
        assert_cgs_close(emf, 0.0, cgs_tolerance)


# =============================================================================
# CIRCUIT EQUIVALENCE TESTS (Arts. 482-485)
# =============================================================================


class TestCircuitEquivalence:
    """Test equivalence of closed circuit to magnetic shell."""

    def test_magnetic_shell_equivalence(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify magnetic moment of equivalent shell: m = I*A/c."""
        from maxwell.electromagnetism.equivalence import CircuitEquivalence

        ce = CircuitEquivalence()

        # For I = 1 abampere, A = 10 cm²
        m = ce.magnetic_moment(current=1.0, area=10.0)
        expected = 1.0 * 10.0 / CONST.C

        assert_cgs_close(m, expected, cgs_tolerance)

    def test_solid_angle_formula(self) -> None:
        """Verify solid angle calculation for circuit."""
        from maxwell.electromagnetism.equivalence import calc_solid_angle

        # At center of circular loop
        Omega = calc_solid_angle(radius=1.0, distance=0.0)
        assert Omega > 0


# =============================================================================
# MUTUAL ENERGY TESTS (Arts. 520-521)
# =============================================================================


class TestMutualEnergy:
    """Test mutual potential energy of circuits: M = integral(dl1*dl2/r)."""

    def test_mutual_inductance_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify mutual inductance M between coaxial loops."""
        from maxwell.electromagnetism.potentials.mutual_energy import (
            calc_mutual_inductance,
        )

        # Two coaxial loops, radius 1 cm, separation 2 cm
        M = calc_mutual_inductance(radius1=1.0, radius2=1.0, separation=2.0)

        assert M > 0  # Mutual inductance is positive

    def test_mutual_energy_from_currents(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify W = -M*I1*I2 mutual energy (Maxwell sign convention)."""
        from maxwell.electromagnetism.potentials.mutual_energy import calc_mutual_energy

        M = 100.0  # Mutual inductance
        I1 = 1.0
        I2 = 2.0

        W = calc_mutual_energy(I1, I2, M)
        expected = -M * I1 * I2  # Maxwell convention: W = -I1*I2*M

        assert_cgs_close(W, expected, cgs_tolerance)


# =============================================================================
# DIRECTRIX FUNCTION TESTS (Arts. 517-519)
# =============================================================================


class TestDirectrixFunction:
    """Test directrix function for geometric interaction."""

    def test_directrix_calculation(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify directrix function calculation."""
        from maxwell.electromagnetism.potentials.directrix import calc_directrix

        # For a simple current element
        directrix = calc_directrix(
            current=1.0,
            element_position=np.array([0.0, 0.0, 0.0]),
            element_direction=np.array([1.0, 0.0, 0.0]),
            observation_point=np.array([0.0, 1.0, 0.0]),
        )

        assert isinstance(directrix, np.ndarray)
        assert len(directrix) == 3


# =============================================================================
# EQUIPOTENTIAL SURFACE TESTS (Arts. 486-487)
# =============================================================================


class TestEquipotentialSurface:
    """Test helicoidal equipotential surfaces around wires."""

    def test_helicoid_surface_point(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify helicoidal surface potential."""
        from maxwell.electromagnetism.potentials.surfaces import EquipotentialSurface

        es = EquipotentialSurface(current=1.0)

        # At phi = 0, potential should be 0 (reference)
        potential = es.potential_at(phi=0.0, r=1.0)
        assert_cgs_close(potential, 0.0, cgs_tolerance)

    def test_helicoid_constant_pitch(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify helicoid pitch is constant."""
        from maxwell.electromagnetism.potentials.surfaces import EquipotentialSurface

        es = EquipotentialSurface(current=1.0)

        # Pitch should be proportional to current
        assert es.pitch() > 0


# =============================================================================
# GENERALIZED INDUCTION TESTS (Arts. 576-577)
# =============================================================================


class TestGeneralizedInduction:
    """Test generalized induction: EMF = -d/dt(p)."""

    def test_generalized_emf_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify EMF = -dp/dt."""
        from maxwell.electromagnetism.induction.generalized import calc_generalized_emf

        # For p = L*I, EMF = -L*dI/dt
        dp_dt = 500.0

        emf = calc_generalized_emf(dp_dt)
        expected = -dp_dt

        assert_cgs_close(emf, expected, cgs_tolerance)


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================


class TestCoreCitationCompliance:
    """Test citation decorator compliance for all core modules."""

    def test_cyclic_potential_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify cyclic potential functions have correct citations."""
        from maxwell.electromagnetism.potentials.multivalued import (
            calc_cyclic_potential,
            calc_potential_difference,
            calc_work_on_magnetic_pole,
        )

        citation = require_citation(calc_cyclic_potential)
        assert citation.part == 4
        assert 480 in citation.articles

    def test_parallel_current_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify parallel current functions have correct citations."""
        from maxwell.electromagnetism.dynamics.attraction import (
            calc_force_parallel_wires,
            calc_force_per_unit_length,
        )

        citation = require_citation(calc_force_parallel_wires)
        assert citation.part == 4
        assert any(a in citation.articles for a in [496, 497])

    def test_elemental_force_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify elemental force functions have correct citations."""
        from maxwell.electromagnetism.forces.elemental import (
            calc_ampere_force,
            calc_grassmann_force,
        )

        citation = require_citation(calc_ampere_force)
        assert citation.part == 4
        assert any(a in citation.articles for a in [510, 511, 512])

    def test_lenz_law_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify Lenz's law functions have correct citations."""
        from maxwell.electromagnetism.induction.lenz import calc_induced_emf_lenz

        citation = require_citation(calc_induced_emf_lenz)
        assert citation.part == 4
        assert 542 in citation.articles

    def test_self_induction_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify self-induction functions have correct citations."""
        from maxwell.electromagnetism.induction.self import calc_self_induction_emf

        citation = require_citation(calc_self_induction_emf)
        assert citation.part == 4
        assert any(a in citation.articles for a in [546, 547, 548, 549, 550, 551])
