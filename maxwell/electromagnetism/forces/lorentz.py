"""
Lorentz Force — the force on currents and moving charges in magnetic fields.

Implements the Lorentz force law as described by Maxwell in Articles 490-492:

- Force on current element: dF = I·dl × B (Art. 490)
- Force on moving charge in magnetic field (Art. 491)
- Force between parallel currents (Art. 492)

Maxwell's CGS-EMU formulation:
    Force on wire: F = I·L × B          (dynes, with I in abamperes, B in gauss, L in cm)
    Force on charge: F = q·v × B        (dynes, in CGS-EMU)
    Parallel currents: F/L = 2·I₁·I₂/r  (dynes/cm, attractive for same direction)

where:
    I = current in abamperes (EMU)
    L = conductor length vector in cm
    B = magnetic flux density in gauss
    q = charge in abcoulombs (EMU) or statcoulombs (ESU)
    v = velocity in cm/s
    F = force in dynes

Category: A (maxwell_original) — Maxwell's theory of electromagnetic forces.

References:
    Part IV, Arts. 490-492: Lorentz force on currents and charges.
    Part IV, Ch. II: Force between current-carrying conductors.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class LorentzForce:
    """
    Lorentz force on a current-carrying conductor in a magnetic field.

    Art. 490-491: The force on a current-carrying conductor placed in a
    magnetic field is given by the cross product of the current element
    and the magnetic field.

    For a straight conductor of length L carrying current I in field B:
        F = I · L × B  (dynes)

    The force direction follows the right-hand rule: point fingers in
    current direction, curl toward B field, thumb points in force direction.

    Attributes:
        current: Current in abamperes (EMU).
        B_field: Magnetic field vector in gauss.
        length: Conductor length vector in cm.
    """

    current: float
    B_field: np.ndarray
    length: np.ndarray

    def __post_init__(self):
        """Validate parameters and convert to arrays.

        Ensures current is non-negative and converts B_field and length
        to numpy arrays with proper shape validation.
        """
        if self.current < 0:
            raise ValueError(f"Current must be non-negative, got {self.current}")

        self.B_field = np.asarray(self.B_field, dtype=np.float64)
        self.length = np.asarray(self.length, dtype=np.float64)

        if self.B_field.shape != (3,):
            raise ValueError(
                f"B_field must be 3D vector, got shape {self.B_field.shape}"
            )
        if self.length.shape != (3,):
            raise ValueError(f"Length must be 3D vector, got shape {self.length.shape}")

    @property
    def force_vector(self) -> np.ndarray:
        """
        Calculate the force vector.

        Returns:
            F = I · L × B (dynes).
        """
        return self.current * np.cross(self.length, self.B_field)

    @property
    def magnitude(self) -> float:
        """
        Magnitude of the Lorentz force.

        Returns:
            |F| = I · |L| · |B| · sin(θ) (dynes), where θ is angle between L and B.
        """
        return float(np.linalg.norm(self.force_vector))

    @property
    def direction(self) -> np.ndarray:
        """
        Unit vector in force direction.

        Returns:
            Unit vector in direction of force, or zero vector if force is zero.
        """
        mag = self.magnitude
        if mag == 0:
            return np.zeros(3)
        return self.force_vector / mag

    @classmethod
    @maxwell_cite(
        490,
        491,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Create Lorentz force from current, length, and B field",
    )
    def from_current_length_field(
        cls,
        current: float,
        length: np.ndarray,
        B_field: np.ndarray,
    ) -> LorentzForce:
        """
        Create Lorentz force calculator from current, conductor length, and field.

        Art. 490-491: The fundamental relation for force on a current-carrying
        conductor in a magnetic field: F = I · L × B

        Args:
            current: Current in abamperes (EMU).
            length: Conductor length vector in cm.
            B_field: Magnetic field vector in gauss.

        Returns:
            LorentzForce object.

        Reference:
            Part IV, Arts. 490-491: Force on current in magnetic field.
        """
        return cls(current=current, B_field=B_field, length=length)

    @maxwell_cite(
        490,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force at a point with given field",
    )
    def force_at(self, position: np.ndarray = None) -> np.ndarray:
        """
        Calculate force vector (position-independent for uniform field).

        Art. 490: The force on a current element depends only on the local
        magnetic field and the current element orientation.

        Args:
            position: Optional position vector (cm) — for compatibility with
                      field-based APIs, though force is position-independent
                      for uniform fields.

        Returns:
            Force vector F = I · L × B (dynes).

        Reference:
            Part IV, Art. 490: Force on current element.
        """
        return self.force_vector

    @maxwell_cite(
        490,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force magnitude",
    )
    def magnitude_at(self, position: np.ndarray = None) -> float:
        """
        Calculate force magnitude.

        Art. 490: |F| = I · |L| · |B| · sin(θ)

        Args:
            position: Optional position vector — for API compatibility.

        Returns:
            Force magnitude (dynes).

        Reference:
            Part IV, Art. 490: Force magnitude calculation.
        """
        return self.magnitude

    @maxwell_cite(
        490,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force direction",
    )
    def direction_at(self, position: np.ndarray = None) -> np.ndarray:
        """
        Calculate unit vector in force direction.

        Art. 490: Force direction follows right-hand rule from L × B.

        Args:
            position: Optional position vector — for API compatibility.

        Returns:
            Unit vector in force direction.

        Reference:
            Part IV, Art. 490: Force direction.
        """
        return self.direction


@maxwell_cite(
    490,
    491,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate force on current-carrying wire: F = I·L × B",
)
def calc_force_on_wire(
    current: float,
    length: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic force on a straight current-carrying wire.

    Art. 490-491: The Lorentz force on a conductor carrying current I
    with length vector L in a magnetic field B is:

        F = I · L × B  (dynes)

    where:
        I = current in abamperes (EMU)
        L = length vector in cm (direction = current direction)
        B = magnetic field in gauss
        F = force in dynes

    The force is perpendicular to both the wire and the field, following
    the right-hand rule.

    Args:
        current: Current in abamperes (EMU). Must be non-negative.
        length: Conductor length vector in cm.
        B_field: Magnetic field vector in gauss.

    Returns:
        Force vector (dynes).

    Raises:
        ValueError: If current is negative.

    Reference:
        Part IV, Arts. 490-491: Lorentz force on current-carrying conductor.

    Example:
        >>> # 1 abampere wire, 10 cm long along x-axis, in 1000 gauss z-field
        >>> F = calc_force_on_wire(1.0, np.array([10, 0, 0]), np.array([0, 0, 1000]))
        >>> print(f"F = {F} dynes")  # F = [0. -10000. 0.] dynes
    """
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")

    length = np.asarray(length, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return current * np.cross(length, B_field)


@maxwell_cite(
    491,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate force on moving charge: F = q·v × B",
)
def calc_force_on_moving_charge(
    charge: float,
    velocity: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic force on a moving charge in a magnetic field.

    Art. 491: A charge q moving with velocity v in a magnetic field B
    experiences a force:

        F = q · v × B

    In CGS-EMU (charge in abcoulombs, v in cm/s, B in gauss):
        F = q · v × B  (dynes)

    In CGS-ESU (charge in statcoulombs):
        F = (q/c) · v × B  (dynes), where c is speed of light

    This function uses CGS-EMU by default. For ESU charges, divide result by c.

    The force is always perpendicular to both velocity and field, so it
    changes the direction of motion but not the speed (no work is done).

    Args:
        charge: Charge in abcoulombs (EMU) or statcoulombs (ESU).
                For ESU, the force will be in units requiring division by c.
        velocity: Velocity vector in cm/s.
        B_field: Magnetic field vector in gauss.

    Returns:
        Force vector (dynes for EMU charge, dynes·c for ESU charge).

    Reference:
        Part IV, Art. 491: Force on moving charge in magnetic field.

    Example:
        >>> # Electron (1.6e-20 abcoulombs) moving at 1e9 cm/s in 1000 gauss field
        >>> F = calc_force_on_moving_charge(1.6e-20, np.array([1e9, 0, 0]), np.array([0, 0, 1000]))
        >>> print(f"F = {F} dynes")  # F = [0. -1.6e-8 0.] dynes
    """
    charge = float(charge)
    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return charge * np.cross(velocity, B_field)


@maxwell_cite(
    492,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate force between parallel currents: F = 2·I₁·I₂·L/r",
)
def calc_force_between_parallel_currents(
    I1: float,
    I2: float,
    separation: float,
    wire_length: float,
) -> float:
    """
    Calculate force between two parallel current-carrying wires.

    Art. 492: Two parallel wires carrying currents exert forces on each other
    due to the magnetic field each produces. For infinitely long parallel wires:

        F/L = 2 · I₁ · I₂ / r  (dynes/cm)

        F = 2 · I₁ · I₂ · L / r  (dynes)

    where:
        I₁, I₂ = currents in abamperes (EMU)
        r = separation between wires in cm
        L = length of wire segment in cm
        F = force in dynes

    The force is attractive when currents flow in the same direction,
    repulsive when they flow in opposite directions (negative I).

    Args:
        I1: Current in first wire (abamperes).
        I2: Current in second wire (abamperes).
        separation: Distance between wires in cm. Must be positive.
        wire_length: Length of wire segment to calculate force for in cm.

    Returns:
        Force magnitude (dynes). Positive = attractive (same direction),
        negative = repulsive (opposite directions).

    Raises:
        ValueError: If separation is not positive.

    Reference:
        Part IV, Art. 492: Force between parallel currents.

    Example:
        >>> # Two 1 abampere wires, 1 cm apart, 10 cm length
        >>> F = calc_force_between_parallel_currents(1.0, 1.0, 1.0, 10.0)
        >>> print(f"F = {F} dynes")  # F = 20.0 dynes (attractive)
    """
    if separation <= 0:
        raise ValueError(f"Separation must be positive, got {separation}")

    # F = 2 · I₁ · I₂ · L / r
    return 2.0 * I1 * I2 * wire_length / separation


@maxwell_cite(
    490,
    491,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate torque on current loop: τ = m × B",
)
def calc_torque_on_current_loop(
    magnetic_moment: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate torque on a current loop (magnetic dipole) in magnetic field.

    Art. 490-491: A current loop with magnetic moment m in a magnetic field B
    experiences a torque:

        τ = m × B  (dyne·cm)

    where:
        m = magnetic moment vector in EMU (erg/gauss or abampere·cm²)
        B = magnetic field in gauss
        τ = torque in dyne·cm

    The torque tends to align the magnetic moment with the field.
    The potential energy is U = -m · B.

    Args:
        magnetic_moment: Magnetic moment vector (EMU, erg/gauss).
        B_field: Magnetic field vector (gauss).

    Returns:
        Torque vector (dyne·cm).

    Reference:
        Part IV, Arts. 490-491: Torque on magnetic dipole.

    Example:
        >>> # Magnetic moment of 100 EMU at 90° to 1000 gauss field
        >>> m = np.array([100, 0, 0])
        >>> B = np.array([0, 0, 1000])
        >>> tau = calc_torque_on_current_loop(m, B)
        >>> print(f"τ = {tau} dyne·cm")  # τ = [0. -100000. 0.] dyne·cm
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return np.cross(magnetic_moment, B_field)


@maxwell_cite(
    490,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate force density: f = J × B",
)
def calc_force_density(
    J: np.ndarray,
    B: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic force density (force per unit volume).

    Art. 490: For a continuous current distribution with current density J
    in a magnetic field B, the force per unit volume is:

        f = J × B  (dynes/cm³)

    where:
        J = current density in abamperes/cm²
        B = magnetic field in gauss
        f = force density in dynes/cm³

    This is the differential form of the Lorentz force, applicable to
    bulk conductors and plasma.

    Args:
        J: Current density vector (abamperes/cm²).
        B: Magnetic field vector (gauss).

    Returns:
        Force density vector (dynes/cm³).

    Reference:
        Part IV, Art. 490: Force density in current distributions.

    Example:
        >>> # Current density of 1 abA/cm² in 1000 gauss field
        >>> f = calc_force_density(np.array([1, 0, 0]), np.array([0, 0, 1000]))
        >>> print(f"f = {f} dynes/cm³")  # f = [0. -1000. 0.] dynes/cm³
    """
    J = np.asarray(J, dtype=np.float64)
    B = np.asarray(B, dtype=np.float64)

    return np.cross(J, B)


@maxwell_cite(
    492,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Verify attraction of parallel currents with same direction",
)
def verify_parallel_current_attraction(
    I1: float = 1.0,
    I2: float = 1.0,
    separation: float = 1.0,
    wire_length: float = 10.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the force law for parallel currents.

    Art. 492: This function verifies the fundamental relationship:

        F = 2 · I₁ · I₂ · L / r

    and confirms that:
    1. Same-direction currents attract (positive force)
    2. Opposite-direction currents repel (negative force)
    3. Force is proportional to product of currents
    4. Force is inversely proportional to separation

    Args:
        I1: Test current in first wire (abamperes, default: 1.0).
        I2: Test current in second wire (abamperes, default: 1.0).
        separation: Wire separation in cm (default: 1.0).
        wire_length: Wire length in cm (default: 10.0).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - force_same_direction: Force when both currents positive (dynes)
        - force_opposite_direction: Force when I2 is negated (dynes)
        - expected_same: Expected force for same direction
        - expected_opposite: Expected force for opposite direction
        - attraction_verified: True if same-direction attracts
        - repulsion_verified: True if opposite-direction repels
        - inverse_r_verified: True if F ∝ 1/r
        - verified: True if all verifications pass

    Reference:
        Part IV, Art. 492: Parallel current force verification.

    Example:
        >>> result = verify_parallel_current_attraction()
        >>> assert result["verified"]  # Should pass for ideal calculation
    """
    # Force for same direction (should be attractive/positive)
    force_same = calc_force_between_parallel_currents(I1, I2, separation, wire_length)
    expected_same = 2.0 * I1 * I2 * wire_length / separation

    # Force for opposite direction (should be repulsive/negative)
    force_opposite = calc_force_between_parallel_currents(
        I1, -I2, separation, wire_length
    )
    expected_opposite = 2.0 * I1 * (-I2) * wire_length / separation

    # Verify inverse-distance law by checking at different separations
    separations_test = [0.5, 1.0, 2.0, 5.0]
    F_r_products = []
    for r in separations_test:
        F = calc_force_between_parallel_currents(I1, I2, r, wire_length)
        F_r_products.append(F * r)  # Should be constant = 2·I₁·I₂·L

    expected_F_r = 2.0 * I1 * I2 * wire_length
    inverse_r_errors = [abs(Fr - expected_F_r) / expected_F_r for Fr in F_r_products]
    inverse_r_max_error = max(inverse_r_errors)

    # Verification checks
    attraction_verified = force_same > 0 and abs(
        force_same - expected_same
    ) < tolerance * abs(expected_same)
    repulsion_verified = force_opposite < 0 and abs(
        force_opposite - expected_opposite
    ) < tolerance * abs(expected_opposite)
    inverse_r_verified = inverse_r_max_error <= tolerance

    verified = attraction_verified and repulsion_verified and inverse_r_verified

    return {
        "force_same_direction": force_same,
        "force_opposite_direction": force_opposite,
        "expected_same": expected_same,
        "expected_opposite": expected_opposite,
        "F_r_products": F_r_products,
        "expected_F_r_constant": expected_F_r,
        "inverse_r_max_error": inverse_r_max_error,
        "attraction_verified": attraction_verified,
        "repulsion_verified": repulsion_verified,
        "inverse_r_verified": inverse_r_verified,
        "verified": verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    490,
    491,
    492,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Complete Lorentz force analysis for current in magnetic field",
)
def analyze_lorentz_force(
    current: float,
    wire_length: np.ndarray,
    B_field: np.ndarray,
    wire_mass: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform comprehensive Lorentz force analysis.

    Art. 490-492: Complete analysis of a current-carrying wire in a
    magnetic field, including:

    1. Force vector and magnitude
    2. Force direction relative to wire and field
    3. Angle between wire and field (affects force magnitude)
    4. Acceleration if wire mass is provided
    5. Power considerations (force does no work on charges)

    Args:
        current: Current in abamperes (EMU).
        wire_length: Wire length vector in cm.
        B_field: Magnetic field vector in gauss.
        wire_mass: Optional wire mass in grams for acceleration calculation.

    Returns:
        Dictionary with:
        - force_vector: F = I·L × B (dynes)
        - force_magnitude: |F| (dynes)
        - force_direction: Unit vector in force direction
        - wire_length_magnitude: |L| (cm)
        - B_field_magnitude: |B| (gauss)
        - angle_wire_field: Angle between wire and field (radians)
        - sin_theta: sin(θ) — determines force magnitude factor
        - max_possible_force: I·L·B (when wire ⊥ field)
        - efficiency: Actual force / max force = sin(θ)
        - acceleration: F/m (cm/s²) if mass provided

    Reference:
        Part IV, Arts. 490-492: Complete Lorentz force analysis.

    Example:
        >>> result = analyze_lorentz_force(
        ...     current=1.0,
        ...     wire_length=np.array([10, 0, 0]),
        ...     B_field=np.array([0, 0, 1000]),
        ...     wire_mass=0.1  # 0.1 gram wire
        ... )
        >>> print(f"Force: {result['force_magnitude']} dynes")
    """
    current = float(current)
    wire_length = np.asarray(wire_length, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    # Force calculation
    force_vector = calc_force_on_wire(current, wire_length, B_field)
    force_magnitude = float(np.linalg.norm(force_vector))
    force_direction = (
        force_vector / force_magnitude if force_magnitude > 0 else np.zeros(3)
    )

    # Geometry
    L_mag = np.linalg.norm(wire_length)
    B_mag = np.linalg.norm(B_field)

    # Angle between wire and field
    if L_mag > 0 and B_mag > 0:
        cos_theta = np.dot(wire_length, B_field) / (L_mag * B_mag)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)  # Numerical stability
        angle = np.arccos(cos_theta)
        sin_theta = np.sin(angle)
    else:
        angle = 0.0
        sin_theta = 0.0

    # Maximum possible force (when wire ⊥ field)
    max_force = current * L_mag * B_mag

    # Efficiency (what fraction of max force we get)
    efficiency = sin_theta if max_force > 0 else 0.0

    result = {
        "force_vector": force_vector,
        "force_magnitude": force_magnitude,
        "force_direction": force_direction,
        "wire_length_magnitude": L_mag,
        "B_field_magnitude": B_mag,
        "angle_wire_field": angle,
        "sin_theta": sin_theta,
        "max_possible_force": max_force,
        "efficiency": efficiency,
    }

    # Acceleration if mass provided
    if wire_mass is not None and wire_mass > 0:
        result["acceleration"] = force_magnitude / wire_mass

    return result


@maxwell_cite(
    490,
    491,
    part=4,
    chapter="Lorentz Force",
    theory_class="maxwell_original",
    description="Calculate force on arbitrary current distribution",
)
def calc_force_on_distribution(
    J_func: Callable[[np.ndarray], np.ndarray],
    B_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    n_points: int = 1000,
) -> np.ndarray:
    """
    Calculate total force on an arbitrary 3D current distribution.

    Art. 490: For a continuous current distribution J(r) in a magnetic field B(r),
    the total force is the volume integral:

        F = ∫∫∫ (J × B) dV

    This function performs numerical integration over a rectangular volume.

    Args:
        J_func: Function returning current density (abA/cm²) at position r.
        B_func: Function returning magnetic field (gauss) at position r.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) in cm.
        n_points: Number of sample points per dimension (n_points³ total).

    Returns:
        Total force vector (dynes).

    Reference:
        Part IV, Art. 490: Force on continuous current distributions.

    Example:
        >>> # Uniform current density in uniform field
        >>> J = lambda r: np.array([1.0, 0, 0])
        >>> B = lambda r: np.array([0, 0, 1000])
        >>> bounds = ((0, 1), (0, 1), (0, 1))  # 1 cm³ volume
        >>> F = calc_force_on_distribution(J, B, bounds, n_points=10)
        >>> print(f"F = {F} dynes")
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds

    # Volume and differential
    volume = (x_max - x_min) * (y_max - y_min) * (z_max - z_min)
    dV = volume / (n_points**3)

    # Generate sample points
    x_vals = np.linspace(x_min, x_max, n_points, endpoint=False)
    y_vals = np.linspace(y_min, y_max, n_points, endpoint=False)
    z_vals = np.linspace(z_min, z_max, n_points, endpoint=False)

    total_force = np.zeros(3)

    for x in x_vals:
        for y in y_vals:
            for z in z_vals:
                r = np.array([x, y, z])
                J = np.asarray(J_func(r), dtype=np.float64)
                B = np.asarray(B_func(r), dtype=np.float64)
                f_density = np.cross(J, B)
                total_force += f_density * dV

    return total_force


class LorentzForceCalculator:
    """
    Comprehensive Lorentz force calculator for various scenarios.

    Art. 490-492: This class provides a unified interface for calculating
    all Lorentz force phenomena:

    - Force on straight current-carrying wires
    - Force on moving charges
    - Force between parallel currents
    - Torque on current loops
    - Force density in continuous distributions

    The class encapsulates Maxwell's complete theory of electromagnetic forces.

    Attributes:
        B_field: Background magnetic field vector (gauss).
    """

    def __init__(self, B_field: np.ndarray = None):
        """
        Initialize Lorentz force calculator.

        Args:
            B_field: Optional background magnetic field (gauss).
                     Can be provided later to individual methods.
        """
        self.B_field = (
            np.asarray(B_field, dtype=np.float64) if B_field is not None else None
        )

    @maxwell_cite(
        490,
        491,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force on wire with this calculator's field",
    )
    def force_on_wire(
        self,
        current: float,
        length: np.ndarray,
        B_field: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate force on a current-carrying wire.

        Art. 490-491: F = I · L × B

        Args:
            current: Current in abamperes.
            length: Wire length vector in cm.
            B_field: Optional override field (uses instance field if not provided).

        Returns:
            Force vector (dynes).

        Reference:
            Part IV, Arts. 490-491: Wire force calculation.
        """
        B = B_field if B_field is not None else self.B_field
        if B is None:
            raise ValueError("B_field must be provided")
        return calc_force_on_wire(current, length, B)

    @maxwell_cite(
        491,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force on moving charge",
    )
    def force_on_charge(
        self,
        charge: float,
        velocity: np.ndarray,
        B_field: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate force on a moving charge.

        Art. 491: F = q · v × B

        Args:
            charge: Charge in abcoulombs (EMU).
            velocity: Velocity vector in cm/s.
            B_field: Optional override field.

        Returns:
            Force vector (dynes).

        Reference:
            Part IV, Art. 491: Moving charge force.
        """
        B = B_field if B_field is not None else self.B_field
        if B is None:
            raise ValueError("B_field must be provided")
        return calc_force_on_moving_charge(charge, velocity, B)

    @maxwell_cite(
        490,
        491,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate torque on current loop",
    )
    def torque_on_loop(
        self,
        magnetic_moment: np.ndarray,
        B_field: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate torque on a magnetic dipole.

        Art. 490-491: τ = m × B

        Args:
            magnetic_moment: Magnetic moment vector (EMU).
            B_field: Optional override field.

        Returns:
            Torque vector (dyne·cm).

        Reference:
            Part IV, Arts. 490-491: Dipole torque.
        """
        B = B_field if B_field is not None else self.B_field
        if B is None:
            raise ValueError("B_field must be provided")
        return calc_torque_on_current_loop(magnetic_moment, B)

    @maxwell_cite(
        490,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Calculate force density",
    )
    def force_density(
        self,
        J: np.ndarray,
        B: np.ndarray = None,
    ) -> np.ndarray:
        """
        Calculate force density (force per unit volume).

        Art. 490: f = J × B

        Args:
            J: Current density (abA/cm²).
            B: Optional override field.

        Returns:
            Force density (dynes/cm³).

        Reference:
            Part IV, Art. 490: Force density.
        """
        B_field = B if B is not None else self.B_field
        if B_field is None:
            raise ValueError("B_field must be provided")
        return calc_force_density(J, B_field)

    @maxwell_cite(
        490,
        491,
        part=4,
        chapter="Lorentz Force",
        theory_class="maxwell_original",
        description="Complete Lorentz force analysis",
    )
    def analyze(
        self,
        current: float,
        wire_length: np.ndarray,
        B_field: np.ndarray = None,
        wire_mass: float = None,
    ) -> dict[str, float | np.ndarray]:
        """
        Perform comprehensive Lorentz force analysis.

        Art. 490-492: Complete analysis including force vector, magnitude,
        direction, geometry, and optional acceleration.

        Args:
            current: Current in abamperes.
            wire_length: Wire length vector in cm.
            B_field: Optional override field.
            wire_mass: Optional wire mass in grams.

        Returns:
            Dictionary with complete analysis results.

        Reference:
            Part IV, Arts. 490-492: Complete analysis.
        """
        B = B_field if B_field is not None else self.B_field
        if B is None:
            raise ValueError("B_field must be provided")
        return analyze_lorentz_force(current, wire_length, B, wire_mass)
