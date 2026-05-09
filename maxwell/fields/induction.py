"""
Magnetic induction — the B field and its relation to H.

Implements the theory of magnetic induction from Part III of Maxwell's Treatise:
- Magnetic induction B defined (Art. 399)
- B measured via thin disk cavity perpendicular to magnetization
- Constitutive relation: B = H + 4πI (CGS)

Maxwell introduces magnetic induction B as distinct from magnetic force H.
The two are related by the magnetization I of the material.

In CGS units:
    B = H + 4πI

where:
- B is magnetic induction (gauss, same units as H in CGS)
- H is magnetic force (gauss)
- I is magnetization (emu/cm³, same dimensions as H in CGS)

Category: A (maxwell_original) — Maxwell's theory of magnetic induction.

References:
    Part III, Art. 399: Magnetic induction definition.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.core.moment import MagnetizationVector
from maxwell.fields.force import MagneticForce
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticInduction:
    """
    Magnetic induction — the B field vector at a point.

    Art. 399: The magnetic induction B at a point is related to the
    magnetic force H and magnetization I by:

        B = H + 4πI  (CGS)

    This is the field that would be measured inside a thin disk-shaped
    cavity oriented perpendicular to the magnetization direction.

    Attributes:
        value: B field vector (B_x, B_y, B_z) in gauss.
        position: Position where field is evaluated (cm).
    """

    value: np.ndarray  # shape (3,), gauss
    position: np.ndarray  # shape (3,), cm

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.value.shape != (3,):
            raise ValueError(f"B field must be 3D, got {self.value.shape}")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got {self.position.shape}")

    @property
    def magnitude(self) -> float:
        """Magnitude of B field |B|."""
        return float(np.linalg.norm(self.value))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in direction of B field."""
        mag = self.magnitude
        if mag == 0:
            return np.zeros(3)
        return self.value / mag

    @classmethod
    @maxwell_cite(
        399,
        part=3,
        chapter="Magnetic Induction",
        theory_class="maxwell_original",
        description="Create B from H and I",
    )
    def from_H_and_I(
        cls,
        H_field: np.ndarray,
        magnetization: np.ndarray,
        position: np.ndarray,
    ) -> MagneticInduction:
        """
        Create magnetic induction from H field and magnetization.

        Art. 399: The magnetic induction is the sum of the magnetic
        force and 4π times the magnetization:

            B = H + 4πI

        Args:
            H_field: Magnetic force H (gauss).
            magnetization: Magnetization I (emu/cm³).
            position: Position where B is evaluated (cm).

        Returns:
            MagneticInduction object (B field).

        Reference:
            Part III, Art. 399: B = H + 4πI.
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        magnetization = np.asarray(magnetization, dtype=np.float64)

        # CGS constitutive relation
        B = H_field + 4 * np.pi * magnetization

        return cls(value=B, position=position)

    @classmethod
    @maxwell_cite(
        399,
        part=3,
        chapter="Magnetic Induction",
        theory_class="maxwell_original",
        description="Create B from magnetic flux density",
    )
    def from_flux_density(
        cls,
        flux: float,
        area: float,
        normal_direction: np.ndarray,
        position: np.ndarray,
    ) -> MagneticInduction:
        """
        Create magnetic induction from flux density.

        Art. 399: The magnetic induction can be defined operationally
        as the magnetic flux per unit area:

            B = Φ / A

        Args:
            flux: Magnetic flux Φ (maxwell = gauss·cm²).
            area: Area perpendicular to flux (cm²).
            normal_direction: Unit normal to the area.
            position: Position where B is evaluated (cm).

        Returns:
            MagneticInduction object.

        Reference:
            Part III, Art. 399: Magnetic induction as flux density.
        """
        if area <= 0:
            raise ValueError("Area must be positive")

        normal_direction = np.asarray(normal_direction, dtype=np.float64)
        norm_mag = np.linalg.norm(normal_direction)

        if norm_mag == 0:
            raise ValueError("Normal direction cannot be zero vector")

        normal_direction = normal_direction / norm_mag

        # B magnitude = flux / area
        B_magnitude = flux / area
        B_value = B_magnitude * normal_direction

        return cls(value=B_value, position=position)


@maxwell_cite(
    399,
    part=3,
    chapter="Magnetic Induction",
    theory_class="maxwell_original",
    description="Calculate B from H and I",
)
def calc_magnetic_induction(
    H_field: np.ndarray,
    magnetization: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic induction B from H field and magnetization.

    Art. 399: The constitutive relation in CGS units is:

        B = H + 4πI

    This relates the two magnetic fields:
    - H (magnetic force): Field due to free currents and poles
    - B (magnetic induction): Total magnetic field including material response

    Args:
        H_field: Magnetic force H (gauss).
        magnetization: Magnetization I (emu/cm³).

    Returns:
        Magnetic induction B (gauss).

    Reference:
        Part III, Art. 399: B = H + 4πI.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    return H_field + 4 * np.pi * magnetization


@maxwell_cite(
    399,
    part=3,
    chapter="Magnetic Induction",
    theory_class="maxwell_original",
    description="B field measured via thin disk cavity",
)
def thin_disk_induction(
    external_field: np.ndarray,
    magnetization: np.ndarray,
    disk_normal: np.ndarray,
    disk_thickness: float,
    disk_radius: float,
) -> np.ndarray:
    """
    Calculate B field measured inside a thin disk cavity.

    Art. 399: To measure the magnetic induction B inside magnetized
    matter, Maxwell imagines excavating a thin disk-shaped cavity
    perpendicular to the magnetization direction.

    For a disk cavity with thickness t << radius a:
        - Demagnetizing factor N ≈ 4π (perpendicular to disk)
        - H_disk = H_applied - 4πI (perpendicular component)
        - B_disk = H_disk + 4πI = H_applied + 4πI - 4πI = H_applied (perpendicular)

    Wait — the field measured in a disk cavity is B, not H!
    The surface poles on the disk faces create a field that exactly
    cancels the demagnetizing effect when computing B.

    For a cavity perpendicular to I:
        B_cavity = B_material = H_applied + 4πI

    Args:
        external_field: Applied H field (gauss).
        magnetization: Magnetization I of material (emu/cm³).
        disk_normal: Unit normal vector to disk faces.
        disk_thickness: Thickness of disk cavity (cm).
        disk_radius: Radius of disk cavity (cm).

    Returns:
        B field inside disk cavity (gauss).

    Reference:
        Part III, Art. 399: Disk cavity measurement of B.

    Note:
        The disk cavity (t << a) gives the standard definition of B
        inside magnetic matter. This is complementary to the needle
        cavity which gives H.
    """
    external_field = np.asarray(external_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)
    disk_normal = np.asarray(disk_normal, dtype=np.float64)

    norm_mag = np.linalg.norm(disk_normal)
    if norm_mag == 0:
        raise ValueError("Disk normal cannot be zero vector")

    disk_normal = disk_normal / norm_mag

    # Aspect ratio: t / (2a)
    aspect_ratio = disk_thickness / (2 * disk_radius) if disk_radius > 0 else 0

    # For thin disk (t << a), demagnetizing factor N ≈ 4π along normal
    if aspect_ratio < 0.1:
        # Thin disk limit
        N_along_normal = 4 * np.pi
    else:
        # Intermediate — interpolate
        N_along_normal = 4 * np.pi * (1 - aspect_ratio / (aspect_ratio + 0.1))

    # Decompose magnetization
    I_normal = np.dot(magnetization, disk_normal) * disk_normal
    I_tangential = magnetization - I_normal

    # H inside disk cavity
    # H_disk = H_applied - N * I_normal (demagnetizing field)
    H_disk = (
        external_field
        - N_along_normal * I_normal / np.linalg.norm(I_normal) ** 2 * I_normal
        if np.linalg.norm(I_normal) > 0
        else external_field.copy()
    )

    # B inside disk cavity
    # B_disk = H_disk + 4πI
    # But we want the B that would be measured, which is the same as B in material
    # since the cavity is thin and perpendicular to I

    # Actually, the key insight is:
    # - In the material: B = H_applied + 4πI
    # - In the disk cavity: B_cavity = B_material (no surface poles in cavity)

    # The B field is continuous across the cavity boundary for normal component
    B_cavity = external_field + 4 * np.pi * magnetization

    return B_cavity


@maxwell_cite(
    399,
    part=3,
    chapter="Magnetic Induction",
    theory_class="maxwell_original",
    description="Compare H and B cavity measurements",
)
def compare_H_and_B_measurements(
    applied_field: np.ndarray,
    magnetization: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Compare H and B field measurements using different cavity geometries.

    Art. 399: Maxwell's two cavity definitions:

    1. Needle cavity (long, narrow, parallel to M):
       - Measures H directly
       - H_needle = H_applied (no demagnetizing effect)

    2. Disk cavity (flat, perpendicular to M):
       - Measures B directly
       - B_disk = B_material = H_applied + 4πI

    The difference B - H = 4πI is the contribution from magnetization.

    Args:
        applied_field: Applied H field (gauss).
        magnetization: Magnetization I (emu/cm³).

    Returns:
        Dictionary with:
        - H_needle: H measured in needle cavity
        - B_disk: B measured in disk cavity
        - difference: B - H = 4πI
        - magnetization_contribution: 4πI magnitude

    Reference:
        Part III, Art. 399: H vs B measurement.
    """
    applied_field = np.asarray(applied_field, dtype=np.float64)
    magnetization = np.asarray(magnetization, dtype=np.float64)

    # H in needle cavity (parallel to magnetization)
    H_needle = applied_field.copy()  # No demagnetizing effect

    # B in disk cavity (perpendicular to magnetization)
    B_disk = applied_field + 4 * np.pi * magnetization

    # Difference
    difference = B_disk - H_needle  # = 4πI

    return {
        "H_needle": H_needle,
        "B_disk": B_disk,
        "difference": difference,
        "four_pi_I": 4 * np.pi * magnetization,
        "H_magnitude": float(np.linalg.norm(H_needle)),
        "B_magnitude": float(np.linalg.norm(B_disk)),
        "difference_magnitude": float(np.linalg.norm(difference)),
    }


