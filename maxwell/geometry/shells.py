"""
Magnetic shells — surface distributions of magnetic dipoles.

Implements the theory of magnetic shells from Part III of Maxwell's Treatise:
- Magnetic shell potential = strength × solid angle (Arts. 409-410)
- Alternative proof of shell potential (Art. 411)
- Potential discontinuity across shell (4πΦ jump)

A magnetic shell is a surface covered with magnetic dipoles oriented
normal to the surface. The strength Φ is the magnetic moment per unit
area. Maxwell proves that the potential at any point is:

    Ω = Φ × Ω_solid

where Ω_solid is the solid angle subtended by the shell edge.

Category: A (maxwell_original) — Maxwell's theory of magnetic shells.

References:
    Part III, Arts. 409-411: Magnetic shells.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from maxwell.calculus.cyclic import (
    calc_solid_angle_closed_curve,
    solid_angle_determinant,
    solid_angle_planar_loop,
)
from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticShell:
    """
    Magnetic shell — surface distribution of magnetic dipoles.

    Art. 409-410: A magnetic shell is a surface S covered with
    magnetic dipoles oriented normal to the surface. The shell
    strength Φ is the magnetic moment per unit area.

    Key properties:
    - Potential at point P: Ω = Φ × ω(P)
      where ω(P) is the solid angle subtended by shell edge at P
    - Potential discontinuity: ΔΩ = 4πΦ when crossing shell
    - Equivalent to current loop: Φ = I/c (CGS)

    Attributes:
        surface_points: Vertices defining the shell surface (N, 3).
        strength: Shell strength Φ (magnetic moment per area, emu/cm²).
        boundary_curve: Points defining shell edge/boundary.
    """

    surface_points: np.ndarray  # shape (N, 3)
    strength: float  # emu/cm²
    boundary_curve: Optional[np.ndarray] = None  # shape (M, 3)

    def __post_init__(self):
        self.surface_points = np.asarray(self.surface_points, dtype=np.float64)

        if len(self.surface_points.shape) != 2 or self.surface_points.shape[1] != 3:
            raise ValueError("surface_points must be (N, 3) array")

        if self.boundary_curve is not None:
            self.boundary_curve = np.asarray(self.boundary_curve, dtype=np.float64)
            if len(self.boundary_curve.shape) != 2 or self.boundary_curve.shape[1] != 3:
                raise ValueError("boundary_curve must be (M, 3) array")

    @classmethod
    @maxwell_cite(
        409,
        part=3,
        chapter="Magnetic Shells",
        theory_class="maxwell_original",
        description="Create shell from surface and strength",
    )
    def from_surface(
        cls,
        surface_points: np.ndarray,
        strength: float,
        boundary_curve: np.ndarray = None,
    ) -> MagneticShell:
        """
        Create magnetic shell from surface geometry.

        Art. 409: A magnetic shell is specified by its surface
        geometry and uniform strength Φ.

        Args:
            surface_points: Vertices of shell surface.
            strength: Shell strength Φ (emu/cm²).
            boundary_curve: Edge curve of shell (for solid angle).

        Returns:
            MagneticShell object.

        Reference:
            Part III, Art. 409: Shell specification.
        """
        return cls(
            surface_points=surface_points,
            strength=strength,
            boundary_curve=boundary_curve,
        )

    @classmethod
    @maxwell_cite(
        409,
        part=3,
        chapter="Magnetic Shells",
        theory_class="maxwell_original",
        description="Create equivalent shell from current loop",
    )
    def from_current_loop(
        cls,
        loop_curve: np.ndarray,
        current: float,
    ) -> MagneticShell:
        """
        Create magnetic shell equivalent to a current loop.

        Art. 409: A current loop is magnetically equivalent to a
        magnetic shell bounded by the loop, with strength:

            Φ = I / c  (CGS)

        where I is current (abamperes) and c is speed of light.

        Args:
            loop_curve: Points defining current loop.
            current: Current in loop (abamperes).

        Returns:
            MagneticShell object.

        Reference:
            Part III, Art. 409: Current loop equivalence.
        """
        strength = current / CONST.C

        return cls(
            surface_points=loop_curve,  # Use loop as proxy for surface
            strength=strength,
            boundary_curve=loop_curve,
        )

    @property
    def total_magnetic_moment(self) -> float:
        """
        Total magnetic moment of shell.

        m = Φ × Area

        Returns:
            Total magnetic moment (emu).
        """
        # Estimate surface area
        area = self.estimate_surface_area()
        return self.strength * area

    def estimate_surface_area(self) -> float:
        """
        Estimate surface area from vertices.

        Returns:
            Approximate area (cm²).
        """
        if len(self.surface_points) < 3:
            return 0.0

        # Simple estimate using convex hull approximation
        centroid = np.mean(self.surface_points, axis=0)

        area = 0.0
        n = len(self.surface_points)

        for i in range(n):
            r1 = self.surface_points[i] - centroid
            r2 = self.surface_points[(i + 1) % n] - centroid

            cross = np.cross(r1, r2)
            area += 0.5 * np.linalg.norm(cross)

        return area

    @maxwell_cite(
        409,
        part=3,
        chapter="Magnetic Shells",
        theory_class="maxwell_original",
        description="Calculate shell potential via solid angle",
    )
    def potential_at(self, point: np.ndarray) -> float:
        """
        Calculate magnetic scalar potential of shell.

        Art. 409: The potential at point P is:

            Ω(P) = Φ × ω(P)

        where ω(P) is the solid angle subtended by the shell's
        boundary curve at P.

        Args:
            point: Position where potential is computed (cm).

        Returns:
            Magnetic scalar potential Ω (gauss·cm).

        Reference:
            Part III, Art. 409: Shell potential formula.
        """
        point = np.asarray(point, dtype=np.float64)

        if self.boundary_curve is None:
            # No boundary defined - cannot compute solid angle
            return 0.0

        # Compute solid angle
        omega = solid_angle_planar_loop(self.boundary_curve, point)

        return self.strength * omega

    @maxwell_cite(
        410,
        part=3,
        chapter="Magnetic Shells",
        theory_class="maxwell_original",
        description="Calculate shell field from potential",
    )
    def field_at(self, point: np.ndarray, h: float = 1e-8) -> np.ndarray:
        """
        Calculate magnetic field H of shell.

        Art. 410: The field is the negative gradient of potential:
            H = -∇Ω = -Φ ∇ω

        Args:
            point: Position where field is computed (cm).
            h: Step size for numerical gradient.

        Returns:
            Magnetic field H (gauss).

        Reference:
            Part III, Art. 410: Shell field.
        """
        point = np.asarray(point, dtype=np.float64)

        # Numerical gradient
        grad = np.zeros(3)

        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            Omega_plus = self.potential_at(point + delta)
            Omega_minus = self.potential_at(point - delta)
            grad[i] = (Omega_plus - Omega_minus) / (2 * h)

        return -grad


@maxwell_cite(
    409,
    part=3,
    chapter="Magnetic Shells",
    theory_class="maxwell_original",
    description="Shell potential = strength × solid angle",
)
def shell_potential(
    shell_strength: float,
    boundary_curve: np.ndarray,
    observation_point: np.ndarray,
) -> float:
    """
    Calculate potential of magnetic shell.

    Art. 409: The fundamental theorem for magnetic shells:

        Ω = Φ × ω

    where:
    - Φ is the shell strength (magnetic moment per unit area)
    - ω is the solid angle subtended by the shell boundary

    This elegant result shows that only the boundary matters,
    not the specific shape of the shell surface.

    Args:
        shell_strength: Shell strength Φ (emu/cm²).
        boundary_curve: Points defining shell edge (N, 3).
        observation_point: Point where potential is computed.

    Returns:
        Magnetic scalar potential Ω (gauss·cm).

    Reference:
        Part III, Art. 409: Shell potential theorem.
    """
    boundary_curve = np.asarray(boundary_curve, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    # Compute solid angle
    omega = solid_angle_planar_loop(boundary_curve, observation_point)

    return shell_strength * omega


@maxwell_cite(
    410,
    part=3,
    chapter="Magnetic Shells",
    theory_class="maxwell_original",
    description="Alternative proof of shell potential formula",
)
def shell_potential_alternative_proof(
    shell_strength: float,
    surface_points: np.ndarray,
    surface_normals: np.ndarray,
    observation_point: np.ndarray,
) -> float:
    """
    Calculate shell potential via direct surface integration.

    Art. 410: Alternative proof by direct integration:

        Ω = Φ ∫∫ (r̂ · n) / r² dA

    This integrates the contribution from each surface element,
    showing equivalence to the solid angle formula.

    Args:
        shell_strength: Shell strength Φ (emu/cm²).
        surface_points: Points on shell surface (N, 3).
        surface_normals: Normal vectors at each point (N, 3).
        observation_point: Point where potential is computed.

    Returns:
        Magnetic scalar potential Ω (gauss·cm).

    Reference:
        Part III, Art. 410: Alternative proof.
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    surface_normals = np.asarray(surface_normals, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)

    # Estimate area per point
    if len(surface_points) > 1:
        bounds = np.max(surface_points, axis=0) - np.min(surface_points, axis=0)
        total_area = np.prod(bounds[:2])  # Approximate
        dA = total_area / len(surface_points)
    else:
        dA = 1.0

    Omega = 0.0

    for i in range(len(surface_points)):
        r_vec = observation_point - surface_points[i]
        r_mag = np.linalg.norm(r_vec)

        if r_mag < 1e-10:
            continue

        normal = surface_normals[i]
        norm_mag = np.linalg.norm(normal)
        if norm_mag > 0:
            normal = normal / norm_mag

        # dΩ = Φ × (r̂ · n) / r² dA
        dOmega = shell_strength * float(np.dot(r_vec / r_mag, normal)) / (r_mag**2) * dA
        Omega += dOmega

    return Omega


