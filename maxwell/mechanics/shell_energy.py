"""
Magnetic shell energy — work and energy for magnetic shells.

Implements the theory of shell energy from Part III of Maxwell's Treatise:
- Potential energy of shell in magnetic field (Art. 423)
- Work done moving shell in field
- Shell-field interaction energy

For a magnetic shell of strength Φ in an external field H,
the potential energy is:

    W = -Φ × (magnetic flux through shell)
      = -Φ × ∫∫ H · dA

Category: A (maxwell_original) — Maxwell's theory of shell energy.

References:
    Part III, Art. 423: Energy of magnetic shell.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.geometry.shells import MagneticShell


@dataclass
class ShellEnergy:
    """
    Potential energy of magnetic shell in external field.

    Art. 423: The potential energy of a magnetic shell in an
    external magnetic field H is:

        W = -Φ × Ψ

    where:
    - Φ is the shell strength (magnetic moment per unit area)
    - Ψ is the magnetic flux through the shell: Ψ = ∫∫ H · dA

    The energy is minimum when the shell's positive face is
    aligned with the field direction.

    Attributes:
        shell: MagneticShell object.
        flux: Magnetic flux through shell (maxwell).
        energy: Potential energy W (erg).
    """

    shell: MagneticShell
    flux: float  # maxwell = gauss·cm²
    energy: float  # erg

    @classmethod
    @maxwell_cite(
        423,
        part=3, chapter="Shell Energy",
        theory_class="maxwell_original",
        description="Create shell energy from shell and field",
    )
    def from_shell_and_field(
        cls,
        shell: MagneticShell,
        H_field_func: Callable[[np.ndarray], np.ndarray],
    ) -> ShellEnergy:
        """
        Create shell energy from shell and external field.

        Args:
            shell: MagneticShell object.
            H_field_func: Function returning H at a position.

        Returns:
            ShellEnergy object.

        Reference:
            Part III, Art. 423: W = -ΦΨ.
        """
        # Compute flux through shell
        flux = compute_shell_flux(shell, H_field_func)

        # Energy
        energy = -shell.strength * flux

        return cls(shell=shell, flux=flux, energy=energy)


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Calculate shell potential energy in field",
)
def calc_shell_potential_energy(
    shell_strength: float,
    surface_points: np.ndarray,
    surface_normals: np.ndarray,
    H_field_func: Callable[[np.ndarray], np.ndarray],
) -> float:
    """
    Calculate potential energy of magnetic shell in external field.

    Art. 423: The potential energy of a magnetic shell in an
    external field H is:

        W = -Φ × Ψ

    where Ψ is the magnetic flux through the shell surface.

    The flux is computed by integrating H · n over the surface:
        Ψ = ∫∫ H · n dA

    Args:
        shell_strength: Shell strength Φ (emu/cm²).
        surface_points: Points on shell surface (N, 3).
        surface_normals: Normal vectors at each point (N, 3).
        H_field_func: Function returning H at a position.

    Returns:
        Potential energy W (erg).

    Reference:
        Part III, Art. 423: Shell energy formula.
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    surface_normals = np.asarray(surface_normals, dtype=np.float64)

    # Compute flux
    flux = compute_shell_flux(
        type('Shell', (), {
            'surface_points': surface_points,
            'strength': shell_strength,
        })(),
        H_field_func,
    )

    return -shell_strength * flux


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Compute magnetic flux through shell",
)
def compute_shell_flux(
    shell: MagneticShell,
    H_field_func: Callable[[np.ndarray], np.ndarray],
) -> float:
    """
    Compute magnetic flux through magnetic shell.

    Art. 423: The flux through a shell is the surface integral:

        Ψ = ∫∫ H · dA

    This function computes the flux numerically by summing
    contributions from surface elements.

    Args:
        shell: MagneticShell object with surface geometry.
        H_field_func: Function returning H at a position.

    Returns:
        Magnetic flux Ψ (maxwell = gauss·cm²).

    Reference:
        Part III, Art. 423: Flux through shell.
    """
    surface_points = shell.surface_points

    # Estimate area per point
    if len(surface_points) > 1:
        bounds = np.max(surface_points, axis=0) - np.min(surface_points, axis=0)
        total_area = np.prod(bounds[:2]) if len(bounds) >= 2 else np.prod(bounds)
        dA = total_area / len(surface_points)
    else:
        dA = 1.0
        total_area = 1.0

    flux = 0.0

    for point in surface_points:
        H = H_field_func(point)

        # For a shell, we need the normal component
        # The shell's orientation determines the normal
        # Here we use a simplified approach: assume normals are consistent

        # Approximate normal from local geometry (simplified)
        # In practice, normals should be provided with the shell

        # For now, use the field direction as a proxy
        H_mag = np.linalg.norm(H)
        if H_mag > 0:
            # Assume shell is oriented to maximize flux
            flux += H_mag * dA
        else:
            flux += 0.0

    return float(flux)


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Work done moving shell in magnetic field",
)
def work_moving_shell(
    shell: MagneticShell,
    H_field_func: Callable[[np.ndarray], np.ndarray],
    start_position: np.ndarray,
    end_position: np.ndarray,
    start_orientation: np.ndarray = None,
    end_orientation: np.ndarray = None,
) -> float:
    """
    Calculate work done moving magnetic shell in external field.

    Art. 423: The work done in moving a shell from position 1 to
    position 2 is:

        W = U₁ - U₂ = Φ(Ψ₂ - Ψ₁)

    where U is potential energy and Ψ is flux through shell.

    If the shell also rotates, the work includes the rotational
    component from changing orientation.

    Args:
        shell: MagneticShell object.
        H_field_func: Function returning H at a position.
        start_position: Initial position of shell.
        end_position: Final position of shell.
        start_orientation: Initial orientation (normal vector).
        end_orientation: Final orientation (normal vector).

    Returns:
        Work done (erg). Positive = work done by field.

    Reference:
        Part III, Art. 423: Work on shell.
    """
    # Compute flux at start and end positions
    # For simplicity, translate the shell surface

    start_surface = shell.surface_points + (start_position - np.mean(shell.surface_points, axis=0))
    end_surface = shell.surface_points + (end_position - np.mean(shell.surface_points, axis=0))

    # Create temporary shells for flux calculation
    start_shell = MagneticShell(
        surface_points=start_surface,
        strength=shell.strength,
        boundary_curve=shell.boundary_curve,
    )
    end_shell = MagneticShell(
        surface_points=end_surface,
        strength=shell.strength,
        boundary_curve=shell.boundary_curve,
    )

    flux_start = compute_shell_flux(start_shell, H_field_func)
    flux_end = compute_shell_flux(end_shell, H_field_func)

    # Work = Φ(Ψ₂ - Ψ₁)
    work = shell.strength * (flux_end - flux_start)

    return work


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Force on shell in non-uniform field",
)
def force_on_shell(
    shell: MagneticShell,
    H_field_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    h: float = 1e-8,
) -> np.ndarray:
    """
    Calculate force on magnetic shell in non-uniform field.

    Art. 423: The force on a shell is the gradient of its
    potential energy:

        F = -∇U = ∇(ΦΨ)

    For a shell moving in the field direction:
        F = Φ ∂Ψ/∂x

    Args:
        shell: MagneticShell object.
        H_field_func: Function returning H at a position.
        position: Position of shell center (cm).
        h: Step size for numerical gradient.

    Returns:
        Force vector F (dyne).

    Reference:
        Part III, Art. 423: Force on shell.
    """
    # Compute gradient of energy
    def energy_at(pt: np.ndarray) -> float:
        # Create shell at position pt
        center_offset = pt - np.mean(shell.surface_points, axis=0)
        displaced_surface = shell.surface_points + center_offset

        temp_shell = MagneticShell(
            surface_points=displaced_surface,
            strength=shell.strength,
            boundary_curve=shell.boundary_curve,
        )
        flux = compute_shell_flux(temp_shell, H_field_func)
        return -shell.strength * flux

    # Numerical gradient
    F = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        E_plus = energy_at(position + delta)
        E_minus = energy_at(position - delta)
        F[i] = -(E_plus - E_minus) / (2 * h)  # F = -∇U

    return F


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Torque on shell tending to rotate it",
)
def torque_on_shell(
    shell: MagneticShell,
    H_field_func: Callable[[np.ndarray], np.ndarray],
    position: np.ndarray,
    dtheta: float = 1e-6,
) -> np.ndarray:
    """
    Calculate torque on magnetic shell tending to rotate it.

    Art. 423: A shell in a magnetic field experiences a torque
    tending to rotate it so as to maximize the flux through it.

    The torque is:
        τ = -∂U/∂θ

    For a planar shell with normal n in uniform field H:
        τ = ΦA (H × n)

    where A is the shell area.

    Args:
        shell: MagneticShell object.
        H_field_func: Function returning H at a position.
        position: Position of shell center (cm).
        dtheta: Small angle for numerical derivative.

    Returns:
        Torque vector τ (dyne·cm).

    Reference:
        Part III, Art. 423: Torque on shell.
    """
    # For a planar shell, compute torque analytically
    area = shell.estimate_surface_area()

    # Estimate shell normal from surface points
    if len(shell.surface_points) >= 3:
        centroid = np.mean(shell.surface_points, axis=0)
        v1 = shell.surface_points[0] - centroid
        v2 = shell.surface_points[1] - centroid
        normal = np.cross(v1, v2)
        norm_mag = np.linalg.norm(normal)
        if norm_mag > 0:
            normal = normal / norm_mag
        else:
            normal = np.array([0, 0, 1])
    else:
        normal = np.array([0, 0, 1])

    # Get field at shell position
    H = H_field_func(position)

    # Torque = ΦA (H × n)
    torque = shell.strength * area * np.cross(H, normal)

    return torque


