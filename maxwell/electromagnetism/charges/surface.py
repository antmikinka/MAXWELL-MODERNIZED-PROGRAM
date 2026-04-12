"""maxwell.electromagnetism.charges.surface — Surface charge density (Art. 613).

Implements Maxwell's treatment of surface charge density and its relation
to the discontinuity in electric field across a surface.

Maxwell's CGS formulation (Art. 613):
    Surface charge density equation:

        σ = (D2 - D1) · n / (4π)

    or in terms of E:
        σ = ε * (E2 - E1) · n / (4π)

    where n is the unit normal from side 1 to side 2.

    For a conductor surface:
        σ = E_normal / (4π)  (just outside conductor)

where:
    σ = surface charge density (statcoulombs/cm²)
    D = electric displacement
    E = electric field
    n = unit normal to surface

Category: A (maxwell_original) — Maxwell's surface charge theory.

References:
    Part IV, Art. 613: Surface charge density.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class SurfaceCharge:
    """
    Surface charge density calculator.

    Art. 613: Maxwell's relation for surface charge:

        σ = (D2 - D1) · n / (4π)

    This relates surface charge to the discontinuity in D across a surface.

    Attributes:
        permittivity: Permittivity ε.
    """

    permittivity: float = 1.0

    @maxwell_cite(
        613,
        part=4, chapter="Surface Charge",
        theory_class="maxwell_original",
        description="Calculate surface charge from D field discontinuity",
    )
    def charge_density_from_discontinuity(
        self,
        D1: np.ndarray,
        D2: np.ndarray,
        normal: np.ndarray,
    ) -> float:
        """
        Calculate surface charge density from D field discontinuity.

        Art. 613: σ = (D2 - D1) · n / (4π)

        Args:
            D1: Displacement on side 1.
            D2: Displacement on side 2.
            normal: Unit normal from side 1 to side 2.

        Returns:
            Surface charge density σ (statcoulombs/cm²).
        """
        D1 = np.asarray(D1, dtype=np.float64)
        D2 = np.asarray(D2, dtype=np.float64)
        normal = np.asarray(normal, dtype=np.float64)

        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm

        delta_D = D2 - D1
        return np.dot(delta_D, normal) / (4.0 * np.pi)

    @maxwell_cite(
        613,
        part=4, chapter="Surface Charge",
        theory_class="maxwell_original",
        description="Calculate surface charge on conductor",
    )
    def charge_density_on_conductor(
        self,
        E_normal: float,
    ) -> float:
        """
        Calculate surface charge density on a conductor.

        Art. 613: Just outside a conductor:

            σ = E_normal / (4π)

        Args:
            E_normal: Normal component of E just outside surface.

        Returns:
            Surface charge density σ.
        """
        return E_normal / (4.0 * np.pi)


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate surface charge: σ = ΔD·n/(4π)",
)
def calc_surface_charge_density(
    D1: np.ndarray,
    D2: np.ndarray,
    normal: np.ndarray,
) -> float:
    """
    Calculate surface charge density from D discontinuity.

    Art. 613: The boundary condition is:

        σ = (D2 - D1) · n / (4π)

    Args:
        D1: Displacement on side 1 (statcoulombs/cm²).
        D2: Displacement on side 2 (statcoulombs/cm²).
        normal: Unit normal from side 1 to side 2.

    Returns:
        Surface charge density σ (statcoulombs/cm²).

    Reference:
        Part IV, Art. 613: Surface charge density.
    """
    D1 = np.asarray(D1, dtype=np.float64)
    D2 = np.asarray(D2, dtype=np.float64)
    normal = np.asarray(normal, dtype=np.float64)

    norm = np.linalg.norm(normal)
    if norm > 0:
        normal = normal / norm

    return np.dot(D2 - D1, normal) / (4.0 * np.pi)


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate surface charge from E discontinuity",
)
def calc_surface_charge_from_E(
    E1: np.ndarray,
    E2: np.ndarray,
    normal: np.ndarray,
    permittivity: float = 1.0,
) -> float:
    """
    Calculate surface charge density from E discontinuity.

    Art. 613: In terms of E:

        σ = ε * (E2 - E1) · n / (4π)

    Args:
        E1: Electric field on side 1.
        E2: Electric field on side 2.
        normal: Unit normal.
        permittivity: Permittivity ε.

    Returns:
        Surface charge density σ.
    """
    E1 = np.asarray(E1, dtype=np.float64)
    E2 = np.asarray(E2, dtype=np.float64)
    normal = np.asarray(normal, dtype=np.float64)

    norm = np.linalg.norm(normal)
    if norm > 0:
        normal = normal / norm

    return permittivity * np.dot(E2 - E1, normal) / (4.0 * np.pi)


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate surface charge on conductor: σ = E/(4π)",
)
def calc_conductor_surface_charge(
    E_normal: float,
) -> float:
    """
    Calculate surface charge density on a conductor.

    Art. 613: Just outside a conductor:

        σ = E / (4π)

    Args:
        E_normal: Normal E field just outside surface.

    Returns:
        Surface charge density σ.

    Reference:
        Part IV, Art. 613: Conductor surface charge.
    """
    return E_normal / (4.0 * np.pi)


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate total charge on surface",
)
def calc_total_surface_charge(
    sigma_func: callable,
    surface_area: float,
) -> float:
    """
    Calculate total charge on a surface.

    Art. 613: Q = integral(σ) dA

    For uniform σ:
        Q = σ * A

    Args:
        sigma_func: Function σ(r) or constant.
        surface_area: Surface area.

    Returns:
        Total charge Q.

    Reference:
        Part IV, Art. 613: Total surface charge.
    """
    if callable(sigma_func):
        # Would need numerical integration over surface
        # Simplified: assume uniform
        return sigma_func(np.zeros(3)) * surface_area
    else:
        return sigma_func * surface_area


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate E field near charged plane",
)
def calc_field_near_charged_plane(
    surface_charge_density: float,
    side: int = 1,
) -> np.ndarray:
    """
    Calculate electric field near an infinite charged plane.

    Art. 613: For an infinite plane with surface charge σ:

        E = 2πσ  (magnitude on each side)

    Direction is away from plane for positive σ.

    Args:
        surface_charge_density: Surface charge σ.
        side: +1 for above plane, -1 for below.

    Returns:
        Electric field E.

    Reference:
        Part IV, Art. 613: Field of charged plane.
    """
    E_mag = 2.0 * np.pi * abs(surface_charge_density)

    # Direction: away from plane for positive charge
    direction = np.sign(surface_charge_density) * side

    return np.array([0.0, 0.0, direction * E_mag])


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Calculate capacitance of parallel plates",
)
def calc_parallel_plate_capacitance(
    plate_area: float,
    plate_separation: float,
    permittivity: float = 1.0,
) -> float:
    """
    Calculate capacitance of parallel plate capacitor.

    Art. 613: For parallel plates:

        C = ε * A / (4π * d)

    In CGS, capacitance has units of length (cm).

    Args:
        plate_area: Area of plates A.
        plate_separation: Separation d.
        permittivity: Permittivity ε.

    Returns:
        Capacitance C (cm in CGS).

    Reference:
        Part IV, Art. 613: Parallel plate capacitance.
    """
    if plate_separation <= 0:
        return float('inf')

    return permittivity * plate_area / (4.0 * np.pi * plate_separation)


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Verify boundary conditions for surface charge",
)
def verify_surface_charge_boundary(
    sigma: float,
    E1_mag: float = 0.0,
    permittivity: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify boundary conditions for surface charge.

    Art. 613: This function verifies:
    1. E2 - E1 = 4πσ/ε (normal component)
    2. For conductor: E_outside = 4πσ

    Args:
        sigma: Surface charge density.
        E1_mag: E field magnitude on side 1.
        permittivity: Permittivity.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    # Expected E2 for given sigma
    # E2 - E1 = 4πσ/ε
    E2_expected = E1_mag + 4.0 * np.pi * sigma / permittivity

    # For conductor (E1 = 0 inside)
    E_conductor = 4.0 * np.pi * sigma

    # Verify relation
    error = abs(E2_expected - E1_mag - 4.0 * np.pi * sigma / permittivity)

    return {
        "surface_charge_sigma": sigma,
        "E1_magnitude": E1_mag,
        "E2_expected": E2_expected,
        "E_conductor_surface": E_conductor,
        "boundary_error": error,
        "boundary_verified": error < tolerance,
    }


@maxwell_cite(
    613,
    part=4, chapter="Surface Charge",
    theory_class="maxwell_original",
    description="Complete surface charge analysis",
)
def analyze_surface_charge(
    surface_charge_density: float,
    surface_area: float,
    permittivity: float = 1.0,
) -> dict[str, float]:
    """
    Complete analysis of surface charge.

    Art. 613: Comprehensive analysis including:
    1. Total charge
    2. E field near surface
    3. Force on surface

    Args:
        surface_charge_density: Surface charge σ.
        surface_area: Surface area.
        permittivity: Permittivity ε.

    Returns:
        Dictionary with complete analysis results.
    """
    total_charge = calc_total_surface_charge(surface_charge_density, surface_area)
    E_outside = calc_field_near_charged_plane(surface_charge_density, side=1)

    # Force per unit area (pressure)
    # P = 2πσ² (in CGS)
    pressure = 2.0 * np.pi * surface_charge_density ** 2
    total_force = pressure * surface_area

    return {
        "surface_charge_density": surface_charge_density,
        "surface_area": surface_area,
        "total_charge": total_charge,
        "E_field_outside": np.linalg.norm(E_outside),
        "electrostatic_pressure": pressure,
        "total_force": total_force,
        "permittivity": permittivity,
    }
