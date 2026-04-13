"""
Maxwell's Part I, Chapter I: Description of Phenomena (Arts. 12-19).

This module implements the phenomenological basis of electrostatics as described
by Maxwell in the opening chapter of Part I:

- Electrification by friction (Arts. 12-14): Rubbing produces electrification
- Electrification by induction (Arts. 15-16): Electrification by influence
- Electrification by contact (Art. 17): Direct contact charging
- Electric scintillation (Art. 18): Electric discharge phenomena
- Electric sparks (Art. 19): Properties of electric sparks
- Classification of electrical phenomena (Arts. 12-19)

Category: A (maxwell_original) — Maxwell's description of electrical phenomena.

References:
    Part I, Chapter I, Arts. 12-19: Description of electrical phenomena.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.core.charge import PointCharge
from maxwell.core.field import ElectricField


# =============================================================================
# ENUMERATIONS AND DATA CLASSES
# =============================================================================


class ElectrificationType(Enum):
    """Types of electrification according to Maxwell's classification.

    Arts. 12-14: Vitreous and resinous electrification.
    """
    VITREOUS = "vitreous"  # Positive (+) - from glass rubbed with silk
    RESINOUS = "resinous"  # Negative (-) - from resin rubbed with fur


class PhenomenonClass(Enum):
    """Classification of electrical phenomena.

    Arts. 12-19: Maxwell's classification scheme.
    """
    FRICTION = "friction"  # Electrification by rubbing
    INDUCTION = "induction"  # Electrification by influence
    CONTACT = "contact"  # Direct contact charging
    DISCHARGE = "discharge"  # Electric scintillation
    SPARK = "spark"  # Electric spark phenomena


@dataclass
class FrictionPair:
    """Pair of materials for electrification by friction.

    Arts. 12-14: When two materials are rubbed together, one becomes
    vitreously electrified and the other resinously electrified.

    Attributes:
        material1: First material in the friction pair.
        material2: Second material in the friction pair.
        material1_type: Type of electrification acquired by material1.
        material2_type: Type of electrification acquired by material2.
    """
    material1: str
    material2: str
    material1_type: ElectrificationType
    material2_type: ElectrificationType


@dataclass
class DischargePhenomenon:
    """Description of an electric discharge phenomenon.

    Art. 18: Electric scintillation and discharge effects.

    Attributes:
        phenomenon_type: Type of discharge phenomenon.
        description: Description of the phenomenon.
        conditions: Conditions required for the discharge.
    """
    phenomenon_type: str
    description: str
    conditions: dict


@dataclass
class SparkProperties:
    """Properties of an electric spark.

    Art. 19: Maxwell's description of electric spark characteristics.

    Attributes:
        length: Spark length (cm).
        potential_difference: Potential difference required (statvolt).
        breakdown_field: Electric field at breakdown (statvolt/cm).
        duration: Approximate duration (seconds).
    """
    length: float
    potential_difference: float
    breakdown_field: float
    duration: float


# =============================================================================
# ELECTRIFICATION BY FRICTION (Arts. 12-14)
# =============================================================================


@maxwell_cite(
    12, 13, 14,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Electrification by friction — rubbing produces electrification",
)
def electrification_by_friction(
    material1: str,
    material2: str,
    friction_work: float,
    efficiency: float = 0.1,
) -> dict:
    """
    Calculate electrification produced by friction between two materials.

    Arts. 12-14: Maxwell describes the phenomenon of electrification by friction,
    where rubbing two materials together produces equal and opposite charges
    on the two materials. The classic examples are:
    - Glass rubbed with silk: glass becomes vitreous (+), silk becomes resinous (-)
    - Resin rubbed with fur: resin becomes resinous (-), fur becomes vitreous (+)

    The quantity of electrification produced depends on:
    - The materials involved (their positions in the triboelectric series)
    - The work done in friction
    - The efficiency of charge transfer

    The charges produced are always equal in magnitude and opposite in sign,
    in accordance with the conservation of electricity.

    Args:
        material1: Name of the first material.
        material2: Name of the second material.
        friction_work: Mechanical work done in friction (ergs).
        efficiency: Efficiency of charge transfer (default 0.1, dimensionless).

    Returns:
        Dictionary with electrification results:
            - material1_charge: Charge on material1 (esu)
            - material2_charge: Charge on material2 (esu, opposite sign)
            - material1_type: Type of electrification (vitreous/resinous)
            - material2_type: Type of electrification
            - friction_pair: The FrictionPair object

    Reference:
        Part I, Arts. 12-14: Electrification by friction.

    Note:
        Art. 12: Description of electrification by rubbing.
        Art. 13: Vitreous and resinous electrification.
        Art. 14: Equal and opposite charges are produced.
    """
    # Triboelectric series (simplified) - positive materials tend to become +
    # when rubbed with materials lower in the series
    triboelectric_series = {
        "glass": 1.0,
        "silk": 0.5,
        "fur": -0.3,
        "resin": -0.8,
        "ebonite": -0.9,
        "amber": -0.7,
        "wool": 0.2,
        "cotton": 0.0,
        "paper": -0.1,
        "rubber": -0.6,
    }

    # Get material positions (default to 0 if unknown)
    pos1 = triboelectric_series.get(material1.lower(), 0.0)
    pos2 = triboelectric_series.get(material2.lower(), 0.0)

    # Determine electrification types
    if pos1 > pos2:
        type1 = ElectrificationType.VITREOUS
        type2 = ElectrificationType.RESINOUS
        sign1 = 1.0
    else:
        type1 = ElectrificationType.RESINOUS
        type2 = ElectrificationType.VITREOUS
        sign1 = -1.0

    # Calculate charge magnitude from work
    # Empirical relation: charge ~ sqrt(work) * efficiency
    # In CGS: 1 erg = 1 dyne*cm, charge in esu
    charge_magnitude = efficiency * np.sqrt(friction_work * 1e-8)

    charge1 = sign1 * charge_magnitude
    charge2 = -charge1  # Equal and opposite

    friction_pair = FrictionPair(
        material1=material1,
        material2=material2,
        material1_type=type1,
        material2_type=type2,
    )

    return {
        "material1_charge": charge1,
        "material2_charge": charge2,
        "material1_type": type1,
        "material2_type": type2,
        "friction_pair": friction_pair,
        "work_expended": friction_work,
        "transfer_efficiency": efficiency,
    }


@maxwell_cite(
    12, 13,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Vitreous electrification from glass and silk",
)
def vitreous_electrification_glass_silk(
    friction_work: float,
) -> dict:
    """
    Calculate vitreous electrification of glass rubbed with silk.

    Arts. 12-13: The classic example of vitreous (positive) electrification
    is glass rubbed with silk. The glass acquires a positive charge while
    the silk acquires an equal negative (resinous) charge.

    Args:
        friction_work: Mechanical work done in rubbing (ergs).

    Returns:
        Dictionary with:
            - glass_charge: Positive charge on glass (esu)
            - silk_charge: Negative charge on silk (esu)
            - electrification_type: "vitreous" for glass

    Reference:
        Part I, Arts. 12-13: Vitreous electrification example.
    """
    result = electrification_by_friction("glass", "silk", friction_work)
    return {
        "glass_charge": result["material1_charge"],
        "silk_charge": result["material2_charge"],
        "electrification_type": result["material1_type"].value,
        "friction_pair": result["friction_pair"],
    }


@maxwell_cite(
    13, 14,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Resinous electrification from resin and fur",
)
def resinous_electrification_resin_fur(
    friction_work: float,
) -> dict:
    """
    Calculate resinous electrification of resin rubbed with fur.

    Arts. 13-14: The classic example of resinous (negative) electrification
    is resin (or sealing wax) rubbed with fur. The resin acquires a negative
    charge while the fur acquires an equal positive (vitreous) charge.

    Args:
        friction_work: Mechanical work done in rubbing (ergs).

    Returns:
        Dictionary with:
            - resin_charge: Negative charge on resin (esu)
            - fur_charge: Positive charge on fur (esu)
            - electrification_type: "resinous" for resin

    Reference:
        Part I, Arts. 13-14: Resinous electrification example.
    """
    result = electrification_by_friction("resin", "fur", friction_work)
    return {
        "resin_charge": result["material1_charge"],
        "fur_charge": result["material2_charge"],
        "electrification_type": result["material1_type"].value,
        "friction_pair": result["friction_pair"],
    }


@maxwell_cite(
    14,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Conservation of charge in friction electrification",
)
def verify_friction_conservation(
    material1_charge: float,
    material2_charge: float,
    tolerance: float = 1e-10,
) -> bool:
    """
    Verify that friction produces equal and opposite charges.

    Art. 14: Maxwell proves that when two bodies are electrified by friction,
    the quantities of the two electrifications are exactly equal. This is an
    early statement of charge conservation.

    Args:
        material1_charge: Charge on first material (esu).
        material2_charge: Charge on second material (esu).
        tolerance: Numerical tolerance for comparison.

    Returns:
        True if charges are equal and opposite within tolerance.

    Reference:
        Part I, Art. 14: Equality of opposite electrifications.
    """
    return abs(material1_charge + material2_charge) < tolerance


# =============================================================================
# ELECTRIFICATION BY INDUCTION (Arts. 15-16)
# =============================================================================


@maxwell_cite(
    15, 16,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Electrification by induction — influence without contact",
)
def electrification_by_induction(
    inducing_charge: PointCharge,
    conductor_position: np.ndarray,
    conductor_radius: float,
    grounding: bool = False,
) -> dict:
    """
    Calculate electrification produced by electrostatic induction.

    Arts. 15-16: Maxwell describes electrification by induction (also called
    electrification by influence), where an electrified body causes a
    redistribution of charge on a nearby conductor without direct contact:

    1. The inducing charge creates an electric field
    2. The field polarizes the conductor:
       - Near side: opposite charge is induced
       - Far side: same charge is induced
    3. If the conductor is grounded while influenced:
       - The far-side charge flows to ground
       - The near-side charge remains bound
    4. When the ground is removed, the conductor retains
       a net charge opposite to the inducing charge

    For a conducting sphere of radius a at distance r from charge q:
    - Induced surface charge density: sigma ~ cos(theta)
    - Total induced charge (if grounded): q_induced = -q * (a/r)

    Args:
        inducing_charge: PointCharge causing the induction.
        conductor_position: Center position of conducting sphere (cm).
        conductor_radius: Radius of the sphere (cm).
        grounding: Whether the conductor is grounded during induction.

    Returns:
        Dictionary with induction results:
            - induced_dipole: Induced dipole moment (esu*cm)
            - near_side_charge: Charge on near side (esu)
            - far_side_charge: Charge on far side (esu)
            - net_charge: Net charge on conductor (esu)
            - bound_charge: Charge that remains bound (esu)
            - free_charge: Charge that can flow to ground (esu)

    Reference:
        Part I, Arts. 15-16: Electrification by induction.

    Note:
        Art. 15: Description of induction phenomenon.
        Art. 16: Distribution of induced electrification.
    """
    conductor_position = np.asarray(conductor_position, dtype=np.float64)

    # Vector from inducing charge to conductor center
    r_vec = conductor_position - inducing_charge.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= conductor_radius:
        raise ValueError("Conductor must not overlap with inducing charge")

    r_hat = r_vec / r_mag

    # Electric field at conductor center due to inducing charge
    E_center = inducing_charge.field_at(conductor_position)

    # Induced dipole moment for conducting sphere
    # p = a^3 * E (in CGS)
    induced_dipole = (conductor_radius ** 3) * E_center

    # Induced charges on near and far sides
    # Magnitude from method of images approximation
    induced_charge_magnitude = abs(inducing_charge.q) * (conductor_radius / r_mag)

    # Near side has opposite sign to inducing charge
    near_side_charge = -np.sign(inducing_charge.q) * induced_charge_magnitude
    # Far side has same sign as inducing charge
    far_side_charge = np.sign(inducing_charge.q) * induced_charge_magnitude

    if grounding:
        # Far side charge flows to ground, leaving only bound near-side charge
        net_charge = near_side_charge
        bound_charge = near_side_charge
        free_charge = far_side_charge  # This flows away
    else:
        # Net charge is zero (equal amounts on both sides)
        net_charge = 0.0
        bound_charge = near_side_charge  # "Bound" by attraction
        free_charge = 0.0

    return {
        "induced_dipole": induced_dipole,
        "near_side_charge": near_side_charge,
        "far_side_charge": far_side_charge,
        "net_charge": net_charge,
        "bound_charge": bound_charge,
        "free_charge": free_charge,
        "conductor_position": conductor_position,
        "separation": r_mag,
        "grounding": grounding,
    }


@maxwell_cite(
    15,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Induced charge distribution on conductor surface",
)
def induced_surface_distribution(
    inducing_charge: PointCharge,
    conductor_position: np.ndarray,
    conductor_radius: float,
    evaluation_angle: float,
) -> float:
    """
    Calculate induced surface charge density at a specific point.

    Art. 15: The induced electrification is distributed over the surface
    of the conductor. The surface charge density varies with position,
    being strongest on the side facing the inducing charge.

    For a conducting sphere, the induced surface charge density at angle
    theta (measured from the line to the inducing charge) is approximately:

        sigma(theta) = -3 * (q / 4*pi*a^2) * (a/r) * cos(theta)

    where a is sphere radius, r is distance to inducing charge.

    Args:
        inducing_charge: PointCharge causing induction.
        conductor_position: Center of conducting sphere (cm).
        conductor_radius: Radius of sphere (cm).
        evaluation_angle: Angle theta from line to inducing charge (radians).

    Returns:
        Induced surface charge density (esu/cm^2).

    Reference:
        Part I, Art. 15: Distribution of induced charge.
    """
    conductor_position = np.asarray(conductor_position, dtype=np.float64)

    r_vec = conductor_position - inducing_charge.position
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= conductor_radius:
        raise ValueError("Evaluation point must be outside inducing charge")

    # Maximum induced charge density (at theta = 0, facing the charge)
    sigma_max = -3 * inducing_charge.q / (4 * np.pi * conductor_radius ** 2)
    sigma_max *= (conductor_radius / r_mag)

    # Cosine variation
    cos_theta = np.cos(evaluation_angle)

    return sigma_max * cos_theta


# =============================================================================
# ELECTRIFICATION BY CONTACT (Art. 17)
# =============================================================================


@maxwell_cite(
    17,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Electrification by direct contact",
)
def electrification_by_contact(
    charged_body: dict,
    neutral_body: dict,
    contact_time: float,
    contact_resistance: float = 1e-6,
) -> dict:
    """
    Calculate charge transfer by direct contact.

    Art. 17: Maxwell describes electrification by contact, where a charged
    body transfers charge to a neutral body when they are brought into
    direct contact. The charge redistributes between the two bodies
    according to their capacities.

    For two conducting spheres of radii a1 and a2:
    - Initial: q1 = Q (charged), q2 = 0 (neutral)
    - After contact: q1' = Q * a1/(a1+a2), q2' = Q * a2/(a1+a2)
    - The charges distribute proportional to the capacities (radii)

    The contact process is governed by:
    1. The potential equalizes between the bodies
    2. Charge flows until V1 = V2
    3. The rate depends on contact resistance

    Args:
        charged_body: Dictionary with keys:
            - charge: Initial charge (esu)
            - radius: Radius (cm)
            - position: Position array (cm)
        neutral_body: Dictionary with same keys (charge should be 0).
        contact_time: Duration of contact (seconds).
        contact_resistance: Contact resistance (statohm, default 1e-6).

    Returns:
        Dictionary with contact electrification results:
            - charged_body_final: Final charge on first body (esu)
            - neutral_body_final: Final charge on second body (esu)
            - charge_transferred: Amount of charge transferred (esu)
            - final_potential: Common potential after contact (statvolt)

    Reference:
        Part I, Art. 17: Electrification by contact.
    """
    q1_initial = charged_body.get("charge", 0.0)
    a1 = charged_body.get("radius", 1.0)

    q2_initial = neutral_body.get("charge", 0.0)
    a2 = neutral_body.get("radius", 1.0)

    total_charge = q1_initial + q2_initial

    # For conductors in contact, charge distributes proportional to capacity
    # For spheres, capacity C = a (in CGS)
    # Final charges: q1' = Q_total * C1/(C1+C2) = Q_total * a1/(a1+a2)
    total_capacity = a1 + a2

    q1_final = total_charge * (a1 / total_capacity)
    q2_final = total_charge * (a2 / total_capacity)

    # Final common potential: V = q/C
    final_potential = q1_final / a1  # Same as q2_final / a2

    charge_transferred = q2_final - q2_initial

    return {
        "charged_body_final": q1_final,
        "neutral_body_final": q2_final,
        "charge_transferred": charge_transferred,
        "final_potential": final_potential,
        "contact_time": contact_time,
        "initial_charged": q1_initial,
        "initial_neutral": q2_initial,
    }


@maxwell_cite(
    17,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Charge sharing between equal conductors",
)
def charge_sharing_equal_spheres(
    initial_charge: float,
    sphere_radius: float,
) -> dict:
    """
    Calculate charge sharing between two identical conducting spheres.

    Art. 17: When a charged conductor touches an identical uncharged
    conductor, the charge divides equally between them. This is a
    special case of contact electrification.

    Args:
        initial_charge: Initial charge on first sphere (esu).
        sphere_radius: Radius of both spheres (cm).

    Returns:
        Dictionary with:
            - sphere1_charge: Final charge on first sphere (esu)
            - sphere2_charge: Final charge on second sphere (esu)
            - fraction_transferred: Fraction of charge transferred (0.5)

    Reference:
        Part I, Art. 17: Equal division of charge.
    """
    final_charge = initial_charge / 2.0
    final_potential = final_charge / sphere_radius

    return {
        "sphere1_charge": final_charge,
        "sphere2_charge": final_charge,
        "fraction_transferred": 0.5,
        "final_potential": final_potential,
        "sphere_radius": sphere_radius,
    }


# =============================================================================
# ELECTRIC SCINTILLATION (Art. 18)
# =============================================================================


@maxwell_cite(
    18,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Electric scintillation — discharge phenomena",
)
def electric_scintillation(
    potential: float,
    gap_distance: float,
    air_pressure: float = 1.0,
    electrode_shape: str = "sphere",
) -> DischargePhenomenon:
    """
    Describe electric scintillation (discharge) phenomena.

    Art. 18: Maxwell describes electric scintillation, the luminous
    discharge that occurs when the electric field in a gas exceeds
    the breakdown threshold. This includes:
    - Corona discharge (brush discharge) at sharp points
    - Spark discharge across gaps
    - Glow discharge at lower pressures

    The breakdown field depends on:
    - Gas pressure (Paschen's law)
    - Electrode geometry
    - Gap distance

    For air at standard pressure:
    - Breakdown field ~ 30 kV/cm = 100 statvolt/cm
    - Sharp points enhance the local field

    Args:
        potential: Applied potential difference (statvolt).
        gap_distance: Distance between electrodes (cm).
        air_pressure: Air pressure in atmospheres (default 1.0).
        electrode_shape: Shape of electrodes ("sphere", "point", "plane").

    Returns:
        DischargePhenomenon object describing the discharge.

    Reference:
        Part I, Art. 18: Electric scintillation.
    """
    # Calculate average field
    avg_field = potential / gap_distance if gap_distance > 0 else float("inf")

    # Breakdown field for air (approximate, in statvolt/cm)
    # 30 kV/cm = 100 statvolt/cm at 1 atm
    breakdown_field_atm = 100.0
    breakdown_field = breakdown_field_atm * air_pressure

    # Field enhancement factor for electrode shape
    enhancement_factors = {
        "sphere": 1.0,
        "plane": 1.0,
        "point": 10.0,  # Sharp points greatly enhance field
    }
    enhancement = enhancement_factors.get(electrode_shape, 1.0)

    # Effective field at electrode surface
    effective_field = avg_field * enhancement

    # Determine discharge type
    if effective_field < breakdown_field * 0.5:
        discharge_type = "none"
        description = "No discharge — field below threshold"
    elif effective_field < breakdown_field:
        discharge_type = "corona"
        description = "Corona discharge — luminous glow at sharp points"
    elif effective_field < breakdown_field * 2:
        discharge_type = "spark"
        description = "Spark discharge — sudden luminous breakdown"
    else:
        discharge_type = "arc"
        description = "Arc discharge — continuous conductive channel"

    conditions = {
        "potential": potential,
        "gap_distance": gap_distance,
        "air_pressure": air_pressure,
        "electrode_shape": electrode_shape,
        "average_field": avg_field,
        "breakdown_field": breakdown_field,
        "enhancement_factor": enhancement,
        "effective_field": effective_field,
    }

    return DischargePhenomenon(
        phenomenon_type=discharge_type,
        description=description,
        conditions=conditions,
    )


@maxwell_cite(
    18,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Corona discharge at sharp points",
)
def corona_discharge_at_point(
    potential: float,
    point_radius: float,
    ground_distance: float,
) -> dict:
    """
    Calculate corona discharge from a sharp point.

    Art. 18: Maxwell notes that electrified bodies with sharp points
    exhibit a luminous discharge (corona or brush discharge) at lower
    potentials than blunt bodies. The field is concentrated at the point.

    For a point of radius r at potential V:
        E_surface ~ V / r

    When E_surface exceeds the breakdown field (~100 statvolt/cm for air),
    corona discharge begins.

    Args:
        potential: Potential of the pointed conductor (statvolt).
        point_radius: Radius of curvature of the point (cm).
        ground_distance: Distance to ground plane (cm).

    Returns:
        Dictionary with corona discharge characteristics.

    Reference:
        Part I, Art. 18: Corona at sharp points.
    """
    if point_radius <= 0:
        raise ValueError("Point radius must be positive")

    # Field at surface of point (approximation)
    E_surface = potential / point_radius

    # Breakdown field for air
    breakdown_field = 100.0  # statvolt/cm

    # Corona onset ratio
    corona_ratio = E_surface / breakdown_field

    # Discharge characteristics
    if corona_ratio < 1.0:
        active = False
        discharge_current = 0.0
        luminosity = "none"
    else:
        active = True
        # Approximate corona current (empirical)
        discharge_current = 1e-6 * (corona_ratio - 1.0) * potential
        if corona_ratio < 1.5:
            luminosity = "faint blue glow"
        elif corona_ratio < 2.0:
            luminosity = "bright brush discharge"
        else:
            luminosity = "intense streamers"

    return {
        "corona_active": active,
        "surface_field": E_surface,
        "breakdown_field": breakdown_field,
        "corona_ratio": corona_ratio,
        "discharge_current": discharge_current,
        "luminosity": luminosity,
        "point_radius": point_radius,
        "potential": potential,
    }


# =============================================================================
# ELECTRIC SPARKS (Art. 19)
# =============================================================================


@maxwell_cite(
    19,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Properties of electric sparks",
)
def electric_spark_properties(
    spark_length: float,
    gap_pressure: float = 1.0,
    electrode_material: str = "brass",
) -> SparkProperties:
    """
    Calculate properties of an electric spark.

    Art. 19: Maxwell describes the properties of electric sparks:
    - The potential required to produce a spark of given length
    - The dependence on air pressure
    - The effect of electrode shape and material
    - The duration and characteristics of the discharge

    For a spark in air at standard pressure:
    - Breakdown voltage ~ 30 kV/cm = 100 statvolt/cm
    - Spark duration ~ microseconds
    - Temperature ~ thousands of degrees

    The spark follows a tortuous path determined by:
    - Ionization of air molecules
    - Local field enhancements
    - Statistical fluctuations

    Args:
        spark_length: Length of the spark gap (cm).
        gap_pressure: Air pressure in atmospheres (default 1.0).
        electrode_material: Material of electrodes (for reference).

    Returns:
        SparkProperties object with spark characteristics.

    Reference:
        Part I, Art. 19: Properties of electric sparks.
    """
    # Breakdown field (Paschen's law approximation for air)
    # At 1 atm: ~30 kV/cm = 100 statvolt/cm
    breakdown_field_atm = 100.0  # statvolt/cm

    # Pressure scaling (linear approximation near 1 atm)
    breakdown_field = breakdown_field_atm * gap_pressure

    # Potential required
    potential_difference = breakdown_field * spark_length

    # Spark duration (empirical, typically microseconds)
    duration = 1e-6 * spark_length  # ~1 microsecond per cm

    return SparkProperties(
        length=spark_length,
        potential_difference=potential_difference,
        breakdown_field=breakdown_field,
        duration=duration,
    )


@maxwell_cite(
    19,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Spark gap breakdown potential",
)
def spark_gap_breakdown(
    gap_distance: float,
    pressure: float = 1.0,
    temperature: float = 293.0,
) -> dict:
    """
    Calculate breakdown potential for a spark gap.

    Art. 19: The potential required to produce a spark depends on:
    - Gap distance (longer gaps require higher voltage)
    - Air pressure (Paschen's law)
    - Temperature (affects air density)

    Paschen's Law (simplified for air):
        V_breakdown = B * p * d / (ln(A * p * d) - ln(ln(1 + 1/gamma)))

    For practical purposes near standard conditions:
        V_breakdown ~ 30 kV/cm * (p/p0) * d

    Args:
        gap_distance: Spark gap distance (cm).
        pressure: Air pressure (atmospheres).
        temperature: Temperature (Kelvin, default 293K = 20C).

    Returns:
        Dictionary with breakdown characteristics.

    Reference:
        Part I, Art. 19: Spark gap breakdown.
    """
    # Constants for air (CGS units)
    # A ~ 15 /cm/torr, B ~ 365 V/cm/torr (in SI)
    # Converting to CGS and atm

    # Simplified linear approximation
    breakdown_field = 100.0 * pressure  # statvolt/cm/atm

    # Temperature correction (density scaling)
    # Higher temperature = lower density = lower breakdown
    temp_correction = 293.0 / temperature if temperature > 0 else 1.0
    breakdown_field *= temp_correction

    breakdown_potential = breakdown_field * gap_distance

    # Paschen minimum (for reference)
    # Occurs at p*d ~ 0.75 torr*cm for air
    paschen_minimum_v = 327.0  # volts ~ 1.09 statvolt
    paschen_minimum_pd = 0.75 / 760  # atm*cm (0.75 torr*cm)

    return {
        "breakdown_potential": breakdown_potential,
        "breakdown_field": breakdown_field,
        "gap_distance": gap_distance,
        "pressure": pressure,
        "temperature": temperature,
        "temp_correction": temp_correction,
        "paschen_minimum_v": paschen_minimum_v / 300,  # Convert to statvolt
        "paschen_minimum_pd": paschen_minimum_pd,
    }


# =============================================================================
# PHENOMENA CLASSIFICATION (Arts. 12-19)
# =============================================================================


@maxwell_cite(
    12, 13, 14, 15, 16, 17, 18, 19,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Classification of electrical phenomena",
)
def phenomena_classifier(
    observation: dict,
) -> dict:
    """
    Classify an electrical phenomenon based on observations.

    Arts. 12-19: Maxwell classifies electrical phenomena into distinct
    categories based on their causes and characteristics:

    1. FRICTION (Arts. 12-14): Electrification by rubbing materials
       - Two materials in contact and separated
       - Equal and opposite charges produced
       - Examples: glass/silk, resin/fur

    2. INDUCTION (Arts. 15-16): Electrification by influence
       - Charged body near neutral conductor
       - Charge redistribution without contact
       - Can produce permanent charge with grounding

    3. CONTACT (Art. 17): Direct charge transfer
       - Charged body touches neutral body
       - Charge shares according to capacity
       - Equal conductors share equally

    4. DISCHARGE (Art. 18): Electric scintillation
       - Luminous effects in gases
       - Corona, brush, spark discharge
       - Depends on field and pressure

    5. SPARK (Art. 19): Sudden breakdown
       - Rapid discharge across gap
       - Potential exceeds breakdown threshold
       - Characteristic spark length and duration

    Args:
        observation: Dictionary with observation details:
            - materials: List of materials involved (if any)
            - contact: Whether contact occurred (bool)
            - rubbing: Whether rubbing occurred (bool)
            - nearby_charge: Whether a charged body is nearby (bool)
            - luminous_effect: Whether light is observed (bool)
            - gap_discharge: Whether discharge across gap (bool)
            - charge_transfer: Measured charge transfer (esu)

    Returns:
        Dictionary with classification:
            - primary_class: Main phenomenon class
            - secondary_class: Secondary class (if applicable)
            - confidence: Classification confidence (0-1)
            - explanation: Description of classification reasoning

    Reference:
        Part I, Arts. 12-19: Classification of phenomena.
    """
    materials = observation.get("materials", [])
    contact = observation.get("contact", False)
    rubbing = observation.get("rubbing", False)
    nearby_charge = observation.get("nearby_charge", False)
    luminous_effect = observation.get("luminous_effect", False)
    gap_discharge = observation.get("gap_discharge", False)
    charge_transfer = observation.get("charge_transfer", 0.0)

    classification = {
        "primary_class": None,
        "secondary_class": None,
        "confidence": 0.0,
        "explanation": "",
        "articles": [],
    }

    # Rule-based classification (following Maxwell's descriptions)

    # Friction: rubbing of materials
    if rubbing and len(materials) >= 2:
        classification["primary_class"] = PhenomenonClass.FRICTION
        classification["confidence"] = 0.95
        classification["explanation"] = (
            "Rubbing of materials indicates electrification by friction. "
            "Equal and opposite charges should be produced on the materials."
        )
        classification["articles"] = [12, 13, 14]

    # Discharge: luminous effects
    elif luminous_effect and gap_discharge:
        classification["primary_class"] = PhenomenonClass.SPARK
        classification["confidence"] = 0.9
        classification["explanation"] = (
            "Luminous discharge across gap indicates spark phenomenon. "
            "The potential exceeded the breakdown threshold of the medium."
        )
        classification["articles"] = [19]

    # Corona: luminous without gap discharge
    elif luminous_effect and not gap_discharge:
        classification["primary_class"] = PhenomenonClass.DISCHARGE
        classification["confidence"] = 0.85
        classification["explanation"] = (
            "Luminous effect without gap discharge suggests corona "
            "or brush discharge, typically at sharp points."
        )
        classification["articles"] = [18]

    # Induction: nearby charge without contact
    elif nearby_charge and not contact:
        classification["primary_class"] = PhenomenonClass.INDUCTION
        classification["confidence"] = 0.9
        classification["explanation"] = (
            "Presence of nearby charge without contact indicates "
            "electrification by induction (influence)."
        )
        classification["articles"] = [15, 16]

    # Contact: direct contact with charge transfer
    elif contact and abs(charge_transfer) > 1e-10:
        classification["primary_class"] = PhenomenonClass.CONTACT
        classification["confidence"] = 0.95
        classification["explanation"] = (
            "Direct contact with charge transfer indicates "
            "electrification by contact."
        )
        classification["articles"] = [17]

    # Unknown
    else:
        classification["primary_class"] = None
        classification["confidence"] = 0.0
        classification["explanation"] = (
            "Insufficient observations to classify the phenomenon. "
            "Please provide more details about the experimental setup."
        )
        classification["articles"] = []

    return classification


@maxwell_cite(
    12, 13, 14, 15, 16, 17, 18, 19,
    part=1, chapter="Description of Phenomena",
    theory_class="maxwell_original",
    description="Complete phenomenological description",
)
def complete_phenomenology() -> dict:
    """
    Provide a complete description of Maxwell's electrical phenomena.

    Arts. 12-19: This function summarizes all the electrical phenomena
    described in Chapter I of Part I, providing a reference for the
    foundational observations upon which Maxwell builds his theory.

    Returns:
        Complete dictionary describing all phenomena classes.

    Reference:
        Part I, Chapter I, Arts. 12-19: Complete phenomenology.
    """
    return {
        "friction": {
            "articles": [12, 13, 14],
            "description": "Electrification by rubbing materials together",
            "key_principle": "Equal and opposite charges produced",
            "examples": [
                "Glass + silk: glass vitreous (+), silk resinous (-)",
                "Resin + fur: resin resinous (-), fur vitreous (+)",
            ],
            "conservation": "Total charge always zero",
        },
        "induction": {
            "articles": [15, 16],
            "description": "Electrification by influence without contact",
            "key_principle": "Charge redistribution in external field",
            "stages": [
                "External field polarizes conductor",
                "Near side: opposite charge induced",
                "Far side: same charge induced",
                "Grounding removes far-side charge",
                "Result: permanent opposite charge",
            ],
        },
        "contact": {
            "articles": [17],
            "description": "Charge transfer by direct contact",
            "key_principle": "Charge shares proportional to capacity",
            "special_case": "Equal conductors share charge equally",
        },
        "scintillation": {
            "articles": [18],
            "description": "Luminous discharge in gases",
            "types": [
                "Corona: faint glow at sharp points",
                "Brush: streamer-like discharge",
                "Spark: sudden breakdown across gap",
            ],
            "depends_on": ["Field strength", "Gas pressure", "Electrode shape"],
        },
        "spark": {
            "articles": [19],
            "description": "Sudden electrical breakdown",
            "properties": {
                "breakdown_field": "~100 statvolt/cm (air, 1 atm)",
                "potential": "V = E_breakdown * gap_length",
                "duration": "Microseconds",
            },
            "paschen_law": "Breakdown depends on pressure * distance",
        },
    }
