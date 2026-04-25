"""
Test Part IV Electromagnetism modules.

Comprehensive test coverage for the 4 new Part IV modules:
1. Oersted's discovery (Arts. 475-479) — magnetic field from current
2. Faraday's induction (Arts. 528-531) — electromagnetic induction
3. Lorentz force (Arts. 490-492) — force on currents and charges
4. Ampere-Maxwell law (Arts. 606-607) — displacement current

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (proportionality, direction)
- Edge cases (zero inputs, singularities)
- Citation decorator compliance
"""

from __future__ import annotations

import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import get_citation, MaxwellCitation


# =============================================================================
# OERSTED MODULE TESTS (Arts. 475-479)
# =============================================================================

class TestOerstedFieldFormula:
    """Test Oersted's field formula H = 2I/r."""

    def test_oersted_field_formula(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify H = 2I/r produces correct numeric value.

        For I = 1 abampere, r = 1 cm:
        H = 2 * 1 / 1 = 2 oersted
        """
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        current = 1.0  # 1 abampere
        distance = 1.0  # 1 cm

        H = calc_oersted_field(current, distance)

        # H = 2I/r = 2 oersted
        assert_cgs_close(H, 2.0, cgs_tolerance)

    def test_oersted_field_doubles_with_current(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify H(2I) = 2 * H(I) — linear proportionality with current."""
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        distance = 1.0  # 1 cm
        I1 = 1.0
        I2 = 2.0

        H1 = calc_oersted_field(I1, distance)
        H2 = calc_oersted_field(I2, distance)

        # H2 should be exactly 2 * H1
        expected = 2.0 * H1
        assert_cgs_close(H2, expected, cgs_tolerance)

    def test_oersted_field_halves_with_distance(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify H(2r) = H(r)/2 — inverse distance relationship."""
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        current = 1.0  # 1 abampere
        r1 = 1.0
        r2 = 2.0

        H1 = calc_oersted_field(current, r1)
        H2 = calc_oersted_field(current, r2)

        # H2 should be exactly H1/2
        expected = H1 / 2.0
        assert_cgs_close(H2, expected, cgs_tolerance)

    def test_oersted_field_zero_distance_raises(
        self
    ) -> None:
        """Verify division by zero is prevented."""
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        with pytest.raises(ValueError, match="Distance must be positive"):
            calc_oersted_field(1.0, 0.0)

    def test_oersted_field_negative_distance_raises(
        self
    ) -> None:
        """Verify negative distance is prevented."""
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        with pytest.raises(ValueError, match="Distance must be positive"):
            calc_oersted_field(1.0, -1.0)

    def test_oersted_field_zero_current(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify zero current produces zero field."""
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field

        H = calc_oersted_field(0.0, 1.0)
        assert_cgs_close(H, 0.0, cgs_tolerance)


class TestOerstedFieldDirection:
    """Test right-hand rule for Oersted field direction."""

    def test_field_direction_is_tangential(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify field direction follows right-hand rule (tangential).

        For current in +z direction:
        - At point (1, 0, 0), field should point in +y direction
        - At point (0, 1, 0), field should point in -x direction
        """
        from maxwell.electromagnetism.sources.oersted import (
            calc_circular_field_direction
        )

        current = 1.0

        # At (1, 0, 0), field should point in +y (tangential)
        pos = np.array([1.0, 0.0, 0.0])
        direction = calc_circular_field_direction(current, pos)
        expected = np.array([0.0, 1.0, 0.0])
        assert_vectors_close(direction, expected, cgs_tolerance)

    def test_field_direction_tangential_at_multiple_points(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify field is always tangential (perpendicular to radius)."""
        from maxwell.electromagnetism.sources.oersted import (
            calc_circular_field_direction
        )

        current = 1.0
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([-1.0, 0.0, 0.0]),
        ]

        for pos in test_positions:
            direction = calc_circular_field_direction(current, pos)
            # Direction should be perpendicular to position (dot product = 0)
            dot = np.dot(direction[:2], pos[:2])
            assert abs(dot) < cgs_tolerance, (
                f"Field direction not tangential at {pos}: dot={dot}"
            )

    def test_field_direction_normalized(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify direction vector is normalized (unit vector)."""
        from maxwell.electromagnetism.sources.oersted import (
            calc_circular_field_direction
        )

        current = 1.0
        pos = np.array([1.0, 0.0, 0.0])

        direction = calc_circular_field_direction(current, pos)
        magnitude = np.linalg.norm(direction)

        assert_cgs_close(magnitude, 1.0, cgs_tolerance)


class TestForceOnPole:
    """Test force on magnetic pole near current-carrying wire."""

    def test_force_on_pole_proportional_to_strength(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify F = m * H — force proportional to pole strength."""
        from maxwell.electromagnetism.sources.oersted import calc_force_on_pole

        current = 1.0  # 1 abampere
        distance = 1.0  # 1 cm

        # H = 2I/r = 2 oersted
        # F = m * H

        m1 = 1.0
        m2 = 2.0

        F1 = calc_force_on_pole(m1, current, distance)
        F2 = calc_force_on_pole(m2, current, distance)

        # F2 should be exactly 2 * F1
        expected = 2.0 * F1
        assert_cgs_close(F2, expected, cgs_tolerance)

    def test_force_on_pole_numeric_value(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify F = m * H = m * 2I/r produces correct value.

        For m = 1 emu, I = 1 abampere, r = 1 cm:
        H = 2I/r = 2 oersted
        F = m * H = 1 * 2 = 2 dynes
        """
        from maxwell.electromagnetism.sources.oersted import calc_force_on_pole

        pole_strength = 1.0  # 1 emu
        current = 1.0  # 1 abampere
        distance = 1.0  # 1 cm

        F = calc_force_on_pole(pole_strength, current, distance)

        # F = 2 * m * I / r = 2 dynes
        assert_cgs_close(F, 2.0, cgs_tolerance)

    def test_force_on_pole_zero_distance_raises(
        self
    ) -> None:
        """Verify division by zero is prevented."""
        from maxwell.electromagnetism.sources.oersted import calc_force_on_pole

        with pytest.raises(ValueError, match="Distance must be positive"):
            calc_force_on_pole(1.0, 1.0, 0.0)


class TestOerstedClass:
    """Test OerstedField class."""

    def test_oersted_field_class_magnitude(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify OerstedField.magnitude property."""
        from maxwell.electromagnetism.sources.oersted import OerstedField

        current = 1.0
        distance = 2.0

        field = OerstedField(current=current, distance=distance)

        # H = 2I/r = 2*1/2 = 1 oersted
        assert_cgs_close(field.magnitude, 1.0, cgs_tolerance)

    def test_oersted_field_class_field_at(
        self,
        assert_vectors_close,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify OerstedField.field_at method."""
        from maxwell.electromagnetism.sources.oersted import OerstedField

        current = 1.0
        distance = 1.0
        position = np.array([1.0, 0.0, 0.0])

        field = OerstedField(current=current, distance=distance)
        H = field.field_at(position)

        # Magnitude should be 2 oersted, direction +y
        assert_cgs_close(np.linalg.norm(H), 2.0, cgs_tolerance)
        # Direction should be +y
        expected_dir = np.array([0.0, 1.0, 0.0])
        actual_dir = H / np.linalg.norm(H)
        assert_vectors_close(actual_dir, expected_dir, cgs_tolerance)

    def test_oersted_field_class_validation(
        self
    ) -> None:
        """Verify OerstedField validates negative current."""
        from maxwell.electromagnetism.sources.oersted import OerstedField

        with pytest.raises(ValueError, match="Current must be non-negative"):
            OerstedField(current=-1.0, distance=1.0)


# =============================================================================
# FARADAY MODULE TESTS (Arts. 528-531)
# =============================================================================

class TestMagneticFluxFormula:
    """Test Faraday's magnetic flux formula."""

    def test_magnetic_flux_formula(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify Φ = B * A * cos(θ).

        For B = 100 gauss, A = 10 cm², θ = 0 (perpendicular):
        Φ = 100 * 10 * 1 = 1000 maxwells
        """
        from maxwell.electromagnetism.induction.faraday import calc_magnetic_flux

        B_field = np.array([0.0, 0.0, 100.0])  # 100 gauss in z-direction
        area = 10.0  # 10 cm²
        normal = np.array([0.0, 0.0, 1.0])  # normal in z-direction

        flux = calc_magnetic_flux(B_field, area, normal)

        # Φ = B * A = 100 * 10 = 1000 maxwells
        assert_cgs_close(flux, 1000.0, cgs_tolerance)

    def test_magnetic_flux_angle_dependence(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify Φ = B * A * cos(θ) angular dependence."""
        from maxwell.electromagnetism.induction.faraday import calc_magnetic_flux

        B_field = np.array([0.0, 0.0, 100.0])  # 100 gauss
        area = 10.0

        # θ = 0: cos(0) = 1, maximum flux
        normal_0 = np.array([0.0, 0.0, 1.0])
        flux_0 = calc_magnetic_flux(B_field, area, normal_0)
        assert_cgs_close(flux_0, 1000.0, cgs_tolerance)

        # θ = 90°: cos(90°) = 0, zero flux
        normal_90 = np.array([1.0, 0.0, 0.0])
        flux_90 = calc_magnetic_flux(B_field, area, normal_90)
        assert_cgs_close(flux_90, 0.0, cgs_tolerance)

        # θ = 60°: cos(60°) = 0.5, normal at 60° from z-axis
        # Normal vector at 60° from z: [sin(60°), 0, cos(60°)]
        normal_60 = np.array([np.sqrt(3)/2, 0.0, 0.5])  # Already normalized
        flux_60 = calc_magnetic_flux(B_field, area, normal_60)
        expected_60 = 1000.0 * 0.5  # cos(60°) = 0.5
        assert_cgs_close(flux_60, expected_60, cgs_tolerance)

    def test_magnetic_flux_negative_area_raises(
        self
    ) -> None:
        """Verify negative area is prevented."""
        from maxwell.electromagnetism.induction.faraday import calc_magnetic_flux

        B_field = np.array([0.0, 0.0, 100.0])

        with pytest.raises(ValueError, match="Area must be positive"):
            calc_magnetic_flux(B_field, -1.0)


class TestInducedEMF:
    """Test Faraday's induced EMF and Lenz's law."""

    def test_induced_emf_opposes_change(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify Lenz's law: negative sign in EMF = -dΦ/dt.

        For increasing flux (dΦ/dt > 0), EMF should be negative.
        For decreasing flux (dΦ/dt < 0), EMF should be positive.
        """
        from maxwell.electromagnetism.induction.faraday import calc_induced_emf

        # Increasing flux: dΦ/dt = 1000 maxwells/s
        emf_increasing = calc_induced_emf(1000.0)
        assert emf_increasing < 0  # Negative, opposes increase
        assert_cgs_close(emf_increasing, -1000.0, cgs_tolerance)

        # Decreasing flux: dΦ/dt = -1000 maxwells/s
        emf_decreasing = calc_induced_emf(-1000.0)
        assert emf_decreasing > 0  # Positive, opposes decrease
        assert_cgs_close(emf_decreasing, 1000.0, cgs_tolerance)

    def test_motional_emf_proportional_to_velocity(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify motional EMF = vBL — proportional to velocity."""
        from maxwell.electromagnetism.induction.faraday import calc_motional_emf

        B_field = np.array([0.0, 0.0, 1000.0])  # 1000 gauss
        conductor_length = 10.0  # 10 cm

        v1 = np.array([100.0, 0.0, 0.0])  # 100 cm/s
        v2 = np.array([200.0, 0.0, 0.0])  # 200 cm/s

        emf1 = calc_motional_emf(v1, B_field, conductor_length)
        emf2 = calc_motional_emf(v2, B_field, conductor_length)

        # EMF2 should be exactly 2 * EMF1
        expected = 2.0 * emf1
        assert_cgs_close(emf2, expected, cgs_tolerance)

    def test_motional_emf_numeric_value(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify motional EMF = vBL produces correct value.

        For v = 100 cm/s, B = 1000 gauss, L = 10 cm (all perpendicular):
        EMF = v * B * L = 100 * 1000 * 10 = 1,000,000 abvolts
        """
        from maxwell.electromagnetism.induction.faraday import calc_motional_emf

        v = np.array([100.0, 0.0, 0.0])  # 100 cm/s
        B_field = np.array([0.0, 0.0, 1000.0])  # 1000 gauss
        conductor_length = 10.0  # 10 cm

        emf = calc_motional_emf(v, B_field, conductor_length)

        # EMF = |v × B| * L = v * B * L (perpendicular) = 1,000,000 abvolts
        assert_cgs_close(emf, 1_000_000.0, cgs_tolerance)

    def test_self_induction_opposes_change(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify self-induction EMF = -L·dI/dt opposes current change."""
        from maxwell.electromagnetism.induction.faraday import calc_self_induction

        inductance = 1000.0  # 1000 cm (abhenries)

        # Increasing current: dI/dt = 10 abamperes/s
        emf_increasing = calc_self_induction(inductance, 10.0)
        assert emf_increasing < 0  # Opposes increase
        assert_cgs_close(emf_increasing, -10000.0, cgs_tolerance)

        # Decreasing current: dI/dt = -10 abamperes/s
        emf_decreasing = calc_self_induction(inductance, -10.0)
        assert emf_decreasing > 0  # Opposes decrease
        assert_cgs_close(emf_decreasing, 10000.0, cgs_tolerance)


class TestLenzLaw:
    """Test Lenz's law verification."""

    def test_lenz_law_verification(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify Lenz's law: induced current opposes flux change."""
        from maxwell.electromagnetism.induction.faraday import verify_lenz_law

        # Increasing flux from 1000 to 2000 maxwells over 0.1 seconds
        result = verify_lenz_law(
            initial_flux=1000.0,
            final_flux=2000.0,
            time_interval=0.1,
            resistance=10.0,
        )

        assert result["lenz_law_verified"] is True
        assert result["opposes_change"] is True
        assert result["induced_emf"] < 0  # Negative, opposes increase

        # Decreasing flux from 2000 to 1000 maxwells
        result_decreasing = verify_lenz_law(
            initial_flux=2000.0,
            final_flux=1000.0,
            time_interval=0.1,
            resistance=10.0,
        )

        assert result_decreasing["lenz_law_verified"] is True
        assert result_decreasing["induced_emf"] > 0  # Positive, opposes decrease

    def test_lenz_law_induced_current_direction(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify induced current direction relative to flux change."""
        from maxwell.electromagnetism.induction.faraday import verify_lenz_law

        # Increasing flux should induce opposing current
        result = verify_lenz_law(
            initial_flux=0.0,
            final_flux=1000.0,
            time_interval=0.1,
            resistance=10.0,
        )

        # Induced current should be negative (opposes the increase)
        assert result["induced_current"] < 0

        # The product of flux_change_rate and induced_emf should be negative
        assert result["flux_change_rate"] * result["induced_emf"] < 0


class TestFaradayClass:
    """Test FaradayInduction class."""

    def test_faraday_induction_flux_per_turn(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify FaradayInduction.magnetic_flux with multiple turns."""
        from maxwell.electromagnetism.induction.faraday import FaradayInduction

        B_field = np.array([0.0, 0.0, 100.0])  # 100 gauss
        area = 10.0  # 10 cm²

        # Single turn
        faraday_1 = FaradayInduction(num_turns=1)
        flux_1 = faraday_1.magnetic_flux(B_field, area)
        assert_cgs_close(flux_1, 1000.0, cgs_tolerance)

        # 100 turns: total flux should be 100x
        faraday_100 = FaradayInduction(num_turns=100)
        flux_100 = faraday_100.magnetic_flux(B_field, area)
        assert_cgs_close(flux_100, 100_000.0, cgs_tolerance)

    def test_faraday_induction_emf(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify FaradayInduction.induced_emf with N turns."""
        from maxwell.electromagnetism.induction.faraday import FaradayInduction

        faraday = FaradayInduction(num_turns=10)

        # dΦ/dt = 1000 maxwells/s per turn
        # EMF = -N * dΦ/dt = -10 * 1000 = -10,000 abvolts
        emf = faraday.induced_emf(1000.0)
        assert_cgs_close(emf, -10_000.0, cgs_tolerance)


# =============================================================================
# LORENTZ MODULE TESTS (Arts. 490-492)
# =============================================================================

class TestForceOnWire:
    """Test Lorentz force on current-carrying wire."""

    def test_force_on_wire_formula(
        self,
        cgs_tolerance,
        assert_cgs_close,
        assert_vectors_close
    ) -> None:
        """Verify F = I·L × B produces correct value.

        For I = 1 abampere, L = 10 cm along x, B = 1000 gauss along z:
        F = I * |L × B| = 1 * 10 * 1000 = 10,000 dynes in -y direction
        """
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire

        current = 1.0  # 1 abampere
        length = np.array([10.0, 0.0, 0.0])  # 10 cm along x
        B_field = np.array([0.0, 0.0, 1000.0])  # 1000 gauss along z

        F = calc_force_on_wire(current, length, B_field)

        # |F| = I * L * B = 1 * 10 * 1000 = 10,000 dynes
        assert_cgs_close(np.linalg.norm(F), 10_000.0, cgs_tolerance)
        # Direction should be -y (right-hand rule: x × z = -y)
        expected_direction = np.array([0.0, -1.0, 0.0])
        actual_direction = F / np.linalg.norm(F)
        assert_vectors_close(actual_direction, expected_direction, cgs_tolerance)

    def test_force_direction_right_hand_rule(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify force direction follows right-hand rule (cross product)."""
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire

        current = 1.0

        # L along x, B along z: F should be along -y
        L_x = np.array([10.0, 0.0, 0.0])
        B_z = np.array([0.0, 0.0, 1000.0])
        F1 = calc_force_on_wire(current, L_x, B_z)
        expected_y_neg = np.array([0.0, -1.0, 0.0])
        assert_vectors_close(F1 / np.linalg.norm(F1), expected_y_neg, cgs_tolerance)

        # L along y, B along z: F should be along +x
        L_y = np.array([0.0, 10.0, 0.0])
        B_z = np.array([0.0, 0.0, 1000.0])
        F2 = calc_force_on_wire(current, L_y, B_z)
        expected_x_pos = np.array([1.0, 0.0, 0.0])
        assert_vectors_close(F2 / np.linalg.norm(F2), expected_x_pos, cgs_tolerance)

    def test_force_on_wire_parallel_to_field(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify zero force when wire parallel to field (sin(0) = 0)."""
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire

        current = 1.0
        length = np.array([0.0, 0.0, 10.0])  # Along z
        B_field = np.array([0.0, 0.0, 1000.0])  # Also along z

        F = calc_force_on_wire(current, length, B_field)

        # Parallel: sin(0) = 0, so F = 0
        assert_cgs_close(np.linalg.norm(F), 0.0, cgs_tolerance)

    def test_force_on_wire_proportional_to_current(
        self,
        cgs_tolerance,
        assert_cgs_close,
        assert_vectors_close
    ) -> None:
        """Verify F ∝ I — linear proportionality with current."""
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire

        length = np.array([10.0, 0.0, 0.0])
        B_field = np.array([0.0, 0.0, 1000.0])

        I1 = 1.0
        I2 = 2.0

        F1 = calc_force_on_wire(I1, length, B_field)
        F2 = calc_force_on_wire(I2, length, B_field)

        # F2 should be exactly 2 * F1
        expected = 2.0 * F1
        assert_vectors_close(F2, expected, cgs_tolerance)

    def test_force_on_wire_negative_current_raises(
        self
    ) -> None:
        """Verify negative current is prevented."""
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire

        with pytest.raises(ValueError, match="Current must be non-negative"):
            calc_force_on_wire(-1.0, np.array([10.0, 0.0, 0.0]), np.array([0.0, 0.0, 1000.0]))


class TestParallelCurrents:
    """Test force between parallel currents."""

    def test_parallel_currents_attract(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify same-direction currents attract (positive force)."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_force_between_parallel_currents
        )

        I1 = 1.0  # 1 abampere
        I2 = 1.0  # 1 abampere (same direction)
        separation = 1.0  # 1 cm
        wire_length = 10.0  # 10 cm

        F = calc_force_between_parallel_currents(I1, I2, separation, wire_length)

        # F = 2 * I1 * I2 * L / r = 2 * 1 * 1 * 10 / 1 = 20 dynes (attractive)
        assert F > 0  # Positive = attractive
        assert_cgs_close(F, 20.0, cgs_tolerance)

    def test_antiparallel_currents_repel(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify opposite-direction currents repel (negative force)."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_force_between_parallel_currents
        )

        I1 = 1.0  # 1 abampere
        I2 = -1.0  # -1 abampere (opposite direction)
        separation = 1.0  # 1 cm
        wire_length = 10.0  # 10 cm

        F = calc_force_between_parallel_currents(I1, I2, separation, wire_length)

        # F = 2 * I1 * I2 * L / r = 2 * 1 * (-1) * 10 / 1 = -20 dynes (repulsive)
        assert F < 0  # Negative = repulsive
        assert_cgs_close(F, -20.0, cgs_tolerance)

    def test_parallel_currents_proportional_to_product(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify F ∝ I1 * I2 — proportional to product of currents."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_force_between_parallel_currents
        )

        separation = 1.0
        wire_length = 10.0

        # I1 = 1, I2 = 1
        F1 = calc_force_between_parallel_currents(1.0, 1.0, separation, wire_length)

        # I1 = 2, I2 = 2: should be 4x the force
        F2 = calc_force_between_parallel_currents(2.0, 2.0, separation, wire_length)

        expected = 4.0 * F1
        assert_cgs_close(F2, expected, cgs_tolerance)

    def test_parallel_currents_inverse_distance(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify F ∝ 1/r — inverse distance relationship."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_force_between_parallel_currents
        )

        I1 = 1.0
        I2 = 1.0
        wire_length = 10.0

        r1 = 1.0
        r2 = 2.0

        F1 = calc_force_between_parallel_currents(I1, I2, r1, wire_length)
        F2 = calc_force_between_parallel_currents(I1, I2, r2, wire_length)

        # F2 should be F1/2 (inverse distance)
        expected = F1 / 2.0
        assert_cgs_close(F2, expected, cgs_tolerance)


class TestTorqueOnCurrentLoop:
    """Test torque on magnetic dipole (current loop)."""

    def test_torque_on_current_loop(
        self,
        cgs_tolerance,
        assert_cgs_close,
        assert_vectors_close
    ) -> None:
        """Verify τ = m × B — torque on current loop.

        For m = 100 EMU along x, B = 1000 gauss along z:
        τ = m × B = 100,000 dyne·cm along -y
        """
        from maxwell.electromagnetism.forces.lorentz import (
            calc_torque_on_current_loop
        )

        magnetic_moment = np.array([100.0, 0.0, 0.0])  # 100 EMU along x
        B_field = np.array([0.0, 0.0, 1000.0])  # 1000 gauss along z

        tau = calc_torque_on_current_loop(magnetic_moment, B_field)

        # |τ| = |m| * |B| * sin(90°) = 100 * 1000 = 100,000 dyne·cm
        assert_cgs_close(np.linalg.norm(tau), 100_000.0, cgs_tolerance)
        # Direction: x × z = -y
        expected_direction = np.array([0.0, -1.0, 0.0])
        actual_direction = tau / np.linalg.norm(tau)
        assert_vectors_close(actual_direction, expected_direction, cgs_tolerance)

    def test_torque_on_loop_aligned_with_field(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify zero torque when dipole aligned with field."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_torque_on_current_loop
        )

        magnetic_moment = np.array([100.0, 0.0, 0.0])
        B_field = np.array([1000.0, 0.0, 0.0])  # Same direction

        tau = calc_torque_on_current_loop(magnetic_moment, B_field)

        # Aligned: sin(0) = 0, so τ = 0
        assert_cgs_close(np.linalg.norm(tau), 0.0, cgs_tolerance)


class TestLorentzClass:
    """Test LorentzForce class."""

    def test_lorentz_force_class_force_vector(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify LorentzForce.force_vector property."""
        from maxwell.electromagnetism.forces.lorentz import LorentzForce

        current = 1.0
        length = np.array([10.0, 0.0, 0.0])
        B_field = np.array([0.0, 0.0, 1000.0])

        lorentz = LorentzForce(current=current, B_field=B_field, length=length)
        F = lorentz.force_vector

        assert_cgs_close(np.linalg.norm(F), 10_000.0, cgs_tolerance)

    def test_lorentz_force_class_magnitude(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify LorentzForce.magnitude property."""
        from maxwell.electromagnetism.forces.lorentz import LorentzForce

        current = 1.0
        length = np.array([10.0, 0.0, 0.0])
        B_field = np.array([0.0, 0.0, 1000.0])

        lorentz = LorentzForce(current=current, B_field=B_field, length=length)

        assert_cgs_close(lorentz.magnitude, 10_000.0, cgs_tolerance)

    def test_lorentz_force_class_direction(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify LorentzForce.direction property."""
        from maxwell.electromagnetism.forces.lorentz import LorentzForce

        current = 1.0
        length = np.array([10.0, 0.0, 0.0])
        B_field = np.array([0.0, 0.0, 1000.0])

        lorentz = LorentzForce(current=current, B_field=B_field, length=length)
        direction = lorentz.direction

        # Direction should be -y
        expected = np.array([0.0, -1.0, 0.0])
        assert_vectors_close(direction, expected, cgs_tolerance)


# =============================================================================
# AMPERE-MAXWELL MODULE TESTS (Arts. 606-607)
# =============================================================================

class TestAmpereLawCirculation:
    """Test Ampere's law circulation formula."""

    def test_ampere_law_circulation(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify ∮H·dl = 4πI for steady current.

        For uniform current density J = 1 abA/cm² and path length 2π cm:
        Effective area A = path²/(4π) = (2π)²/(4π) = π cm²
        I_enclosed = J * A = 1 * π = π abamperes
        ∮H·dl = 4πI = 4π * π = 4π² ≈ 39.48 oersted·cm
        """
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_ampere_law

        J = np.array([0.0, 0.0, 1.0])  # 1 abA/cm²
        path_length = 2 * np.pi  # cm

        result = calc_ampere_law(J, path_length)

        # I = J * A = 1 * π = π
        # ∮H·dl = 4πI = 4π²
        expected = 4.0 * np.pi * np.pi
        assert_cgs_close(result, expected, cgs_tolerance)

    def test_ampere_law_proportional_to_current(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify ∮H·dl ∝ I — proportional to current."""
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_ampere_law

        path_length = 2 * np.pi

        J1 = np.array([0.0, 0.0, 1.0])
        J2 = np.array([0.0, 0.0, 2.0])

        result1 = calc_ampere_law(J1, path_length)
        result2 = calc_ampere_law(J2, path_length)

        # Result2 should be exactly 2 * Result1
        expected = 2.0 * result1
        assert_cgs_close(result2, expected, cgs_tolerance)


class TestDisplacementCurrent:
    """Test Maxwell's displacement current."""

    def test_displacement_current_formula(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify J_d = (ε/4π)·dE/dt.

        For dE/dt = 4π × 10^6 statV/cm/s in vacuum (ε = 1):
        J_d = (1/4π) * 4π × 10^6 = 10^6 abamperes/cm²
        """
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_displacement_current

        dE_dt = np.array([0.0, 0.0, 4 * np.pi * 1e6])
        permittivity = 1.0  # Vacuum

        J_d = calc_displacement_current(np.zeros(3), dE_dt, permittivity)

        # J_d = (ε/4π) * dE/dt = 10^6 abamperes/cm²
        assert_cgs_close(np.linalg.norm(J_d), 1e6, cgs_tolerance)

    def test_displacement_current_proportional_to_dE_dt(
        self,
        cgs_tolerance,
        assert_cgs_close,
        assert_vectors_close
    ) -> None:
        """Verify J_d ∝ dE/dt — linear proportionality."""
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_displacement_current

        permittivity = 1.0

        dE_dt_1 = np.array([0.0, 0.0, 1e6])
        dE_dt_2 = np.array([0.0, 0.0, 2e6])

        J_d_1 = calc_displacement_current(np.zeros(3), dE_dt_1, permittivity)
        J_d_2 = calc_displacement_current(np.zeros(3), dE_dt_2, permittivity)

        # J_d_2 should be exactly 2 * J_d_1
        expected = 2.0 * J_d_1
        assert_vectors_close(J_d_2, expected, cgs_tolerance)

    def test_displacement_current_direction(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify displacement current is in same direction as dE/dt."""
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_displacement_current

        dE_dt = np.array([0.0, 1.0, 0.0])
        permittivity = 1.0

        J_d = calc_displacement_current(np.zeros(3), dE_dt, permittivity)

        # J_d should be in same direction as dE_dt
        expected_direction = np.array([0.0, 1.0, 0.0])
        actual_direction = J_d / np.linalg.norm(J_d)
        assert_vectors_close(actual_direction, expected_direction, cgs_tolerance)


class TestTotalCurrent:
    """Test total current including displacement current."""

    def test_total_current_includes_displacement(
        self,
        cgs_tolerance,
        assert_cgs_close,
        assert_vectors_close
    ) -> None:
        """Verify J_total = J + J_d — total current formula."""
        from maxwell.electromagnetism.fields.ampere_maxwell import (
            calc_total_current_density
        )

        J_cond = np.array([1e-6, 0.0, 0.0])
        dE_dt = np.array([4 * np.pi * 1e-6, 0.0, 0.0])
        permittivity = 1.0

        J_total = calc_total_current_density(J_cond, dE_dt, permittivity)

        # J_d = (1/4π) * 4π × 10^-6 = 10^-6
        # J_total = J_cond + J_d = 2 × 10^-6
        expected = np.array([2e-6, 0.0, 0.0])
        assert_vectors_close(J_total, expected, cgs_tolerance)


class TestDisplacementCurrentNecessity:
    """Test the capacitor paradox and necessity of displacement current."""

    def test_displacement_current_necessity(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify capacitor paradox is resolved by displacement current.

        Without displacement current: ∮H·dl = 0 for surface between plates
        With displacement current: ∮H·dl = 4πI (consistent with wire surface)
        """
        from maxwell.electromagnetism.fields.ampere_maxwell import (
            verify_displacement_current_necessity
        )

        charging_current = 1.0  # 1 abampere
        plate_area = 100.0  # cm²
        plate_separation = 1.0  # cm
        time_interval = 1.0  # s

        result = verify_displacement_current_necessity(
            charging_current=charging_current,
            plate_area=plate_area,
            plate_separation=plate_separation,
            time_interval=time_interval,
        )

        # Displacement current should equal conduction current
        assert_cgs_close(result["displacement_current"], charging_current, cgs_tolerance)

        # Without displacement current: ∮H·dl = 0 (wrong!)
        assert_cgs_close(result["without_displacement"], 0.0, cgs_tolerance)

        # With displacement current: ∮H·dl = 4πI (correct!)
        expected = 4.0 * np.pi * charging_current
        assert_cgs_close(result["with_displacement"], expected, cgs_tolerance)

        # Paradox should be resolved
        assert bool(result["paradox_resolved"]) is True
        assert bool(result["current_match"]) is True

    def test_displacement_current_necessity_zero_current_raises(
        self
    ) -> None:
        """Verify zero charging current is prevented."""
        from maxwell.electromagnetism.fields.ampere_maxwell import (
            verify_displacement_current_necessity
        )

        with pytest.raises(ValueError, match="Charging current must be positive"):
            verify_displacement_current_necessity(
                charging_current=0.0,
                plate_area=100.0,
                plate_separation=1.0,
                time_interval=1.0,
            )


class TestAmpereMaxwellLaw:
    """Test complete Ampere-Maxwell law."""

    def test_ampere_maxwell_law_verification(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify ∇ × H = 4πJ_cond + dD/dt."""
        from maxwell.electromagnetism.fields.ampere_maxwell import calc_ampere_maxwell

        # Set up a scenario where Ampere-Maxwell law holds
        J_cond = np.array([1e-7, 0.0, 0.0])
        dD_dt = np.array([5e-7, 0.0, 0.0])

        # Calculate what curl H should be
        rhs_conduction = 4.0 * np.pi * J_cond
        rhs_displacement = dD_dt
        rhs_total = rhs_conduction + rhs_displacement

        # Use the correct curl H that satisfies the equation
        H_curl = rhs_total

        result = calc_ampere_maxwell(H_curl, J_cond, dD_dt)

        assert bool(result["verified"]) is True
        assert_cgs_close(result["residual"], 0.0, cgs_tolerance)


class TestDisplacementCurrentClass:
    """Test DisplacementCurrent class."""

    def test_displacement_current_class_J_d_property(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify DisplacementCurrent.J_displacement property."""
        from maxwell.electromagnetism.fields.ampere_maxwell import DisplacementCurrent

        dE_dt = np.array([0.0, 0.0, 4 * np.pi * 1e6])
        permittivity = 1.0

        dc = DisplacementCurrent(E_field=np.zeros(3), dE_dt=dE_dt, permittivity=permittivity)

        # J_d = (ε/4π) * dD/dt = (1/4π) * ε * dE/dt = 10^6
        J_d = dc.J_displacement
        assert_cgs_close(np.linalg.norm(J_d), 1e6, cgs_tolerance)

    def test_displacement_current_class_D_field_property(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify DisplacementCurrent.D_field property (D = εE)."""
        from maxwell.electromagnetism.fields.ampere_maxwell import DisplacementCurrent

        E_field = np.array([0.0, 0.0, 1000.0])
        dE_dt = np.zeros(3)
        permittivity = 1.0

        dc = DisplacementCurrent(E_field=E_field, dE_dt=dE_dt, permittivity=permittivity)

        # D = εE = 1000
        D = dc.D_field
        assert_cgs_close(np.linalg.norm(D), 1000.0, cgs_tolerance)


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================

class TestPartIVCitationCompliance:
    """Test citation decorator compliance for all Part IV modules."""

    def test_oersted_module_citations(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Oersted module functions have correct citations."""
        from maxwell.electromagnetism.sources.oersted import (
            calc_oersted_field,
            calc_field_from_element,
            calc_force_on_pole,
            calc_circular_field_direction,
            verify_inverse_distance_law,
        )

        # Check calc_oersted_field
        citation = require_citation(calc_oersted_field)
        assert citation.part == 4
        assert 475 in citation.articles or 476 in citation.articles

        # Check calc_force_on_pole
        citation = require_citation(calc_force_on_pole)
        assert citation.part == 4
        assert 479 in citation.articles

    def test_faraday_module_citations(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Faraday module functions have correct citations."""
        from maxwell.electromagnetism.induction.faraday import (
            calc_magnetic_flux,
            calc_induced_emf,
            calc_motional_emf,
            calc_self_induction,
            verify_lenz_law,
        )

        # Check calc_magnetic_flux
        citation = require_citation(calc_magnetic_flux)
        assert citation.part == 4
        assert any(a in citation.articles for a in [528, 529, 530])

        # Check calc_induced_emf
        citation = require_citation(calc_induced_emf)
        assert citation.part == 4
        assert any(a in citation.articles for a in [529, 531])

    def test_lorentz_module_citations(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Lorentz module functions have correct citations."""
        from maxwell.electromagnetism.forces.lorentz import (
            calc_force_on_wire,
            calc_force_on_moving_charge,
            calc_force_between_parallel_currents,
            calc_torque_on_current_loop,
        )

        # Check calc_force_on_wire
        citation = require_citation(calc_force_on_wire)
        assert citation.part == 4
        assert any(a in citation.articles for a in [490, 491])

        # Check calc_force_between_parallel_currents
        citation = require_citation(calc_force_between_parallel_currents)
        assert citation.part == 4
        assert 492 in citation.articles

    def test_ampere_maxwell_module_citations(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Ampere-Maxwell module functions have correct citations."""
        from maxwell.electromagnetism.fields.ampere_maxwell import (
            calc_ampere_law,
            calc_displacement_current,
            calc_total_current_density,
            verify_displacement_current_necessity,
        )

        # Check calc_ampere_law
        citation = require_citation(calc_ampere_law)
        assert citation.part == 4
        assert 606 in citation.articles

        # Check calc_displacement_current
        citation = require_citation(calc_displacement_current)
        assert citation.part == 4
        assert 606 in citation.articles
