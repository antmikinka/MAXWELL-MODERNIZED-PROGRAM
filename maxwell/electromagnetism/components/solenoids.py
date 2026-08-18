"""maxwell.electromagnetism.components.solenoids — Solenoid fields (Arts. 675-685).

Implements Maxwell's treatment of solenoids and Helmholtz coils.

Maxwell's CGS formulation (Arts. 675-685):
    For a long solenoid with n turns per unit length:

        B = 4*pi*n*I / c  (inside, far from ends)

    For a finite solenoid of length L, radius a:

        B(z) = 2*pi*n*I/c * (cos(theta1) + cos(theta2))

    where theta1, theta2 are the angles from z to the two ends.

    For Helmholtz coils (separation = radius):
        B_center = (8/sqrt(125)) * 4*pi*n*I / c
        The field is uniform to second order.

where:
    n = turns per unit length (cm^-1)
    I = current (abamperes)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's solenoid theory.

References:
    Part IV, Arts. 675-685: Solenoid and Helmholtz coil fields.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import calc_coil_off_axis
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    675,
    676,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Calculate magnetic field of long solenoid",
)
def calc_solenoid_field(
    current: float,
    turns_per_cm: float,
    solenoid_length: float,
    solenoid_radius: float,
    axial_position: float,
) -> float:
    """
    Calculate magnetic field inside a finite solenoid on axis.

    Art. 675-676: For a finite solenoid:

        B(z) = 2*pi*n*I/c * (cos(theta1) + cos(theta2))

    where theta1, theta2 are angles from the point to the two ends.

    For an infinite solenoid:
        B = 4*pi*n*I/c

    Args:
        current: Current (abamperes).
        turns_per_cm: Turns per unit length.
        solenoid_length: Total length (cm).
        solenoid_radius: Radius (cm).
        axial_position: Axial position from center (cm).

    Returns:
        Axial magnetic field B_z (gauss).
    """
    a = solenoid_radius
    L = solenoid_length
    z = axial_position

    # Distances to ends
    z1 = L / 2 - z  # distance to near end
    z2 = L / 2 + z  # distance to far end

    # Angles
    r1 = np.sqrt(a**2 + z1**2)
    r2 = np.sqrt(a**2 + z2**2)

    if r1 < 1e-15 or r2 < 1e-15:
        return 2.0 * np.pi * turns_per_cm * current / CONST.C

    cos_theta1 = z1 / r1
    cos_theta2 = z2 / r2

    return 2.0 * np.pi * turns_per_cm * current / CONST.C * (cos_theta1 + cos_theta2)


@maxwell_cite(
    677,
    678,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Calculate infinite solenoid field",
)
def calc_infinite_solenoid_field(
    current: float,
    turns_per_cm: float,
) -> float:
    """
    Calculate magnetic field of an infinite solenoid.

    Art. 677-678: For an infinitely long solenoid:

        B = 4*pi*n*I/c

    This is the ideal limit.

    Args:
        current: Current (abamperes).
        turns_per_cm: Turns per unit length.

    Returns:
        Uniform magnetic field inside solenoid (gauss).
    """
    return 4.0 * np.pi * turns_per_cm * current / CONST.C


@maxwell_cite(
    679,
    680,
    681,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Calculate Helmholtz coil field at center",
)
def calc_helmholtz_center(
    current: float,
    coil_radius: float,
    n_turns: int = 1,
) -> float:
    """
    Calculate magnetic field at center of Helmholtz coil pair.

    Art. 679-681: For Helmholtz coils (separation = radius):

        B_center = (8 / sqrt(125)) * 4*pi*n*I / c
                 = 0.7155 * 4*pi*n*I / c

    Args:
        current: Current per coil (abamperes).
        coil_radius: Coil radius (cm).
        n_turns: Turns per coil.

    Returns:
        Field at center (gauss).
    """
    # Field from single coil at z = a/2
    from maxwell.electromagnetism.components.circular_coils import calc_coil_on_axis

    B_single = calc_coil_on_axis(current, coil_radius, coil_radius / 2, n_turns)
    return 2 * B_single


@maxwell_cite(
    682,
    683,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Calculate Helmholtz coil uniformity region",
)
def calc_helmholtz_uniformity(
    current: float,
    coil_radius: float,
    n_turns: int = 1,
    max_offset: float = None,
) -> dict[str, float]:
    """
    Calculate field uniformity of Helmholtz coil pair.

    Art. 682-683: The Helmholtz configuration provides uniform field
    to second order near the center.

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        n_turns: Turns per coil.
        max_offset: Maximum offset to test (cm, default 0.1*radius).

    Returns:
        Dictionary with uniformity data.
    """
    if max_offset is None:
        max_offset = 0.1 * coil_radius

    B_center = calc_helmholtz_center(current, coil_radius, n_turns)

    # Test field at offsets
    from maxwell.electromagnetism.components.circular_coils import (
        calc_double_coil_field,
    )

    offsets = np.linspace(0, max_offset, 10)
    variations = []

    for offset in offsets:
        B = calc_double_coil_field(
            current, coil_radius, np.array([0, 0, offset]), n_turns=n_turns
        )
        B_mag = np.linalg.norm(B)
        variation = (
            abs(B_mag - abs(B_center)) / abs(B_center) if abs(B_center) > 1e-15 else 0
        )
        variations.append(variation)

    return {
        "B_center": B_center,
        "max_offset": max_offset,
        "offsets": list(offsets),
        "variations": variations,
        "max_variation": max(variations) if variations else 0,
    }


@dataclass
class Solenoid:
    """
    Solenoid magnetic field calculator.

    Art. 675-685: Handles finite and infinite solenoids,
    and Helmholtz coil pairs.

    Attributes:
        current: Current (abamperes).
        turns_per_cm: Turns per unit length.
        length: Solenoid length (cm).
        radius: Solenoid radius (cm).
    """

    current: float
    turns_per_cm: float
    length: float
    radius: float

    @maxwell_cite(
        675,
        part=4,
        chapter="Solenoids",
        theory_class="maxwell_original",
        description="Get field at axial position",
    )
    def field_at(self, axial_position: float) -> float:
        """Calculate field at axial position from center."""
        return calc_solenoid_field(
            self.current,
            self.turns_per_cm,
            self.length,
            self.radius,
            axial_position,
        )

    @maxwell_cite(
        677,
        part=4,
        chapter="Solenoids",
        theory_class="maxwell_original",
        description="Get infinite solenoid approximation",
    )
    def infinite_field(self) -> float:
        """Infinite solenoid field approximation."""
        return calc_infinite_solenoid_field(self.current, self.turns_per_cm)

    @maxwell_cite(
        675,
        part=4,
        chapter="Solenoids",
        theory_class="maxwell_original",
        description="Get field at center",
    )
    def center_field(self) -> float:
        """Field at solenoid center."""
        return self.field_at(0)


@maxwell_cite(
    675,
    676,
    677,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Verify solenoid field relations",
)
def verify_solenoid_field(
    current: float = 1.0,
    turns_per_cm: float = 10.0,
    radius: float = 1.0,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify solenoid field relations.

    Art. 675-677: This function verifies:
    1. Long solenoid approaches infinite limit
    2. Center field formula
    3. End field = half of center

    Args:
        current: Test current (abamperes).
        turns_per_cm: Test turns per cm.
        radius: Test solenoid radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    B_inf = calc_infinite_solenoid_field(current, turns_per_cm)

    # Very long solenoid should approach infinite limit
    long_L = 1000 * radius
    B_long = calc_solenoid_field(current, turns_per_cm, long_L, radius, 0)
    long_error = abs(B_long - B_inf) / B_inf if B_inf > 1e-15 else abs(B_long)

    # End field should be approximately half of center
    B_center = calc_solenoid_field(current, turns_per_cm, long_L, radius, 0)
    B_end = calc_solenoid_field(current, turns_per_cm, long_L, radius, long_L / 2)
    end_ratio = B_end / B_center if B_center > 1e-15 else 0
    end_error = abs(end_ratio - 0.5)

    return {
        "B_infinite": B_inf,
        "B_long_solenoid": B_long,
        "long_solenoid_error": long_error,
        "B_center": B_center,
        "B_end": B_end,
        "end_ratio": end_ratio,
        "end_error": end_error,
        "long_solenoid_verified": bool(long_error < tolerance),
        "end_field_verified": bool(end_error < 0.01),
        "verified": bool(long_error < tolerance and end_error < 0.01),
    }


@maxwell_cite(
    675,
    676,
    677,
    678,
    679,
    680,
    681,
    part=4,
    chapter="Solenoids",
    theory_class="maxwell_original",
    description="Complete solenoid analysis",
)
def analyze_solenoid(
    current: float,
    turns_per_cm: float,
    length: float,
    radius: float,
) -> dict[str, float | list]:
    """
    Complete analysis of solenoid magnetic field.

    Art. 675-681: Comprehensive analysis including:
    1. Axial field profile
    2. Comparison with infinite solenoid
    3. End effects
    4. Helmholtz uniformity

    Args:
        current: Current (abamperes).
        turns_per_cm: Turns per unit length.
        length: Solenoid length (cm).
        radius: Solenoid radius (cm).

    Returns:
        Dictionary with complete analysis results.
    """
    B_inf = calc_infinite_solenoid_field(current, turns_per_cm)

    # Axial profile
    z_values = np.linspace(-length, length, 40)
    B_profile = [
        calc_solenoid_field(current, turns_per_cm, length, radius, z) for z in z_values
    ]

    # Center and end fields
    B_center = calc_solenoid_field(current, turns_per_cm, length, radius, 0)
    B_end = calc_solenoid_field(current, turns_per_cm, length, radius, length / 2)

    # Helmholtz comparison
    B_helmholtz = calc_helmholtz_center(current, radius)

    return {
        "current": current,
        "turns_per_cm": turns_per_cm,
        "length": length,
        "radius": radius,
        "B_infinite": B_inf,
        "B_center": B_center,
        "B_end": B_end,
        "end_to_center_ratio": B_end / B_center if B_center > 0 else 0,
        "axial_positions": list(z_values),
        "axial_field": B_profile,
        "helmholtz_center_field": B_helmholtz,
    }
