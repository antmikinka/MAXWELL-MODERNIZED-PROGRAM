"""
General Theorems in Electrostatics and Electrical Work & Energy.

This module implements Maxwell's general theorems from Part I:

1. **Green's Theorem & General Theorems** (Arts. 95-102):
   - Green's theorem in three dimensions
   - Green's reciprocity theorem
   - Potential from charge distributions
   - Uniqueness theorem for electrostatic solutions

2. **Electrical Work and Energy** (Arts. 86-94):
   - Electrostatic energy of charge systems
   - Energy density in the electric field
   - Total energy of electrified systems
   - Principle of virtual work for forces

Maxwell's key insight: The energy of an electrified system can be expressed
either in terms of charges and potentials (W = 1/2 * sum(q*V)) or as an
integral over the field energy density (W = integral(E^2/(8*pi))).

CGS-ESU units are used throughout, following Maxwell's conventions:
    - Energy: ergs
    - Electric field: statvolts/cm
    - Potential: statvolts
    - Charge: statcoulombs (esu)
    - Energy density: ergs/cm^3

Category: A (maxwell_original) — Maxwell's general theorems and energy theory.

References:
    Part I, Chapter III: Electrical Work and Energy (Arts. 86-94).
    Part I, Chapter IV: General Theorems in Electrostatics (Arts. 95-102).
"""

from __future__ import annotations

from typing import Callable
import numpy as np
from scipy import integrate

from maxwell.meta.citation import maxwell_cite


# =============================================================================
# GREEN'S THEOREM (Arts. 95-97)
# =============================================================================

@maxwell_cite(
    95, 96, 97,
    part=1, chapter="General Theorems in Electrostatics",
    theory_class="standard_math",
    description="Green's theorem in three dimensions"
)
def greens_theorem(
    U: Callable[[np.ndarray], float],
    V: Callable[[np.ndarray], float],
    volume_bounds: tuple,
    grad_U: Callable[[np.ndarray], np.ndarray] = None,
    grad_V: Callable[[np.ndarray], np.ndarray] = None,
    laplacian_U: Callable[[np.ndarray], float] = None,
    laplacian_V: Callable[[np.ndarray], float] = None,
) -> dict[str, float]:
    """
    Green's theorem in three dimensions.

    Arts. 95-97: Maxwell states Green's theorem, which relates volume
    integrals to surface integrals. For scalar functions U and V:

        integral_V (U * nabla^2 V + grad U . grad V) dV
        = surface_S (U * grad V . n) dS

    where n is the outward unit normal to the surface S bounding V.

    In symmetric form (Green's second identity):

        integral_V (U * nabla^2 V - V * nabla^2 U) dV
        = surface_S (U * grad V - V * grad U) . n dS

    This theorem is fundamental to potential theory and is used to
    derive Green's reciprocity theorem.

    Args:
        U: First scalar function U(x, y, z).
        V: Second scalar function V(x, y, z).
        volume_bounds: Tuple defining integration bounds ((x0, x1), (y0, y1), (z0, z1)).
        grad_U: Function returning gradient of U. If None, computed numerically.
        grad_V: Function returning gradient of V. If None, computed numerically.
        laplacian_U: Function returning Laplacian of U. If None, computed numerically.
        laplacian_V: Function returning Laplacian of V. If None, computed numerically.

    Returns:
        Dictionary with:
        - volume_integral_U_laplacian_V: integral(U * laplacian_V) dV
        - volume_integral_V_laplacian_U: integral(V * laplacian_U) dV
        - volume_integral_grad_dot: integral(grad U . grad V) dV
        - greens_identity: LHS of Green's identity (should equal surface integral)
        - volume_bounds: Input bounds

    References:
        Part I, Art. 95: Statement of Green's theorem.
        Part I, Art. 96: Application to electricity.
        Part I, Art. 97: Extension to infinite domains.

    Example:
        >>> def U(r): return 1.0 / np.linalg.norm(r + 0.1)
        >>> def V(r): return np.sum(r**2)
        >>> bounds = ((0, 1), (0, 1), (0, 1))
        >>> result = greens_theorem(U, V, bounds)
    """

    def numerical_gradient(f: Callable[[np.ndarray], float], r: np.ndarray, h: float = 1e-6) -> np.ndarray:
        """Compute gradient numerically using central differences."""
        grad = np.zeros(3)
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            grad[i] = (f(r + delta) - f(r - delta)) / (2 * h)
        return grad

    def numerical_laplacian(f: Callable[[np.ndarray], float], r: np.ndarray, h: float = 1e-4) -> float:
        """Compute Laplacian numerically."""
        laplacian = 0.0
        for i in range(3):
            delta = np.zeros(3)
            delta[i] = h
            laplacian += (f(r + delta) - 2 * f(r) + f(r - delta)) / (h ** 2)
        return laplacian

    # Use provided gradient functions or compute numerically
    if grad_U is None:
        grad_U = lambda r: numerical_gradient(U, r)
    if grad_V is None:
        grad_V = lambda r: numerical_gradient(V, r)
    if laplacian_U is None:
        laplacian_U = lambda r: numerical_laplacian(U, r)
    if laplacian_V is None:
        laplacian_V = lambda r: numerical_laplacian(V, r)

    # Volume integration integrands
    def integrand_U_laplacian_V(x, y, z):
        r = np.array([x, y, z])
        return U(r) * laplacian_V(r)

    def integrand_V_laplacian_U(x, y, z):
        r = np.array([x, y, z])
        return V(r) * laplacian_U(r)

    def integrand_grad_dot(x, y, z):
        r = np.array([x, y, z])
        return np.dot(grad_U(r), grad_V(r))

    # Perform volume integration
    (x0, x1), (y0, y1), (z0, z1) = volume_bounds

    vol_int_U_lap_V, _ = integrate.tplquad(
        integrand_U_laplacian_V, x0, x1, y0, y1, z0, z1, epsabs=1e-8
    )

    vol_int_V_lap_U, _ = integrate.tplquad(
        integrand_V_laplacian_U, x0, x1, y0, y1, z0, z1, epsabs=1e-8
    )

    vol_int_grad_dot, _ = integrate.tplquad(
        integrand_grad_dot, x0, x1, y0, y1, z0, z1, epsabs=1e-8
    )

    # Green's identity: integral(U * laplacian_V + grad U . grad V) dV
    greens_lhs = vol_int_U_lap_V + vol_int_grad_dot

    return {
        "volume_integral_U_laplacian_V": vol_int_U_lap_V,
        "volume_integral_V_laplacian_U": vol_int_V_lap_U,
        "volume_integral_grad_dot": vol_int_grad_dot,
        "greens_identity_lhs": greens_lhs,
        "volume_bounds": volume_bounds,
    }


