"""
Magnetic potential — scalar and vector potentials for magnetic fields.

Implements the theory of magnetic potential from Part III of Maxwell's Treatise:
- Potential of an infinitesimal magnetic element (Art. 385)
- Potential of a finite magnet (Art. 386)
- Two formulations of finite magnet potential

Maxwell develops the scalar potential Ω where H = -∇Ω, analogous to
electric potential. For a magnetic dipole: Ω = (m·r) / r³

Category: A (maxwell_original) — Maxwell's theory of magnetic potential.

References:
    Part III, Arts. 385-386: Magnetic potential theory.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.magnet import Magnet, MagneticPole
from maxwell.core.moment import MagneticMoment, MagneticParticle
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticPotential:
    """
    Magnetic scalar potential — potential function for magnetic field.

    Art. 385-386: The magnetic scalar potential Ω is defined such that
    the magnetic field H is the negative gradient of Ω:
        H = -∇Ω

    For a magnetic pole of strength m at distance r:
        Ω = m / r

    For a magnetic dipole with moment m:
        Ω = (m·r) / r³ = (m·r̂) / r²

    Attributes:
        value: Potential value Ω (gauss·cm).
        position: Position where potential is evaluated (cm).
    """

    value: float
    position: np.ndarray  # shape (3,)

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got {self.position.shape}")


@maxwell_cite(
    385,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Potential from infinitesimal magnetic element",
)
def calc_element_potential(
    magnetic_moment: np.ndarray,
    element_position: np.ndarray,
    field_point: np.ndarray,
) -> float:
    """
    Calculate magnetic scalar potential from an infinitesimal magnetic element.

    Art. 385: The potential of a magnetic element (infinitesimal dipole)
    at a point is proportional to the projection of the moment on the
    line joining the element to the point, divided by the square of
    the distance.

    For a dipole with moment m at position r₀, the potential at r is:
        Ω(r) = (m · (r - r₀)) / |r - r₀|³
             = (m · r̂) / r²  (where r̂ is unit vector from element to point)

    Args:
        magnetic_moment: Magnetic moment vector of element (emu).
        element_position: Position of the magnetic element (cm).
        field_point: Position where potential is calculated (cm).

    Returns:
        Magnetic scalar potential Ω (gauss·cm).

    Reference:
        Part III, Art. 385: Potential of magnetic element.

    Note:
        This is the fundamental building block for computing potentials
        of extended magnets by integration.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    element_position = np.asarray(element_position, dtype=np.float64)
    field_point = np.asarray(field_point, dtype=np.float64)

    # Vector from element to field point
    r_vec = field_point - element_position
    r_mag = np.linalg.norm(r_vec)

    if r_mag == 0:
        return 0.0  # Singularity at the element itself

    # Ω = (m · r) / r³
    return float(np.dot(magnetic_moment, r_vec) / (r_mag**3))


