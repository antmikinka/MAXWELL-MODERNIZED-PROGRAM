"""maxwell.electromagnetism.dynamics.attraction — Parallel current interaction (Arts. 496-497).

Implements Maxwell's treatment of the forces between current-carrying conductors,
including the fundamental attraction/repulsion of parallel currents.

Maxwell's CGS formulation (Arts. 496-497):
    Force per unit length between parallel wires:
        F/L = 2 * I1 * I2 / r  (dynes/cm)

    - Attractive for currents in same direction
    - Repulsive for currents in opposite directions

    This force is the basis for the definition of the electromagnetic unit of current.

where:
    I1, I2 = currents in abamperes (EMU)
    r = separation (cm)
    F/L = force per unit length (dynes/cm)

Category: A (maxwell_original) — Maxwell's theory of electromagnetic forces.

References:
    Part IV, Arts. 496-497: Forces between current-carrying conductors.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class ParallelConductorForce:
    """
    Force calculator for parallel current-carrying conductors.

    Art. 496-497: Maxwell analyzed the forces between parallel conductors
    carrying currents. The force per unit length is:

        F/L = 2 * I1 * I2 / r

    where r is the separation between conductors.

    The force is:
    - Attractive when currents flow in the same direction
    - Repulsive when currents flow in opposite directions

    This force law is fundamental to electromagnetic theory and was used
    to define the absolute unit of current (abampere).

    Attributes:
        current1: Current in first conductor (abamperes).
        current2: Current in second conductor (abamperes).
        separation: Distance between conductors (cm).
        length: Length of conductors (cm).
    """

    current1: float
    current2: float
    separation: float
    length: float = 1.0

    def __post_init__(self):
        """Validate parameters."""
        if self.separation <= 0:
            raise ValueError(f"Separation must be positive, got {self.separation}")
        if self.length <= 0:
            raise ValueError(f"Length must be positive, got {self.length}")

    @property
    def force_per_unit_length(self) -> float:
        """
        Force per unit length between conductors.

        Returns:
            F/L = 2*I1*I2/r (dynes/cm). Positive = attractive.
        """
        return 2.0 * self.current1 * self.current2 / self.separation

    @property
    def total_force(self) -> float:
        """
        Total force between conductors of given length.

        Returns:
            F = 2*I1*I2*L/r (dynes). Positive = attractive.
        """
        return self.force_per_unit_length * self.length

    @property
    def is_attractive(self) -> bool:
        """
        Check if force is attractive.

        Returns:
            True if currents are in same direction (product > 0).
        """
        return self.current1 * self.current2 > 0

    @property
    def is_repulsive(self) -> bool:
        """
        Check if force is repulsive.

        Returns:
            True if currents are in opposite directions (product < 0).
        """
        return self.current1 * self.current2 < 0


@maxwell_cite(
    496, 497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate force between parallel currents: F = 2*I1*I2*L/r",
)
def calc_force_parallel_wires(
    current1: float,
    current2: float,
    separation: float,
    length: float = 1.0,
) -> float:
    """
    Calculate force between parallel current-carrying wires.

    Art. 496-497: The force between two infinitely long parallel wires
    carrying currents I1 and I2 is:

        F = 2 * I1 * I2 * L / r

    where:
        I1, I2 = currents (abamperes)
        r = separation (cm)
        L = length of wire segment (cm)
        F = force (dynes)

    The force is attractive for same-direction currents, repulsive for
    opposite-direction currents.

    Args:
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        separation: Distance between wires (cm).
        length: Length of wire segment (cm, default 1.0).

    Returns:
        Force (dynes). Positive = attractive, negative = repulsive.

    Raises:
        ValueError: If separation or length is not positive.

    Reference:
        Part IV, Arts. 496-497: Parallel wire force.

    Example:
        >>> # Two 1 abampere wires, 1 cm apart, 10 cm length
        >>> F = calc_force_parallel_wires(1.0, 1.0, 1.0, 10.0)
        >>> print(f"F = {F} dynes")  # F = 20.0 dynes (attractive)
    """
    if separation <= 0:
        raise ValueError(f"Separation must be positive, got {separation}")
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")

    return 2.0 * current1 * current2 * length / separation


@maxwell_cite(
    496,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate force per unit length: F/L = 2*I1*I2/r",
)
def calc_force_per_unit_length(
    current1: float,
    current2: float,
    separation: float,
) -> float:
    """
    Calculate force per unit length between parallel wires.

    Art. 496: For infinitely long parallel wires:

        F/L = 2 * I1 * I2 / r

    Args:
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        separation: Distance between wires (cm).

    Returns:
        Force per unit length (dynes/cm).

    Reference:
        Part IV, Art. 496: Force per unit length.
    """
    if separation <= 0:
        raise ValueError(f"Separation must be positive, got {separation}")

    return 2.0 * current1 * current2 / separation


@maxwell_cite(
    497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate force between inclined conductors",
)
def calc_force_inclined_wires(
    current1: float,
    current2: float,
    separation: float,
    angle: float,
    length: float = 1.0,
) -> float:
    """
    Calculate force between inclined current-carrying wires.

    Art. 497: For wires at an angle theta to each other, the force is
    modified by a geometric factor. For small angles and large separations:

        F ≈ (2 * I1 * I2 * L / r) * cos(theta)

    where theta is the angle between the wire directions.

    Args:
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        separation: Minimum distance between wires (cm).
        angle: Angle between wire directions (radians).
        length: Length of wire segment (cm).

    Returns:
        Force magnitude (dynes).

    Reference:
        Part IV, Art. 497: Inclined wire force.
    """
    if separation <= 0:
        raise ValueError(f"Separation must be positive, got {separation}")

    # Geometric reduction factor
    cos_theta = np.cos(angle)

    return 2.0 * current1 * current2 * length / separation * abs(cos_theta)


@maxwell_cite(
    496, 497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate force between current elements",
)
def calc_force_between_elements(
    I1: float,
    dl1: np.ndarray,
    I2: float,
    dl2: np.ndarray,
    r_vector: np.ndarray,
) -> np.ndarray:
    """
    Calculate force between two current elements.

    Art. 496-497: The force between current elements I1*dl1 and I2*dl2
    separated by vector r is given by Ampere's force law:

        dF = (I1*I2/r³) * [2(dl1·r)(dl2·r)/r² - 3(dl1·dl2)] * r_hat
             + (I1*I2/r²) * (dl1·dl2) * r_hat

    In the form Maxwell used (equivalent to Grassmann's form):

        d²F = (I1*I2/r²) * [dl2 × (dl1 × r_hat)]

    This gives the force on element 2 due to element 1.

    Args:
        I1: Current in first element (abamperes).
        dl1: First element vector (cm).
        I2: Current in second element (abamperes).
        dl2: Second element vector (cm).
        r_vector: Vector from element 1 to element 2 (cm).

    Returns:
        Force on element 2 (dynes).

    Reference:
        Part IV, Arts. 496-497: Current element force.
    """
    dl1 = np.asarray(dl1, dtype=np.float64)
    dl2 = np.asarray(dl2, dtype=np.float64)
    r_vector = np.asarray(r_vector, dtype=np.float64)

    r_mag = np.linalg.norm(r_vector)
    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = r_vector / r_mag

    # Grassmann form: dF = (I1*I2/r²) * dl2 × (dl1 × r_hat)
    cross1 = np.cross(dl1, r_hat)
    cross2 = np.cross(dl2, cross1)

    return (I1 * I2 / (r_mag ** 2)) * cross2


@maxwell_cite(
    496,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate equilibrium current for force balance",
)
def calc_equilibrium_current(
    force_per_cm: float,
    separation: float,
    reference_current: float,
) -> float:
    """
    Calculate current needed for force equilibrium.

    Art. 496: Given a force per unit length and separation, the current
    required (assuming equal currents in both wires) is:

        I = sqrt(F/L * r / 2)

    Args:
        force_per_cm: Force per unit length (dynes/cm).
        separation: Wire separation (cm).
        reference_current: Reference current for comparison (abamperes).

    Returns:
        Required current (abamperes).

    Reference:
        Part IV, Art. 496: Equilibrium current calculation.
    """
    if separation <= 0:
        raise ValueError(f"Separation must be positive, got {separation}")

    return np.sqrt(force_per_cm * separation / 2.0)


@maxwell_cite(
    496, 497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Verify force law for parallel currents",
)
def verify_parallel_force_law(
    current1: float = 1.0,
    current2: float = 1.0,
    separations: list[float] = None,
    tolerance: float = 1e-10,
) -> dict[str, float | bool | list]:
    """
    Verify the force law for parallel currents.

    Art. 496-497: This function verifies:
    1. Force is proportional to I1 * I2
    2. Force is inversely proportional to separation
    3. Same-direction currents attract
    4. Opposite-direction currents repel

    Args:
        current1: First test current (abamperes).
        current2: Second test current (abamperes).
        separations: List of separations to test (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 496-497: Force law verification.
    """
    if separations is None:
        separations = [0.5, 1.0, 2.0, 5.0, 10.0]

    # Test inverse-distance law
    F_r_products = []
    for r in separations:
        F = calc_force_parallel_wires(current1, current2, r, length=1.0)
        F_r_products.append(F * r)  # Should be constant = 2*I1*I2

    expected_constant = 2.0 * current1 * current2
    deviations = [abs(Fr - expected_constant) / abs(expected_constant) for Fr in F_r_products if expected_constant != 0]
    max_deviation = max(deviations) if deviations else 0

    # Test current reversal (should change sign)
    F_same = calc_force_parallel_wires(current1, current2, 1.0, 1.0)
    F_opposite = calc_force_parallel_wires(current1, -current2, 1.0, 1.0)

    sign_change_verified = np.sign(F_same) != np.sign(F_opposite)
    magnitude_match = abs(abs(F_same) - abs(F_opposite)) < tolerance

    # Test current scaling (should be proportional)
    F_scaled = calc_force_parallel_wires(2*current1, current2, 1.0, 1.0)
    scaling_verified = abs(F_scaled - 2*F_same) < tolerance * abs(F_same)

    inverse_r_verified = max_deviation < tolerance

    return {
        "current1": current1,
        "current2": current2,
        "separations": separations,
        "F_r_products": F_r_products,
        "expected_constant": expected_constant,
        "max_deviation": max_deviation,
        "force_same_direction": F_same,
        "force_opposite_direction": F_opposite,
        "sign_change_verified": sign_change_verified,
        "magnitude_match": magnitude_match,
        "scaling_verified": scaling_verified,
        "inverse_r_verified": inverse_r_verified,
        "verified": all([sign_change_verified, magnitude_match, scaling_verified, inverse_r_verified]),
    }


@maxwell_cite(
    496, 497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Calculate work done by electromagnetic force",
)
def calc_work_parallel_wires(
    current1: float,
    current2: float,
    initial_separation: float,
    final_separation: float,
) -> float:
    """
    Calculate work done by electromagnetic force when wires move.

    Art. 496-497: When parallel wires move from separation r1 to r2,
    the work done by the electromagnetic force is:

        W = integral(F dr) = 2*I1*I2 * integral(dr/r) = 2*I1*I2 * ln(r2/r1)

    Args:
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        initial_separation: Initial separation (cm).
        final_separation: Final separation (cm).

    Returns:
        Work done (ergs). Positive = work done by field.

    Reference:
        Part IV, Arts. 496-497: Work calculation.
    """
    if initial_separation <= 0 or final_separation <= 0:
        raise ValueError("Separations must be positive")

    return 2.0 * current1 * current2 * np.log(final_separation / initial_separation)


@maxwell_cite(
    496, 497,
    part=4, chapter="Forces Between Conductors",
    theory_class="maxwell_original",
    description="Complete analysis of parallel conductor forces",
)
def analyze_parallel_conductor_forces(
    current1: float,
    current2: float,
    separation: float,
    length: float = 1.0,
    wire1_mass_per_length: float = None,
    wire2_mass_per_length: float = None,
) -> dict[str, float | bool]:
    """
    Complete analysis of forces between parallel conductors.

    Art. 496-497: Comprehensive analysis including:
    1. Force magnitude and direction
    2. Force per unit length
    3. Potential energy
    4. Acceleration (if masses provided)
    5. Equilibrium conditions

    Args:
        current1: Current in first wire (abamperes).
        current2: Current in second wire (abamperes).
        separation: Distance between wires (cm).
        length: Length of wires (cm).
        wire1_mass_per_length: Mass per unit length of wire 1 (g/cm).
        wire2_mass_per_length: Mass per unit length of wire 2 (g/cm).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 496-497: Complete force analysis.
    """
    force_obj = ParallelConductorForce(
        current1=current1, current2=current2,
        separation=separation, length=length
    )

    result = {
        "force_total": force_obj.total_force,
        "force_per_unit_length": force_obj.force_per_unit_length,
        "is_attractive": force_obj.is_attractive,
        "is_repulsive": force_obj.is_repulsive,
        "potential_energy": -2.0 * current1 * current2 * np.log(separation),
    }

    # Acceleration if masses provided
    if wire1_mass_per_length is not None and wire1_mass_per_length > 0:
        result["wire1_acceleration"] = force_obj.force_per_unit_length / wire1_mass_per_length

    if wire2_mass_per_length is not None and wire2_mass_per_length > 0:
        result["wire2_acceleration"] = force_obj.force_per_unit_length / wire2_mass_per_length

    # Equilibrium check (forces balanced)
    result["equilibrium"] = abs(force_obj.total_force) < 1e-15

    return result