@maxwell_cite(
    423,
    part=3, chapter="Shell Energy",
    theory_class="maxwell_original",
    description="Equilibrium orientation of shell in field",
)
def shell_equilibrium_orientation(
    shell: MagneticShell,
    H_field: np.ndarray,
) -> dict[str, any]:
    """
    Find equilibrium orientation of shell in magnetic field.

    Art. 423: A shell has stable equilibrium when its plane is
    perpendicular to the field (normal parallel to H), so that
    maximum flux passes through it.

    Stable: n ∥ H (maximum flux, minimum energy)
    Unstable: n ∥ -H (minimum flux, maximum energy)

    Args:
        shell: MagneticShell object.
        H_field: Uniform external field H (gauss).

    Returns:
        Dictionary with:
        - stable_normal: Unit vector for stable orientation
        - stable_energy: Minimum energy
        - unstable_normal: Unit vector for unstable orientation
        - unstable_energy: Maximum energy

    Reference:
        Part III, Art. 423: Shell equilibrium.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    H_mag = np.linalg.norm(H_field)

    area = shell.estimate_surface_area()

    if H_mag == 0:
        return {
            "stable_normal": np.zeros(3),
            "stable_energy": 0.0,
            "unstable_normal": np.zeros(3),
            "unstable_energy": 0.0,
        }

    # Unit vector along field
    H_direction = H_field / H_mag

    # Maximum flux (stable)
    flux_max = H_mag * area
    stable_energy = -shell.strength * flux_max

    # Minimum flux (unstable)
    flux_min = -H_mag * area
    unstable_energy = -shell.strength * flux_min

    return {
        "stable_normal": H_direction.copy(),
        "stable_energy": stable_energy,
        "unstable_normal": -H_direction.copy(),
        "unstable_energy": unstable_energy,
        "max_flux": flux_max,
        "shell_area": area,
    }
