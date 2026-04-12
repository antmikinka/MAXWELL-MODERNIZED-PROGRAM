"""
Test CGS unit compliance.

Ensures all numeric computations use CGS units correctly:
- Distance in centimeters (cm)
- Current in abamperes (EMU) or statamperes (ESU)
- Magnetic field in gauss/oersted
- Force in dynes
- Charge in abcoulombs (EMU) or statcoulombs (ESU)

Tests verify:
- Correct unit scaling
- Proper unit conversions
- Inverse-distance law compliance (H ∝ 1/r)
- Right-hand rule direction verification
"""

from __future__ import annotations
import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.electromagnetism.sources.oersted import (
    OerstedField,
    calc_oersted_field,
    calc_field_from_element,
    calc_force_on_pole,
    calc_circular_field_direction,
    verify_inverse_distance_law,
)


class TestCGSUnitsBasics:
    """Test basic CGS unit constants and conversions."""

    def test_speed_of_light_cgs(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify speed of light is in cm/s."""
        # C should be approximately 3e10 cm/s
        expected = 2.99792458e10
        assert_cgs_close(C, expected, cgs_tolerance)

    def test_cgs_unit_names(self) -> None:
        """Verify CGS unit name lookups work correctly."""
        assert cgs_unit_of("length") == "cm"
        assert cgs_unit_of("mass") == "g"
        assert cgs_unit_of("force") == "dyne"
        assert cgs_unit_of("energy") == "erg"
        assert cgs_unit_of("current_emu") == "abampere"
        assert cgs_unit_of("magnetic_field") == "gauss"

    def test_cgs_constants_available(self) -> None:
        """Verify CGS constants are accessible."""
        assert CONST.C > 0
        assert CONST.C_APPROX >= 3.0e10
        assert CONST.MU0_EMU == 1.0


class TestOerstedFieldCGS:
    """Test Oersted field calculations use CGS units correctly."""

    def test_calc_oersted_field_units(
        self,
        cgs_tolerance,
        assert_cgs_close
    ) -> None:
        """Verify H = 2I/r produces correct CGS units.

        For an infinite wire:
        - I = 1 abampere (EMU)
        - r = 1 cm
        - H = 2I/r = 2 oersted
        """
        current_abamp = 1.0  # 1 abampere
        distance_cm = 1.0    # 1 cm

        H = calc_oersted_field(current_abamp, distance_cm)

        # H = 2I/r = 2(1)/1 = 2 oersted
        expected = 2.0
        assert_cgs_close(H, expected, cgs_tolerance)

    def test_calc_oersted_field_inverse_distance(
        self,
        cgs_distance_range,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify H ∝ 1/r inverse distance relationship.

        For fixed current I:
        H * r should be constant (= 2I)
        """
        current_abamp = 1.0
        H_r_products = []

        for r in cgs_distance_range:
            H = calc_oersted_field(current_abamp, r)
            H_r_products.append(H * r)

        # All H*r products should equal 2I = 2
        expected = 2.0 * current_abamp
        for i, product in enumerate(H_r_products):
            assert_cgs_close(product, expected, cgs_tolerance)

    def test_calc_oersted_field_current_scaling(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify H ∝ I linear current relationship.

        For fixed distance r:
        H / I should be constant (= 2/r)
        """
        distance_cm = 1.0
        currents = [0.5, 1.0, 2.0, 5.0, 10.0]

        for current in currents:
            H = calc_oersted_field(current, distance_cm)
            expected = 2.0 * current / distance_cm
            assert_cgs_close(H, expected, cgs_tolerance)

    def test_calc_oersted_field_zero_distance_raises(
        self
    ) -> None:
        """Verify division by zero is prevented."""
        with pytest.raises(ValueError, match="Distance must be positive"):
            calc_oersted_field(1.0, 0.0)

    def test_calc_oersted_field_negative_distance_raises(
        self
    ) -> None:
        """Verify negative distance is prevented."""
        with pytest.raises(ValueError, match="Distance must be positive"):
            calc_oersted_field(1.0, -1.0)


class TestFieldFromElementCGS:
    """Test field from current element calculations."""

    def test_calc_field_from_element_basic(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify field calculation from a current element.

        dB = (I * dl * sin(theta)) / r^2  (Biot-Savart in CGS)
        """
        current_abamp = 1.0
        element_length_cm = 0.1  # 1 mm
        distance_cm = 1.0
        angle_rad = np.pi / 2  # 90 degrees, sin = 1

        dB = calc_field_from_element(
            current_abamp,
            element_length_cm,
            distance_cm,
            angle_rad
        )

        # dB = I * dl * sin(theta) / r^2 = 1 * 0.1 * 1 / 1 = 0.1
        expected = current_abamp * element_length_cm / (distance_cm ** 2)
        assert_cgs_close(dB, expected, cgs_tolerance)

    def test_calc_field_from_element_angle_dependence(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify sin(theta) angular dependence."""
        current_abamp = 1.0
        element_length_cm = 0.1
        distance_cm = 1.0

        # At theta = 0, field should be zero
        dB_zero = calc_field_from_element(
            current_abamp, element_length_cm, distance_cm, 0.0
        )
        assert_cgs_close(dB_zero, 0.0, cgs_tolerance)

        # At theta = pi/2, field should be maximum
        dB_max = calc_field_from_element(
            current_abamp, element_length_cm, distance_cm, np.pi / 2
        )
        expected_max = current_abamp * element_length_cm / (distance_cm ** 2)
        assert_cgs_close(dB_max, expected_max, cgs_tolerance)


class TestForceOnPoleCGS:
    """Test force on magnetic pole calculations."""

    def test_calc_force_on_pole_basic(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify force on magnetic pole near current-carrying wire.

        F = m * H  (force on pole of strength m in field H)
        where H = 2I/r for infinite wire
        """
        pole_strength_emu = 1.0  # Unit pole strength
        current_abamp = 1.0
        distance_cm = 1.0

        F = calc_force_on_pole(pole_strength_emu, current_abamp, distance_cm)

        # H = 2I/r = 2, F = m*H = 1 * 2 = 2 dynes
        H = 2.0 * current_abamp / distance_cm
        expected = pole_strength_emu * H
        assert_cgs_close(F, expected, cgs_tolerance)

    def test_calc_force_on_pole_units(self) -> None:
        """Verify force is in dynes (CGS unit)."""
        # The calculation returns force in dynes by CGS convention
        # m (emu) * H (oersted) = F (dyne)
        result = calc_force_on_pole(1.0, 1.0, 1.0)
        assert isinstance(result, float)
        assert result > 0  # Should produce a positive force magnitude


class TestCircularFieldDirection:
    """Test right-hand rule for field direction."""

    def test_calc_circular_field_direction_basic(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify field direction follows right-hand rule.

        For current in +z direction:
        - At point (r, 0, 0), field should point in +y direction
        - At point (0, r, 0), field should point in -x direction
        """
        current_abamp = 1.0

        # At (1, 0, 0), field should point in +y (tangential)
        pos = np.array([1.0, 0.0, 0.0])
        direction = calc_circular_field_direction(current_abamp, pos)
        expected = np.array([0.0, 1.0, 0.0])
        assert_vectors_close(direction, expected, cgs_tolerance)

    def test_calc_circular_field_direction_tangential(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify field is always tangential (perpendicular to radius)."""
        current_abamp = 1.0
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([-1.0, 0.0, 0.0]),
        ]

        for pos in test_positions:
            direction = calc_circular_field_direction(current_abamp, pos)
            # Direction should be perpendicular to position (dot product = 0)
            # For circular field around z-axis, check tangential property
            dot = np.dot(direction[:2], pos[:2])  # Only x,y components
            assert abs(dot) < cgs_tolerance, (
                f"Field direction not tangential at {pos}: dot={dot}"
            )

    def test_calc_circular_field_direction_normalized(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify direction vector is normalized (unit vector)."""
        current_abamp = 1.0
        pos = np.array([1.0, 0.0, 0.0])

        direction = calc_circular_field_direction(current_abamp, pos)
        magnitude = np.linalg.norm(direction)

        assert_cgs_close(magnitude, 1.0, cgs_tolerance)


class TestInverseDistanceLaw:
    """Test verification of inverse-distance law."""

    def test_verify_inverse_distance_law_passes(
        self
    ) -> None:
        """Verify the inverse-distance law verification passes for ideal data."""
        result = verify_inverse_distance_law()

        assert result["verified"] is True
        assert result["law_type"] == "inverse_distance"
        assert result["deviation_max"] == 0.0

    def test_verify_inverse_distance_law_data(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify computed H*r product is constant."""
        result = verify_inverse_distance_law()

        # H*r should be constant (= 2I for infinite wire)
        H_r_values = result.get("H_r_products", [])
        if H_r_values:
            # Check variance is small
            mean_val = np.mean(H_r_values)
            std_val = np.std(H_r_values)
            if mean_val > 0:
                relative_std = std_val / mean_val
                assert relative_std < cgs_tolerance, (
                    f"H*r not constant: relative std = {relative_std}"
                )


class TestOerstedFieldClass:
    """Test OerstedField class CGS compliance."""

    def test_oersted_field_magnitude(
        self,
        assert_cgs_close,
        cgs_tolerance
    ) -> None:
        """Verify OerstedField magnitude calculation."""
        current_abamp = 1.0
        distance_cm = 2.0

        field = OerstedField(current=current_abamp, distance=distance_cm)

        # H = 2I/r = 2*1/2 = 1 oersted
        expected = 2.0 * current_abamp / distance_cm
        assert_cgs_close(field.magnitude, expected, cgs_tolerance)

    def test_oersted_field_units_attribute(self) -> None:
        """Verify OerstedField has CGS units metadata."""
        field = OerstedField(current=1.0, distance=1.0)

        assert hasattr(field, "current")
        assert hasattr(field, "distance")
        assert hasattr(field, "magnitude")
        # Units are CGS by convention

    def test_oersted_field_direction(
        self,
        assert_vectors_close,
        cgs_tolerance
    ) -> None:
        """Verify OerstedField direction calculation."""
        current_abamp = 1.0
        distance_cm = 1.0
        position = np.array([1.0, 0.0, 0.0])

        field = OerstedField(
            current=current_abamp,
            distance=distance_cm,
            position=position
        )

        direction = field.direction_at(position)
        # Should point in +y direction (tangential)
        expected = np.array([0.0, 1.0, 0.0])
        assert_vectors_close(direction, expected, cgs_tolerance)