# =============================================================================
# GREEN'S RECIPROCITY THEOREM (Arts. 98-99)
# =============================================================================

@maxwell_cite(
    98, 99,
    part=1, chapter="General Theorems in Electrostatics",
    theory_class="maxwell_original",
    description="Green's reciprocity theorem for electrostatics"
)
def greens_reciprocity(
    charges_1: list[tuple[float, np.ndarray]],
    potentials_1: list[float],
    charges_2: list[tuple[float, np.ndarray]],
    potentials_2: list[float],
) -> dict[str, float]:
    """
    Green's reciprocity theorem for electrostatic systems.

    Arts. 98-99: Maxwell's reciprocity theorem states that for two
    different electrified systems with the same conductors:

        sum_i (q1_i * V2_i) = sum_i (q2_i * V1_i)

    where q1_i, V1_i are the charges and potentials in system 1,
    and q2_i, V2_i are the charges and potentials in system 2.

    This theorem is extremely useful for solving electrostatic problems
    by relating known solutions to new configurations.

    Physical interpretation: The work done in assembling system 1 in
    the presence of system 2 equals the work done in assembling
    system 2 in the presence of system 1.

    Args:
        charges_1: List of (charge, position) tuples for system 1.
        potentials_1: List of potentials at each charge position in system 1
                     (due to all other charges in system 1).
        charges_2: List of (charge, position) tuples for system 2.
        potentials_2: List of potentials at each charge position in system 2
                     (due to all other charges in system 2).

    Returns:
        Dictionary with:
        - sum_q1_V2: sum(q1_i * V2_i)
        - sum_q2_V1: sum(q2_i * V1_i)
        - difference: |sum_q1_V2 - sum_q2_V1| (should be ~0)
        - reciprocity_holds: True if difference < tolerance

    References:
        Part I, Art. 98: Statement of reciprocity theorem.
        Part I, Art. 99: Application to coefficient relations.

    Example:
        >>> # System 1: charge q1 at r1, potential V1 at r1
        >>> # System 2: charge q2 at r2, potential V2 at r2
        >>> charges_1 = [(1.0, np.array([0, 0, 0]))]
        >>> potentials_1 = [0.5]  # Potential at origin due to other charges
        >>> charges_2 = [(2.0, np.array([1, 0, 0]))]
        >>> potentials_2 = [0.25]
        >>> result = greens_reciprocity(charges_1, potentials_1, charges_2, potentials_2)
    """
    tol = 1e-10

    # Compute sum(q1_i * V2_i)
    sum_q1_V2 = 0.0
    for i, (q1, pos1) in enumerate(charges_1):
        # V2_i is the potential at pos1 due to system 2
        # For point charges: V2_i = sum_j (q2_j / |pos1 - pos2_j|)
        V2_at_pos1 = 0.0
        for j, (q2, pos2) in enumerate(charges_2):
            r = np.linalg.norm(pos1 - pos2)
            if r > tol:
                V2_at_pos1 += q2 / r
        # Add contribution from specified potential if available
        if i < len(potentials_2):
            V2_at_pos1 += potentials_2[i] if i < len(potentials_2) else 0.0
        sum_q1_V2 += q1 * V2_at_pos1

    # Compute sum(q2_i * V1_i)
    sum_q2_V1 = 0.0
    for i, (q2, pos2) in enumerate(charges_2):
        # V1_i is the potential at pos2 due to system 1
        V1_at_pos2 = 0.0
        for j, (q1, pos1) in enumerate(charges_1):
            r = np.linalg.norm(pos2 - pos1)
            if r > tol:
                V1_at_pos2 += q1 / r
        if i < len(potentials_1):
            V1_at_pos2 += potentials_1[i] if i < len(potentials_1) else 0.0
        sum_q2_V1 += q2 * V1_at_pos2

    difference = abs(sum_q1_V2 - sum_q2_V1)

    return {
        "sum_q1_V2": sum_q1_V2,
        "sum_q2_V1": sum_q2_V1,
        "difference": difference,
        "reciprocity_holds": difference < 1e-6,
    }


# =============================================================================
# POTENTIAL FROM CHARGE DISTRIBUTION (Arts. 100-101)
# =============================================================================

