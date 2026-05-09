"""
Oersted's Discovery of Electromagnetism — the foundation of Part IV.

Implements Hans Christian Oersted's 1820 discovery that an electric current
produces a magnetic field, as described by Maxwell in Articles 475-479:

- Current-carrying wire produces magnetic field (Art. 475)
- Field circles around wire perpendicular to current (Art. 476)
- Force magnitude: H = 2I/r for infinite wire (Art. 477)
- Field from current element (Biot-Savart law) (Art. 478)
- Force on magnetic pole near current (Art. 479)

Maxwell's CGS-EMU formulation:
    H = 2I / r              (oersted, for infinite straight wire)
    dB = I * dl * sin(θ) / r²  (field from current element)
    F = m * H               (force on magnetic pole)

where:
    I = current in abamperes (EMU)
    r = distance from wire in cm
    H = magnetic field intensity in oersted (gauss)
    m = magnetic pole strength in EMU
    F = force in dynes

Category: A (maxwell_original) — Maxwell's theory of electromagnetism.

References:
    Part IV, Arts. 475-479: Oersted's discovery and its mathematical formulation.
    Part IV, Ch. I: Fundamental phenomena of electromagnetism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class OerstedField:
    """
    Magnetic field produced by a current-carrying wire (Oersted field).

    Art. 475-476: Oersted discovered that a current-carrying conductor
    produces a magnetic field that circles around the wire. The field
    direction follows the right-hand rule: thumb in current direction,
    fingers curl in field direction.

    For an infinite straight wire:
        H = 2I / r  (oersted)

    where I is current in abamperes and r is distance in cm.

    Attributes:
        current: Current in abamperes (EMU).
        distance: Radial distance from wire in cm.
        wire_axis: Unit vector along wire direction (default: z-axis).
        position: Reference position for field evaluation (cm).
    """

    current: float
    distance: float
    wire_axis: np.ndarray | None = None
    position: np.ndarray | None = None

    def __post_init__(self):
        """Validate parameters and set defaults.

        Ensures current is non-negative and distance is positive.
        Normalizes wire_axis to unit vector. Sets default position
        on the x-axis at the specified distance if not provided.
        """
        if self.current < 0:
            raise ValueError(f"Current must be non-negative, got {self.current}")
        if self.distance <= 0:
            raise ValueError(f"Distance must be positive, got {self.distance}")

        # Default wire axis is z-direction
        if self.wire_axis is None:
            self.wire_axis = np.array([0.0, 0.0, 1.0])
        else:
            self.wire_axis = np.asarray(self.wire_axis, dtype=np.float64)
            self.wire_axis = self.wire_axis / np.linalg.norm(self.wire_axis)

        # Default position is on x-axis at specified distance
        if self.position is None:
            self.position = np.array([self.distance, 0.0, 0.0])
        else:
            self.position = np.asarray(self.position, dtype=np.float64)

    @property
    def magnitude(self) -> float:
        """
        Magnitude of the Oersted field.

        Returns:
            H = 2I/r (oersted).
        """
        return 2.0 * self.current / self.distance

    @classmethod
    @maxwell_cite(
        475,
        476,
        part=4,
        chapter="Oersted's Discovery",
        theory_class="maxwell_original",
        description="Create Oersted field from current and distance",
    )
    def from_current_and_distance(
        cls,
        current: float,
        distance: float,
        wire_axis: np.ndarray = None,
    ) -> OerstedField:
        """
        Create an Oersted field from current and radial distance.

        Art. 475-476: The fundamental relation between current and
        the magnetic field it produces.

        Args:
            current: Current in abamperes (EMU).
            distance: Radial distance from wire (cm).
            wire_axis: Optional unit vector along wire (default: z-axis).

        Returns:
            OerstedField object.

        Reference:
            Part IV, Arts. 475-476: Oersted's discovery of electromagnetism.
        """
        return cls(current=current, distance=distance, wire_axis=wire_axis)

    @maxwell_cite(
        477,
        part=4,
        chapter="Oersted's Discovery",
        theory_class="maxwell_original",
        description="Calculate field magnitude at specified position",
    )
    def field_at(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field vector at a specified position.

        Art. 477: The field magnitude varies inversely with distance
        from the wire, and the direction is tangential (circular).

        For a wire along z-axis at position (x, y, z):
            H = (2I/r²) * (-y, x, 0)  (tangential direction)

        Args:
            position: Position vector (cm) where field is evaluated.

        Returns:
            Magnetic field vector (oersted).

        Reference:
            Part IV, Art. 477: Field magnitude and direction.
        """
        position = np.asarray(position, dtype=np.float64)

        # Find radial vector from wire to position
        # Project position onto plane perpendicular to wire
        z_component = np.dot(position, self.wire_axis)
        radial_vector = position - z_component * self.wire_axis
        r_mag = np.linalg.norm(radial_vector)

        if r_mag == 0:
            return np.zeros(3)  # On the wire itself (singularity)

        # Field magnitude: H = 2I/r
        H_mag = 2.0 * self.current / r_mag

        # Tangential direction: perpendicular to both radial and wire axis
        # Using right-hand rule: tangential = wire_axis × radial_unit
        radial_unit = radial_vector / r_mag
        tangential = np.cross(self.wire_axis, radial_unit)

        return H_mag * tangential

    @maxwell_cite(
        476,
        part=4,
        chapter="Oersted's Discovery",
        theory_class="maxwell_original",
        description="Calculate field direction at a point",
    )
    def direction_at(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate unit vector in field direction at a position.

        Art. 476: The magnetic field lines form closed circles around
        the wire, following the right-hand rule.

        Args:
            position: Position vector (cm).

        Returns:
            Unit vector in field direction.

        Reference:
            Part IV, Art. 476: Circular field lines.
        """
        position = np.asarray(position, dtype=np.float64)

        # Radial vector from wire
        z_component = np.dot(position, self.wire_axis)
        radial_vector = position - z_component * self.wire_axis
        r_mag = np.linalg.norm(radial_vector)

        if r_mag == 0:
            return np.zeros(3)

        # Tangential direction (right-hand rule)
        radial_unit = radial_vector / r_mag
        return np.cross(self.wire_axis, radial_unit)

    @maxwell_cite(
        477,
        part=4,
        chapter="Oersted's Discovery",
        theory_class="maxwell_original",
        description="Calculate field magnitude at a point",
    )
    def magnitude_at(self, position: np.ndarray) -> float:
        """
        Calculate field magnitude at a specific position.

        Art. 477: H = 2I/r where r is the perpendicular distance
        from the wire to the point.

        Args:
            position: Position vector (cm).

        Returns:
            Field magnitude (oersted).

        Reference:
            Part IV, Art. 477: Inverse distance law.
        """
        position = np.asarray(position, dtype=np.float64)

        # Perpendicular distance from wire
        z_component = np.dot(position, self.wire_axis)
        radial_vector = position - z_component * self.wire_axis
        r_mag = np.linalg.norm(radial_vector)

        if r_mag == 0:
            return float("inf")  # Singularity on wire

        return 2.0 * self.current / r_mag


@maxwell_cite(
    475,
    476,
    477,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Oersted field for infinite straight wire: H = 2I/r",
)
def calc_oersted_field(
    current: float,
    distance: float,
) -> float:
    """
    Calculate magnetic field intensity from an infinite straight current-carrying wire.

    Art. 475-477: Oersted's fundamental discovery — a current produces a
    circular magnetic field around the wire. For an infinitely long straight wire,
    the field magnitude at perpendicular distance r is:

        H = 2I / r  (oersted)

    where:
        I = current in abamperes (EMU)
        r = perpendicular distance from wire in cm
        H = magnetic field intensity in oersted (gauss)

    The field direction is tangential to circles centered on the wire,
    following the right-hand rule.

    Args:
        current: Current in abamperes (EMU). Must be non-negative.
        distance: Perpendicular distance from wire in cm. Must be positive.

    Returns:
        Magnetic field intensity H (oersted).

    Raises:
        ValueError: If distance is not positive.

    Reference:
        Part IV, Arts. 475-477: Oersted's discovery and field calculation.

    Example:
        >>> # 1 abampere current at 1 cm distance
        >>> H = calc_oersted_field(1.0, 1.0)
        >>> print(f"H = {H} oersted")  # H = 2.0 oersted
    """
    if distance <= 0:
        raise ValueError(f"Distance must be positive, got {distance}")
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")

    return 2.0 * current / distance


@maxwell_cite(
    477,
    478,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Field from a current element (Biot-Savart law in CGS)",
)
def calc_field_from_element(
    current: float,
    element_length: float,
    distance: float,
    angle: float,
) -> float:
    """
    Calculate magnetic field from a finite current element.

    Art. 477-478: The field contribution from a small segment of current-carrying
    wire is given by the Biot-Savart law (in CGS-EMU form):

        dB = (I * dl * sin(θ)) / r²

    where:
        I = current in abamperes
        dl = length of current element in cm
        r = distance from element to observation point in cm
        θ = angle between current direction and position vector

    This is the differential form that, when integrated, gives the complete
    field from arbitrary current distributions.

    Args:
        current: Current in abamperes (EMU).
        element_length: Length of current element (cm).
        distance: Distance from element to observation point (cm).
        angle: Angle between current direction and position vector (radians).

    Returns:
        Magnetic field contribution dB (oersted).

    Raises:
        ValueError: If distance is not positive.

    Reference:
        Part IV, Arts. 477-478: Field from current elements.

    Example:
        >>> # Current element at 90 degrees
        >>> dB = calc_field_from_element(1.0, 0.1, 1.0, np.pi/2)
        >>> print(f"dB = {dB} oersted")  # dB = 0.1 oersted
    """
    if distance <= 0:
        raise ValueError(f"Distance must be positive, got {distance}")

    # Biot-Savart: dB = I * dl * sin(θ) / r²
    return current * element_length * np.sin(angle) / (distance**2)


@maxwell_cite(
    479,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Force on magnetic pole near current-carrying wire",
)
def calc_force_on_pole(
    pole_strength: float,
    current: float,
    distance: float,
) -> float:
    """
    Calculate force on a magnetic pole placed near a current-carrying wire.

    Art. 479: A magnetic pole placed in the field produced by a current
    experiences a force proportional to its pole strength and the field intensity:

        F = m * H

    where for an infinite wire:
        H = 2I / r

    Therefore:
        F = m * (2I / r) = 2*m*I / r

    where:
        m = magnetic pole strength (EMU)
        I = current in abamperes
        r = distance from wire in cm
        F = force in dynes

    The force direction is tangential (same as field direction for N pole,
    opposite for S pole).

    Args:
        pole_strength: Magnetic pole strength m (EMU).
                       Positive = N pole, negative = S pole.
        current: Current in abamperes.
        distance: Distance from wire in cm.

    Returns:
        Force magnitude (dyne). Sign indicates direction relative to field.

    Raises:
        ValueError: If distance is not positive.

    Reference:
        Part IV, Art. 479: Force on magnetic poles in electromagnetic field.

    Example:
        >>> # Unit N pole at 1 cm from 1 abampere wire
        >>> F = calc_force_on_pole(1.0, 1.0, 1.0)
        >>> print(f"F = {F} dynes")  # F = 2.0 dynes
    """
    if distance <= 0:
        raise ValueError(f"Distance must be positive, got {distance}")

    # H = 2I/r, then F = m*H
    H = 2.0 * current / distance
    return pole_strength * H


@maxwell_cite(
    475,
    476,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Field direction vector from right-hand rule",
)
def calc_circular_field_direction(
    current: float,
    position: np.ndarray,
    wire_axis: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate the direction of the magnetic field at a point.

    Art. 475-476: The magnetic field lines form closed circles around
    the current-carrying wire. The direction is given by the right-hand rule:
    point thumb in current direction, fingers curl in field direction.

    Mathematically, for a wire along the z-axis:
        direction = (wire_axis) × (radial_unit_vector)

    The field is always perpendicular to both:
    - The wire axis (current direction)
    - The radial vector from wire to observation point

    Args:
        current: Current in abamperes (determines magnitude scaling).
        position: Position vector (cm) where direction is calculated.
        wire_axis: Optional unit vector along wire (default: z-axis [0,0,1]).

    Returns:
        Unit vector in field direction (tangential to circle around wire).

    Raises:
        ValueError: If position is on the wire (radial distance = 0).

    Reference:
        Part IV, Arts. 475-476: Circular field geometry and right-hand rule.

    Example:
        >>> # At (1, 0, 0) with current in +z: field points in +y
        >>> direction = calc_circular_field_direction(1.0, np.array([1.0, 0.0, 0.0]))
        >>> print(direction)  # [0. 1. 0.]
    """
    position = np.asarray(position, dtype=np.float64)

    if wire_axis is None:
        wire_axis = np.array([0.0, 0.0, 1.0])
    else:
        wire_axis = np.asarray(wire_axis, dtype=np.float64)
        wire_axis = wire_axis / np.linalg.norm(wire_axis)

    # Radial vector from wire to position (perpendicular to wire)
    z_component = np.dot(position, wire_axis)
    radial_vector = position - z_component * wire_axis
    r_mag = np.linalg.norm(radial_vector)

    if r_mag == 0:
        raise ValueError("Position cannot be on the wire (radial distance = 0)")

    # Right-hand rule: field direction = wire_axis × radial_unit
    radial_unit = radial_vector / r_mag
    return np.cross(wire_axis, radial_unit)


@maxwell_cite(
    475,
    476,
    477,
    478,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Verify inverse-distance law H ∝ 1/r",
)
def verify_inverse_distance_law(
    current: float = 1.0,
    distances: list[float] = None,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the inverse-distance law for Oersted's electromagnetic field.

    Art. 475-478: The field from an infinite straight wire obeys:
        H ∝ 1/r

    This means H * r should be constant (= 2I) at all distances.
    This function verifies this relationship numerically.

    Args:
        current: Test current in abamperes (default: 1.0).
        distances: List of distances to test (default: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0] cm).
        tolerance: Acceptable fractional deviation from constant H*r.

    Returns:
        Dictionary with verification results:
        - H_r_products: List of H*r values (should all equal 2I)
        - expected_constant: Expected constant value (2I)
        - deviation_max: Maximum fractional deviation from expected
        - deviation_mean: Mean fractional deviation
        - verified: True if all deviations within tolerance
        - law_type: "inverse_distance"

    Reference:
        Part IV, Arts. 475-478: Inverse-distance law verification.

    Example:
        >>> result = verify_inverse_distance_law()
        >>> assert result["verified"]  # Should pass for ideal calculation
    """
    if distances is None:
        distances = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

    expected_constant = 2.0 * current

    H_r_products = []
    for r in distances:
        if r <= 0:
            continue
        H = calc_oersted_field(current, r)
        H_r_products.append(H * r)

    if len(H_r_products) < 2:
        return {
            "verified": False,
            "error": "Need at least 2 valid distances",
            "law_type": "inverse_distance",
        }

    # Calculate deviations from expected constant
    deviations = [
        abs(Hr - expected_constant) / expected_constant
        for Hr in H_r_products
        if expected_constant != 0
    ]

    deviation_max = max(deviations)
    deviation_mean = float(np.mean(deviations))

    verified = deviation_max <= tolerance

    return {
        "H_r_products": H_r_products,
        "expected_constant": expected_constant,
        "deviation_max": deviation_max,
        "deviation_mean": deviation_mean,
        "verified": verified,
        "tolerance_used": tolerance,
        "law_type": "inverse_distance",
    }


@maxwell_cite(
    477,
    478,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Calculate field at point from finite wire segment",
)
def calc_field_from_finite_wire(
    current: float,
    wire_start: np.ndarray,
    wire_end: np.ndarray,
    observation_point: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic field at a point from a finite straight wire segment.

    Art. 477-478: Integration of the Biot-Savart law over a finite wire segment.
    For a straight segment from point A to point B, the field at point P is:

        H = (I / r_perp) * (cos(θ₁) - cos(θ₂)) * φ_hat

    where:
        r_perp = perpendicular distance from P to wire line
        θ₁, θ₂ = angles from P to wire endpoints
        φ_hat = azimuthal (tangential) direction

    Args:
        current: Current in abamperes.
        wire_start: Start point of wire segment (cm).
        wire_end: End point of wire segment (cm).
        observation_point: Point where field is calculated (cm).

    Returns:
        Magnetic field vector (oersted).

    Reference:
        Part IV, Arts. 477-478: Field from finite current distributions.
    """
    wire_start = np.asarray(wire_start, dtype=np.float64)
    wire_end = np.asarray(wire_end, dtype=np.float64)
    obs_point = np.asarray(observation_point, dtype=np.float64)

    # Wire direction and length
    wire_dir = wire_end - wire_start
    wire_length = np.linalg.norm(wire_dir)

    if wire_length == 0:
        return np.zeros(3)  # Zero-length wire

    wire_unit = wire_dir / wire_length

    # Vector from wire start to observation point
    r_vec = obs_point - wire_start

    # Perpendicular distance from observation point to wire line
    # r_perp = |r × wire_unit|
    cross_prod = np.cross(r_vec, wire_unit)
    r_perp = np.linalg.norm(cross_prod)

    if r_perp < 1e-15:
        return np.zeros(3)  # Point is on wire line (singularity)

    # Projection of r_vec onto wire (gives position along wire)
    s = np.dot(r_vec, wire_unit)

    # Distances to endpoints along perpendicular plane
    # cos(θ) = s / sqrt(s² + r_perp²)
    r1_mag = np.sqrt(s**2 + r_perp**2)  # Distance to start
    r2_mag = np.sqrt((s - wire_length) ** 2 + r_perp**2)  # Distance to end

    cos_theta1 = s / r1_mag if r1_mag > 0 else 0
    cos_theta2 = (s - wire_length) / r2_mag if r2_mag > 0 else 0

    # Field magnitude: H = (I / r_perp) * (cos(θ₁) - cos(θ₂))
    H_mag = (current / r_perp) * (cos_theta1 - cos_theta2)

    # Direction: tangential (perpendicular to both wire and radial)
    radial_unit = cross_prod / r_perp if r_perp > 0 else np.zeros(3)
    tangential_dir = np.cross(wire_unit, radial_unit)

    return H_mag * tangential_dir


@maxwell_cite(
    479,
    part=4,
    chapter="Oersted's Discovery",
    theory_class="maxwell_original",
    description="Force and torque on dipole in Oersted field",
)
def calc_dipole_interaction(
    magnetic_moment: np.ndarray,
    current: float,
    dipole_position: np.ndarray,
    wire_axis: np.ndarray = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate force and torque on a magnetic dipole in Oersted field.

    Art. 479: A magnet (dipole) in a non-uniform magnetic field experiences
    both a force and a torque:

        Torque: τ = m × H
        Force: F = (m · ∇)H  (gradient of field dotted with moment)

    For the Oersted field from a wire, the field is non-uniform (H ∝ 1/r),
    so both effects occur.

    Args:
        magnetic_moment: Magnetic moment vector m (EMU, erg/gauss).
        current: Current in abamperes.
        dipole_position: Position of dipole (cm).
        wire_axis: Optional unit vector along wire (default: z-axis).

    Returns:
        Dictionary with:
        - torque: Torque vector (dyne·cm)
        - force: Force vector (dyne)
        - field: Local field vector (oersted)
        - potential_energy: Energy -m·H (erg)

    Reference:
        Part IV, Art. 479: Magnetic dipole in electromagnetic field.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    dipole_position = np.asarray(dipole_position, dtype=np.float64)

    if wire_axis is None:
        wire_axis = np.array([0.0, 0.0, 1.0])
    else:
        wire_axis = np.asarray(wire_axis, dtype=np.float64)

    # Create Oersted field object
    r_perp = np.linalg.norm(
        dipole_position - np.dot(dipole_position, wire_axis) * wire_axis
    )

    if r_perp <= 0:
        return {
            "torque": np.zeros(3),
            "force": np.zeros(3),
            "field": np.zeros(3),
            "potential_energy": 0.0,
            "error": "Dipole on wire axis",
        }

    field_obj = OerstedField(current=current, distance=r_perp, wire_axis=wire_axis)

    # Local field
    H = field_obj.field_at(dipole_position)

    # Torque: τ = m × H
    torque = np.cross(magnetic_moment, H)

    # Potential energy: U = -m · H
    energy = -np.dot(magnetic_moment, H)

    # Force: F = (m · ∇)H
    # For Oersted field, H ∝ 1/r, so ∇H points radially inward
    # F ≈ (m · r_hat) * (dH/dr) in the radial direction
    # dH/dr = -2I/r² = -H/r

    radial_dir = dipole_position - np.dot(dipole_position, wire_axis) * wire_axis
    radial_dir = (
        radial_dir / np.linalg.norm(radial_dir)
        if np.linalg.norm(radial_dir) > 0
        else np.zeros(3)
    )

    # Gradient contribution (simplified for central field)
    dH_dr = -2.0 * current / (r_perp**2)

    # Force from field gradient
    m_radial = np.dot(magnetic_moment, radial_dir)
    force = m_radial * dH_dr * radial_dir

    # Additional force from torque-induced alignment (simplified)
    # This is a first-order approximation

    return {
        "torque": torque,
        "force": force,
        "field": H,
        "potential_energy": energy,
        "field_magnitude": np.linalg.norm(H),
    }