@maxwell_cite(
    385,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Field from infinitesimal magnetic element via potential",
)
def calc_element_field(
    magnetic_moment: np.ndarray,
    element_position: np.ndarray,
    field_point: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate magnetic field from infinitesimal element using potential gradient.

    Art. 385: The magnetic field is the negative gradient of the potential:
        H = -∇Ω

    This function computes the field numerically by evaluating the
    potential gradient using finite differences.

    Args:
        magnetic_moment: Magnetic moment vector of element (emu).
        element_position: Position of the magnetic element (cm).
        field_point: Position where field is calculated (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Magnetic field vector H (gauss).

    Reference:
        Part III, Art. 385: Field from magnetic element.
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    element_position = np.asarray(element_position, dtype=np.float64)
    field_point = np.asarray(field_point, dtype=np.float64)

    def potential_at(point: np.ndarray) -> float:
        return calc_element_potential(magnetic_moment, element_position, point)

    # Numerical gradient using central differences
    grad = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        Omega_plus = potential_at(field_point + delta)
        Omega_minus = potential_at(field_point - delta)
        grad[i] = (Omega_plus - Omega_minus) / (2 * h)

    # H = -∇Ω
    return -grad


@maxwell_cite(
    386,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Potential of finite magnet via volume integration",
)
def calc_finite_potential(
    magnet: Magnet,
    field_point: np.ndarray,
    method: str = "dipole",
) -> float:
    """
    Calculate magnetic scalar potential of a finite magnet.

    Art. 386: The potential of a finite magnet can be computed by
    integrating the contributions from all magnetic elements within it.

    Two equivalent formulations:

    1. Dipole formulation (volume integral):
       Ω = ∫ (M(r') · (r - r')) / |r - r'|³ dV'

    2. Pole formulation (surface integral):
       Ω = ∫ σ(r') / |r - r'| dS'

    where M is magnetization and σ is surface pole density.

    Args:
        magnet: Magnet object with defined poles.
        field_point: Position where potential is calculated (cm).
        method: 'dipole' for dipole approximation, 'poles' for exact pole sum.

    Returns:
        Magnetic scalar potential Ω (gauss·cm).

    Reference:
        Part III, Art. 386: Potential of finite magnet.

    Note:
        For distances large compared to magnet size, the dipole
        approximation is accurate. Near the magnet, the pole
        formulation gives exact results.
    """
    field_point = np.asarray(field_point, dtype=np.float64)

    if method == "poles":
        # Exact potential from two poles
        # Ω = m_N / r_N + m_S / r_S

        r_N_vec = field_point - magnet.north_pole.position
        r_S_vec = field_point - magnet.south_pole.position

        r_N_mag = np.linalg.norm(r_N_vec)
        r_S_mag = np.linalg.norm(r_S_vec)

        if r_N_mag == 0 and r_S_mag == 0:
            return 0.0

        omega = 0.0
        if r_N_mag > 0:
            omega += magnet.north_pole.signed_strength / r_N_mag
        if r_S_mag > 0:
            omega += magnet.south_pole.signed_strength / r_S_mag

        return float(omega)

    elif method == "dipole":
        # Dipole approximation (valid for r >> magnet size)
        # Ω = (m · r̂) / r²

        center = (magnet.north_pole.position + magnet.south_pole.position) / 2
        r_vec = field_point - center
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return 0.0

        m = magnet.magnetic_moment
        return float(np.dot(m, r_vec) / (r_mag**3))

    else:
        raise ValueError(f"Unknown method '{method}'. Use 'dipole' or 'poles'.")


@maxwell_cite(
    386,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Field of finite magnet via potential gradient",
)
def calc_finite_field(
    magnet: Magnet,
    field_point: np.ndarray,
    method: str = "dipole",
) -> np.ndarray:
    """
    Calculate magnetic field of a finite magnet.

    Art. 386: The field is obtained from the potential by H = -∇Ω.

    For a dipole (far field approximation):
        H(r) = (3(m·r̂)r̂ - m) / r³

    For exact calculation (near field), sum contributions from both poles:
        H = m_N * (r - r_N) / |r - r_N|³ + m_S * (r - r_S) / |r - r_S|³

    Args:
        magnet: Magnet object.
        field_point: Position where field is calculated (cm).
        method: 'dipole' for dipole approximation, 'poles' for exact.

    Returns:
        Magnetic field vector H (gauss).

    Reference:
        Part III, Art. 386: Field of finite magnet.
    """
    field_point = np.asarray(field_point, dtype=np.float64)

    if method == "poles":
        # Exact field from two poles
        H = np.zeros(3)

        for pole in [magnet.north_pole, magnet.south_pole]:
            r_vec = field_point - pole.position
            r_mag = np.linalg.norm(r_vec)

            if r_mag > 0:
                # H = m * r̂ / r² = m * r / r³
                H += pole.signed_strength * r_vec / (r_mag**3)

        return H

    elif method == "dipole":
        # Dipole field (far-field approximation)
        center = (magnet.north_pole.position + magnet.south_pole.position) / 2
        r_vec = field_point - center
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return np.zeros(3)

        m = magnet.magnetic_moment
        r_hat = r_vec / r_mag

        # H = (3(m·r̂)r̂ - m) / r³
        m_dot_r = np.dot(m, r_hat)
        H = (3 * m_dot_r * r_hat - m) / (r_mag**3)

        return H

    else:
        raise ValueError(f"Unknown method '{method}'. Use 'dipole' or 'poles'.")


@maxwell_cite(
    386,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Alternative proof of finite magnet potential via integration",
)
def finite_potential_by_integration(
    magnetization: np.ndarray,
    volume: float,
    center: np.ndarray,
    field_point: np.ndarray,
    num_elements: int = 100,
) -> float:
    """
    Calculate potential by numerical volume integration.

    Art. 386: The potential of a magnetized body can be computed by
    integrating over its volume:

        Ω(r) = ∫_V (M(r') · (r - r')) / |r - r'|³ dV'

    This function performs numerical integration by dividing the
    magnetized volume into small elements.

    Args:
        magnetization: Uniform magnetization vector M (emu/cm³).
        volume: Total volume of magnetized body (cm³).
        center: Center of magnetized body (cm).
        field_point: Position where potential is calculated (cm).
        num_elements: Number of volume elements for integration.

    Returns:
        Magnetic scalar potential Ω (gauss·cm).

    Reference:
        Part III, Art. 386: Integration method for potential.

    Note:
        This is a simplified numerical integration assuming uniform
        magnetization. For exact results, use analytical formulas.
    """
    magnetization = np.asarray(magnetization, dtype=np.float64)
    center = np.asarray(center, dtype=np.float64)
    field_point = np.asarray(field_point, dtype=np.float64)

    if volume <= 0:
        return 0.0

    # Volume per element
    dV = volume / num_elements

    # Simple model: distribute elements along magnetization direction
    # This approximates a uniformly magnetized bar
    moment_per_element = magnetization * dV

    omega = 0.0
    for i in range(num_elements):
        # Distribute elements along a line through center
        # Simplified 1D distribution
        t = (i + 0.5) / num_elements - 0.5  # Range: -0.5 to 0.5
        element_pos = center + t * magnetization * 0.1  # Scale for numerical stability

        # Add contribution from this element
        r_vec = field_point - element_pos
        r_mag = np.linalg.norm(r_vec)

        if r_mag > 0:
            omega += float(np.dot(moment_per_element, r_vec) / (r_mag**3))

    return omega


@maxwell_cite(
    385,
    386,
    part=3,
    chapter="Magnetic Potential",
    theory_class="maxwell_original",
    description="Compare two formulations of finite magnet potential",
)
def compare_potential_formulations(
    magnet: Magnet,
    field_point: np.ndarray,
) -> dict[str, float]:
    """
    Compare the two formulations of finite magnet potential.

    Art. 386: Maxwell presents two equivalent formulations:
    1. Integration over magnetic elements (dipole formulation)
    2. Sum over magnetic poles (pole formulation)

    This function computes both and compares them, demonstrating
    their equivalence and range of validity.

    Args:
        magnet: Magnet object.
        field_point: Position where potential is evaluated (cm).

    Returns:
        Dictionary with:
        - pole_formulation: Result from pole sum method
        - dipole_formulation: Result from dipole approximation
        - relative_difference: |Ω_pole - Ω_dipole| / |Ω_pole|
        - distance_from_center: Distance from magnet center (cm)
        - is_far_field: True if distance >> magnet size

    Reference:
        Part III, Art. 386: Two formulations of potential.
    """
    field_point = np.asarray(field_point, dtype=np.float64)

    # Pole formulation (exact)
    omega_pole = calc_finite_potential(magnet, field_point, method="poles")

    # Dipole formulation (approximation)
    omega_dipole = calc_finite_potential(magnet, field_point, method="dipole")

    # Distance from center
    center = (magnet.north_pole.position + magnet.south_pole.position) / 2
    distance = float(np.linalg.norm(field_point - center))

    # Relative difference
    if abs(omega_pole) > 1e-15:
        rel_diff = abs(omega_pole - omega_dipole) / abs(omega_pole)
    else:
        rel_diff = abs(omega_pole - omega_dipole)

    # Far field criterion: distance > 10x magnet size
    is_far_field = distance > 10 * magnet.magnetic_length

    return {
        "pole_formulation": omega_pole,
        "dipole_formulation": omega_dipole,
        "relative_difference": rel_diff,
        "distance_from_center": distance,
        "magnet_length": magnet.magnetic_length,
        "is_far_field": is_far_field,
    }