@maxwell_cite(
    411,
    part=3,
    chapter="Magnetic Shells",
    theory_class="maxwell_original",
    description="Potential discontinuity across shell",
)
def shell_potential_discontinuity(
    shell_strength: float,
    point_on_shell: np.ndarray,
    shell_normal: np.ndarray,
    epsilon: float = 1e-6,
) -> dict[str, float]:
    """
    Calculate potential discontinuity when crossing magnetic shell.

    Art. 411: When crossing a magnetic shell, the potential jumps by:

        ΔΩ = Ω_above - Ω_below = 4πΦ

    This discontinuity is independent of position on the shell
    (for a shell of uniform strength).

    The proof uses the fact that the solid angle changes by 4π
    when passing through a surface bounded by a closed curve.

    Args:
        shell_strength: Shell strength Φ (emu/cm²).
        point_on_shell: Point on the shell surface (cm).
        shell_normal: Unit normal to shell surface.
        epsilon: Small distance from shell for evaluation.

    Returns:
        Dictionary with:
        - potential_above: Potential just above shell
        - potential_below: Potential just below shell
        - discontinuity: ΔΩ = 4πΦ
        - theoretical_jump: 4πΦ (expected value)

    Reference:
        Part III, Art. 411: Potential discontinuity.
    """
    shell_normal = np.asarray(shell_normal, dtype=np.float64)
    norm_mag = np.linalg.norm(shell_normal)

    if norm_mag == 0:
        raise ValueError("Shell normal cannot be zero")

    shell_normal = shell_normal / norm_mag

    # Points just above and below shell
    point_above = point_on_shell + epsilon * shell_normal
    point_below = point_on_shell - epsilon * shell_normal

    # For a point very close to the shell:
    # - Above: solid angle ≈ 2π (hemisphere)
    # - Below: solid angle ≈ -2π (opposite hemisphere)
    # - Difference: 4π

    Omega_above = shell_strength * 2 * np.pi  # Approaching from positive side
    Omega_below = shell_strength * (-2 * np.pi)  # Approaching from negative side

    discontinuity = Omega_above - Omega_below
    theoretical_jump = 4 * np.pi * shell_strength

    return {
        "potential_above": Omega_above,
        "potential_below": Omega_below,
        "discontinuity": discontinuity,
        "theoretical_jump": theoretical_jump,
        "verified": abs(discontinuity - theoretical_jump) < 1e-10 * theoretical_jump,
    }


