"""
maxwell.components — Magnetic components with analytical solutions.

This subpackage implements analytical solutions for magnetic bodies
of specific shapes from Maxwell's Treatise:
- Spherical magnets (spheres.py, Arts. 431-436)
- Ellipsoidal magnets (ellipsoids.py, Arts. 437-438)

Category: A (maxwell_original) — Maxwell's analytical solutions.
"""

from __future__ import annotations

from maxwell.components.ellipsoids import (
    MagneticEllipsoid,
    OblateSpheroid,
    ProlateSpheroid,
    ellipsoid_demagnetizing_energy,
    ellipsoid_field,
    ellipsoid_induced_magnetization,
    find_easy_axis,
    verify_ellipsoid_magnetism,
)
from maxwell.components.spheres import (
    HollowMagneticSphere,
    MagneticSphere,
    hollow_sphere_in_field,
    sphere_demagnetizing_field,
    sphere_equivalent_dipole,
    sphere_field,
    sphere_induced_magnetization,
    verify_sphere_magnetism,
)

__all__ = [
    # Magnetic Spheres (Arts. 431-436)
    "MagneticSphere",
    "sphere_field",
    "sphere_demagnetizing_field",
    "sphere_equivalent_dipole",
    "sphere_induced_magnetization",
    "HollowMagneticSphere",
    "hollow_sphere_in_field",
    "verify_sphere_magnetism",
    # Magnetic Ellipsoids (Arts. 437-438)
    "MagneticEllipsoid",
    "ProlateSpheroid",
    "OblateSpheroid",
    "ellipsoid_field",
    "ellipsoid_induced_magnetization",
    "ellipsoid_demagnetizing_energy",
    "find_easy_axis",
    "verify_ellipsoid_magnetism",
]
