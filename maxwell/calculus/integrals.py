"""
Magnetic integrals — line and surface integrals of magnetic fields.

Implements the integral calculus of magnetism from Part III of Maxwell's Treatise:
- Line integral of magnetic force ∫H·dl (Arts. 401-402)
- Surface integral of magnetic induction ∬B·dA
- Ampère's law and magnetic circulation

Maxwell develops the integral forms of magnetic field equations:
- ∮H·dl = 4πI/c (Ampère's law, CGS)
- ∬B·dA = 0 (Gauss's law for magnetism)

Category: A (maxwell_original) — Maxwell's magnetic integral calculus.

References:
    Part III, Arts. 401-402: Magnetic line and surface integrals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticLineIntegral:
    """
    Line integral of magnetic force along a path.

    Art. 401: The line integral of magnetic force H along a path C is:

        ∫_C H · dl

    This represents the magnetomotive force (MMF) along the path,
    analogous to electromotive force (EMF) for electric fields.

    For a closed loop, this equals the enclosed current times 4π/c
    (Ampère's law in CGS).

    Attributes:
        path: Array of points defining the path (N, 3).
        integral_value: Computed line integral value.
        path_length: Total length of path (cm).
    """

    path: np.ndarray  # shape (N, 3)
    integral_value: float
    path_length: float

    @classmethod
    @maxwell_cite(
        401,
        part=3,
        chapter="Magnetic Integrals",
        theory_class="maxwell_original",
        description="Compute line integral of H field",
    )
    def compute(
        cls,
        H_field_func: Callable[[np.ndarray], np.ndarray],
        path: np.ndarray,
    ) -> MagneticLineIntegral:
        """
        Compute line integral of H field along a path.

        Art. 401: The line integral is computed numerically by
        summing H·dl over small segments of the path.

        Args:
            H_field_func: Function returning H at a position.
            path: Array of points defining the path (N, 3).

        Returns:
            MagneticLineIntegral object.

        Reference:
            Part III, Art. 401: Line integral of H.
        """
        path = np.asarray(path, dtype=np.float64)

        if len(path.shape) != 2 or path.shape[1] != 3:
            raise ValueError("path must be (N, 3) array")

        integral = 0.0
        total_length = 0.0

        for i in range(len(path) - 1):
            dl = path[i + 1] - path[i]
            segment_length = np.linalg.norm(dl)

            if segment_length > 0:
                # Midpoint evaluation
                midpoint = (path[i] + path[i + 1]) / 2
                H_mid = H_field_func(midpoint)

                integral += np.dot(H_mid, dl)
                total_length += segment_length

        return cls(path=path, integral_value=float(integral), path_length=total_length)


@dataclass
class MagneticSurfaceIntegral:
    """
    Surface integral of magnetic induction — magnetic flux.

    Art. 402: The surface integral of magnetic induction B over a
    surface S is the magnetic flux:

        Φ = ∬_S B · dA

    For a closed surface, this integral is always zero (∇·B = 0).

    Attributes:
        surface_points: Vertices defining the surface (N, 3).
        flux: Computed magnetic flux (maxwell).
        surface_area: Area of surface (cm²).
    """

    surface_points: np.ndarray  # shape (N, 3)
    normals: np.ndarray  # shape (N, 3)
    areas: np.ndarray  # shape (N,)
    flux: float
    surface_area: float

    @classmethod
    @maxwell_cite(
        402,
        part=3,
        chapter="Magnetic Integrals",
        theory_class="maxwell_original",
        description="Compute surface integral of B field",
    )
    def compute(
        cls,
        B_field_func: Callable[[np.ndarray], np.ndarray],
        surface_points: np.ndarray,
        normals: np.ndarray,
        element_areas: np.ndarray,
    ) -> MagneticSurfaceIntegral:
        """
        Compute surface integral of B field over a surface.

        Art. 402: The surface integral is computed by summing
        B·n dA over surface elements.

        Args:
            B_field_func: Function returning B at a position.
            surface_points: Centroid positions of surface elements (N, 3).
            normals: Normal vectors for each element (N, 3).
            element_areas: Area of each element (cm²).

        Returns:
            MagneticSurfaceIntegral object.

        Reference:
            Part III, Art. 402: Surface integral of B.
        """
        surface_points = np.asarray(surface_points, dtype=np.float64)
        normals = np.asarray(normals, dtype=np.float64)
        element_areas = np.asarray(element_areas, dtype=np.float64)

        if len(surface_points) != len(normals):
            raise ValueError("Must have normal for each point")
        if len(surface_points) != len(element_areas):
            raise ValueError("Must have area for each point")

        flux = 0.0
        total_area = float(np.sum(element_areas))

        for i in range(len(surface_points)):
            point = surface_points[i]
            normal = normals[i]
            area = element_areas[i]

            # Normalize normal
            norm_mag = np.linalg.norm(normal)
            if norm_mag > 0:
                normal = normal / norm_mag

            B = B_field_func(point)
            flux += float(np.dot(B, normal) * area)

        return cls(
            surface_points=surface_points,
            normals=normals,
            areas=element_areas,
            flux=float(flux),
            surface_area=total_area,
        )


@maxwell_cite(
    401,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="maxwell_original",
    description="Line integral of H force along path",
)
def calc_line_integral_force(
    H_field_func: Callable[[np.ndarray], np.ndarray],
    path: np.ndarray,
) -> float:
    """
    Calculate line integral of magnetic force H along a path.

    Art. 401: The magnetomotive force (MMF) along a path is:

        MMF = ∫_C H · dl

    This is the magnetic analog of electromotive force (EMF).
    For a closed loop, MMF = 4πI/c where I is the enclosed current.

    Args:
        H_field_func: Function returning H at a position.
        path: Array of points defining the path (N, 3).

    Returns:
        Line integral value (gilbert, the CGS unit of MMF).

    Reference:
        Part III, Art. 401: Line integral of magnetic force.
    """
    path = np.asarray(path, dtype=np.float64)

    if len(path.shape) != 2 or path.shape[1] != 3:
        raise ValueError("path must be (N, 3) array")

    integral = 0.0

    for i in range(len(path) - 1):
        dl = path[i + 1] - path[i]
        midpoint = (path[i] + path[i + 1]) / 2
        H_mid = H_field_func(midpoint)
        integral += np.dot(H_mid, dl)

    return float(integral)


@maxwell_cite(
    402,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="maxwell_original",
    description="Surface integral of magnetic induction",
)
def calc_surface_induction(
    B_field_func: Callable[[np.ndarray], np.ndarray],
    surface_points: np.ndarray,
    normals: np.ndarray,
    element_areas: np.ndarray,
) -> float:
    """
    Calculate surface integral of magnetic induction B.

    Art. 402: The magnetic flux through a surface is:

        Φ = ∬_S B · dA

    For a closed surface, Φ = 0 (no magnetic monopoles).

    Args:
        B_field_func: Function returning B at a position.
        surface_points: Centroid positions of surface elements (N, 3).
        normals: Normal vectors for each element (N, 3).
        element_areas: Area of each element (cm²).

    Returns:
        Magnetic flux Φ (maxwell = gauss·cm²).

    Reference:
        Part III, Art. 402: Surface integral of B.
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    normals = np.asarray(normals, dtype=np.float64)
    element_areas = np.asarray(element_areas, dtype=np.float64)

    flux = 0.0

    for i in range(len(surface_points)):
        point = surface_points[i]
        normal = normals[i]
        area = element_areas[i]

        norm_mag = np.linalg.norm(normal)
        if norm_mag > 0:
            normal = normal / norm_mag

        B = B_field_func(point)
        flux += float(np.dot(B, normal) * area)

    return flux


@maxwell_cite(
    401,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="maxwell_original",
    description="Closed loop integral — Ampère's law",
)
def amperes_law_integral(
    H_field_func: Callable[[np.ndarray], np.ndarray],
    closed_loop: np.ndarray,
) -> dict[str, float]:
    """
    Verify Ampère's law for a closed loop.

    Art. 401: For a closed loop C enclosing current I:

        ∮_C H · dl = 4πI/c  (CGS)

    In CGS, c = speed of light ≈ 3×10¹⁰ cm/s.
    The enclosed current I is in esu (statampere·cm).

    Args:
        H_field_func: Function returning H at a position.
        closed_loop: Array of points defining closed path (N, 3).

    Returns:
        Dictionary with:
        - circulation: ∮H·dl value
        - enclosed_current_esu: Inferred current I = circulation * c / 4π
        - enclosed_current_abampere: Inferred current in abamperes (EMU)

    Reference:
        Part III, Art. 401: Ampère's circuital law.
    """
    closed_loop = np.asarray(closed_loop, dtype=np.float64)

    # Ensure loop is closed
    if not np.allclose(closed_loop[0], closed_loop[-1]):
        closed_loop = np.vstack([closed_loop, closed_loop[0]])

    circulation = calc_line_integral_force(H_field_func, closed_loop)

    # Ampère's law: circulation = 4πI/c
    # I = circulation * c / 4π (in esu)
    I_esu = circulation * CONST.C / (4 * np.pi)

    # Convert to abamperes (EMU): 1 abampere = c statampere
    I_abampere = I_esu / CONST.C

    return {
        "circulation": circulation,
        "enclosed_current_esu": I_esu,
        "enclosed_current_abampere": I_abampere,
        "enclosed_current_ampere": I_abampere * 10,  # 1 abampere = 10 ampere
    }


@maxwell_cite(
    402,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="maxwell_original",
    description="Verify zero flux through closed surface",
)
def verify_closed_surface_zero_flux(
    B_field_func: Callable[[np.ndarray], np.ndarray],
    closed_surface_points: np.ndarray,
    closed_surface_normals: np.ndarray,
    closed_surface_areas: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, any]:
    """
    Verify that flux through a closed surface is zero.

    Art. 402: For any closed surface:

        ∯ B · dA = 0

    This is the integral form of ∇·B = 0, expressing the
    non-existence of magnetic monopoles.

    Args:
        B_field_func: Function returning B at a position.
        closed_surface_points: Centroids of surface elements.
        closed_surface_normals: Outward normals for each element.
        closed_surface_areas: Areas of surface elements.
        tolerance: Maximum acceptable deviation from zero.

    Returns:
        Dictionary with:
        - net_flux: Total flux through closed surface
        - is_zero: True if |flux| < tolerance
        - positive_flux: Sum of outward (positive) flux
        - negative_flux: Sum of inward (negative) flux

    Reference:
        Part III, Art. 402: Zero flux through closed surface.
    """
    flux = calc_surface_induction(
        B_field_func,
        closed_surface_points,
        closed_surface_normals,
        closed_surface_areas,
    )

    # Separate positive and negative contributions
    positive_flux = 0.0
    negative_flux = 0.0

    for i in range(len(closed_surface_points)):
        normal = closed_surface_normals[i]
        area = closed_surface_areas[i]
        norm_mag = np.linalg.norm(normal)

        if norm_mag > 0:
            normal = normal / norm_mag

        B = B_field_func(closed_surface_points[i])
        dPhi = float(np.dot(B, normal) * area)

        if dPhi > 0:
            positive_flux += dPhi
        else:
            negative_flux += dPhi

    return {
        "net_flux": flux,
        "is_zero": abs(flux) <= tolerance,
        "positive_flux": positive_flux,
        "negative_flux": negative_flux,
        "flux_balance": (
            abs(negative_flux) / positive_flux if positive_flux > 0 else float("inf")
        ),
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    401,
    402,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="maxwell_original",
    description="Stokes' theorem for magnetic field",
)
def stokes_theorem_magnetic(
    H_field_func: Callable[[np.ndarray], np.ndarray],
    curl_H_func: Callable[[np.ndarray], np.ndarray],
    surface_points: np.ndarray,
    surface_normals: np.ndarray,
    surface_areas: np.ndarray,
    boundary_curve: np.ndarray,
) -> dict[str, float]:
    """
    Verify Stokes' theorem for magnetic field.

    Art. 401-402: Stokes' theorem relates line and surface integrals:

        ∮_C H · dl = ∬_S (∇×H) · dA

    The circulation around a closed curve equals the flux of curl
    through any surface bounded by that curve.

    Args:
        H_field_func: Function returning H at a position.
        curl_H_func: Function returning ∇×H at a position.
        surface_points: Points on surface bounded by curve.
        surface_normals: Normals to surface elements.
        surface_areas: Areas of surface elements.
        boundary_curve: Closed curve bounding the surface.

    Returns:
        Dictionary with:
        - line_integral: ∮H·dl around boundary
        - surface_integral: ∬(∇×H)·dA over surface
        - difference: |line - surface|
        - verified: True if difference < tolerance

    Reference:
        Part III, Arts. 401-402: Stokes' theorem application.
    """
    # Line integral around boundary
    line_integral = calc_line_integral_force(H_field_func, boundary_curve)

    # Surface integral of curl
    curl_flux = calc_surface_induction(
        curl_H_func,
        surface_points,
        surface_normals,
        surface_areas,
    )

    difference = abs(line_integral - curl_flux)
    tolerance = 1e-6 * max(abs(line_integral), abs(curl_flux), 1.0)

    return {
        "line_integral": line_integral,
        "surface_integral": curl_flux,
        "difference": difference,
        "tolerance": tolerance,
        "verified": difference <= tolerance,
    }
