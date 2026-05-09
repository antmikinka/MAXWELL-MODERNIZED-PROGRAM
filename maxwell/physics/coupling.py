"""
Dipole coupling — force and torque between magnetic dipoles.

Implements the theory of dipole interaction from Part III of Maxwell's Treatise:
- Force between two magnetic dipoles (Art. 387)
- Torque and mutual action (Art. 388)
- Special cases: aligned, perpendicular, collinear configurations

Maxwell derives the complete force and torque laws for interacting
magnetic dipoles, showing how orientation affects the interaction.

Category: A (maxwell_original) — Maxwell's theory of dipole coupling.

References:
    Part III, Arts. 387-388: Dipole interaction theory.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.magnet import Magnet
from maxwell.core.moment import MagneticMoment
from maxwell.meta.citation import maxwell_cite


@dataclass
class DipoleInteraction:
    """
    Complete description of dipole-dipole interaction.

    Art. 387-388: Two magnetic dipoles exert both force and torque
    on each other. The interaction depends on:
    - The magnitudes of both moments
    - The distance between dipoles
    - The relative orientations of moments and separation vector

    Attributes:
        force: Force vector on dipole 2 due to dipole 1 (dyne).
        torque: Torque vector on dipole 2 (dyne·cm).
        potential_energy: Interaction energy (erg).
        separation: Separation distance (cm).
    """

    force: np.ndarray  # shape (3,)
    torque: np.ndarray  # shape (3,)
    potential_energy: float
    separation: float

    def __post_init__(self):
        self.force = np.asarray(self.force, dtype=np.float64)
        self.torque = np.asarray(self.torque, dtype=np.float64)

        if self.force.shape != (3,):
            raise ValueError(f"Force must be 3D")
        if self.torque.shape != (3,):
            raise ValueError(f"Torque must be 3D")


@maxwell_cite(
    387,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Complete dipole-dipole force and torque",
)
def calc_dipole_interaction(
    moment1: np.ndarray,
    moment2: np.ndarray,
    separation: np.ndarray,
) -> DipoleInteraction:
    """
    Calculate complete force and torque between two magnetic dipoles.

    Art. 387: The force between two magnetic dipoles depends on their
    relative orientation. Unlike point charges, dipoles experience
    both translational force and rotational torque.

    For dipole 1 at origin with moment m1, and dipole 2 at position r
    with moment m2:

    Field from dipole 1:
        H₁(r) = (3(m₁·r̂)r̂ - m₁) / r³

    Force on dipole 2:
        F₂ = ∇(m₂ · H₁)

    Torque on dipole 2:
        τ₂ = m₂ × H₁

    Potential energy:
        W = -m₂ · H₁ = (m₁·m₂)/r³ - 3(m₁·r)(m₂·r)/r⁵

    Args:
        moment1: Magnetic moment of dipole 1 (emu).
        moment2: Magnetic moment of dipole 2 (emu).
        separation: Vector from dipole 1 to dipole 2 (cm).

    Returns:
        DipoleInteraction object with force, torque, and energy.

    Reference:
        Part III, Art. 387: Dipole force and torque.

    Note:
        The force formula assumes dipole 1 is fixed and computes
        the force on dipole 2. By Newton's third law, the force
        on dipole 1 is equal and opposite.
    """
    moment1 = np.asarray(moment1, dtype=np.float64)
    moment2 = np.asarray(moment2, dtype=np.float64)
    separation = np.asarray(separation, dtype=np.float64)

    r_mag = np.linalg.norm(separation)
    if r_mag == 0:
        return DipoleInteraction(
            force=np.zeros(3),
            torque=np.zeros(3),
            potential_energy=0.0,
            separation=0.0,
        )

    r_hat = separation / r_mag

    # Field from dipole 1 at position of dipole 2
    m1_dot_r = np.dot(moment1, r_hat)
    H1 = (3 * m1_dot_r * r_hat - moment1) / (r_mag**3)

    # Torque on dipole 2: τ = m2 × H1
    torque = np.cross(moment2, H1)

    # Potential energy: W = -m2 · H1
    energy = -float(np.dot(moment2, H1))

    # Force on dipole 2: F = ∇(m2 · H1)
    # Using the gradient of the dipole field:
    # F = (3/r⁴) * [(m1·m2)r̂ + (m1·r̂)m2 + (m2·r̂)m1 - 5(m1·r̂)(m2·r̂)r̂]

    m2_dot_r = np.dot(moment2, r_hat)
    m1_dot_m2 = np.dot(moment1, moment2)

    force = (3 / (r_mag**4)) * (
        m1_dot_m2 * r_hat
        + m1_dot_r * moment2
        + m2_dot_r * moment1
        - 5 * m1_dot_r * m2_dot_r * r_hat
    )

    return DipoleInteraction(
        force=force,
        torque=torque,
        potential_energy=energy,
        separation=float(r_mag),
    )


@maxwell_cite(
    387,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Force between dipoles from field gradient",
)
def dipole_force_from_gradient(
    moment1: np.ndarray,
    moment2: np.ndarray,
    separation: np.ndarray,
) -> np.ndarray:
    """
    Calculate force on dipole 2 from gradient of dipole 1's field.

    Art. 387: The force on a dipole in a non-uniform field is given by
    the gradient of the potential energy:

        F = ∇(m · H)

    This function computes the force using the analytical gradient
    of the dipole field.

    Args:
        moment1: Magnetic moment of dipole 1 (source).
        moment2: Magnetic moment of dipole 2 (experiencing force).
        separation: Vector from dipole 1 to dipole 2.

    Returns:
        Force vector on dipole 2 (dyne).

    Reference:
        Part III, Art. 387: Dipole force derivation.
    """
    # Delegate to the complete interaction formula
    interaction = calc_dipole_interaction(moment1, moment2, separation)
    return interaction.force


@maxwell_cite(
    387,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Potential energy of dipole pair",
)
def dipole_potential_energy(
    moment1: np.ndarray,
    moment2: np.ndarray,
    separation: np.ndarray,
) -> float:
    """
    Calculate potential energy of two interacting dipoles.

    Art. 387: The mutual potential energy of two dipoles is the work
    required to bring them from infinite separation to their current
    configuration.

    W = (m₁·m₂)/r³ - 3(m₁·r)(m₂·r)/r⁵
      = [m₁·m₂ - 3(m₁·r̂)(m₂·r̂)] / r³

    The energy is minimum when dipoles are aligned head-to-tail
    along the separation vector.

    Args:
        moment1: Magnetic moment of dipole 1 (emu).
        moment2: Magnetic moment of dipole 2 (emu).
        separation: Vector from dipole 1 to dipole 2 (cm).

    Returns:
        Potential energy (erg). Negative = attractive configuration.

    Reference:
        Part III, Art. 387: Dipole potential energy.
    """
    moment1 = np.asarray(moment1, dtype=np.float64)
    moment2 = np.asarray(moment2, dtype=np.float64)
    separation = np.asarray(separation, dtype=np.float64)

    r_mag = np.linalg.norm(separation)
    if r_mag == 0:
        return 0.0

    r_hat = separation / r_mag

    m1_dot_m2 = np.dot(moment1, moment2)
    m1_dot_r = np.dot(moment1, r_hat)
    m2_dot_r = np.dot(moment2, r_hat)

    return (m1_dot_m2 - 3 * m1_dot_r * m2_dot_r) / (r_mag**3)


@maxwell_cite(
    388,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Torque on dipole in field of another dipole",
)
def dipole_torque(
    moment1: np.ndarray,
    moment2: np.ndarray,
    separation: np.ndarray,
) -> np.ndarray:
    """
    Calculate torque on dipole 2 due to dipole 1's field.

    Art. 388: A dipole in an external magnetic field experiences a
    torque tending to align it with the field:

        τ = m × H

    For dipole 2 in the field of dipole 1, this torque tends to
    rotate dipole 2 into an equilibrium orientation.

    Args:
        moment1: Magnetic moment of dipole 1 (field source).
        moment2: Magnetic moment of dipole 2 (experiencing torque).
        separation: Vector from dipole 1 to dipole 2.

    Returns:
        Torque vector on dipole 2 (dyne·cm).

    Reference:
        Part III, Art. 388: Dipole torque.
    """
    moment1 = np.asarray(moment1, dtype=np.float64)
    moment2 = np.asarray(moment2, dtype=np.float64)
    separation = np.asarray(separation, dtype=np.float64)

    r_mag = np.linalg.norm(separation)
    if r_mag == 0:
        return np.zeros(3)

    r_hat = separation / r_mag

    # Field from dipole 1
    m1_dot_r = np.dot(moment1, r_hat)
    H1 = (3 * m1_dot_r * r_hat - moment1) / (r_mag**3)

    # Torque = m2 × H1
    return np.cross(moment2, H1)


@maxwell_cite(
    387,
    388,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Special dipole configurations: aligned, perpendicular, collinear",
)
def special_dipole_cases(
    moment1_mag: float,
    moment2_mag: float,
    separation: float,
    configuration: str,
) -> dict[str, float]:
    """
    Calculate force and torque for special dipole configurations.

    Art. 387-388: Maxwell analyzes several important special cases:

    1. Collinear (both moments along separation vector):
       - Maximum attractive/repulsive force
       - Zero torque (moments already aligned with field)

    2. Parallel (moments parallel, perpendicular to separation):
       - Repulsive force
       - Non-zero torque tending to rotate moments

    3. Perpendicular (one moment perpendicular to other):
       - Complex force pattern
       - Maximum torque in certain orientations

    4. Anti-parallel (moments opposite):
       - Attractive force
       - Unstable equilibrium

    Args:
        moment1_mag: Magnitude of moment 1 (emu).
        moment2_mag: Magnitude of moment 2 (emu).
        separation: Distance between dipoles (cm).
        configuration: One of 'collinear', 'parallel', 'perpendicular',
                      'anti_parallel', 'broadside'.

    Returns:
        Dictionary with force magnitude, torque magnitude, and energy.

    Reference:
        Part III, Arts. 387-388: Special dipole cases.
    """
    if separation <= 0:
        raise ValueError("Separation must be positive")

    # Define unit vectors
    r_hat = np.array([1.0, 0.0, 0.0])  # Separation along x-axis

    if configuration == "collinear":
        # Both moments along separation (x-axis)
        m1 = moment1_mag * r_hat
        m2 = moment2_mag * r_hat

    elif configuration == "parallel":
        # Both moments parallel (y-axis), perpendicular to separation
        m1 = moment1_mag * np.array([0.0, 1.0, 0.0])
        m2 = moment2_mag * np.array([0.0, 1.0, 0.0])

    elif configuration == "perpendicular":
        # m1 along separation, m2 perpendicular
        m1 = moment1_mag * r_hat
        m2 = moment2_mag * np.array([0.0, 1.0, 0.0])

    elif configuration == "anti_parallel":
        # Moments opposite to each other, both along separation
        m1 = moment1_mag * r_hat
        m2 = -moment2_mag * r_hat

    elif configuration == "broadside":
        # Side-by-side, moments perpendicular to line joining them
        m1 = moment1_mag * np.array([0.0, 1.0, 0.0])
        m2 = moment2_mag * np.array([0.0, 1.0, 0.0])
        # Use different separation direction for this case
        r_hat = np.array([1.0, 0.0, 0.0])

    else:
        raise ValueError(f"Unknown configuration '{configuration}'")

    # Compute interaction
    sep_vec = separation * r_hat
    interaction = calc_dipole_interaction(m1, m2, sep_vec)

    # Determine force direction (attractive vs repulsive)
    # Negative force_x = attractive (pulling toward dipole 1)
    force_along_r = float(np.dot(interaction.force, r_hat))
    is_attractive = force_along_r < 0

    return {
        "force_magnitude": float(np.linalg.norm(interaction.force)),
        "force_along_separation": force_along_r,
        "is_attractive": is_attractive,
        "torque_magnitude": float(np.linalg.norm(interaction.torque)),
        "torque_on_dipole_2": float(np.linalg.norm(interaction.torque)),
        "potential_energy": interaction.potential_energy,
        "configuration": configuration,
    }


@maxwell_cite(
    387,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Equilibrium orientations for dipole pair",
)
def dipole_equilibrium_orientations(
    moment1: np.ndarray,
    separation: np.ndarray,
) -> list[dict[str, np.ndarray | float]]:
    """
    Find equilibrium orientations for dipole 2 in dipole 1's field.

    Art. 387: A dipole in an external field has equilibrium orientations
    where the torque is zero. These occur when the dipole is aligned
    or anti-aligned with the local field direction.

    Stable equilibrium: m parallel to H (minimum energy)
    Unstable equilibrium: m anti-parallel to H (maximum energy)

    Args:
        moment1: Fixed magnetic moment of dipole 1 (emu).
        separation: Vector from dipole 1 to dipole 2 (cm).

    Returns:
        List of equilibrium configurations, each with:
        - orientation: Unit vector for m2 direction
        - energy: Potential energy at this orientation
        - is_stable: True if stable equilibrium

    Reference:
        Part III, Art. 387: Dipole equilibrium.
    """
    moment1 = np.asarray(moment1, dtype=np.float64)
    separation = np.asarray(separation, dtype=np.float64)

    r_mag = np.linalg.norm(separation)
    if r_mag == 0:
        return []

    r_hat = separation / r_mag

    # Field direction from dipole 1
    m1_dot_r = np.dot(moment1, r_hat)
    H1 = (3 * m1_dot_r * r_hat - moment1) / (r_mag**3)

    H1_mag = np.linalg.norm(H1)
    if H1_mag == 0:
        # Degenerate case: zero field (e.g., at equatorial plane)
        return []

    # Unit vector along field
    H1_hat = H1 / H1_mag

    # Stable equilibrium: m2 parallel to H1 (minimum energy)
    # Energy = -|m2| * |H1| when aligned
    stable_energy = -H1_mag  # Per unit moment

    # Unstable equilibrium: m2 anti-parallel to H1 (maximum energy)
    # Energy = +|m2| * |H1| when anti-aligned
    unstable_energy = H1_mag

    return [
        {
            "orientation": H1_hat.copy(),
            "energy": stable_energy,
            "is_stable": True,
            "description": "Aligned with field (stable)",
        },
        {
            "orientation": -H1_hat.copy(),
            "energy": unstable_energy,
            "is_stable": False,
            "description": "Anti-aligned with field (unstable)",
        },
    ]


@maxwell_cite(
    387,
    388,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Angular dependence of dipole interaction",
)
def angular_dependence(
    moment1_mag: float,
    moment2_mag: float,
    separation: float,
    theta1: float,
    theta2: float,
    phi: float,
) -> dict[str, float]:
    """
    Calculate interaction as function of angular orientation.

    Art. 387-388: The dipole interaction depends on the angles:
    - θ₁: angle between m1 and separation vector r
    - θ₂: angle between m2 and separation vector r
    - φ: azimuthal angle difference between m1 and m2 projections

    The potential energy can be written:
    W = (m₁m₂/r³) * [cos(θ₁₂) - 3cos(θ₁)cos(θ₂)]

    where θ₁₂ is the angle between the two moments.

    Args:
        moment1_mag: Magnitude of m1 (emu).
        moment2_mag: Magnitude of m2 (emu).
        separation: Distance (cm).
        theta1: Angle of m1 from r axis (radians).
        theta2: Angle of m2 from r axis (radians).
        phi: Azimuthal angle difference (radians).

    Returns:
        Dictionary with energy, force magnitude, and torque.

    Reference:
        Part III, Arts. 387-388: Angular dependence.
    """
    if separation <= 0:
        raise ValueError("Separation must be positive")

    # Construct moment vectors in spherical coordinates
    # r is along x-axis
    # m1 in x-y plane at angle theta1 from x
    m1_x = moment1_mag * np.cos(theta1)
    m1_y = moment1_mag * np.sin(theta1)
    m1_z = 0.0
    m1 = np.array([m1_x, m1_y, m1_z])

    # m2 at angle theta2 from x, rotated by phi around x
    m2_x = moment2_mag * np.cos(theta2)
    m2_perp = moment2_mag * np.sin(theta2)
    m2_y = m2_perp * np.cos(phi)
    m2_z = m2_perp * np.sin(phi)
    m2 = np.array([m2_x, m2_y, m2_z])

    # Separation along x-axis
    sep_vec = np.array([separation, 0.0, 0.0])

    # Compute interaction
    interaction = calc_dipole_interaction(m1, m2, sep_vec)

    return {
        "potential_energy": interaction.potential_energy,
        "force_magnitude": float(np.linalg.norm(interaction.force)),
        "torque_magnitude": float(np.linalg.norm(interaction.torque)),
        "m1_direction": (theta1, 0.0),
        "m2_direction": (theta2, phi),
    }


@maxwell_cite(
    387,
    388,
    part=3,
    chapter="Dipole Interaction",
    theory_class="maxwell_original",
    description="Force between two magnet objects",
)
def magnet_to_magnet_force(
    magnet1: Magnet,
    magnet2: Magnet,
) -> DipoleInteraction:
    """
    Calculate complete interaction between two magnet objects.

    Art. 387-388: For two finite magnets at distances large compared
    to their sizes, we can treat them as point dipoles located at
    their centers.

    This function computes the force and torque between two magnets
    using the dipole approximation.

    Args:
        magnet1: First magnet (source of field).
        magnet2: Second magnet (experiencing force/torque).

    Returns:
        DipoleInteraction object with complete interaction data.

    Reference:
        Part III, Arts. 387-388: Magnet-magnet interaction.

    Note:
        For nearby magnets, use the exact pole-to-pole calculation
        instead of the dipole approximation.
    """
    # Get centers and moments
    center1 = (magnet1.north_pole.position + magnet1.south_pole.position) / 2
    center2 = (magnet2.north_pole.position + magnet2.south_pole.position) / 2

    separation = center2 - center1
    m1 = magnet1.magnetic_moment
    m2 = magnet2.magnetic_moment

    return calc_dipole_interaction(m1, m2, separation)