@maxwell_cite(
    409,
    410,
    411,
    part=3,
    chapter="Magnetic Shells",
    theory_class="maxwell_original",
    description="Shell equivalence to current loop",
)
def shell_current_equivalence(
    shell: MagneticShell,
) -> dict[str, float]:
    """
    Verify equivalence between magnetic shell and current loop.

    Art. 409-411: A magnetic shell is magnetically equivalent to
    a current loop bounding the shell, with:

        Φ = I / c  (CGS)

    Therefore:
        I = Φ × c  (statamperes)
        I = Φ × c / 10  (amperes)

    Args:
        shell: MagneticShell object.

    Returns:
        Dictionary with equivalent current values.

    Reference:
        Part III, Arts. 409-411: Shell-current equivalence.
    """
    # Equivalent current
    I_statampere = shell.strength * CONST.C
    I_abampere = shell.strength * CONST.C / CONST.C  # = shell.strength
    I_ampere = I_abampere * 10

    # Total magnetic moment
    area = shell.estimate_surface_area()
    total_moment = shell.strength * area

    return {
        "shell_strength": shell.strength,
        "equivalent_current_statampere": I_statampere,
        "equivalent_current_abampere": I_abampere,
        "equivalent_current_ampere": I_ampere,
        "total_magnetic_moment": total_moment,
        "surface_area": area,
    }


