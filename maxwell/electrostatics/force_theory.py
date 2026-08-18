"""
Force and Elementary Theory of Electricity — Maxwell's Part I.

Implements the theory of electrostatic force and the elementary theory
of electricity from Part I of the Treatise:

- Force (Arts. 27-28, 31-37, 41-42):
  - Electric tension along lines of force
  - Attraction between charged bodies
  - Repulsion between like charges
  - Role of medium in electrostatic force
  - Superposition of electrostatic forces

- Elementary Theory of Electricity (Arts. 50-63, 65):
  - Two-fluid theory (historical)
  - One-fluid theory (Franklin)
  - Charge conservation
  - Vitreous vs resinous electricity
  - Electrostatic induction
  - Field concept: action at a distance vs medium

Category: A (maxwell_original) — Maxwell's theory of electrostatic force
and historical theories of electricity.

References:
    Part I, Chapter I, Arts. 27-28: Electric tension.
    Part I, Chapter I, Arts. 31-37: Attraction and repulsion.
    Part I, Chapter I, Arts. 41-42: Superposition of forces.
    Part I, Chapter I, Arts. 50-65: Elementary theory of electricity.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.charge import PointCharge
from maxwell.core.field import ElectricField
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# FORCE THEORY (Arts. 27-28, 31-37, 41-42)
# =============================================================================


@maxwell_cite(
    27,
    28,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electric tension along lines of force",
)
def electric_tension(
    field: ElectricField,
    length: float,
) -> float:
    """
    Calculate electric tension along a line of force.

    Arts. 27-28: Maxwell introduces the concept of electric tension as the
    integral of the electric intensity along a line of force. This represents
    the work done per unit charge and is equivalent to the potential difference
    between two points.

    For a uniform field along the line:
        Tension = |E| * L

    For a non-uniform field:
        Tension = integral(E . dl) along the line of force

    Args:
        field: ElectricField object representing the field along the line.
        length: Length of the line segment (cm).

    Returns:
        Electric tension (statvolt).

    Reference:
        Part I, Arts. 27-28: Electric tension and lines of force.

    Note:
        Art. 27: Electrification by friction produces a state of tension.
        Art. 28: The tension is measured by the potential difference.
    """
    # For uniform field approximation
    return field.magnitude * length


@maxwell_cite(
    31,
    32,
    33,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electrostatic attraction between oppositely charged bodies",
)
def electrostatic_attraction(
    charge1: PointCharge,
    charge2: PointCharge,
) -> np.ndarray:
    """
    Calculate the electrostatic force of attraction between two charged bodies.

    Arts. 31-33: Maxwell describes the law of attraction between electrified
    bodies. When charges are opposite (one positive, one negative), the force
    is attractive.

    Coulomb's law in CGS-ESU:
        F = q1 * q2 / r^2  (attractive if q1*q2 < 0)

    The force on charge 2 due to charge 1 is:
        F_12 = (q1 * q2 / r^2) * r_hat_12

    where r_hat_12 points from charge 1 to charge 2.

    Args:
        charge1: First PointCharge object.
        charge2: Second PointCharge object.

    Returns:
        Force vector on charge2 due to charge1 (dyne).
        Negative (attractive) when charges are opposite.

    Reference:
        Part I, Arts. 31-33: Law of attraction between electrified bodies.

    Note:
        Art. 31: Bodies with opposite electrification attract.
        Art. 32: Force varies as inverse square of distance.
        Art. 33: Force proportional to product of charges.
    """
    r_vec = charge2.position - charge1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag == 0:
        raise ValueError("Charges cannot occupy the same position")

    r_hat = r_vec / r_mag
    # F = q1 * q2 / r^2 (CGS-ESU)
    # If q1*q2 < 0, force is attractive (negative sign in direction of r_hat)
    force_magnitude = (charge1.q * charge2.q) / (r_mag**2)

    return force_magnitude * r_hat


@maxwell_cite(
    34,
    35,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electrostatic repulsion between like-charged bodies",
)
def repulsion_law(
    charge1: PointCharge,
    charge2: PointCharge,
) -> np.ndarray:
    """
    Calculate the electrostatic force of repulsion between like-charged bodies.

    Arts. 34-35: Maxwell describes repulsion between bodies with the same
    type of electrification. When both charges are positive (vitreous) or
    both negative (resinous), the force is repulsive.

    Coulomb's law in CGS-ESU:
        F = q1 * q2 / r^2  (repulsive if q1*q2 > 0)

    The force on charge 2 due to charge 1 is:
        F_12 = (q1 * q2 / r^2) * r_hat_12

    where r_hat_12 points from charge 1 to charge 2.

    Args:
        charge1: First PointCharge object.
        charge2: Second PointCharge object.

    Returns:
        Force vector on charge2 due to charge1 (dyne).
        Positive (repulsive) when charges have same sign.

    Reference:
        Part I, Arts. 34-35: Law of repulsion between like-charged bodies.

    Note:
        Art. 34: Bodies with same electrification repel.
        Art. 35: Law follows inverse square law like attraction.
    """
    r_vec = charge2.position - charge1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag == 0:
        raise ValueError("Charges cannot occupy the same position")

    r_hat = r_vec / r_mag
    # F = q1 * q2 / r^2 (CGS-ESU)
    # If q1*q2 > 0, force is repulsive (positive sign)
    force_magnitude = (charge1.q * charge2.q) / (r_mag**2)

    return force_magnitude * r_hat


@maxwell_cite(
    36,
    37,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Role of medium in electrostatic force",
)
def force_medium(
    charge1: PointCharge,
    charge2: PointCharge,
    inductive_capacity: float = 1.0,
) -> np.ndarray:
    """
    Calculate electrostatic force in a dielectric medium.

    Arts. 36-37: Maxwell discusses how the medium between charged bodies
    affects the electrostatic force. The specific inductive capacity
    (dielectric constant) K of the medium modifies the force.

    In a medium with specific inductive capacity K:
        F = (q1 * q2) / (K * r^2)

    For vacuum or air: K = 1
    For other dielectrics: K > 1 (force is reduced)

    Args:
        charge1: First PointCharge object.
        charge2: Second PointCharge object.
        inductive_capacity: Specific inductive capacity K of the medium
            (default 1.0 for vacuum/air).

    Returns:
        Force vector on charge2 due to charge1 in the medium (dyne).

    Reference:
        Part I, Arts. 36-37: Action of the medium on electrified bodies.

    Note:
        Art. 36: The medium transmits the electric force.
        Art. 37: Different media have different inductive capacities.
    """
    r_vec = charge2.position - charge1.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag == 0:
        raise ValueError("Charges cannot occupy the same position")

    if inductive_capacity <= 0:
        raise ValueError("Inductive capacity must be positive")

    r_hat = r_vec / r_mag
    # F = q1 * q2 / (K * r^2) (CGS-ESU with dielectric)
    force_magnitude = (charge1.q * charge2.q) / (inductive_capacity * r_mag**2)

    return force_magnitude * r_hat


@maxwell_cite(
    41,
    42,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Superposition of electrostatic forces",
)
def force_superposition(
    test_charge: PointCharge,
    source_charges: list[PointCharge],
) -> np.ndarray:
    """
    Calculate resultant force on a test charge from multiple source charges.

    Arts. 41-42: Maxwell states the principle of superposition for
    electrostatic forces. The resultant force on a charged body is the
    vector sum of the forces due to each individual charged body.

    F_resultant = sum_i (q_test * q_i / r_i^2) * r_hat_i

    Args:
        test_charge: The PointCharge on which to calculate the force.
        source_charges: List of PointCharge objects exerting forces.

    Returns:
        Resultant force vector on test_charge (dyne).

    Reference:
        Part I, Arts. 41-42: Superposition of electrostatic forces.

    Note:
        Art. 41: The force from each charge is independent of others.
        Art. 42: Resultant is the vector sum of all individual forces.
    """
    resultant_force = np.zeros(3)

    for source in source_charges:
        r_vec = test_charge.position - source.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            continue  # Skip coincident charges (singularity)

        r_hat = r_vec / r_mag
        # F = q_test * q_source / r^2 (CGS-ESU)
        force_magnitude = (test_charge.q * source.q) / (r_mag**2)
        # Force on test charge is in direction of r_hat if attractive
        # (opposite signs), opposite if repulsive (same signs)
        resultant_force += force_magnitude * r_hat

    return resultant_force


# =============================================================================
# ELEMENTARY THEORY OF ELECTRICITY (Arts. 50-63, 65)
# =============================================================================


class ElectricityType(Enum):
    """Types of electricity according to Maxwell's classification.

    Art. 59: Two kinds of electrification.
    """

    VITREOUS = "vitreous"  # Positive (+)
    RESINOUS = "resinous"  # Negative (-)


class HistoricalTheory(Enum):
    """Historical theories of electricity.

    Arts. 50-55: Competing theories that Maxwell reviews.
    """

    TWO_FLUID = "two_fluid"  # Symmer's theory (Arts. 50-52)
    ONE_FLUID = "one_fluid"  # Franklin's theory (Arts. 53-55)


@maxwell_cite(
    50,
    51,
    52,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Two-fluid theory of electricity (Symmer)",
)
def two_fluid_theory() -> dict:
    """
    Describe the historical two-fluid theory of electricity.

    Arts. 50-52: Maxwell reviews Symmer's two-fluid theory, which posits
    that electricity consists of two distinct fluids:
    - Positive (vitreous) fluid
    - Negative (resinous) fluid

    In this theory:
    - Neutral bodies contain equal amounts of both fluids
    - Electrification occurs when one fluid is in excess
    - The fluids attract each other but repel their own kind

    Maxwell notes this theory explains phenomena but is ultimately
    inadequate for a complete mathematical theory.

    Returns:
        Dictionary describing the two-fluid theory.

    Reference:
        Part I, Arts. 50-52: Two-fluid theory of electricity.

    Note:
        Art. 50: Description of the two-fluid hypothesis.
        Art. 51: Properties attributed to the fluids.
        Art. 52: Limitations of the theory.
    """
    return {
        "name": "Two-Fluid Theory",
        "proponent": "Robert Symmer (1759)",
        "description": (
            "Electricity consists of two distinct, weightless fluids: "
            "vitreous (positive) and resinous (negative)."
        ),
        "properties": {
            "neutral_state": "Equal mixture of both fluids",
            "vitreous_electrification": "Excess of positive fluid",
            "resinous_electrification": "Excess of negative fluid",
            "interaction": "Fluids attract opposites, repel likes",
        },
        "limitations": [
            "No experimental evidence for distinct fluids",
            "Cannot explain all induction phenomena",
            "Superseded by field theory",
        ],
    }


@maxwell_cite(
    53,
    54,
    55,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="One-fluid theory of electricity (Franklin)",
)
def one_fluid_theory() -> dict:
    """
    Describe Franklin's historical one-fluid theory of electricity.

    Arts. 53-55: Maxwell reviews Franklin's one-fluid theory, which posits
    that electricity is a single fluid that permeates all matter:
    - Normal bodies contain a natural quantity of the fluid
    - Positive electrification = excess of fluid
    - Negative electrification = deficiency of fluid

    In this theory:
    - The fluid is self-repulsive but attracted to matter
    - Conservation of the fluid explains charge conservation
    - Matter particles attract the electric fluid

    Maxwell notes this theory anticipated charge conservation but
    lacks the mathematical structure for field theory.

    Returns:
        Dictionary describing the one-fluid theory.

    Reference:
        Part I, Arts. 53-55: Franklin's one-fluid theory.

    Note:
        Art. 53: Description of the one-fluid hypothesis.
        Art. 54: Properties of the electric fluid.
        Art. 55: How the theory explains positive/negative states.
    """
    return {
        "name": "One-Fluid Theory",
        "proponent": "Benjamin Franklin (1747)",
        "description": (
            "Electricity is a single, subtle fluid that permeates all matter. "
            "Positive charge = excess fluid; negative charge = fluid deficiency."
        ),
        "properties": {
            "normal_state": "Natural quantity of fluid",
            "positive_electrification": "Excess of electric fluid",
            "negative_electrification": "Deficiency of electric fluid",
            "fluid_behavior": "Self-repulsive, attracted to matter",
        },
        "successes": [
            "Correctly anticipated charge conservation",
            "Explained Leyden jar phenomena",
            "Introduced positive/negative terminology",
        ],
        "limitations": [
            "No mechanism for fluid-matter interaction",
            "Cannot fully explain two-body attraction",
            "Superseded by field theory",
        ],
    }


@maxwell_cite(
    56,
    57,
    58,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Conservation of electric charge",
)
def charge_conservation(charges: list[PointCharge]) -> tuple[float, bool]:
    """
    Verify the conservation of electric charge.

    Arts. 56-58: Maxwell proves that the total quantity of electricity
    in an isolated system remains constant. This is a fundamental law:
    - In any electrification process, equal and opposite charges are produced
    - The algebraic sum of all charges is invariant
    - Charge cannot be created or destroyed, only transferred

    The total charge Q_total = sum_i(q_i) is conserved.

    Args:
        charges: List of PointCharge objects in the system.

    Returns:
        Tuple of (total_charge, is_conserved):
            - total_charge: Algebraic sum of all charges (esu)
            - is_conserved: True if total is zero (for isolated system)

    Reference:
        Part I, Arts. 56-58: Conservation of electricity.

    Note:
        Art. 56: Experimental basis for conservation.
        Art. 57: Theoretical proof from induction.
        Art. 58: Universal application of the law.
    """
    total_charge = sum(c.q for c in charges)

    # For an isolated system initially neutral, total should be zero
    # Allow small numerical tolerance
    is_conserved = abs(total_charge) < 1e-10

    return total_charge, is_conserved


@maxwell_cite(
    56,
    57,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Charge conservation in isolated system",
)
def verify_isolated_system_conservation(
    initial_charges: list[PointCharge],
    final_charges: list[PointCharge],
) -> bool:
    """
    Verify charge conservation by comparing initial and final states.

    For an isolated system, the total charge before and after any
    electrification process must be identical.

    Args:
        initial_charges: List of PointCharge objects in initial state.
        final_charges: List of PointCharge objects in final state.

    Returns:
        True if total charge is conserved between states.

    Reference:
        Part I, Arts. 56-57: Conservation in electrification processes.
    """
    initial_total = sum(c.q for c in initial_charges)
    final_total = sum(c.q for c in final_charges)

    return abs(initial_total - final_total) < 1e-10


@maxwell_cite(
    59,
    60,
    61,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Types of electrification: vitreous and resinous",
)
def electrification_types(charge_value: float) -> ElectricityType:
    """
    Classify the type of electrification based on charge sign.

    Arts. 59-61: Maxwell distinguishes two kinds of electrification:
    - Vitreous (positive): Produced by rubbing glass with silk
    - Resinous (negative): Produced by rubbing resin with fur

    Bodies with the same type repel; opposite types attract.
    The terms "positive" and "negative" are conventional (Franklin).

    Args:
        charge_value: Charge value in esu (statcoulombs).

    Returns:
        ElectricityType: VITREOUS if positive, RESINOUS if negative.

    Reference:
        Part I, Arts. 59-61: Two kinds of electrification.

    Note:
        Art. 59: Experimental distinction between types.
        Art. 60: Like kinds repel, opposites attract.
        Art. 61: Conventional naming (positive/negative).
    """
    if charge_value >= 0:
        return ElectricityType.VITREOUS
    else:
        return ElectricityType.RESINOUS


@maxwell_cite(
    59,
    60,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Force between different electrification types",
)
def force_between_types(
    type1: ElectricityType,
    type2: ElectricityType,
    magnitude1: float,
    magnitude2: float,
    distance: float,
) -> float:
    """
    Calculate the magnitude of force between two charges based on their types.

    Arts. 59-60: Like electrifications repel, opposite electrifications attract.
    The magnitude follows Coulomb's law.

    Args:
        type1: ElectricityType of first charge.
        type2: ElectricityType of second charge.
        magnitude1: Absolute value of first charge (esu).
        magnitude2: Absolute value of second charge (esu).
        distance: Separation distance (cm).

    Returns:
        Force magnitude with sign (positive = repulsive, negative = attractive).

    Reference:
        Part I, Arts. 59-60: Interaction between electrification types.
    """
    if distance <= 0:
        raise ValueError("Distance must be positive")

    # Determine sign based on types
    if type1 == type2:
        sign = 1.0  # Repulsive
    else:
        sign = -1.0  # Attractive

    # Coulomb's law magnitude (CGS-ESU)
    force_magnitude = (magnitude1 * magnitude2) / (distance**2)

    return sign * force_magnitude


@dataclass
class InductionSystem:
    """System for analyzing electrostatic induction.

    Art. 62-63: Induction of electrification on nearby bodies.

    Attributes:
        inducing_charge: The charge causing induction.
        induced_body_position: Position of the body being polarized.
        induced_body_radius: Effective radius of the induced body (cm).
    """

    inducing_charge: PointCharge
    induced_body_position: np.ndarray
    induced_body_radius: float

    def __post_init__(self):
        self.induced_body_position = np.asarray(
            self.induced_body_position, dtype=np.float64
        )


@maxwell_cite(
    62,
    63,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Electrostatic induction on a nearby body",
)
def charge_induction(
    inducing_charge: PointCharge,
    induced_body_position: np.ndarray,
    induced_body_radius: float,
) -> dict:
    """
    Analyze electrostatic induction on a nearby uncharged body.

    Arts. 62-63: Maxwell describes electrostatic induction, where an
    electrified body causes a redistribution of charge on a nearby
    uncharged body without direct contact:
    - The near side acquires opposite electrification
    - The far side acquires same electrification
    - Net charge of induced body remains zero
    - Induced charges produce an attractive force

    For a conducting sphere of radius a at distance r from charge q:
    - Induced surface charge density varies with position
    - Net effect is attraction toward the inducing charge

    Args:
        inducing_charge: PointCharge causing the induction.
        induced_body_position: Center position of induced body (cm).
        induced_body_radius: Radius of the spherical induced body (cm).

    Returns:
        Dictionary with induction analysis results:
            - induced_dipole: Approximate induced dipole moment
            - attractive_force: Force of attraction (always negative)
            - near_side_charge: Effective charge on near side
            - far_side_charge: Effective charge on far side

    Reference:
        Part I, Arts. 62-63: Induction of electrification.

    Note:
        Art. 62: Description of induction phenomenon.
        Art. 63: Explanation of apparent action at a distance.
    """
    induced_body_position = np.asarray(induced_body_position, dtype=np.float64)

    # Vector from inducing charge to induced body
    r_vec = induced_body_position - inducing_charge.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= induced_body_radius:
        raise ValueError("Induced body must not overlap with inducing charge")

    r_hat = r_vec / r_mag

    # For a conducting sphere, the induced dipole moment is:
    # p = a^3 * E_external (in CGS)
    # where E_external is the field at the sphere center
    E_at_sphere = inducing_charge.field_at(induced_body_position)
    induced_dipole = (induced_body_radius**3) * E_at_sphere

    # The induced charges:
    # Near side: opposite sign to inducing charge
    # Far side: same sign as inducing charge
    # Magnitude depends on geometry and field strength
    induced_charge_magnitude = abs(
        inducing_charge.q * (induced_body_radius / r_mag) ** 2
    )

    # Near side has opposite sign
    near_side_charge = -np.sign(inducing_charge.q) * induced_charge_magnitude
    # Far side has same sign
    far_side_charge = np.sign(inducing_charge.q) * induced_charge_magnitude

    # Net attractive force (dipole in non-uniform field)
    # F = p . grad(E) ~ p * dE/dr
    # For point charge: dE/dr ~ 2q/r^3
    dE_dr = 2 * abs(inducing_charge.q) / (r_mag**3)
    attractive_force = -abs(induced_dipole[0]) * dE_dr  # Always attractive

    return {
        "induced_dipole": induced_dipole,
        "attractive_force": attractive_force,
        "near_side_charge": near_side_charge,
        "far_side_charge": far_side_charge,
        "induced_body_position": induced_body_position,
        "separation": r_mag,
    }


@maxwell_cite(
    62,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Induced charge distribution on conductor",
)
def induced_charge_distribution(
    inducing_charge: PointCharge,
    conductor_position: np.ndarray,
    conductor_radius: float,
    evaluation_angle: float,
) -> float:
    """
    Calculate induced surface charge density at a point on a conductor.

    For a conducting sphere in the field of a point charge, the induced
    surface charge density at angle theta (measured from the line to
    the inducing charge) is:

        sigma_induced(theta) = -(q / 4*pi*a^2) * (a/r)^2 * (3*cos(theta))

    where a is sphere radius, r is distance to inducing charge.

    Args:
        inducing_charge: PointCharge causing induction.
        conductor_position: Center of conducting sphere (cm).
        conductor_radius: Radius of sphere (cm).
        evaluation_angle: Angle theta from line to inducing charge (radians).

    Returns:
        Induced surface charge density (esu/cm^2).

    Reference:
        Part I, Art. 62: Distribution of induced charge.
    """
    conductor_position = np.asarray(conductor_position, dtype=np.float64)

    r_vec = conductor_position - inducing_charge.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= conductor_radius:
        raise ValueError("Evaluation point must be outside conductor")

    # Simplified model: sigma ~ cos(theta) distribution
    # Maximum induced charge on the side facing the inducing charge
    cos_theta = np.cos(evaluation_angle)
    sigma_max = -inducing_charge.q / (4 * np.pi * conductor_radius**2)
    sigma_induced = sigma_max * (conductor_radius / r_mag) ** 2 * 3 * cos_theta

    return sigma_induced


@maxwell_cite(
    65,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Field concept: action at a distance vs medium",
)
def field_concept() -> dict:
    """
    Explain Maxwell's field concept and its relation to action at a distance.

    Art. 65: Maxwell concludes the elementary theory by contrasting two
    views of electric action:

    1. Action at a Distance (Newtonian view):
       - Charges act directly on each other across empty space
       - No intermediate mechanism required
       - Force depends only on positions and magnitudes

    2. Action through a Medium (Faraday/Maxwell view):
       - Electric effects are transmitted through a medium
       - The medium is in a state of stress (the field)
       - Forces arise from tensions and pressures in the field
       - The field has physical reality independent of charges

    Maxwell adopts the field view as the foundation for his theory:
    - The electric field exists at all points in space
    - Field lines represent the direction of force
    - Field intensity represents force per unit charge
    - Energy is stored in the field itself

    Returns:
        Dictionary comparing the two views and stating Maxwell's position.

    Reference:
        Part I, Art. 65: Field concept and the nature of electric action.

    Note:
        This article marks Maxwell's transition from elementary theory
        to his mathematical field theory developed in subsequent chapters.
    """
    return {
        "action_at_distance": {
            "description": (
                "Charges act directly on each other across empty space "
                "without any intermediate mechanism."
            ),
            "proponents": ["Newton", "Coulomb", "Ampère"],
            "characteristics": [
                "Instantaneous action",
                "No medium required",
                "Force depends on position only",
                "Mathematical description via potential",
            ],
            "limitations": [
                "No physical mechanism for force transmission",
                "Cannot explain finite propagation speed",
                "Incompatible with field energy storage",
            ],
        },
        "action_through_medium": {
            "description": (
                "Electric effects are transmitted through a medium "
                "which is in a state of electric stress (the field)."
            ),
            "proponents": ["Faraday", "Maxwell"],
            "characteristics": [
                "Field exists at all points in space",
                "Medium is in state of tension/pressure",
                "Forces arise from field stresses",
                "Energy stored in the field itself",
                "Finite propagation speed (wave theory)",
            ],
            "mathematical_formulation": [
                "Electric field E = force per unit charge",
                "Field lines show direction of force",
                "Potential satisfies Poisson/Laplace equation",
                "Energy density = E^2 / 8*pi (CGS)",
            ],
        },
        "maxwell_position": (
            "Maxwell adopts the field (medium) view as fundamental. "
            "The electric field is a real physical entity that: "
            "(1) exists independently of test charges, "
            "(2) stores and transports energy, "
            "(3) propagates at finite speed (speed of light), "
            "(4) obeys local differential equations. "
            "This view leads directly to electromagnetic wave theory."
        ),
    }


@maxwell_cite(
    65,
    part=1,
    chapter="Elementary Theory",
    theory_class="maxwell_original",
    description="Electric field as physical reality",
)
def field_reality_statement() -> str:
    """
    State Maxwell's position on the physical reality of the electric field.

    Art. 65: Maxwell's declaration that the electric field is not merely
    a mathematical construct but a physical reality with independent
    existence and energy content.

    Returns:
        Statement of field reality according to Maxwell.

    Reference:
        Part I, Art. 65: The electric field as physical entity.
    """
    return (
        "The electric field is a real physical state of the medium, "
        "not merely a mathematical abstraction. It stores energy, "
        "transmits forces, and can propagate as waves. The field exists "
        "at every point in space and has independent reality whether or "
        "not a test charge is present to measure it. This field concept "
        "is the foundation of electromagnetic theory."
    )


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


@maxwell_cite(
    30,
    31,
    34,
    part=1,
    chapter="Electrification",
    theory_class="standard_math",
    description="Coulomb force between two point charges",
)
def coulomb_force(
    charge1: PointCharge,
    charge2: PointCharge,
    inductive_capacity: float = 1.0,
) -> np.ndarray:
    """
    Calculate the complete Coulomb force between two point charges.

    This is a convenience function that combines attraction and repulsion
    into a single force law. Uses CGS-ESU units.

    F = (q1 * q2) / (K * r^2) * r_hat

    Args:
        charge1: First PointCharge object.
        charge2: Second PointCharge object.
        inductive_capacity: Specific inductive capacity K of medium.

    Returns:
        Force vector on charge2 due to charge1 (dyne).
        Positive (repulsive) for like charges, negative (attractive) for opposite.

    Reference:
        Part I, Arts. 30-31, 34-35: Coulomb's law.
    """
    return force_medium(charge1, charge2, inductive_capacity)


@maxwell_cite(
    41,
    42,
    part=1,
    chapter="Electrification",
    theory_class="standard_math",
    description="Electric field from multiple charges via superposition",
)
def field_from_charges(
    source_charges: list[PointCharge],
    evaluation_point: np.ndarray,
) -> ElectricField:
    """
    Calculate the electric field at a point from multiple source charges.

    Uses the superposition principle: the total field is the vector sum
    of fields from individual charges.

    Args:
        source_charges: List of PointCharge objects.
        evaluation_point: Position where field is calculated (cm).

    Returns:
        ElectricField at the evaluation point.

    Reference:
        Part I, Arts. 41-42: Superposition principle.
    """
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)

    total_field = np.zeros(3)
    for charge in source_charges:
        total_field += charge.field_at(evaluation_point)

    return ElectricField(value=total_field, position=evaluation_point)


@maxwell_cite(
    56,
    57,
    58,
    part=1,
    chapter="Elementary Theory",
    theory_class="standard_math",
    description="Check charge conservation for a system",
)
def check_charge_conservation(
    charges: list[PointCharge],
    expected_total: float = 0.0,
    tolerance: float = 1e-10,
) -> tuple[bool, float]:
    """
    Verify charge conservation with a specified expected total.

    Args:
        charges: List of PointCharge objects.
        expected_total: Expected total charge (default 0 for isolated neutral system).
        tolerance: Numerical tolerance for comparison.

    Returns:
        Tuple of (is_conserved, actual_total).

    Reference:
        Part I, Arts. 56-58: Conservation of charge.
    """
    actual_total = sum(c.q for c in charges)
    is_conserved = abs(actual_total - expected_total) < tolerance
    return is_conserved, actual_total
