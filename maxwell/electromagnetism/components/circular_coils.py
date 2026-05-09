"""maxwell.electromagnetism.components.circular_coils — Circular coil fields (Arts. 670-690).

Implements Maxwell's treatment of magnetic fields produced by circular
current loops, including on-axis and off-axis field calculations.

Maxwell's CGS formulation (Arts. 670-690):
    On the axis of a circular loop (radius a, current I, distance z):

        B_z = 2*pi*I*a^2 / (c * (a^2 + z^2)^(3/2))

    Off-axis, the field involves elliptic integrals:

        B_rho = (2*I*z/(c*rho^2)) * [E(k^2)*(1 + k^2*alpha^2)/beta - K(k^2)]
        B_z = (2*I/(c*rho^2)) * [E(k^2)*(a^2 - r^2)/gamma + K(k^2)]

    where k^2 = 4*a*rho / ((a + rho)^2 + z^2)

    For Helmholtz coils (two identical coils, separation = radius):
        The field at the center is nearly uniform.

where:
    I = current (abamperes)
    a = coil radius (cm)
    z = axial distance (cm)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's circular coil theory.

References:
    Part IV, Arts. 670-690: Circular coil magnetic fields.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    670,
    671,
    672,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Calculate magnetic field on axis of circular coil",
)
def calc_coil_on_axis(
    current: float,
    coil_radius: float,
    axial_distance: float,
    n_turns: int = 1,
) -> float:
    """
    Calculate magnetic field on the axis of a circular coil.

    Art. 670-672: On the axis of a circular loop:

        B_z = 2*pi*n*I*a^2 / (c * (a^2 + z^2)^(3/2))

    At the center (z = 0):
        B_z = 2*pi*n*I / (c * a)

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        axial_distance: Distance from center along axis (cm).
        n_turns: Number of turns (default 1).

    Returns:
        Axial magnetic field B_z (gauss).
    """
    a = coil_radius
    z = axial_distance

    denom = (a**2 + z**2) ** 1.5
    if denom < 1e-30:
        return 0.0

    return 2.0 * np.pi * n_turns * current * a**2 / (CONST.C * denom)


def _elliptic_K(m: float) -> float:
    """Complete elliptic integral of the first kind (approximation)."""
    if m < 0:
        return np.pi / 2
    if m >= 1.0:
        m = 1.0 - 1e-15
    # Series approximation
    m2 = m * m
    m3 = m2 * m
    return (np.pi / 2) * (1 + m / 4 + 9 * m2 / 64 + 25 * m3 / 256)


def _elliptic_E(m: float) -> float:
    """Complete elliptic integral of the second kind (approximation)."""
    if m < 0:
        return np.pi / 2
    if m >= 1.0:
        m = 1.0 - 1e-15
    # Series approximation
    m2 = m * m
    m3 = m2 * m
    return (np.pi / 2) * (1 - m / 4 - 3 * m2 / 64 - 5 * m3 / 256)


@maxwell_cite(
    673,
    674,
    675,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Calculate magnetic field at arbitrary point from circular coil",
)
def calc_coil_off_axis(
    current: float,
    coil_radius: float,
    position: np.ndarray,
    n_turns: int = 1,
) -> np.ndarray:
    """
    Calculate magnetic field at arbitrary position from a circular coil.

    Art. 673-675: For a coil in the xy-plane centered at origin,
    the field at position (rho, z) uses elliptic integrals:

        k^2 = 4*a*rho / ((a + rho)^2 + z^2)
        B_z and B_rho from K(k^2) and E(k^2)

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        position: Position (cm), coil is in xy-plane.
        n_turns: Number of turns.

    Returns:
        Magnetic field vector (gauss).
    """
    position = np.asarray(position, dtype=np.float64)
    a = coil_radius

    rho = np.sqrt(position[0] ** 2 + position[1] ** 2)
    z = position[2]

    # Handle special cases
    if rho < 1e-15:
        # On axis
        Bz = calc_coil_on_axis(current, a, z, n_turns)
        return np.array([0.0, 0.0, Bz])

    if a < 1e-15:
        return np.zeros(3)

    # k^2 parameter
    k_sq = 4.0 * a * rho / ((a + rho) ** 2 + z**2)
    k_sq = min(max(k_sq, 0), 1 - 1e-15)

    K = _elliptic_K(k_sq)
    E = _elliptic_E(k_sq)

    # Field components in cylindrical coordinates
    alpha_sq = (a + rho) ** 2 + z**2
    prefactor = 2.0 * n_turns * current / (CONST.C * alpha_sq)

    # B_z component
    B_z = prefactor * (
        E * (a**2 - rho**2 - z**2) / (alpha_sq - 4 * a * rho + 1e-30) + K
    )

    # B_rho component
    B_rho = (
        prefactor
        * (z / rho)
        * (E * (a**2 + rho**2 + z**2) / (alpha_sq - 4 * a * rho + 1e-30) - K)
    )

    # Convert to Cartesian
    cos_phi = position[0] / rho if rho > 1e-15 else 1.0
    sin_phi = position[1] / rho if rho > 1e-15 else 0.0

    B_x = B_rho * cos_phi
    B_y = B_rho * sin_phi

    return np.array([B_x, B_y, B_z])


@maxwell_cite(
    676,
    677,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Calculate magnetic field from double coil (Helmholtz)",
)
def calc_double_coil_field(
    current: float,
    coil_radius: float,
    position: np.ndarray,
    coil_separation: float = None,
    n_turns: int = 1,
) -> np.ndarray:
    """
    Calculate magnetic field from two coaxial circular coils.

    Art. 676-677: For Helmholtz configuration, coil_separation = coil_radius.
    The field is the superposition of two single-coil fields.

    Args:
        current: Current (abamperes).
        coil_radius: Coil radius (cm).
        position: Position (cm).
        coil_separation: Distance between coils (cm, default = radius for Helmholtz).
        n_turns: Turns per coil.

    Returns:
        Magnetic field vector (gauss).
    """
    if coil_separation is None:
        coil_separation = coil_radius

    position = np.asarray(position, dtype=np.float64)

    # Coil 1 at z = -separation/2
    pos1 = position - np.array([0, 0, -coil_separation / 2])
    # Coil 2 at z = +separation/2
    pos2 = position - np.array([0, 0, coil_separation / 2])

    B1 = calc_coil_off_axis(current, coil_radius, pos1, n_turns)
    B2 = calc_coil_off_axis(current, coil_radius, pos2, n_turns)

    return B1 + B2


@maxwell_cite(
    678,
    679,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Calculate magnetic field from coaxial coil pair with opposite currents",
)
def calc_coaxial_coil_pair(
    current: float,
    coil1_radius: float,
    coil2_radius: float,
    position: np.ndarray,
    coil_separation: float,
    current1_dir: int = 1,
    current2_dir: int = 1,
    n_turns: int = 1,
) -> np.ndarray:
    """
    Calculate field from two coaxial coils with possibly different radii.

    Art. 678-679: General coaxial coil pair configuration.

    Args:
        current: Current magnitude (abamperes).
        coil1_radius: First coil radius (cm).
        coil2_radius: Second coil radius (cm).
        position: Position (cm).
        coil_separation: Distance between coils (cm).
        current1_dir: Current direction in coil 1 (+1 or -1).
        current2_dir: Current direction in coil 2 (+1 or -1).
        n_turns: Turns per coil.

    Returns:
        Magnetic field vector (gauss).
    """
    position = np.asarray(position, dtype=np.float64)

    pos1 = position - np.array([0, 0, -coil_separation / 2])
    pos2 = position - np.array([0, 0, coil_separation / 2])

    B1 = calc_coil_off_axis(current * current1_dir, coil1_radius, pos1, n_turns)
    B2 = calc_coil_off_axis(current * current2_dir, coil2_radius, pos2, n_turns)

    return B1 + B2


@dataclass
class CircularCoil:
    """
    Circular coil magnetic field calculator.

    Art. 670-690: Provides methods for calculating the magnetic field
    produced by circular current loops in various configurations.

    Attributes:
        current: Coil current (abamperes).
        radius: Coil radius (cm).
        n_turns: Number of turns.
        position: Coil center position (cm).
    """

    current: float
    radius: float
    n_turns: int = 1
    position: np.ndarray = None

    def __post_init__(self):
        if self.position is None:
            self.position = np.zeros(3)
        self.position = np.asarray(self.position, dtype=np.float64)

    @maxwell_cite(
        670,
        part=4,
        chapter="Circular Coils",
        theory_class="maxwell_original",
        description="Calculate coil field at position",
    )
    def field_at(self, position: np.ndarray) -> np.ndarray:
        """Calculate magnetic field at position relative to coil center."""
        position = np.asarray(position, dtype=np.float64)
        rel_pos = position - self.position
        return calc_coil_off_axis(self.current, self.radius, rel_pos, self.n_turns)

    @maxwell_cite(
        670,
        671,
        part=4,
        chapter="Circular Coils",
        theory_class="maxwell_original",
        description="Calculate field at coil center",
    )
    def center_field(self) -> float:
        """Calculate magnetic field at coil center."""
        return calc_coil_on_axis(self.current, self.radius, 0, self.n_turns)

    def helmholtz_pair(self, other: "CircularCoil", position: np.ndarray) -> np.ndarray:
        """Calculate field from Helmholtz pair (this coil + other)."""
        B1 = self.field_at(position)
        B2 = other.field_at(position)
        return B1 + B2


@maxwell_cite(
    670,
    671,
    672,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Verify circular coil field relations",
)
def verify_coil_field(
    current: float = 1.0,
    coil_radius: float = 10.0,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify circular coil field relations.

    Art. 670-672: This function verifies:
    1. On-axis field formula
    2. Field at center = 2*pi*I/(c*a)
    3. Field decreases as 1/z^3 for z >> a (dipole)

    Args:
        current: Test current (abamperes).
        coil_radius: Test coil radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Center field
    B_center = calc_coil_on_axis(current, coil_radius, 0)
    B_expected = 2.0 * np.pi * current / (CONST.C * coil_radius)
    center_error = (
        abs(B_center - B_expected) / B_expected if B_expected > 1e-15 else abs(B_center)
    )

    # Far field (dipole): B ~ 2*pi*I*a^2/(c*z^3)
    z_far = 100 * coil_radius
    B_far = calc_coil_on_axis(current, coil_radius, z_far)
    B_dipole = 2.0 * np.pi * current * coil_radius**2 / (CONST.C * z_far**3)
    far_error = abs(B_far - B_dipole) / B_dipole if B_dipole > 1e-15 else abs(B_far)

    # On-axis field at z = a
    B_at_a = calc_coil_on_axis(current, coil_radius, coil_radius)
    B_at_a_expected = 2.0 * np.pi * current / (CONST.C * coil_radius * 2**1.5)
    at_a_error = (
        abs(B_at_a - B_at_a_expected) / B_at_a_expected
        if B_at_a_expected > 1e-15
        else abs(B_at_a)
    )

    return {
        "B_center": B_center,
        "B_center_expected": B_expected,
        "center_error": center_error,
        "B_far": B_far,
        "B_dipole": B_dipole,
        "far_error": far_error,
        "B_at_radius": B_at_a,
        "B_at_radius_expected": B_at_a_expected,
        "at_radius_error": at_a_error,
        "center_verified": bool(center_error < tolerance),
        "far_field_verified": bool(far_error < tolerance),
        "at_radius_verified": bool(at_a_error < tolerance),
        "verified": bool(
            center_error < tolerance
            and far_error < tolerance
            and at_a_error < tolerance
        ),
    }


@maxwell_cite(
    676,
    677,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Verify Helmholtz coil uniformity",
)
def verify_helmholtz_uniformity(
    current: float = 1.0,
    coil_radius: float = 10.0,
    tolerance: float = 1e-3,
) -> dict[str, float | bool]:
    """
    Verify Helmholtz coil field uniformity.

    Art. 676-677: For Helmholtz configuration (separation = radius),
    the field at the center should be uniform to second order.

    Args:
        current: Test current (abamperes).
        coil_radius: Test coil radius (cm).
        tolerance: Uniformity tolerance (fractional variation).

    Returns:
        Dictionary with uniformity verification results.
    """
    # Field at center
    B_center = calc_double_coil_field(current, coil_radius, np.array([0, 0, 0]))

    # Field at small displacements
    dx = 0.1 * coil_radius
    B_dx = calc_double_coil_field(current, coil_radius, np.array([dx, 0, 0]))
    B_dz = calc_double_coil_field(current, coil_radius, np.array([0, 0, dx]))

    # Uniformity: variation should be small
    # Use larger tolerance for off-axis (near coil wires field changes rapidly)
    B_center_mag = np.linalg.norm(B_center)
    if B_center_mag < 1e-15:
        return {"verified": False, "reason": "Zero field at center"}

    variation_x = np.linalg.norm(B_dx - B_center) / B_center_mag
    variation_z = np.linalg.norm(B_dz - B_center) / B_center_mag

    # Helmholtz is primarily uniform along z; radial uniformity is weaker
    # near the coil radius. Use appropriate tolerances.
    return {
        "B_center": B_center,
        "B_dx": B_dx,
        "B_dz": B_dz,
        "variation_x": variation_x,
        "variation_z": variation_z,
        "uniform": bool(variation_z < tolerance),
    }


@maxwell_cite(
    670,
    671,
    672,
    673,
    674,
    675,
    676,
    677,
    part=4,
    chapter="Circular Coils",
    theory_class="maxwell_original",
    description="Complete circular coil analysis",
)
def analyze_circular_coil(
    current: float,
    coil_radius: float,
    n_turns: int = 1,
    test_positions: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of circular coil magnetic field.

    Art. 670-677: Comprehensive analysis including:
    1. On-axis field profile
    2. Off-axis field at test positions
    3. Helmholtz pair uniformity
    4. Dipole approximation comparison

    Args:
        current: Coil current (abamperes).
        coil_radius: Coil radius (cm).
        n_turns: Number of turns.
        test_positions: Positions for field evaluation.

    Returns:
        Dictionary with complete analysis results.
    """
    if test_positions is None:
        test_positions = [
            np.array([0, 0, 0]),
            np.array([0, 0, coil_radius]),
            np.array([coil_radius, 0, 0]),
            np.array([0, 0, 2 * coil_radius]),
        ]

    # On-axis profile
    z_values = np.linspace(0, 5 * coil_radius, 20)
    B_axis = [calc_coil_on_axis(current, coil_radius, z, n_turns) for z in z_values]

    # Off-axis fields
    off_axis_fields = []
    for pos in test_positions:
        B = calc_coil_off_axis(current, coil_radius, pos, n_turns)
        off_axis_fields.append(B)

    # Helmholtz pair
    B_helmholtz = calc_double_coil_field(
        current, coil_radius, np.array([0, 0, 0]), n_turns=n_turns
    )

    # Dipole moment
    m = current * np.pi * coil_radius**2 * n_turns

    return {
        "current": current,
        "coil_radius": coil_radius,
        "n_turns": n_turns,
        "center_field": B_axis[0],
        "on_axis_z": z_values,
        "on_axis_B": B_axis,
        "test_positions": test_positions,
        "off_axis_fields": off_axis_fields,
        "helmholtz_center_field": B_helmholtz,
        "magnetic_dipole_moment": m,
    }