@maxwell_cite(
    100, 101,
    part=1, chapter="General Theorems in Electrostatics",
    theory_class="maxwell_original",
    description="Calculate potential from arbitrary charge distribution"
)
def potential_from_charge_distribution(
    charge_density: Callable[[np.ndarray], float],
    observation_point: np.ndarray,
    integration_bounds: tuple,
    num_points: int = 50,
) -> dict[str, float | np.ndarray]:
    """
    Calculate electric potential from a volume charge distribution.

    Arts. 100-101: The potential at a point P due to a continuous
    charge distribution rho(r') is:

        V(P) = integral(rho(r') / |r - r'|) dV'

    where r is the position of P and r' is the source position.

    In CGS-ESU, this gives the potential in statvolts.

    For numerical computation, the integral is evaluated using
    adaptive quadrature over the specified bounds.

    Args:
        charge_density: Function rho(x, y, z) returning charge density (esu/cm^3).
        observation_point: Position vector r where potential is computed (cm).
        integration_bounds: Tuple ((x0, x1), (y0, y1), (z0, z1)) for integration.
        num_points: Number of evaluation points (default 50).

    Returns:
        Dictionary with:
        - potential: V at observation point (statvolts)
        - observation_point: Position where computed
        - total_charge: Total charge in integration volume (esu)
        - integration_bounds: Input bounds

    References:
        Part I, Art. 100: Potential from continuous charge distribution.
        Part I, Art. 101: Limitations near singularities.

    Example:
        >>> # Uniform sphere of charge
        >>> def rho(r): return 1.0 if np.linalg.norm(r) < 1.0 else 0.0
        >>> V = potential_from_charge_distribution(
        ...     rho, np.array([2, 0, 0]), ((-1, 1), (-1, 1), (-1, 1))
        ... )
    """
    observation_point = np.asarray(observation_point, dtype=np.float64)

    def integrand(x, y, z):
        r_source = np.array([x, y, z])
        r = observation_point - r_source
        distance = np.linalg.norm(r)
        rho_val = charge_density(r_source)
        if distance < 1e-12:
            # Handle singularity (should not occur if observation point outside)
            return 0.0
        return rho_val / distance

    (x0, x1), (y0, y1), (z0, z1) = integration_bounds

    # Compute potential
    potential, error = integrate.tplquad(
        integrand, x0, x1, y0, y1, z0, z1, epsabs=1e-8
    )

    # Compute total charge for reference
    def charge_integrand(x, y, z):
        r_source = np.array([x, y, z])
        return charge_density(r_source)

    total_charge, _ = integrate.tplquad(
        charge_integrand, x0, x1, y0, y1, z0, z1, epsabs=1e-8
    )

    return {
        "potential": potential,
        "observation_point": observation_point,
        "total_charge": total_charge,
        "integration_bounds": integration_bounds,
        "estimated_error": error,
    }