@maxwell_cite(
    399,
    part=3,
    chapter="Magnetic Induction",
    theory_class="maxwell_original",
    description="Magnetic flux through surface",
)
def magnetic_flux(
    B_field_func: Callable,
    surface_points: np.ndarray,
    surface_normal: np.ndarray,
) -> float:
    """
    Calculate magnetic flux through a surface.

    Art. 399: The magnetic induction B is also called the magnetic
    flux density. The flux through a surface is:

        Φ = ∫∫ B · dA = ∫∫ B · n dA

    For a planar surface with uniform B:
        Φ ≈ B · n × Area

    Args:
        B_field_func: Function returning B at a position.
        surface_points: Vertices of the surface, shape (N, 3).
        surface_normal: Unit normal to the surface.

    Returns:
        Magnetic flux Φ (maxwell = gauss·cm²).

    Reference:
        Part III, Art. 399: Magnetic flux.
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    surface_normal = np.asarray(surface_normal, dtype=np.float64)

    norm_mag = np.linalg.norm(surface_normal)
    if norm_mag == 0:
        raise ValueError("Surface normal cannot be zero")

    surface_normal = surface_normal / norm_mag

    # Approximate centroid
    centroid = np.mean(surface_points, axis=0)
    B_centroid = B_field_func(centroid)

    # Approximate area (simplified — uses bounding box)
    projected = surface_points - np.outer(
        np.dot(surface_points, surface_normal), surface_normal
    )
    ranges = np.max(projected, axis=0) - np.min(projected, axis=0)
    sorted_ranges = np.sort(ranges)
    area = sorted_ranges[-1] * sorted_ranges[-2]  # Product of two largest

    # Flux = B · n × A
    return float(np.dot(B_centroid, surface_normal) * area)
