"""
Magnetic force — magnetic field intensity H and force calculations.

Implements the theory of magnetic force from Part III of Maxwell's Treatise:
- Magnetic force defined as H = -∇Ω (Art. 395)
- Force in cylindrical cavity — H field measurement (Art. 396)
- Force in general magnetized matter (Art. 397)
- Force in elongated cylinder/needle cavity (Art. 398)

Maxwell distinguishes between two magnetic fields:
- H (magnetic force): Measured in a long narrow cavity parallel to magnetization
- B (magnetic induction): Measured in a flat disk cavity perpendicular to magnetization

In CGS: B = H + 4πI, where I is magnetization.

Category: A (maxwell_original) — Maxwell's theory of magnetic force.

References:
    Part III, Arts. 395-398: Magnetic force and field definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.moment import MagnetizationVector
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticForce:
    """
    Magnetic force field — the H field vector at a point.

    Art. 395: The magnetic force H at a point is the negative gradient
    of the magnetic scalar potential Ω:

        H = -∇Ω

    This is the field that would be measured inside a long narrow
    cavity oriented parallel to the magnetization direction.

    Attributes:
        value: H field vector (H_x, H_y, H_z) in gauss.
        position: Position where field is evaluated (cm).
    """

    value: np.ndarray  # shape (3,), gauss
    position: np.ndarray  # shape (3,), cm

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.value.shape != (3,):
            raise ValueError(f"H field must be 3D, got {self.value.shape}")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got {self.position.shape}")

    @property
    def magnitude(self) -> float:
        """Magnitude of H field |H|."""
        return float(np.linalg.norm(self.value))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in direction of H field."""
        mag = self.magnitude
        if mag == 0:
            return np.zeros(3)
        return self.value / mag

    @classmethod
    @maxwell_cite(
        395,
        part=3,
        chapter="Magnetic Force",
        theory_class="maxwell_original",
        description="Create H field from potential gradient",
    )
    def from_potential(
        cls,
        potential_func: Callable[[np.ndarray], float],
        position: np.ndarray,
        h: float = 1e-8,
    ) -> MagneticForce:
        """
        Create magnetic force from scalar potential.

        Art. 395: The magnetic force is the negative gradient of
        the magnetic scalar potential:

            H = -∇Ω

        This function computes H numerically using finite differences.

        Args:
            potential_func: Function returning Ω at a position.
            position: Position where H is calculated (cm).
            h: Step size for numerical differentiation (cm).

        Returns:
            MagneticForce object (H field).

        Reference:
            Part III, Art. 395: H from potential.
        """
        position = np.asarray(position, dtype=np.float64)

        # Numerical gradient using central differences
        grad = np.zeros(3)
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            Omega_plus = potential_func(position + delta)
            Omega_minus = potential_func(position - delta)
            grad[i] = (Omega_plus - Omega_minus) / (2 * h)

        # H = -∇Ω
        return cls(value=-grad, position=position)

    @classmethod
    @maxwell_cite(
        395,
        part=3,
        chapter="Magnetic Force",
        theory_class="maxwell_original",
        description="Create H field from force on unit pole",
    )
    def from_force_on_unit_pole(
        cls,
        force_on_pole: np.ndarray,
        pole_strength: float,
        position: np.ndarray,
    ) -> MagneticForce:
        """
        Create magnetic force from force on a test pole.

        Art. 395: The magnetic force H at a point is defined as the
        force experienced by a unit north pole placed at that point:

            H = F / m

        Args:
            force_on_pole: Force on test pole (dyne).
            pole_strength: Strength of test pole (emu).
            position: Position of test pole (cm).

        Returns:
            MagneticForce object (H field in gauss).

        Reference:
            Part III, Art. 395: H defined via force on pole.
        """
        if pole_strength == 0:
            raise ValueError("Pole strength cannot be zero")

        position = np.asarray(position, dtype=np.float64)
        H = np.asarray(force_on_pole, dtype=np.float64) / pole_strength

        return cls(value=H, position=position)


