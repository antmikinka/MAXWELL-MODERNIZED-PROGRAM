"""
Electric potential and potential theory — the scalar field of electrostatics.

Implements the theory of electric potential from Part I:
- Electric potential definition (Art. 70)
- Potential from charge distributions (Arts. 70-73)
- Laplace's equation (Art. 77)
- Poisson's equation (Art. 77)
- Boundary conditions (Arts. 78a-c)
- Conductor equipotential properties (Art. 72)

Category: A (maxwell_original) — Maxwell's theory of electric potential.

References:
    Part I, Chapter II, Arts. 69-73: Potential fundamentals.
    Part I, Chapter II, Art. 77: Poisson's extension of Laplace's equation.
    Part I, Chapter II, Arts. 78a-c: Boundary conditions.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np
from scipy import ndimage
from maxwell.meta.citation import maxwell_cite
from maxwell.core.charge import PointCharge
from maxwell.core.field import ElectricField


@dataclass
class ElectricPotential:
    """
    Electric potential at a point in space.

    Art. 70: The electric potential at a point is the work done in
    bringing a unit positive charge from infinity to that point.

    For a point charge in CGS-ESU:
        V = q / r  (statvolt)

    The potential is related to the electric field by:
        E = -grad(V)

    Attributes:
        value: Potential value (statvolt) at the position.
        position: Position vector (x, y, z) in cm where potential is evaluated.
    """

    value: float
    position: np.ndarray  # shape (3,)

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got shape {self.position.shape}")

    @classmethod
    @maxwell_cite(
        70,
        part=1, chapter="Mathematical Definitions",
        theory_class="maxwell_original",
        description="Electric potential at a point",
    )
    def from_point_charge(cls, charge: PointCharge, point: np.ndarray) -> ElectricPotential:
        """
        Create electric potential due to a point charge at a given position.

        V = q / r  (Art. 70)

        Args:
            charge: PointCharge object with charge q and position.
            point: Position vector (cm) where potential is evaluated.

        Returns:
            ElectricPotential object at the specified point.

        Reference:
            Part I, Art. 70: Electric potential.
        """
        point = np.asarray(point, dtype=np.float64)
        potential_value = charge.potential_at(point)
        return cls(value=potential_value, position=point)

    @classmethod
    @maxwell_cite(
        73,
        part=1, chapter="Mathematical Definitions",
        theory_class="maxwell_original",
        description="Potential from multiple charges — superposition",
    )
    def from_charges(
        cls, charges: list[PointCharge], point: np.ndarray
    ) -> ElectricPotential:
        """
        Calculate resultant potential from multiple point charges.

        Art. 73: The potential of any system is the sum of the potentials
        of its parts (superposition principle).

        V = sum_i (q_i / r_i)

        Args:
            charges: List of PointCharge objects.
            point: Position vector (cm) where potential is evaluated.

        Returns:
            Resultant ElectricPotential at the specified point.

        Reference:
            Part I, Art. 73: Potential due to an electrified system.
        """
        point = np.asarray(point, dtype=np.float64)
        total_potential = sum(c.potential_at(point) for c in charges)
        return cls(value=total_potential, position=point)

    @classmethod
    @maxwell_cite(
        72,
        part=1, chapter="Mathematical Definitions",
        theory_class="maxwell_original",
        description="Conductor is an equipotential volume",
    )
    def conductor_surface(
        cls,
        total_charge: float,
        surface_points: np.ndarray,
        centroid: np.ndarray,
    ) -> ElectricPotential:
        """
        Calculate potential of a charged conductor surface.

        Art. 72: The potential is constant throughout a conductor in
        electrostatic equilibrium. All charge resides on the surface.

        For a spherical conductor: V = Q / R

        Args:
            total_charge: Total charge on conductor (esu).
            surface_points: Points on conductor surface.
            centroid: Center of conductor.

        Returns:
            ElectricPotential (constant over conductor).

        Reference:
            Part I, Art. 72: Potential of all points of a conductor is the same.
        """
        surface_points = np.asarray(surface_points, dtype=np.float64)
        centroid = np.asarray(centroid, dtype=np.float64)

        # Approximate effective radius from surface points
        distances = np.linalg.norm(surface_points - centroid, axis=1)
        effective_radius = np.mean(distances)

        if effective_radius == 0:
            raise ValueError("Effective radius cannot be zero")

        # V = Q / R for spherical approximation
        potential_value = total_charge / effective_radius
        return cls(value=potential_value, position=centroid)


@maxwell_cite(
    77,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Laplace's equation — potential in charge-free region",
)
def laplace_equation(
    potential_grid: np.ndarray,
    grid_spacing: float = 1.0,
) -> np.ndarray:
    """
    Compute the Laplacian of the potential field.

    Art. 77: In regions where there is no charge, the potential satisfies
    Laplace's equation:

        nabla^2 V = 0

    In Cartesian coordinates:
        d^2V/dx^2 + d^2V/dy^2 + d^2V/dz^2 = 0

    Args:
        potential_grid: 3D array of potential values on a grid.
        grid_spacing: Spacing between grid points.

    Returns:
        Laplacian of potential at each grid point.

    Reference:
        Part I, Art. 77: Poisson's extension of Laplace's equation.
    """
    # Use scipy's Laplacian operator
    laplacian = ndimage.laplace(potential_grid) / (grid_spacing ** 2)
    return laplacian


@maxwell_cite(
    77,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Poisson's equation — potential with charge density",
)
def poisson_equation(
    potential_grid: np.ndarray,
    charge_density_grid: np.ndarray,
    grid_spacing: float = 1.0,
) -> np.ndarray:
    """
    Verify Poisson's equation for a potential field with charge distribution.

    Art. 77: Poisson extended Laplace's equation to regions containing charge:

        nabla^2 V = -4 * pi * rho

    where rho is the volume charge density.

    In CGS-ESU, this relates the potential to the charge distribution.

    Args:
        potential_grid: 3D array of potential values on a grid.
        charge_density_grid: 3D array of charge density (esu/cm^3).
        grid_spacing: Spacing between grid points.

    Returns:
        Residual of Poisson's equation (should be ~0 where satisfied).

    Reference:
        Part I, Art. 77: Poisson's extension of Laplace's equation.
    """
    laplacian = laplace_equation(potential_grid, grid_spacing)
    # Poisson: nabla^2 V + 4*pi*rho = 0
    residual = laplacian + 4.0 * np.pi * charge_density_grid
    return residual


@maxwell_cite(
    77,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Solve Poisson's equation for given charge distribution",
)
def solve_poisson(
    charge_density_grid: np.ndarray,
    grid_spacing: float = 1.0,
    boundary_potential: float = 0.0,
    max_iterations: int = 1000,
    tolerance: float = 1e-6,
) -> np.ndarray:
    """
    Solve Poisson's equation using iterative relaxation.

    Uses Gauss-Seidel iteration with successive over-relaxation (SOR)
    to solve:

        nabla^2 V = -4 * pi * rho

    with Dirichlet boundary conditions.

    Args:
        charge_density_grid: 3D array of charge density (esu/cm^3).
        grid_spacing: Spacing between grid points (cm).
        boundary_potential: Fixed potential at boundaries (statvolt).
        max_iterations: Maximum number of iterations.
        tolerance: Convergence tolerance.

    Returns:
        Potential grid satisfying Poisson's equation.

    Reference:
        Part I, Art. 77: Poisson's equation.

    Note:
        This is a numerical solver for boundary value problems.
        Maxwell used analytical methods; this implementation uses
        modern computational techniques.
    """
    nz, ny, nx = charge_density_grid.shape

    # Initialize potential with zeros
    V = np.zeros_like(charge_density_grid)

    # Set boundary conditions
    V[0, :, :] = boundary_potential
    V[-1, :, :] = boundary_potential
    V[:, 0, :] = boundary_potential
    V[:, -1, :] = boundary_potential
    V[:, :, 0] = boundary_potential
    V[:, :, -1] = boundary_potential

    # SOR iteration
    omega = 1.5  # Over-relaxation parameter (1 < omega < 2)
    factor = -4.0 * np.pi * (grid_spacing ** 2)

    for iteration in range(max_iterations):
        max_change = 0.0

        # Update interior points
        for i in range(1, nz - 1):
            for j in range(1, ny - 1):
                for k in range(1, nx - 1):
                    # Five-point stencil (3D: seven-point)
                    neighbor_sum = (
                        V[i+1, j, k] + V[i-1, j, k] +
                        V[i, j+1, k] + V[i, j-1, k] +
                        V[i, j, k+1] + V[i, j, k-1]
                    )

                    # Gauss-Seidel update
                    V_new = (neighbor_sum + factor * charge_density_grid[i, j, k]) / 6.0

                    # SOR acceleration
                    V_old = V[i, j, k]
                    V[i, j, k] = (1 - omega) * V_old + omega * V_new
                    max_change = max(max_change, abs(V[i, j, k] - V_old))

        if max_change < tolerance:
            break

    return V


@maxwell_cite(
    77,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Solve Laplace's equation with boundary conditions",
)
def solve_laplace(
    grid_shape: tuple[int, int, int],
    grid_spacing: float = 1.0,
    boundary_potential: float | np.ndarray = 0.0,
    max_iterations: int = 1000,
    tolerance: float = 1e-6,
) -> np.ndarray:
    """
    Solve Laplace's equation using iterative relaxation.

    Solves:
        nabla^2 V = 0

    with specified boundary conditions.

    Args:
        grid_shape: Shape of the computational grid (nz, ny, nx).
        grid_spacing: Spacing between grid points (cm).
        boundary_potential: Either a scalar for uniform Dirichlet BCs,
                           or a 6-tuple for different values on each face.
        max_iterations: Maximum number of iterations.
        tolerance: Convergence tolerance.

    Returns:
        Potential grid satisfying Laplace's equation.

    Reference:
        Part I, Art. 77: Laplace's equation in charge-free regions.
    """
    nz, ny, nx = grid_shape
    V = np.zeros(grid_shape)

    # Parse boundary conditions
    if isinstance(boundary_potential, (int, float)):
        bc = [boundary_potential] * 6
    else:
        bc = list(boundary_potential)  # [z_min, z_max, y_min, y_max, x_min, x_max]

    # Set boundary conditions
    V[0, :, :] = bc[0]
    V[-1, :, :] = bc[1]
    V[:, 0, :] = bc[2]
    V[:, -1, :] = bc[3]
    V[:, :, 0] = bc[4]
    V[:, :, -1] = bc[5]

    # Jacobi iteration (simpler than SOR, more stable for Laplace)
    for iteration in range(max_iterations):
        V_new = V.copy()
        max_change = 0.0

        for i in range(1, nz - 1):
            for j in range(1, ny - 1):
                for k in range(1, nx - 1):
                    V_new[i, j, k] = (
                        V[i+1, j, k] + V[i-1, j, k] +
                        V[i, j+1, k] + V[i, j-1, k] +
                        V[i, j, k+1] + V[i, j, k-1]
                    ) / 6.0
                    max_change = max(max_change, abs(V_new[i, j, k] - V[i, j, k]))

        V = V_new

        if max_change < tolerance:
            break

    return V


@maxwell_cite(
    78,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Boundary condition — continuity of potential",
)
def boundary_condition_potential(
    potential_inside: float,
    potential_outside: float,
    tolerance: float = 1e-10,
) -> bool:
    """
    Verify continuity of potential across a boundary.

    Art. 78a: The potential is continuous across any surface.
    There is no sudden jump in potential.

    Args:
        potential_inside: Potential just inside the boundary.
        potential_outside: Potential just outside the boundary.
        tolerance: Numerical tolerance for comparison.

    Returns:
        True if potential is continuous within tolerance.

    Reference:
        Part I, Art. 78a: Conditions at an electrified surface (potential).
    """
    return abs(potential_inside - potential_outside) < tolerance


@maxwell_cite(
    78,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Boundary condition — discontinuity of normal field",
)
def boundary_condition_normal_derivative(
    field_normal_inside: float,
    field_normal_outside: float,
    surface_charge_density: float,
    tolerance: float = 1e-10,
) -> bool:
    """
    Verify boundary condition for normal component of electric field.

    Art. 78b: The normal component of the electric field has a
    discontinuity proportional to the surface charge density:

        E_n(outside) - E_n(inside) = 4 * pi * sigma

    where sigma is the surface charge density.

    Args:
        field_normal_inside: Normal component of E just inside.
        field_normal_outside: Normal component of E just outside.
        surface_charge_density: Surface charge density sigma (esu/cm^2).
        tolerance: Numerical tolerance for comparison.

    Returns:
        True if boundary condition is satisfied within tolerance.

    Reference:
        Part I, Art. 78b: Conditions at an electrified surface (normal derivative).
    """
    expected_jump = 4.0 * np.pi * surface_charge_density
    actual_jump = field_normal_outside - field_normal_inside
    return abs(actual_jump - expected_jump) < tolerance


@maxwell_cite(
    78,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Boundary condition — continuity of tangential field",
)
def boundary_condition_tangential(
    field_tangential_inside: np.ndarray,
    field_tangential_outside: np.ndarray,
    tolerance: float = 1e-10,
) -> bool:
    """
    Verify boundary condition for tangential component of electric field.

    Art. 78c: The tangential component of the electric field is
    continuous across any boundary:

        E_t(outside) = E_t(inside)

    This ensures that the line integral of E around a closed loop
    is zero (conservative field).

    Args:
        field_tangential_inside: Tangential component of E just inside.
        field_tangential_outside: Tangential component of E just outside.
        tolerance: Numerical tolerance for comparison.

    Returns:
        True if boundary condition is satisfied within tolerance.

    Reference:
        Part I, Art. 78c: Conditions at an electrified surface (tangential).
    """
    field_tangential_inside = np.asarray(field_tangential_inside)
    field_tangential_outside = np.asarray(field_tangential_outside)
    return np.allclose(field_tangential_inside, field_tangential_outside, atol=tolerance)


@maxwell_cite(
    85,
    part=1, chapter="Electrified Systems in Equilibrium",
    theory_class="maxwell_original",
    description="Energy of an electrified system in terms of potentials",
)
def system_energy(
    charges: list[PointCharge],
    potentials: list[float],
) -> float:
    """
    Calculate the electrostatic energy of a system of charges.

    Art. 85: The potential energy of an electrified system is:

        U = (1/2) * sum_i (q_i * V_i)

    where V_i is the potential at charge i due to all other charges.

    Args:
        charges: List of PointCharge objects.
        potentials: List of potentials at each charge position (due to others).

    Returns:
        Total electrostatic energy (erg).

    Reference:
        Part I, Art. 85: Energy of electrified systems.
    """
    if len(charges) != len(potentials):
        raise ValueError("charges and potentials must have same length")

    energy = 0.0
    for q, V in zip(charges, potentials):
        energy += q * V

    return 0.5 * energy


@maxwell_cite(
    70,
    part=1, chapter="Mathematical Definitions",
    theory_class="standard_math",
    description="Potential difference between two points",
)
def potential_difference(
    potential_a: ElectricPotential,
    potential_b: ElectricPotential,
) -> float:
    """
    Calculate potential difference between two points.

    The potential difference (voltage) is:

        Delta V = V_B - V_A

    This is the work done per unit charge moving from A to B.

    Args:
        potential_a: ElectricPotential at point A.
        potential_b: ElectricPotential at point B.

    Returns:
        Potential difference (statvolt).

    Reference:
        Part I, Art. 70: Electric potential definition.
    """
    return potential_b.value - potential_a.value


@maxwell_cite(
    45,
    part=1, chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Electromotive force as potential difference",
)
def electromotive_force_potential(
    potential_start: float,
    potential_end: float,
) -> float:
    """
    Calculate electromotive force from potential difference.

    Art. 45: The electromotive force between two points is equal to
    the difference of potentials between those points.

    EMF = V_start - V_end

    Args:
        potential_start: Potential at starting point.
        potential_end: Potential at ending point.

    Returns:
        Electromotive force (statvolt).

    Reference:
        Part I, Art. 45: Electromotive force and potential.
    """
    return potential_start - potential_end
