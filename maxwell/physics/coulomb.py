"""
Coulomb's Law — the fundamental law of electrostatic force.

Implements the inverse-square law of electrostatic attraction and repulsion
from Part I of Maxwell's Treatise:

- Direct and inverse variation of force (Arts. 38-40)
- Law of force between electrified bodies (Art. 66)
- Resultant force calculations (Art. 67)
- Resultant intensity (Art. 68)
- Proof of the inverse-square law (Art. 43)

Maxwell's formulation (CGS-ESU):
    F = q1 * q2 / r^2  (dyne)

where q1, q2 are in statcoulombs (esu) and r is in centimeters.

Category: A (maxwell_original) — Maxwell's law of electrostatic force.

References:
    Part I, Arts. 38-40: Measurement and variation of electric force.
    Part I, Arts. 66-68: Mathematical formulation of Coulomb's law.
    Part I, Art. 43: Experimental proof of inverse-square law.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.charge import PointCharge
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectrostaticForce:
    """
    The electrostatic force between two charged bodies.

    Art. 38-40: The force of attraction or repulsion between electrified bodies.

    Coulomb's Law in CGS-ESU:
        F = q1 * q2 / r^2

    The force is:
    - Repulsive (F > 0) when charges have the same sign
    - Attractive (F < 0) when charges have opposite signs

    Attributes:
        magnitude: Force magnitude (dyne).
        direction: Unit vector pointing from q1 to q2.
        q1: First charge (esu).
        q2: Second charge (esu).
        separation: Distance between charges (cm).
    """

    magnitude: float
    direction: np.ndarray  # shape (3,)
    q1: float
    q2: float
    separation: float

    def __post_init__(self):
        self.direction = np.asarray(self.direction, dtype=np.float64)
        if self.direction.shape != (3,):
            raise ValueError(f"Direction must be 3D, got shape {self.direction.shape}")

    @property
    def force_vector(self) -> np.ndarray:
        """Force vector acting on q2 due to q1."""
        return self.magnitude * self.direction

    @property
    def is_attractive(self) -> bool:
        """True if the force is attractive (opposite charges)."""
        return self.q1 * self.q2 < 0

    @property
    def is_repulsive(self) -> bool:
        """True if the force is repulsive (like charges)."""
        return self.q1 * self.q2 > 0


@maxwell_cite(
    66,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Coulomb's law — force between two point charges",
)
def coulomb_law(
    q1: float,
    q2: float,
    r: float,
) -> float:
    """
    Calculate the magnitude of electrostatic force between two point charges.

    Art. 66: The law of force between electrified bodies varies inversely
    as the square of the distance.

    In CGS-ESU:
        F = q1 * q2 / r^2

    where:
    - q1, q2 are in statcoulombs (esu)
    - r is in centimeters
    - F is in dynes

    Args:
        q1: First charge (esu).
        q2: Second charge (esu).
        r: Separation distance (cm).

    Returns:
        Force magnitude (dyne). Positive = repulsive, negative = attractive.

    Reference:
        Part I, Art. 66: Law of force between electrified bodies.

    Note:
        Maxwell's notation uses C for charge, but we use q for clarity.
        The CGS-ESU system makes the proportionality constant = 1.
    """
    if r <= 0:
        raise ValueError(f"Separation must be positive, got {r}")

    return q1 * q2 / (r**2)


@maxwell_cite(
    67,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Resultant force between two charged bodies",
)
def resultant_force(
    charge1: PointCharge,
    charge2: PointCharge,
) -> ElectrostaticForce:
    """
    Calculate the resultant force between two point charges.

    Art. 67: The resultant force on a body due to multiple attractions
    and repulsions is the vector sum of individual forces.

    For two charges:
        F = (q1 * q2 / r^2) * r_hat

    where r_hat is the unit vector from q1 to q2.

    Args:
        charge1: First PointCharge object.
        charge2: Second PointCharge object.

    Returns:
        ElectrostaticForce object with magnitude and direction.

    Reference:
        Part I, Art. 67: Resultant force between two bodies.
    """
    r_vec = charge2.position - charge1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag == 0:
        raise ValueError("Charges cannot occupy the same position")

    r_hat = r_vec / r_mag

    # Coulomb's law magnitude
    F_mag = coulomb_law(charge1.q, charge2.q, r_mag)

    return ElectrostaticForce(
        magnitude=F_mag,
        direction=r_hat,
        q1=charge1.q,
        q2=charge2.q,
        separation=r_mag,
    )


@maxwell_cite(
    67,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Resultant force on a charge from multiple sources",
)
def resultant_force_multiple(
    target_charge: PointCharge,
    source_charges: list[PointCharge],
) -> np.ndarray:
    """
    Calculate resultant force on a charge from multiple source charges.

    Art. 67: The resultant is found by compounding all the separate forces
    using the parallelogram law (vector addition).

    F_resultant = sum_i F_i

    where F_i is the force from each source charge.

    Args:
        target_charge: The PointCharge experiencing the force.
        source_charges: List of PointCharge objects exerting forces.

    Returns:
        Resultant force vector (dyne).

    Reference:
        Part I, Art. 67: Resultant force from multiple sources.
    """
    F_total = np.zeros(3)

    for source in source_charges:
        r_vec = target_charge.position - source.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            continue  # Skip self-interaction

        r_hat = r_vec / r_mag
        F_mag = coulomb_law(source.q, target_charge.q, r_mag)

        # Force on target points away from source if repulsive
        F_total += F_mag * r_hat

    return F_total


@maxwell_cite(
    68,
    part=1,
    chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Resultant intensity of electric force at a point",
)
def field_intensity(
    point: np.ndarray,
    source_charges: list[PointCharge],
) -> np.ndarray:
    """
    Calculate the resultant electric intensity at a point.

    Art. 68: The resultant intensity at any point is the resultant force
    on a unit positive charge placed at that point.

    E = F / q_test  (as q_test -> 1)

    In CGS-ESU:
        E = sum_i (q_i / r_i^2) * r_hat_i

    Args:
        point: Position vector (cm) where intensity is calculated.
        source_charges: List of PointCharge objects creating the field.

    Returns:
        Electric field intensity vector (statvolt/cm = dyne/esu).

    Reference:
        Part I, Art. 68: Resultant intensity of electric force.
    """
    point = np.asarray(point, dtype=np.float64)

    E_total = np.zeros(3)

    for source in source_charges:
        r_vec = point - source.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            continue  # Skip singularity

        r_hat = r_vec / r_mag
        E_mag = source.q / (r_mag**2)

        E_total += E_mag * r_hat

    return E_total


@maxwell_cite(
    38,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Measurement of force between electrified bodies",
)
def measure_force(
    q1: float,
    q2: float,
    distance_cm: float,
) -> dict[str, float]:
    """
    Measure and analyze the force between two electrified bodies.

    Art. 38: By means of the torsion-balance we can measure the force
    between two charged bodies at different distances.

    Returns a dictionary with:
    - force_dyne: Force in dynes
    - force_newton: Force in newtons (SI equivalent)
    - separation_cm: Separation in centimeters

    Args:
        q1: First charge (esu).
        q2: Second charge (esu).
        distance_cm: Separation distance (cm).

    Returns:
        Dictionary with force measurements.

    Reference:
        Part I, Art. 38: Measurement of the force between electrified bodies.
    """
    force_dyne = coulomb_law(q1, q2, distance_cm)
    force_newton = force_dyne * 1e-5  # 1 dyne = 10^-5 newton

    return {
        "force_dyne": force_dyne,
        "force_newton": force_newton,
        "separation_cm": distance_cm,
        "q1_esu": q1,
        "q2_esu": q2,
    }


@maxwell_cite(
    39,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Relation between force and quantities of electricity",
)
def force_charge_relation(
    force_dyne: float,
    distance_cm: float,
    known_charge: float,
) -> float:
    """
    Determine an unknown charge from force measurements.

    Art. 39: From measurements of force at known distances, we can
    determine the quantities of electricity on each body.

    Given F, r, and q1:
        q2 = F * r^2 / q1

    Args:
        force_dyne: Measured force (dyne).
        distance_cm: Separation distance (cm).
        known_charge: Known charge q1 (esu).

    Returns:
        Unknown charge q2 (esu).

    Reference:
        Part I, Art. 39: Relation between force and quantities of electricity.
    """
    if distance_cm <= 0:
        raise ValueError(f"Distance must be positive, got {distance_cm}")
    if known_charge == 0:
        raise ValueError("Known charge cannot be zero")

    return force_dyne * (distance_cm**2) / known_charge


@maxwell_cite(
    40,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Variation of force with distance — inverse square law",
)
def force_distance_law(
    q1: float,
    q2: float,
    distances: list[float],
) -> list[dict[str, float]]:
    """
    Calculate force at various distances to verify inverse-square law.

    Art. 40: The force varies inversely as the square of the distance.

    F is proportional to 1/r^2

    This function computes the force at multiple distances, allowing
    experimental verification of the inverse-square relationship.

    Args:
        q1: First charge (esu).
        q2: Second charge (esu).
        distances: List of separation distances (cm) to evaluate.

    Returns:
        List of dictionaries with distance, force, and 1/r^2 values.

    Reference:
        Part I, Art. 40: Variation of the force with distance.
    """
    results = []
    for r in distances:
        if r <= 0:
            continue
        F = coulomb_law(q1, q2, r)
        results.append(
            {
                "distance_cm": r,
                "force_dyne": F,
                "inverse_r_squared": 1.0 / (r**2),
                "F_times_r_squared": F * (r**2),  # Should be constant = q1*q2
            }
        )
    return results


@maxwell_cite(
    43,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Proof of the inverse-square law — Cavendish's experiment",
)
def verify_inverse_square_law(
    measured_forces: list[float],
    distances: list[float],
    tolerance: float = 0.01,
) -> dict[str, float]:
    """
    Verify the inverse-square law from experimental data.

    Art. 43: Cavendish's proof that the force varies inversely as the
    square of the distance. If F * r^2 is constant, the law is verified.

    This function analyzes measured forces at different distances to
    determine how well they fit the inverse-square relationship.

    Args:
        measured_forces: List of measured forces (dyne).
        distances: List of corresponding distances (cm).
        tolerance: Acceptable deviation from constant (fractional).

    Returns:
        Dictionary with verification results:
        - constant_mean: Mean of F*r^2 values
        - constant_std: Standard deviation
        - deviation_max: Maximum fractional deviation
        - verified: True if within tolerance

    Reference:
        Part I, Art. 43: Proof of the law of force (Cavendish's experiment).
    """
    if len(measured_forces) != len(distances):
        raise ValueError("Forces and distances must have same length")
    if len(measured_forces) < 2:
        raise ValueError("Need at least 2 measurements")

    # Calculate F * r^2 for each measurement (should be constant)
    fr_squared = [F * (r**2) for F, r in zip(measured_forces, distances) if r > 0]

    if len(fr_squared) < 2:
        raise ValueError("Need at least 2 valid measurements")

    constant_mean = np.mean(fr_squared)
    constant_std = np.std(fr_squared)

    # Calculate maximum fractional deviation
    deviations = [
        abs(val - constant_mean) / constant_mean
        for val in fr_squared
        if constant_mean != 0
    ]
    deviation_max = max(deviations)

    verified = deviation_max <= tolerance

    return {
        "constant_mean": constant_mean,
        "constant_std": constant_std,
        "deviation_max": deviation_max,
        "verified": verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    30,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Conservation of charge in force interactions",
)
def verify_charge_conservation_force(
    initial_charges: list[float],
    final_charges: list[float],
    tolerance: float = 1e-10,
) -> bool:
    """
    Verify charge conservation in an interaction.

    Art. 30: The algebraic sum of all charges remains constant.
    Electrification always occurs in equal and opposite quantities.

    Args:
        initial_charges: List of charges before interaction.
        final_charges: List of charges after interaction.
        tolerance: Numerical tolerance for comparison.

    Returns:
        True if total charge is conserved.

    Reference:
        Part I, Art. 30: Conservation of charge.
    """
    initial_total = sum(initial_charges)
    final_total = sum(final_charges)
    return abs(initial_total - final_total) < tolerance


@maxwell_cite(
    84,
    part=1,
    chapter="Electrified Systems in Equilibrium",
    theory_class="maxwell_original",
    description="Superposition principle for electrostatic forces",
)
def superposition_force(
    test_charge: PointCharge,
    source_charges: list[PointCharge],
) -> np.ndarray:
    """
    Apply superposition principle to calculate total force.

    Art. 84: The resultant force on any body is the vector sum of
    the forces due to each of the other bodies separately.

    This is the principle of superposition applied to forces.

    Args:
        test_charge: The charge experiencing the force.
        source_charges: List of source charges.

    Returns:
        Total force vector (dyne).

    Reference:
        Part I, Art. 84: Superposition of electrified systems.
    """
    return resultant_force_multiple(test_charge, source_charges)


@maxwell_cite(
    44,
    part=1,
    chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Electric field as force per unit charge",
)
def electric_field_from_force(
    force_on_test: np.ndarray,
    test_charge: float,
) -> np.ndarray:
    """
    Calculate electric field from force on a test charge.

    Art. 44: The electric field is defined as the force per unit charge:

        E = F / q

    This is the operational definition of the electric field.

    Args:
        force_on_test: Force vector on test charge (dyne).
        test_charge: Magnitude of test charge (esu).

    Returns:
        Electric field vector (statvolt/cm = dyne/esu).

    Reference:
        Part I, Art. 44: Definition of the electric field.
    """
    if test_charge == 0:
        raise ValueError("Test charge cannot be zero")
    return force_on_test / test_charge