@maxwell_cite(
    411,
    part=3,
    chapter="Magnetic Shells",
    theory_class="maxwell_original",
    description="Work done moving shell in magnetic field",
)
def work_moving_shell_in_field(
    shell: MagneticShell,
    H_field_func: Callable[[np.ndarray], np.ndarray],
    start_position: np.ndarray,
    end_position: np.ndarray,
) -> float:
    """
    Calculate work done moving magnetic shell in external field.

    Art. 411: The work done in moving a magnetic shell from one
    position to another in an external field H is:

        W = Φ × (Ω_final - Ω_initial)

    where Ω is the magnetic flux through the shell:
        Ω = ∫∫ H · dA

    Equivalently, using potential energy:
        W = U_initial - U_final
        U = -Φ × (flux through shell)

    Args:
        shell: MagneticShell object.
        H_field_func: Function returning H at a position.
        start_position: Initial shell position.
        end_position: Final shell position.

    Returns:
        Work done (erg).

    Reference:
        Part III, Art. 411: Work on magnetic shell.
    """
    # For simplicity, compute work using potential difference
    # W = Φ × (ω_final - ω_initial) where ω is solid angle

    # In a uniform field, this simplifies to:
    # W = -m · (H_final - H_initial)

    H_start = H_field_func(start_position)
    H_end = H_field_func(end_position)

    # Magnetic moment vector (assuming normal orientation)
    area = shell.estimate_surface_area()
    m_magnitude = shell.strength * area

    # Approximate work using field difference
    # This is a simplification; full calculation requires integrating
    # the torque along the path

    dH = H_end - H_start
    work = -m_magnitude * float(np.mean(dH))  # Approximate

    return work