@maxwell_cite(
    100,
    part=1, chapter="General Theorems in Electrostatics",
    theory_class="maxwell_original",
    description="Potential from point charges — discrete sum"
)
def potential_from_point_charges(
    charges: list[tuple[float, np.ndarray]],
    observation_point: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Calculate potential from discrete point charges.

    Art. 100: The potential at point P due to a system of point charges is:

        V(P) = sum_i (q_i / |r - r_i|)

    where q_i is the charge and r_i is the position of charge i.

    This is the discrete version of the continuous integral, applicable
    when charges are localized at points.

    Args:
        charges: List of (charge, position) tuples.
        observation_point: Position vector r where potential is computed (cm).

    Returns:
        Dictionary with:
        - potential: V at observation point (statvolts)
        - observation_point: Position where computed
        - total_charge: Sum of all charges (esu)
        - contributions: List of individual contributions

    References:
        Part I, Art. 100: Potential from discrete charges.

    Example:
        >>> charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
        >>> result = potential_from_point_charges(charges, np.array([0.5, 0, 0]))
    """
    observation_point = np.asarray(observation_point, dtype=np.float64)

    potential = 0.0
    contributions = []

    for q, pos in charges:
        pos = np.asarray(pos, dtype=np.float64)
        r = observation_point - pos
        distance = np.linalg.norm(r)
        if distance > 1e-12:
            contrib = q / distance
            potential += contrib
            contributions.append({"charge": q, "distance": distance, "contribution": contrib})
        else:
            contributions.append({"charge": q, "distance": 0.0, "contribution": float("inf")})

    total_charge = sum(q for q, _ in charges)

    return {
        "potential": potential,
        "observation_point": observation_point,
        "total_charge": total_charge,
        "contributions": contributions,
    }


# =============================================================================
# UNIQUENESS THEOREM (Art. 102)
# =============================================================================

@maxwell_cite(
    102,
    part=1, chapter="General Theorems in Electrostatics",
    theory_class="maxwell_original",
    description="Uniqueness theorem for electrostatic solutions"
)
def uniqueness_theorem(
    potential_1: Callable[[np.ndarray], float],
    potential_2: Callable[[np.ndarray], float],
    boundary_points: np.ndarray,
    volume_points: np.ndarray,
    charge_density: Callable[[np.ndarray], float] = None,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify uniqueness of electrostatic solution.

    Art. 102: Maxwell's uniqueness theorem states that the solution to
    Poisson's equation (or Laplace's equation) is unique given:
        1. The charge distribution rho throughout the volume, AND
        2. The potential V on all boundaries (Dirichlet conditions), OR
        3. The normal derivative dV/dn on all boundaries (Neumann conditions)

    If two solutions V1 and V2 satisfy the same boundary conditions
    and the same charge distribution, then V1 = V2 everywhere.

    This function verifies uniqueness by checking:
        - Boundary condition agreement
        - Laplacian agreement (same charge density)
        - Maximum difference in the volume

    Args:
        potential_1: First potential function V1(x, y, z).
        potential_2: Second potential function V2(x, y, z).
        boundary_points: Array of points on the boundary, shape (N, 3).
        volume_points: Array of points in the volume, shape (M, 3).
        charge_density: Optional rho function. If None, only BCs checked.
        tolerance: Numerical tolerance for comparisons.

    Returns:
        Dictionary with:
        - boundary_match: True if V1 = V2 on all boundary points
        - max_boundary_difference: Maximum |V1 - V2| on boundary
        - volume_match: True if V1 = V2 throughout volume
        - max_volume_difference: Maximum |V1 - V2| in volume
        - solutions_identical: True if both conditions satisfied

    References:
        Part I, Art. 102: Uniqueness of electrostatic solutions.

    Example:
        >>> # Two solutions that should be identical
        >>> def V1(r): return 1.0 / np.linalg.norm(r + 0.1)
        >>> def V2(r): return 1.0 / np.linalg.norm(r + 0.1)
        >>> boundary = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
        >>> volume = np.array([[0.5, 0.5, 0.5]])
        >>> result = uniqueness_theorem(V1, V2, boundary, volume)
    """
    boundary_points = np.asarray(boundary_points, dtype=np.float64)
    volume_points = np.asarray(volume_points, dtype=np.float64)

    # Check boundary conditions
    boundary_diffs = []
    for pt in boundary_points:
        V1_val = potential_1(pt)
        V2_val = potential_2(pt)
        boundary_diffs.append(abs(V1_val - V2_val))

    max_boundary_diff = max(boundary_diffs) if boundary_diffs else 0.0
    boundary_match = max_boundary_diff < tolerance

    # Check volume agreement
    volume_diffs = []
    laplacian_match = True
    max_laplacian_diff = 0.0

    if charge_density is not None:
        h = 1e-4
        for pt in volume_points:
            # Numerical Laplacian
            laplacian_1 = 0.0
            laplacian_2 = 0.0
            for i in range(3):
                delta = np.zeros(3)
                delta[i] = h
                laplacian_1 += (
                    potential_1(pt + delta) - 2 * potential_1(pt) + potential_1(pt - delta)
                ) / (h ** 2)
                laplacian_2 += (
                    potential_2(pt + delta) - 2 * potential_2(pt) + potential_2(pt - delta)
                ) / (h ** 2)

            lap_diff = abs(laplacian_1 - laplacian_2)
            max_laplacian_diff = max(max_laplacian_diff, lap_diff)
            if lap_diff > tolerance:
                laplacian_match = False

            volume_diffs.append(abs(potential_1(pt) - potential_2(pt)))
    else:
        for pt in volume_points:
            volume_diffs.append(abs(potential_1(pt) - potential_2(pt)))

    max_volume_diff = max(volume_diffs) if volume_diffs else 0.0
    volume_match = max_volume_diff < tolerance

    solutions_identical = boundary_match and volume_match

    return {
        "boundary_match": boundary_match,
        "max_boundary_difference": max_boundary_diff,
        "volume_match": volume_match,
        "max_volume_difference": max_volume_diff,
        "laplacian_match": laplacian_match if charge_density is not None else None,
        "max_laplacian_difference": max_laplacian_diff if charge_density is not None else None,
        "solutions_identical": solutions_identical,
    }


# =============================================================================
# ELECTROSTATIC ENERGY (Arts. 86-88)
# =============================================================================

@maxwell_cite(
    86, 87, 88,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Electrostatic energy of a charge system"
)
def electrostatic_energy(
    charges: list[tuple[float, np.ndarray]],
    potentials: list[float] = None,
) -> dict[str, float]:
    """
    Calculate electrostatic potential energy of a system of charges.

    Arts. 86-88: Maxwell defines the potential energy of an electrified
    system as the work done in assembling the charges from infinity.

    For a system of point charges:

        W = (1/2) * sum_i (q_i * V_i)

    where V_i is the potential at charge i due to all OTHER charges
    (not including the self-potential).

    The factor of 1/2 avoids double-counting the pairwise interactions.

    In CGS-ESU, the energy is in ergs.

    Args:
        charges: List of (charge, position) tuples.
        potentials: Optional list of pre-computed potentials at each position.
                   If None, computed from the other charges.

    Returns:
        Dictionary with:
        - energy: Total electrostatic energy (ergs)
        - pairwise_energies: List of (i, j, energy_ij) tuples
        - total_charge: Sum of all charges (esu)

    References:
        Part I, Art. 86: Work required to electrify a body.
        Part I, Art. 87: Potential energy of electrified systems.
        Part I, Art. 88: General expression for energy.

    Example:
        >>> charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
        >>> result = electrostatic_energy(charges)
        >>> print(f"Energy = {result['energy']:.4f} ergs")
    """
    n = len(charges)
    energy = 0.0
    pairwise_energies = []

    # Compute potential at each charge due to all others
    if potentials is None:
        potentials = []
        for i, (q_i, r_i) in enumerate(charges):
            V_i = 0.0
            for j, (q_j, r_j) in enumerate(charges):
                if i != j:
                    r = np.linalg.norm(r_i - r_j)
                    if r > 1e-12:
                        V_i += q_j / r
            potentials.append(V_i)

    # W = (1/2) * sum(q_i * V_i)
    for i, (q_i, r_i) in enumerate(charges):
        energy += 0.5 * q_i * potentials[i]

    # Compute pairwise energies for reference
    for i in range(n):
        for j in range(i + 1, n):
            q_i, r_i = charges[i]
            q_j, r_j = charges[j]
            r_ij = np.linalg.norm(r_i - r_j)
            if r_ij > 1e-12:
                W_ij = q_i * q_j / r_ij
                pairwise_energies.append((i, j, W_ij))

    total_charge = sum(q for q, _ in charges)

    return {
        "energy": energy,
        "pairwise_energies": pairwise_energies,
        "total_charge": total_charge,
        "potentials_used": potentials,
    }


@maxwell_cite(
    86, 87,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Work to assemble charges from infinity"
)
def work_to_assemble_charges(
    charges: list[tuple[float, np.ndarray]],
) -> dict[str, float]:
    """
    Calculate work required to assemble charges from infinity.

    Arts. 86-87: The work done in bringing charges one by one from
    infinity to their final positions equals the potential energy.

    For charges q_1, q_2, ..., q_n brought in sequence:
        W_1 = 0 (first charge, no field)
        W_2 = q_2 * V_1(r_2) = q_2 * q_1 / r_12
        W_3 = q_3 * (V_1(r_3) + V_2(r_3)) = q_3 * (q_1/r_13 + q_2/r_23)
        ...

    Total W = sum of all W_i = (1/2) * sum(q_i * V_i)

    Args:
        charges: List of (charge, position) tuples in assembly order.

    Returns:
        Dictionary with:
        - total_work: Total work done (ergs)
        - step_works: Work done at each step [W_1, W_2, ...]
        - final_energy: Same as total_work (stored energy)

    References:
        Part I, Art. 86: Work to electrify.
        Part I, Art. 87: Energy as stored work.
    """
    n = len(charges)
    total_work = 0.0
    step_works = []

    for i in range(n):
        q_i, r_i = charges[i]
        # Potential at r_i due to already-placed charges
        V_i = 0.0
        for j in range(i):
            q_j, r_j = charges[j]
            r_ij = np.linalg.norm(r_i - r_j)
            if r_ij > 1e-12:
                V_i += q_j / r_ij

        W_i = q_i * V_i
        step_works.append(W_i)
        total_work += W_i

    return {
        "total_work": total_work,
        "step_works": step_works,
        "final_energy": total_work,
        "num_charges": n,
    }


# =============================================================================
# ENERGY DENSITY IN THE FIELD (Arts. 89-90)
# =============================================================================

@maxwell_cite(
    89, 90,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Energy density in the electric field"
)
def energy_density_field(
    electric_field: np.ndarray | Callable[[np.ndarray], np.ndarray],
    position: np.ndarray = None,
    integration_bounds: tuple = None,
    num_points: int = 50,
) -> dict[str, float | np.ndarray]:
    """
    Calculate energy density in the electric field.

    Arts. 89-90: Maxwell showed that the energy of an electrified
    system can be regarded as distributed throughout the field with
    energy density:

        u = E^2 / (8 * pi)  (ergs/cm^3 in CGS-ESU)

    where E is the magnitude of the electric field.

    The total energy is the volume integral:

        W = integral(u dV) = integral(E^2 / (8*pi)) dV

    This function computes either:
        - Local energy density at a point, OR
        - Total field energy in a volume

    Args:
        electric_field: Either a field vector E (shape (3,)) or a function E(r).
        position: Position where field is evaluated (if field is constant).
        integration_bounds: Bounds ((x0,x1), (y0,y1), (z0,z1)) for volume integral.
        num_points: Number of evaluation points for integration.

    Returns:
        Dictionary with:
        - energy_density: u at position (ergs/cm^3) if point evaluation
        - field_magnitude: |E| at position
        - total_energy: Volume integral of u (ergs) if bounds provided
        - integration_bounds: Input bounds

    References:
        Part I, Art. 89: Energy density in the field.
        Part I, Art. 90: Total energy as field integral.

    Example:
        >>> # Point evaluation
        >>> E = np.array([100, 0, 0])
        >>> result = energy_density_field(E)
        >>> print(f"u = {result['energy_density']:.4f} ergs/cm^3")

        >>> # Volume integral
        >>> def E_field(r): return np.array([1.0/np.linalg.norm(r)**2, 0, 0])
        >>> result = energy_density_field(E_field, integration_bounds=...)
    """
    result = {}

    # Handle both vector and function inputs
    if callable(electric_field):
        if position is None:
            raise ValueError("position required when electric_field is a function")
        position = np.asarray(position, dtype=np.float64)
        E_vec = electric_field(position)
    else:
        E_vec = np.asarray(electric_field, dtype=np.float64)
        if position is not None:
            position = np.asarray(position, dtype=np.float64)

    E_mag = np.linalg.norm(E_vec)
    energy_density = (E_mag ** 2) / (8.0 * np.pi)

    result["energy_density"] = energy_density
    result["field_magnitude"] = E_mag
    result["electric_field"] = E_vec
    if position is not None:
        result["position"] = position

    # Volume integral if bounds provided
    if integration_bounds is not None and callable(electric_field):
        def energy_integrand(x, y, z):
            r = np.array([x, y, z])
            E = electric_field(r)
            E_mag = np.linalg.norm(E)
            return (E_mag ** 2) / (8.0 * np.pi)

        (x0, x1), (y0, y1), (z0, z1) = integration_bounds
        total_energy, error = integrate.tplquad(
            energy_integrand, x0, x1, y0, y1, z0, z1, epsabs=1e-8
        )
        result["total_energy"] = total_energy
        result["integration_bounds"] = integration_bounds
        result["estimated_error"] = error

    return result


@maxwell_cite(
    89, 90,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Energy density for uniform electric field"
)
def energy_density_uniform_field(
    field_magnitude: float,
) -> dict[str, float]:
    """
    Energy density for a uniform electric field.

    Arts. 89-90: For a uniform field (such as between parallel plates),
    the energy density is constant throughout the field region:

        u = E^2 / (8 * pi)

    This is useful for capacitors and other uniform-field configurations.

    Args:
        field_magnitude: |E| in statvolts/cm.

    Returns:
        Dictionary with:
        - energy_density: u (ergs/cm^3)
        - field_magnitude: Input E

    References:
        Part I, Art. 89: Energy density formula.
    """
    energy_density = (field_magnitude ** 2) / (8.0 * np.pi)

    return {
        "energy_density": energy_density,
        "field_magnitude": field_magnitude,
    }


# =============================================================================
# ENERGY OF A SYSTEM (Arts. 91-92)
# =============================================================================

@maxwell_cite(
    91, 92,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Total energy of an electrified system"
)
def energy_of_system(
    charges: list[tuple[float, np.ndarray]] = None,
    conductors: list[dict] = None,
    field_func: Callable[[np.ndarray], np.ndarray] = None,
    integration_bounds: tuple = None,
) -> dict[str, float]:
    """
    Calculate total energy of an electrified system.

    Arts. 91-92: The total energy of an electrified system can be
    computed in two equivalent ways:

    Method 1 (Charge-Potential):
        W = (1/2) * sum(q_i * V_i)

    Method 2 (Field Energy):
        W = integral(E^2 / (8*pi)) dV

    Maxwell proved these are equivalent (Arts. 91-92).

    This function supports multiple input formats:
        - Point charges: use 'charges' parameter
        - Conductors with charges/potentials: use 'conductors' parameter
        - Field distribution: use 'field_func' and 'integration_bounds'

    Args:
        charges: List of (charge, position) tuples for point charges.
        conductors: List of dicts with 'charge' and 'potential' keys.
        field_func: Function E(r) for field energy method.
        integration_bounds: Bounds for field energy integral.

    Returns:
        Dictionary with:
        - total_energy: Total energy (ergs)
        - method: Method used ('charge_potential' or 'field_energy')
        - contributions: Breakdown of energy contributions

    References:
        Part I, Art. 91: Energy in terms of charges and potentials.
        Part I, Art. 92: Energy in terms of field intensity.

    Example:
        >>> # Point charges
        >>> charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
        >>> result = energy_of_system(charges=charges)

        >>> # Conductors
        >>> conductors = [{'charge': 10, 'potential': 5}, {'charge': -10, 'potential': 3}]
        >>> result = energy_of_system(conductors=conductors)
    """
    result = {}

    # Method 1: Charge-potential
    if charges is not None:
        energy_result = electrostatic_energy(charges)
        return {
            "total_energy": energy_result["energy"],
            "method": "charge_potential",
            "pairwise_energies": energy_result["pairwise_energies"],
            "total_charge": energy_result["total_charge"],
        }

    # Method 1b: Conductors with known charges and potentials
    if conductors is not None:
        energy = 0.0
        contributions = []
        for cond in conductors:
            q = cond.get("charge", 0)
            V = cond.get("potential", 0)
            W = 0.5 * q * V
            energy += W
            contributions.append({"conductor": cond, "energy": W})
        return {
            "total_energy": energy,
            "method": "conductor_charge_potential",
            "contributions": contributions,
        }

    # Method 2: Field energy
    if field_func is not None and integration_bounds is not None:
        def energy_integrand(x, y, z):
            r = np.array([x, y, z])
            E = field_func(r)
            E_mag = np.linalg.norm(E)
            return (E_mag ** 2) / (8.0 * np.pi)

        (x0, x1), (y0, y1), (z0, z1) = integration_bounds
        total_energy, error = integrate.tplquad(
            energy_integrand, x0, x1, y0, y1, z0, z1, epsabs=1e-8
        )
        return {
            "total_energy": total_energy,
            "method": "field_energy",
            "integration_bounds": integration_bounds,
            "estimated_error": error,
        }

    raise ValueError(
        "Must provide either 'charges', 'conductors', or ('field_func' + 'integration_bounds')"
    )


@maxwell_cite(
    91,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Energy of a system of charged conductors"
)
def energy_of_conductor_system(
    charges: list[float],
    potentials: list[float],
) -> dict[str, float]:
    """
    Calculate energy of a system of charged conductors.

    Art. 91: For a system of conductors with charges q_i and
    potentials V_i, the total energy is:

        W = (1/2) * sum(q_i * V_i)

    This can also be expressed in terms of coefficients of potential
    or coefficients of capacitance.

    Args:
        charges: List of charges on each conductor (esu).
        potentials: List of potentials of each conductor (statvolts).

    Returns:
        Dictionary with:
        - total_energy: Total energy (ergs)
        - conductor_energies: Energy contribution from each conductor
        - total_charge: Sum of all charges
        - average_potential: Charge-weighted average potential

    References:
        Part I, Art. 91: Energy of conductor systems.
    """
    if len(charges) != len(potentials):
        raise ValueError("charges and potentials must have same length")

    energy = 0.0
    conductor_energies = []

    for q, V in zip(charges, potentials):
        W = 0.5 * q * V
        energy += W
        conductor_energies.append(W)

    total_charge = sum(charges)
    avg_potential = sum(q * V for q, V in zip(charges, potentials)) / total_charge if total_charge != 0 else 0

    return {
        "total_energy": energy,
        "conductor_energies": conductor_energies,
        "total_charge": total_charge,
        "average_potential": avg_potential,
        "num_conductors": len(charges),
    }


# =============================================================================
# PRINCIPLE OF VIRTUAL WORK (Arts. 93-94)
# =============================================================================

@maxwell_cite(
    93, 94,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Force from energy derivative — virtual work principle"
)
def virtual_work_principle(
    energy_func: Callable[[float], float],
    coordinate: float,
    delta: float = 1e-6,
) -> dict[str, float]:
    """
    Calculate force from energy derivative using virtual work principle.

    Arts. 93-94: Maxwell's principle of virtual work states that the
    mechanical force (or torque) tending to change a coordinate is
    the negative derivative of the energy with respect to that coordinate:

        F_x = -dW/dx  (force in x direction)

    For a system at constant charge, this gives the mechanical force.
    For a system at constant potential, the force is:

        F_x = +dW/dx  (note the sign change)

    This principle allows calculation of forces between electrified
    bodies without directly computing the field.

    Args:
        energy_func: Function W(x) giving energy as function of coordinate.
        coordinate: Value of coordinate x where force is computed.
        delta: Step size for numerical derivative.

    Returns:
        Dictionary with:
        - force: F = -dW/dx at the coordinate (dynes)
        - energy: W at the coordinate (ergs)
        - energy_derivative: dW/dx (negative of force)
        - coordinate: Input coordinate value

    References:
        Part I, Art. 93: Force at constant charge.
        Part I, Art. 94: Force at constant potential.

    Example:
        >>> # Force between capacitor plates
        >>> def energy(x): return 0.5 * Q**2 / C(x)  # C depends on plate separation x
        >>> result = virtual_work_principle(energy, coordinate=0.01)
    """
    # Compute energy at current position
    energy = energy_func(coordinate)

    # Numerical derivative (central difference for accuracy)
    energy_plus = energy_func(coordinate + delta)
    energy_minus = energy_func(coordinate - delta)
    dW_dx = (energy_plus - energy_minus) / (2 * delta)

    # Force is negative gradient (for constant charge)
    force = -dW_dx

    return {
        "force": force,
        "energy": energy,
        "energy_derivative": dW_dx,
        "coordinate": coordinate,
        "delta": delta,
    }


@maxwell_cite(
    93,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Force between conductors at constant charge"
)
def force_between_conductors_constant_charge(
    charges: list[float],
    potentials_func: Callable[[float], list[float]],
    coordinate: float,
    delta: float = 1e-6,
) -> dict[str, float]:
    """
    Calculate force between conductors at constant charge.

    Art. 93: When charges are held constant, the force tending to
    increase a coordinate x is:

        F = -dW/dx

    where W = (1/2) * sum(q_i * V_i) and V_i depends on x through
    the geometry (coefficients of potential).

    Args:
        charges: Fixed charges on conductors (esu).
        potentials_func: Function V(x) returning list of potentials.
        coordinate: Coordinate value (e.g., separation distance).
        delta: Step size for derivative.

    Returns:
        Dictionary with:
        - force: Mechanical force (dynes)
        - energy: Energy at coordinate (ergs)
        - potentials: Potentials at current coordinate

    References:
        Part I, Art. 93: Force at constant charge.
    """
    potentials = potentials_func(coordinate)
    energy = 0.5 * sum(q * V for q, V in zip(charges, potentials))

    potentials_plus = potentials_func(coordinate + delta)
    potentials_minus = potentials_func(coordinate - delta)

    energy_plus = 0.5 * sum(q * V for q, V in zip(charges, potentials_plus))
    energy_minus = 0.5 * sum(q * V for q, V in zip(charges, potentials_minus))

    dW_dx = (energy_plus - energy_minus) / (2 * delta)
    force = -dW_dx

    return {
        "force": force,
        "energy": energy,
        "potentials": potentials,
        "coordinate": coordinate,
    }


@maxwell_cite(
    94,
    part=1, chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Force between conductors at constant potential"
)
def force_between_conductors_constant_potential(
    potentials: list[float],
    charges_func: Callable[[float], list[float]],
    coordinate: float,
    delta: float = 1e-6,
) -> dict[str, float]:
    """
    Calculate force between conductors at constant potential.

    Art. 94: When potentials are held constant (e.g., connected to
    batteries), the force tending to increase coordinate x is:

        F = +dW/dx

    Note the POSITIVE sign, opposite to constant charge case.

    This is because the batteries do work as the configuration changes,
    and the total energy change includes both mechanical work and
    electrical work from the batteries.

    Args:
        potentials: Fixed potentials on conductors (statvolts).
        charges_func: Function Q(x) returning list of charges.
        coordinate: Coordinate value (e.g., separation distance).
        delta: Step size for derivative.

    Returns:
        Dictionary with:
        - force: Mechanical force (dynes)
        - energy: Energy at coordinate (ergs)
        - charges: Charges at current coordinate

    References:
        Part I, Art. 94: Force at constant potential.
    """
    charges = charges_func(coordinate)
    energy = 0.5 * sum(q * V for q, V in zip(charges, potentials))

    charges_plus = charges_func(coordinate + delta)
    charges_minus = charges_func(coordinate - delta)

    energy_plus = 0.5 * sum(q * V for q, V in zip(charges_plus, potentials))
    energy_minus = 0.5 * sum(q * V for q, V in zip(charges_minus, potentials))

    dW_dx = (energy_plus - energy_minus) / (2 * delta)
    # Note: positive sign for constant potential
    force = dW_dx

    return {
        "force": force,
        "energy": energy,
        "charges": charges,
        "coordinate": coordinate,
    }


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("GENERAL THEOREMS IN ELECTROSTATICS AND ELECTRICAL ENERGY")
    print("Maxwell's Treatise, Part I, Chapters III-IV (Arts. 86-102)")
    print("=" * 70)

    # Test Green's theorem
    print("\n--- Green's Theorem (Arts. 95-97) ---")
    def U(r): return 1.0 / np.linalg.norm(r + 0.1)
    def V(r): return np.sum(r ** 2)
    bounds = ((0.1, 1), (0.1, 1), (0.1, 1))
    result = greens_theorem(U, V, bounds)
    print(f"  Green's identity LHS: {result['greens_identity_lhs']:.6f}")

    # Test Green's reciprocity
    print("\n--- Green's Reciprocity Theorem (Arts. 98-99) ---")
    charges_1 = [(1.0, np.array([0, 0, 0]))]
    potentials_1 = [0.0]
    charges_2 = [(2.0, np.array([1, 0, 0]))]
    potentials_2 = [0.0]
    result = greens_reciprocity(charges_1, potentials_1, charges_2, potentials_2)
    print(f"  sum(q1*V2): {result['sum_q1_V2']:.6f}")
    print(f"  sum(q2*V1): {result['sum_q2_V1']:.6f}")
    print(f"  Reciprocity holds: {result['reciprocity_holds']}")

    # Test potential from point charges
    print("\n--- Potential from Charge Distribution (Arts. 100-101) ---")
    charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
    result = potential_from_point_charges(charges, np.array([0.5, 0, 0]))
    print(f"  Potential at (0.5, 0, 0): {result['potential']:.6f} statV")

    # Test uniqueness theorem
    print("\n--- Uniqueness Theorem (Art. 102) ---")
    def V1(r): return 1.0 / np.linalg.norm(r + 0.1)
    def V2(r): return 1.0 / np.linalg.norm(r + 0.1)
    boundary = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    volume = np.array([[0.5, 0.5, 0.5]])
    result = uniqueness_theorem(V1, V2, boundary, volume)
    print(f"  Solutions identical: {result['solutions_identical']}")

    # Test electrostatic energy
    print("\n--- Electrostatic Energy (Arts. 86-88) ---")
    charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
    result = electrostatic_energy(charges)
    print(f"  Energy: {result['energy']:.6f} ergs")

    # Test work to assemble charges
    print("\n--- Work to Assemble Charges (Arts. 86-87) ---")
    charges = [(1.0, np.array([0, 0, 0])), (2.0, np.array([1, 0, 0])), (3.0, np.array([0, 1, 0]))]
    result = work_to_assemble_charges(charges)
    print(f"  Total work: {result['total_work']:.6f} ergs")
    print(f"  Step works: {[f'{w:.4f}' for w in result['step_works']]}")

    # Test energy density
    print("\n--- Energy Density in Field (Arts. 89-90) ---")
    E = np.array([100.0, 0.0, 0.0])
    result = energy_density_field(E)
    print(f"  E = 100 statV/cm")
    print(f"  Energy density u = {result['energy_density']:.6f} ergs/cm^3")

    # Test uniform field energy density
    print("\n--- Uniform Field Energy Density ---")
    result = energy_density_uniform_field(50.0)
    print(f"  E = 50 statV/cm -> u = {result['energy_density']:.6f} ergs/cm^3")

    # Test energy of system
    print("\n--- Energy of System (Arts. 91-92) ---")
    charges = [(1.0, np.array([0, 0, 0])), (-1.0, np.array([1, 0, 0]))]
    result = energy_of_system(charges=charges)
    print(f"  Method: {result['method']}")
    print(f"  Total energy: {result['total_energy']:.6f} ergs")

    # Test conductor system energy
    print("\n--- Energy of Conductor System ---")
    charges = [10.0, -10.0]
    potentials = [5.0, 3.0]
    result = energy_of_conductor_system(charges, potentials)
    print(f"  Total energy: {result['total_energy']:.6f} ergs")

    # Test virtual work principle
    print("\n--- Virtual Work Principle (Arts. 93-94) ---")
    def energy_func(x):
        # Simple harmonic oscillator energy
        return 0.5 * 100.0 * x ** 2
    result = virtual_work_principle(energy_func, coordinate=0.1)
    print(f"  At x = 0.1: F = {result['force']:.4f} dynes")
    print(f"  Expected: F = -k*x = -100 * 0.1 = -10 dynes")

    # Test force at constant charge
    print("\n--- Force at Constant Charge (Art. 93) ---")
    charges = [1.0, -1.0]
    def potentials_func(x):
        # Two conductors: V1 = q1*C11 + q2*C12, etc.
        # Simplified: V = q / C where C depends on x
        return [1.0 / (x + 0.1), -1.0 / (x + 0.1)]
    result = force_between_conductors_constant_charge(charges, potentials_func, 0.5)
    print(f"  Force at x = 0.5: {result['force']:.4f} dynes")

    # Test force at constant potential
    print("\n--- Force at Constant Potential (Art. 94) ---")
    potentials = [1.0, -1.0]
    def charges_func(x):
        # Q = C * V, C depends on x
        return [(x + 0.1) * 1.0, -(x + 0.1) * 1.0]
    result = force_between_conductors_constant_potential(potentials, charges_func, 0.5)
    print(f"  Force at x = 0.5: {result['force']:.4f} dynes")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)
