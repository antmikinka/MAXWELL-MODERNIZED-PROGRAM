"""maxwell.electromagnetism.components.cylinders — Cylindrical conductors (Arts. 680-688).

Implements Maxwell's treatment of fields within and around cylindrical
conductors carrying current.

Maxwell's CGS formulation (Arts. 680-688):
    Inside a cylindrical conductor (radius a, current I):

        B(r) = 2*I*r / (c*a^2)  for r < a

    Outside the conductor:

        B(r) = 2*I / (c*r)  for r >= a

    For a hollow cylinder (inner radius a, outer radius b):
        B = 0 for r < a (no current inside)
        B(r) = 2*I*(r^2 - a^2)/(c*r*(b^2 - a^2)) for a < r < b
        B(r) = 2*I/(c*r) for r >= b

    The self-inductance per unit length of a cylindrical wire:
        L' = 1/2 + 2*ln(d/a)  (CGS-EMU, per cm)

where:
    I = current (abamperes)
    a = conductor radius (cm)
    r = radial distance (cm)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's cylindrical conductor theory.

References:
    Part IV, Arts. 680-688: Cylindrical conductor fields.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    680,
    681,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Calculate magnetic field of cylindrical conductor",
)
def calc_cylindrical_field(
    current: float,
    conductor_radius: float,
    radial_distance: float,
) -> float:
    """
    Calculate magnetic field of a cylindrical conductor.

    Art. 680-681: Inside the conductor (r < a):

        B(r) = 2*I*r / (c*a^2)

    Outside the conductor (r >= a):

        B(r) = 2*I / (c*r)

    The field is azimuthal (circulating around the wire).

    Args:
        current: Current (abamperes).
        conductor_radius: Wire radius (cm).
        radial_distance: Distance from center (cm).

    Returns:
        Magnetic field magnitude (gauss).
    """
    a = conductor_radius
    r = radial_distance

    if r < 1e-15:
        return 0.0

    if r <= a:
        # Inside: B = 2*I*r/(c*a^2)
        return 2.0 * current * r / (CONST.C * a**2)
    else:
        # Outside: B = 2*I/(c*r)
        return 2.0 * current / (CONST.C * r)


@maxwell_cite(
    682,
    683,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Calculate field of hollow cylindrical conductor",
)
def calc_hollow_cylinder_field(
    current: float,
    inner_radius: float,
    outer_radius: float,
    radial_distance: float,
) -> float:
    """
    Calculate magnetic field of a hollow cylindrical conductor.

    Art. 682-683: For a hollow cylinder with inner radius a and
    outer radius b:

        B = 0 for r < a
        B(r) = 2*I*(r^2 - a^2)/(c*r*(b^2 - a^2)) for a < r < b
        B(r) = 2*I/(c*r) for r >= b

    Args:
        current: Current (abamperes).
        inner_radius: Inner radius (cm).
        outer_radius: Outer radius (cm).
        radial_distance: Distance from center (cm).

    Returns:
        Magnetic field magnitude (gauss).
    """
    a = inner_radius
    b = outer_radius
    r = radial_distance

    if r < 1e-15:
        return 0.0

    if r <= a:
        return 0.0
    elif r <= b:
        # Inside the conductor wall
        return 2.0 * current * (r**2 - a**2) / (CONST.C * r * (b**2 - a**2))
    else:
        return 2.0 * current / (CONST.C * r)


@maxwell_cite(
    684,
    685,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Calculate self-inductance per unit length of wire",
)
def calc_wire_self_inductance(
    wire_radius: float,
    wire_length: float = 1.0,
    permeability: float = 1.0,
) -> float:
    """
    Calculate self-inductance per unit length of cylindrical wire.

    Art. 684-685: The self-inductance per unit length of a wire
    with radius a:

        L' = 1/2 + 2*mu*ln(d/a)  (per cm in CGS-EMU)

    where d is the return path distance.

    Args:
        wire_radius: Wire radius (cm).
        wire_length: Wire length (cm).
        permeability: Relative permeability (default 1.0).

    Returns:
        Self-inductance (cm in CGS-EMU).
    """
    # Return path assumed at distance d = 10*a
    d = 10.0 * wire_radius

    if wire_radius < 1e-15 or d < 1e-15:
        return 0.0

    L_per_cm = 0.5 + 2.0 * permeability * np.log(d / wire_radius)
    return L_per_cm * wire_length


@maxwell_cite(
    686,
    687,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Calculate vector potential inside cylindrical conductor",
)
def calc_cylinder_vector_potential(
    current: float,
    conductor_radius: float,
    radial_distance: float,
) -> float:
    """
    Calculate vector potential inside/outside cylindrical conductor.

    Art. 686-687: For a cylindrical conductor:

        A_z(r) = -I/c * (r^2/a^2)  for r < a
        A_z(r) = -I/c * (1 + 2*ln(r/a))  for r >= a

    Args:
        current: Current (abamperes).
        conductor_radius: Wire radius (cm).
        radial_distance: Distance from center (cm).

    Returns:
        Vector potential A_z (gauss*cm).
    """
    a = conductor_radius
    r = radial_distance

    if r < 1e-15:
        return -current / CONST.C

    if r <= a:
        return -current / CONST.C * (r**2 / a**2)
    else:
        return -current / CONST.C * (1 + 2 * np.log(r / a))


@dataclass
class CylindricalConductor:
    """
    Cylindrical conductor field calculator.

    Art. 680-688: Handles solid and hollow cylindrical conductors.

    Attributes:
        current: Current (abamperes).
        radius: Conductor radius (cm).
        inner_radius: Inner radius for hollow conductors (0 for solid).
    """

    current: float
    radius: float
    inner_radius: float = 0.0

    @maxwell_cite(
        680,
        part=4,
        chapter="Cylindrical Conductors",
        theory_class="maxwell_original",
        description="Get field at radial distance",
    )
    def field_at(self, radial_distance: float) -> float:
        """Calculate field at radial distance."""
        if self.inner_radius > 0:
            return calc_hollow_cylinder_field(
                self.current, self.inner_radius, self.radius, radial_distance
            )
        return calc_cylindrical_field(self.current, self.radius, radial_distance)

    @maxwell_cite(
        686,
        part=4,
        chapter="Cylindrical Conductors",
        theory_class="maxwell_original",
        description="Get vector potential at radial distance",
    )
    def vector_potential_at(self, radial_distance: float) -> float:
        """Calculate vector potential at radial distance."""
        return calc_cylinder_vector_potential(
            self.current, self.radius, radial_distance
        )


@maxwell_cite(
    680,
    681,
    682,
    683,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Verify cylindrical conductor field relations",
)
def verify_cylindrical_field(
    current: float = 1.0,
    radius: float = 1.0,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify cylindrical conductor field relations.

    Art. 680-683: This function verifies:
    1. Inside field increases linearly with r
    2. Outside field decreases as 1/r
    3. Field continuous at surface
    4. Hollow cylinder B = 0 inside

    Args:
        current: Test current (abamperes).
        radius: Test conductor radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Inside field at r = a/2: B = 2*I*(a/2)/(c*a^2) = I/(c*a)
    B_half = calc_cylindrical_field(current, radius, radius / 2)
    B_half_expected = current / (CONST.C * radius)
    half_error = abs(B_half - B_half_expected) / B_half_expected

    # Outside field at r = 2a: B = 2*I/(c*2a) = I/(c*a)
    B_double = calc_cylindrical_field(current, radius, 2 * radius)
    B_double_expected = current / (CONST.C * radius)
    double_error = abs(B_double - B_double_expected) / B_double_expected

    # Continuity at surface
    B_inside_surface = calc_cylindrical_field(current, radius, radius * 0.999)
    B_outside_surface = calc_cylindrical_field(current, radius, radius * 1.001)
    continuity_error = abs(B_inside_surface - B_outside_surface) / B_inside_surface

    # Hollow cylinder: B = 0 for r < a
    B_hollow_inside = calc_hollow_cylinder_field(
        current, radius, 2 * radius, radius / 2
    )
    hollow_error = abs(B_hollow_inside)

    return {
        "B_at_half_radius": B_half,
        "B_half_expected": B_half_expected,
        "half_radius_error": half_error,
        "B_at_double_radius": B_double,
        "B_double_expected": B_double_expected,
        "double_radius_error": double_error,
        "continuity_error": continuity_error,
        "B_hollow_inside": B_hollow_inside,
        "hollow_cylinder_error": hollow_error,
        "inside_verified": bool(half_error < tolerance),
        "outside_verified": bool(double_error < tolerance),
        "continuity_verified": bool(continuity_error < 0.01),
        "hollow_verified": bool(hollow_error < tolerance),
        "verified": bool(
            half_error < tolerance
            and double_error < tolerance
            and continuity_error < 0.01
            and hollow_error < tolerance
        ),
    }


@maxwell_cite(
    680,
    681,
    682,
    683,
    684,
    685,
    part=4,
    chapter="Cylindrical Conductors",
    theory_class="maxwell_original",
    description="Complete cylindrical conductor analysis",
)
def analyze_cylindrical_conductor(
    current: float,
    radius: float,
    inner_radius: float = 0.0,
) -> dict[str, float | list]:
    """
    Complete analysis of cylindrical conductor fields.

    Art. 680-685: Comprehensive analysis including:
    1. Field profile inside and outside
    2. Vector potential profile
    3. Self-inductance calculation
    4. Hollow vs solid comparison

    Args:
        current: Current (abamperes).
        radius: Conductor radius (cm).
        inner_radius: Inner radius for hollow (0 for solid).

    Returns:
        Dictionary with complete analysis results.
    """
    # Field profile
    r_values = np.linspace(0, 3 * radius, 30)
    B_profile = []
    A_profile = []

    for r in r_values:
        if inner_radius > 0:
            B = calc_hollow_cylinder_field(current, inner_radius, radius, r)
        else:
            B = calc_cylindrical_field(current, radius, r)
        B_profile.append(B)

        A = calc_cylinder_vector_potential(current, radius, r)
        A_profile.append(A)

    # Self-inductance
    L = calc_wire_self_inductance(radius)

    # Max field
    B_max = calc_cylindrical_field(current, radius, radius)

    return {
        "current": current,
        "radius": radius,
        "inner_radius": inner_radius,
        "hollow": inner_radius > 0,
        "B_surface": B_max,
        "radial_positions": list(r_values),
        "B_profile": B_profile,
        "A_profile": A_profile,
        "self_inductance_per_cm": L,
    }