@maxwell_cite(
    395,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="Magnetic force from scalar potential",
)
def magnetic_force_from_potential(
    potential_func: Callable[[np.ndarray], float],
    position: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate magnetic force H from scalar potential.

    Art. 395: The magnetic force is the negative gradient of the
    magnetic scalar potential:

        H = -∇Ω

    In components:
        H_x = -∂Ω/∂x, H_y = -∂Ω/∂y, H_z = -∂Ω/∂z

    Args:
        potential_func: Function returning Ω at a position.
        position: Position where H is calculated (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Magnetic force vector H (gauss).

    Reference:
        Part III, Art. 395: H = -∇Ω.
    """
    position = np.asarray(position, dtype=np.float64)

    # Numerical gradient
    grad = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        Omega_plus = potential_func(position + delta)
        Omega_minus = potential_func(position - delta)
        grad[i] = (Omega_plus - Omega_minus) / (2 * h)

    return -grad


@maxwell_cite(
    396,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="H field measured in cylindrical cavity",
)
def cylindric_cavity_force(
    external_field: np.ndarray,
    magnetization: np.ndarray,
    cavity_length: float,
    cavity_radius: float,
) -> np.ndarray:
    """
    Calculate H field measured inside a cylindrical cavity.

    Art. 396: To measure the magnetic force H inside magnetized matter,
    Maxwell imagines excavating a long narrow cylindrical cavity parallel
    to the magnetization direction. The field inside this cavity equals
    the macroscopic H field.

    For a cavity with length L >> radius a (elongated cylinder):
        H_cavity ≈ H_external - (demagnetizing field)

    The demagnetizing factor for a long cylinder parallel to M is
    approximately zero, so H_cavity ≈ H_external.

    Args:
        external_field: Applied H field (gauss).
        magnetization: Magnetization I of surrounding material (emu/cm³).
        cavity_length: Length of cylindrical cavity (cm).
        cavity_radius: Radius of cylindrical cavity (cm).

    Returns:
        H field inside cavity (gauss).

    Reference:
        Part III, Art. 396: Cylindrical cavity measurement.

    Note:
        This is the standard method for defining H inside magnetic matter.
        The elongated cavity minimizes surface pole effects.
    """
    external_field = np.asarray(external_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    aspect_ratio = (
        cavity_length / (2 * cavity_radius) if cavity_radius > 0 else float("inf")
    )

    # For long cylinder (L >> a), demagnetizing factor N ≈ 0
    # Demagnetizing field H_d = -N * I
    if aspect_ratio > 10:
        # Long cylinder limit — demagnetizing field negligible
        demag_field = np.zeros(3)
    else:
        # Approximate demagnetizing factor for finite cylinder
        # N ≈ 4π * (a/L)² for moderate aspect ratios
        N_approx = (
            4 * np.pi * (cavity_radius / cavity_length) ** 2 if cavity_length > 0 else 0
        )
        demag_field = -N_approx * magnetization

    return external_field + demag_field


@maxwell_cite(
    397,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="H field in general magnetized matter",
)
def general_magnet_force(
    applied_field: np.ndarray,
    magnetization_field: list[MagnetizationVector],
    evaluation_point: np.ndarray,
) -> np.ndarray:
    """
    Calculate H field inside generally magnetized matter.

    Art. 397: The magnetic force at any point in magnetized matter is
    the sum of the applied field and the field due to all magnetic
    poles (both surface and volume distributions).

    H = H_applied + H_poles

    where H_poles is computed from the magnetic charge distribution:
    - Volume pole density: ρ_m = -∇·I
    - Surface pole density: σ_m = I·n

    Args:
        applied_field: External applied H field (gauss).
        magnetization_field: List of MagnetizationVector objects
                           representing the magnetization distribution.
        evaluation_point: Position where H is calculated (cm).

    Returns:
        Total H field (gauss).

    Reference:
        Part III, Art. 397: H in magnetized matter.
    """
    applied_field = np.asarray(applied_field, dtype=np.float64)
    evaluation_point = np.asarray(evaluation_point, dtype=np.float64)

    # Field from magnetization (sum over all volume elements)
    H_from_mag = np.zeros(3)

    for mag_vec in magnetization_field:
        r_vec = evaluation_point - mag_vec.position
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            continue  # Skip self-interaction

        # Treat each volume element as a dipole
        # dH = (3(m·r̂)r̂ - m) / r³ where m = I dV
        # For simplicity, assume unit volume elements
        m = mag_vec.value  # This is I, treat as moment for unit volume

        r_hat = r_vec / r_mag
        m_dot_r = np.dot(m, r_hat)

        dH = (3 * m_dot_r * r_hat - m) / (r_mag**3)
        H_from_mag += dH

    return applied_field + H_from_mag


@maxwell_cite(
    398,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="H field in elongated cylinder/needle cavity limit",
)
def elongated_cylinder_force(
    applied_field: np.ndarray,
    magnetization: np.ndarray,
    axis_direction: np.ndarray,
) -> np.ndarray:
    """
    Calculate H field in the needle cavity limit.

    Art. 398: When the cavity is very elongated (L >> a), forming a
    "needle cavity" parallel to the magnetization, the demagnetizing
    field approaches zero. This gives the true H field:

        H_needle = H_applied (parallel component)
        H_needle = H_applied - 4πI (perpendicular component, limited)

    For a cavity parallel to I:
        H_inside = H_applied (no demagnetizing effect)

    For a cavity perpendicular to I:
        H_inside = H_applied - 4πI (maximum demagnetizing effect)

    Args:
        applied_field: External applied H field (gauss).
        magnetization: Magnetization I of material (emu/cm³).
        axis_direction: Unit vector along cavity axis.

    Returns:
        H field inside needle cavity (gauss).

    Reference:
        Part III, Art. 398: Needle cavity limit.

    Note:
        The needle cavity (L → ∞, a → 0) gives the standard definition
        of H inside magnetic matter.
    """
    applied_field = np.asarray(applied_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)
    axis_direction = np.asarray(axis_direction, dtype=np.float64)

    axis_mag = np.linalg.norm(axis_direction)
    if axis_mag == 0:
        raise ValueError("Axis direction cannot be zero vector")

    axis_direction = axis_direction / axis_mag

    # Decompose magnetization into parallel and perpendicular components
    I_parallel = np.dot(magnetization, axis_direction) * axis_direction
    I_perpendicular = magnetization - I_parallel

    # For needle cavity (infinite aspect ratio):
    # - Parallel component: no demagnetizing (N_parallel = 0)
    # - Perpendicular component: demagnetizing factor N_perp = 2π

    # Demagnetizing field
    H_demag_parallel = np.zeros(3)  # N_parallel = 0
    H_demag_perpendicular = -2 * np.pi * I_perpendicular  # N_perp = 2π for cylinder

    H_demag = H_demag_parallel + H_demag_perpendicular

    return applied_field + H_demag


@maxwell_cite(
    396,
    397,
    398,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="Compare H field in different cavity geometries",
)
def compare_cavity_fields(
    applied_field: np.ndarray,
    magnetization: np.ndarray,
    cavity_aspect_ratio: float,
) -> dict[str, np.ndarray]:
    """
    Compare H field measured in different cavity geometries.

    Art. 396-398: Maxwell shows that the measured field depends on
    cavity shape:

    1. Needle cavity (L >> a, parallel to M): H = H_applied
    2. Disk cavity (a >> L, perpendicular to M): B = H + 4πI
    3. Spherical cavity (L = 2a): Intermediate case

    This function computes H for various aspect ratios.

    Args:
        applied_field: External H field (gauss).
        magnetization: Magnetization I (emu/cm³).
        cavity_aspect_ratio: L/(2a) ratio (1 = sphere, >>1 = needle).

    Returns:
        Dictionary with H fields for different cavity types.

    Reference:
        Part III, Arts. 396-398: Cavity field comparisons.
    """
    applied_field = np.asarray(applied_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    # Decompose into parallel and perpendicular components
    if np.linalg.norm(applied_field) > 0:
        field_direction = applied_field / np.linalg.norm(applied_field)
    else:
        field_direction = np.zeros(3)

    I_parallel = np.dot(magnetization, field_direction) * field_direction
    I_perpendicular = magnetization - I_parallel

    # Demagnetizing factors for different geometries
    if cavity_aspect_ratio >= 10:
        # Needle limit
        N_parallel = 0
        N_perpendicular = 2 * np.pi
    elif cavity_aspect_ratio <= 0.1:
        # Disk limit
        N_parallel = 4 * np.pi
        N_perpendicular = 0
    else:
        # Intermediate (approximate as sphere-like)
        # For sphere: N = 4π/3 for all directions
        t = cavity_aspect_ratio / (cavity_aspect_ratio + 0.1)  # Interpolation factor
        N_parallel = (1 - t) * 4 * np.pi + t * 0
        N_perpendicular = (1 - t) * 0 + t * 2 * np.pi

    # Demagnetizing field
    H_demag = (
        -N_parallel * I_parallel / np.linalg.norm(I_parallel) ** 2 * I_parallel
        if np.linalg.norm(I_parallel) > 0
        else np.zeros(3)
    )
    H_demag += (
        -N_perpendicular
        * I_perpendicular
        / np.linalg.norm(I_perpendicular) ** 2
        * I_perpendicular
        if np.linalg.norm(I_perpendicular) > 0
        else np.zeros(3)
    )

    H_cavity = applied_field + H_demag

    return {
        "H_cavity": H_cavity,
        "H_demag": H_demag,
        "N_parallel": N_parallel,
        "N_perpendicular": N_perpendicular,
        "cavity_type": (
            "needle"
            if cavity_aspect_ratio >= 10
            else ("disk" if cavity_aspect_ratio <= 0.1 else "intermediate")
        ),
    }


@maxwell_cite(
    395,
    part=3,
    chapter="Magnetic Force",
    theory_class="maxwell_original",
    description="Force on magnetic pole in H field",
)
def force_on_magnetic_pole(
    pole_strength: float,
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate force on a magnetic pole in external H field.

    Art. 395: The force on a magnetic pole of strength m in a
    magnetic field H is:

        F = m * H

    This is the defining relation for H — it is the force per
    unit pole strength.

    Args:
        pole_strength: Pole strength m (emu). Positive = N, negative = S.
        H_field: Magnetic field H (gauss).

    Returns:
        Force vector F (dyne).

    Reference:
        Part III, Art. 395: Force on magnetic pole.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    return pole_strength * H_field
